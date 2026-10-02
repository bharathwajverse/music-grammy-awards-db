// ==============================================================================
// MASTER ADVANCED MONGODB QUERIES DEMONSTRATION SUITE
// Course: Advanced Database Management Systems (ADBMS) — Module 10
// Phase 19: Advanced MongoDB Queries & Complex Operators
// ==============================================================================
// Covers all 17 mandatory query operators and clauses across all 5 databases:
// 1. Comparison: $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin
// 2. Logical: $and, $or, $not
// 3. Cursor Clauses: sort, limit, skip, projection
// 4. Arrays: Containment, $all, $size, $elemMatch, Positional Index (.0)
// 5. Embedded Documents: Dot-Notation on Subdocuments (_source_provenance)
// ==============================================================================

print("==================================================================");
print("PHASE 19: MASTER ADVANCED QUERIES DEMONSTRATION SUITE");
print("==================================================================");

// ==============================================================================
// 1. DATABASE: grammy_history_db (Member 1: History)
// ==============================================================================
var histDB = db.getSiblingDB("grammy_history_db");
print("\n>>> [1/5] grammy_history_db Demonstrations <<<");

// Operator: $eq
print("\n[1.1] $eq — Match ceremonies broadcast on CBS");
histDB.ceremonies.find(
  { primary_network: { $eq: "CBS" } },
  { _id: 0, ceremony_id: 1, broadcast_year: 1, primary_network: 1 }
).sort({ broadcast_year: -1 }).limit(3).forEach(printjson);

// Operator: $ne
print("\n[1.2] $ne — Venues situated outside Los Angeles");
histDB.venues.find(
  { city: { $ne: "Los Angeles" } },
  { _id: 0, venue_id: 1, venue_name: 1, city: 1, max_seating_capacity: 1 }
).sort({ max_seating_capacity: -1 }).limit(3).forEach(printjson);

// Operator: $gt
print("\n[1.3] $gt — Ceremonies broadcast after 2010");
histDB.ceremonies.find(
  { broadcast_year: { $gt: 2010 } },
  { _id: 0, ceremony_id: 1, broadcast_year: 1, host_city: 1 }
).sort({ broadcast_year: 1 }).limit(3).forEach(printjson);

// Operator: $gte
print("\n[1.4] $gte — Telecasts with >= 20.0 million US viewers");
histDB.viewership_ratings.find(
  { us_viewers_millions: { $gte: 20.0 } },
  { _id: 0, rating_id: 1, us_viewers_millions: 1, ceremony_id: 1 }
).sort({ us_viewers_millions: -1 }).limit(3).forEach(printjson);

// Operator: $lt
print("\n[1.5] $lt — Foundational telecasts broadcast prior to 1970");
histDB.ceremonies.find(
  { broadcast_year: { $lt: 1970 } },
  { _id: 0, ceremony_id: 1, edition_number: 1, broadcast_year: 1 }
).sort({ edition_number: 1 }).limit(3).forEach(printjson);

// Operator: $lte
print("\n[1.6] $lte — First decade of Grammy editions (<= 10)");
histDB.ceremonies.find(
  { edition_number: { $lte: 10 } },
  { _id: 0, ceremony_id: 1, edition_number: 1, broadcast_year: 1 }
).sort({ edition_number: 1 }).limit(3).forEach(printjson);

// Operator: $in
print("\n[1.7] $in — Venues in Beverly Hills or Los Angeles");
histDB.venues.find(
  { city: { $in: ["Beverly Hills", "Los Angeles"] } },
  { _id: 0, venue_id: 1, venue_name: 1, city: 1 }
).limit(3).forEach(printjson);

// Operator: $nin
print("\n[1.8] $nin — Ceremonies on networks other than commercial syndicates");
histDB.ceremonies.find(
  { primary_network: { $nin: ["ABC", "FOX"] } },
  { _id: 0, ceremony_id: 1, broadcast_year: 1, primary_network: 1 }
).limit(3).forEach(printjson);

// Operator: $and
print("\n[1.9] $and — Modern CBS telecasts presenting >80 awards");
histDB.ceremonies.find(
  {
    $and: [
      { broadcast_year: { $gte: 2000 } },
      { primary_network: { $eq: "CBS" } },
      { total_awards_presented: { $gt: 80 } }
    ]
  },
  { _id: 0, ceremony_id: 1, broadcast_year: 1, primary_network: 1, total_awards_presented: 1 }
).limit(3).forEach(printjson);

// Operator: $or
print("\n[1.10] $or — Venues with capacity >= 10,000 OR in Beverly Hills");
histDB.venues.find(
  {
    $or: [
      { max_seating_capacity: { $gte: 10000 } },
      { city: { $eq: "Beverly Hills" } }
    ]
  },
  { _id: 0, venue_name: 1, city: 1, max_seating_capacity: 1 }
).limit(3).forEach(printjson);

// Operator: $not
print("\n[1.11] $not — Ceremonies where total awards is NOT < 50");
histDB.ceremonies.find(
  { total_awards_presented: { $not: { $lt: 50 } } },
  { _id: 0, ceremony_id: 1, edition_number: 1, total_awards_presented: 1 }
).limit(3).forEach(printjson);

// Clauses: sort, limit, skip, projection
print("\n[1.12] sort, limit, skip, projection — Deterministic Pagination");
histDB.ceremonies.find(
  { broadcast_year: { $gte: 1990 } },
  { _id: 0, ceremony_id: 1, edition_number: 1, broadcast_year: 1, host_city: 1 }
)
.sort({ broadcast_year: -1 })
.skip(5)
.limit(5)
.forEach(printjson);

// Embedded Documents: Dot Notation
print("\n[1.13] embedded documents — Traversal into _source_provenance");
histDB.ceremonies.find(
  {
    "_source_provenance.source_id": { $eq: "SRC-01" },
    "_source_provenance.provenance_tier": { $eq: "PRIMARY OFFICIAL SOURCE" }
  },
  { _id: 0, ceremony_id: 1, edition_number: 1, "_source_provenance.source_name": 1 }
).limit(2).forEach(printjson);

// ==============================================================================
// 2. DATABASE: grammy_categories_db (Member 2: Categories)
// ==============================================================================
var catDB = db.getSiblingDB("grammy_categories_db");
print("\n>>> [2/5] grammy_categories_db Demonstrations <<<");

// Arrays: Element Containment
print("\n[2.1] arrays (Containment) — source_category_ids contains 'LEGACY_CAT_MALE_0'");
catDB.merged_split_history.find(
  { source_category_ids: "LEGACY_CAT_MALE_0" },
  { _id: 0, event_id: 1, restructuring_type: 1, source_category_ids: 1 }
).limit(2).forEach(printjson);

// Arrays: $all
print("\n[2.2] arrays ($all) — source_category_ids contains BOTH male & female legacy IDs");
catDB.merged_split_history.find(
  { source_category_ids: { $all: ["LEGACY_CAT_MALE_0", "LEGACY_CAT_FEMALE_0"] } },
  { _id: 0, event_id: 1, primary_category_id: 1, source_category_ids: 1 }
).limit(2).forEach(printjson);

// Arrays: $size
print("\n[2.3] arrays ($size) — source_category_ids with exact length 2");
catDB.merged_split_history.find(
  { source_category_ids: { $size: 2 } },
  { _id: 0, event_id: 1, source_category_ids: 1 }
).limit(2).forEach(printjson);

// Arrays: Positional Index (.0)
print("\n[2.4] arrays (Index .0) — First element matches 'LEGACY_CAT_MALE_0'");
catDB.merged_split_history.find(
  { "source_category_ids.0": "LEGACY_CAT_MALE_0" },
  { _id: 0, event_id: 1, "source_category_ids.0": 1 }
).limit(2).forEach(printjson);

// ==============================================================================
// 3. DATABASE: grammy_nominations_db (Member 3: Nominations)
// ==============================================================================
var nomDB = db.getSiblingDB("grammy_nominations_db");
print("\n>>> [3/5] grammy_nominations_db Demonstrations <<<");

// Arrays: Containment on tied_nomination_ids
print("\n[3.1] arrays (Containment) — tied_nomination_ids contains 'NOM_001_RECORD_OF__0000'");
nomDB.tied_nominations.find(
  { tied_nomination_ids: "NOM_001_RECORD_OF__0000" },
  { _id: 0, tie_id: 1, category_id: 1, tied_nomination_ids: 1 }
).limit(2).forEach(printjson);

// Arrays: $elemMatch on secondary_genre_tags
print("\n[3.2] arrays ($elemMatch) — secondary_genre_tags element matches regex '^Adult'");
nomDB.genre_classifications.find(
  { secondary_genre_tags: { $elemMatch: { $regex: "^Adult" } } },
  { _id: 0, classification_id: 1, work_id: 1, secondary_genre_tags: 1 }
).limit(2).forEach(printjson);

// Compound Boolean Filter
print("\n[3.3] Compound Filter ($and + $or + Comparison) — Historical Winner Nominations");
nomDB.nomination_entries.find(
  {
    $and: [
      { nomination_year: { $gte: 1959, $lte: 1965 } },
      {
        $or: [
          { is_winner_flag: { $eq: true } },
          { ballot_slot_order: { $eq: 1 } }
        ]
      }
    ]
  },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, nomination_year: 1, is_winner_flag: 1 }
).limit(3).forEach(printjson);

// ==============================================================================
// 4. DATABASE: grammy_winners_db (Member 4: Winners)
// ==============================================================================
var winDB = db.getSiblingDB("grammy_winners_db");
print("\n>>> [4/5] grammy_winners_db Demonstrations <<<");

// Arrays: Containment on individuals_acknowledged
print("\n[4.1] arrays (Containment) — individuals_acknowledged contains 'Family'");
winDB.acceptance_speeches.find(
  { individuals_acknowledged: "Family" },
  { _id: 0, speech_id: 1, individuals_acknowledged: 1 }
).limit(2).forEach(printjson);

// Arrays: $all on individuals_acknowledged
print("\n[4.2] arrays ($all) — individuals_acknowledged contains BOTH 'Record Label' and 'Fans'");
winDB.acceptance_speeches.find(
  { individuals_acknowledged: { $all: ["Record Label", "Fans"] } },
  { _id: 0, speech_id: 1, individuals_acknowledged: 1 }
).limit(2).forEach(printjson);

// Arrays: $size on individuals_acknowledged
print("\n[4.3] arrays ($size) — Speeches acknowledging exactly 4 distinct entities");
winDB.acceptance_speeches.find(
  { individuals_acknowledged: { $size: 4 } },
  { _id: 0, speech_id: 1, individuals_acknowledged: 1 }
).limit(2).forEach(printjson);

// Cursor Methods: Compound sort and pagination
print("\n[4.4] sort, skip, limit, projection — Multi-attribute ranking on winner_records");
winDB.winner_records.find(
  { presented_live_on_telecast: true },
  { _id: 0, winner_record_id: 1, winning_work_id: 1, trophy_statuettes_awarded_count: 1 }
)
.sort({ trophy_statuettes_awarded_count: -1, winner_record_id: 1 })
.skip(2)
.limit(4)
.forEach(printjson);

// ==============================================================================
// 5. DATABASE: grammy_creators_db (Member 5: Creators/Music)
// ==============================================================================
var crtDB = db.getSiblingDB("grammy_creators_db");
print("\n>>> [5/5] grammy_creators_db Demonstrations <<<");

// Comparison & Logical on songwriters
print("\n[5.1] $and + $in + $gte — Prolific ASCAP/BMI songwriters with >= 100 works");
crtDB.songwriters_composers.find(
  {
    $and: [
      { pro_affiliation: { $in: ["ASCAP", "BMI"] } },
      { registered_works_count: { $gte: 100 } }
    ]
  },
  { _id: 0, songwriter_id: 1, pro_affiliation: 1, registered_works_count: 1 }
).sort({ registered_works_count: -1 }).limit(3).forEach(printjson);

// Embedded Documents on artists
print("\n[5.2] embedded documents — Provenance source_id match on artists");
crtDB.artists.find(
  { "_source_provenance.source_id": { $eq: "SRC-03" } },
  { _id: 0, artist_id: 1, stage_name: 1, "_source_provenance.source_name": 1 }
).limit(2).forEach(printjson);

print("\n==================================================================");
print("MASTER ADVANCED QUERY SUITE EXECUTION COMPLETED");
print("==================================================================");
