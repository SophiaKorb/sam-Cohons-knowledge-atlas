#!/usr/bin/env python3
"""Check that the tracked, source-first archive and published-site snapshots agree.

Runs entirely offline. This validates metadata integrity, not audio access,
interpretive accuracy, intellectual-work deduplication, or screen-reader use.
"""
from collections import Counter
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DIST = ROOT / "dist"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_js_array(path: Path, prefix: str, suffix: str):
    data = path.read_text(encoding="utf-8").strip()
    assert data.startswith(prefix) and data.endswith(suffix), f"Unexpected JS bundle: {path}"
    return json.loads(data[len(prefix):-len(suffix)])


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    radio = [
        row for path in sorted((DATA / "episodes-by-year").glob("*.json"))
        for row in load(path)
    ]
    stats = load(DATA / "stats.json")
    writing = load(DATA / "writings" / "beit-simcha-blog.json")["records"]
    standalone = load(DATA / "writings" / "rabbisamcohon-blog.json")
    if isinstance(standalone, dict):
        standalone = standalone["records"]
    wstats = load(DATA / "writings" / "stats.json")
    sources = load(DATA / "writings" / "sources.json")["sources"]
    teaching = load(DATA / "teaching" / "beit-simcha-audiocasts.json")
    if isinstance(teaching, dict):
        teaching = teaching["records"]

    require(len(radio) == stats["total_records"], "Radio source count mismatch")
    require(len({r["id"] for r in radio}) == len(radio), "Radio IDs not unique")
    require(dict(Counter(str(r["year"]) for r in radio)) == stats["year_counts"], "Year counts mismatch")
    require(dict(Counter(r["official_link_status"] for r in radio)) == stats["link_status_counts"], "Link-status counts mismatch")
    require(sum(stats["role_counts"].values()) == len(radio), "Radio role counts mismatch")
    require(all(r["transcript_status"] == "not_ingested" for r in radio), "Unexpected transcript-review claim")
    require(len(writing) == wstats["beit_simcha_blog_records"], "Writing source count mismatch")
    require(len(standalone) == wstats["standalone_blog_records"], "Standalone source count mismatch")
    require(len(writing) + len(standalone) == wstats["source_records_total"], "Writing totals mismatch")
    require(len({r["url"] for r in writing}) == len(writing), "Blog canonical URLs not unique")
    require(len(teaching) == 26, "Unexpected teaching listing count")
    community = load(DATA / "writings" / "community-publications.json")["records"]
    historical = load(DATA / "teaching" / "historical-source-leads.json")["records"]
    require(len({r["url"] for r in community}) == len(community), "Community source URLs not unique")
    require(len(community) >= 17, "Historical community excerpt records missing")
    require(len({r["id"] for r in historical}) == len(historical), "Historical audio-lead IDs not unique")
    require(any(r["id"] == "TE-2013-PODCAST-LEAD" and
                r["media_recovery_status"] == "no_audio_binary_or_specific_class_episode_recovered"
                for r in historical), "Unverified historical podcast lead misrepresented")
    for excerpt_title in ("Baking Holiness", "The Necessary Chutzpah of Saving Refugees"):
        relevant = [r for r in community if excerpt_title in r["title"]]
        require(len(relevant) == 1 and relevant[0]["full_text_ingested"] is False,
                f"Historical excerpt must not be treated as full manuscript: {excerpt_title}")
    latest_episodes = {r["broadcast_date"]: r for r in radio}
    for date in ("2026-09-27", "2026-10-04"):
        episode = latest_episodes[date]
        require(episode.get("podbean_download_url", "").startswith("https://www.podbean.com/media/share/"),
                f"Missing first-party download href for {date}")
        require("not checked" in episode.get("podbean_download_evidence", ""),
                f"Do not mark unverified Podbean MP3 as downloaded: {date}")
    require(latest_episodes["2026-09-27"]["official_link_status"] == "live" and
            latest_episodes["2026-09-27"]["official_http_status"] == 200 and
            latest_episodes["2026-09-27"]["official_link_checked_at"] == "2026-10-15T04:41:40+00:00",
            "September 27 verified official HEAD status missing")
    proof = load(DATA / "verification" / "too-jewish-2026-09-27-head-2026-10-15.json")
    require(proof["episode_id"] == "tj-2026-09-27" and
            proof["observations"][-1]["content_type"] == "audio/mpeg" and
            proof["observations"][-1]["redirect_count"] == 0 and
            proof["observations"][-1]["http_status"] == 200,
            "Targeted publisher HEAD evidence missing or inconsistent")
    require(proof["audio_bytes_downloaded"] is False and proof["transcribed"] is False,
            "HTTP link validation misrepresented as speech-to-text completion")
    require(stats["link_checked_at"] == "2026-09-22T04:38:34+00:00",
            "Full corpus HEAD timestamp must remain historical")
    require(stats["link_status_counts"].get("not_checked", 0) == 0 and
            stats["link_status_counts"]["live"] == 890,
            "Targeted HEAD count reconciliation mismatch")
    require(latest_episodes["2026-10-04"]["official_link_status"] == "not_listed",
            "October 4 official audio listing remains unverified")
    require(sum([len(radio), len(writing), len(standalone), len(teaching)]) == 1605, "Corpus total mismatch")

    lookup = {r["url"]: r for r in writing}
    older = "https://beitsimchatucson.org/blog/finding-gratitude"
    newer = "https://beitsimchatucson.org/blog/finding-gratitude-1"
    require(older in lookup and newer in lookup, "Both Gratitude editions required")
    require(lookup[older]["published_date"] == "2024-10-29", "Historical edition date lost")
    require(lookup[newer]["published_date"] == "2026-09-30", "New edition date missing")
    require(lookup[older]["related_source_url"] == newer, "Old edition relation missing")
    require(lookup[newer]["related_source_url"] == older, "New edition relation missing")
    edition_status = "near_verbatim_republication_calendar_updated_full_body_verified_2026-10-13"
    require(all(lookup[u].get("relation_status") == edition_status for u in (older, newer)),
            "Finding Gratitude edition evidence missing in source records")
    dedupe = load(DATA / "writings" / "dedupe-candidates.json")
    require(dedupe["confirmed_redundant_source_records_minimum"] ==
            wstats["confirmed_redundant_source_records_minimum"], "Dedupe count mismatch")
    require(wstats["conservative_distinct_work_upper_bound"] ==
            wstats["source_records_total"] - wstats["confirmed_redundant_source_records_minimum"],
            "Dedupe arithmetic mismatch")
    require(dedupe["conservative_distinct_work_upper_bound_from_316"] ==
            wstats["conservative_distinct_work_upper_bound"], "Dedupe ledger upper bound mismatch")

    registry = {entry["name"]: entry for entry in sources}
    require(registry["Congregation Beit Simcha Rabbi's Blog"]["records"] == len(writing), "Source registry mismatch")
    require(registry["Too Jewish Radio official archive"]["records"] == len(radio) - 1, "Podbean-only episode needs separate provenance")

    meta = read_js_array(DIST / "data-meta.js", "window.__COHON_META__=", ";")
    require(meta["stats"] == stats, "Site radio stats and source metrics differ")
    compact_prefix = ("window.__COHON_EPISODES__=window.__COHON_EPISODES__||[];"
                      "window.__COHON_EPISODES__.push(...")
    compact = [
        row for a, b in [(2002, 2006), (2007, 2011), (2012, 2016), (2017, 2021), (2022, 2026)]
        for row in read_js_array(DIST / f"data-{a}-{b}.js", compact_prefix, ");")
    ]
    require(len(compact) == len(radio), "Site radio bundle does not contain all episodes")
    require(all(0 <= r["r"] < len(meta["roles"]) for r in compact), "Guest-role index outside dictionary")
    require(all(all(0 <= t < len(meta["topics"]) for t in r["t"]) for r in compact), "Topic index outside dictionary")
    latest = {r["d"]: r for r in compact}
    require(latest["2026-09-27"]["s"] == "l" and "k" not in latest["2026-09-27"], "Verified recent MP3 must appear checked in browser")
    require(latest["2026-10-04"]["s"] == "m", "Podbean-only episode must not claim listed official audio")

    site_writing = read_js_array(DIST / "writings-data.js", "window.SAM_WRITINGS=", ";")
    require(len(site_writing) == len(writing) + len(standalone), "Site writing count mismatch")
    require({r["url"] for r in site_writing} ==
            {r["url"] for r in writing} | {r["url"] for r in standalone},
            "Website source URLs do not match canonical writing ledgers")
    site_editions = {r["url"]: r for r in site_writing}
    require(all(site_editions[u].get("relation_status") == edition_status for u in (older, newer)),
            "Generated writing browser uses old Gratitude edition status")
    html = (DIST / "index.html").read_text(encoding="utf-8")
    require("1,605" in html and "1,599" not in html, "Stale site aggregate")
    require("makeRadioBrowser()" in html and "data-2022-2026.js" in html, "Radio browser missing")
    require("310 distinct works" in html, "Distinct-work upper-bound notice missing")

    print(f"PASS: {len(radio)} radio + {len(writing) + len(standalone)} writing + "
          f"{len(teaching)} teaching = 1,605 indexed records; editions and site bundles agree.")


if __name__ == "__main__":
    main()
