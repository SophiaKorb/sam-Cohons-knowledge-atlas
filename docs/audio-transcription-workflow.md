# Sam M. Cohon archive — private audio transcription workflow

Updated October 14, 2026 (Arizona). This is the draft-branch research protocol, **not** permission to share or publish any recording or transcript.

## Ground rules and source recovery

1. Locate the original first-party MP3/M4A or a permissioned export. Record the episode/class ID, exact source URL, original filename, broadcast/class date with provenance, MIME/codec, running time and SHA-256; check that the **bytes decode**, not merely that HEAD succeeds.
2. Preserve original bytes without editing, when storage/rights permit. Record any trimmed samples separately with absolute time offsets and transformation commands. Keep unpublished audio **outside the public GitHub repository**.
3. Verify rights and approval for third-party audio processing before transferring any private or unpublished recording. Public listenability is not equivalent to a redistribution or training license.
4. Create a raw **unaltered** transcription with the exact tool/model, settings and time range recorded. Machine recognition is provisional; neither the raw transcript nor an automated confidence score is a verbatim scholarly source.

## Choosing the transcription route

| Case | Default | When to use TurboScribe |
| --- | --- | --- |
| Short technical sample and reproducible first-pass QA | Local offline Whisper/faster-whisper | Optional comparison if local ASR is clearly unreliable |
| Full *Too Jewish* interview, especially more than ~15 minutes | Accurate source download, then a batch transcription pass | **Preferred secondary/long-form pass** when an authorized TurboScribe account and suitable processing rights are available |
| Multiple speakers, overlap, Hebrew or Yiddish, names, poor audio, or uncertain timestamps | Preserve short WAV excerpt and source offsets; compare ASR systems | Turn on speaker recognition if useful, choose the original audio language rather than automatic translation, and export a timestamped transcript |
| Original 16-class Introductory Judaism lecture materials | Reuse preexisting private audio and **ten already preserved unedited TurboScribe RAW transcript files**, carefully joined to true class provenance | Use TurboScribe for the **missing or newly recovered lesson audio**, not to overwrite existing raw records or invent dates |

[TurboScribe](https://turboscribe.com/) supports MP3/M4A and other audio uploads, speaker recognition and TXT, DOCX, SRT and VTT exports. Treat it as an **optional external service**, not an automatic data transfer. There is currently no direct TurboScribe app connection available through this ChatGPT session; use user-authorized account upload/export and import the results back into the private Library when available. Do not paste privileged API credentials into a public repo or GitHub Actions.

## Provenance, QA and publication gates

- Save raw tool exports separately in the private ChatGPT Library: `/Writing/` for radio and `/Judaism for Beginners/` for the teaching course. Keep original TXT/SRT/VTT and the tool's submission date, mode, language, speaker-recognition settings, segment time offsets, and source checksum. Mark **raw_unreviewed**.
- For a second engine, save its unedited output separately (e.g., `TURBOSCRIBE_RAW`); never silently use it to correct Whisper. Compare both to **actual playback**, focusing on Sam's name, names of guests, Hebrew and Yiddish, biblical quotations, dates, contact addresses, and theological nuance.
- Editorial review: listen through at least the targeted passages, attach absolute timestamps, label speakers only when supported by listening, log corrections and uncertainties; preserve raw originals and issue a new version labeled **human_reviewed** only after a real person checks it.
- Transcripts or excerpt quotations need additional rights, context, and publication approval. The public Knowledge Atlas may index factual **metadata only** until these gates are met. Do **not** count private raw fragments as completed episode transcripts.
- Distinguish the separately preserved **Introductory Judaism** raw TurboScribe files from the `Too Jewish` radio corpus; do not increment either catalogue count from private supporting evidence.

## First Too Jewish radio pilot (not a completed episode)

- September 27, 2026 — Lynn Golodner; **00:30–03:00 sample** (150 seconds) from 54:54 original MP3.
- Official MP3 SHA-256: `819f02fa9585df7728cabcffa251c69348f31d90bd28aeb71d42e71581263b0c`.
- Decoded on an ephemeral GitHub-hosted worker, then processed via faster-whisper `tiny.en` on 16kHz mono audio. **43 timestamped raw segments / about 395 words**. Speaker identification, transcription accuracy, Hebrew and rights **not yet reviewed**.
- Raw segment text was public-key encrypted before artifact upload; decrypted using the private key **outside GitHub** and saved to private Library at `/Writing/Too_Jewish_2026-09-27_Raw_ASR_30-180s_PRIVATE.{json,txt}` with QA notes. No MP3 bytes or transcript lines are present in the public repository.
- Publisher head request passed HTTP 200/`audio/mpeg` October 15 UTC. The prior verified episode-link ledger is unchanged apart from that targeted result. **One 150-second machine draft != one transcribed episode**; `transcript_status` remains `not_ingested` and fully reviewed radio transcripts remain **zero**.
- This initial short Whisper result is a natural candidate for an independent **TurboScribe** full-episode pass if authorized, with speaker recognition and careful audio reconciliation.

## Next action

Obtain the September 27 audio for **actual editorial playback** and decide if TurboScribe processing is authorized. If yes, transcribe the remaining full episode and compare timestamped outputs, preserving raw text and marking uncertainties. Continue the five-episode pilot, including the 2020 interview with Rabbi Baruch Cohon, only as permissions and actual audio access permit. No merge, public transcripts, or deployment.
