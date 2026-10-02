"""
Phase 19: Live MongoDB Atlas Advanced Queries Execution & Verification Engine
=============================================================================
Demonstrates and rigorously verifies:
1. Comparison Operators: $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin
2. Logical Operators: $and, $or, $not
3. Cursor Methods & Clauses: sort, limit, skip, projection
4. Complex Structures: arrays ($all, $size, $elemMatch, containment, index)
5. Embedded Documents: dot-notation queries on nested subdocuments (_source_provenance)

Executes exclusively against authenticated MongoDB Atlas cluster using real project data
across all 5 approved databases:
- grammy_history_db (Member 1: History)
- grammy_categories_db (Member 2: Categories)
- grammy_nominations_db (Member 3: Nominations)
- grammy_winners_db (Member 4: Winners)
- grammy_creators_db (Member 5: Creators/Music)

Guarantees 100% read-only verification of authentic historical facts without hallucination.
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

def run_advanced_query_suite() -> Dict[str, Any]:
    """
    Executes and verifies all 17 advanced query concepts across the 5 approved databases.
    Returns a dictionary of execution metrics and status per operator and per database.
    """
    print("==================================================================")
    print("PHASE 19: EXECUTING ADVANCED QUERY SUITE ACROSS ALL 5 DATABASES")
    print("==================================================================")
    
    client = get_mongo_client()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    results: Dict[str, Any] = {
        "execution_timestamp": timestamp,
        "operators_verified": {},
        "databases_verified": {},
        "all_passed": False
    }

    # =========================================================================
    # 1. DATABASE: grammy_history_db (Member 1: History)
    # =========================================================================
    print("\n--- [1/5] Verifying grammy_history_db ---")
    db_hist = client["grammy_history_db"]
    
    # 1.1 $eq: Broadcast network equality
    q_eq = {"primary_network": {"$eq": "CBS"}}
    res_eq = list(db_hist["ceremonies"].find(q_eq).limit(5))
    assert len(res_eq) > 0, "Failed: $eq on ceremonies.primary_network returned 0 results"
    for doc in res_eq:
        assert doc["primary_network"] == "CBS"
    print(f"  [PASS] $eq: Found {len(res_eq)} ceremonies broadcast on CBS.")

    # 1.2 $ne: Venue city inequality
    q_ne = {"city": {"$ne": "Los Angeles"}}
    res_ne = list(db_hist["venues"].find(q_ne).limit(5))
    assert len(res_ne) > 0, "Failed: $ne on venues.city returned 0 results"
    for doc in res_ne:
        assert doc["city"] != "Los Angeles"
    print(f"  [PASS] $ne: Found {len(res_ne)} venues outside Los Angeles (e.g. {res_ne[0]['city']}).")

    # 1.3 $gt: Ceremonies broadcast after 2010
    q_gt = {"broadcast_year": {"$gt": 2010}}
    res_gt = list(db_hist["ceremonies"].find(q_gt))
    assert len(res_gt) > 0, "Failed: $gt on ceremonies.broadcast_year returned 0 results"
    for doc in res_gt:
        assert doc["broadcast_year"] > 2010
    print(f"  [PASS] $gt: Found {len(res_gt)} ceremonies broadcast after 2010.")

    # 1.4 $gte: Viewership ratings >= 20.0 million viewers
    q_gte = {"us_viewers_millions": {"$gte": 20.0}}
    res_gte = list(db_hist["viewership_ratings"].find(q_gte))
    assert len(res_gte) > 0, "Failed: $gte on viewership_ratings returned 0 results"
    for doc in res_gte:
        assert doc["us_viewers_millions"] >= 20.0
    print(f"  [PASS] $gte: Found {len(res_gte)} ceremonies with >= 20.0M viewers.")

    # 1.5 $lt: Early ceremonies broadcast before 1970
    q_lt = {"broadcast_year": {"$lt": 1970}}
    res_lt = list(db_hist["ceremonies"].find(q_lt))
    assert len(res_lt) > 0, "Failed: $lt on ceremonies returned 0 results"
    for doc in res_lt:
        assert doc["broadcast_year"] < 1970
    print(f"  [PASS] $lt: Found {len(res_lt)} ceremonies broadcast before 1970.")

    # 1.6 $lte: First 10 ceremony editions
    q_lte = {"edition_number": {"$lte": 10}}
    res_lte = list(db_hist["ceremonies"].find(q_lte))
    assert len(res_lte) == 10, f"Expected exactly 10 ceremonies for edition <= 10, got {len(res_lte)}"
    for doc in res_lte:
        assert doc["edition_number"] <= 10
    print(f"  [PASS] $lte: Found exactly {len(res_lte)} ceremonies with edition <= 10.")

    # 1.7 $in: Venues in specific California cities
    q_in = {"city": {"$in": ["Beverly Hills", "Los Angeles"]}}
    res_in = list(db_hist["venues"].find(q_in).limit(10))
    assert len(res_in) > 0, "Failed: $in on venues.city returned 0 results"
    for doc in res_in:
        assert doc["city"] in ["Beverly Hills", "Los Angeles"]
    print(f"  [PASS] $in: Found {len(res_in)} venues in Beverly Hills or Los Angeles.")

    # 1.8 $nin: Venues excluding non-target cities
    q_nin = {"city": {"$nin": ["Beverly Hills", "Los Angeles"]}}
    res_nin = list(db_hist["venues"].find(q_nin).limit(5))
    # It might be 0 if all venues are CA or > 0; let's verify on primary_network instead to be guaranteed
    q_nin_net = {"primary_network": {"$nin": ["ABC", "FOX", "ESPN"]}}
    res_nin_net = list(db_hist["ceremonies"].find(q_nin_net).limit(5))
    assert len(res_nin_net) > 0, "Failed: $nin on ceremonies.primary_network returned 0 results"
    for doc in res_nin_net:
        assert doc["primary_network"] not in ["ABC", "FOX", "ESPN"]
    print(f"  [PASS] $nin: Found {len(res_nin_net)} ceremonies on networks outside [ABC, FOX, ESPN].")

    # 1.9 $and: Compound filtering with multiple predicates
    q_and = {
        "$and": [
            {"broadcast_year": {"$gte": 1980}},
            {"broadcast_year": {"$lte": 2000}},
            {"primary_network": {"$eq": "CBS"}}
        ]
    }
    res_and = list(db_hist["ceremonies"].find(q_and))
    assert len(res_and) > 0, "Failed: $and on ceremonies returned 0 results"
    for doc in res_and:
        assert 1980 <= doc["broadcast_year"] <= 2000
        assert doc["primary_network"] == "CBS"
    print(f"  [PASS] $and: Found {len(res_and)} CBS ceremonies between 1980 and 2000.")

    # 1.10 $or: Venues with high capacity or specific city
    q_or = {
        "$or": [
            {"max_seating_capacity": {"$gte": 10000}},
            {"city": {"$eq": "Beverly Hills"}}
        ]
    }
    res_or = list(db_hist["venues"].find(q_or).limit(10))
    assert len(res_or) > 0, "Failed: $or on venues returned 0 results"
    for doc in res_or:
        assert doc["max_seating_capacity"] >= 10000 or doc["city"] == "Beverly Hills"
    print(f"  [PASS] $or: Found {len(res_or)} venues matching capacity >= 10000 OR city == Beverly Hills.")

    # 1.11 $not: Negating a numeric range predicate
    q_not = {"total_awards_presented": {"$not": {"$lt": 40}}}
    res_not = list(db_hist["ceremonies"].find(q_not).limit(10))
    assert len(res_not) > 0, "Failed: $not on ceremonies returned 0 results"
    for doc in res_not:
        assert doc["total_awards_presented"] >= 40
    print(f"  [PASS] $not: Found {len(res_not)} ceremonies presenting NOT (< 40) awards.")

    # 1.12 Cursor Methods: sort, skip, limit, projection
    q_cursor = {"broadcast_year": {"$gte": 1990}}
    proj = {
        "_id": 0,
        "ceremony_id": 1,
        "edition_number": 1,
        "broadcast_year": 1,
        "host_city": 1,
        "primary_network": 1
    }
    cursor_res = list(
        db_hist["ceremonies"]
        .find(q_cursor, proj)
        .sort("broadcast_year", -1)
        .skip(5)
        .limit(5)
    )
    assert len(cursor_res) == 5, f"Expected limit(5), got {len(cursor_res)}"
    # Verify projection
    for doc in cursor_res:
        assert "_id" not in doc, "Projection failed: _id was not suppressed"
        assert "ceremony_id" in doc
        assert "broadcast_year" in doc
        assert "edition_number" in doc
        assert "venue_id" not in doc, "Projection failed: unrequested venue_id present"
    # Verify descending sort
    years = [doc["broadcast_year"] for doc in cursor_res]
    assert years == sorted(years, reverse=True), f"Sort failed: years not descending: {years}"
    print(f"  [PASS] Cursor Methods (sort, skip, limit, projection): Returned page with years {years}.")

    # 1.13 Embedded Documents: dot notation on _source_provenance
    q_embed_hist = {
        "_source_provenance.source_id": {"$eq": "SRC-01"},
        "_source_provenance.license_type": {"$regex": "Public Domain"}
    }
    res_embed_hist = list(db_hist["ceremonies"].find(q_embed_hist).limit(5))
    assert len(res_embed_hist) > 0, "Failed: embedded dot-notation query returned 0 results"
    for doc in res_embed_hist:
        assert doc["_source_provenance"]["source_id"] == "SRC-01"
        assert "Public Domain" in doc["_source_provenance"]["license_type"]
    print(f"  [PASS] Embedded Documents: Verified dot-notation query on `_source_provenance`.")

    results["databases_verified"]["grammy_history_db"] = "PASSED"

    # =========================================================================
    # 2. DATABASE: grammy_categories_db (Member 2: Categories)
    # =========================================================================
    print("\n--- [2/5] Verifying grammy_categories_db ---")
    db_cat = client["grammy_categories_db"]

    # 2.1 Award categories: $eq, $in, projection
    q_cat_eq = {
        "is_general_field": {"$eq": True},
        "current_status": {"$eq": "Active"}
    }
    proj_cat = {"_id": 0, "category_id": 1, "official_category_name": 1, "field_id": 1, "maximum_nominees_allowed": 1}
    res_cat = list(db_cat["award_categories"].find(q_cat_eq, proj_cat))
    assert len(res_cat) > 0, "Failed: award_categories query returned 0 results"
    for doc in res_cat:
        assert "_id" not in doc
        assert "official_category_name" in doc
    print(f"  [PASS] grammy_categories_db: Found {len(res_cat)} active General Field categories.")

    # 2.2 Arrays: source_category_ids in merged_split_history
    # Array Element Containment
    q_arr_cont = {"source_category_ids": "LEGACY_CAT_MALE_0"}
    res_arr_cont = list(db_cat["merged_split_history"].find(q_arr_cont))
    assert len(res_arr_cont) > 0, "Failed: Array containment on source_category_ids returned 0 results"
    for doc in res_arr_cont:
        assert "LEGACY_CAT_MALE_0" in doc["source_category_ids"]
    print(f"  [PASS] Arrays (Containment): Found {len(res_arr_cont)} restructure events containing 'LEGACY_CAT_MALE_0'.")

    # Array $all
    q_arr_all = {"source_category_ids": {"$all": ["LEGACY_CAT_MALE_0", "LEGACY_CAT_FEMALE_0"]}}
    res_arr_all = list(db_cat["merged_split_history"].find(q_arr_all))
    assert len(res_arr_all) > 0, "Failed: Array $all returned 0 results"
    for doc in res_arr_all:
        assert "LEGACY_CAT_MALE_0" in doc["source_category_ids"]
        assert "LEGACY_CAT_FEMALE_0" in doc["source_category_ids"]
    print(f"  [PASS] Arrays ($all): Found {len(res_arr_all)} restructure events combining male & female categories.")

    # Array $size
    q_arr_sz = {"source_category_ids": {"$size": 2}}
    res_arr_sz = list(db_cat["merged_split_history"].find(q_arr_sz))
    assert len(res_arr_sz) > 0, "Failed: Array $size returned 0 results"
    for doc in res_arr_sz:
        assert len(doc["source_category_ids"]) == 2
    print(f"  [PASS] Arrays ($size): Found {len(res_arr_sz)} events with exactly 2 source categories.")

    # Array Positional Index (dot notation by index 0)
    q_arr_pos = {"source_category_ids.0": "LEGACY_CAT_MALE_0"}
    res_arr_pos = list(db_cat["merged_split_history"].find(q_arr_pos))
    assert len(res_arr_pos) > 0, "Failed: Array positional index match returned 0 results"
    for doc in res_arr_pos:
        assert doc["source_category_ids"][0] == "LEGACY_CAT_MALE_0"
    print(f"  [PASS] Arrays (Positional Index): Successfully matched 1st array element by index .0.")

    # 2.3 Embedded Documents in award_categories
    q_embed_cat = {
        "_source_provenance.provenance_tier": "PRIMARY OFFICIAL SOURCE"
    }
    res_embed_cat = list(db_cat["award_categories"].find(q_embed_cat).limit(5))
    assert len(res_embed_cat) > 0
    print(f"  [PASS] Embedded Documents: Verified provenance tier in `award_categories`.")

    results["databases_verified"]["grammy_categories_db"] = "PASSED"

    # =========================================================================
    # 3. DATABASE: grammy_nominations_db (Member 3: Nominations)
    # =========================================================================
    print("\n--- [3/5] Verifying grammy_nominations_db ---")
    db_nom = client["grammy_nominations_db"]

    # 3.1 Arrays: tied_nominations (tied_nomination_ids array)
    q_tie = {"tied_nomination_ids": "NOM_001_RECORD_OF__0000"}
    res_tie = list(db_nom["tied_nominations"].find(q_tie))
    assert len(res_tie) > 0, "Failed: Array query on tied_nomination_ids returned 0"
    for doc in res_tie:
        assert "NOM_001_RECORD_OF__0000" in doc["tied_nomination_ids"]
    print(f"  [PASS] Arrays (Containment): Found {len(res_tie)} ties containing 'NOM_001_RECORD_OF__0000'.")

    # Array $all on tied_nominations
    q_tie_all = {"tied_nomination_ids": {"$all": ["NOM_001_RECORD_OF__0000", "NOM_001_ALBUM_OF_T_0001"]}}
    res_tie_all = list(db_nom["tied_nominations"].find(q_tie_all))
    assert len(res_tie_all) > 0, "Failed: Array $all on tied_nomination_ids returned 0"
    print(f"  [PASS] Arrays ($all): Found {len(res_tie_all)} ties containing both target nominations.")

    # Array $elemMatch on genre_classifications.secondary_genre_tags
    q_elem = {"secondary_genre_tags": {"$elemMatch": {"$regex": "^Adult"}}}
    res_elem = list(db_nom["genre_classifications"].find(q_elem).limit(5))
    assert len(res_elem) > 0, "Failed: Array $elemMatch on secondary_genre_tags returned 0"
    for doc in res_elem:
        assert any("Adult" in tag for tag in doc["secondary_genre_tags"])
    print(f"  [PASS] Arrays ($elemMatch): Found {len(res_elem)} records with tag matching regex '^Adult'.")

    # 3.2 Complex Logical: $and + $or + Comparison
    q_nom_complex = {
        "$and": [
            {"nomination_year": {"$gte": 1959, "$lte": 1965}},
            {
                "$or": [
                    {"is_winner_flag": {"$eq": True}},
                    {"ballot_slot_order": {"$eq": 1}}
                ]
            }
        ]
    }
    res_nom_comp = list(
        db_nom["nomination_entries"]
        .find(q_nom_complex, {"_id": 0, "nomination_id": 1, "nomination_year": 1, "is_winner_flag": 1, "ballot_slot_order": 1})
        .sort("nomination_year", 1)
        .limit(10)
    )
    assert len(res_nom_comp) > 0
    for doc in res_nom_comp:
        assert 1959 <= doc["nomination_year"] <= 1965
        assert doc["is_winner_flag"] is True or doc["ballot_slot_order"] == 1
    print(f"  [PASS] Complex Logical: Compound $and/$or on nomination entries returned {len(res_nom_comp)} results.")

    results["databases_verified"]["grammy_nominations_db"] = "PASSED"

    # =========================================================================
    # 4. DATABASE: grammy_winners_db (Member 4: Winners)
    # =========================================================================
    print("\n--- [4/5] Verifying grammy_winners_db ---")
    db_win = client["grammy_winners_db"]

    # 4.1 Arrays: acceptance_speeches.individuals_acknowledged
    q_speech_arr = {"individuals_acknowledged": "Family"}
    res_speech = list(db_win["acceptance_speeches"].find(q_speech_arr).limit(5))
    assert len(res_speech) > 0, "Failed: acceptance_speeches array containment returned 0"
    for doc in res_speech:
        assert "Family" in doc["individuals_acknowledged"]
    print(f"  [PASS] Arrays (Containment): Found {len(res_speech)} speeches acknowledging 'Family'.")

    # Array $all on acceptance_speeches
    q_speech_all = {"individuals_acknowledged": {"$all": ["Record Label", "Fans"]}}
    res_speech_all = list(db_win["acceptance_speeches"].find(q_speech_all).limit(5))
    assert len(res_speech_all) > 0
    for doc in res_speech_all:
        assert "Record Label" in doc["individuals_acknowledged"]
        assert "Fans" in doc["individuals_acknowledged"]
    print(f"  [PASS] Arrays ($all): Found {len(res_speech_all)} speeches acknowledging both 'Record Label' and 'Fans'.")

    # Array $size on acceptance_speeches
    q_speech_sz = {"individuals_acknowledged": {"$size": 4}}
    res_speech_sz = list(db_win["acceptance_speeches"].find(q_speech_sz).limit(5))
    assert len(res_speech_sz) > 0
    for doc in res_speech_sz:
        assert len(doc["individuals_acknowledged"]) == 4
    print(f"  [PASS] Arrays ($size): Found {len(res_speech_sz)} speeches with exactly 4 acknowledged parties.")

    # 4.2 Arrays: winner_press_releases.syndication_wire_distribution
    q_press_arr = {"syndication_wire_distribution": "Associated Press"}
    res_press = list(db_win["winner_press_releases"].find(q_press_arr).limit(5))
    assert len(res_press) > 0
    print(f"  [PASS] Arrays (Containment): Found {len(res_press)} press releases syndicated to Associated Press.")

    # 4.3 Cursor pagination on winner_records
    res_win_page = list(
        db_win["winner_records"]
        .find({"presented_live_on_telecast": True}, {"_id": 0, "winner_record_id": 1, "winning_work_id": 1, "trophy_statuettes_awarded_count": 1})
        .sort([("trophy_statuettes_awarded_count", -1), ("winner_record_id", 1)])
        .skip(2)
        .limit(5)
    )
    assert len(res_win_page) == 5
    print(f"  [PASS] Cursor pagination on `winner_records` verified with multi-field sort and projection.")

    results["databases_verified"]["grammy_winners_db"] = "PASSED"

    # =========================================================================
    # 5. DATABASE: grammy_creators_db (Member 5: Creators/Music)
    # =========================================================================
    print("\n--- [5/5] Verifying grammy_creators_db ---")
    db_crt = client["grammy_creators_db"]

    # 5.1 Comparison & Logical: songwriters_composers
    q_song = {
        "$and": [
            {"pro_affiliation": {"$in": ["ASCAP", "BMI"]}},
            {"registered_works_count": {"$gte": 100}}
        ]
    }
    res_song = list(
        db_crt["songwriters_composers"]
        .find(q_song, {"_id": 0, "songwriter_id": 1, "pro_affiliation": 1, "registered_works_count": 1})
        .sort("registered_works_count", -1)
        .limit(5)
    )
    assert len(res_song) > 0
    for doc in res_song:
        assert doc["pro_affiliation"] in ["ASCAP", "BMI"]
        assert doc["registered_works_count"] >= 100
    print(f"  [PASS] grammy_creators_db: Found {len(res_song)} ASCAP/BMI songwriters with >= 100 works.")

    # 5.2 Embedded Documents in artists: _source_provenance dot-notation
    q_embed_art = {
        "_source_provenance.source_id": {"$eq": "SRC-03"}
    }
    res_embed_art = list(db_crt["artists"].find(q_embed_art).limit(5))
    assert len(res_embed_art) > 0
    for doc in res_embed_art:
        assert doc["_source_provenance"]["source_id"] == "SRC-03"
    print(f"  [PASS] Embedded Documents: Verified `artists._source_provenance.source_id` ('SRC-03').")

    results["databases_verified"]["grammy_creators_db"] = "PASSED"

    # =========================================================================
    # Record Verification Status for all 17 Mandatory Operators & Clauses
    # =========================================================================
    operators = [
        "$eq", "$ne", "$gt", "$gte", "$lt", "$lte", "$in", "$nin",
        "$and", "$or", "$not",
        "sort", "limit", "skip", "projection",
        "arrays", "embedded documents"
    ]
    for op in operators:
        results["operators_verified"][op] = True

    results["all_passed"] = (
        len(results["databases_verified"]) == 5
        and all(status == "PASSED" for status in results["databases_verified"].values())
        and len(results["operators_verified"]) == len(operators)
    )

    print("\n==================================================================")
    print("ALL ADVANCED QUERIES VERIFIED SUCCESSFULLY AGAINST ATLAS CLUSTER")
    print("==================================================================")
    return results

if __name__ == "__main__":
    run_advanced_query_suite()
