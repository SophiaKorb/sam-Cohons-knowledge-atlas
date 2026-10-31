# October 31, 2026 — repository QA verification and runner incompatibility

**Scope:** Research branch only; report/evidence update without changing the CI workflow, app code, production or publishing anything. An October 31 source-ledger checkpoint added public metadata for Kol Ami's legacy Temple connection, a real 2021 Temple Times issue, and the PRX Hearing Voices producer collection; the new source types remain marked as **unproven custody of the requested manuscripts or HV009 media**.

## Observed GitHub Actions runs

- [Run 41238432791](https://github.com/SophiaKorb/sam-Cohons-knowledge-atlas/actions/runs/41238432791) — test/verification-assertion commit `f3a27bf6b413dd5f18568cf61fb1d61dfac5bb37`: **overall failed in browser installation step**, not from the newly committed provenance assertions.
- [Run 41238352648](https://github.com/SophiaKorb/sam-Cohons-knowledge-atlas/actions/runs/41238352648) — initial structured metadata commit `7612f102ab6e6955f56905addd241fe67ffe13da`: **same runner/browser failure** before any browser QA.

Job-step results for 41238432791 were:

1. Rebuild radio site bundles from tracked source files — **PASS**
2. Check regenerated bundles against committed build — **PASS**
3. Targeted read-only publisher audio probe tests — **PASS**
4. Source ledger and browser-bundle-count consistency — **PASS**
5. Parse JavaScript scripts and browser bundles — **PASS**
6. Install Chromium test runner — **FAIL**
7. Verify searchable site in Chromium — **SKIPPED / NOT TESTED**

**Exact cause (GitHub job log):** `.github/workflows/verify-archive.yml` uses `runs-on: ubuntu-latest`, a moving runner image, and installs `playwright==1.55.0` before `python -m playwright install --with-deps chromium`. On October 31 GitHub supplied **Ubuntu 26.04**, and Playwright aborted:

```text
BEWARE: your OS is not officially supported by Playwright; installing dependencies for ubuntu26.04-x64 as a fallback.
Cannot install dependencies for ubuntu26.04-x64 with Playwright 1.55.0-beta-1756314050000!
Failed to install browsers
Error: ERROR: Playwright does not support chromium on ubuntu26.04-x64
```

This is a **test-infrastructure compatibility defect**, not evidence of a browser behavior regression or a pass. The last complete green browser QA is the earlier verified checkpoint, **not** the October 31 branch state. As of this report **full comprehensive QA is incomplete**, although all five non-browser checks passed.

## Source-verified remediation choices (no changes applied)

The [official Playwright Python release notes](https://playwright.dev/python/docs/release-notes) document that **Playwright 1.61 adds Ubuntu 26.04 support**. [System requirements](https://playwright.dev/python/docs/intro) likewise include Ubuntu 26.04. Two possible workflow repairs need independent CI verification:

- **Low-diff deterministic runner repair:** explicitly pin `runs-on: ubuntu-24.04` in `.github/workflows/verify-archive.yml` and retain existing Playwright 1.55.0, then rerun the full CI; this avoids a Playwright API upgrade but is not verified until tested.
- **Modern runner repair:** upgrade the Playwright dependency in the workflow from `1.55.0` to a release that supports Ubuntu 26.04 (at least `1.61.0`), rerun browser QA and inspect test compatibility. Version 1.61 is known supported; whether the existing browser test suite remains unchanged is **not yet verified**.

**Authorization boundary:** The user's scope is to *commit verified public metadata only* on the research branch. A workflow patch is executable source/configuration, outside that explicit commit boundary. **No workflow file, build/test source or production branch was modified to force green CI.** No reruns claimed to have passed. **Ready for Human Review:** approve a test-infrastructure-only configuration change if full browser QA is required under the changed GitHub runner.

## Other scope and integrity checks

- The source data readback confirms three *source/archival holding leads* with explicit **false** status for target manuscript/audio custody, along with three false-positive collection exclusions.
- Historical 2000/2001/2015 manuscript original flags and 2008/2013 audio byte status remain **false**. No new core record was counted; **1,265 radio + 316 first-party blog + 26 teaching = 1,607**, plus **19** supplemental publications.
- Private originals, metadata about unrelated private files, manuscripts and media have not been copied, and no external contact, merge, deployment, rights change or public manuscript/transcript publication was performed.
