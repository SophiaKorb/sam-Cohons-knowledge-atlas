# Too Jewish Radio — targeted historical link-recovery investigation

**Date:** 2026-10-15 (Arizona)  
**Source dataset:** checked-in `data/episodes-by-year/` files and `data/stats.json`; archived September 22, 2026 HTTP HEAD check.  
**Classification:** metadata and URL triage, **not** confirmed audio recovery.

## Confirmed concentration, by catalog year

| Broadcast year | Catalog records | Previously failed official links |
|---|---:|---:|
| 2004 | 52 | 49 |
| 2005 | 52 | 52 |
| 2006 | 53 | 52 |
| 2007 | 52 | 50 |
| 2008 | 52 | 51 |
| 2009 | 52 | 50 |
| **Total** | **313** | **304** |

The six-year cohort accounts for **304 of 330 (92.1%)** historically failed URLs in the repository's September ledger. These counts were independently recalculated from the six checked-in annual episode files during this investigation, not estimated from page descriptions. Failures in this sampled cohort carry recorded HTTP 404 status.

## Two concrete primary-source URL probes

| Episode ID | Original URL | Historical status | New result |
|---|---|---|---|
| `tj-2004-12-26` | `https://toojewishradio.com/Too%20Jewish%20MP3's/Too_Jewish_12-26-04.mp3` | 404 | 2026-10-15: URL inaccessible through the available web page retrieval tool; **no HTTP GET status or audio verification recorded** |
| `tj-2005-12-25` | `https://toojewishradio.com/Too%20Jewish%20MP3's/Too_Jewish_Tuc_12-25-05.mp3` | 404 | 2026-10-15: URL inaccessible through the available web page retrieval tool; **no HTTP GET status or audio verification recorded** |

Original addresses are retained as source evidence. A web retrieval error is **not** equivalent to a newly verified 404, a missing master recording, or an inability to recover the file elsewhere.

## Alternate first-party source examined

- `https://toojewishradio.podbean.com/` currently has an active publisher-controlled episode archive. Its site presents contemporary episodes, and search discovers an older episode from July 2011, but **neither of the above 2004/2005 episodes was independently located or audio-verified**.
- Because catalog entries from 2004–2009 typically have null `podbean_url`, do not infer missing audio exists on Podbean without an exact episode/date match.
- The repository's 736 previously matched Podbean entries remain metadata correlations, not audio playback tests.

## Triage interpretation

1. Treat the 2004–2009 file cohort as **priority A** for archival recovery rather than randomly rechecking all years. A high concentration of 404s suggests a systematic older-path or storage problem, but its cause is **unknown**, not established.
2. Before classifying a recording irrecoverable, try bounded GET/Range requests, redirects, case variations when supported by a publisher index, publisher backups and contemporaneous web archive captures. Never claim success from search snippets.
3. Ask the program's rights holder or archive maintainer whether masters from 2004–2009 exist in offline storage. This is an inquiry, not a rights grant.
4. Keep original URLs and September HTTP status fields unchanged. Store subsequent attempts in an append-only retry ledger with explicit tool/method, time and evidence type.
5. No source media, derived audio, participant recordings or transcripts were added to GitHub; public playback permissions remain unresolved.

## Actual outcomes

- **304** historical failed links concentrated in 2004–2009 confirmed from checked-in annual datasets.
- **2** concrete historical URLs examined through web retrieval; both returned tool accessibility errors, **not a new definitive HTTP response**.
- **0** formerly failed audio URLs confirmed recovered or playable.
- **0** historical source records overwritten, **0** audio rights approvals inferred.

**Next technical task:** perform bounded GET/Range batch testing from a network environment that exposes status, headers and redirect chains, starting with 2004–2009. Use this record as the triage baseline rather than replacing the original link-check ledger.
