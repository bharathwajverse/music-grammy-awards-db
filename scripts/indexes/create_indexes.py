#!/usr/bin/env python3
"""
=============================================================================
GRAMMY Awards Information & Analytics System — Index Management Script
=============================================================================
Phase: PHASE 21 — INDEXING
Module: Module 10 — Advanced Query Operators & Multikey Indexing
Author: ADBMS Architecture Team

Provides enterprise lifecycle management for all 44 custom indexes across the
five distributed MongoDB databases:
  1. grammy_history_db (Member 1: History)
  2. grammy_categories_db (Member 2: Categories)
  3. grammy_nominations_db (Member 3: Nominations)
  4. grammy_winners_db (Member 4: Winners)
  5. grammy_creators_db (Member 5: Creators/Music)

Supports commands:
  --create   (default) Creates all recommended indexes if not already present.
  --verify   Verifies that all 44 custom indexes are active on MongoDB Atlas.
  --drop     Drops only the custom-managed indexes (preserves default _id_).
  --stats    Displays index sizes and collection storage statistics.
=============================================================================
"""

import os
import sys
import argparse
import re
import certifi
import pymongo
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# MASTER INDEX SPECIFICATION CATALOG (44 Custom Indexes Across 5 Databases)
# ---------------------------------------------------------------------------
INDEX_CATALOG = {
    "grammy_history_db": {
        "ceremonies": [
            {
                "name": "idx_ceremonies_ceremony_id",
                "keys": [("ceremony_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Enforces natural key uniqueness on ceremony_id and accelerates point lookups.",
                "query": "db.ceremonies.findOne({ ceremony_id: 'CEREMONY_001' })",
                "benefit": "Replaces full collection scan with O(1)/O(log N) point seek, eliminating 66 unnecessary document reads."
            },
            {
                "name": "idx_ceremonies_broadcast_year",
                "keys": [("broadcast_year", -1)],
                "unique": False,
                "type": "Single Field",
                "reason": "Accelerates temporal range queries ($gt, $lt, $gte) and chronological sorting on broadcast years.",
                "query": "db.ceremonies.find({ broadcast_year: { $gt: 2010 } }).sort({ broadcast_year: 1 })",
                "benefit": "Enables B-tree range scan with index-ordered traversal, avoiding collection scans."
            },
            {
                "name": "idx_ceremonies_venue_id",
                "keys": [("venue_id", 1)],
                "unique": False,
                "type": "Single Field / Foreign Key",
                "reason": "Accelerates $lookup joins from ceremony records to venue collections.",
                "query": "db.ceremonies.aggregate([{ $lookup: { from: 'venues', localField: 'venue_id', foreignField: 'venue_id', as: 'v' } }])",
                "benefit": "Transforms join lookups from nested collection scans into indexed B-tree lookups."
            },
            {
                "name": "idx_ceremonies_network_year_esr",
                "keys": [("primary_network", 1), ("broadcast_year", -1)],
                "unique": False,
                "type": "Compound (ESR)",
                "reason": "Satisfies Equality on primary_network, Sort/Range on broadcast_year per ESR rule.",
                "query": "db.ceremonies.find({ primary_network: 'CBS', broadcast_year: { $gte: 2000 } }).sort({ broadcast_year: -1 })",
                "benefit": "Eliminates in-memory blocking sort and prunes scanned documents to exact network partition."
            }
        ],
        "venues": [
            {
                "name": "idx_venues_venue_id",
                "keys": [("venue_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Guarantees venue identifier uniqueness and serves as target for foreign key lookups.",
                "query": "db.venues.findOne({ venue_id: 'VEN_BEVERLY_HILTON' })",
                "benefit": "Instantaneous point lookup and enforced referential uniqueness."
            },
            {
                "name": "idx_venues_city",
                "keys": [("city", 1)],
                "unique": False,
                "type": "Single Field",
                "reason": "Accelerates geographic filtering ($eq, $in) on host cities.",
                "query": "db.venues.find({ city: { $in: ['Beverly Hills', 'Los Angeles'] } })",
                "benefit": "Direct index bounds scan matching target cities, avoiding 60-document collection scan."
            }
        ],
        "viewership_ratings": [
            {
                "name": "idx_ratings_ceremony_viewers_esr",
                "keys": [("ceremony_id", 1), ("us_viewers_millions", -1)],
                "unique": False,
                "type": "Compound (ESR)",
                "reason": "Supports ceremony-specific viewership lookups sorted by audience size.",
                "query": "db.viewership_ratings.find({ us_viewers_millions: { $gte: 20.0 } }).sort({ us_viewers_millions: -1 })",
                "benefit": "Avoids collection scan and provides pre-sorted metric retrieval."
            }
        ]
    },
    "grammy_categories_db": {
        "award_categories": [
            {
                "name": "idx_categories_category_id",
                "keys": [("category_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Enforces natural key uniqueness on category_id and supports cross-database referencing.",
                "query": "db.award_categories.findOne({ category_id: 'CAT_RECORD_OF_THE_YEAR_000' })",
                "benefit": "Direct index seek on core category dimension, eliminating 119 document reads."
            },
            {
                "name": "idx_categories_field_id",
                "keys": [("field_id", 1)],
                "unique": False,
                "type": "Single Field / Foreign Key",
                "reason": "Supports category classification lookups by field (General Field, Pop, Rock, etc.).",
                "query": "db.award_categories.find({ field_id: 'FLD_GENERAL' })",
                "benefit": "Direct index match on field partition, pruning non-matching categories instantly."
            },
            {
                "name": "idx_categories_status_nominees_esr",
                "keys": [("current_status", 1), ("maximum_nominees_allowed", -1)],
                "unique": False,
                "type": "Compound (ESR)",
                "reason": "Supports filtering active categories ordered by nominee quota capacity.",
                "query": "db.award_categories.find({ current_status: 'Active' }).sort({ maximum_nominees_allowed: -1 })",
                "benefit": "Index provides both equality filtering and sorted stream without temporary in-memory sort buffer."
            },
            {
                "name": "idx_categories_field_inaugural_esr",
                "keys": [("field_id", 1), ("inaugural_edition", 1)],
                "unique": False,
                "type": "Compound (ESR)",
                "reason": "Supports field-specific chronological queries on category origin.",
                "query": "db.award_categories.find({ field_id: { $in: ['FLD_POP', 'FLD_ROCK'] } }).sort({ inaugural_edition: 1 })",
                "benefit": "Restricts search space to specified fields with natural edition ordering."
            }
        ],
        "award_fields": [
            {
                "name": "idx_fields_field_id",
                "keys": [("field_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Enforces unique field identifiers across award taxonomy.",
                "query": "db.award_fields.findOne({ field_id: 'FLD_GENERAL' })",
                "benefit": "Guarantees taxonomy integrity and rapid point lookups."
            }
        ],
        "merged_split_history": [
            {
                "name": "idx_merged_split_source_cats_multikey",
                "keys": [("source_category_ids", 1)],
                "unique": False,
                "type": "Multikey (Array)",
                "reason": "Indexes array of source category IDs to accelerate $all, element containment, and $size queries.",
                "query": "db.merged_split_history.find({ source_category_ids: 'LEGACY_CAT_MALE_0' })",
                "benefit": "Enables multikey B-tree index traversal over array elements without document unfolding."
            },
            {
                "name": "idx_merged_split_primary_cat",
                "keys": [("primary_category_id", 1)],
                "unique": False,
                "type": "Single Field / Foreign Key",
                "reason": "Accelerates joins and lookups linking restructurings to target categories.",
                "query": "db.merged_split_history.find({ primary_category_id: 'CAT_RECORD_OF_THE_YEAR_000' })",
                "benefit": "Fast index lookup for category restructuring lineage."
            }
        ]
    },
    "grammy_nominations_db": {
        "nomination_entries": [
            {
                "name": "idx_nom_entries_nomination_id",
                "keys": [("nomination_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Guarantees uniqueness of nomination_id and accelerates point lookups.",
                "query": "db.nomination_entries.findOne({ nomination_id: 'NOM_001_RECORD_OF__0000' })",
                "benefit": "Guaranteed uniqueness and O(1) retrieval of nomination records, pruning 499 docs."
            },
            {
                "name": "idx_nom_entries_artist_id",
                "keys": [("primary_artist_id", 1)],
                "unique": False,
                "type": "Single Field / Analytical",
                "reason": "Supports high-frequency analytical queries calculating career nominations per artist (Pipeline 01 & 06).",
                "query": "db.nomination_entries.find({ primary_artist_id: 'CRT_HENRY_MANCINI_0001' })",
                "benefit": "Enables instant artist nomination filtering without scanning all 500 documents."
            },
            {
                "name": "idx_nom_entries_work_id",
                "keys": [("work_id", 1)],
                "unique": False,
                "type": "Single Field / Foreign Key",
                "reason": "Supports $lookup joins to nominated_works and work-specific nomination queries.",
                "query": "db.nomination_entries.aggregate([{ $lookup: { from: 'nominated_works', localField: 'work_id', foreignField: 'work_id', as: 'w' } }])",
                "benefit": "Drastically accelerates join stage by enabling index lookups on work reference."
            },
            {
                "name": "idx_nom_entries_category_year_esr",
                "keys": [("category_id", 1), ("nomination_year", -1)],
                "unique": False,
                "type": "Compound (ESR)",
                "reason": "Supports category-based filtering combined with chronological annual ordering (Pipeline 04 & 05).",
                "query": "db.nomination_entries.find({ category_id: 'CAT_RECORD_OF_THE_YEAR_000' }).sort({ nomination_year: -1 })",
                "benefit": "Index satisfies category equality and outputs sorted stream by year."
            },
            {
                "name": "idx_nom_entries_winner_year_slot_esr",
                "keys": [("is_winner_flag", 1), ("nomination_year", -1), ("ballot_slot_order", 1)],
                "unique": False,
                "type": "Compound (ESR)",
                "reason": "Supports compound queries filtering winners over year ranges with ballot slot ordering.",
                "query": "db.nomination_entries.find({ is_winner_flag: true, nomination_year: { $gte: 1959, $lte: 1965 } }).sort({ nomination_year: 1 })",
                "benefit": "Perfect ESR alignment: Equality on winner flag, Range/Sort on year, Sort on ballot slot."
            }
        ],
        "nominated_works": [
            {
                "name": "idx_nominated_works_work_id",
                "keys": [("work_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Enforces unique work_id and serves as target for $lookup joins from nomination_entries.",
                "query": "db.nominated_works.findOne({ work_id: 'WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000' })",
                "benefit": "High-speed indexed join target for Pipeline 01, eliminating 499 document inspections."
            },
            {
                "name": "idx_nominated_works_primary_label",
                "keys": [("primary_label_id", 1)],
                "unique": False,
                "type": "Single Field / Foreign Key",
                "reason": "Supports queries filtering works by record label.",
                "query": "db.nominated_works.find({ primary_label_id: 'LBL_WARNER_RECORDS_001' })",
                "benefit": "Index scan on label catalog without table scan."
            }
        ],
        "tied_nominations": [
            {
                "name": "idx_tied_noms_tied_ids_multikey",
                "keys": [("tied_nomination_ids", 1)],
                "unique": False,
                "type": "Multikey (Array)",
                "reason": "Indexes array of tied nomination IDs for containment and $all queries.",
                "query": "db.tied_nominations.find({ tied_nomination_ids: 'NOM_001_RECORD_OF__0000' })",
                "benefit": "Multikey B-tree index lookup directly on array values, pruning collection scan."
            },
            {
                "name": "idx_tied_noms_ceremony_category",
                "keys": [("ceremony_id", 1), ("category_id", 1)],
                "unique": False,
                "type": "Compound",
                "reason": "Supports finding ties within a specific ceremony and category.",
                "query": "db.tied_nominations.find({ ceremony_id: 'CEREMONY_001', category_id: 'CAT_RECORD_OF_THE_YEAR_000' })",
                "benefit": "Immediate narrow index seek on ceremony/category pair."
            }
        ],
        "genre_classifications": [
            {
                "name": "idx_genre_class_secondary_tags_multikey",
                "keys": [("secondary_genre_tags", 1)],
                "unique": False,
                "type": "Multikey (Array)",
                "reason": "Indexes array of genre tags to accelerate element matching and genre analytics.",
                "query": "db.genre_classifications.find({ secondary_genre_tags: 'Adult Contemporary' })",
                "benefit": "Multikey index traversal over secondary genre tags."
            },
            {
                "name": "idx_genre_class_work_id",
                "keys": [("work_id", 1)],
                "unique": False,
                "type": "Single Field / Foreign Key",
                "reason": "Links genre classifications to specific works.",
                "query": "db.genre_classifications.find({ work_id: 'WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000' })",
                "benefit": "Fast foreign key lookup on work identifier."
            }
        ],
        "multi_nomination_packages": [
            {
                "name": "idx_packages_nominated_works_multikey",
                "keys": [("nominated_work_ids", 1)],
                "unique": False,
                "type": "Multikey (Array)",
                "reason": "Indexes array of works bundled within multi-nomination packages.",
                "query": "db.multi_nomination_packages.find({ nominated_work_ids: 'WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000' })",
                "benefit": "Direct array index lookup for bundled packages."
            },
            {
                "name": "idx_packages_creator_ceremony",
                "keys": [("creator_id", 1), ("ceremony_year", -1)],
                "unique": False,
                "type": "Compound (ESR)",
                "reason": "Supports finding multi-nomination packages for a creator across ceremony years.",
                "query": "db.multi_nomination_packages.find({ creator_id: 'CRT_HENRY_MANCINI_0001' }).sort({ ceremony_year: -1 })",
                "benefit": "Exact creator filtering with sorted yearly history."
            }
        ]
    },
    "grammy_winners_db": {
        "winner_records": [
            {
                "name": "idx_winner_records_winner_id",
                "keys": [("winner_record_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Enforces uniqueness of winner_record_id and accelerates point lookups.",
                "query": "db.winner_records.findOne({ winner_record_id: 'WIN_NOM_001_RECORD_OF__0000' })",
                "benefit": "Ensures winner record integrity and enables instant point retrieval, pruning 399 docs."
            },
            {
                "name": "idx_winner_records_artist_id",
                "keys": [("primary_artist_id", 1)],
                "unique": False,
                "type": "Single Field / Analytical",
                "reason": "Supports high-frequency queries calculating career wins per artist (Pipeline 02 & 07).",
                "query": "db.winner_records.find({ primary_artist_id: 'CRT_HENRY_MANCINI_0001' })",
                "benefit": "Reduces scanned documents from 400 to exact artist wins."
            },
            {
                "name": "idx_winner_records_category_year_esr",
                "keys": [("category_id", 1), ("ceremony_year", -1)],
                "unique": False,
                "type": "Compound (ESR)",
                "reason": "Supports historical winner queries per category ordered chronologically (Pipeline 03).",
                "query": "db.winner_records.find({ category_id: 'CAT_SONG_OF_THE_YEAR_002' }).sort({ ceremony_year: -1 })",
                "benefit": "Index covers category filtering and sorts result stream naturally."
            },
            {
                "name": "idx_winner_records_telecast_statuettes_esr",
                "keys": [("presented_live_on_telecast", 1), ("trophy_statuettes_awarded_count", -1)],
                "unique": False,
                "type": "Compound (ESR)",
                "reason": "Supports queries filtering live telecast presentations sorted by statuette counts.",
                "query": "db.winner_records.find({ presented_live_on_telecast: true }).sort({ trophy_statuettes_awarded_count: -1 })",
                "benefit": "Avoids in-memory sort and scans only live telecast index entries."
            }
        ],
        "acceptance_speeches": [
            {
                "name": "idx_speeches_speech_id",
                "keys": [("speech_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Guarantees speech_id uniqueness.",
                "query": "db.acceptance_speeches.findOne({ speech_id: 'SPEECH_001' })",
                "benefit": "Instant speech point lookup."
            },
            {
                "name": "idx_speeches_winner_record_id",
                "keys": [("winner_record_id", 1)],
                "unique": False,
                "type": "Single Field / Foreign Key",
                "reason": "Supports $lookup join from winner_records to acceptance_speeches in Pipeline 02.",
                "query": "db.winner_records.aggregate([{ $lookup: { from: 'acceptance_speeches', localField: 'winner_record_id', foreignField: 'winner_record_id', as: 's' } }])",
                "benefit": "Powers high-performance relational joins without collection scans."
            },
            {
                "name": "idx_speeches_ack_multikey",
                "keys": [("individuals_acknowledged", 1)],
                "unique": False,
                "type": "Multikey (Array)",
                "reason": "Indexes array of acknowledged entities for containment, $all, and $unwind analytics (Pipeline 08).",
                "query": "db.acceptance_speeches.find({ individuals_acknowledged: 'Family' })",
                "benefit": "Multikey index scan for acknowledged parties across speeches, avoiding table scan."
            }
        ],
        "consecutive_winners": [
            {
                "name": "idx_consecutive_creator_id",
                "keys": [("creator_id", 1)],
                "unique": False,
                "type": "Single Field / Foreign Key",
                "reason": "Supports joining consecutive winning streaks to creators in Pipeline 07.",
                "query": "db.consecutive_winners.find({ creator_id: 'CRT_HENRY_MANCINI_0001' })",
                "benefit": "Direct index match on creator winning streak records."
            },
            {
                "name": "idx_consecutive_winning_works_multikey",
                "keys": [("winning_work_ids_list", 1)],
                "unique": False,
                "type": "Multikey (Array)",
                "reason": "Indexes array of works constituting consecutive winning streaks.",
                "query": "db.consecutive_winners.find({ winning_work_ids_list: 'WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000' })",
                "benefit": "Multikey index scan for works participating in streaks."
            }
        ]
    },
    "grammy_creators_db": {
        "artists": [
            {
                "name": "idx_artists_artist_id",
                "keys": [("artist_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Enforces uniqueness of universal artist_id and supports cross-database lookups.",
                "query": "db.artists.findOne({ artist_id: 'CRT_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000' })",
                "benefit": "Guarantees artist entity integrity and enables O(1) point lookups, pruning 299 docs."
            },
            {
                "name": "idx_artists_stage_name",
                "keys": [("stage_name", 1)],
                "unique": False,
                "type": "Single Field",
                "reason": "Supports artist lookups and alphabetical sorting by stage name.",
                "query": "db.artists.find({ stage_name: 'Henry Mancini' }).sort({ stage_name: 1 })",
                "benefit": "B-tree index scan on artist billing title."
            },
            {
                "name": "idx_artists_group_career_esr",
                "keys": [("is_group_ensemble_flag", 1), ("active_career_start_year", 1)],
                "unique": False,
                "type": "Compound (ESR)",
                "reason": "Supports filtering solo artists or ensembles ordered chronologically by career start.",
                "query": "db.artists.find({ is_group_ensemble_flag: false, active_career_start_year: { $gte: 1950 } }).sort({ active_career_start_year: 1 })",
                "benefit": "Satisfies Equality on group flag and Range/Sort on career start year without in-memory sort."
            }
        ],
        "songwriters_composers": [
            {
                "name": "idx_songwriters_songwriter_id",
                "keys": [("songwriter_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Enforces uniqueness on songwriter_id.",
                "query": "db.songwriters_composers.findOne({ songwriter_id: 'SONG_001' })",
                "benefit": "Direct indexed point lookup for songwriter entities."
            },
            {
                "name": "idx_songwriters_pro_works_esr",
                "keys": [("pro_affiliation", 1), ("registered_works_count", -1)],
                "unique": False,
                "type": "Compound (ESR)",
                "reason": "Supports queries filtering PRO affiliations (ASCAP, BMI) sorted by catalog size.",
                "query": "db.songwriters_composers.find({ pro_affiliation: { $in: ['ASCAP', 'BMI'] } }).sort({ registered_works_count: -1 })",
                "benefit": "Index accelerates set equality and supplies pre-sorted works count ordering."
            }
        ],
        "musical_groups": [
            {
                "name": "idx_musical_groups_group_id",
                "keys": [("group_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Enforces uniqueness on group_id.",
                "query": "db.musical_groups.findOne({ group_id: 'GRP_001' })",
                "benefit": "Direct indexed point lookup."
            },
            {
                "name": "idx_musical_groups_formation_year",
                "keys": [("formation_calendar_year", 1)],
                "unique": False,
                "type": "Single Field",
                "reason": "Supports chronological queries on group formation dates.",
                "query": "db.musical_groups.find({ formation_calendar_year: { $lte: 1965 } })",
                "benefit": "B-tree index range scan on formation year."
            }
        ],
        "record_labels": [
            {
                "name": "idx_record_labels_label_id",
                "keys": [("label_id", 1)],
                "unique": True,
                "type": "Single Field / Unique Secondary",
                "reason": "Enforces uniqueness on label_id.",
                "query": "db.record_labels.findOne({ label_id: 'LBL_WARNER_RECORDS_001' })",
                "benefit": "Direct indexed point lookup on record labels."
            }
        ]
    }
}


def mask_uri(uri: str) -> str:
    """Masks credentials in MongoDB URI for safe logging."""
    if not uri:
        return "<EMPTY>"
    return re.sub(r":([^@]+)@", ":****@", uri)


def get_mongo_client() -> pymongo.MongoClient:
    """Instantiates authenticated MongoDB client with TLS verification."""
    load_dotenv(REPO_ROOT / ".env")
    uri = os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_URI not found in .env file!")
    print(f">> Connecting to MongoDB Atlas: {mask_uri(uri)}")
    client = pymongo.MongoClient(
        uri,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
    )
    client.admin.command("ping")
    print(">> [SUCCESS] Authenticated with Atlas cluster.")
    return client


def create_indexes(client: pymongo.MongoClient):
    """Creates all 44 recommended indexes."""
    print("\n=======================================================")
    print("DEPLOYING 44 RECOMMENDED INDEXES TO ATLAS")
    print("=======================================================")
    created = 0
    already_present = 0

    for db_name, collections in INDEX_CATALOG.items():
        db = client[db_name]
        print(f"\n--- Database: {db_name} ---")
        for coll_name, index_list in collections.items():
            coll = db[coll_name]
            existing_names = {idx["name"] for idx in coll.list_indexes()}

            for idx_def in index_list:
                name = idx_def["name"]
                keys = idx_def["keys"]
                unique = idx_def.get("unique", False)

                if name in existing_names:
                    print(f"  [EXISTS] {coll_name}.{name}")
                    already_present += 1
                else:
                    print(f"  [CREATE] {coll_name}.{name} {dict(keys)} (unique={unique})...")
                    res = coll.create_index(keys, name=name, unique=unique)
                    print(f"    -> Created: {res}")
                    created += 1

    print("\n-------------------------------------------------------")
    print(f"Total Indexes Verified/Created: {created + already_present}")
    print(f"  - Newly Created: {created}")
    print(f"  - Already Active: {already_present}")
    print("-------------------------------------------------------")


def verify_indexes(client: pymongo.MongoClient) -> bool:
    """Verifies that all 44 custom indexes are present and active on Atlas."""
    print("\n=======================================================")
    print("VERIFYING ACTIVE INDEXES ON MONGODB ATLAS")
    print("=======================================================")
    missing = []
    total_expected = 0

    for db_name, collections in INDEX_CATALOG.items():
        db = client[db_name]
        print(f"\n--- Checking Database: {db_name} ---")
        for coll_name, index_list in collections.items():
            coll = db[coll_name]
            existing = {idx["name"]: idx for idx in coll.list_indexes()}

            for idx_def in index_list:
                total_expected += 1
                name = idx_def["name"]
                if name not in existing:
                    print(f"  [MISSING] {coll_name}.{name}")
                    missing.append((db_name, coll_name, name))
                else:
                    idx = existing[name]
                    key_dict = dict(idx["key"])
                    unique = idx.get("unique", False)
                    print(f"  [VERIFIED] {coll_name}.{name} | Key: {key_dict} | Unique: {unique}")

    print("\n-------------------------------------------------------")
    if not missing:
        print(f"ALL {total_expected} RECOMMENDED INDEXES SUCCESSFULLY VERIFIED!")
        return True
    else:
        print(f"VERIFICATION FAILED: {len(missing)} indexes missing!")
        return False


def drop_custom_indexes(client: pymongo.MongoClient):
    """Drops only the custom-managed indexes (preserves default _id_)."""
    print("\n=======================================================")
    print("DROPPING CUSTOM-MANAGED INDEXES (PRESERVING _id_)")
    print("=======================================================")
    dropped = 0

    for db_name, collections in INDEX_CATALOG.items():
        db = client[db_name]
        print(f"\n--- Database: {db_name} ---")
        for coll_name, index_list in collections.items():
            coll = db[coll_name]
            existing_names = {idx["name"] for idx in coll.list_indexes()}

            for idx_def in index_list:
                name = idx_def["name"]
                if name in existing_names:
                    print(f"  [DROP] Dropping {coll_name}.{name}...")
                    coll.drop_index(name)
                    dropped += 1

    print(f"\n>> Dropped {dropped} custom indexes.")


def display_stats(client: pymongo.MongoClient):
    """Displays index sizes and collection storage statistics."""
    print("\n=======================================================")
    print("INDEX STORAGE STATISTICS (WIREDTIGER STORAGE ENGINE)")
    print("=======================================================")

    for db_name, collections in INDEX_CATALOG.items():
        db = client[db_name]
        print(f"\nDatabase: {db_name}")
        for coll_name in collections.keys():
            coll = db[coll_name]
            stats = db.command("collStats", coll_name)
            count = stats.get("count", 0)
            size_kb = stats.get("size", 0) / 1024
            idx_size_kb = stats.get("totalIndexSize", 0) / 1024
            n_indexes = stats.get("nindexes", 0)
            print(f"  {coll_name:<26} | Docs: {count:4d} | Data: {size_kb:6.2f} KB | Indexes: {n_indexes} ({idx_size_kb:6.2f} KB)")


def main():
    parser = argparse.ArgumentParser(description="MongoDB Atlas Index Management CLI")
    parser.add_argument("--create", action="store_true", default=True, help="Create all indexes (default)")
    parser.add_argument("--verify", action="store_true", help="Verify all indexes are present on Atlas")
    parser.add_argument("--drop", action="store_true", help="Drop custom-managed indexes")
    parser.add_argument("--stats", action="store_true", help="Display index storage statistics")

    args = parser.parse_args()
    client = get_mongo_client()

    if args.drop:
        drop_custom_indexes(client)
    elif args.verify:
        success = verify_indexes(client)
        sys.exit(0 if success else 1)
    elif args.stats:
        display_stats(client)
    else:
        create_indexes(client)
        verify_indexes(client)


if __name__ == "__main__":
    main()
