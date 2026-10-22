# Samuel M. Cohon Knowledge Atlas

An independent, source-tracked archive of Rabbi Samuel M. Cohon’s public work.

The project currently contains three substantial catalogued collections plus a discovery-only social layer:

- **Collection 01: Too Jewish Radio** — 1,265 broadcasts catalogued from August 4, 2002 through October 18, 2026 (three newly publisher-listed MP3 URLs awaiting independent verification).
- **Collection 02: Authored Works** — 316 first-party writing source records located: 47 from Sam's standalone blog and 269 from the Congregation Beit Simcha Rabbi's Blog.
- **Collection 03: Teaching & Services** — 26 unique first-party teaching-recording listings normalized from Beit Simcha's audio archive.
- **Collection 04: Public Media discovery** — 12 first-party Facebook URLs retained as discovery-only because direct source access is login-gated.

The main catalogued corpus now contains **1,607 source records** (1,265 radio + 316 writing + 26 teaching recordings). The 316 writing records are **publication/source records, not a claim of 316 unique intellectual works**. Cross-source deduplication, date enrichment, and source-text review are active research stages.

## Current research status

### Too Jewish Radio
- 1,265 broadcast records normalized (September 27 direct official MP3 now link-verified via targeted HEAD; October 4 remains Podbean-only)
- 1,219 first-party MP3 links checked in the September 22 batch, plus a targeted first-party September 27 HEAD 200 audio/mpeg check on October 15 (without audio download)
- 889 official links responded successfully to HEAD in the September 22 batch; 1 additional verified October 15 (890 link-live records total; no playback claims)
- 738 records cross-checked against the official listing and Podbean catalogue; one new item is Podbean-only
- 330 listed links unavailable
- 42 broadcasts with no official audio link listed
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

Two radio broadcasts (September 27 and October 4) and one first-party blog entry (October 9) were added to the source datasets. The October 4 show is Podbean-only in the checked official show list, and the September 27 official MP3 was later HTTP-tested on October 15 (HEAD 200, audio/mpeg, zero redirects; audio not downloaded). The September 30 **Finding Gratitude** has its own `finding-gratitude-1` URL; the earlier 2024 version remains at `finding-gratitude`. Full first-party body comparison completed October 13: 20/21 paragraphs identical, one holiday-calendar update. Preserve two publication entries but count one substantive sermon. Also indexed September 22 *Redemption* and September 28 *A Donation*. **The generated `dist/` site is current and CI-validated; older full-corpus links have not been rechecked since September 22.**

## Repository structure

- `data/episodes-by-year/` — normalized Too Jewish research dataset
- `data/link-checks-by-year/` — audio-link verification ledger
- `data/stats.json` — generated radio archive metrics and methods
- `data/writings/rabbisamcohon-blog.json` — 47 first-party standalone-blog records
- `data/writings/beit-simcha-blog.json` — 269 first-party Beit Simcha blog records
- `data/writings/sources.json` — source registry and research-state ledger
- `data/writings/dedupe-candidates.json` — cross-source title candidates plus first-pass text-comparison findings
- `data/writings/stats.json` — authored-work chronology and dedupe metrics
- `data/teaching/beit-simcha-audiocasts.json` — 26 normalized first-party teaching recording listings
- `data/teaching/current-programs.json` — current teaching-program context from Beit Simcha
- `data/teaching/historical-source-leads.json` — earlier Temple Emanu-El podcast-channel provenance; no claimed surviving audio
- `data/social/facebook-discovery.json` — first-party Facebook URLs discovered through public indexing, not treated as source-reviewed content
- `scripts/` — ingestion, verification, and site-data tooling
- `dist/` — deployable static presentation site
- `.github/workflows/pages.yml` — GitHub Pages deployment workflow


### Historical evidence intake (not included in the 1,607 core catalogue records)
- Two attributed **excerpt-only** Temple Emanu-El-era writing leads were preserved in `data/writings/community-publications.json`: *Baking Holiness* (first-party newsletter dated April 30, 2013) and *The Necessary Chutzpah of Saving Refugees* (2015 Union for Reform Judaism roundup). Neither complete original manuscript is ingested, and neither is added to the 316 core blog-source total.
- The same 2013 newsletter advertises a Temple Emanu-El podcast account for adult classes, with Sam teaching Basic/Intermediate Judaism and Zohar. `historical-source-leads.json` preserves the historical channel URL, **not** a claim that a particular MP3 was recovered or remains playable.
- Publisher Podbean pages exposed Download hrefs for the September 27 and October 4, 2026 *Too Jewish* episodes. Their direct audio response, bytes and rights remain **unverified**; the source episode rows retain their original official-link statuses, and the core counts do not change.

### October 15 single-link publisher response evidence
The verified publisher September 27 MP3 URL returned **HTTP 200**, `audio/mpeg`, **zero redirects** on a GitHub-hosted runner. Evidence is retained at `data/verification/too-jewish-2026-09-27-head-2026-10-15.json`, linked to two read-only workflow runs. The status is **official URL HTTP-live only**; binary integrity, playback, transcription, speaker attribution and reuse rights remain unreviewed. Keep the September 22 full-corpus verification timestamp unchanged.

### Read-only audio link diagnostics
The historic `scripts/verify_links.py` originally assumed the deleted combined `data/episodes.json` and would write statuses across the entire catalogue. It has been replaced with a **targeted, non-mutating** official-MP3 HEAD probe. It reads the canonical `data/episodes-by-year/*.json` files and prints JSON evidence only:

```sh
python scripts/verify_links.py --id tj-2026-09-27
python scripts/verify_links.py --id tj-2026-09-27 --id tj-2026-10-04
```

The diagnostic never downloads the audio and **never updates source records, generated site files, historic link-status counts, or verified timestamps**. A 404/410 from a successful HEAD is an observation, not automatic permanent proof of an unavailable recording; network errors, blocks and 403/405/5xx replies remain inconclusive. Only first-party official MP3 hosts are probed, and no bulk mode is offered. Independent review and a separate controlled ingestion step would be needed to promote statuses.

### Private Too Jewish pilot transcription and optional TurboScribe route (October 15 UTC)
A genuine **150-second** September 27, 2026 show segment was decoded and transcribed in a networked ephemeral runner, creating **43 raw timestamped segments (about 395 words)**. Source SHA-256 and quality limitations are documented in `data/verification/too-jewish-2026-09-27-asr-private-pilot.json`; **raw text lives only in private Library /Writing**, never in this repository. The full 54:54 episode is *not* transcribed or editorially reviewed. Public radio episode `transcript_status` stays `not_ingested`, and completed transcripts still count **zero**.

Use [TurboScribe](https://turboscribe.com/) **when appropriate** for long-form interviews, multi-speaker audio, Hebrew/Yiddish and difficult first-pass results, subject to permissions and user-authorized external processing. Preserve its untouched export separately and compare to original audio; see [audio transcription protocol](docs/audio-transcription-workflow.md). Historical ten raw TurboScribe course transcripts belong to the private **Introductory Judaism** project, not the radio episode count.

### Second private radio transcription pilot (October 15 UTC)
The original September 27 broadcast MP3 SHA-256 was reconfirmed on a private networked worker. An independent **five-minute** `small.en` pass yielded **74 raw timed segments / 564 recognized words**; a **150-second MP3 listening sample** was separately preserved in private Library `/Writing/` with the raw transcript and a QA comparison. The roughly overlapping first and second passes have **94.4% machine-to-machine word-sequence similarity**, **not accuracy against the recording**. Eleven listening-review questions remain, including an extended **03:34–05:03 music section** for which speech transcription is not reliable. The one-time private runner was deleted after artifact retrieval. Provenance is recorded in `data/verification/too-jewish-2026-09-27-asr-private-pilot.json`; no audio or raw transcript text was added to the repository. **Zero completed/reviewed full radio episode transcripts.** TurboScribe remains an optional authorized separate comparison, not used for this pass.

### Full original radio audio and private machine-only episode draft (October 15 UTC)
The exact **79,065,806-byte, 54:54** September 27 *Too Jewish* original publisher MP3 was recovered, checksum-verified and preserved privately in Library `/Writing/`. [Temporary private-processing run 38688088219](https://github.com/SophiaKorb/sam-Cohons-knowledge-atlas/actions/runs/38688088219) completed **six encrypted, full-duration `small.en` ASR shards**, then their unmodified outputs were recovered privately. The combined **unreviewed machine transcript spans the full recording** with **823 timestamped segments and 7,765 recognized words**. All six unchanged original part files, joined JSON/TXT, full-audio QA notes and the original MP3 are preserved separately in private Library. Source checksums and stage boundaries are in `data/verification/too-jewish-2026-09-27-asr-private-pilot.json`.

**Full audio machine coverage is not human verification**: no speakers or words have been approved by listening. Music/lyrics, Hebrew words, guest attribution and transitions at 09:10, 18:20, 27:30, 36:40 and 45:50 require correction against original sound. Thirteen short original-audio excerpts were extracted into a **private** QA packet; waveform/VAD signal detection did not prove phrase accuracy. The one-shot encrypted workflow has been removed. **0 editorially reviewed full radio transcripts** and public `transcript_status=not_ingested`. No MP3, transcript content or decryption key is in GitHub. TurboScribe was not used and remains optional with suitable user authorization.

### Additional sound-grounded editorial triage (October 15 UTC)
The original checksum-verified full recording was re-decoded into **five separate 24-second clips**, each covering 12 seconds on either side of the six-part ASR split boundaries (**09:10, 18:20, 27:30, 36:40, 45:50**). The source raw recognition timings show **-1.53, -0.23, +0.46, 0.00 and +0.08 seconds** between adjacent parts (negative = overlapping ASR timestamps, not necessarily repeated source words). Audio clips were decoded and independently SHA-256 checked; **these technical checks do not determine what was spoken**. The original recording and six raw machine outputs remain unchanged.

A new **private annotation-only derivative** retains **all 823 raw text segments without changing words**, with flags for the **11 previously identified disputed passages** and five chunk seams. The five new clips, their manifest and a private quantitative QA memo are stored in the existing `/Writing/` Library folder. The public [pilot evidence](data/verification/too-jewish-2026-09-27-asr-private-pilot.json) contains **metadata and hashes only**. Human listening, speaker identification, music/lyrics verification, editorial signoff and publication rights remain outstanding; reviewed radio transcript count stays **0**. TurboScribe was not used.

## Research boundaries

The atlas is centered on Sam Cohon's own public work, first-party congregational materials, radio, teaching, interviews, and neutral biographical/professional context.

The project does **not** ingest unrelated scandal coverage.

Episode audio, sermon text, article text, and descriptions remain with their original publishers. The atlas stores source-tracked metadata and research-navigation records rather than republishing full copyrighted texts.

### October 21, 2026: Too Jewish publisher-listing intake (unpublished research branch)

The official show index now lists **October 11: Jonah Platt** and **October 18: Professor Shai Davidai**. The previous October 4 Podbean-only item (Rabbi Noa Kushner) also now has an official indexed MP3 href. All three publisher MP3 URLs have `official_link_status=not_checked`: the first-party HTML link is confirmed, but an independent successful HTTP response, binary acquisition, audio playback and reuse rights have not been verified. The 2026 ledger includes 42 radio records; the overall radio corpus now contains **1,265 episodes**. The full-corpus September 22 HTTP checks and September 27 private audio/transcription work retain their historical provenance. The full-episode editorially reviewed transcript count remains **zero**. The research index contains 1,265 radio, 316 first-party writing source records, and 26 teaching recordings = **1,607 source records**.

This is a research-branch-only intake; it does not merge into `main` or update the deployed public archive.
