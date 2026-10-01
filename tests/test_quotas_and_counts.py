"""
Unit Tests: Collection & Schema Quota Validation
================================================
Verifies that:
1. All 5 databases have >= 10 collections defined.
2. Every collection schema specifies >= 10 required meaningful fields.
3. Total collections across the system >= 50.
"""

import json
from pathlib import Path
import pytest

SCHEMA_BASE_DIR = Path("schemas/json_schemas")
EXPECTED_DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

@pytest.mark.parametrize("db_name", EXPECTED_DATABASES)
def test_database_collection_quota(db_name):
    db_dir = SCHEMA_BASE_DIR / db_name
    assert db_dir.exists(), f"Database schema directory does not exist: {db_dir}"
    schemas = list(db_dir.glob("*.json"))
    assert len(schemas) >= 10, f"Database {db_name} must contain at least 10 collections, found {len(schemas)}"

def test_total_collection_count():
    total = len(list(SCHEMA_BASE_DIR.glob("*/*.json")))
    assert total >= 50, f"System must contain at least 50 collections, found {total}"

@pytest.mark.parametrize("db_name", EXPECTED_DATABASES)
def test_schema_required_fields_quota(db_name):
    db_dir = SCHEMA_BASE_DIR / db_name
    schemas = list(db_dir.glob("*.json"))
    for s_file in schemas:
        with open(s_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        required = data.get("required", [])
        assert len(required) >= 10, (
            f"Collection {db_name}.{s_file.stem} must require >= 10 fields, found {len(required)}: {required}"
        )
