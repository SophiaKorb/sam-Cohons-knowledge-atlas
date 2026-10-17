#!/usr/bin/env python3
"""Read-only structural validation of first-party authored-writing catalog."""
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def load(rel):
    return json.loads((root / rel).read_text(encoding="utf-8"))
beit = load("data/writings/beit-simcha-blog.json")
standalone = load("data/writings/rabbisamcohon-blog.json")
stats = load("data/writings/stats.json")
records = beit["records"] + standalone["records"]
urls = [r.get("url") for r in records]
issues = []
def expect(condition, message):
    if not condition:
        issues.append(message)
expect(len(beit["records"]) == beit["record_count"], "Beit Simcha record_count mismatch")
expect(len(standalone["records"]) == standalone["record_count"], "Standalone record_count mismatch")
expect(len(records) == stats["source_records_total"], "Writing total mismatch")
expect(len(beit["records"]) == stats["beit_simcha_blog_records"], "Beit Simcha stats mismatch")
expect(len(standalone["records"]) == stats["standalone_blog_records"], "Standalone stats mismatch")
expect(len(set(urls)) == len(urls), "Duplicate canonical URLs detected")
for i, record in enumerate(records):
    expect(bool(record.get("title")), f"Missing title in record {i}")
    expect(str(record.get("url","")).startswith("https://"), f"Missing/invalid HTTPS URL in record {i}")
for i, record in enumerate(beit["records"]):
    expect(bool(record.get("published_date")), f"Missing Beit Simcha date in record {i}")
years = dict(sorted(Counter(r["published_date"][:4] for r in beit["records"]).items()))
expect(years == {k:int(v) for k,v in stats["beit_simcha_records_by_year"].items()}, "Beit Simcha year totals mismatch")
expect(len(beit["records"]) == stats["beit_simcha_records_with_dates"], "Published-date coverage mismatch")
print(json.dumps({"passed":not issues,"source_records":len(records),"beit_simcha":len(beit["records"]),"standalone":len(standalone["records"]),"years":years,"issues":issues},indent=2))
if issues:
    raise SystemExit(1)
