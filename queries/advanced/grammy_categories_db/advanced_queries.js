// ==============================================================================
// Database: grammy_categories_db
// Domain: Award Fields, Categories, Lineages, Quotas, and Restructuring Events
// Phase 19: Advanced MongoDB Queries & Complex Operators
// ==============================================================================

const db = db.getSiblingDB("grammy_categories_db");

print("==================================================================");
print("ADVANCED QUERIES: grammy_categories_db (Member 2: Categories)");
print("==================================================================");

// ------------------------------------------------------------------------------
// 1. COMPARISON: $eq (Equality)
// Select marquee General Field categories (Record, Album, Song, Best New Artist).
// Relational Algebra equivalent: \sigma_{field_id = 'FLD_GENERAL'}(award_categories)
// ------------------------------------------------------------------------------
print("\n--- 1. Query: $eq (Field ID = FLD_GENERAL) ---");
db.award_categories.find(
  { field_id: { $eq: "FLD_GENERAL" } },
  { _id: 0, category_id: 1, official_category_name: 1, is_general_field: 1, maximum_nominees_allowed: 1 }
);

// ------------------------------------------------------------------------------
// 2. COMPARISON: $ne (Inequality)
// Retrieve genre-specific craft categories excluding general field awards.
// Relational Algebra equivalent: \sigma_{is_general_field \ne true}(award_categories)
// ------------------------------------------------------------------------------
print("\n--- 2. Query: $ne (is_general_field != true) ---");
db.award_categories.find(
  { is_general_field: { $ne: true } },
  { _id: 0, category_id: 1, official_category_name: 1, field_id: 1 }
).limit(4);

// ------------------------------------------------------------------------------
// 3. COMPARISON: $gt (Greater Than)
// Award fields housing more than 4 active competing categories.
// Relational Algebra equivalent: \sigma_{active_categories_count > 4}(award_fields)
// ------------------------------------------------------------------------------
print("\n--- 3. Query: $gt (Active Categories Count > 4) ---");
db.award_fields.find(
  { active_categories_count: { $gt: 4 } },
  { _id: 0, field_id: 1, field_name: 1, active_categories_count: 1 }
).sort({ active_categories_count: -1 }).limit(3);

// ------------------------------------------------------------------------------
// 4. COMPARISON: $gte (Greater Than or Equal)
// Modern categories accommodating an expanded slate of 8 or more nominees.
// Relational Algebra equivalent: \sigma_{maximum_nominees_allowed \ge 8}(award_categories)
// ------------------------------------------------------------------------------
print("\n--- 4. Query: $gte (Max Nominees Allowed >= 8) ---");
db.award_categories.find(
  { maximum_nominees_allowed: { $gte: 8 } },
  { _id: 0, category_id: 1, official_category_name: 1, maximum_nominees_allowed: 1 }
).limit(4);

// ------------------------------------------------------------------------------
// 5. COMPARISON: $lt (Less Than)
// Historic categories inaugurated during the founding four ceremonies (< 5).
// Relational Algebra equivalent: \sigma_{inaugural_edition < 5}(award_categories)
// ------------------------------------------------------------------------------
print("\n--- 5. Query: $lt (Inaugural Edition < 5) ---");
db.award_categories.find(
  { inaugural_edition: { $lt: 5 } },
  { _id: 0, category_id: 1, official_category_name: 1, inaugural_edition: 1 }
).sort({ inaugural_edition: 1 }).limit(4);

// ------------------------------------------------------------------------------
// 6. COMPARISON: $lte (Less Than or Equal)
// Categories strictly bound by the traditional 5-nominee slate limit.
// Relational Algebra equivalent: \sigma_{maximum_nominees_allowed \le 5}(award_categories)
// ------------------------------------------------------------------------------
print("\n--- 6. Query: $lte (Max Nominees Allowed <= 5) ---");
db.award_categories.find(
  { maximum_nominees_allowed: { $lte: 5 } },
  { _id: 0, category_id: 1, official_category_name: 1, maximum_nominees_allowed: 1 }
).limit(4);

// ------------------------------------------------------------------------------
// 7. COMPARISON: $in (Set Membership)
// Filter categories belonging to Pop, Rock, or R&B core fields.
// Relational Algebra equivalent: \sigma_{field_id \in \{'FLD_POP', 'FLD_ROCK', 'FLD_R_AND_B'\}}(award_categories)
// ------------------------------------------------------------------------------
print("\n--- 7. Query: $in (Field ID in Pop, Rock, R&B) ---");
db.award_categories.find(
  { field_id: { $in: ["FLD_POP", "FLD_ROCK", "FLD_R_AND_B"] } },
  { _id: 0, category_id: 1, official_category_name: 1, field_id: 1 }
).limit(4);

// ------------------------------------------------------------------------------
// 8. COMPARISON: $nin (Set Non-Membership)
// Categories outside the General Field and Pop classifications.
// Relational Algebra equivalent: \sigma_{field_id \notin \{'FLD_GENERAL', 'FLD_POP'\}}(award_categories)
// ------------------------------------------------------------------------------
print("\n--- 8. Query: $nin (Field ID NOT in General or Pop) ---");
db.award_categories.find(
  { field_id: { $nin: ["FLD_GENERAL", "FLD_POP"] } },
  { _id: 0, category_id: 1, official_category_name: 1, field_id: 1 }
).limit(4);

// ------------------------------------------------------------------------------
// 9. LOGICAL: $and (Conjunction)
// Active categories with expanded nomination slates (>= 8).
// Relational Algebra equivalent: \sigma_{(current_status = 'Active') \land (maximum_nominees_allowed \ge 8)}(award_categories)
// ------------------------------------------------------------------------------
print("\n--- 9. Query: $and (Active Status AND Nominees >= 8) ---");
db.award_categories.find(
  {
    $and: [
      { current_status: { $eq: "Active" } },
      { maximum_nominees_allowed: { $gte: 8 } }
    ]
  },
  { _id: 0, category_id: 1, official_category_name: 1, maximum_nominees_allowed: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 10. LOGICAL: $or (Disjunction)
// Categories matching either Record of the Year OR Album of the Year short codes.
// Relational Algebra equivalent: \sigma_{(short_code = 'RECORD_OF_TH') \lor (short_code = 'ALBUM_OF_THE')}(award_categories)
// ------------------------------------------------------------------------------
print("\n--- 10. Query: $or (Marquee Short Codes) ---");
db.award_categories.find(
  {
    $or: [
      { standard_short_code: { $eq: "RECORD_OF_TH" } },
      { standard_short_code: { $eq: "ALBUM_OF_THE" } }
    ]
  },
  { _id: 0, category_id: 1, official_category_name: 1, standard_short_code: 1 }
);

// ------------------------------------------------------------------------------
// 11. LOGICAL: $not (Negation)
// Categories where nominee limit is NOT greater than 5.
// Relational Algebra equivalent: \sigma_{\neg (maximum_nominees_allowed > 5)}(award_categories)
// ------------------------------------------------------------------------------
print("\n--- 11. Query: $not (NOT Max Nominees > 5) ---");
db.award_categories.find(
  { maximum_nominees_allowed: { $not: { $gt: 5 } } },
  { _id: 0, category_id: 1, official_category_name: 1, maximum_nominees_allowed: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 12. ARRAYS: Element Containment, $all, $size, Positional Index
// Collection: merged_split_history (field: source_category_ids)
// ------------------------------------------------------------------------------
print("\n--- 12. Query: Arrays in merged_split_history ---");

// 12a. Array Element Containment: Matches documents containing 'LEGACY_CAT_MALE_0'
print("  [12a] Array Containment: source_category_ids containing 'LEGACY_CAT_MALE_0'");
db.merged_split_history.find(
  { source_category_ids: "LEGACY_CAT_MALE_0" },
  { _id: 0, event_id: 1, restructuring_type: 1, effective_year: 1, source_category_ids: 1 }
).limit(2);

// 12b. Array $all: Matches documents whose array contains BOTH elements
print("  [12b] Array $all: source_category_ids containing BOTH male & female legacy IDs");
db.merged_split_history.find(
  { source_category_ids: { $all: ["LEGACY_CAT_MALE_0", "LEGACY_CAT_FEMALE_0"] } },
  { _id: 0, event_id: 1, primary_category_id: 1, source_category_ids: 1 }
).limit(2);

// 12c. Array $size: Matches documents where source_category_ids has exact length 2
print("  [12c] Array $size: source_category_ids with exact length 2");
db.merged_split_history.find(
  { source_category_ids: { $size: 2 } },
  { _id: 0, event_id: 1, effective_year: 1, source_category_ids: 1 }
).limit(2);

// 12d. Array Positional Index (.0): Matches first element of array
print("  [12d] Array Positional Index (.0): 1st element equals 'LEGACY_CAT_MALE_0'");
db.merged_split_history.find(
  { "source_category_ids.0": "LEGACY_CAT_MALE_0" },
  { _id: 0, event_id: 1, "source_category_ids.0": 1 }
).limit(2);

// ------------------------------------------------------------------------------
// 13. EMBEDDED DOCUMENTS: Dot Notation on _source_provenance
// ------------------------------------------------------------------------------
print("\n--- 13. Query: Embedded Documents in award_categories ---");
db.award_categories.find(
  { "_source_provenance.provenance_tier": { $eq: "PRIMARY OFFICIAL SOURCE" } },
  { _id: 0, category_id: 1, official_category_name: 1, "_source_provenance.source_name": 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 14. CURSOR CLAUSES: Multi-field sort, skip, limit, projection
// ------------------------------------------------------------------------------
print("\n--- 14. Query: Cursor Clauses (Sort, Skip, Limit, Projection) ---");
db.award_categories.find(
  { current_status: "Active" },
  { _id: 0, category_id: 1, official_category_name: 1, field_id: 1, maximum_nominees_allowed: 1 }
)
.sort({ maximum_nominees_allowed: -1, inaugural_edition: 1 })
.skip(2)
.limit(4);
