# Temple Emanu-El Tucson — 2000 primary-history context and 2015 newsletter false positives

**Date:** October 31, 2026. **Scope:** Public-source historical research only, within `research/2026-10-21-too-jewish-intake`. This is a verification appendix to the October 31 multiissue/producer-audio source checkpoint, not a catalogue expansion or original manuscript recovery.

## A. First-party Tucson history narrows the documented 2000 institutional events

A separate [detailed Kol Ami institutional history](https://www.katucson.org/history-v2) identifies two specific 90th-anniversary events at the original Temple Emanu-El of Tucson:

- **March 11, 2000:** Heritage Shabbat at the historic Stone Avenue Temple.
- **March 17, 2000:** separate recognition of congregants Joan and Donald Diamond for supporting the Temple.

These details document **real Tucson institutional commemorations during 2000**, but **do not** authenticate Rabbi Samuel M. Cohon's *The Origins of Awareness*, separately attributed to **Yom Kippur 5761, October 8–9, 2000**. The earlier sermon remains a substantial third-party mixed-author compilation reproduction, not an author-approved original. Neither anniversary event is a newly recovered Cohon sermon, audio master, manuscript or delivery date for the Yom Kippur address.

[An August 20, 2010 Arizona Jewish Post report](https://azjewishpost.com/2010/jewish-history-museum-celebrates-with-centennial-exhibit/) describes an old Temple Emanu-El newsletter exhibited at the Jewish History Museum in Tucson's original Stone Avenue synagogue, alongside historic photographs and other early Jewish community artifacts. This is an **early legacy publication display**, not evidence of the museum currently holding a 2000, 2001 or 2015 Cohon original. No museum contact or private collection access was undertaken.

## B. False-positive 2015 “Temple Times” issues — exclude different congregation

Two 2015 PDF documents returned by a broad web search carry a misleadingly similar *Temple Times* masthead:

- [March/April 2015](https://images.shulcloud.com/15008/uploads/Newsletter/Newsletter-201503.pdf)
- [September/October 2015](https://images.shulcloud.com/15008/uploads/Newsletter/Newsletter-201509.pdf)

Both identify **Temple Beth Shalom**, *established 1953*, as publisher and refer to the **United Synagogue of Conservative Judaism**. Their original ShulCloud collection identifier is `15008`, and their files reside at `/uploads/Newsletter/`.

The verified Tucson first-party *Temple Times* PDFs instead identify **Temple Emanu-El, 225 North Country Club Road, Tucson**, and are at **ShulCloud collection `2920`**, `/uploads/Documents/Temple-Times/`; see [previous six-issue checkpoint](temple-recovery-2026-10-31-multiissue-audio-links.md).

**Editorial rule:** Do not count, infer, merge, or search within the Temple Beth Shalom 2015 issues as though they were the Tucson Temple's 2015 Rosh Hashanah bulletin or Cohon sermon. Similar newsletter titles, identical year and common hosting infrastructure are *not institution identity evidence*. This source-specific rejection is recorded as a concrete false positive, not an archive-wide claim that no 2015 Tucson bulletins survive.

## C. Original sermon and media gates unchanged

The [public author-operated blog](https://www.rabbisamcohon.com/) is real, but its currently visible later-era posts do not provide evidence of the exact 2000/2001/2015 Temple-era original works. The [Hearing Voices primary-series index](https://www.hearingvoices.org/hv-series/) still identifies **HV009**, April 30, 2008, *Shoah*, with Cohon as presenter; a renewed first-party index-link traversal to its original detail page gave a cache miss. No authenticated direct source MP3 or binary/voice evidence was recovered. No original 2013 Temple class RSS GUID or enclosure was recovered.

The actual 2000 Yom Kippur original, 2001 Erev Rosh Hashanah delivered replacement manuscript, 2001 pre-9/11 **undelivered** drafts, and 2015 *Necessary Chutzpah* manuscript remain missing/unverified. The only first-party 2001 text evidence remains the author's later self-quotation, not a contemporaneous original.

**Count/release fence:** **1,265** Too Jewish radio + **316** first-party blog + **26** teaching entries = **1,607 core**, plus 19 separate community-publication records. **Zero** additions or new recoveries. No original files changed, manuscripts/transcripts copied, private material exposed, outreach, rights assessment, merge, deployment or workflow modification.

## QA

The machine-readable source and exclusion findings are in [`temple-2000-context-and-false-positive-2015-bulletins-2026-10-31.json`](../data/verification/temple-2000-context-and-false-positive-2015-bulletins-2026-10-31.json). Regression tests must enforce correct institution identities, date/non-original status, counts, and preservation controls. **Known independent CI limitation:** GitHub `ubuntu-latest` migrated to Ubuntu 26.04 while the workflow pins Playwright 1.55; non-browser source QA runs, but Chromium installation can fail. No workflow changes are authorized here; browser QA must not be reported as passing without execution.
