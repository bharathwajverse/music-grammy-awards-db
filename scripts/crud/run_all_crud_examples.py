"""
Phase 18: Live MongoDB Atlas CRUD Execution Engine & Verification Harness
========================================================================
Executes all 8 CRUD operations (insertOne, insertMany, find, findOne,
updateOne, updateMany, deleteOne, deleteMany) across all 5 databases:
1. grammy_history_db (ceremonies)
2. grammy_categories_db (award_categories)
3. grammy_nominations_db (nomination_entries)
4. grammy_winners_db (winner_records)
5. grammy_creators_db (artists)

Validates filtering and projection logic on each read operation.
Guarantees transactional cleanliness by removing all demonstration documents.
"""

import os
import re
import certifi
import pymongo
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

def mask_uri(uri: str) -> str:
    """Masks credentials in MongoDB URI for safe logging."""
    if not uri:
        return "<EMPTY>"
    return re.sub(r":([^@]+)@", ":****@", uri)

def get_mongo_client() -> pymongo.MongoClient:
    """Connects securely to MongoDB Atlas cluster."""
    load_dotenv(REPO_ROOT / ".env")
    uri = os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_URI not found in .env file!")
    
    masked = mask_uri(uri)
    print(f">> Connecting to MongoDB Atlas cluster: {masked}")
    
    client = pymongo.MongoClient(
        uri,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000
    )
    client.admin.command("ping")
    print(">> [SUCCESS] Successfully authenticated with MongoDB Atlas cluster.")
    return client

def run_crud_suite() -> Dict[str, Any]:
    """Executes and verifies all 8 CRUD operations across all 5 databases."""
    print("==================================================================")
    print("PHASE 18: EXECUTING LIVE CRUD SUITE ACROSS ALL 5 DATABASES")
    print("==================================================================")
    
    client = get_mongo_client()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    suite_results: Dict[str, Dict[str, Any]] = {}

    # --------------------------------------------------------------------------
    # Database 1: grammy_history_db (ceremonies)
    # --------------------------------------------------------------------------
    print("\n[1/5] Executing CRUD on `grammy_history_db.ceremonies`...")
    db_hist = client["grammy_history_db"]
    col_hist = db_hist["ceremonies"]
    col_hist.delete_many({"_id": {"$regex": "^CEREMONY_CRUD_DEMO_"}})
    initial_count = col_hist.count_documents({})

    # 1. insertOne
    doc1 = {
        "_id": "CEREMONY_CRUD_DEMO_01",
        "ceremony_id": "CEREMONY_CRUD_DEMO_01",
        "edition_number": 99,
        "ceremony_date": "2057-02-15",
        "broadcast_year": 2057,
        "eligibility_period_start": "2055-10-01",
        "eligibility_period_end": "2056-09-30",
        "host_city": "Los Angeles",
        "venue_id": "VEN_STAPLES_CRYPTO_ARENA",
        "primary_network": "CBS",
        "total_awards_presented": 84,
        "created_at": "2057-01-01T00:00:00Z"
    }
    r_ins_one = col_hist.insert_one(doc1)
    assert r_ins_one.inserted_id == "CEREMONY_CRUD_DEMO_01"

    # 2. insertMany
    docs_batch = [
        {
            "_id": "CEREMONY_CRUD_DEMO_02",
            "ceremony_id": "CEREMONY_CRUD_DEMO_02",
            "edition_number": 100,
            "ceremony_date": "2058-02-14",
            "broadcast_year": 2058,
            "eligibility_period_start": "2056-10-01",
            "eligibility_period_end": "2057-09-30",
            "host_city": "New York",
            "venue_id": "VEN_MADISON_SQUARE_GARDEN",
            "primary_network": "CBS",
            "total_awards_presented": 86,
            "created_at": "2058-01-01T00:00:00Z"
        },
        {
            "_id": "CEREMONY_CRUD_DEMO_03",
            "ceremony_id": "CEREMONY_CRUD_DEMO_03",
            "edition_number": 101,
            "ceremony_date": "2059-02-16",
            "broadcast_year": 2059,
            "eligibility_period_start": "2057-10-01",
            "eligibility_period_end": "2058-09-30",
            "host_city": "Nashville",
            "venue_id": "VEN_NASHVILLE_AUDITORIUM",
            "primary_network": "NBC",
            "total_awards_presented": 88,
            "created_at": "2059-01-01T00:00:00Z"
        }
    ]
    r_ins_many = col_hist.insert_many(docs_batch)
    assert len(r_ins_many.inserted_ids) == 2

    # 3. find (Filtering + Projection)
    find_docs = list(col_hist.find(
        {"broadcast_year": {"$gte": 2000, "$lte": 2024}, "primary_network": {"$in": ["CBS", "NBC"]}},
        {"_id": 0, "ceremony_id": 1, "edition_number": 1, "broadcast_year": 1, "primary_network": 1}
    ).limit(5))
    assert len(find_docs) > 0
    assert "_id" not in find_docs[0] and "ceremony_id" in find_docs[0]

    # 4. findOne (Filtering + Projection)
    find_one_doc = col_hist.find_one(
        {"ceremony_id": "CEREMONY_001"},
        {"_id": 0, "ceremony_id": 1, "edition_number": 1, "host_city": 1}
    )
    assert find_one_doc is not None
    assert find_one_doc["ceremony_id"] == "CEREMONY_001" and "_id" not in find_one_doc

    # 5. updateOne
    r_up_one = col_hist.update_one(
        {"ceremony_id": "CEREMONY_CRUD_DEMO_01"},
        {"$set": {"host_city": "Las Vegas"}, "$inc": {"total_awards_presented": 2}}
    )
    assert r_up_one.matched_count == 1 and r_up_one.modified_count == 1

    # 6. updateMany
    r_up_many = col_hist.update_many(
        {"ceremony_id": {"$regex": "^CEREMONY_CRUD_DEMO_"}},
        {"$set": {"venue_id": "VEN_TEMPORARY_STAGING"}}
    )
    assert r_up_many.matched_count == 3 and r_up_many.modified_count == 3

    # 7. deleteOne
    r_del_one = col_hist.delete_one({"ceremony_id": "CEREMONY_CRUD_DEMO_01"})
    assert r_del_one.deleted_count == 1

    # 8. deleteMany
    r_del_many = col_hist.delete_many({"ceremony_id": {"$regex": "^CEREMONY_CRUD_DEMO_"}})
    assert r_del_many.deleted_count == 2
    assert col_hist.count_documents({}) == initial_count

    suite_results["grammy_history_db"] = {
        "collection": "ceremonies",
        "operations_tested": ["insertOne", "insertMany", "find", "findOne", "updateOne", "updateMany", "deleteOne", "deleteMany"],
        "filtering_verified": True,
        "projection_verified": True,
        "clean_state_restored": True,
        "status": "PASSED"
    }

    # --------------------------------------------------------------------------
    # Database 2: grammy_categories_db (award_categories)
    # --------------------------------------------------------------------------
    print("[2/5] Executing CRUD on `grammy_categories_db.award_categories`...")
    db_cat = client["grammy_categories_db"]
    col_cat = db_cat["award_categories"]
    col_cat.delete_many({"_id": {"$regex": "^CAT_CRUD_DEMO_"}})
    initial_count_cat = col_cat.count_documents({})

    # 1. insertOne
    r_ins_one = col_cat.insert_one({
        "_id": "CAT_CRUD_DEMO_01",
        "category_id": "CAT_CRUD_DEMO_01",
        "field_id": "FLD_GEN",
        "official_category_name": "Best Experimental Spatial Audio Recording",
        "standard_short_code": "SPATIAL_AUDIO",
        "inaugural_edition": 70,
        "is_general_field": False,
        "current_status": "Active",
        "maximum_nominees_allowed": 5,
        "voting_tier_access": "Craft Specialist Voting Members",
        "trophy_statuette_eligibility_rule": "Presented to engineer and producer",
        "entry_fee_tier": "Standard OEP Tier 1"
    })
    assert r_ins_one.inserted_id == "CAT_CRUD_DEMO_01"

    # 2. insertMany
    r_ins_many = col_cat.insert_many([
        {
            "_id": "CAT_CRUD_DEMO_02",
            "category_id": "CAT_CRUD_DEMO_02",
            "field_id": "FLD_POP",
            "official_category_name": "Best Contemporary Hyperpop Vocal Performance",
            "standard_short_code": "HYPERPOP_VOC",
            "inaugural_edition": 71,
            "is_general_field": False,
            "current_status": "Active",
            "maximum_nominees_allowed": 5,
            "voting_tier_access": "Craft Specialist Voting Members",
            "trophy_statuette_eligibility_rule": "Presented to lead artists",
            "entry_fee_tier": "Standard OEP Tier 1"
        },
        {
            "_id": "CAT_CRUD_DEMO_03",
            "category_id": "CAT_CRUD_DEMO_03",
            "field_id": "FLD_GLOBAL",
            "official_category_name": "Best Global Electronic Fusion Album",
            "standard_short_code": "GLOBAL_FUSION",
            "inaugural_edition": 72,
            "is_general_field": False,
            "current_status": "Active",
            "maximum_nominees_allowed": 5,
            "voting_tier_access": "Craft Specialist Voting Members",
            "trophy_statuette_eligibility_rule": "Presented to lead artists",
            "entry_fee_tier": "Standard OEP Tier 1"
        }
    ])
    assert len(r_ins_many.inserted_ids) == 2

    # 3. find (Filtering + Projection)
    find_cats = list(col_cat.find(
        {"$or": [{"is_general_field": True}, {"official_category_name": {"$regex": "Album Of The Year", "$options": "i"}}]},
        {"_id": 0, "category_id": 1, "official_category_name": 1, "maximum_nominees_allowed": 1}
    ).limit(5))
    assert len(find_cats) > 0 and "_id" not in find_cats[0]

    # 4. findOne (Filtering + Projection)
    find_one_cat = col_cat.find_one(
        {"category_id": "CAT_RECORD_OF_THE_YEAR_000"},
        {"_id": 0, "category_id": 1, "official_category_name": 1}
    )
    assert find_one_cat is not None and "_id" not in find_one_cat

    # 5. updateOne
    r_up_one = col_cat.update_one(
        {"category_id": "CAT_CRUD_DEMO_01"},
        {"$inc": {"maximum_nominees_allowed": 3}, "$set": {"entry_fee_tier": "Premium Tier"}}
    )
    assert r_up_one.matched_count == 1 and r_up_one.modified_count == 1

    # 6. updateMany
    r_up_many = col_cat.update_many(
        {"category_id": {"$regex": "^CAT_CRUD_DEMO_"}},
        {"$set": {"current_status": "Pending Review"}}
    )
    assert r_up_many.matched_count == 3 and r_up_many.modified_count == 3

    # 7. deleteOne
    r_del_one = col_cat.delete_one({"category_id": "CAT_CRUD_DEMO_01"})
    assert r_del_one.deleted_count == 1

    # 8. deleteMany
    r_del_many = col_cat.delete_many({"category_id": {"$regex": "^CAT_CRUD_DEMO_"}})
    assert r_del_many.deleted_count == 2
    assert col_cat.count_documents({}) == initial_count_cat

    suite_results["grammy_categories_db"] = {
        "collection": "award_categories",
        "operations_tested": ["insertOne", "insertMany", "find", "findOne", "updateOne", "updateMany", "deleteOne", "deleteMany"],
        "filtering_verified": True,
        "projection_verified": True,
        "clean_state_restored": True,
        "status": "PASSED"
    }

    # --------------------------------------------------------------------------
    # Database 3: grammy_nominations_db (nomination_entries)
    # --------------------------------------------------------------------------
    print("[3/5] Executing CRUD on `grammy_nominations_db.nomination_entries`...")
    db_nom = client["grammy_nominations_db"]
    col_nom = db_nom["nomination_entries"]
    col_nom.delete_many({"_id": {"$regex": "^NOM_CRUD_DEMO_"}})
    initial_count_nom = col_nom.count_documents({})

    # 1. insertOne
    r_ins_one = col_nom.insert_one({
        "_id": "NOM_CRUD_DEMO_01",
        "nomination_id": "NOM_CRUD_DEMO_01",
        "ceremony_id": "CEREMONY_066",
        "category_id": "CAT_RECORD_OF_THE_YEAR_000",
        "work_id": "WRK_FLOWERS_0001",
        "nomination_year": 2024,
        "entry_billing_title": "Flowers (Demo Master Entry)",
        "primary_artist_id": "CRT_MILEY_CYRUS_0001",
        "is_winner_flag": False,
        "ballot_slot_order": 1,
        "auditor_validation_code": "DELOITTE-AUDIT-VALID-2024-DEMO1",
        "created_timestamp": "2024-01-10T12:00:00Z"
    })
    assert r_ins_one.inserted_id == "NOM_CRUD_DEMO_01"

    # 2. insertMany
    r_ins_many = col_nom.insert_many([
        {
            "_id": "NOM_CRUD_DEMO_02",
            "nomination_id": "NOM_CRUD_DEMO_02",
            "ceremony_id": "CEREMONY_066",
            "category_id": "CAT_ALBUM_OF_THE_YEAR_001",
            "work_id": "WRK_MIDNIGHTS_0002",
            "nomination_year": 2024,
            "entry_billing_title": "Midnights (Demo Album Entry)",
            "primary_artist_id": "CRT_TAYLOR_SWIFT_0002",
            "is_winner_flag": True,
            "ballot_slot_order": 2,
            "auditor_validation_code": "DELOITTE-AUDIT-VALID-2024-DEMO2",
            "created_timestamp": "2024-01-10T12:05:00Z"
        },
        {
            "_id": "NOM_CRUD_DEMO_03",
            "nomination_id": "NOM_CRUD_DEMO_03",
            "ceremony_id": "CEREMONY_066",
            "category_id": "CAT_SONG_OF_THE_YEAR_002",
            "work_id": "WRK_WHAT_WAS_I_MADE_FOR_0003",
            "nomination_year": 2024,
            "entry_billing_title": "What Was I Made For? (Demo Song Entry)",
            "primary_artist_id": "CRT_BILLIE_EILISH_0003",
            "is_winner_flag": True,
            "ballot_slot_order": 3,
            "auditor_validation_code": "DELOITTE-AUDIT-VALID-2024-DEMO3",
            "created_timestamp": "2024-01-10T12:10:00Z"
        }
    ])
    assert len(r_ins_many.inserted_ids) == 2

    # 3. find (Filtering + Projection)
    find_noms = list(col_nom.find(
        {"$and": [{"is_winner_flag": True}, {"nomination_year": {"$gte": 2000}}, {"ballot_slot_order": {"$lte": 3}}]},
        {"_id": 0, "nomination_id": 1, "entry_billing_title": 1, "nomination_year": 1}
    ).limit(5))
    assert len(find_noms) > 0 and "_id" not in find_noms[0]

    # 4. findOne (Filtering + Projection)
    find_one_nom = col_nom.find_one(
        {"nomination_id": "NOM_001_RECORD_OF__0000"},
        {"_id": 0, "nomination_id": 1, "entry_billing_title": 1}
    )
    assert find_one_nom is not None and "_id" not in find_one_nom

    # 5. updateOne
    r_up_one = col_nom.update_one(
        {"nomination_id": "NOM_CRUD_DEMO_01"},
        {"$set": {"is_winner_flag": True, "auditor_validation_code": "DELOITTE-AUDIT-WINNER-CONFIRMED-DEMO"}}
    )
    assert r_up_one.matched_count == 1 and r_up_one.modified_count == 1

    # 6. updateMany
    r_up_many = col_nom.update_many(
        {"nomination_id": {"$regex": "^NOM_CRUD_DEMO_"}},
        {"$set": {"entry_billing_title": "Audited Demonstration Entry"}}
    )
    assert r_up_many.matched_count == 3 and r_up_many.modified_count == 3

    # 7. deleteOne
    r_del_one = col_nom.delete_one({"nomination_id": "NOM_CRUD_DEMO_01"})
    assert r_del_one.deleted_count == 1

    # 8. deleteMany
    r_del_many = col_nom.delete_many({"nomination_id": {"$regex": "^NOM_CRUD_DEMO_"}})
    assert r_del_many.deleted_count == 2
    assert col_nom.count_documents({}) == initial_count_nom

    suite_results["grammy_nominations_db"] = {
        "collection": "nomination_entries",
        "operations_tested": ["insertOne", "insertMany", "find", "findOne", "updateOne", "updateMany", "deleteOne", "deleteMany"],
        "filtering_verified": True,
        "projection_verified": True,
        "clean_state_restored": True,
        "status": "PASSED"
    }

    # --------------------------------------------------------------------------
    # Database 4: grammy_winners_db (winner_records)
    # --------------------------------------------------------------------------
    print("[4/5] Executing CRUD on `grammy_winners_db.winner_records`...")
    db_win = client["grammy_winners_db"]
    col_win = db_win["winner_records"]
    col_win.delete_many({"_id": {"$regex": "^WIN_CRUD_DEMO_"}})
    initial_count_win = col_win.count_documents({})

    # 1. insertOne
    r_ins_one = col_win.insert_one({
        "_id": "WIN_CRUD_DEMO_01",
        "winner_record_id": "WIN_CRUD_DEMO_01",
        "nomination_id": "NOM_001_RECORD_OF__0000",
        "ceremony_id": "CEREMONY_066",
        "category_id": "CAT_RECORD_OF_THE_YEAR_000",
        "winning_work_id": "WRK_FLOWERS_0001",
        "primary_artist_id": "CRT_MILEY_CYRUS_0001",
        "broadcast_presentation_order": 12,
        "presented_live_on_telecast": True,
        "acceptance_speech_delivered": False,
        "trophy_statuettes_awarded_count": 2,
        "verified_timestamp": "2024-02-04T23:30:00Z"
    })
    assert r_ins_one.inserted_id == "WIN_CRUD_DEMO_01"

    # 2. insertMany
    r_ins_many = col_win.insert_many([
        {
            "_id": "WIN_CRUD_DEMO_02",
            "winner_record_id": "WIN_CRUD_DEMO_02",
            "nomination_id": "NOM_001_RECORD_OF__0000",
            "ceremony_id": "CEREMONY_066",
            "category_id": "CAT_ALBUM_OF_THE_YEAR_001",
            "winning_work_id": "WRK_MIDNIGHTS_0002",
            "primary_artist_id": "CRT_TAYLOR_SWIFT_0002",
            "broadcast_presentation_order": 15,
            "presented_live_on_telecast": True,
            "acceptance_speech_delivered": False,
            "trophy_statuettes_awarded_count": 4,
            "verified_timestamp": "2024-02-04T23:45:00Z"
        },
        {
            "_id": "WIN_CRUD_DEMO_03",
            "winner_record_id": "WIN_CRUD_DEMO_03",
            "nomination_id": "NOM_001_RECORD_OF__0000",
            "ceremony_id": "CEREMONY_066",
            "category_id": "CAT_SONG_OF_THE_YEAR_002",
            "winning_work_id": "WRK_WHAT_WAS_I_MADE_FOR_0003",
            "primary_artist_id": "CRT_BILLIE_EILISH_0003",
            "broadcast_presentation_order": 10,
            "presented_live_on_telecast": True,
            "acceptance_speech_delivered": False,
            "trophy_statuettes_awarded_count": 2,
            "verified_timestamp": "2024-02-04T23:15:00Z"
        }
    ])
    assert len(r_ins_many.inserted_ids) == 2

    # 3. find (Filtering + Projection)
    find_wins = list(col_win.find(
        {"presented_live_on_telecast": True, "trophy_statuettes_awarded_count": {"$gte": 2}},
        {"_id": 0, "winner_record_id": 1, "primary_artist_id": 1, "trophy_statuettes_awarded_count": 1}
    ).limit(5))
    assert len(find_wins) > 0 and "_id" not in find_wins[0]

    # 4. findOne (Filtering + Projection)
    find_one_win = col_win.find_one(
        {"winner_record_id": "WIN_NOM_001_RECORD_OF__0000"},
        {"_id": 0, "winner_record_id": 1, "primary_artist_id": 1}
    )
    assert find_one_win is not None and "_id" not in find_one_win

    # 5. updateOne
    r_up_one = col_win.update_one(
        {"winner_record_id": "WIN_CRUD_DEMO_01"},
        {"$inc": {"trophy_statuettes_awarded_count": 1}, "$set": {"broadcast_presentation_order": 1}}
    )
    assert r_up_one.matched_count == 1 and r_up_one.modified_count == 1

    # 6. updateMany
    r_up_many = col_win.update_many(
        {"winner_record_id": {"$regex": "^WIN_CRUD_DEMO_"}},
        {"$set": {"acceptance_speech_delivered": True}}
    )
    assert r_up_many.matched_count == 3 and r_up_many.modified_count == 3

    # 7. deleteOne
    r_del_one = col_win.delete_one({"winner_record_id": "WIN_CRUD_DEMO_01"})
    assert r_del_one.deleted_count == 1

    # 8. deleteMany
    r_del_many = col_win.delete_many({"winner_record_id": {"$regex": "^WIN_CRUD_DEMO_"}})
    assert r_del_many.deleted_count == 2
    assert col_win.count_documents({}) == initial_count_win

    suite_results["grammy_winners_db"] = {
        "collection": "winner_records",
        "operations_tested": ["insertOne", "insertMany", "find", "findOne", "updateOne", "updateMany", "deleteOne", "deleteMany"],
        "filtering_verified": True,
        "projection_verified": True,
        "clean_state_restored": True,
        "status": "PASSED"
    }

    # --------------------------------------------------------------------------
    # Database 5: grammy_creators_db (artists)
    # --------------------------------------------------------------------------
    print("[5/5] Executing CRUD on `grammy_creators_db.artists`...")
    db_crt = client["grammy_creators_db"]
    col_crt = db_crt["artists"]
    col_crt.delete_many({"_id": {"$regex": "^CRT_CRUD_DEMO_"}})
    initial_count_crt = col_crt.count_documents({})

    # 1. insertOne
    r_ins_one = col_crt.insert_one({
        "_id": "CRT_CRUD_DEMO_01",
        "artist_id": "CRT_CRUD_DEMO_01",
        "full_legal_name": "Demo Vanguard Ensemble Group",
        "stage_name": "Demo Vanguard Ensemble",
        "primary_musical_genre": "Pop / Vocal",
        "birth_or_formation_date": "2005-06-20",
        "country_of_citizenship": "United States",
        "active_career_start_year": 2020,
        "is_group_ensemble_flag": True,
        "musicbrainz_artist_gid": "b7132962-d922-4a0e-9477-88981d330001",
        "official_website_url": "https://musicbrainz.org/artist/b7132962-d922-4a0e-9477-88981d330001",
        "biography_overview": "Demo Vanguard Ensemble Group is an acclaimed experimental pop recording ensemble."
    })
    assert r_ins_one.inserted_id == "CRT_CRUD_DEMO_01"

    # 2. insertMany
    r_ins_many = col_crt.insert_many([
        {
            "_id": "CRT_CRUD_DEMO_02",
            "artist_id": "CRT_CRUD_DEMO_02",
            "full_legal_name": "Aura Symphony Project",
            "stage_name": "Aura Symphony Collective",
            "primary_musical_genre": "Classical Crossover",
            "birth_or_formation_date": "2010-09-15",
            "country_of_citizenship": "United Kingdom",
            "active_career_start_year": 2022,
            "is_group_ensemble_flag": True,
            "musicbrainz_artist_gid": "c8142962-d922-4a0e-9477-88981d330002",
            "official_website_url": "https://musicbrainz.org/artist/c8142962-d922-4a0e-9477-88981d330002",
            "biography_overview": "Aura Symphony Collective is an international classical crossover performance group."
        },
        {
            "_id": "CRT_CRUD_DEMO_03",
            "artist_id": "CRT_CRUD_DEMO_03",
            "full_legal_name": "Neon Rhythm Productions",
            "stage_name": "Neon Rhythm Syndicate",
            "primary_musical_genre": "R&B / Soul",
            "birth_or_formation_date": "1998-04-12",
            "country_of_citizenship": "United States",
            "active_career_start_year": 2018,
            "is_group_ensemble_flag": False,
            "musicbrainz_artist_gid": "d9152962-d922-4a0e-9477-88981d330003",
            "official_website_url": "https://musicbrainz.org/artist/d9152962-d922-4a0e-9477-88981d330003",
            "biography_overview": "Neon Rhythm Syndicate is a contemporary urban soul and R&B music producer and solo artist."
        }
    ])
    assert len(r_ins_many.inserted_ids) == 2

    # 3. find (Filtering + Projection)
    find_crts = list(col_crt.find(
        {"active_career_start_year": {"$gte": 1950}, "country_of_citizenship": {"$in": ["United States", "Canada", "United Kingdom"]}},
        {"_id": 0, "artist_id": 1, "stage_name": 1, "primary_musical_genre": 1, "active_career_start_year": 1}
    ).limit(5))
    assert len(find_crts) > 0 and "_id" not in find_crts[0]

    # 4. findOne (Filtering + Projection)
    find_one_crt = col_crt.find_one(
        {"artist_id": "CRT_HENRY_MANCINI_0001"},
        {"_id": 0, "artist_id": 1, "stage_name": 1, "active_career_start_year": 1}
    )
    assert find_one_crt is not None and "_id" not in find_one_crt

    # 5. updateOne
    r_up_one = col_crt.update_one(
        {"artist_id": "CRT_CRUD_DEMO_01"},
        {"$set": {"biography_overview": "Updated biography overview for demo ensemble celebrating milestone achievements."}}
    )
    assert r_up_one.matched_count == 1 and r_up_one.modified_count == 1

    # 6. updateMany
    r_up_many = col_crt.update_many(
        {"artist_id": {"$regex": "^CRT_CRUD_DEMO_"}},
        {"$set": {"country_of_citizenship": "International"}}
    )
    assert r_up_many.matched_count == 3 and r_up_many.modified_count == 3

    # 7. deleteOne
    r_del_one = col_crt.delete_one({"artist_id": "CRT_CRUD_DEMO_01"})
    assert r_del_one.deleted_count == 1

    # 8. deleteMany
    r_del_many = col_crt.delete_many({"artist_id": {"$regex": "^CRT_CRUD_DEMO_"}})
    assert r_del_many.deleted_count == 2
    assert col_crt.count_documents({}) == initial_count_crt

    suite_results["grammy_creators_db"] = {
        "collection": "artists",
        "operations_tested": ["insertOne", "insertMany", "find", "findOne", "updateOne", "updateMany", "deleteOne", "deleteMany"],
        "filtering_verified": True,
        "projection_verified": True,
        "clean_state_restored": True,
        "status": "PASSED"
    }

    print("\n>> All 5 databases passed live CRUD verification!")
    return suite_results

if __name__ == "__main__":
    run_crud_suite()
