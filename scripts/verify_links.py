#!/usr/bin/env python3
"""Verify first-party Too Jewish audio links without downloading audio."""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EPISODES_PATH = ROOT / "data" / "episodes.json"
STATS_PATH = ROOT / "data" / "stats.json"
CHECKS_PATH = ROOT / "data" / "link_checks.json"
USER_AGENT = "Mozilla/5.0 (compatible; Samuel-Cohon-Archive/1.0; link verification)"
WORKERS = 12
TIMEOUT = 25


def verify_all(records: list[dict]) -> list[dict]:
    args = [
        "curl", "--parallel", "--parallel-immediate", "--parallel-max", str(WORKERS),
        "--head", "--location", "--silent", "--show-error",
        "--connect-timeout", "10", "--max-time", str(TIMEOUT),
        "--retry", "1", "--retry-delay", "1", "--user-agent", USER_AGENT,
        "--write-out", "%{urlnum}\\t%{http_code}\\t%{exitcode}\\t%{errormsg}\\n",
    ]
    for record in records:
        args.extend(["--output", "/dev/null", record["official_audio_url"]])

    process = subprocess.run(args, capture_output=True, text=True, check=False)
    by_index: dict[int, tuple[int | None, int, str | None]] = {}
    for line in process.stdout.splitlines():
        parts = line.split("\t", 3)
        if len(parts) < 3 or not parts[0].isdigit():
            continue
        index = int(parts[0])
        status = int(parts[1]) if parts[1].isdigit() and int(parts[1]) else None
        exit_code = int(parts[2]) if parts[2].isdigit() else 1
        error = parts[3].strip() if len(parts) > 3 and parts[3].strip() else None
        by_index[index] = (status, exit_code, error)

    results: list[dict] = []
    for index, record in enumerate(records):
        status, exit_code, error = by_index.get(index, (None, 1, "curl returned no result"))
        state = "live" if exit_code == 0 and status is not None and 200 <= status < 400 else "dead" if status in {404, 410} else "error"
        results.append(
            {
                "id": record["id"],
                "url": record["official_audio_url"],
                "state": state,
                "http_status": status,
                "error": error if state == "error" else None,
            }
        )
    return results


def main() -> None:
    records = json.loads(EPISODES_PATH.read_text(encoding="utf-8"))
    linked = [record for record in records if record.get("official_audio_url")]
    checks = verify_all(linked)

    checks.sort(key=lambda item: item["id"])
    checked_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    check_by_id = {check["id"]: check for check in checks}
    for record in records:
        check = check_by_id.get(record["id"])
        if check:
            record["official_link_status"] = check["state"]
            record["official_http_status"] = check["http_status"]
            record["official_link_checked_at"] = checked_at
        else:
            record["official_link_status"] = "not_listed"
            record["official_http_status"] = None
            record["official_link_checked_at"] = checked_at

    states = Counter(record["official_link_status"] for record in records)
    stats = json.loads(STATS_PATH.read_text(encoding="utf-8"))
    stats["link_checked_at"] = checked_at
    stats["link_status_counts"] = dict(states)
    stats["link_verification_method"] = "HTTP HEAD against each first-party MP3 URL; network errors remain errors and are not counted as dead links."

    EPISODES_PATH.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    STATS_PATH.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CHECKS_PATH.write_text(json.dumps({"checked_at": checked_at, "checks": checks}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"checked": len(checks), "states": dict(states), "checked_at": checked_at}, indent=2))


if __name__ == "__main__":
    main()
