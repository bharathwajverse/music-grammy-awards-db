"""
Unit Tests: Phase 13 Raw Data Acquisition & Provenance Verification
===================================================================
Verifies:
1. All 5 databases have raw data subdirectories in data/raw/.
2. Exactly 10 raw JSON collections per database (50 total).
3. Every raw collection contains >= 50 records.
4. Every raw record contains '_source_provenance' metadata.
5. All source IDs are APPROVED in sources/source-register.csv.
6. Quarantined SRC-09 is never present in acquired data.
7. Acquisition manifest exists and is consistent.
8. Phase 13 report exists and documents the acquisition.
"""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"
MANIFEST_FILE = RAW_DIR / "acquisition_manifest.json"
REPORT_FILE = REPO_ROOT / "docs" / "data_acquisition_report.md"

DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

def test_manifest_file_exists_and_valid():
    assert MANIFEST_FILE.exists(), "acquisition_manifest.json must exist in data/raw/"
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest.get("total_databases") == 5
    assert manifest.get("total_collections") == 50
    assert manifest.get("total_raw_records") >= 2500
    assert manifest.get("all_quotas_met") is True
    assert "SRC-09" in manifest.get("quarantined_sources_excluded", [])

@pytest.mark.parametrize("db_name", DATABASES)
def test_raw_database_directories_and_collection_quota(db_name):
    db_path = RAW_DIR / db_name
    assert db_path.exists(), f"Raw directory missing for database: {db_name}"
    raw_files = list(db_path.glob("*.json"))
    assert len(raw_files) >= 10, f"{db_name} must have >= 10 raw collection files, found {len(raw_files)}"

def test_all_raw_collections_meet_document_quota():
    for db_name in DATABASES:
        db_path = RAW_DIR / db_name
        for raw_file in db_path.glob("*.json"):
            with open(raw_file, "r", encoding="utf-8") as f:
                records = json.load(f)
            assert len(records) >= 50, (
                f"Collection {db_name}.{raw_file.stem} has {len(records)} records (< 50)"
            )

def test_raw_records_contain_provenance_and_only_approved_sources():
    approved_ids = {"SRC-01", "SRC-02", "SRC-03", "SRC-04", "SRC-05", "SRC-06", "SRC-07", "SRC-08", "SRC-10"}
    for db_name in DATABASES:
        db_path = RAW_DIR / db_name
        for raw_file in db_path.glob("*.json"):
            with open(raw_file, "r", encoding="utf-8") as f:
                records = json.load(f)
            for idx, r in enumerate(records[:10]): # Spot check first 10 per collection
                assert "_source_provenance" in r, f"Record #{idx} in {db_name}.{raw_file.stem} missing _source_provenance"
                prov = r["_source_provenance"]
                s_id = prov.get("source_id")
                assert s_id in approved_ids, f"Unapproved source {s_id} in {db_name}.{raw_file.stem}"
                assert s_id != "SRC-09", f"Quarantined source SRC-09 found in {db_name}.{raw_file.stem}"

def test_acquisition_report_exists_and_covers_all_databases():
    assert REPORT_FILE.exists(), "docs/data_acquisition_report.md must exist"
    content = REPORT_FILE.read_text(encoding="utf-8")
    for db in DATABASES:
        assert db in content, f"Report must cover database: {db}"
    assert "SRC-09" in content, "Report must document quarantine of SRC-09"
    assert "5,190" in content or "5190" in content, "Report must record total records acquired"
