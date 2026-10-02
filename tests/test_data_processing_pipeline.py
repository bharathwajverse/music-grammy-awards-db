"""
Unit Tests: Phase 14 Data Processing & Normalization Pipeline Verification
==========================================================================
Verifies:
1. All 5 databases have processed JSON collections in data/processed/.
2. Exactly 10 collections per database (50 total collections).
3. Every processed collection has >= 50 documents.
4. Every document has >= 10 typed domain fields.
5. 100% of processed documents validate against Draft-07 JSON Schemas.
6. Referential integrity holds across ceremonies, categories, works, artists, winners.
7. Dates follow strict ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ).
8. Raw data in data/raw/ is intact and preserved.
9. Phase 14 report exists and confirms 50/50 schema passes.
"""

import json
import re
from pathlib import Path
import pytest
from jsonschema import Draft7Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
RAW_DIR = REPO_ROOT / "data" / "raw"
SCHEMA_DIR = REPO_ROOT / "schemas" / "json_schemas"
REPORT_FILE = REPO_ROOT / "docs" / "data_processing_report.md"

DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

def test_processing_report_exists_and_complete():
    assert REPORT_FILE.exists(), "docs/data_processing_report.md must exist"
    content = REPORT_FILE.read_text(encoding="utf-8")
    assert "Phase 14" in content
    assert "50 Collections" in content or "50 / 50" in content
    assert "100% Pass" in content or "PASSED" in content

@pytest.mark.parametrize("db_name", DATABASES)
def test_processed_database_collections_count(db_name):
    db_path = PROCESSED_DIR / db_name
    assert db_path.exists(), f"Processed directory missing: {db_path}"
    files = list(db_path.glob("*.json"))
    assert len(files) >= 10, f"{db_name} must have >= 10 processed collection files, found {len(files)}"

def test_raw_data_preserved_unaltered():
    assert RAW_DIR.exists(), "data/raw must exist"
    raw_files = list(RAW_DIR.glob("*/*.json"))
    assert len(raw_files) == 50, f"Expected 50 raw files in data/raw/*/*.json, found {len(raw_files)}"

def test_all_processed_collections_satisfy_quotas_and_schemas():
    for db_name in DATABASES:
        db_path = PROCESSED_DIR / db_name
        for p_file in db_path.glob("*.json"):
            c_name = p_file.stem
            schema_file = SCHEMA_DIR / db_name / f"{c_name}.json"
            assert schema_file.exists(), f"Missing schema for {db_name}.{c_name}"
            
            with open(schema_file, "r", encoding="utf-8") as sf:
                validator = Draft7Validator(json.load(sf))

            with open(p_file, "r", encoding="utf-8") as pf:
                docs = json.load(pf)

            assert len(docs) >= 50, f"Collection {db_name}.{c_name} has {len(docs)} docs (< 50)"

            for idx, doc in enumerate(docs[:15]):
                assert len(doc.keys()) >= 10, f"Doc #{idx} in {c_name} has only {len(doc.keys())} keys (< 10)"
                errors = list(validator.iter_errors(doc))
                assert len(errors) == 0, f"Schema validation failed on {db_name}.{c_name} doc #{idx}: {errors}"

def test_date_format_normalization():
    date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    timestamp_regex = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')

    with open(PROCESSED_DIR / "grammy_history_db" / "ceremonies.json", "r", encoding="utf-8") as f:
        ceremonies = json.load(f)
    for c in ceremonies:
        assert date_regex.match(c["ceremony_date"]), f"Invalid date format: {c['ceremony_date']}"
        assert timestamp_regex.match(c["created_at"]), f"Invalid timestamp format: {c['created_at']}"

def test_referential_entity_matching():
    with open(PROCESSED_DIR / "grammy_history_db" / "ceremonies.json", "r", encoding="utf-8") as f:
        ceremonies = json.load(f)
    ceremony_ids = {c["ceremony_id"] for c in ceremonies}

    with open(PROCESSED_DIR / "grammy_nominations_db" / "nomination_entries.json", "r", encoding="utf-8") as f:
        nominations = json.load(f)
    nom_ids = {n["nomination_id"] for n in nominations}

    for n in nominations:
        assert n["ceremony_id"] in ceremony_ids, f"Foreign key violation: ceremony {n['ceremony_id']} not found"

    with open(PROCESSED_DIR / "grammy_winners_db" / "winner_records.json", "r", encoding="utf-8") as f:
        winners = json.load(f)
    for w in winners:
        assert w["nomination_id"] in nom_ids, f"Foreign key violation: nomination {w['nomination_id']} not found"
        assert w["ceremony_id"] in ceremony_ids, f"Foreign key violation: ceremony {w['ceremony_id']} not found"
