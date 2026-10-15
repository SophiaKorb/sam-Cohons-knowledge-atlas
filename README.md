# Samuel M. Cohon Knowledge Atlas

An independent, source-tracked archive of Rabbi Samuel M. Cohon’s public work.

The project currently contains three substantial catalogued collections plus a discovery-only social layer:

- **Collection 01: Too Jewish Radio** — 1,263 broadcasts catalogued from August 4, 2002 through October 4, 2026 (latest two entries staged for source/link QA).
- **Collection 02: Authored Works** — 316 first-party writing source records located: 47 from Sam's standalone blog and 269 from the Congregation Beit Simcha Rabbi's Blog.
- **Collection 03: Teaching & Services** — 26 unique first-party teaching-recording listings normalized from Beit Simcha's audio archive.
- **Collection 04: Public Media discovery** — 12 first-party Facebook URLs retained as discovery-only because direct source access is login-gated.

The main catalogued corpus now contains **1,605 source records** (1,263 radio + 316 writing + 26 teaching recordings). The 316 writing records are **publication/source records, not a claim of 316 unique intellectual works**. Cross-source deduplication, date enrichment, and source-text review are active research stages.

## Current research status

### Too Jewish Radio
- 1,263 broadcast records normalized (2 incremental source records require final audio verification)
- 1,219 first-party MP3 links checked as of September 22; one newly listed audio URL remains unchecked
- 889 live audio links confirmed in the September 22 verification batch
- 737 records cross-checked against the official listing and Podbean catalogue; one new item is Podbean-only
- 330 listed links unavailable
- 43 broadcasts with no official audio link listed
- 0 transcript-level reviews claimed in the first radio batch

### Authored Works
- 47 first-party records from the complete 23-page Rabbi Sam Cohon blog archive
- 269 first-party records from the Beit Simcha Rabbi's Blog archive (4 new September–October 2026 first-party source URLs added)
- 269/269 Beit Simcha records now have first-party archive publication dates
- 269/269 Beit Simcha titles verified from archive cards; 164 slug-derived titles corrected
- Cross-source deduplication in candidate-review stage
- Individual date/source-text enrichment ongoing
- First source-text dedupe pass complete on the seven strongest candidate groups
- At least 6 redundant source records confirmed: five earlier cross-source republications and the full-body-verified 2024/2026 *Finding Gratitude* calendar edition. Conservative upper bound: **310 distinct works from 316 publication records**.
- Strong-overlap candidates remain separate pending manual/source-boundary review
- Public Facebook records are kept as discovery-only when direct content is login-gated

### Teaching & Services
- 27 recording entries displayed on the Beit Simcha source page
- 26 unique recording records after normalizing a duplicated History of Zionism Class One listing
- 3-part History of Zionism sequence dated from the first-party event schedule
- Introductory Judaism Classes 1-11 date-enriched where dates are explicit in titles
- 7 current first-party teaching-program context records indexed separately; these are not counted as discrete works

Metadata discovery, source-text review, transcription, thematic synthesis, and evidence mapping are maintained as separate layers.


### October 12, 2026 incremental research branch

Two radio broadcasts (September 27 and October 4) and one first-party blog entry (October 9) were added to the source datasets. The October 4 show is Podbean-only in the checked official show list, and the September 27 official MP3 was not HTTP-tested. The September 30 **Finding Gratitude** has its own `finding-gratitude-1` URL; the earlier 2024 version remains at `finding-gratitude`. Full first-party body comparison completed October 13: 20/21 paragraphs identical, one holiday-calendar update. Preserve two publication entries but count one substantive sermon. Also indexed September 22 *Redemption* and September 28 *A Donation*. **The generated `dist/` site and older full-corpus link checks have not been regenerated or reverified on this branch**; rebuild them and run validation before merging or publishing.

## Repository structure

- `data/episodes-by-year/` — normalized Too Jewish research dataset
- `data/link-checks-by-year/` — audio-link verification ledger
- `data/stats.json` — generated radio archive metrics and methods
- `data/writings/rabbisamcohon-blog.json` — 47 first-party standalone-blog records
- `data/writings/beit-simcha-blog.json` — 265 first-party Beit Simcha blog records
- `data/writings/sources.json` — source registry and research-state ledger
- `data/writings/dedupe-candidates.json` — cross-source title candidates plus first-pass text-comparison findings
- `data/writings/stats.json` — authored-work chronology and dedupe metrics
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
