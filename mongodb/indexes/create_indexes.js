// ==============================================================================
// GRAMMY Awards Information & Analytics System — Native mongosh Index Creation
// ==============================================================================
// Phase: PHASE 21 — INDEXING
// Module: Module 10 — Advanced Query Operators & Multikey Indexing
// Author: ADBMS Architecture Team
//
// Target Databases:
//   1. grammy_history_db (Member 1: History)
//   2. grammy_categories_db (Member 2: Categories)
//   3. grammy_nominations_db (Member 3: Nominations)
//   4. grammy_winners_db (Member 4: Winners)
//   5. grammy_creators_db (Member 5: Creators/Music)
//
// Demonstrates:
//   - Single Field Indexes
//   - Compound Indexes with ESR Rule (Equality, Sort, Range)
//   - Multikey Indexes on BSON Array Fields
//   - Unique Secondary Indexes for Business Natural Keys
// ==============================================================================

print("==================================================================");
print("PHASE 21: MONGODB INDEX IMPLEMENTATION SUITE");
print("==================================================================");

// ==============================================================================
// 1. DATABASE: grammy_history_db (Member 1: History)
// ==============================================================================
var histDB = db.getSiblingDB("grammy_history_db");
print("\n>>> [1/5] Deploying Indexes to grammy_history_db <<<");

// Collection: ceremonies
print("  Deploying indexes on 'ceremonies'...");
histDB.ceremonies.createIndex(
  { ceremony_id: 1 },
  { name: "idx_ceremonies_ceremony_id", unique: true }
);

histDB.ceremonies.createIndex(
  { broadcast_year: -1 },
  { name: "idx_ceremonies_broadcast_year" }
);

histDB.ceremonies.createIndex(
  { venue_id: 1 },
  { name: "idx_ceremonies_venue_id" }
);

histDB.ceremonies.createIndex(
  { primary_network: 1, broadcast_year: -1 },
  { name: "idx_ceremonies_network_year_esr" }
);

// Collection: venues
print("  Deploying indexes on 'venues'...");
histDB.venues.createIndex(
  { venue_id: 1 },
  { name: "idx_venues_venue_id", unique: true }
);

histDB.venues.createIndex(
  { city: 1 },
  { name: "idx_venues_city" }
);

// Collection: viewership_ratings
print("  Deploying indexes on 'viewership_ratings'...");
histDB.viewership_ratings.createIndex(
  { ceremony_id: 1, us_viewers_millions: -1 },
  { name: "idx_ratings_ceremony_viewers_esr" }
);

// ==============================================================================
// 2. DATABASE: grammy_categories_db (Member 2: Categories)
// ==============================================================================
var catDB = db.getSiblingDB("grammy_categories_db");
print("\n>>> [2/5] Deploying Indexes to grammy_categories_db <<<");

// Collection: award_categories
print("  Deploying indexes on 'award_categories'...");
catDB.award_categories.createIndex(
  { category_id: 1 },
  { name: "idx_categories_category_id", unique: true }
);

catDB.award_categories.createIndex(
  { field_id: 1 },
  { name: "idx_categories_field_id" }
);

catDB.award_categories.createIndex(
  { current_status: 1, maximum_nominees_allowed: -1 },
  { name: "idx_categories_status_nominees_esr" }
);

catDB.award_categories.createIndex(
  { field_id: 1, inaugural_edition: 1 },
  { name: "idx_categories_field_inaugural_esr" }
);

// Collection: award_fields
print("  Deploying indexes on 'award_fields'...");
catDB.award_fields.createIndex(
  { field_id: 1 },
  { name: "idx_fields_field_id", unique: true }
);

// Collection: merged_split_history
print("  Deploying indexes on 'merged_split_history'...");
catDB.merged_split_history.createIndex(
  { source_category_ids: 1 },
  { name: "idx_merged_split_source_cats_multikey" }
);

catDB.merged_split_history.createIndex(
  { primary_category_id: 1 },
  { name: "idx_merged_split_primary_cat" }
);

// ==============================================================================
// 3. DATABASE: grammy_nominations_db (Member 3: Nominations)
// ==============================================================================
var nomDB = db.getSiblingDB("grammy_nominations_db");
print("\n>>> [3/5] Deploying Indexes to grammy_nominations_db <<<");

// Collection: nomination_entries
print("  Deploying indexes on 'nomination_entries'...");
nomDB.nomination_entries.createIndex(
  { nomination_id: 1 },
  { name: "idx_nom_entries_nomination_id", unique: true }
);

nomDB.nomination_entries.createIndex(
  { primary_artist_id: 1 },
  { name: "idx_nom_entries_artist_id" }
);

nomDB.nomination_entries.createIndex(
  { work_id: 1 },
  { name: "idx_nom_entries_work_id" }
);

nomDB.nomination_entries.createIndex(
  { category_id: 1, nomination_year: -1 },
  { name: "idx_nom_entries_category_year_esr" }
);

nomDB.nomination_entries.createIndex(
  { is_winner_flag: 1, nomination_year: -1, ballot_slot_order: 1 },
  { name: "idx_nom_entries_winner_year_slot_esr" }
);

// Collection: nominated_works
print("  Deploying indexes on 'nominated_works'...");
nomDB.nominated_works.createIndex(
  { work_id: 1 },
  { name: "idx_nominated_works_work_id", unique: true }
);

nomDB.nominated_works.createIndex(
  { primary_label_id: 1 },
  { name: "idx_nominated_works_primary_label" }
);

// Collection: tied_nominations
print("  Deploying indexes on 'tied_nominations'...");
nomDB.tied_nominations.createIndex(
  { tied_nomination_ids: 1 },
  { name: "idx_tied_noms_tied_ids_multikey" }
);

nomDB.tied_nominations.createIndex(
  { ceremony_id: 1, category_id: 1 },
  { name: "idx_tied_noms_ceremony_category" }
);

// Collection: genre_classifications
print("  Deploying indexes on 'genre_classifications'...");
nomDB.genre_classifications.createIndex(
  { secondary_genre_tags: 1 },
  { name: "idx_genre_class_secondary_tags_multikey" }
);

nomDB.genre_classifications.createIndex(
  { work_id: 1 },
  { name: "idx_genre_class_work_id" }
);

// Collection: multi_nomination_packages
print("  Deploying indexes on 'multi_nomination_packages'...");
nomDB.multi_nomination_packages.createIndex(
  { nominated_work_ids: 1 },
  { name: "idx_packages_nominated_works_multikey" }
);

nomDB.multi_nomination_packages.createIndex(
  { creator_id: 1, ceremony_year: -1 },
  { name: "idx_packages_creator_ceremony" }
);

// ==============================================================================
// 4. DATABASE: grammy_winners_db (Member 4: Winners)
// ==============================================================================
var winDB = db.getSiblingDB("grammy_winners_db");
print("\n>>> [4/5] Deploying Indexes to grammy_winners_db <<<");

// Collection: winner_records
print("  Deploying indexes on 'winner_records'...");
winDB.winner_records.createIndex(
  { winner_record_id: 1 },
  { name: "idx_winner_records_winner_id", unique: true }
);

winDB.winner_records.createIndex(
  { primary_artist_id: 1 },
  { name: "idx_winner_records_artist_id" }
);

winDB.winner_records.createIndex(
  { category_id: 1, ceremony_year: -1 },
  { name: "idx_winner_records_category_year_esr" }
);

winDB.winner_records.createIndex(
  { presented_live_on_telecast: 1, trophy_statuettes_awarded_count: -1 },
  { name: "idx_winner_records_telecast_statuettes_esr" }
);

// Collection: acceptance_speeches
print("  Deploying indexes on 'acceptance_speeches'...");
winDB.acceptance_speeches.createIndex(
  { speech_id: 1 },
  { name: "idx_speeches_speech_id", unique: true }
);

winDB.acceptance_speeches.createIndex(
  { winner_record_id: 1 },
  { name: "idx_speeches_winner_record_id" }
);

winDB.acceptance_speeches.createIndex(
  { individuals_acknowledged: 1 },
  { name: "idx_speeches_ack_multikey" }
);

// Collection: consecutive_winners
print("  Deploying indexes on 'consecutive_winners'...");
winDB.consecutive_winners.createIndex(
  { creator_id: 1 },
  { name: "idx_consecutive_creator_id" }
);

winDB.consecutive_winners.createIndex(
  { winning_work_ids_list: 1 },
  { name: "idx_consecutive_winning_works_multikey" }
);

// ==============================================================================
// 5. DATABASE: grammy_creators_db (Member 5: Creators/Music)
// ==============================================================================
var crtDB = db.getSiblingDB("grammy_creators_db");
print("\n>>> [5/5] Deploying Indexes to grammy_creators_db <<<");

// Collection: artists
print("  Deploying indexes on 'artists'...");
crtDB.artists.createIndex(
  { artist_id: 1 },
  { name: "idx_artists_artist_id", unique: true }
);

crtDB.artists.createIndex(
  { stage_name: 1 },
  { name: "idx_artists_stage_name" }
);

crtDB.artists.createIndex(
  { is_group_ensemble_flag: 1, active_career_start_year: 1 },
  { name: "idx_artists_group_career_esr" }
);

// Collection: songwriters_composers
print("  Deploying indexes on 'songwriters_composers'...");
crtDB.songwriters_composers.createIndex(
  { songwriter_id: 1 },
  { name: "idx_songwriters_songwriter_id", unique: true }
);

crtDB.songwriters_composers.createIndex(
  { pro_affiliation: 1, registered_works_count: -1 },
  { name: "idx_songwriters_pro_works_esr" }
);

// Collection: musical_groups
print("  Deploying indexes on 'musical_groups'...");
crtDB.musical_groups.createIndex(
  { group_id: 1 },
  { name: "idx_musical_groups_group_id", unique: true }
);

crtDB.musical_groups.createIndex(
  { formation_calendar_year: 1 },
  { name: "idx_musical_groups_formation_year" }
);

// Collection: record_labels
print("  Deploying indexes on 'record_labels'...");
crtDB.record_labels.createIndex(
  { label_id: 1 },
  { name: "idx_record_labels_label_id", unique: true }
);

print("\n==================================================================");
print("ALL 44 INDEXES SUCCESSFULLY CREATED ACROSS 5 DATABASES");
print("==================================================================");
