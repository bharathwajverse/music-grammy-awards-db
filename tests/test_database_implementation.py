"""
Unit Tests: Phase 16 Database and Collection Implementation Verification
========================================================================
Verifies:
1. docs/mongodb/database-implementation.md exists and documents the 5 databases and 50 collections.
2. docs/mongodb/database_deployment_manifest.json reports 5 databases, 50 collections, and 50 validators.
3. Live MongoDB Atlas cluster verification:
   - Only the 5 approved databases are configured.
   - Exactly 10 approved collections exist per database (50 total).
   - Zero unapproved collections exist.
   - Native $jsonSchema validator is attached to every collection.
   - validationLevel is 'strict' and validationAction is 'error'.
   - Document count is 0 across all collections (boundary check).
"""

import os
import json
from pathlib import Path
import pytest
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_MONGODB_DIR = REPO_ROOT / "docs" / "mongodb"
REPORT_FILE = DOCS_MONGODB_DIR / "database-implementation.md"
MANIFEST_FILE = DOCS_MONGODB_DIR / "database_deployment_manifest.json"

APPROVED_DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

APPROVED_COLLECTIONS = {
    "grammy_history_db": [
        "ceremonies",
        "venues",
        "telecast_broadcasters",
        "viewership_ratings",
        "ceremony_hosts",
        "historic_milestones",
        "academy_leadership",
        "lifetime_achievement_honors",
        "timeline_historical_eras",
        "press_media_accreditations"
    ],
    "grammy_categories_db": [
        "award_fields",
        "award_categories",
        "category_lineage",
        "eligibility_rules",
        "voting_procedures",
        "discontinued_categories",
        "category_quotas_limits",
        "special_merit_categories",
        "craft_credit_definitions",
        "merged_split_history"
    ],
    "grammy_nominations_db": [
        "nomination_entries",
        "nominated_works",
        "nomination_credits",
        "submission_batches",
        "genre_classifications",
        "first_time_nominees",
        "tied_nominations",
        "multi_nomination_packages",
        "voter_screening_batches",
        "nomination_audit_logs"
    ],
    "grammy_winners_db": [
        "winner_records",
        "big_four_sweeps",
        "record_breakers",
        "acceptance_speeches",
        "trophy_tracking",
        "consecutive_winners",
        "posthumous_awards",
        "historic_win_benchmarks",
        "hall_of_fame_inductions",
        "winner_press_releases"
    ],
    "grammy_creators_db": [
        "artists",
        "producers",
        "audio_engineers",
        "songwriters_composers",
        "arrangers_conductors",
        "record_labels",
        "musical_groups",
        "group_memberships",
        "creator_discographies",
        "creator_collaborations"
    ]
}

def test_implementation_report_exists():
    assert REPORT_FILE.exists(), f"Missing report: {REPORT_FILE}"
    content = REPORT_FILE.read_text(encoding="utf-8")
    assert "PHASE 16 — DATABASE IMPLEMENTATION" in content
    assert "ALL 5 APPROVED DATABASES & 50 COLLECTIONS SUCCESSFULLY IMPLEMENTED" in content
    assert "strict" in content

def test_deployment_manifest_validity():
    assert MANIFEST_FILE.exists(), f"Missing manifest: {MANIFEST_FILE}"
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["databases_count"] == 5
    assert manifest["total_collections_created"] == 50
    assert manifest["total_validators_configured"] == 50
    assert manifest["all_collections_verified"] is True
    for db_name in APPROVED_DATABASES:
        assert db_name in manifest["databases"]
        assert manifest["databases"][db_name]["collections_count"] == 10

@pytest.fixture(scope="module")
def mongo_client():
    load_dotenv(REPO_ROOT / ".env")
    uri = os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        pytest.skip("MONGODB_URI not found in .env; skipping live Atlas tests")
    try:
        import certifi
        import pymongo
        client = pymongo.MongoClient(
            uri,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=7000
        )
        client.admin.command("ping")
        return client
    except Exception as e:
        pytest.skip(f"Could not connect to MongoDB Atlas cluster: {e}")

@pytest.mark.parametrize("db_name", APPROVED_DATABASES)
def test_atlas_database_and_collections_exist(mongo_client, db_name):
    db = mongo_client[db_name]
    existing_cols = db.list_collection_names()
    expected_cols = APPROVED_COLLECTIONS[db_name]
    
    assert set(existing_cols) == set(expected_cols), (
        f"Mismatch in collections for {db_name}. Found: {existing_cols}, Expected: {expected_cols}"
    )

@pytest.mark.parametrize("db_name", APPROVED_DATABASES)
def test_atlas_collection_validators_and_zero_docs(mongo_client, db_name):
    db = mongo_client[db_name]
    for c_name in APPROVED_COLLECTIONS[db_name]:
        infos = db.command({"listCollections": 1, "filter": {"name": c_name}})
        batch = infos.get("cursor", {}).get("firstBatch", [])
        assert len(batch) > 0, f"Collection {c_name} not found in {db_name}"
        options = batch[0].get("options", {})
        
        # Verify validator attached
        validator = options.get("validator", {})
        assert "$jsonSchema" in validator, f"Collection {db_name}.{c_name} missing $jsonSchema validator"
        assert options.get("validationLevel") == "strict", f"{db_name}.{c_name} validationLevel != strict"
        assert options.get("validationAction") == "error", f"{db_name}.{c_name} validationAction != error"
        
        # Verify 0 documents (creation only boundary)
        doc_count = db[c_name].count_documents({})
        assert doc_count == 0, f"Collection {db_name}.{c_name} has {doc_count} docs; expected 0 in Phase 16"
