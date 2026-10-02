#!/usr/bin/env python3
"""
=============================================================================
Phase 20: Aggregation Framework & Analytical Pipelines Execution Harness
=============================================================================
Project: Advanced Database Management Systems (ADBMS)
Module: Module 10 — Advanced Query & Aggregation Framework

Demonstrates:
  - $match
  - $group
  - $sort
  - $project
  - $count
  - $lookup
  - $unwind

Mandatory Analytical Pipelines:
  1. Nominations per artist
  2. Wins per artist
  3. Wins by category
  4. Nominations by year
  5. Category trends
  6. Artists appearing in multiple categories
  7. Multi-time winners

Calculated Results Label:
  Explicitly verified and marked as DERIVED.
=============================================================================
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
        connectTimeoutMS=10000,
    )
    client.admin.command("ping")
    print(">> [SUCCESS] Successfully authenticated with MongoDB Atlas cluster.")
    return client


def run_all_aggregations() -> Dict[str, Any]:
    """
    Executes and validates all analytical aggregation pipelines against live MongoDB Atlas cluster.
    """
    client = get_mongo_client()
    summary: Dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pipelines_executed": 0,
        "pipelines_passed": 0,
        "operators_verified": {},
        "pipeline_results": {},
    }

    db_nom = client["grammy_nominations_db"]
    db_win = client["grammy_winners_db"]
    db_cat = client["grammy_categories_db"]
    db_his = client["grammy_history_db"]

    print("\n" + "=" * 66)
    print("EXECUTING MANDATORY ANALYTICAL AGGREGATION PIPELINES (PHASE 20)")
    print("=" * 66)

    # -------------------------------------------------------------------------
    # Pipeline 1: Nominations per Artist
    # Operators: $match, $lookup, $unwind, $group, $project, $sort, $limit
    # -------------------------------------------------------------------------
    print("\n--- [1/7] Pipeline 01: Nominations per Artist ---")
    pipe01 = [
        {"$match": {"primary_artist_id": {"$exists": True, "$ne": None}}},
        {
            "$lookup": {
                "from": "nominated_works",
                "localField": "work_id",
                "foreignField": "work_id",
                "as": "work_details",
            }
        },
        {"$unwind": {"path": "$work_details", "preserveNullAndEmptyArrays": True}},
        {
            "$group": {
                "_id": "$primary_artist_id",
                "artist_billing_name": {"$first": "$entry_billing_title"},
                "DERIVED_total_nominations": {"$sum": 1},
                "DERIVED_earliest_nomination_year": {"$min": "$nomination_year"},
                "DERIVED_latest_nomination_year": {"$max": "$nomination_year"},
                "DERIVED_distinct_works": {"$addToSet": "$work_details.work_title"},
                "DERIVED_categories_nominated": {"$addToSet": "$category_id"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "artist_id": "$_id",
                "artist_billing_name": 1,
                "DERIVED_total_nominations": 1,
                "DERIVED_earliest_nomination_year": 1,
                "DERIVED_latest_nomination_year": 1,
                "DERIVED_career_span_years": {
                    "$subtract": [
                        "$DERIVED_latest_nomination_year",
                        "$DERIVED_earliest_nomination_year",
                    ]
                },
                "DERIVED_distinct_works_count": {"$size": "$DERIVED_distinct_works"},
                "DERIVED_distinct_categories_count": {
                    "$size": "$DERIVED_categories_nominated"
                },
                "DERIVED_calculation_status": {"$literal": "DERIVED"},
            }
        },
        {"$sort": {"DERIVED_total_nominations": -1, "artist_billing_name": 1}},
        {"$limit": 5},
    ]
    res01 = list(db_nom["nomination_entries"].aggregate(pipe01))
    assert len(res01) > 0, "Pipeline 01 returned zero results"
    for r in res01:
        assert "DERIVED_total_nominations" in r
        assert r["DERIVED_calculation_status"] == "DERIVED"
        assert r["DERIVED_total_nominations"] >= 1
    print(
        f"  [PASS] Top artist: {res01[0]['artist_billing_name']} with {res01[0]['DERIVED_total_nominations']} nominations across {res01[0]['DERIVED_distinct_categories_count']} categories."
    )
    summary["pipeline_results"]["01_nominations_per_artist"] = res01[0]
    summary["pipelines_executed"] += 1
    summary["pipelines_passed"] += 1

    # -------------------------------------------------------------------------
    # Pipeline 2: Wins per Artist
    # Operators: $match, $lookup, $group, $project, $sort, $limit
    # -------------------------------------------------------------------------
    print("\n--- [2/7] Pipeline 02: Wins per Artist ---")
    pipe02 = [
        {"$match": {"primary_artist_id": {"$exists": True, "$ne": None}}},
        {
            "$lookup": {
                "from": "acceptance_speeches",
                "localField": "winner_record_id",
                "foreignField": "winner_record_id",
                "as": "speech_records",
            }
        },
        {
            "$group": {
                "_id": "$primary_artist_id",
                "DERIVED_total_wins": {"$sum": 1},
                "DERIVED_total_statuettes_awarded": {
                    "$sum": "$trophy_statuettes_awarded_count"
                },
                "DERIVED_live_telecast_wins": {
                    "$sum": {"$cond": ["$presented_live_on_telecast", 1, 0]}
                },
                "DERIVED_speeches_delivered": {
                    "$sum": {"$cond": ["$acceptance_speech_delivered", 1, 0]}
                },
                "DERIVED_winning_categories": {"$addToSet": "$category_id"},
                "DERIVED_winning_ceremonies": {"$addToSet": "$ceremony_id"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "artist_id": "$_id",
                "DERIVED_total_wins": 1,
                "DERIVED_total_statuettes_awarded": 1,
                "DERIVED_avg_statuettes_per_win": {
                    "$round": [
                        {
                            "$divide": [
                                "$DERIVED_total_statuettes_awarded",
                                "$DERIVED_total_wins",
                            ]
                        },
                        2,
                    ]
                },
                "DERIVED_live_telecast_wins": 1,
                "DERIVED_speeches_delivered": 1,
                "DERIVED_distinct_winning_categories_count": {
                    "$size": "$DERIVED_winning_categories"
                },
                "DERIVED_distinct_ceremonies_count": {
                    "$size": "$DERIVED_winning_ceremonies"
                },
                "DERIVED_calculation_status": {"$literal": "DERIVED"},
            }
        },
        {"$sort": {"DERIVED_total_wins": -1, "DERIVED_total_statuettes_awarded": -1}},
        {"$limit": 5},
    ]
    res02 = list(db_win["winner_records"].aggregate(pipe02))
    assert len(res02) > 0, "Pipeline 02 returned zero results"
    for r in res02:
        assert "DERIVED_total_wins" in r
        assert r["DERIVED_calculation_status"] == "DERIVED"
        assert r["DERIVED_total_wins"] >= 1
    print(
        f"  [PASS] Top winning artist ID: {res02[0]['artist_id']} with {res02[0]['DERIVED_total_wins']} wins ({res02[0]['DERIVED_total_statuettes_awarded']} statuettes)."
    )
    summary["pipeline_results"]["02_wins_per_artist"] = res02[0]
    summary["pipelines_executed"] += 1
    summary["pipelines_passed"] += 1

    # -------------------------------------------------------------------------
    # Pipeline 3: Wins by Category
    # Operators: $match, $group, $project, $sort, $limit
    # -------------------------------------------------------------------------
    print("\n--- [3/7] Pipeline 03: Wins by Category ---")
    pipe03 = [
        {"$match": {"category_id": {"$exists": True, "$ne": None}}},
        {
            "$group": {
                "_id": "$category_id",
                "DERIVED_total_historical_wins": {"$sum": 1},
                "DERIVED_cumulative_statuettes": {
                    "$sum": "$trophy_statuettes_awarded_count"
                },
                "DERIVED_telecast_presentations": {
                    "$sum": {"$cond": ["$presented_live_on_telecast", 1, 0]}
                },
                "DERIVED_distinct_winners": {"$addToSet": "$primary_artist_id"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "category_id": "$_id",
                "DERIVED_total_historical_wins": 1,
                "DERIVED_cumulative_statuettes": 1,
                "DERIVED_telecast_presentations": 1,
                "DERIVED_telecast_percentage": {
                    "$round": [
                        {
                            "$multiply": [
                                {
                                    "$divide": [
                                        "$DERIVED_telecast_presentations",
                                        "$DERIVED_total_historical_wins",
                                    ]
                                },
                                100,
                            ]
                        },
                        2,
                    ]
                },
                "DERIVED_distinct_winners_count": {
                    "$size": "$DERIVED_distinct_winners"
                },
                "DERIVED_calculation_status": {"$literal": "DERIVED"},
            }
        },
        {
            "$sort": {
                "DERIVED_total_historical_wins": -1,
                "DERIVED_cumulative_statuettes": -1,
            }
        },
        {"$limit": 5},
    ]
    res03 = list(db_win["winner_records"].aggregate(pipe03))
    assert len(res03) > 0, "Pipeline 03 returned zero results"
    for r in res03:
        assert "DERIVED_total_historical_wins" in r
        assert r["DERIVED_calculation_status"] == "DERIVED"
    print(
        f"  [PASS] Top category: {res03[0]['category_id']} with {res03[0]['DERIVED_total_historical_wins']} wins ({res03[0]['DERIVED_telecast_percentage']}% on telecast)."
    )
    summary["pipeline_results"]["03_wins_by_category"] = res03[0]
    summary["pipelines_executed"] += 1
    summary["pipelines_passed"] += 1

    # -------------------------------------------------------------------------
    # Pipeline 4: Nominations by Year
    # Operators: $match, $group, $project, $sort
    # -------------------------------------------------------------------------
    print("\n--- [4/7] Pipeline 04: Nominations by Year ---")
    pipe04 = [
        {"$match": {"nomination_year": {"$exists": True, "$gte": 1958}}},
        {
            "$group": {
                "_id": "$nomination_year",
                "DERIVED_total_nominations": {"$sum": 1},
                "DERIVED_total_winners": {
                    "$sum": {"$cond": ["$is_winner_flag", 1, 0]}
                },
                "DERIVED_distinct_categories": {"$addToSet": "$category_id"},
                "DERIVED_distinct_nominees": {"$addToSet": "$primary_artist_id"},
                "DERIVED_average_ballot_slot": {"$avg": "$ballot_slot_order"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "ceremony_year": "$_id",
                "DERIVED_total_nominations": 1,
                "DERIVED_total_winners": 1,
                "DERIVED_distinct_categories_count": {
                    "$size": "$DERIVED_distinct_categories"
                },
                "DERIVED_distinct_nominees_count": {
                    "$size": "$DERIVED_distinct_nominees"
                },
                "DERIVED_avg_slot_depth": {
                    "$round": ["$DERIVED_average_ballot_slot", 2]
                },
                "DERIVED_calculation_status": {"$literal": "DERIVED"},
            }
        },
        {"$sort": {"ceremony_year": 1}},
        {"$limit": 5},
    ]
    res04 = list(db_nom["nomination_entries"].aggregate(pipe04))
    assert len(res04) > 0, "Pipeline 04 returned zero results"
    for r in res04:
        assert "DERIVED_total_nominations" in r
        assert r["DERIVED_calculation_status"] == "DERIVED"
    print(
        f"  [PASS] Inaugural year: {res04[0]['ceremony_year']} had {res04[0]['DERIVED_total_nominations']} nominations across {res04[0]['DERIVED_distinct_categories_count']} categories."
    )
    summary["pipeline_results"]["04_nominations_by_year"] = res04[0]
    summary["pipelines_executed"] += 1
    summary["pipelines_passed"] += 1

    # -------------------------------------------------------------------------
    # Pipeline 5: Category Trends
    # Operators: $match, $group, $project, $sort
    # -------------------------------------------------------------------------
    print("\n--- [5/7] Pipeline 05: Category Trends ---")
    pipe05 = [
        {
            "$match": {
                "category_id": {
                    "$in": [
                        "CAT_RECORD_OF_THE_YEAR_000",
                        "CAT_ALBUM_OF_THE_YEAR_001",
                        "CAT_SONG_OF_THE_YEAR_002",
                        "CAT_BEST_NEW_ARTIST_003",
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "category_id": "$category_id",
                    "decade": {
                        "$multiply": [
                            {"$floor": {"$divide": ["$nomination_year", 10]}},
                            10,
                        ]
                    },
                },
                "DERIVED_nominations_in_decade": {"$sum": 1},
                "DERIVED_winners_in_decade": {
                    "$sum": {"$cond": ["$is_winner_flag", 1, 0]}
                },
                "DERIVED_distinct_artists": {"$addToSet": "$primary_artist_id"},
                "min_year": {"$min": "$nomination_year"},
                "max_year": {"$max": "$nomination_year"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "category_id": "$_id.category_id",
                "decade_label": {"$concat": [{"$toString": "$_id.decade"}, "s"]},
                "DERIVED_nominations_count": "$DERIVED_nominations_in_decade",
                "DERIVED_winners_count": "$DERIVED_winners_in_decade",
                "DERIVED_distinct_artists_count": {
                    "$size": "$DERIVED_distinct_artists"
                },
                "DERIVED_decade_span": {
                    "$concat": [
                        {"$toString": "$min_year"},
                        " - ",
                        {"$toString": "$max_year"},
                    ]
                },
                "DERIVED_calculation_status": {"$literal": "DERIVED"},
            }
        },
        {"$sort": {"category_id": 1, "decade_label": 1}},
        {"$limit": 6},
    ]
    res05 = list(db_nom["nomination_entries"].aggregate(pipe05))
    assert len(res05) > 0, "Pipeline 05 returned zero results"
    for r in res05:
        assert "DERIVED_nominations_count" in r
        assert r["DERIVED_calculation_status"] == "DERIVED"
    print(
        f"  [PASS] Category trend: {res05[0]['category_id']} in {res05[0]['decade_label']} had {res05[0]['DERIVED_nominations_count']} nominations."
    )
    summary["pipeline_results"]["05_category_trends"] = res05[0]
    summary["pipelines_executed"] += 1
    summary["pipelines_passed"] += 1

    # -------------------------------------------------------------------------
    # Pipeline 6: Artists Appearing in Multiple Categories
    # Operators: $match, $group, $project, post-$match, $sort, $limit
    # -------------------------------------------------------------------------
    print("\n--- [6/7] Pipeline 06: Artists Appearing in Multiple Categories ---")
    pipe06 = [
        {"$match": {"primary_artist_id": {"$exists": True, "$ne": None}}},
        {
            "$group": {
                "_id": "$primary_artist_id",
                "artist_billing_title": {"$first": "$entry_billing_title"},
                "categories_set": {"$addToSet": "$category_id"},
                "years_set": {"$addToSet": "$nomination_year"},
                "DERIVED_total_nominations": {"$sum": 1},
            }
        },
        {
            "$project": {
                "_id": 0,
                "artist_id": "$_id",
                "artist_billing_title": 1,
                "DERIVED_distinct_categories_count": {"$size": "$categories_set"},
                "DERIVED_distinct_categories_list": "$categories_set",
                "DERIVED_distinct_years_count": {"$size": "$years_set"},
                "DERIVED_total_nominations": 1,
                "DERIVED_calculation_status": {"$literal": "DERIVED"},
            }
        },
        {"$match": {"DERIVED_distinct_categories_count": {"$gt": 1}}},
        {
            "$sort": {
                "DERIVED_distinct_categories_count": -1,
                "DERIVED_total_nominations": -1,
            }
        },
        {"$limit": 5},
    ]
    res06 = list(db_nom["nomination_entries"].aggregate(pipe06))
    assert len(res06) > 0, "Pipeline 06 returned zero results"
    for r in res06:
        assert r["DERIVED_distinct_categories_count"] > 1
        assert r["DERIVED_calculation_status"] == "DERIVED"
    print(
        f"  [PASS] Top versatile artist: {res06[0]['artist_billing_title']} appeared in {res06[0]['DERIVED_distinct_categories_count']} distinct categories across {res06[0]['DERIVED_distinct_years_count']} years."
    )
    summary["pipeline_results"]["06_artists_in_multiple_categories"] = res06[0]
    summary["pipelines_executed"] += 1
    summary["pipelines_passed"] += 1

    # -------------------------------------------------------------------------
    # Pipeline 7: Multi-Time Winners & Repeat Recipients
    # Operators: $match, $group, post-$match, $lookup, $project, $sort, $limit, $count
    # -------------------------------------------------------------------------
    print("\n--- [7/7] Pipeline 07: Multi-Time Winners ---")
    pipe07 = [
        {"$match": {"primary_artist_id": {"$exists": True, "$ne": None}}},
        {
            "$group": {
                "_id": "$primary_artist_id",
                "DERIVED_career_wins_count": {"$sum": 1},
                "DERIVED_total_statuettes": {
                    "$sum": "$trophy_statuettes_awarded_count"
                },
                "DERIVED_winning_ceremonies": {"$addToSet": "$ceremony_id"},
                "DERIVED_winning_categories": {"$addToSet": "$category_id"},
            }
        },
        {"$match": {"DERIVED_career_wins_count": {"$gt": 1}}},
        {
            "$lookup": {
                "from": "consecutive_winners",
                "localField": "_id",
                "foreignField": "artist_id",
                "as": "streak_records",
            }
        },
        {
            "$project": {
                "_id": 0,
                "artist_id": "$_id",
                "DERIVED_career_wins_count": 1,
                "DERIVED_total_statuettes": 1,
                "DERIVED_distinct_ceremonies_count": {
                    "$size": "$DERIVED_winning_ceremonies"
                },
                "DERIVED_distinct_categories_count": {
                    "$size": "$DERIVED_winning_categories"
                },
                "DERIVED_has_consecutive_streaks": {
                    "$gt": [{"$size": "$streak_records"}, 0]
                },
                "DERIVED_consecutive_streaks_count": {"$size": "$streak_records"},
                "DERIVED_calculation_status": {"$literal": "DERIVED"},
            }
        },
        {
            "$sort": {
                "DERIVED_career_wins_count": -1,
                "DERIVED_total_statuettes": -1,
            }
        },
        {"$limit": 5},
    ]
    res07 = list(db_win["winner_records"].aggregate(pipe07))
    assert len(res07) > 0, "Pipeline 07 returned zero results"
    for r in res07:
        assert r["DERIVED_career_wins_count"] > 1
        assert r["DERIVED_calculation_status"] == "DERIVED"
    print(
        f"  [PASS] Top multi-time winner: {res07[0]['artist_id']} with {res07[0]['DERIVED_career_wins_count']} career wins and {res07[0]['DERIVED_total_statuettes']} statuettes."
    )
    summary["pipeline_results"]["07_multi_time_winners"] = res07[0]
    summary["pipelines_executed"] += 1
    summary["pipelines_passed"] += 1

    # -------------------------------------------------------------------------
    # Operator Demonstration: $count
    # -------------------------------------------------------------------------
    print("\n--- Operator Demonstration: $count ---")
    pipe_count = [
        {"$match": {"primary_artist_id": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": "$primary_artist_id", "wins": {"$sum": 1}}},
        {"$match": {"wins": {"$gt": 1}}},
        {"$count": "DERIVED_total_multi_time_winners_count"},
    ]
    res_count = list(db_win["winner_records"].aggregate(pipe_count))
    assert len(res_count) == 1, "Count stage failed to return scalar result"
    total_multi_winners = res_count[0]["DERIVED_total_multi_time_winners_count"]
    print(
        f"  [PASS] $count operator verified: {total_multi_winners} total multi-time winners in dataset."
    )
    summary["operators_verified"]["$count"] = total_multi_winners

    # -------------------------------------------------------------------------
    # Supplementary Pipelines (8, 9, 10)
    # -------------------------------------------------------------------------
    print("\n--- Supplementary Pipelines (08, 09, 10) ---")

    # Pipeline 08: Speech acknowledgments ($unwind)
    pipe08 = [
        {
            "$match": {
                "individuals_acknowledged": {
                    "$exists": True,
                    "$type": "array",
                    "$ne": [],
                }
            }
        },
        {"$unwind": "$individuals_acknowledged"},
        {
            "$group": {
                "_id": "$individuals_acknowledged",
                "DERIVED_acknowledgment_frequency": {"$sum": 1},
                "DERIVED_avg_speech_duration_seconds": {
                    "$avg": "$speech_duration_seconds"
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "acknowledged_entity": "$_id",
                "DERIVED_acknowledgment_frequency": 1,
                "DERIVED_avg_duration_sec": {
                    "$round": ["$DERIVED_avg_speech_duration_seconds", 2]
                },
                "DERIVED_calculation_status": {"$literal": "DERIVED"},
            }
        },
        {"$sort": {"DERIVED_acknowledgment_frequency": -1}},
        {"$limit": 3},
    ]
    res08 = list(db_win["acceptance_speeches"].aggregate(pipe08))
    assert len(res08) > 0
    print(
        f"  [PASS] Pipeline 08 ($unwind): Top acknowledged entity is '{res08[0]['acknowledged_entity']}' ({res08[0]['DERIVED_acknowledgment_frequency']} times)."
    )
    summary["pipelines_executed"] += 1
    summary["pipelines_passed"] += 1

    # Pipeline 09: Venue hosting ($lookup, $unwind)
    pipe09 = [
        {"$match": {"venue_id": {"$exists": True, "$ne": None}}},
        {
            "$lookup": {
                "from": "venues",
                "localField": "venue_id",
                "foreignField": "venue_id",
                "as": "venue_details",
            }
        },
        {"$unwind": "$venue_details"},
        {
            "$group": {
                "_id": "$venue_details.venue_name",
                "DERIVED_ceremonies_hosted_count": {"$sum": 1},
            }
        },
        {
            "$project": {
                "_id": 0,
                "venue_name": "$_id",
                "DERIVED_ceremonies_hosted_count": 1,
                "DERIVED_calculation_status": {"$literal": "DERIVED"},
            }
        },
        {"$sort": {"DERIVED_ceremonies_hosted_count": -1}},
        {"$limit": 3},
    ]
    res09 = list(db_his["ceremonies"].aggregate(pipe09))
    assert len(res09) > 0
    print(
        f"  [PASS] Pipeline 09 ($lookup, $unwind): Top venue is '{res09[0]['venue_name']}' ({res09[0]['DERIVED_ceremonies_hosted_count']} ceremonies)."
    )
    summary["pipelines_executed"] += 1
    summary["pipelines_passed"] += 1

    # Pipeline 10: Category restructures ($unwind, $group)
    pipe10 = [
        {"$match": {"primary_category_id": {"$exists": True, "$ne": None}}},
        {"$unwind": "$source_category_ids"},
        {
            "$group": {
                "_id": "$primary_category_id",
                "DERIVED_merged_source_categories_count": {"$sum": 1},
            }
        },
        {
            "$project": {
                "_id": 0,
                "primary_category_id": "$_id",
                "DERIVED_merged_source_categories_count": 1,
                "DERIVED_calculation_status": {"$literal": "DERIVED"},
            }
        },
        {"$sort": {"DERIVED_merged_source_categories_count": -1}},
        {"$limit": 3},
    ]
    res10 = list(db_cat["merged_split_history"].aggregate(pipe10))
    assert len(res10) > 0
    print(
        f"  [PASS] Pipeline 10 ($unwind): Category restructures analyzed ({len(res10)} categories displayed)."
    )
    summary["pipelines_executed"] += 1
    summary["pipelines_passed"] += 1

    # -------------------------------------------------------------------------
    # Verify All 7 Mandatory Operators
    # -------------------------------------------------------------------------
    mandatory_operators = [
        "$match",
        "$group",
        "$sort",
        "$project",
        "$count",
        "$lookup",
        "$unwind",
    ]
    for op in mandatory_operators:
        summary["operators_verified"][op] = "VERIFIED"

    print("\n" + "=" * 66)
    print("ALL 10 AGGREGATION PIPELINES VERIFIED SUCCESSFULLY AGAINST ATLAS")
    print(f"Total pipelines executed: {summary['pipelines_executed']}")
    print(f"Total pipelines passed:   {summary['pipelines_passed']}")
    print(f"Operators verified:       {list(summary['operators_verified'].keys())}")
    print("=" * 66)

    return summary


if __name__ == "__main__":
    run_all_aggregations()
