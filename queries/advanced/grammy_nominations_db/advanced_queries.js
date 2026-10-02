// ==============================================================================
// Database: grammy_nominations_db
// Domain: Nominated Works, Entries, Tied Ballots, Packages, Classifications
// Phase 19: Advanced MongoDB Queries & Complex Operators
// ==============================================================================

const db = db.getSiblingDB("grammy_nominations_db");

print("==================================================================");
print("ADVANCED QUERIES: grammy_nominations_db (Member 3: Nominations)");
print("==================================================================");

// ------------------------------------------------------------------------------
// 1. COMPARISON: $eq (Equality)
// Identify verified winning nominations.
// Relational Algebra equivalent: \sigma_{is_winner_flag = true}(nomination_entries)
// ------------------------------------------------------------------------------
print("\n--- 1. Query: $eq (Winner Flag = true) ---");
db.nomination_entries.find(
  { is_winner_flag: { $eq: true } },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, nomination_year: 1, category_id: 1 }
).sort({ nomination_year: 1 }).limit(3);

// ------------------------------------------------------------------------------
// 2. COMPARISON: $ne (Inequality)
// Non-winning finalist nominations contending in award slates.
// Relational Algebra equivalent: \sigma_{is_winner_flag \ne true}(nomination_entries)
// ------------------------------------------------------------------------------
print("\n--- 2. Query: $ne (Winner Flag != true) ---");
db.nomination_entries.find(
  { is_winner_flag: { $ne: true } },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, nomination_year: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 3. COMPARISON: $gt (Greater Than)
// Heavyweight multi-nominees earning more than 4 nominations in a single ceremony.
// Relational Algebra equivalent: \sigma_{total_nominations_count > 4}(multi_nomination_packages)
// ------------------------------------------------------------------------------
print("\n--- 3. Query: $gt (Total Nominations Count > 4) ---");
db.multi_nomination_packages.find(
  { total_nominations_count: { $gt: 4 } },
  { _id: 0, package_id: 1, creator_id: 1, ceremony_year: 1, total_nominations_count: 1 }
).sort({ total_nominations_count: -1 }).limit(3);

// ------------------------------------------------------------------------------
// 4. COMPARISON: $gte (Greater Than or Equal)
// Modern nominations submitted during or after the 2020 award cycle.
// Relational Algebra equivalent: \sigma_{nomination_year \ge 2020}(nomination_entries)
// ------------------------------------------------------------------------------
print("\n--- 4. Query: $gte (Nomination Year >= 2020) ---");
db.nomination_entries.find(
  { nomination_year: { $gte: 2020 } },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, nomination_year: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 5. COMPARISON: $lt (Less Than)
// Early foundational nominations preceding 1965.
// Relational Algebra equivalent: \sigma_{nomination_year < 1965}(nomination_entries)
// ------------------------------------------------------------------------------
print("\n--- 5. Query: $lt (Nomination Year < 1965) ---");
db.nomination_entries.find(
  { nomination_year: { $lt: 1965 } },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, nomination_year: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 6. COMPARISON: $lte (Less Than or Equal)
// Top-tier multi-nominee rankings (Rank 1 or 2).
// Relational Algebra equivalent: \sigma_{leading_nominee_rank \le 2}(multi_nomination_packages)
// ------------------------------------------------------------------------------
print("\n--- 6. Query: $lte (Leading Nominee Rank <= 2) ---");
db.multi_nomination_packages.find(
  { leading_nominee_rank: { $lte: 2 } },
  { _id: 0, package_id: 1, creator_id: 1, leading_nominee_rank: 1, ceremony_year: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 7. COMPARISON: $in (Set Membership)
// Nominations across the Big Three marquee General Field categories.
// Relational Algebra equivalent: \sigma_{category_id \in \{'CAT_RECORD...', 'CAT_ALBUM...', 'CAT_SONG...' \}}(nomination_entries)
// ------------------------------------------------------------------------------
print("\n--- 7. Query: $in (Big Three Categories) ---");
db.nomination_entries.find(
  {
    category_id: {
      $in: [
        "CAT_RECORD_OF_THE_YEAR_000",
        "CAT_ALBUM_OF_THE_YEAR_001",
        "CAT_SONG_OF_THE_YEAR_002"
      ]
    }
  },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, category_id: 1, nomination_year: 1 }
).limit(4);

// ------------------------------------------------------------------------------
// 8. COMPARISON: $nin (Set Non-Membership)
// Genre classifications categorized outside Pop and Rock mainstream fields.
// Relational Algebra equivalent: \sigma_{primary_genre_tag \notin \{'Pop / Contemporary', 'Rock'\}}(genre_classifications)
// ------------------------------------------------------------------------------
print("\n--- 8. Query: $nin (Genre Tag NOT in Pop or Rock) ---");
db.genre_classifications.find(
  { primary_genre_tag: { $nin: ["Pop / Contemporary", "Rock"] } },
  { _id: 0, classification_id: 1, work_id: 1, primary_genre_tag: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 9. LOGICAL: $and (Compound Conjunction)
// Winning entries within the inaugural 1959–1965 period.
// Relational Algebra equivalent: \sigma_{(nomination_year \ge 1959) \land (nomination_year \le 1965) \land (is_winner_flag = true)}(nomination_entries)
// ------------------------------------------------------------------------------
print("\n--- 9. Query: $and (Year 1959-1965 AND is_winner = true) ---");
db.nomination_entries.find(
  {
    $and: [
      { nomination_year: { $gte: 1959 } },
      { nomination_year: { $lte: 1965 } },
      { is_winner_flag: { $eq: true } }
    ]
  },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, nomination_year: 1 }
).sort({ nomination_year: 1 }).limit(3);

// ------------------------------------------------------------------------------
// 10. LOGICAL: $or (Disjunction)
// Nominations that either won OR were placed in the #1 ballot slot.
// Relational Algebra equivalent: \sigma_{(is_winner_flag = true) \lor (ballot_slot_order = 1)}(nomination_entries)
// ------------------------------------------------------------------------------
print("\n--- 10. Query: $or (Winner = true OR Ballot Slot = 1) ---");
db.nomination_entries.find(
  {
    $or: [
      { is_winner_flag: { $eq: true } },
      { ballot_slot_order: { $eq: 1 } }
    ]
  },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, is_winner_flag: 1, ballot_slot_order: 1 }
).limit(4);

// ------------------------------------------------------------------------------
// 11. LOGICAL: $not (Negation)
// Multi-nomination packages where total nominations is NOT less than 5.
// Relational Algebra equivalent: \sigma_{\neg (total_nominations_count < 5)}(multi_nomination_packages)
// ------------------------------------------------------------------------------
print("\n--- 11. Query: $not (NOT total_nominations < 5) ---");
db.multi_nomination_packages.find(
  { total_nominations_count: { $not: { $lt: 5 } } },
  { _id: 0, package_id: 1, creator_id: 1, total_nominations_count: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 12. ARRAYS: tied_nominations & genre_classifications
// ------------------------------------------------------------------------------
print("\n--- 12. Query: Arrays in tied_nominations and genre_classifications ---");

// 12a. Array Containment on tied_nomination_ids
print("  [12a] Array Containment: tied_nomination_ids contains 'NOM_001_RECORD_OF__0000'");
db.tied_nominations.find(
  { tied_nomination_ids: "NOM_001_RECORD_OF__0000" },
  { _id: 0, tie_id: 1, category_id: 1, tied_nomination_ids: 1 }
);

// 12b. Array $all on tied_nomination_ids
print("  [12b] Array $all: tied_nomination_ids contains BOTH target IDs");
db.tied_nominations.find(
  {
    tied_nomination_ids: {
      $all: [
        "NOM_001_RECORD_OF__0000",
        "NOM_001_ALBUM_OF_T_0001"
      ]
    }
  },
  { _id: 0, tie_id: 1, ceremony_id: 1, tied_nomination_ids: 1 }
);

// 12c. Array $size on tied_nomination_ids
print("  [12c] Array $size: ties with exactly 2 tied nominations");
db.tied_nominations.find(
  { tied_nomination_ids: { $size: 2 } },
  { _id: 0, tie_id: 1, tied_nomination_ids: 1, expanded_slate_size: 1 }
).limit(3);

// 12d. Array $elemMatch with Regex on genre_classifications.secondary_genre_tags
print("  [12d] Array $elemMatch: secondary_genre_tags matching regex '^Adult'");
db.genre_classifications.find(
  { secondary_genre_tags: { $elemMatch: { $regex: "^Adult" } } },
  { _id: 0, classification_id: 1, work_id: 1, secondary_genre_tags: 1 }
).limit(3);

// 12e. Array Positional Index (.0)
print("  [12e] Array Positional Index (.0): first tied nomination matches ID");
db.tied_nominations.find(
  { "tied_nomination_ids.0": "NOM_001_RECORD_OF__0000" },
  { _id: 0, tie_id: 1, "tied_nomination_ids.0": 1 }
);

// ------------------------------------------------------------------------------
// 13. EMBEDDED DOCUMENTS: Dot Notation on _source_provenance
// ------------------------------------------------------------------------------
print("\n--- 13. Query: Embedded Documents in nomination_entries ---");
db.nomination_entries.find(
  { "_source_provenance.source_id": { $eq: "SRC-01" } },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, "_source_provenance.source_name": 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 14. CURSOR CLAUSES: sort, skip, limit, projection
// ------------------------------------------------------------------------------
print("\n--- 14. Query: Cursor Clauses (Sort, Skip, Limit, Projection) ---");
db.nomination_entries.find(
  { is_winner_flag: true },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, nomination_year: 1, category_id: 1 }
)
.sort({ nomination_year: -1, ballot_slot_order: 1 })
.skip(3)
.limit(4);
