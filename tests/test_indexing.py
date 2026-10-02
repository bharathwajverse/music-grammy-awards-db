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


def plan_has_stage(p, stage_name):
    if not p:
        return False
    if p.get("stage") == stage_name:
        return True
    if "inputStage" in p and plan_has_stage(p["inputStage"], stage_name):
        return True
    for ch in p.get("inputStages", []):
        if plan_has_stage(ch, stage_name):
            return True
    return False


@pytest.mark.parametrize(
    "db_name,coll_name,key_field,duplicate_value",
    [
        ("grammy_history_db", "ceremonies", "ceremony_id", "CEREMONY_001"),
        ("grammy_categories_db", "award_categories", "category_id", "CAT_RECORD_OF_THE_YEAR_000"),
        ("grammy_nominations_db", "nominated_works", "work_id", "WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000"),
        ("grammy_winners_db", "winner_records", "winner_record_id", "WIN_NOM_001_RECORD_OF__0000"),
        ("grammy_creators_db", "artists", "artist_id", "CRT_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000"),
    ],
)
def test_unique_secondary_index_enforcement(mongo_client, db_name, coll_name, key_field, duplicate_value):
    """Verifies that unique secondary indexes reject duplicate key insertions across all 5 databases."""
    db = mongo_client[db_name]
    coll = db[coll_name]

    # Fetch an existing document to construct a valid duplicate document
    existing_doc = coll.find_one({key_field: duplicate_value})
    assert existing_doc is not None, f"Sample document with {key_field}={duplicate_value} not found!"

    # Clone document with a new distinct _id but identical natural key
    duplicate_doc = dict(existing_doc)
    duplicate_doc["_id"] = f"{duplicate_value}_DUPLICATE_TEST_TEMP"

    with pytest.raises(pymongo.errors.DuplicateKeyError):
        coll.insert_one(duplicate_doc)

    # Clean up test artifact if by any chance it persisted
    coll.delete_one({"_id": f"{duplicate_value}_DUPLICATE_TEST_TEMP"})


@pytest.mark.parametrize(
    "db_name,coll_name,query_filter,description",
    [
        ("grammy_winners_db", "acceptance_speeches", {"individuals_acknowledged": "Family"}, "Speech acknowledgments"),
        ("grammy_categories_db", "merged_split_history", {"source_category_ids": {"$all": ["LEGACY_CAT_MALE_0", "LEGACY_CAT_FEMALE_0"]}}, "Merged split history source categories"),
        ("grammy_nominations_db", "tied_nominations", {"tied_nomination_ids": "NOM_001_RECORD_OF__0000"}, "Tied nomination IDs"),
        ("grammy_nominations_db", "genre_classifications", {"secondary_genre_tags": "Adult Contemporary"}, "Genre classification tags"),
        ("grammy_nominations_db", "multi_nomination_packages", {"nominated_work_ids": "WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000"}, "Multi-nomination packages works"),
        ("grammy_winners_db", "consecutive_winners", {"winning_work_ids_list": "WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000"}, "Consecutive winning works list"),
    ],
)
def test_multikey_index_queries_use_ixscan(mongo_client, db_name, coll_name, query_filter, description):
    """Verifies that queries over all multikey array fields utilize IXSCAN."""
    db = mongo_client[db_name]
    coll = db[coll_name]
    cursor = coll.find(query_filter)
    explain = cursor.explain()
    plan = explain.get("queryPlanner", {}).get("winningPlan", {})

    assert plan_has_stage(plan, "IXSCAN"), f"Query on {db_name}.{coll_name} ({description}) should utilize IXSCAN"


@pytest.mark.parametrize(
    "db_name,coll_name,filter_spec,sort_spec,description",
    [
        (
            "grammy_nominations_db",
            "nomination_entries",
            {"is_winner_flag": True, "nomination_year": {"$gte": 1959, "$lte": 1965}},
            [("nomination_year", -1), ("ballot_slot_order", 1)],
            "nomination_entries winner + year range + ballot sort",
        ),
        (
            "grammy_history_db",
            "ceremonies",
            {"primary_network": "CBS", "broadcast_year": {"$gte": 2000}},
            [("broadcast_year", -1)],
            "ceremonies network + broadcast year sort",
        ),
        (
            "grammy_categories_db",
            "award_categories",
            {"current_status": "Active"},
            [("maximum_nominees_allowed", -1)],
            "award_categories active status + nominees capacity sort",
        ),
        (
            "grammy_winners_db",
            "winner_records",
            {"presented_live_on_telecast": True},
            [("trophy_statuettes_awarded_count", -1)],
            "winner_records live telecast + statuettes sort",
        ),
        (
            "grammy_creators_db",
            "artists",
            {"is_group_ensemble_flag": False, "active_career_start_year": {"$gte": 1950}},
            [("active_career_start_year", 1)],
            "artists solo flag + career start year sort",
        ),
    ],
)
def test_compound_esr_query_plans_use_ixscan(mongo_client, db_name, coll_name, filter_spec, sort_spec, description):
    """Verifies that compound queries adhering to ESR rule utilize IXSCAN without in-memory blocking sort."""
    db = mongo_client[db_name]
    coll = db[coll_name]
    cursor = coll.find(filter_spec).sort(sort_spec)
    explain = cursor.explain()
    winning_plan = explain.get("queryPlanner", {}).get("winningPlan", {})

    assert plan_has_stage(winning_plan, "IXSCAN"), f"ESR query on {coll_name} ({description}) should utilize IXSCAN"
    assert not plan_has_stage(winning_plan, "SORT"), f"ESR query on {coll_name} ({description}) should eliminate blocking SORT stage"


@pytest.mark.parametrize(
    "db_name,coll_name,point_filter",
    [
        ("grammy_nominations_db", "nomination_entries", {"nomination_id": "NOM_001_RECORD_OF__0000"}),
        ("grammy_history_db", "ceremonies", {"ceremony_id": "CEREMONY_001"}),
        ("grammy_creators_db", "artists", {"artist_id": "CRT_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000"}),
        ("grammy_history_db", "venues", {"venue_id": "VEN_BEVERLY_HILTON"}),
    ],
)
def test_single_field_point_lookup_efficiency(mongo_client, db_name, coll_name, point_filter):
    """Verifies that point lookups examine exactly 1 document and 1 index key."""
    db = mongo_client[db_name]
    coll = db[coll_name]
    cursor = coll.find(point_filter)
    explain = cursor.explain()
    exec_stats = explain.get("executionStats", {})

    assert exec_stats.get("totalDocsExamined") == 1, (
        f"Point lookup on {coll_name} should examine 1 doc, examined {exec_stats.get('totalDocsExamined')}"
    )
    assert exec_stats.get("totalKeysExamined") == 1, (
        f"Point lookup on {coll_name} should examine 1 key, examined {exec_stats.get('totalKeysExamined')}"
    )


def test_all_44_custom_indexes_produce_ixscan(mongo_client):
    """Verifies that EVERY SINGLE ONE of all 44 custom indexes in INDEX_CATALOG produces IXSCAN."""
    for db_name, collections in INDEX_CATALOG.items():
        db = mongo_client[db_name]
        for coll_name, index_list in collections.items():
            coll = db[coll_name]
            for idx_def in index_list:
                name = idx_def["name"]
                keys = idx_def["keys"]
                first_k, _ = keys[0]
                sample = coll.find_one({first_k: {"$exists": True, "$ne": None}})
                assert sample is not None, f"No sample found for {db_name}.{coll_name}.{first_k}"
                sample_val = sample[first_k]
                if isinstance(sample_val, list) and len(sample_val) > 0:
                    query_val = sample_val[0]
                else:
                    query_val = sample_val

                cursor = coll.find({first_k: query_val}).hint(name)
                explain = cursor.explain()
                wp = explain.get("queryPlanner", {}).get("winningPlan", {})
                has_scan = plan_has_stage(wp, "IXSCAN") or plan_has_stage(wp, "EXPRESS_IXSCAN")
                assert has_scan, f"Index {name} on {db_name}.{coll_name} failed to produce IXSCAN"


@pytest.mark.parametrize(
    "db_name,coll_name,min_indexes",
    [
        ("grammy_nominations_db", "nomination_entries", 6),
        ("grammy_history_db", "ceremonies", 5),
        ("grammy_categories_db", "award_categories", 5),
        ("grammy_winners_db", "winner_records", 5),
        ("grammy_creators_db", "artists", 4),
    ],
)
def test_wiredtiger_index_storage_allocated(mongo_client, db_name, coll_name, min_indexes):
    """Verifies that WiredTiger engine reports allocated index sizes for indexed collections."""
    db = mongo_client[db_name]
    stats = db.command("collStats", coll_name)

    assert stats.get("nindexes") >= min_indexes, f"{coll_name} should have >= {min_indexes} indexes"
    assert stats.get("totalIndexSize", 0) > 0, f"{coll_name} totalIndexSize should be > 0"

