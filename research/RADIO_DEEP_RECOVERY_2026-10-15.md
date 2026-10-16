# Deep radio recovery cycle — 2026-10-15

## Verified during this cycle

- The first-party episode index at https://www.toojewishradio.com/too_jewish_shows.htm is accessible and still lists the broadcasts dated **2004-12-26** (Judith Cohen) and **2005-12-25** (Allen Salkin).
- The original MP3 URL for 2004-12-26 is inaccessible through the web retrieval interface. This is **not** a reliable fresh HTTP 404 result and **not** proof the recording was lost.
- A direct bounded GET attempted from the isolated container failed at DNS resolution; consequently it returned **no usable HTTP response**, no byte signature, and no recovered audio.
- The Podbean first-party podcast is accessible and currently advertises hundreds of episodes; no exact recovered copy of these two historical broadcasts has been established.
- The checked-in historical ledger attributes 304 of 330 failed radio MP3 links to 2004–2009. This prioritization comes from archival metadata, not newly performed comprehensive HTTP tests.

## Executable implementation

The separate script `scripts/recheck_legacy_audio.py` now performs bounded GET/Range attempts (at most 1024 response bytes), logs HTTP/network errors and possible MP3 signatures into **append-only JSONL**, and retains the original catalog URL. This is a recovery *verification utility*, not a download tool. A MIME match or MP3 header is only an audio candidate; actual recording identity and permission need later review.

Example after cloning the repository in a network-enabled environment:

```bash
python3 scripts/recheck_legacy_audio.py --episodes data/episodes-by-year/2004.json --ledger evidence/retries-2004.jsonl --limit 10
```

For each year 2004–2009, rerun with a separate ledger or maintain a combined append-only file. Review network errors independently rather than automatically classifying them as dead. Avoid committing full audio, tokens, private participant recordings, or sensitive logs.

## Boundaries and status

**Recovered recordings: 0.** No new audio playback or byte-level identity verification, no rights approvals, no altered historical URL status fields, and no deployment. The next measurable stage is running the new checker in an environment with reliable access to the original host, then testing official backups for those episodes that return confirmed 404/410 responses.
