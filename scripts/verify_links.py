#!/usr/bin/env python3
"""Targeted, read-only HEAD diagnostics for first-party Too Jewish MP3 URLs.

This tool deliberately does NOT mutate the canonical episode records, source
link-status counts, historical verification timestamps or generated site.
It is safe to run even when the network is unavailable.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
EPISODE_DIR = ROOT / "data" / "episodes-by-year"
ALLOWED_HOSTS = frozenset({"toojewishradio.com", "www.toojewishradio.com"})
MAX_IDS = 20


def load_records(directory: Path = EPISODE_DIR) -> list[dict]:
    paths = sorted(directory.glob("[0-9][0-9][0-9][0-9].json"))
    if not paths:
        raise ValueError(f"No year-split canonical episode files found in {directory}")
    records = [r for path in paths for r in json.loads(path.read_text(encoding="utf-8"))]
    ids = [r["id"] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate episode IDs in source files; refusing to probe")
    return records


def select_records(records: list[dict], ids: list[str]) -> list[dict]:
    if not ids or len(ids) > MAX_IDS or len(set(ids)) != len(ids):
        raise ValueError(f"Supply 1–{MAX_IDS} distinct episode IDs via --id")
    lookup = {r["id"]: r for r in records}
    unknown = [item for item in ids if item not in lookup]
    if unknown:
        raise ValueError(f"Unknown episode ID(s): {', '.join(unknown)}")
    return [lookup[item] for item in ids]


def probe_url(url: str, runner=subprocess.run) -> dict:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Official MP3 HEAD check requires an HTTPS toojewishradio.com URL")
    if parsed.username or parsed.password:
        raise ValueError("Userinfo in URL not permitted")
    cmd = [
        "curl", "--head", "--location", "--silent", "--show-error",
        "--output", "/dev/null", "--connect-timeout", "10", "--max-time", "25",
        "--retry", "0", "--write-out", "%{http_code}", "--", url,
    ]
    try:
        run = runner(cmd, capture_output=True, text=True, check=False, timeout=35)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"observed_state": "inconclusive", "http_status": None,
                "error": str(exc)[:400]}
    raw_code = (run.stdout or "").strip()
    code = int(raw_code) if re.fullmatch(r"\d{3}", raw_code) else None
    if run.returncode == 0 and code is not None and 200 <= code < 400:
        state = "responded_successfully_to_HEAD"
    elif run.returncode == 0 and code in (404, 410):
        state = "HEAD_reported_missing"
    else:
        state = "inconclusive"
    return {"observed_state": state, "http_status": code,
            "error": (run.stderr or "").strip()[:400] if state == "inconclusive" else None}


def run_checks(records: list[dict], ids: list[str], probe=probe_url) -> dict:
    selected = select_records(records, ids)
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    findings = []
    for record in selected:
        url = record.get("official_audio_url")
        finding = {
            "id": record["id"],
            "broadcast_date": record["broadcast_date"],
            "official_audio_url": url,
            "catalogued_link_status_unchanged": record["official_link_status"],
        }
        if url:
            finding.update(probe(url))
        else:
            finding.update({"observed_state": "no_official_audio_url",
                            "http_status": None, "error": None})
        findings.append(finding)
    return {
        "checked_at_utc": now,
        "scope": "targeted non-mutating HEAD diagnostic only; NOT a persisted verified link status",
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", action="append", dest="ids", required=True,
                        help="Exact episode ID, repeat up to 20 times. No bulk/overwrite mode.")
    args = parser.parse_args(argv)
    try:
        result = run_checks(load_records(), args.ids)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
