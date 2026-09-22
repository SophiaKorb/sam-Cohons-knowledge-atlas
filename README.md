# Samuel M. Cohon Knowledge Atlas

An independent, source-tracked archive of Rabbi Samuel M. Cohon’s public work.

The project currently contains two substantial collections:

- **Collection 01: Too Jewish Radio** — 1,261 broadcasts catalogued from August 4, 2002 through September 20, 2026.
- **Collection 02: Authored Works** — 312 first-party writing source records located: 47 from Sam's standalone blog and 265 from the Congregation Beit Simcha Rabbi's Blog.

The 312 writing records are **source records, not yet a claim of 312 unique intellectual works**. Cross-source deduplication, date enrichment, and source-text review are active research stages.

## Current research status

### Too Jewish Radio
- 1,261 broadcast records normalized
- 1,219 first-party MP3 links checked
- 889 live audio links
- 736 records cross-checked against the Podbean catalogue
- 330 listed links unavailable
- 42 broadcasts with no audio link listed
- 0 transcript-level reviews claimed in the first radio batch

### Authored Works
- 47 first-party records from the complete 23-page Rabbi Sam Cohon blog archive
- 265 first-party records from the complete 14-page Beit Simcha Rabbi's Blog archive
- Cross-source deduplication pending
- Individual date/source-text enrichment ongoing
- Public Facebook records are kept as discovery-only when direct content is login-gated

Metadata discovery, source-text review, transcription, thematic synthesis, and evidence mapping are maintained as separate layers.

## Repository structure

- `data/episodes-by-year/` — normalized Too Jewish research dataset
- `data/link-checks-by-year/` — audio-link verification ledger
- `data/stats.json` — generated radio archive metrics and methods
- `data/writings/rabbisamcohon-blog.json` — 47 first-party standalone-blog records
- `data/writings/beit-simcha-blog.json` — 265 first-party Beit Simcha blog records
- `data/writings/sources.json` — source registry and research-state ledger
- `data/social/facebook-discovery.json` — first-party Facebook URLs discovered through public indexing, not treated as source-reviewed content
- `scripts/` — ingestion, verification, and site-data tooling
- `dist/` — deployable static presentation site
- `.github/workflows/pages.yml` — GitHub Pages deployment workflow

## Research boundaries

The atlas is centered on Sam Cohon's own public work, first-party congregational materials, radio, teaching, interviews, and neutral biographical/professional context.

The project does **not** ingest unrelated scandal coverage.

Episode audio, sermon text, article text, and descriptions remain with their original publishers. The atlas stores source-tracked metadata and research-navigation records rather than republishing full copyrighted texts.
