# Samuel M. Cohon Knowledge Atlas

An independent, source-tracked archive of Rabbi Samuel M. Cohon’s public work.

The first collection is **Too Jewish Radio**, with 1,261 broadcasts catalogued from August 4, 2002 through September 20, 2026.

## Current research status

- 1,261 broadcast records normalized
- 1,219 first-party MP3 links checked
- 889 live audio links
- 736 records cross-checked against the Podbean catalogue
- 330 listed links unavailable
- 42 broadcasts with no audio link listed
- 0 transcript-level reviews claimed in this first batch

Metadata, transcript review, thematic synthesis, and evidence mapping are maintained as separate layers. Topic tags in the current release are deterministic discovery aids derived from published episode descriptions.

## Repository structure

- `data/episodes-by-year/` — normalized research dataset, split into reviewable yearly files
- `data/link-checks-by-year/` — URL verification ledger, split by year
- `data/stats.json` — generated archive metrics and methods
- `scripts/build_data.py` — first-party archive ingestion and normalization
- `scripts/verify_links.py` — non-destructive audio-link verification
- `scripts/build_site_data.py` — compact browser bundle generator
- `dist/` — deployable static site

## Rebuild

```bash
python3 scripts/build_data.py
python3 scripts/verify_links.py
python3 scripts/build_site_data.py
```

## Sources

- [Official Too Jewish show archive](https://toojewishradio.com/too_jewish_shows.htm)
- [Too Jewish on Podbean](https://toojewishradio.podbean.com/)

Episode audio and descriptions remain with their original publishers.
