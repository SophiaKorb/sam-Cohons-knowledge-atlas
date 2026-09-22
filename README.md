# Samuel M. Cohon Knowledge Atlas

An independent, source-tracked archive of Rabbi Samuel M. Cohon’s public work.

The project currently contains three substantial catalogued collections plus a discovery-only social layer:

- **Collection 01: Too Jewish Radio** — 1,261 broadcasts catalogued from August 4, 2002 through September 20, 2026.
- **Collection 02: Authored Works** — 312 first-party writing source records located: 47 from Sam's standalone blog and 265 from the Congregation Beit Simcha Rabbi's Blog.
- **Collection 03: Teaching & Services** — 26 unique first-party teaching-recording listings normalized from Beit Simcha's audio archive.
- **Collection 04: Public Media discovery** — 12 first-party Facebook URLs retained as discovery-only because direct source access is login-gated.

The main catalogued corpus now contains **1,599 source records** (1,261 radio + 312 writing + 26 teaching recordings). The 312 writing records are **source records, not yet a claim of 312 unique intellectual works**. Cross-source deduplication, date enrichment, and source-text review are active research stages.

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
- 265/265 Beit Simcha records now have first-party archive publication dates
- 265/265 Beit Simcha titles verified from archive cards; 164 slug-derived titles corrected
- Cross-source deduplication in candidate-review stage
- Individual date/source-text enrichment ongoing
- Dedupe candidate ledger created; source-text comparison still required before collapsing records
- Public Facebook records are kept as discovery-only when direct content is login-gated

### Teaching & Services
- 27 recording entries displayed on the Beit Simcha source page
- 26 unique recording records after normalizing a duplicated History of Zionism Class One listing
- 3-part History of Zionism sequence dated from the first-party event schedule
- Introductory Judaism Classes 1-11 date-enriched where dates are explicit in titles
- 7 current first-party teaching-program context records indexed separately; these are not counted as discrete works

Metadata discovery, source-text review, transcription, thematic synthesis, and evidence mapping are maintained as separate layers.

## Repository structure

- `data/episodes-by-year/` — normalized Too Jewish research dataset
- `data/link-checks-by-year/` — audio-link verification ledger
- `data/stats.json` — generated radio archive metrics and methods
- `data/writings/rabbisamcohon-blog.json` — 47 first-party standalone-blog records
- `data/writings/beit-simcha-blog.json` — 265 first-party Beit Simcha blog records
- `data/writings/sources.json` — source registry and research-state ledger
- `data/writings/dedupe-candidates.json` — cross-source title-match candidates awaiting source-text comparison
- `data/teaching/beit-simcha-audiocasts.json` — 26 normalized first-party teaching recording listings
- `data/teaching/current-programs.json` — current teaching-program context from Beit Simcha
- `data/social/facebook-discovery.json` — first-party Facebook URLs discovered through public indexing, not treated as source-reviewed content
- `scripts/` — ingestion, verification, and site-data tooling
- `dist/` — deployable static presentation site
- `.github/workflows/pages.yml` — GitHub Pages deployment workflow

## Research boundaries

The atlas is centered on Sam Cohon's own public work, first-party congregational materials, radio, teaching, interviews, and neutral biographical/professional context.

The project does **not** ingest unrelated scandal coverage.

Episode audio, sermon text, article text, and descriptions remain with their original publishers. The atlas stores source-tracked metadata and research-navigation records rather than republishing full copyrighted texts.
