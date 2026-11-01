#!/usr/bin/env python3
"""Check that the tracked, source-first archive and published-site snapshots agree.

Runs entirely offline. This validates metadata integrity, not audio access,
interpretive accuracy, intellectual-work deduplication, or screen-reader use.
"""
from collections import Counter
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DIST = ROOT / "dist"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_js_array(path: Path, prefix: str, suffix: str):
    data = path.read_text(encoding="utf-8").strip()
    assert data.startswith(prefix) and data.endswith(suffix), f"Unexpected JS bundle: {path}"
    return json.loads(data[len(prefix):-len(suffix)])


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    radio = [
        row for path in sorted((DATA / "episodes-by-year").glob("*.json"))
        for row in load(path)
    ]
    stats = load(DATA / "stats.json")
    writing = load(DATA / "writings" / "beit-simcha-blog.json")["records"]
    standalone = load(DATA / "writings" / "rabbisamcohon-blog.json")
    if isinstance(standalone, dict):
        standalone = standalone["records"]
    wstats = load(DATA / "writings" / "stats.json")
    sources = load(DATA / "writings" / "sources.json")["sources"]
    teaching = load(DATA / "teaching" / "beit-simcha-audiocasts.json")
    if isinstance(teaching, dict):
        teaching = teaching["records"]

    require(len(radio) == stats["total_records"], "Radio source count mismatch")
    # Transcript pilot is private metadata only: never conflate 150 seconds of raw
    # Whisper output with a complete, editorially reviewed radio episode.
    pilot = load(DATA / "verification" / "too-jewish-2026-09-27-asr-private-pilot.json")
    policy = (ROOT / "docs" / "audio-transcription-workflow.md").read_text(encoding="utf-8")
    require(pilot["episode_id"] == "tj-2026-09-27" and pilot["sample_duration_seconds"] == 150,
            "Raw radio ASR sample provenance missing or inaccurate")
    require(pilot["raw_timed_segment_count"] == 43 and pilot["raw_approximate_word_count"] == 395,
            "Private raw ASR sample totals changed unexpectedly")
    require(not pilot["reviewed_against_audio"] and not pilot["full_episode_transcribed"] and
            not pilot["transcript_text_in_public_git"], "Private ASR pilot misrepresented")
    require(pilot["public_catalogue_episode_transcript_status"] == "not_ingested",
            "Raw pilot must not be counted as ingested episode transcript")
    followup = pilot["second_pass"]
    require(followup["source_checksum_match"] is True and
            followup["window_seconds"] == [30, 330] and
            followup["segments"] == 74 and followup["recognized_words"] == 564,
            "Independent private machine sample metadata inconsistent")
    require(followup["music_interval_seconds"] == [214.5, 303.2] and
            followup["review_windows"] == 11 and
            0.94 < followup["comparison_ratio"] < 0.95,
            "Comparative listening QA notes inconsistent")
    boundary = pilot["boundary_audio_review"]
    require(boundary["source_sha256_reconfirmed"] is True and
            boundary["boundary_seconds"] == [550, 1100, 1650, 2200, 2750] and
            boundary["raw_asr_start_minus_previous_end_seconds"] == [-1.53, -0.23, 0.46, 0, 0.08],
            "Original audio boundary alignment evidence incorrect")
    require(boundary["boundary_clips"] == 5 and
            boundary["boundary_clip_duration_seconds"] == 24 and
            boundary["raw_machine_segments_reproduced_unchanged"] == 823 and
            boundary["priority_uncertainty_topics"] == 11,
            "Private boundary review item counts changed")
    require(boundary["speech_word_changes_applied"] == 0 and
            boundary["human_listener_audio_verified"] is False and
            boundary["speaker_labels_verified"] is False and
            boundary["music_lyrics_verified"] is False and
            boundary["rights_reviewer_approved"] is False,
            "Machine sound QA is not a human-reviewed transcription")
    for key in ("private_zip_sha256", "private_report_sha256",
                "annotated_derivative_sha256"):
        require(len(boundary[key]) == 64, "Original-audio boundary review SHA-256 missing")

    full = pilot["full_private_first_pass"]
    require(full["status"] == "complete_duration_raw_machine_draft_private_not_human_reviewed"
            and full["source_original_sha256_verified"] is True
            and full["original_mp3_bytes"] == 79065806
            and full["original_mp3_preserved_in_private_library"] is True,
            "Original recording's private checksum-provenance missing")
    require(full["raw_shards"] == 6 and full["raw_segments"] == 823
            and full["raw_words"] == 7765 and full["audio_grounded_review_clips"] == 13
            and full["internal_chunk_cut_seconds"] == [550, 1100, 1650, 2200, 2750],
            "Full episode raw ASR source QA totals or boundaries inconsistent")
    require(full["public_archive_transcript_status"] == "not_ingested"
            and full["machine_similarity_is_not_accuracy"] is True
            and full["human_listening_verified"] is False
            and full["editorial_episode_approved"] is False
            and full["rights_for_publication_approved"] is False
            and full["public_raw_media_or_transcript_committed"] is False
            and full["ephemeral_runner_removed"] is True
            and full["direct_turboscribe_used"] is False,
            "Private ASR must never be promoted to reviewed or published transcript")
    require(followup["private_library_saved"] is True and
            followup["human_audio_review"] is False and
            followup["episode_complete"] is False and
            followup["turboscribe_used"] is False and
            followup["raw_audio_or_transcript_committed"] is False,
            "Raw private pilot must not be represented as a finished episode")

    require("TurboScribe" in policy and "third-party" in policy and "human_reviewed" in policy,
            "Optional TurboScribe selection, privacy or QA guidance missing")
    require(len({r["id"] for r in radio}) == len(radio), "Radio IDs not unique")
    require(dict(Counter(str(r["year"]) for r in radio)) == stats["year_counts"], "Year counts mismatch")
    require(dict(Counter(r["official_link_status"] for r in radio)) == stats["link_status_counts"], "Link-status counts mismatch")
    require(sum(stats["role_counts"].values()) == len(radio), "Radio role counts mismatch")
    require(all(r["transcript_status"] == "not_ingested" for r in radio), "Unexpected transcript-review claim")
    require(len(writing) == wstats["beit_simcha_blog_records"], "Writing source count mismatch")
    require(len(standalone) == wstats["standalone_blog_records"], "Standalone source count mismatch")
    require(len(writing) + len(standalone) == wstats["source_records_total"], "Writing totals mismatch")
    require(len({r["url"] for r in writing}) == len(writing), "Blog canonical URLs not unique")
    require(len(teaching) == 26, "Unexpected teaching listing count")
    hias_2015 = load(DATA / "verification" / "hias-2015-primary-signatory-witness-2026-10-31.json")
    require(hias_2015["research_date"] == "2026-10-31" and
            len(hias_2015["records"]) == 1 and
            hias_2015["records"][0]["id"] == "HIAS-2015-REFUGEE-RABBINIC-LETTER-COHON-SIGNATORY",
            "HIAS 2015 source must be an individually identified, single public signatory witness")
    hias_record = hias_2015["records"][0]
    require(hias_record["source_publisher"] == "HIAS" and
            hias_record["source_public_url"] ==
            "https://hias.org/wp-content/uploads/hias_1000_rabbis_support_refugees.pdf" and
            hias_record["text_document_date"] == "2015-12-02" and
            hias_record["signatory_list_as_of"].startswith("2015-12-04") and
            hias_record["subject_name_as_printed"] == "Rabbi Samuel M. Cohon - Tucson, AZ" and
            hias_record["source_evidence_tier"] ==
            "primary_organization_hosted_contemporaneous_signatory_list_text_verified" and
            hias_record["source_list_reported_count"] == 1216,
            "HIAS witness requires exact first-party dated source, printed named signatory and reported count")
    require(hias_record["authored_work_classification"] ==
            "collectively_signed_statement_not_an_individually_authored_sermon" and
            hias_record["distinct_from_target_sermon"]["original_temple_sermon_manuscript_recovered"] is False and
            hias_record["distinct_from_target_sermon"]["text_shared_with_original_sermon_verified"] is False and
            hias_record["full_text_ingested"] is False and
            hias_record["copyright_rights_cleared"] is False and
            hias_record["core_catalogue_count_included"] is False and
            hias_record["supplemental_publications_count_included"] is False and
            all(value is False for value in hias_2015["unchanged_recovery_flags"].values()) and
            hias_2015["unchanged_counts"] == {
                "radio": 1265, "first_party_blog": 316, "teaching": 26,
                "core_total": 1607, "supplemental_publication_records": 19},
            "HIAS signatory letter must not be misclassified as original sermon or counted as individually authored publication")
    require(all(value is True for value in hias_2015["release_gates"].values()),
            "HIAS evidence gate must preserve privacy, no contact and no production changes")
    hias_note = (ROOT / "docs" / "temple-recovery-2026-10-31-hias-primary-source.md").read_text(encoding="utf-8")
    require("1216" in hias_note.replace(",", "") and
            "signed rather than individually authored" in hias_note and
            "not" in hias_note and
            "1,607" in hias_note and "HIAS" in hias_note,
            "HIAS primary source checkpoint missing date/count or evidence-tier caveat")
    context_2000 = load(DATA / "verification" / "temple-2000-context-and-false-positive-2015-bulletins-2026-10-31.json")
    events_2000 = context_2000["first_party_historical_context"]
    reject_2015 = context_2000["same_title_false_positive"]
    require(context_2000["review_date"] == "2026-10-31" and
            events_2000["source_url"] == "https://www.katucson.org/history-v2" and
            {e["date"] for e in events_2000["date_specific_events"]} == {"2000-03-11", "2000-03-17"} and
            events_2000["original_yom_kippur_2000_manuscript_confirmed"] is False and
            events_2000["original_2001_erev_rosh_hashanah_manuscript_confirmed"] is False and
            events_2000["original_2015_refugee_sermon_confirmed"] is False,
            "March 2000 heritage events cannot authenticate October 2000 or other historical sermons")
    require(len(reject_2015["identified_docs"]) == 2 and
            all(r["owning_congregation"] == "Temple Beth Shalom" and
                r["shulcloud_collection"] == "15008" and
                "/15008/uploads/Newsletter/" in r["url"]
                for r in reject_2015["identified_docs"]) and
            reject_2015["separate_verified_tucson_archive_host_prefix"] ==
            "https://images.shulcloud.com/2920/uploads/Documents/Temple-Times/" and
            reject_2015["excluded_from_sam_cohon_corpus"] is True and
            reject_2015["exclude_audio_and_sermon_inferences"] is True,
            "2015 same-title Temple Times PDFs from different congregation must not enter Tucson corpus")
    require(all(value is False for value in context_2000["original_work_boundaries"].values()) and
            context_2000["count_constraints"]["total"] == 1607 and
            context_2000["count_constraints"]["supplemental_publications"] == 19 and
            context_2000["count_constraints"]["new_core_records"] == 0 and
            context_2000["release_and_rights_controls"]["public_metadata_only"] is True and
            all(v is False for k,v in context_2000["release_and_rights_controls"].items()
                if k != "public_metadata_only"),
            "October 31 provenance supplement must not assert new originals, publication, private changes or deployment")
    identity_note = (ROOT / "docs" / "temple-recovery-2026-10-31-chronology-and-2015-source-identity.md").read_text(encoding="utf-8")
    require("March 11, 2000" in identity_note and
            "Temple Beth Shalom" in identity_note and
            "Temple Emanu-El, 225 North Country Club Road" in identity_note and
            "HV009" in identity_note and
            "1,607" in identity_note,
            "2000 chronology / 2015 false-positive audit lacks supporting readable checkpoint")
    successor_holdings = load(DATA / "verification" / "temple-successor-archive-holdings-2026-10-31.json")
    require(successor_holdings["review_date"] == "2026-10-31" and
            len(successor_holdings["source_holding_leads"]) == 3 and
            len({x["id"] for x in successor_holdings["source_holding_leads"]}) == 3 and
            successor_holdings["core_records_unchanged"] == {
                "radio": 1265,
                "first_party_blog": 316,
                "teaching": 26,
                "total": 1607,
                "supplemental_publications": 19
            },
            "October 31 new archive routes must not inflate core publication counts")
    successor_by_id = {x["id"]: x for x in successor_holdings["source_holding_leads"]}
    require(successor_by_id["KOL-AMI-LEGACY-TEMPLE-EMANU-EL"]["source"] ==
            "https://www.katucson.org/synagogue-history" and
            successor_by_id["KOL-AMI-LEGACY-TEMPLE-EMANU-EL"]["specific_target_manuscripts_confirmed_in_holding"] is False and
            successor_by_id["TEMPLE-TIMES-2021-LEGACY-SHULCLOUD"]["source"] ==
            "https://images.shulcloud.com/2920/uploads/Documents/Temple-Times/21-jun-jul.pdf" and
            successor_by_id["TEMPLE-TIMES-2021-LEGACY-SHULCLOUD"]["specific_target_manuscripts_confirmed_in_holding"] is False and
            successor_by_id["PRX-HEARING-VOICES-PUBLISHER-GROUP"]["hv009_prx_item_verified"] is False and
            successor_by_id["PRX-HEARING-VOICES-PUBLISHER-GROUP"]["hv009_enclosure_recovered"] is False and
            successor_by_id["PRX-HEARING-VOICES-PUBLISHER-GROUP"]["hv009_audio_bytes_verified"] is False,
            "Institutional successor, 2021 bulletin and PRX catalogue may not be misrepresented as target manuscripts/media")
    require(len(successor_holdings["false_positive_collections"]) == 3 and
            all(x["assessment"] for x in successor_holdings["false_positive_collections"]) and
            all(not value for key,value in successor_holdings["permissions"].items()
                if key != "private_originals_untouched") and
            successor_holdings["permissions"]["private_originals_untouched"] is True and
            all(not value for fields in successor_holdings["target_recovery_status"].values()
                for value in fields.values()),
            "Recovery audit must retain identity disambiguation, five missing originals, and full rights gates")
    successor_note = (ROOT / "docs" / "temple-recovery-2026-10-31-successor-archives.md").read_text(encoding="utf-8")
    require("Kol Ami" in successor_note and "Temple Times" in successor_note and
            "PRX" in successor_note and "Samuel S. Cohon" in successor_note and
            "1,607" in successor_note and "No manuscripts" in successor_note,
            "Successor archive research checkpoint missing or overclaiming source recovery")
    source_gates = load(DATA / "verification" / "temple-source-recovery-gates-2026-10-23.json")
    require(source_gates["checked_at"] == "2026-10-23" and
            len(source_gates["targets"]) == 5 and
            len({r["id"] for r in source_gates["targets"]}) == 5 and
            all(r["core_count_change"] == 0 and r["repeat_condition"] for r in source_gates["targets"]) and
            source_gates["unchanged_core"] == {
                "radio": 1265,
                "first_party_blog": 316,
                "teaching": 26,
                "total": 1607,
                "supplemental_publications": 19
            },
            "Source recovery gates must preserve five distinct targets and unchanged core counts")
    gate_by_id = {r["id"]: r for r in source_gates["targets"]}
    require(gate_by_id["TEMPLE-2000-ORIGINS"]["original_manuscript_recovered"] is False and
            gate_by_id["TEMPLE-2000-ORIGINS"]["rights_cleared"] is False and
            gate_by_id["TEMPLE-2001-EREV-ROSH-HASHANAH"]["delivered_replacement_complete_recovered"] is False and
            gate_by_id["TEMPLE-2001-EREV-ROSH-HASHANAH"]["planned_undelivered_drafts_recovered"] is False and
            gate_by_id["TEMPLE-2015-REFUGEE"]["original_manuscript_recovered"] is False and
            gate_by_id["HV-2008-009"]["audio_binary_recovered"] is False and
            gate_by_id["HV-2008-009"]["cohon_voice_listened_and_confirmed"] is False and
            gate_by_id["HV-2008-009"]["not_too_jewish_core"] is True and
            gate_by_id["HV-2008-009"]["not_2013_temple_class"] is True and
            gate_by_id["TE-2013-PODBEAN"]["audio_binary_recovered"] is False and
            gate_by_id["TE-2013-PODBEAN"]["specific_episode_recovered"] is False,
            "Unrecovered originals, episodes and manuscripts must not be upgraded by broken links or replicated indexes")
    require(source_gates["read_only_private_search"]["private_file_names_or_ids_recorded"] is False and
            source_gates["read_only_private_search"]["no_grounds_for_archive_wide_absence"] is True and
            all(v is False for k,v in source_gates["permissions"].items() if k != "private_originals_untouched") and
            source_gates["permissions"]["private_originals_untouched"] is True,
            "Source metadata gate must preserve privacy, rights, release and no-contact boundaries")
    gate_note = (ROOT / "docs" / "temple-recovery-2026-10-23-source-gates.md").read_text(encoding="utf-8")
    require("## Actionable evidence gates" in gate_note and
            "source-recovery-gates-2026-10-23.json" in gate_note and
            "no authenticated original or playable historical recording" in gate_note.lower() and
            "1,607" in gate_note,
            "Bounded negative search must retain a readable checkpoint and future evidence triggers")
    temple_witnesses = load(DATA / "writings" / "historical-sermon-witnesses.json")
    historical_2001 = temple_witnesses["records"]
    require(len(historical_2001) == 1 and
            historical_2001[0]["id"] == "TEMPLE-2001-EREV-ROSH-HASHANAH-AUTHOR-SELF-EXCERPT" and
            historical_2001[0]["source_witness_url"] ==
            "https://beitsimchatucson.org/blog/911-25-years-before-and-since" and
            historical_2001[0]["delivery_status"] == "excerpt_of_reportedly_delivered_sermon" and
            historical_2001[0]["original_pre_911_drafts_status"] ==
            "existence_historically_reported_but_not_delivered_and_not_recovered" and
            historical_2001[0]["complete_original_sermon_recovered"] is False and
            historical_2001[0]["original_drafts_recovered"] is False and
            historical_2001[0]["original_temple_manuscript_authenticated"] is False and
            historical_2001[0]["copyright_full_text_ingested"] is False and
            historical_2001[0]["core_count_added"] is False and
            historical_2001[0]["rights_status"] == "not_assessed" and
            any(r["url"] == historical_2001[0]["source_witness_url"] for r in writing),
            "2001 replacement sermon excerpt and undelivered drafts must remain distinct, linked to existing blog source")
    recent_checkpoint = (ROOT / "docs" / "temple-recovery-2026-10-22-late-audit.md").read_text(encoding="utf-8")
    require("September 2001" in recent_checkpoint and
            "never delivered" in recent_checkpoint and
            "not an original manuscript" in recent_checkpoint and
            "HV009" in recent_checkpoint and
            "1,607" in recent_checkpoint,
            "Late manuscript/audio provenance checkpoint missing or overly strong")
    community = load(DATA / "writings" / "community-publications.json")["records"]
    historical = load(DATA / "teaching" / "historical-source-leads.json")["records"]
    require(len({r["url"] for r in community}) == len(community), "Community source URLs not unique")
    require(len(community) >= 17, "Historical community excerpt records missing")
    require(len({r["id"] for r in historical}) == len(historical), "Historical audio-lead IDs not unique")
    require(any(r["id"] == "TE-2013-PODCAST-LEAD" and
                r["media_recovery_status"] == "no_audio_binary_or_specific_class_episode_recovered"
                for r in historical), "Unverified historical podcast lead misrepresented")
    for excerpt_title in ("Baking Holiness", "The Necessary Chutzpah of Saving Refugees"):
        relevant = [r for r in community if excerpt_title in r["title"]]
        require(len(relevant) == 1 and relevant[0]["full_text_ingested"] is False,
                f"Historical excerpt must not be treated as full manuscript: {excerpt_title}")
    origins = [r for r in community if r["title"].startswith("The Origins of Awareness")]
    require(len(origins) == 1 and
            origins[0]["date"] == "2000" and
            origins[0]["type"] == "historical_sermon_substantially_complete_public_reproduction" and
            origins[0]["sermon_pdf_pages_1_indexed"] == [7, 8, 9, 10, 11, 12, 13] and
            origins[0]["original_temple_manuscript_recovered"] is False and
            origins[0]["publicly_available_substantial_sermon_text"] is True and
            origins[0]["full_text_ingested"] is False and
            origins[0]["audio_binary_recovered"] is False and
            origins[0]["rights_status"] == "not_assessed" and
            origins[0]["core_catalogue_count_included"] is False,
            "2000 public sermon reproduction is not a verified Temple original or cleared full text")
    provenance = origins[0]["public_textual_crosscheck"]
    require(provenance["byte_for_byte_identity_verified"] is False and
            "not_independent_authentication" in provenance["status"] and
            origins[0]["first_party_text_authentication_status"] == "unverified" and
            origins[0]["institutional_context"]["original_host_authenticated"] is False and
            origins[0]["provenance_audit_path"] ==
            "data/verification/temple-2000-source-authentication-audit-2026-10-22.json",
            "Secondary 2000 PDF representations must not imply first-party manuscript authentication")
    verification = load(DATA / "verification" / "temple-2000-source-authentication-audit-2026-10-22.json")
    evidence = verification["manuscript"]
    qa_limits = evidence["qa_limits"]
    require(evidence["count_in_1607_core_catalogue"] is False and
            evidence["source_pdf_index_page_count"] == 14 and
            evidence["apparent_last_page_number_1_based"] == 14 and
            evidence["assessment"].endswith("Do not claim original recovered.") and
            qa_limits["signed_original_compared"] is False and
            qa_limits["full_legal_rights_cleared"] is False and
            qa_limits["checksum_established"] is False and
            qa_limits["pdf_screenshot_success"] is False and
            qa_limits["full_text_public_repo_ingested"] is False and
            verification["refugee_sermon_2015"]["complete_sermon_copy_recovered"] is False and
            verification["early_2013_audio"]["audio_binary_recovered"] is False and
            verification["controls"]["contact_anyone"] is False,
            "New verification ledger must preserve rights, byte-level and historical-recovery boundaries")
    yk_window = origins[0]["calendar_corroboration"]
    require(yk_window["observed_civil_window_start"] == "2000-10-08" and
            yk_window["observed_civil_window_end"] == "2000-10-09" and
            yk_window["source"] == "https://www.hebcal.com/holidays/yom-kippur-2000" and
            "delivery_day_unverified" in yk_window["event_date_confidence"],
            "Oct 23 calendars must be event-level, not fabricated sermon delivery time")
    erev_witness = historical_2001[0]["calendar_corroboration"]
    require(erev_witness["erev_rosh_hashanah_civil_date"] == "2001-09-17" and
            erev_witness["first_day_of_rosh_hashanah"] == "2001-09-18" and
            "not_delivery_documentation" in erev_witness["corroboration_level"],
            "2001 Erev Rosh Hashanah holiday date is not documentary proof of original delivery")
    recheck = verification["october_23_recheck"]
    require(recheck["manuscript_2000"]["original_first_party_manuscript_found"] is False and
            recheck["manuscript_2000"]["exact_service_or_sermon_delivery_time_confirmed"] is False and
            recheck["manuscript_2000"]["screenshot_result"].startswith("Web screenshot retrieval failed") and
            recheck["refugee_2015"]["original_text_recovered"] is False and
            recheck["retrospective_2001"]["excerpt_is_original_verified_manuscript"] is False and
            recheck["hv009"]["direct_audio_url_recovered"] is False and
            recheck["hv009"]["cohon_voice_verified"] is False and
            recheck["permission_controls"]["publish_manuscripts_or_transcripts"] is False,
            "Oct 23 audit must not overclaim source, rights, audio or delivery")
    latest_checkpoint = (ROOT / "docs" / "temple-recovery-2026-10-23-calendar-and-hv009.md").read_text(encoding="utf-8")
    require("October 8" in latest_checkpoint and
            "September 17" in latest_checkpoint and
            "2015 written-text access" in latest_checkpoint and
            "not recovered" in latest_checkpoint and
            "1,607" in latest_checkpoint,
            "October 23 recovery checkpoint missing calendar, access or source-count boundaries")
    recording_letter = [r for r in community if r["title"] == "Music article welcome, falls short"]
    require(len(recording_letter) == 1 and
            recording_letter[0]["date"] == "2012-10-04" and
            recording_letter[0]["full_text_ingested"] is False and
            recording_letter[0]["core_catalogue_count_included"] is False,
            "2012 signed recording-history letter must remain supplemental metadata")
    service_lead = [r for r in historical if r["id"] == "TE-2012-HOLIDAY-SERVICES-RECORDING-LEAD"]
    require(len(service_lead) == 1 and
            service_lead[0]["media_recovery_status"] ==
            "no_audio_binary_or_specific_class_episode_recovered" and
            service_lead[0]["rights_status"] == "not_assessed",
            "2012 recording-practice claim must not imply any recovered audio")
    independent_episode = [r for r in historical if r["id"] == "HV-2008-009-COHON"]
    require(len(independent_episode) == 1 and
            independent_episode[0]["broadcast_date"] == "2008-04-30" and
            independent_episode[0]["episode_identifier"] == "HV009" and
            independent_episode[0]["publisher"] == "Hearing Voices (independent radio series)" and
            independent_episode[0]["first_party_publisher_index_url"] ==
            "https://www.hearingvoices.org/hv-series/" and
            independent_episode[0]["media_recovery_status"] ==
            "specific_episode_listed_without_verified_audio_enclosure_or_binary" and
            independent_episode[0]["audio_enclosure_url"] is None and
            independent_episode[0]["audio_bytes_verified"] is False and
            independent_episode[0]["speaker_voice_verified_by_listening"] is False and
            independent_episode[0]["rights_status"] == "not_assessed" and
            independent_episode[0]["core_catalogue_count_included"] is False,
            "Independent radio HV009 may not be counted as a recovered class, canonical radio episode, or playable master")
    followup = verification["additional_followup"]
    require(followup["2000_manuscript"]["original_temple_source_recovered"] is False and
            followup["2015_sermon"]["full_text_recovered"] is False and
            followup["2008_other_production"]["episode_number"] == "009" and
            followup["2008_other_production"]["audio_enclosure_discovered"] is False and
            followup["2008_other_production"]["audio_bytes_confirmed"] is False and
            followup["2013_temple_audio"]["enclosure_found"] is False,
            "New historical research must preserve manuscript and media evidence tiers")
    historical_2013 = next(r for r in historical if r["id"] == "TE-2013-PODCAST-LEAD")
    require(historical_2013["rss_checks"]["checked_at"] == "2026-10-22" and
            len(historical_2013["rss_checks"]["attempted_urls"]) == 2 and
            "no episode IDs" in historical_2013["rss_checks"]["result"],
            "2013 RSS access failure must not be represented as recovered enclosures")
    discovery_note = (ROOT / "docs" / "temple-early-sermon-audio-recovery-2026-10-22.md").read_text(encoding="utf-8")
    require("Origins of Awareness" in discovery_note and
            "2012 signed letter" in discovery_note and
            "No one was contacted" in discovery_note and
            "visual fidelity" in discovery_note and
            "1,607" in discovery_note,
            "Early-sermon recovery checkpoint lacks metadata or explicit caveats")
    baking = next(r for r in community if r["title"].startswith("Baking Holiness"))
    require(baking["original_temple_manuscript_recovered"] is False and
            baking["full_text_ingested"] is False and
            baking["complete_parallel_text_status"] ==
            "complete_authored_published_commentary_readable_at_source_not_copied" and
            baking["complete_parallel_published_url"].startswith("https://reformjudaism.org/"),
            "Reform movement complete adaptation must not be mistaken for Temple original")
    refugees = next(r for r in community if r["title"].startswith("The Necessary Chutzpah"))
    require(refugees["full_text_ingested"] is False and
            refugees["review_state"] == "reform_movement_attributed_excerpt_verified_full_manuscript_not_recovered",
            "Original 2015 Temple manuscript still missing")
    editorial = refugees["historical_editorial_manuscript_evidence"]
    require(editorial["roundup_byline"] == "Mark J. Pelavin" and
            "does not establish present-day possession" in editorial["byline_evidence"],
            "Named URJ editor must not be misrepresented as current manuscript custodian")
    require(editorial["complete_written_text_recovered"] is False and
            editorial["rights_assessed"] is False and
            editorial["review_date"] == "2026-10-22" and
            editorial["source"] == "https://urj.org/blog/our-second-annual-rosh-hashanah-sermon-round" and
            "written text" in editorial["basis"].lower() and
            "editor had access to a written version" in editorial["interpretation"] and
            "inaccessible" in editorial["independent_archive_snapshot_result"],
            "URJ editor-method lead must not imply a recovered original or rights")
    current_note = (ROOT / "docs" / "temple-historical-recovery-2026-10-22.md").read_text(encoding="utf-8")
    require("written version" in current_note and
            "no" in current_note.lower() and
            "1,607" in current_note and
            "No contact attempted" in current_note,
            "Current historical recovery provenance or publication gate missing")
    temple_channel = next(r for r in historical if r["id"] == "TE-2013-PODCAST-LEAD")
    require(temple_channel["last_access_attempt_date"] == "2026-10-21" and
            temple_channel["media_recovery_status"] ==
            "no_audio_binary_or_specific_class_episode_recovered" and
            "Invalid Podbean Site" in temple_channel["observed_access_result"],
            "2013 teaching podcast redirect is a lead, not an audio recovery")
    recovery_note = (ROOT / "docs" / "temple-historical-recovery-2026-10-21.md").read_text(encoding="utf-8")
    require("Baking Holiness" in recovery_note and
            "The Necessary Chutzpah of Saving Refugees" in recovery_note and
            "historical class audio" in recovery_note.lower() and
            "does not reproduce manuscripts" in recovery_note.lower(),
            "Historical recovery checkpoint missing or incomplete")
    latest_episodes = {r["broadcast_date"]: r for r in radio}
    for date in ("2026-09-27", "2026-10-04"):
        episode = latest_episodes[date]
        require(episode.get("podbean_download_url", "").startswith("https://www.podbean.com/media/share/"),
                f"Missing first-party download href for {date}")
        require("not checked" in episode.get("podbean_download_evidence", ""),
                f"Do not mark unverified Podbean MP3 as downloaded: {date}")
    require(latest_episodes["2026-09-27"]["official_link_status"] == "live" and
            latest_episodes["2026-09-27"]["official_http_status"] == 200 and
            latest_episodes["2026-09-27"]["official_link_checked_at"] == "2026-10-15T04:41:40+00:00",
            "September 27 verified official HEAD status missing")
    proof = load(DATA / "verification" / "too-jewish-2026-09-27-head-2026-10-15.json")
    require(proof["episode_id"] == "tj-2026-09-27" and
            proof["observations"][-1]["content_type"] == "audio/mpeg" and
            proof["observations"][-1]["redirect_count"] == 0 and
            proof["observations"][-1]["http_status"] == 200,
            "Targeted publisher HEAD evidence missing or inconsistent")
    require(proof["audio_bytes_downloaded"] is False and proof["transcribed"] is False,
            "HTTP link validation misrepresented as speech-to-text completion")
    require(stats["link_checked_at"] == "2026-09-22T04:38:34+00:00",
            "Full corpus HEAD timestamp must remain historical")
    require(stats["link_status_counts"].get("not_checked", 0) == 3 and
            stats["link_status_counts"]["live"] == 890,
            "Targeted HEAD count reconciliation mismatch")
    require(latest_episodes["2026-10-04"]["official_link_status"] == "not_checked",
            "October 4 official URL must remain HTTP-unchecked")
    require(sum([len(radio), len(writing), len(standalone), len(teaching)]) == 1607, "Corpus total mismatch")
    for episode_id in ("tj-2026-10-04", "tj-2026-10-11", "tj-2026-10-18"):
        row = {r["id"]: r for r in radio}[episode_id]
        require(row["official_link_status"] == "not_checked" and row["official_audio_url"]
                and row["official_http_status"] is None and row["transcript_status"] == "not_ingested",
                "Publisher href is not independent audio verification: " + episode_id)

    lookup = {r["url"]: r for r in writing}
    older = "https://beitsimchatucson.org/blog/finding-gratitude"
    newer = "https://beitsimchatucson.org/blog/finding-gratitude-1"
    require(older in lookup and newer in lookup, "Both Gratitude editions required")
    require(lookup[older]["published_date"] == "2024-10-29", "Historical edition date lost")
    require(lookup[newer]["published_date"] == "2026-09-30", "New edition date missing")
    require(lookup[older]["related_source_url"] == newer, "Old edition relation missing")
    require(lookup[newer]["related_source_url"] == older, "New edition relation missing")
    edition_status = "near_verbatim_republication_calendar_updated_full_body_verified_2026-10-13"
    require(all(lookup[u].get("relation_status") == edition_status for u in (older, newer)),
            "Finding Gratitude edition evidence missing in source records")
    dedupe = load(DATA / "writings" / "dedupe-candidates.json")
    require(dedupe["confirmed_redundant_source_records_minimum"] ==
            wstats["confirmed_redundant_source_records_minimum"], "Dedupe count mismatch")
    require(wstats["conservative_distinct_work_upper_bound"] ==
            wstats["source_records_total"] - wstats["confirmed_redundant_source_records_minimum"],
            "Dedupe arithmetic mismatch")
    require(dedupe["conservative_distinct_work_upper_bound_from_316"] ==
            wstats["conservative_distinct_work_upper_bound"], "Dedupe ledger upper bound mismatch")

    registry = {entry["name"]: entry for entry in sources}
    require(registry["Congregation Beit Simcha Rabbi's Blog"]["records"] == len(writing), "Source registry mismatch")
    require(registry["Too Jewish Radio official archive"]["records"] == len(radio), "Podbean-only episode needs separate provenance")

    meta = read_js_array(DIST / "data-meta.js", "window.__COHON_META__=", ";")
    require(meta["stats"] == stats, "Site radio stats and source metrics differ")
    compact_prefix = ("window.__COHON_EPISODES__=window.__COHON_EPISODES__||[];"
                      "window.__COHON_EPISODES__.push(...")
    compact = [
        row for a, b in [(2002, 2006), (2007, 2011), (2012, 2016), (2017, 2021), (2022, 2026)]
        for row in read_js_array(DIST / f"data-{a}-{b}.js", compact_prefix, ");")
    ]
    require(len(compact) == len(radio), "Site radio bundle does not contain all episodes")
    require(all(0 <= r["r"] < len(meta["roles"]) for r in compact), "Guest-role index outside dictionary")
    require(all(all(0 <= t < len(meta["topics"]) for t in r["t"]) for r in compact), "Topic index outside dictionary")
    latest = {r["d"]: r for r in compact}
    require(latest["2026-09-27"]["s"] == "l" and "k" not in latest["2026-09-27"], "Verified recent MP3 must appear checked in browser")
    require(latest["2026-10-04"]["s"] == "u", "Official-listed Oct 4 URL must remain independently unverified")
    for broadcast_date in ("2026-10-11", "2026-10-18"):
        require(latest[broadcast_date]["s"] == "u" and latest[broadcast_date].get("k") is None,
                "New unprobed publisher links must display HTTP-unchecked state")

    site_writing = read_js_array(DIST / "writings-data.js", "window.SAM_WRITINGS=", ";")
    require(len(site_writing) == len(writing) + len(standalone), "Site writing count mismatch")
    require({r["url"] for r in site_writing} ==
            {r["url"] for r in writing} | {r["url"] for r in standalone},
            "Website source URLs do not match canonical writing ledgers")
    site_editions = {r["url"]: r for r in site_writing}
    require(all(site_editions[u].get("relation_status") == edition_status for u in (older, newer)),
            "Generated writing browser uses old Gratitude edition status")
    html = (DIST / "index.html").read_text(encoding="utf-8")
    require("1,607" in html and "1,599" not in html, "Stale site aggregate")
    require("makeRadioBrowser()" in html and "data-2022-2026.js" in html, "Radio browser missing")
    require("310 distinct works" in html, "Distinct-work upper-bound notice missing")

    print(f"PASS: {len(radio)} radio + {len(writing) + len(standalone)} writing + "
          f"{len(teaching)} teaching = 1,607 indexed records; editions and site bundles agree.")


if __name__ == "__main__":
    main()
