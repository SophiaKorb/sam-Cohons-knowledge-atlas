#!/usr/bin/env python3
"""Offline regression tests for safe, non-mutating official-MP3 diagnostics."""
from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts import verify_links as checker

URL = "https://toojewishradio.com/Too%20Jewish%20MP3's/Too_Jewish_2026-09-27.mp3"
ROW = {"id": "tj-2026-09-27", "broadcast_date": "2026-09-27",
       "official_audio_url": URL, "official_link_status": "not_checked"}
NO_AUDIO = {"id": "tj-2026-10-04", "broadcast_date": "2026-10-04",
            "official_audio_url": None, "official_link_status": "not_listed"}


class SelectionTests(unittest.TestCase):
    def test_exact_id_selection_and_rejection(self):
        self.assertEqual(checker.select_records([ROW, NO_AUDIO],
                         ["tj-2026-10-04"])[0]["id"], NO_AUDIO["id"])
        for ids in ([], ["missing"], [ROW["id"], ROW["id"]], [ROW["id"]] * 21):
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                checker.select_records([ROW, NO_AUDIO], ids)

    def test_empty_folder_and_duplicate_index_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            with self.assertRaises(ValueError):
                checker.load_records(path)
            (path / "2025.json").write_text(json.dumps([ROW]), encoding="utf-8")
            (path / "2026.json").write_text(json.dumps([ROW]), encoding="utf-8")
            with self.assertRaises(ValueError):
                checker.load_records(path)


class ProbeTests(unittest.TestCase):
    @staticmethod
    def run_with(code: str, returncode: int = 0, stderr: str = ""):
        def runner(cmd, **kwargs):
            assert cmd[-2:] == ["--", URL], "Curl URL must follow --"
            return SimpleNamespace(stdout=code, returncode=returncode, stderr=stderr)
        return runner

    def test_live_missing_and_inconclusive_are_distinct(self):
        for code, rc, state in [
            ("200", 0, "responded_successfully_to_HEAD"),
            ("302", 0, "responded_successfully_to_HEAD"),
            ("404", 0, "HEAD_reported_missing"),
            ("410", 0, "HEAD_reported_missing"),
            ("403", 0, "inconclusive"),
            ("405", 0, "inconclusive"),
            ("503", 0, "inconclusive"),
            ("000", 6, "inconclusive"),
            ("unexpected", 0, "inconclusive"),
        ]:
            with self.subTest(code=code, rc=rc):
                self.assertEqual(checker.probe_url(
                    URL, runner=self.run_with(code, rc))["observed_state"], state)

    def test_no_arbitrary_urls_and_network_exceptions(self):
        for url in ["http://toojewishradio.com/a.mp3",
                    "https://other.example/a.mp3",
                    "https://toojewishradio.com.evil.example/a.mp3"]:
            with self.assertRaises(ValueError):
                checker.probe_url(url, runner=self.run_with("200"))
        def bad(*args, **kwargs):
            raise OSError("network unreachable")
        self.assertEqual(checker.probe_url(URL, runner=bad)["observed_state"],
                         "inconclusive")

    def test_no_url_is_not_probed_and_status_untouched(self):
        def bad(*args, **kwargs):
            self.fail("A null audio URL must not trigger a request")
        report = checker.run_checks([ROW, NO_AUDIO], [NO_AUDIO["id"]], probe=bad)
        self.assertEqual(report["findings"][0]["observed_state"],
                         "no_official_audio_url")
        self.assertEqual(NO_AUDIO["official_link_status"], "not_listed")


class ReadOnlyTests(unittest.TestCase):
    def test_cli_never_modifies_canonical_record_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "data" / "episodes-by-year"
            base.mkdir(parents=True)
            file = base / "2026.json"
            original = json.dumps([ROW, NO_AUDIO], ensure_ascii=False, indent=2)
            file.write_text(original, encoding="utf-8")
            def fake_probe(url):
                return {"observed_state": "inconclusive", "http_status": None,
                        "error": "blocked"}
            with patch.object(checker, "EPISODE_DIR", base), \
                 patch.object(checker, "probe_url", fake_probe):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = checker.main(["--id", ROW["id"]])
            self.assertEqual(code, 0)
            self.assertEqual(file.read_text(encoding="utf-8"), original)
            self.assertEqual(json.loads(out.getvalue())["findings"][0]
                             ["catalogued_link_status_unchanged"], "not_checked")


if __name__ == "__main__":
    unittest.main()
