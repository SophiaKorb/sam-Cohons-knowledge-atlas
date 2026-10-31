# Tucson Temple Times and Hearing Voices original media-route verification — October 31, 2026

**Scope:** Isolated research branch, verified public metadata only. Follows `temple-recovery-2026-10-31-successor-archives.md`. No private materials, copyrighted full texts, audio, transcripts, release actions or external contact.

## Verified: more than one original Tucson Temple bulletin survived

The earlier archive checkpoint established a [June–July 2021 Temple Times](https://images.shulcloud.com/2920/uploads/Documents/Temple-Times/21-jun-jul.pdf) issue on the former Temple Emanu-El Tucson ShulCloud storage path, `images.shulcloud.com/2920/uploads/Documents/Temple-Times/`.

New original, individually indexed links to issues under the **same collection path** were located and the public web-PDF's extracted mastheads identified the original congregation:

| Verified issue | Publication designation | Public original PDF |
|---|---|---|
| April 2019 | Vol. LXVII, no. 8 | [19-apr.pdf](https://images.shulcloud.com/2920/uploads/Documents/Temple-Times/19-apr.pdf) |
| August 2019 | Vol. LXVII, no. 12 | [19-aug.pdf](https://images.shulcloud.com/2920/uploads/Documents/Temple-Times/19-aug.pdf) |
| September 2019 | Vol. LXVIII, no. 1 | [19-sep.pdf](https://images.shulcloud.com/2920/uploads/Documents/Temple-Times/19-sep.pdf) |
| October 2019 | Vol. LXVIII, no. 2 | [19-oct.pdf](https://images.shulcloud.com/2920/uploads/Documents/Temple-Times/19-oct.pdf) |
| January 2020 | Vol. LXVIII, no. 5 | [20-jan.pdf](https://images.shulcloud.com/2920/uploads/Documents/Temple-Times/20-jan.pdf) |
| June–July 2021 (prior checkpoint) | Vol. LXIX, no. 10 | [21-jun-jul.pdf](https://images.shulcloud.com/2920/uploads/Documents/Temple-Times/21-jun-jul.pdf) |

This is a real **multi-year first-party institutional newsletter collection**. The 2019 issues include writing under Rabbi Batsheva Appel's name (post-Cohon's Temple tenure), and the 2020 issue discusses successor-congregation planning. **No issue from 2000, 2001 or 2015 was found using grounded public filenames**, and the data above neither implies continuity into those years nor authenticates a manuscript. Do not generate speculative earlier filenames from the 2019 naming pattern.

**PDF QA limitation:** The web reader exposed parsed text, and document mastheads were checked. The required web screenshots of the examined PDF title pages failed because the screenshot backend did not resolve PDF content as a screenshot-enabled document; therefore **image-level inspection, file hashes, original-file byte download, and visual page comparisons were not completed**. No claim of digital preservation or author-approved manuscripts.

## Verified: Hearing Voices publishes explicit MP3s for *other* numbered episodes

The first-party [Hearing Voices producer homepage](https://hearingvoices.com/) visibly links three actual MP3 URLs with episode numbers and names:

- **HV101, John Ono Lennon**: `https://hearingvoices.com/news/wp-content/uploads/hours/101JohnOnoLennon.mp3`
- **HV073, Home Team**: `https://hearingvoices.com/news/wp-content/uploads/hours/073HomeTeam.mp3`
- **HV074, Bloody Hell**: `https://hearingvoices.com/news/wp-content/uploads/hours/074BloodyHell.mp3`

These are **exact source-supplied links observed in publisher HTML**, not speculative reconstructions; actual MP3 bytes were not fetched. They establish a publisher-hosted public audio distribution mechanism, but **none corresponds to HV009**. The [producer's HV Series index](https://hearingvoices.com/hv-series/) still identifies **HV009, April 30, 2008, *Shoah: For Holocaust Remembrance Day*** with Rabbi Samuel Cohon as presenter, but its detail-page link failed to fetch. Search for an exact published HV009 MP3 did not identify an authenticated direct URL. **Do not invent `009...` filenames based on the three other links.** No Cohon performance was listened to or verified, and no media rights assessed. HV009 remains a separate independently produced program, not canonical Too Jewish or a Temple class.

## Additional University of Arizona archive clarification

The [Southwest Jewish Archives' Temple Emanu-El institutional page](https://swja.arizona.edu/content/temple-emanu-el) identifies the Tucson congregation and its historic locations. This institutional history is **not** a finding aid or direct custody confirmation of Cohon's later sermons. The university's [SJA 006 Bloom photograph collection](https://swja.arizona.edu/content/bloom-southwest-jewish-archives-photograph-collection-ca-1850-ca-1995) includes Temple-related photographs, but its ca. 1850–1995 collecting range **predates** all of the 2000/2001/2015 original-manuscript targets. A genuine local archive does not automatically establish a relevant late-date holding.

## Conservation and source status

No original or verified playable source was recovered for: the 2000 *Origins of Awareness* Temple original, the delivered 2001 Erev Rosh Hashanah replacement, the separate pre-9/11 undelivered drafts, the complete 2015 *Necessary Chutzpah of Saving Refugees*, 2008 Hearing Voices HV009, or 2013 Temple Podbean classes.

**Core counts unchanged:** 1,265 Too Jewish listings + 316 first-party blog publication records + 26 teaching recordings = **1,607** core source records; **19** supplemental community publications separately. This pass adds **one** public-only verification ledger (with six original bulletin URLs and three unrelated publisher MP3 examples). No core works, recovered media, or audio count increased.

**Rights and production:** All private originals and unreviewed transcripts remain untouched. No full copyrighted article/manuscript/MP3 text was copied into public GitHub; no external contact, merger, deployment, permissions changes, rights claims or workflow change.

## QA state: known environment blocker remains

The last full browser verification attempt failed on the GitHub-hosted Ubuntu 26.04 runner while `verify-archive.yml` pins Playwright 1.55.0. Source-ledger checks passed on that attempt, but Chromium was **not executed**. This metadata-only research task does not authorize changing workflows or claiming that issue is fixed. See `docs/ci-browser-qa-blocker-2026-10-31.md`.
