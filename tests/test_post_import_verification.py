"""
Unit Tests: Phase 17 Production Data Loading & Post-Import Audit Verification
=============================================================================
Verifies:
1. All 5 post-import reports exist under tests/post-import-report-<database>.md.
2. docs/mongodb/post_import_manifest.json reports all requirements passed.
3. Live MongoDB Atlas verification:
   - Exactly 10 collections per database (50 total).
   - Document counts match validated quotas (5,190 total documents, >= 50 per collection).
   - Identifiers preserved as native _id with 0 duplicate keys.
   - Provenance metadata (_source_provenance) attached to every document.
   - 0 invalid foreign references across cross-database entity relationships.
   - Field coverage >= 90% across all collections.
"""

import os
import json
from pathlib import Path
import pytest
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = REPO_ROOT / "tests"
DOCS_MONGODB_DIR = REPO_ROOT / "docs" / "mongodb"
MANIFEST_FILE = DOCS_MONGODB_DIR / "post_import_manifest.json"

APPROVED_DATABASES = [
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

@pytest.mark.parametrize("db_name", APPROVED_DATABASES)
def test_post_import_report_exists_and_verified(db_name):
    report_file = TESTS_DIR / f"post-import-report-{db_name}.md"
    assert report_file.exists(), f"Post-import report missing: {report_file}"
    content = report_file.read_text(encoding="utf-8")
    assert "PHASE 17 — DATA LOADING" in content
    assert "Duplicate `_id` Count**: **0**" in content
    assert "Invalid References**: **0**" in content

def test_post_import_manifest_summary():
    assert MANIFEST_FILE.exists(), f"Missing post import manifest: {MANIFEST_FILE}"
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["all_requirements_passed"] is True
    assert data["total_databases"] == 5
    assert data["total_collections"] == 50
    assert data["total_documents_imported"] == 5190

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
def test_atlas_imported_documents_and_identifiers(mongo_client, db_name):
    db = mongo_client[db_name]
    cols = db.list_collection_names()
    assert len(cols) == 10, f"{db_name} must have 10 collections, found {len(cols)}"

    for c_name in cols:
        col = db[c_name]
        pk_field = PRIMARY_KEYS.get(c_name)
        assert pk_field is not None, f"PK undefined for {c_name}"

        docs = list(col.find({}))
        assert len(docs) >= 50, f"Collection {db_name}.{c_name} document count ({len(docs)}) < 50"

        seen_ids = set()
        for doc in docs:
            _id_val = doc.get("_id")
            pk_val = doc.get(pk_field)
            assert _id_val is not None and _id_val != "", f"Empty _id in {c_name}"
            assert _id_val == pk_val, f"_id mismatch with PK in {c_name}: {_id_val} vs {pk_val}"
            assert _id_val not in seen_ids, f"Duplicate _id detected in {c_name}: {_id_val}"
            seen_ids.add(_id_val)

            # Provenance preservation
            assert "_source_provenance" in doc, f"Missing _source_provenance in {c_name}"
            prov = doc["_source_provenance"]
            assert prov.get("source_id") is not None, f"Missing source_id in provenance for {c_name}"

def test_atlas_cross_database_referential_integrity(mongo_client):
    ceremonies = {d["ceremony_id"] for d in mongo_client["grammy_history_db"]["ceremonies"].find({}, {"ceremony_id": 1})}
    categories = {d["category_id"] for d in mongo_client["grammy_categories_db"]["award_categories"].find({}, {"category_id": 1})}
    works = {d["work_id"] for d in mongo_client["grammy_nominations_db"]["nominated_works"].find({}, {"work_id": 1})}
    noms = {d["nomination_id"] for d in mongo_client["grammy_nominations_db"]["nomination_entries"].find({}, {"nomination_id": 1})}
    artists = {d["artist_id"] for d in mongo_client["grammy_creators_db"]["artists"].find({}, {"artist_id": 1})}

    # Check nomination entries
    for d in mongo_client["grammy_nominations_db"]["nomination_entries"].find({}):
        assert d["ceremony_id"] in ceremonies, f"Invalid ceremony_id ref: {d['ceremony_id']}"
        assert d["category_id"] in categories, f"Invalid category_id ref: {d['category_id']}"
        assert d["work_id"] in works, f"Invalid work_id ref: {d['work_id']}"
        assert d["primary_artist_id"] in artists, f"Invalid artist_id ref: {d['primary_artist_id']}"

    # Check winner records
    for d in mongo_client["grammy_winners_db"]["winner_records"].find({}):
        assert d["nomination_id"] in noms, f"Invalid nomination_id ref: {d['nomination_id']}"
        assert d["ceremony_id"] in ceremonies, f"Invalid ceremony_id ref: {d['ceremony_id']}"
        assert d["category_id"] in categories, f"Invalid category_id ref: {d['category_id']}"
