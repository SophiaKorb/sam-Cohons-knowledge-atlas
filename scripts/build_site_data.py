#!/usr/bin/env python3
"""Create the compact, browser-ready data bundle for the static archive."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DIST_DIR = ROOT / "dist"
EPISODE_SPLIT_DIR = DATA_DIR / "episodes-by-year"
CHECK_SPLIT_DIR = DATA_DIR / "link-checks-by-year"
OFFICIAL_PREFIX = "https://toojewishradio.com/"
PODBEAN_PREFIX = "https://toojewishradio.podbean.com/"
YEAR_GROUPS = [(2002, 2006), (2007, 2011), (2012, 2016), (2017, 2021), (2022, 2026)]


def main() -> None:
    episodes = json.loads((DATA_DIR / "episodes.json").read_text(encoding="utf-8"))
    stats = json.loads((DATA_DIR / "stats.json").read_text(encoding="utf-8"))
    checks = json.loads((DATA_DIR / "link_checks.json").read_text(encoding="utf-8"))["checks"]
    topics = sorted({topic for episode in episodes for topic in episode["topics"]})
    roles = sorted({episode["guest_role"] for episode in episodes})
    topic_index = {topic: index for index, topic in enumerate(topics)}
    role_index = {role: index for index, role in enumerate(roles)}

    compact = []
    for episode in episodes:
        official_url = episode.get("official_audio_url") or ""
        podbean_url = episode.get("podbean_url") or ""
        compact.append(
            {
                "d": episode["broadcast_date"],
                "g": episode["guest"],
                "x": episode["description"],
                "r": role_index[episode["guest_role"]],
                "t": [topic_index[topic] for topic in episode["topics"]],
                "a": official_url.removeprefix(OFFICIAL_PREFIX) if official_url else "",
                "s": {"live": "l", "dead": "d", "not_listed": "m"}[episode["official_link_status"]],
                "p": podbean_url.removeprefix(PODBEAN_PREFIX) if podbean_url else "",
                "u": episode.get("duration") or "",
                "c": 1 if episode["review_status"].endswith("two_first_party_sources") else 0,
            }
        )

    by_year: dict[int, list[dict]] = defaultdict(list)
    for episode in episodes:
        by_year[episode["year"]].append(episode)
    EPISODE_SPLIT_DIR.mkdir(parents=True, exist_ok=True)
    for year, rows in sorted(by_year.items()):
        (EPISODE_SPLIT_DIR / f"{year}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    checks_by_year: dict[int, list[dict]] = defaultdict(list)
    date_by_id = {episode["id"]: episode["year"] for episode in episodes}
    for check in checks:
        checks_by_year[date_by_id[check["id"]]].append(check)
    CHECK_SPLIT_DIR.mkdir(parents=True, exist_ok=True)
    for year, rows in sorted(checks_by_year.items()):
        (CHECK_SPLIT_DIR / f"{year}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    old_bundle = DIST_DIR / "data.js"
    if old_bundle.exists():
        old_bundle.unlink()
    meta = {
        "stats": stats,
        "topics": topics,
        "roles": roles,
        "official_prefix": OFFICIAL_PREFIX,
        "podbean_prefix": PODBEAN_PREFIX,
        "topic_provenance": "deterministic inference from first-party episode description",
        "transcript_status": "not_ingested",
        "evidence_boundary": "Catalogue metadata only; no claims attributed without source-text review.",
    }
    (DIST_DIR / "data-meta.js").write_text(
        "window.__COHON_META__=" + json.dumps(meta, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    for start, end in YEAR_GROUPS:
        rows = [row for row in compact if start <= int(row["d"][:4]) <= end]
        text = "window.__COHON_EPISODES__=window.__COHON_EPISODES__||[];window.__COHON_EPISODES__.push(..." + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ");\n"
        (DIST_DIR / f"data-{start}-{end}.js").write_text(text, encoding="utf-8")
    print(f"Wrote {len(episodes)} episodes across {len(YEAR_GROUPS)} browser bundles and {len(by_year)} research files")


if __name__ == "__main__":
    main()
