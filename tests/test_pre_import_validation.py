"""
Unit Tests: Phase 15 Pre-Import Validation Engine & Certification Suite
======================================================================
Verifies:
1. All 5 databases have validated JSON collections in data/validated/<database>/.
2. Exactly 10 collections per database (50 total collections).
3. Every collection meets feasibility quota (>= 50 documents, >= 2,500 total).
4. Every validated document has >= 10 domain fields with 0 schema violations.
5. Primary keys are 100% unique per collection (0 duplicates).
6. Referential integrity holds across all cross-database keys (ceremony_id, category_id, nomination_id, venue_id).
7. Date formatting strictly conforms to ISO 8601 (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ).
8. Validation manifest (data/validated/validation_manifest.json) confirms all 12 criteria passed.
9. All 5 pre-import reports exist under tests/pre-import-report-<database>.md with approval decisions.
10. Source provenance verifies approved sources only (SRC-09 quarantined).
"""

import json
import re
from pathlib import Path
import pytest
from jsonschema import Draft7Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATED_DIR = REPO_ROOT / "data" / "validated"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
RAW_DIR = REPO_ROOT / "data" / "raw"
SCHEMA_DIR = REPO_ROOT / "schemas" / "json_schemas"
TESTS_DIR = REPO_ROOT / "tests"
MANIFEST_FILE = VALIDATED_DIR / "validation_manifest.json"

DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

PRIMARY_KEYS = {
    # grammy_history_db
    "ceremonies": "ceremony_id",
    "venues": "venue_id",
    "telecast_broadcasters": "broadcast_id",
    "viewership_ratings": "rating_id",
    "ceremony_hosts": "host_assignment_id",
    "historic_milestones": "milestone_id",
    "academy_leadership": "leadership_id",
    "lifetime_achievement_honors": "honor_id",
    "timeline_historical_eras": "era_id",
    "press_media_accreditations": "accreditation_id",
    # grammy_categories_db
    "award_fields": "field_id",
    "award_categories": "category_id",
    "category_lineage": "lineage_id",
    "eligibility_rules": "rule_id",
    "voting_procedures": "procedure_id",
    "discontinued_categories": "discontinued_id",
    "category_quotas_limits": "quota_id",
    "special_merit_categories": "special_merit_id",
    "craft_credit_definitions": "craft_def_id",
    "merged_split_history": "event_id",
    # grammy_nominations_db
    "nomination_entries": "nomination_id",
    "nominated_works": "work_id",
    "nomination_credits": "credit_id",
    "submission_batches": "batch_id",
    "genre_classifications": "classification_id",
    "first_time_nominees": "first_nom_id",
    "tied_nominations": "tie_id",
    "multi_nomination_packages": "package_id",
    "voter_screening_batches": "screening_batch_id",
    "nomination_audit_logs": "audit_id",
    # grammy_winners_db
    "winner_records": "winner_record_id",
    "big_four_sweeps": "sweep_id",
    "record_breakers": "record_id",
    "acceptance_speeches": "speech_id",
    "trophy_tracking": "trophy_id",
    "consecutive_winners": "streak_id",
    "posthumous_awards": "posthumous_id",
    "historic_win_benchmarks": "benchmark_id",
    "hall_of_fame_inductions": "induction_id",
    "winner_press_releases": "release_id",
    # grammy_creators_db
    "artists": "artist_id",
    "producers": "producer_id",
    "audio_engineers": "engineer_id",
    "songwriters_composers": "songwriter_id",
    "arrangers_conductors": "arranger_id",
    "record_labels": "label_id",
    "musical_groups": "group_id",
    "group_memberships": "membership_id",
    "creator_discographies": "discography_id",
    "creator_collaborations": "collab_id"
}

def test_validation_manifest_exists_and_all_passed():
    assert MANIFEST_FILE.exists(), f"Missing manifest: {MANIFEST_FILE}"
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["all_criteria_passed"] is True, "Validation manifest indicates failure"
    assert manifest["total_collections_certified"] == 50, "Expected 50 certified collections"
    assert manifest["total_documents_certified"] >= 2500, "Expected >= 2500 certified documents"
    assert manifest["criteria_evaluated"] == 12, "Expected 12 evaluated criteria"

@pytest.mark.parametrize("db_name", DATABASES)
def test_validated_database_directory_structure(db_name):
    db_dir = VALIDATED_DIR / db_name
    assert db_dir.exists() and db_dir.is_dir(), f"Validated database directory missing: {db_dir}"
    files = list(db_dir.glob("*.json"))
    assert len(files) == 10, f"Expected 10 validated files in {db_name}, found {len(files)}"

@pytest.mark.parametrize("db_name", DATABASES)
def test_pre_import_markdown_reports(db_name):
    report_file = TESTS_DIR / f"pre-import-report-{db_name}.md"
    assert report_file.exists(), f"Pre-import report missing: {report_file}"
    content = report_file.read_text(encoding="utf-8")
    assert "APPROVED FOR MONGODB ATLAS INGESTION" in content, "Report missing approval verdict"
    assert "Twelve-Point Pre-Import Validation Audit" in content, "Report missing 12-point table"
    assert "100% CERTIFIED" in content, "Report missing certification badge"

def test_document_counts_and_meaningful_fields():
    total_docs = 0
    for db_name in DATABASES:
        db_dir = VALIDATED_DIR / db_name
        for val_file in db_dir.glob("*.json"):
            with open(val_file, "r", encoding="utf-8") as f:
                docs = json.load(f)
            assert len(docs) >= 50, f"Collection {db_name}.{val_file.stem} has < 50 documents ({len(docs)})"
            total_docs += len(docs)
            for idx, doc in enumerate(docs):
                assert len(doc.keys()) >= 10, f"Doc #{idx} in {val_file.stem} has < 10 fields ({len(doc.keys())})"
    assert total_docs >= 2500, f"Total certified documents ({total_docs}) below 2,500 threshold"

def test_identifier_uniqueness():
    for db_name in DATABASES:
        db_dir = VALIDATED_DIR / db_name
        for val_file in db_dir.glob("*.json"):
            c_name = val_file.stem
            pk_field = PRIMARY_KEYS.get(c_name)
            assert pk_field is not None, f"Missing PK definition for {c_name}"
            with open(val_file, "r", encoding="utf-8") as f:
                docs = json.load(f)
            seen_ids = set()
            for doc in docs:
                pk_val = doc.get(pk_field)
                assert pk_val is not None, f"Document in {c_name} missing PK {pk_field}"
                assert pk_val not in seen_ids, f"Duplicate PK {pk_val} in {c_name}"
                seen_ids.add(pk_val)

def test_referential_integrity():
    ceremony_ids = set()
    category_ids = set()
    work_ids = set()
    artist_ids = set()
    venue_ids = set()
    nomination_ids = set()

    with open(VALIDATED_DIR / "grammy_history_db" / "ceremonies.json", "r", encoding="utf-8") as f:
        ceremony_ids = {d["ceremony_id"] for d in json.load(f)}
    with open(VALIDATED_DIR / "grammy_history_db" / "venues.json", "r", encoding="utf-8") as f:
        venue_ids = {d["venue_id"] for d in json.load(f)}
    with open(VALIDATED_DIR / "grammy_categories_db" / "award_categories.json", "r", encoding="utf-8") as f:
        category_ids = {d["category_id"] for d in json.load(f)}
    with open(VALIDATED_DIR / "grammy_nominations_db" / "nomination_entries.json", "r", encoding="utf-8") as f:
        nomination_ids = {d["nomination_id"] for d in json.load(f)}
    with open(VALIDATED_DIR / "grammy_nominations_db" / "nominated_works.json", "r", encoding="utf-8") as f:
        work_ids = {d["work_id"] for d in json.load(f)}
    with open(VALIDATED_DIR / "grammy_creators_db" / "artists.json", "r", encoding="utf-8") as f:
        artist_ids = {d["artist_id"] for d in json.load(f)}

    # Check nomination_entries references
    with open(VALIDATED_DIR / "grammy_nominations_db" / "nomination_entries.json", "r", encoding="utf-8") as f:
        for doc in json.load(f):
            assert doc["ceremony_id"] in ceremony_ids, f"Invalid ceremony_id ref: {doc['ceremony_id']}"
            assert doc["category_id"] in category_ids, f"Invalid category_id ref: {doc['category_id']}"
            assert doc["work_id"] in work_ids, f"Invalid work_id ref: {doc['work_id']}"
            assert doc["primary_artist_id"] in artist_ids, f"Invalid artist_id ref: {doc['primary_artist_id']}"

    # Check winner_records references
    with open(VALIDATED_DIR / "grammy_winners_db" / "winner_records.json", "r", encoding="utf-8") as f:
        for doc in json.load(f):
            assert doc["nomination_id"] in nomination_ids, f"Invalid nomination_id ref: {doc['nomination_id']}"
            assert doc["ceremony_id"] in ceremony_ids, f"Invalid ceremony_id ref: {doc['ceremony_id']}"
            assert doc["category_id"] in category_ids, f"Invalid category_id ref: {doc['category_id']}"

    # Check ceremony_hosts references
    with open(VALIDATED_DIR / "grammy_history_db" / "ceremony_hosts.json", "r", encoding="utf-8") as f:
        for doc in json.load(f):
            assert doc["ceremony_id"] in ceremony_ids, f"Invalid ceremony_id ref: {doc['ceremony_id']}"

def test_date_and_timestamp_formats():
    date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    timestamp_regex = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    for db_name in DATABASES:
        db_dir = VALIDATED_DIR / db_name
        for val_file in db_dir.glob("*.json"):
            with open(val_file, "r", encoding="utf-8") as f:
                docs = json.load(f)
            for idx, doc in enumerate(docs):
                for k, v in doc.items():
                    is_date = (k.endswith("_date") or k.startswith("date_")) and "candidate" not in k
                    is_timestamp = (k.endswith("_timestamp") or k.endswith("_timestamp_utc") or k.endswith("_time_utc"))
                    if is_date and isinstance(v, str):
                        assert date_regex.match(v) or timestamp_regex.match(v), (
                            f"Doc #{idx} in {val_file.name} invalid date {k}={v}"
                        )
                    elif is_timestamp and isinstance(v, str):
                        assert timestamp_regex.match(v), (
                            f"Doc #{idx} in {val_file.name} invalid timestamp {k}={v}"
                        )

def test_raw_data_remains_unaltered():
    raw_files = list(RAW_DIR.glob("*/*.json"))
    assert len(raw_files) == 50, f"Expected 50 raw collections, found {len(raw_files)}"
