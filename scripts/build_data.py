#!/usr/bin/env python3
"""Build a normalized Too Jewish episode catalogue from first-party sources."""

from __future__ import annotations

import csv
import datetime as dt
import html as html_lib
import json
import re
import sys
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree as ET

from lxml import html


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ARCHIVE_URL = "https://toojewishradio.com/too_jewish_shows.htm"
RSS_URL = "https://feed.podbean.com/toojewishradio/feed.xml"
PODBEAN_URL = "https://toojewishradio.podbean.com/"
USER_AGENT = "Mozilla/5.0 (compatible; Samuel-Cohon-Archive/1.0; research catalogue)"

DATE_RE = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b")
SPACE_RE = re.compile(r"\s+")
TAG_RE = re.compile(r"<[^>]+>")


TOPIC_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("Holocaust & World War II", ("holocaust", "shoah", "nazi", "world war ii", "ww ii", "auschwitz", "treblinka", "ghetto", "nuremberg", "righteous among")),
    ("Antisemitism & Jewish security", ("antisemit", "anti-semit", "jewish security", "hate crime", "adl", "anti-defamation", "jew hatred")),
    ("Israel & the Middle East", ("israel", "israeli", "jerusalem", "zionis", "gaza", "west bank", "palestin", "middle east", "intifada", "lebanon", "iran", "hamas", "hezbollah", "october 7", "kibbutz")),
    ("Jewish history & memory", ("jewish history", "historian", "archive", "museum", "heritage", "ellis island", "shtetl", "genealog", "sephard", "mizrahi", "yiddish", "ladino", "soviet jew", "ancient jew")),
    ("Religion, Torah & Jewish thought", ("torah", "talmud", "midrash", "kabbal", "rabbi", "jewish thought", "theology", "spiritual", "god", "prayer", "litur", "shabbat", "sabbath", "passover", "pesach", "rosh hashanah", "yom kippur", "hanukkah", "purim", "jewish law", "halakh")),
    ("Jewish movements & institutions", ("reform judaism", "conservative judaism", "orthodox", "reconstructionist", "synagogue", "congregation", "hillel", "chabad", "union for reform", "urj", "rabbinical", "seminary")),
    ("Books & literature", ("author", "novel", "poet", "poetry", "book", "memoir", "biograph", "journalist", "writer", "literature", "playwright", "graphic novel")),
    ("Film, television & theater", ("film", "movie", "television", "tv ", "actor", "actress", "director", "producer", "screenwriter", "documentary", "broadway", "theater", "theatre", "streaming series", "showrunner")),
    ("Music", ("music", "singer", "songwriter", "composer", "cantor", "band", "musician", "recording artist", "opera", "orchestra", "jazz", "violin", "pianist")),
    ("Politics, law & public affairs", ("president", "senator", "congress", "mayor", "governor", "ambassador", "election", "politic", "supreme court", "lawyer", "legal", "civil rights", "free speech", "white house", "diplomat")),
    ("Interfaith & pluralism", ("interfaith", "christian", "muslim", "islam", "imam", "bishop", "church", "catholic", "pluralism", "religious freedom", "tolerance")),
    ("Identity, family & community", ("identity", "family", "parent", "marriage", "wedding", "conversion", "intermarriage", "community", "jewish life", "american jew", "young jew", "lgbt", "gay", "lesbian", "gender")),
    ("Education & youth", ("education", "educator", "student", "school", "campus", "college", "university", "teacher", "youth", "child", "teen", "curriculum")),
    ("Science, health & psychology", ("doctor", "dr.", "professor", "science", "medical", "medicine", "health", "psycholog", "psychiatr", "genetic", "consciousness", "aging", "palliative", "mental health", "neuroscience", "covid")),
    ("Food & everyday culture", ("food", "cook", "cuisine", "chef", "restaurant", "kosher", "wine", "comedy", "comedian", "humor", "sports", "baseball", "basketball")),
    ("Philanthropy & social action", ("philanthrop", "charity", "relief", "social action", "social justice", "nonprofit", "foundation", "humanitarian", "volunteer", "refugee", "poverty")),
]

ROLE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("Author / writer", ("author", "writer", "novelist", "poet", "journalist", "playwright")),
    ("Rabbi / clergy", ("rabbi", "cantor", "imam", "bishop", "reverend", "clergy")),
    ("Scholar / educator", ("professor", "historian", "scholar", "educator", "teacher", "university", "researcher")),
    ("Artist / performer", ("actor", "actress", "singer", "musician", "composer", "comedian", "director", "filmmaker", "artist", "showrunner")),
    ("Public official / diplomat", ("senator", "congress", "ambassador", "mayor", "governor", "diplomat", "minister", "justice")),
    ("Organization leader", ("ceo", "president", "director", "founder", "chair", "executive")),
    ("Health / science professional", ("doctor", "dr.", "psychologist", "psychiatrist", "scientist", "physician", "medical")),
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    return SPACE_RE.sub(" ", html_lib.unescape(value)).strip()


def strip_markup(value: str | None) -> str:
    return clean_text(TAG_RE.sub(" ", value or ""))


def parse_date(value: str) -> dt.date | None:
    match = DATE_RE.search(value)
    if not match:
        return None
    month, day, year = (int(part) for part in match.groups())
    if year < 100:
        year += 2000
    try:
        return dt.date(year, month, day)
    except ValueError:
        return None


def tags_for(text: str) -> list[str]:
    lowered = text.casefold()
    tags = [label for label, needles in TOPIC_RULES if any(needle in lowered for needle in needles)]
    return tags or ["General Jewish life"]


def role_for(text: str) -> str:
    lowered = text.casefold()
    for label, needles in ROLE_RULES:
        if any(needle in lowered for needle in needles):
            return label
    return "Guest / community voice"


def normalize_audio_url(raw_href: str) -> str:
    if raw_href.lower().startswith("file:"):
        path = unquote(urlsplit(raw_href).path)
        return urljoin("https://toojewishradio.com/", path.lstrip("/"))
    return urljoin(ARCHIVE_URL, raw_href)


def parse_official_archive(payload: bytes) -> list[dict]:
    document = html.fromstring(payload, base_url=ARCHIVE_URL)
    records: list[dict] = []
    seen_dates: Counter[str] = Counter()

    for row in document.xpath("//table//tr"):
        cells = row.xpath("./td")
        if len(cells) < 2:
            continue
        date_text = clean_text(cells[0].text_content())
        broadcast_date = parse_date(date_text)
        if not broadcast_date:
            continue
        description = clean_text(cells[1].text_content())
        if not description:
            continue
        links = cells[1].xpath(".//a[@href]")
        audio_link = next((link for link in links if ".mp3" in (link.get("href") or "").lower()), None)
        audio_url = normalize_audio_url(audio_link.get("href")) if audio_link is not None else None
        guest_label = clean_text(audio_link.text_content()) if audio_link is not None else ""
        if not guest_label:
            guest_label = clean_text(re.split(r"[,;:]", description, maxsplit=1)[0])

        iso = broadcast_date.isoformat()
        seen_dates[iso] += 1
        suffix = f"-{seen_dates[iso]}" if seen_dates[iso] > 1 else ""
        topics = tags_for(description)
        records.append(
            {
                "id": f"tj-{iso}{suffix}",
                "broadcast_date": iso,
                "display_date": broadcast_date.strftime("%-m/%-d/%y"),
                "year": broadcast_date.year,
                "guest": guest_label,
                "description": description,
                "guest_role": role_for(description),
                "topics": topics,
                "primary_topic": topics[0],
                "topic_provenance": "deterministic inference from first-party episode description",
                "official_archive_url": ARCHIVE_URL,
                "official_audio_url": audio_url,
                "official_link_state": "listed_direct_audio" if audio_url else "no_audio_link_listed",
                "podbean_url": None,
                "podbean_audio_url": None,
                "podbean_download_url": None,
                "podbean_guid": None,
                "published_at": None,
                "duration": None,
                "review_status": "metadata_normalized",
                "transcript_status": "not_ingested",
                "rights_status": "public_first_party_source; reuse_not_assessed",
                "evidence_boundary": "Catalogue metadata only; no claims attributed without source-text review.",
            }
        )
    records.sort(key=lambda item: (item["broadcast_date"], item["id"]), reverse=True)
    return records


def parse_rss(payload: bytes) -> list[dict]:
    root = ET.fromstring(payload)
    ns = {
        "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        "content": "http://purl.org/rss/1.0/modules/content/",
    }
    items: list[dict] = []
    for item in root.findall("./channel/item"):
        title = clean_text(item.findtext("title"))
        link = clean_text(item.findtext("link"))
        guid = clean_text(item.findtext("guid"))
        pub_date = clean_text(item.findtext("pubDate"))
        duration = clean_text(item.findtext("itunes:duration", namespaces=ns)) or None
        description = strip_markup(item.findtext("description"))
        content = strip_markup(item.findtext("content:encoded", namespaces=ns))
        enclosure = item.find("enclosure")
        audio_url = enclosure.get("url") if enclosure is not None else None
        broadcast_date = parse_date(title) or parse_date(description)
        items.append(
            {
                "title": title,
                "link": link,
                "guid": guid,
                "published_at": pub_date or None,
                "duration": duration,
                "description": content or description,
                "audio_url": audio_url,
                "broadcast_date": broadcast_date.isoformat() if broadcast_date else None,
            }
        )
    return items


def parse_podbean_page(payload: bytes, page_url: str) -> list[dict]:
    document = html.fromstring(payload, base_url=page_url)
    items: list[dict] = []
    for card in document.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " card-body ")]'):
        title_links = card.xpath('.//h3[contains(@class,"card-title")]/a[contains(@href,"/e/")]')
        if not title_links:
            continue
        title_link = title_links[0]
        title = clean_text(title_link.text_content())
        broadcast_date = parse_date(title)
        if not broadcast_date:
            continue
        description_nodes = card.xpath('.//div[contains(@class,"episode-description")]')
        description = clean_text(description_nodes[0].text_content()) if description_nodes else ""
        duration_nodes = card.xpath('.//*[contains(@class,"episode-duration")]')
        duration = clean_text(duration_nodes[0].text_content()) if duration_nodes else None
        download_links = card.xpath('.//a[@title="Download" or contains(@aria-label,"Download")]')
        date_nodes = card.xpath('.//*[contains(@class,"episode-date")]')
        items.append(
            {
                "title": title,
                "link": urljoin(PODBEAN_URL, title_link.get("href")),
                "download_url": urljoin(PODBEAN_URL, download_links[0].get("href")) if download_links else None,
                "description": description,
                "duration": duration,
                "site_published_date": clean_text(date_nodes[0].text_content()) if date_nodes else None,
                "broadcast_date": broadcast_date.isoformat(),
            }
        )
    return items


def scrape_podbean_archive(home_payload: bytes) -> list[dict]:
    text = home_payload.decode("utf-8", errors="replace")
    match = re.search(r'\\"listTotalPage\\":(\d+)', text)
    total_pages = int(match.group(1)) if match else 1
    payloads: dict[int, bytes] = {1: home_payload}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(fetch, f"{PODBEAN_URL}page/{page}/"): page
            for page in range(2, total_pages + 1)
        }
        for future in as_completed(futures):
            page = futures[future]
            payloads[page] = future.result()

    items: list[dict] = []
    for page in range(1, total_pages + 1):
        page_url = PODBEAN_URL if page == 1 else f"{PODBEAN_URL}page/{page}/"
        items.extend(parse_podbean_page(payloads[page], page_url))
    return items


def merge_sources(records: list[dict], rss_items: list[dict], podbean_items: list[dict]) -> dict:
    by_date: dict[str, list[dict]] = {}
    for item in rss_items:
        if item["broadcast_date"]:
            by_date.setdefault(item["broadcast_date"], []).append(item)

    podbean_by_date: dict[str, list[dict]] = {}
    for item in podbean_items:
        podbean_by_date.setdefault(item["broadcast_date"], []).append(item)

    rss_matched = 0
    podbean_matched = 0
    for record in records:
        page_candidates = podbean_by_date.get(record["broadcast_date"], [])
        if page_candidates:
            candidate = page_candidates[0]
            record["podbean_url"] = candidate["link"] or None
            record["podbean_download_url"] = candidate["download_url"] or None
            record["duration"] = candidate["duration"]
            record["published_at"] = candidate["site_published_date"]
            record["review_status"] = "metadata_crosschecked_two_first_party_sources"
            podbean_matched += 1

        rss_candidates = by_date.get(record["broadcast_date"], [])
        if rss_candidates:
            candidate = rss_candidates[0]
            record["podbean_url"] = candidate["link"] or record["podbean_url"]
            record["podbean_audio_url"] = candidate["audio_url"] or None
            record["podbean_guid"] = candidate["guid"] or None
            record["published_at"] = candidate["published_at"] or record["published_at"]
            record["duration"] = candidate["duration"] or record["duration"]
            record["review_status"] = "metadata_crosschecked_two_first_party_sources"
            rss_matched += 1

    return {
        "rss_items": len(rss_items),
        "rss_matches": rss_matched,
        "podbean_items": len(podbean_items),
        "podbean_matches": podbean_matched,
    }


def write_outputs(records: list[dict], rss_stats: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    topic_counts = Counter(tag for record in records for tag in record["topics"])
    year_counts = Counter(record["year"] for record in records)
    role_counts = Counter(record["guest_role"] for record in records)
    stats = {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source_checked_at": dt.date.today().isoformat(),
        "total_records": len(records),
        "date_range": {
            "start": min(record["broadcast_date"] for record in records),
            "end": max(record["broadcast_date"] for record in records),
        },
        "years": len(year_counts),
        "direct_audio_listed": sum(bool(record["official_audio_url"]) for record in records),
        "without_audio_link": sum(not record["official_audio_url"] for record in records),
        "rss_items": rss_stats["rss_items"],
        "rss_matches": rss_stats["rss_matches"],
        "podbean_items": rss_stats["podbean_items"],
        "podbean_matches": rss_stats["podbean_matches"],
        "two_source_records": sum(record["review_status"].endswith("two_first_party_sources") for record in records),
        "transcript_reviewed": 0,
        "topic_counts": dict(topic_counts.most_common()),
        "year_counts": {str(year): year_counts[year] for year in sorted(year_counts)},
        "role_counts": dict(role_counts.most_common()),
        "method": {
            "catalogue_source": ARCHIVE_URL,
            "podcast_source": RSS_URL,
            "topic_method": "Deterministic keyword inference from first-party episode descriptions; topic labels are discovery aids, not source-text findings.",
            "evidence_policy": "Metadata and source-text review remain separate. No episode claim is attributed until audio or transcript review.",
        },
    }

    (DATA_DIR / "episodes.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA_DIR / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fieldnames = [
        "id", "broadcast_date", "year", "guest", "description", "guest_role", "primary_topic",
        "topics", "official_audio_url", "official_link_state", "podbean_url", "podbean_audio_url", "podbean_download_url",
        "duration", "review_status", "transcript_status", "rights_status", "evidence_boundary",
    ]
    with (DATA_DIR / "episodes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["topics"] = " | ".join(record["topics"])
            writer.writerow(row)

    print(json.dumps(stats, ensure_ascii=False, indent=2))


def main() -> int:
    official = fetch(ARCHIVE_URL)
    rss = fetch(RSS_URL)
    podbean_home = fetch(PODBEAN_URL)
    records = parse_official_archive(official)
    rss_items = parse_rss(rss)
    podbean_items = scrape_podbean_archive(podbean_home)
    rss_stats = merge_sources(records, rss_items, podbean_items)
    if len(records) < 500:
        raise RuntimeError(f"Archive parse returned only {len(records)} records; refusing to publish an incomplete catalogue")
    write_outputs(records, rss_stats)
    return 0


if __name__ == "__main__":
    sys.exit(main())
