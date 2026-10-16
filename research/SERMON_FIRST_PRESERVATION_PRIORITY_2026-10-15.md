# Cohon Archive — sermon-first preservation and transcription priority

**Decision recorded:** 2026-10-15. The immediate archive priority is **(1) sermon manuscripts, (2) original audio acquisition and preservation, (3) machine transcription, (4) verified editorial transcripts**. Historical 2004–2009 Too Jewish missing-audio recovery is secondary and should not displace this work.

## Direct inventory findings (ChatGPT Library, 2026-10-15)

- `/Writing` contains a substantial collection of sermon DOCX manuscript files, including 5785–5787 material. A folder listing yielded 96 visible items with additional pagination; **96 is not a certified sermon total** because the folder also contains research notes, ZIPs and Too Jewish files.
- The root Library contains multiple unrenamed `audio##########.m4a` recordings and apparent size-matched copies of Introductory Judaism Classes 1–4. Matching file sizes suggest duplicate candidates, **not byte-confirmed duplicates**.
- The `/Judaism for Beginners` folder contains four original class M4A recordings and a Torah Tykes recording, plus machine-generated transcript derivatives for multiple sessions. These are teaching material, **not sermon recordings**.
- The Library also contains Too Jewish full-show audio and short clip files, including a September 27, 2026 recording; these must not be counted as sermon recordings.
- No sermon-specific M4A or MP3 recordings were confidently identified by title in the scoped Library audio-file inventory. This is a *local search finding*, not proof that sermon recordings do not exist in other providers or source websites.

## Required sermon object model

One *work* can have multiple *manifestations*:

- Work ID, exact manuscript title, likely delivery date and Jewish calendar date (each with evidence and uncertainty), Torah portion/occasion, author.
- Original manuscript: source file ID/path/provider, byte count, SHA-256 on actual bytes, accession timestamp, permission, not a public text.
- Original audio: first-party publisher URL or private-file ID, verified audio bytes, duration, codec, SHA-256, recording date when evidenced, speaker confidence, public/private access status.
- ASR transcript: model/service, run date, language, source-audio SHA-256, word timestamps if available, uncertainty flags; never labeled verbatim-verified.
- Editorial transcript: reviewed against original audio, review scope/timecodes, Hebrew and names checked, speaker label checks and corrections.
- Derived public excerpts: exact manuscript/audio anchors, publisher provenance, rights and editorial approval documented separately.

## Preservation order

1. Inventory sermon manuscripts by explicit title/occasion and group likely duplicates, preserving every original. Avoid overwriting filenames or assuming near-identical titles are identical sermons.
2. Locate *sermon audio* from publisher websites, connected private source libraries, and the author's original files. Save durable private archival copies only where authorized, record SHA-256 and original URL immediately. **Do not substitute class recordings or Too Jewish episodes.**
3. Transcribe only after recording bytes are saved, hashed, and tied to a sermon work ID. Keep raw ASR and cleaned versions separately; use Hebrew-sensitive review.
4. Compare transcript with manuscript but do not silently rewrite spontaneous delivery to match the prepared text. Maintain manuscript, spoken delivery and corrections as distinct evidence.
5. Publish only metadata and expressly approved excerpts. Classroom/participant voices and private unpublished originals stay private.

## Readiness

**Archive inventory and source relationships:** technically executable. **Audio downloads:** only from accessible sources under authorized access, with actual file verification. **Transcription:** blocked per item until audio is recoverable and readable by an available transcription engine. **Audio authentication, editorial acceptance and public reuse rights:** separate human review gates.

No bulk transcript production, audio byte acquisition, sermon-by-sermon verification, or website publication is claimed by this priority decision.
