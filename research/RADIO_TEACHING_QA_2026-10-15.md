# Radio and teaching archive — evidence QA, 2026-10-15

## Scope

This review checks **existing repository claims** against checked-in stats and the accessible first-party Beit Simcha recording-listing page. No batch radio MP3 network recheck or audio listening was performed. The new `data/teaching/private-source-crosswalk.json` intentionally contains only privacy-safe associations.

## Radio baseline (the 2026-09-22 audit, not a fresh link check)

| Metric | Value | Meaning |
|---|---:|---|
| Broadcast records | 1,261 | Catalog records over 2002–2026 |
| Direct audio URL listed | 1,219 | URL present in catalog |
| HEAD reported live | 889 | HEAD succeeded during September check, not playback verified |
| HEAD reported dead | 330 | Failed under recorded link-check classification; needs GET/browser retest before declaring permanently missing |
| No MP3 URL listed | 42 | Catalog lacks a direct URL; not proof no audio exists |
| Matched Podbean | 736 | Catalog match, not direct listening |
| Transcript/audio content reviewed | 0 | No radio claims should be attributed to unheard episodes |

**Consistency checks:** 889 + 330 = 1,219 links tested; 1,219 + 42 = 1,261 total records. The 330 `dead` link ledger entries must not be presented as permanently lost recordings without re-testing via range-GET / redirect handling / publisher archive review. Some servers reject HEAD while serving GET. Keep the historical machine status immutable; record later checks in new timestamped fields.

### Next radio link audit protocol

1. Recheck each formerly non-live URL with HEAD and a bounded HTTP GET (Range when supported), follow redirects, and record exact status code, final URL, content type, elapsed time, and error class.
2. Do not download full recordings just to test existence; cap network transfer and verify file signatures where permitted.
3. Distinguish 404/410, 403/429, timeouts/TLS failures, redirect loops, HTML denial pages and confirmed valid audio content.
4. Search publisher and Podbean equivalents for truly inaccessible links. Retain the original URL, observation timestamp and replacement provenance; never silently rewrite history.
5. Introduce `last_checked_at`, `check_method`, `http_status`, `content_type`, `redirect_target`, `retrieval_evidence` and `rights_state` only on actually checked records.
6. Keep broadcast guest/topic inference separate from the audio evidence. Never infer episode guest speech from keyword categories.

## Teaching listing / private holdings

On October 15, the first-party Beit Simcha recording-listing webpage was independently opened and still visibly contained the listed course sequence, including Classes 1–16, History of Zionism, Zohar and Adult B'nai Mitzvah. The repeated History of Zionism Class One item persists. Source: https://beitsimchatucson.org/videocasts-from-beit-simcha

The machine-readable private-source crosswalk associates 11 public teaching catalog records with archival holdings or candidate transcript matches, including Classes 1–5, 7, 10–13 and 16. These are **relationships, not eleven newly recovered works**. All eleven remain `transcript_audio_verified: false` and `public_republication_approved: false`.

The existing teaching dataset stores `published_date` even where the first-party listing title gives a *class session date*. Future schema should distinguish `session_date`, `listing_publication_date`, and `date_basis`. Do not assert that every currently populated `published_date` is the date the webpage or audio was first published.

## Material gaps and safe handling

- No audio authentication was conducted on candidate Class 2 concepts-of-God transcript. The competing legacy `Class 4.txt` label is not sufficient evidence.
- No original private audio was placed into this public GitHub repository.
- No participant speech or unpublished manuscript text was copied into public data.
- The Shema MP3 variants and Torah Tykes song medley are separate archival manifestations; neither automatically validates lesson playback or recording rights.
- No human approval, publisher rights clearance or public course deployment was performed.

## Release gates

**Ready for human review, not cleared:** Rabbi editorial fidelity; original-audio listening and spoken-word checks; classroom participant privacy; audio and manuscript reuse rights; explicit publication approval. Keep technical metadata completion distinct from these decisions.
