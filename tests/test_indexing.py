"""
=============================================================================
Phase 21 Test Suite: MongoDB Atlas Index Verification & Explain Plans
=============================================================================
Project: Advanced Database Management Systems (ADBMS)
Course Module: Module 10 — Advanced Query Operators & Multikey Indexing
Phase: PHASE 21 — INDEXING

Verifies:
  1. Live Atlas connectivity
  2. All 44 recommended indexes present and active across all 5 databases
  3. Unique constraint enforcement on secondary natural keys
  4. Multikey index behaviors on BSON array fields
  5. Compound ESR index key orderings
  6. Explain query plans transitioning from COLLSCAN to IXSCAN
  7. WiredTiger index storage allocation metrics
=============================================================================
"""

import os
import certifi
import pytest
import pymongo
from pathlib import Path
from dotenv import load_dotenv

import sys
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import index catalog directly from management script
from scripts.indexes.create_indexes import INDEX_CATALOG



@pytest.fixture(scope="session")
def mongo_client():
    """Session fixture for authenticated MongoDB client."""
    load_dotenv(REPO_ROOT / ".env")
    uri = os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    assert uri, "MONGODB_URI must be configured in .env"
    client = pymongo.MongoClient(
        uri,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
    )
    # Ping
    ping_res = client.admin.command("ping")
    assert ping_res.get("ok") == 1.0
    return client


def test_atlas_cluster_connection(mongo_client):
    """Verifies live connectivity to MongoDB Atlas cluster."""
    ping = mongo_client.admin.command("ping")
    assert ping.get("ok") == 1.0


def test_all_five_databases_exist(mongo_client):
    """Verifies that all 5 target databases are active on Atlas."""
    db_names = mongo_client.list_database_names()
    for expected_db in INDEX_CATALOG.keys():
        assert expected_db in db_names, f"Database {expected_db} missing from Atlas!"


@pytest.mark.parametrize("db_name", list(INDEX_CATALOG.keys()))
def test_all_indexes_present_in_database(mongo_client, db_name):
    """Verifies that every recommended index exists with proper key specification."""
    db = mongo_client[db_name]
    coll_catalog = INDEX_CATALOG[db_name]

    for coll_name, index_list in coll_catalog.items():
        coll = db[coll_name]
        existing_indexes = {idx["name"]: idx for idx in coll.list_indexes()}

        for idx_def in index_list:
            name = idx_def["name"]
            assert name in existing_indexes, f"Index '{name}' missing on {db_name}.{coll_name}"

            existing = existing_indexes[name]
            expected_keys = dict(idx_def["keys"])
            actual_keys = dict(existing["key"])
            assert actual_keys == expected_keys, (
                f"Index key mismatch on {coll_name}.{name}: expected {expected_keys}, got {actual_keys}"
            )

            if idx_def.get("unique", False):
                assert existing.get("unique") is True, (
                    f"Index {name} expected to be unique but got unique={existing.get('unique')}"
                )


def test_total_custom_index_count(mongo_client):
    """Verifies total count of custom indexes deployed across all 5 databases equals exactly 44."""
    total_custom_found = 0
    total_catalog_count = sum(
        len(indexes)
        for collections in INDEX_CATALOG.values()
        for indexes in collections.values()
    )
    assert total_catalog_count == 44, f"Expected 44 indexes in catalog, got {total_catalog_count}"

    for db_name, collections in INDEX_CATALOG.items():
        db = mongo_client[db_name]
        for coll_name, index_list in collections.items():
            coll = db[coll_name]
            existing_names = {idx["name"] for idx in coll.list_indexes()}
            for idx_def in index_list:
                if idx_def["name"] in existing_names:
                    total_custom_found += 1

    assert total_custom_found == 44, f"Expected 44 active custom indexes, found {total_custom_found}"


def test_unique_secondary_index_enforcement(mongo_client):
    """Verifies that unique secondary indexes reject duplicate key insertions."""
    db = mongo_client["grammy_history_db"]
    coll = db["ceremonies"]

    # Attempt inserting a duplicate ceremony_id (CEREMONY_001 already exists)
    duplicate_doc = {
        "_id": "CEREMONY_DUPLICATE_TEST_TEMP",
        "ceremony_id": "CEREMONY_001",  # duplicate natural key
        "edition_number": 999,
        "ceremony_date": "2099-01-01",
        "broadcast_year": 2099,
        "eligibility_period_start": "2098-01-01",
        "eligibility_period_end": "2098-12-31",
        "host_city": "Los Angeles",
        "venue_id": "VEN_BEVERLY_HILTON",
        "primary_network": "CBS",
        "total_awards_presented": 50,
        "created_at": "2099-01-01T00:00:00Z",
        "_source_provenance": {
            "source_id": "SRC-01",
            "source_name": "Test",
            "license_type": "Test",
            "provenance_tier": "PRIMARY OFFICIAL SOURCE"
        }
    }

    with pytest.raises(pymongo.errors.DuplicateKeyError):
        coll.insert_one(duplicate_doc)

    # Ensure no residual document
    coll.delete_one({"_id": "CEREMONY_DUPLICATE_TEST_TEMP"})


def test_multikey_index_queries_use_ixscan(mongo_client):
    """Verifies that queries over array fields utilize multikey IXSCAN."""
    # 1. Acceptance speeches individuals_acknowledged
    db_win = mongo_client["grammy_winners_db"]
    cursor1 = db_win.acceptance_speeches.find({"individuals_acknowledged": "Family"})
    explain1 = cursor1.explain()
    plan1 = explain1.get("queryPlanner", {}).get("winningPlan", {})

    def plan_has_stage(p, stage_name):
        if p.get("stage") == stage_name:
            return True
        if "inputStage" in p and plan_has_stage(p["inputStage"], stage_name):
            return True
        for ch in p.get("inputStages", []):
            if plan_has_stage(ch, stage_name):
                return True
        return False

    assert plan_has_stage(plan1, "IXSCAN"), "acceptance_speeches query should utilize IXSCAN"

    # 2. Merged split history source_category_ids
    db_cat = mongo_client["grammy_categories_db"]
    cursor2 = db_cat.merged_split_history.find({
        "source_category_ids": {"$all": ["LEGACY_CAT_MALE_0", "LEGACY_CAT_FEMALE_0"]}
    })
    explain2 = cursor2.explain()
    plan2 = explain2.get("queryPlanner", {}).get("winningPlan", {})
    assert plan_has_stage(plan2, "IXSCAN"), "merged_split_history query should utilize IXSCAN"


def test_compound_esr_query_plans_use_ixscan(mongo_client):
    """Verifies that compound queries adhering to ESR rule utilize IXSCAN without in-memory blocking sort."""
    db_nom = mongo_client["grammy_nominations_db"]
    # Query: Equality on is_winner_flag, Range on nomination_year, Sort on nomination_year / ballot_slot
    cursor = db_nom.nomination_entries.find({
        "is_winner_flag": True,
        "nomination_year": {"$gte": 1959, "$lte": 1965}
    }).sort([("nomination_year", -1), ("ballot_slot_order", 1)])

    explain = cursor.explain()
    winning_plan = explain.get("queryPlanner", {}).get("winningPlan", {})

    def plan_has_stage(p, stage_name):
        if p.get("stage") == stage_name:
            return True
        if "inputStage" in p and plan_has_stage(p["inputStage"], stage_name):
            return True
        for ch in p.get("inputStages", []):
            if plan_has_stage(ch, stage_name):
                return True
        return False

    assert plan_has_stage(winning_plan, "IXSCAN"), "Compound ESR query should utilize IXSCAN"
    # An optimal ESR compound index satisfies sort order directly, meaning no standalone blocking SORT stage
    assert not plan_has_stage(winning_plan, "SORT"), "ESR index should eliminate blocking SORT stage"


def test_single_field_point_lookup_efficiency(mongo_client):
    """Verifies that point lookups examine exactly 1 document and 1 index key."""
    db_nom = mongo_client["grammy_nominations_db"]
    cursor = db_nom.nomination_entries.find({"nomination_id": "NOM_001_RECORD_OF__0000"})
    explain = cursor.explain()
    exec_stats = explain.get("executionStats", {})

    assert exec_stats.get("totalDocsExamined") == 1, (
        f"Point lookup should examine exactly 1 doc, examined {exec_stats.get('totalDocsExamined')}"
    )
    assert exec_stats.get("totalKeysExamined") == 1, (
        f"Point lookup should examine exactly 1 key, examined {exec_stats.get('totalKeysExamined')}"
    )


def test_wiredtiger_index_storage_allocated(mongo_client):
    """Verifies that WiredTiger engine reports allocated index sizes for indexed collections."""
    db_nom = mongo_client["grammy_nominations_db"]
    stats = db_nom.command("collStats", "nomination_entries")

    assert stats.get("nindexes") >= 6, "nomination_entries should have at least 6 indexes (_id + 5 custom)"
    assert stats.get("totalIndexSize", 0) > 0, "totalIndexSize should be greater than 0 bytes"
