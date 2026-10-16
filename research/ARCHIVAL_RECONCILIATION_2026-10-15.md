# Archival reconciliation — October 15, 2026

## Scope and status
This is a **metadata crosswalk**, not a transcription, approval, or release. It reconciles the public Knowledge Atlas with separately preserved private teaching and manuscript material, without putting private recordings, raw transcript text, unpublished sermons, or attendee remarks into this public repository.

### Counts that must not be silently combined

| Dataset | Verified repository baseline | Later research claim | Treatment |
|---|---:|---:|---|
| Too Jewish radio | 1,261 broadcasts | — | Retain 1,261; link verification is a separate question from broadcast discovery |
| First-party authored writing (standalone blog + Beit Simcha) | 47 + 265 = **312 source records** | Private October 2026 editorial memo describes **316** first-party records (47 + 269) | **312 is still the checked-in catalog baseline**; do not replace with 316 without four identifiable added source records, record-level source URLs, and dedupe checks |
| Teaching & services | **26 distinct index listings** | Private local classroom recordings and raw transcripts also exist | These are different manifestations; do not add local audio copies as 26 new published works or assert all have audio/transcript verification |
| Supplemental community publications | Source registry identifies JCC and AZ Jewish Post batches | — | Track separately; not automatically added to first-party distinct-work count |

The README already notes at least five confirmed duplicate/republication source records and a **conservative upper bound of 307 distinct works** among the 312 first-party writing records. That number is not a verified total of unique works.

## Public-to-private teaching source crosswalk

Public Atlas record IDs refer to the Beit Simcha teaching listing. Private recording/transcript accessions were independently inventoried under the *Judaism for Beginners* archive and are described only by their relationship to the first-party listing.

| Atlas ID | Public catalog title/date | Private archival relationship | Confidence and restriction |
|---|---|---|---|
| BS-TEACH-005 | Introductory Judaism Class 1, October 27, 2024 | Original M4A and automatic transcript retained separately; existing intake notes provide thematic/timecode anchors | **Catalog-date match and archival association**; no assertion of word-level audio validation |
| BS-TEACH-006 | Introductory Judaism Class 2, November 3, 2024 | Original M4A retained; a transcript whose legacy label says “Class 4” is a possible *concepts of God* pairing | **Candidate transcript association only**. Do not relabel or quote as Class 2 until recording is reviewed |
| BS-TEACH-007 etc. | Adult Bar/Bat Mitzvah series | No corresponding private file pairing established in this reconciliation | **Do not infer locally recovered recordings** |

The private introductory-Judaism Class 3 and Class 4 recordings exist, but this register does not invent a direct Atlas ID without checking those complete records individually. The Class 4 minor-festivals source must not be conflated with the candidate concepts-of-God transcript.

## Source-object hierarchy

A sermon or lecture can be represented by several **manifestations** without becoming several intellectual works:

1. **Work** — a distinct sermon, class lecture, broadcast, interview, or article.
2. **Event** — the date and place of delivery (may differ from a publication date).
3. **Source object** — publisher listing, original DOCX/M4A, archived blog article, podcast page, or catalog record.
4. **Derivative** — automatic transcript, edited transcript, MP3 excerpt, HTML adaptation, teaching-guide excerpt.
5. **Evidence** — first-party URL, source timestamp, exact source-text position, SHA-256 of bytes inspected, and proof of permissions.
6. **Approval** — religious editorial acceptance, privacy decision, rights clearance and publication authorization. These are independent of technical readiness.

Use stable IDs per work and per source object; use a relation such as `isManifestationOf`, `isDerivedFrom`, or `possibleMatchTo`. A `possibleMatchTo` relation is *not* a dedupe decision.

## Immediate independently executable research backlog

- Identify the precise four Beit Simcha blog records implied by the private memo's 269 vs repository's 265; verify first-party URLs/titles/dates, check whether they are truly newly discovered or alternate presentations, then update all generated counts together.
- Crosswalk private sermon manuscript titles to existing blog records by title and content evidence, while retaining unpublished originals in private storage.
- Preserve the Class 2/“Class 4.txt” candidate-match warning, and do not certify a transcript based on a filename or topic.
- Add source-object provenance and source-check timestamp fields incrementally; preserve distinction between link-validity checks and audio-content checks.
- Record explicit editorial/rights gates before authorizing any archive-site audio or manuscript reproduction.

## Methodology and limits

This file was written after inspecting the repository README and the checked-in `data/writings/sources.json`, `data/writings/stats.json`, and `data/teaching/beit-simcha-audiocasts.json`, plus the separate private archival inventory and its October research memo. It does not imply that a new audio recording was listened to, a manuscript compared word-for-word, a source checksum calculated, or an updated live website deployed.
