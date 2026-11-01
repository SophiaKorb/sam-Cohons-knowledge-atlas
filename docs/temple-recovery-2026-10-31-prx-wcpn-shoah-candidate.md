# October 31, 2026 — PRX/WCPN *Shoah* distributor title, not verified HV009 audio

## Source-specific new lead: a named PRX station purchase

A publicly indexed [PRX station page for WCPN](https://exchange.prx.org/station/wcpn?m=false&page=22) lists the following under its **Purchased Pieces** heading:

> HV Special: Shoah (Holocaust Remembrance) — 04/25/22

This is the first concrete **title-level PRX distributor record** located in the investigation that may relate to *Hearing Voices* Holocaust programming. It is meaningfully more specific than merely finding the [Hearing Voices PRX producer group](https://assets1.prx.org/group/hearingvoices/) or its original 2008 [program-series index](https://www.hearingvoices.org/hv-series/).

The source, however, does **not** supply an identified PRX piece number, source-issued direct item link, credited host/presenter, content inventory, enclosure URL, audio bytes or rights terms in the accessible search text. The full station page returned **HTTP 403** in the web reader, so the displayed indexed purchase cannot be independently inspected through the page UI or clicked through to the underlying PRX piece at this time.

### Critical identity distinction: similar name is not a crosswalk

The original *Hearing Voices* publisher index lists **HV009 (April 30, 2008), “Shoah: For Holocaust Remembrance Day”**, and names **Rabbi Samuel Cohon** as its presenter. The separately found PRX purchase list gives a **differently worded title**, *HV Special: Shoah (Holocaust Remembrance)*, associated with **April 25, 2022**.

There is a plausible connection in producer abbreviation and Holocaust theme, but no **verified work identity, master equivalence, presenter credit on the PRX record, or audible voice confirmation**. The 2022 date is the date appearing beside the purchased-piece listing; do **not** treat it as the original HV009 broadcast date, assume an authorized 2008 master is recoverable, or imply the broadcast content is identical. An edited encore, separate special, or different compilation remain live possibilities. Likewise, no original PRX media file was retrieved and PRX's distribution listing confers no copyright permission on the Atlas.

This candidate has been added as a **subordinate cross-reference to the existing HV009 historical lead**, **not** as a fourth lead record, a canonical *Too Jewish* program, Temple Podbean class, or recovered audio. Existing HV009 fields remain `audio_enclosure_url: null`, `audio_bytes_verified: false` and `speaker_voice_verified_by_listening: false`.

### Next evidence gate

Locate an **actual source-issued PRX piece permalink or stable identifier** attached to *HV Special: Shoah (Holocaust Remembrance)*, read original contributor/host credits, and compare its specific program description to the 2008 Hearing Voices HV009 entry. Only if identity is established should recoverable audio bytes or a verified Cohon voice be considered; rights remain a separate gate. Do not guess numbered MP3 filenames, assume 2022 purchase implies media is publicly playable, or contact the station/producer under present restrictions.

## Bounded manuscript recovery search — unchanged findings

This pass also searched independently for Cohon-specific item records via archives/public university and congregation domains, exact original 2000/2015 sermon titles, and September 2001 year/title combinations. Results returned the already-known 2000 attributed mixed-author reproduction, 2015 URJ excerpts, the retrospective Cohon-authored 2001 quotation, and wrong-person American Jewish Archives results. **No dated first-party manuscript accession or authorized original facsimile for the target sermons was identified**. The undelivered 2001 planned drafts remain separated from the delivered Erev Rosh Hashanah replacement.

The previously verified [AJA MS-630 1993 item](temple-recovery-2026-10-31-aja-ms630-original-tucson-sermon.md) is a **Thomas A. Louchheim**, not Cohon, original. AJA MS-674 is a real 2001 thematic sermon collection but **does not list Cohon**. These institutional discoveries must not be upgraded by proximity or thematic relevance.

This is **bounded negative discovery**, not a statement that archival documents cannot exist.

## Repo and QA controls

- [Source-specific PRX crosswalk ledger](../data/verification/prx-wcpn-shoah-title-candidate-2026-10-31.json) contains the date, named station, exact title, source URL, permitted inference and evidence needed to advance.
- The prior [historical-source-leads file](../data/teaching/historical-source-leads.json) still has **three**, not four, records, and the HV009 item remains distinct from canonical *Too Jewish* and 2013 Temple classes.
- Core counts remain **1,265 radio + 316 first-party blog + 26 teaching = 1,607**, with **19 supplemental** published community records. No new published work, sermon original or media was ingested.
- Public metadata and documentation only; no copyrighted program audio or manuscript texts, private original access, permissions changes, external contact, workflow change, merge or deployment.
- Source-ledger tests must assert the 2022 PRX entry is **not** a confirmed link to the 2008 original. Browser QA is independently blocked by the existing Ubuntu 26.04 / Playwright 1.55 Chromium installation issue; do not call it passed without an executed browser step.
