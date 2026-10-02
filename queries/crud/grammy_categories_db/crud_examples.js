// ==============================================================================
// Database: grammy_categories_db
// Collection: award_categories
// Phase 18: Documented CRUD Operations
// Demonstrating: insertOne, insertMany, find, findOne, updateOne, updateMany,
//                deleteOne, deleteMany, filtering, and projection
// ==============================================================================

const db = db.getSiblingDB("grammy_categories_db");

// ------------------------------------------------------------------------------
// 1. CREATE: insertOne
// Inserts a single award category conforming to strict $jsonSchema rules.
// ------------------------------------------------------------------------------
db.award_categories.insertOne({
  _id: "CAT_CRUD_DEMO_01",
  category_id: "CAT_CRUD_DEMO_01",
  field_id: "FLD_GEN",
  official_category_name: "Best Experimental Spatial Audio Recording",
  standard_short_code: "SPATIAL_AUDIO",
  inaugural_edition: 70,
  is_general_field: false,
  current_status: "Active",
  maximum_nominees_allowed: 5,
  voting_tier_access: "Craft Specialist Voting Members",
  trophy_statuette_eligibility_rule: "Presented to mastering engineer and immersive audio producer",
  entry_fee_tier: "Standard OEP Tier 1",
  _source_provenance: {
    source_id: "SRC-01",
    source_name: "Recording Academy (NARAS) Official Archive",
    license_type: "Public Domain Historical Facts / Educational Fair Use",
    provenance_tier: "PRIMARY OFFICIAL SOURCE"
  }
});

// ------------------------------------------------------------------------------
// 2. CREATE: insertMany
// Inserts multiple categories in batch.
// ------------------------------------------------------------------------------
db.award_categories.insertMany([
  {
    _id: "CAT_CRUD_DEMO_02",
    category_id: "CAT_CRUD_DEMO_02",
    field_id: "FLD_POP",
    official_category_name: "Best Contemporary Hyperpop Vocal Performance",
    standard_short_code: "HYPERPOP_VOC",
    inaugural_edition: 71,
    is_general_field: false,
    current_status: "Active",
    maximum_nominees_allowed: 5,
    voting_tier_access: "Craft Specialist Voting Members",
    trophy_statuette_eligibility_rule: "Presented to lead artist and featured artists",
    entry_fee_tier: "Standard OEP Tier 1",
    _source_provenance: { source_id: "SRC-01", source_name: "Recording Academy" }
  },
  {
    _id: "CAT_CRUD_DEMO_03",
    category_id: "CAT_CRUD_DEMO_03",
    field_id: "FLD_GLOBAL",
    official_category_name: "Best Global Electronic Fusion Album",
    standard_short_code: "GLOBAL_FUSION",
    inaugural_edition: 72,
    is_general_field: false,
    current_status: "Active",
    maximum_nominees_allowed: 5,
    voting_tier_access: "Craft Specialist Voting Members",
    trophy_statuette_eligibility_rule: "Presented to lead artists and primary producers",
    entry_fee_tier: "Standard OEP Tier 1",
    _source_provenance: { source_id: "SRC-01", source_name: "Recording Academy" }
  }
]);

// ------------------------------------------------------------------------------
// 3. READ: find (Filtering with $or, $regex and Field Projection)
// Finds categories in the General field OR with 'Album' in their official name.
// Projects official name, field ID, and max nominees.
// ------------------------------------------------------------------------------
db.award_categories.find(
  {
    $or: [
      { is_general_field: true },
      { official_category_name: { $regex: "Album Of The Year", $options: "i" } }
    ],
    maximum_nominees_allowed: { $gte: 5 }
  },
  {
    _id: 0,
    category_id: 1,
    official_category_name: 1,
    field_id: 1,
    is_general_field: 1,
    maximum_nominees_allowed: 1,
    voting_tier_access: 1
  }
).sort({ maximum_nominees_allowed: -1 }).limit(10);

// ------------------------------------------------------------------------------
// 4. READ: findOne (Exact match with Projection)
// Queries the flagship Record of the Year category.
// ------------------------------------------------------------------------------
db.award_categories.findOne(
  { category_id: "CAT_RECORD_OF_THE_YEAR_000" },
  {
    _id: 0,
    category_id: 1,
    official_category_name: 1,
    is_general_field: 1,
    maximum_nominees_allowed: 1,
    trophy_statuette_eligibility_rule: 1
  }
);

// ------------------------------------------------------------------------------
// 5. UPDATE: updateOne
// Increases maximum nominees allowed and adjusts entry fee tier.
// ------------------------------------------------------------------------------
db.award_categories.updateOne(
  { category_id: "CAT_CRUD_DEMO_01" },
  {
    $set: { entry_fee_tier: "Premium Special Merit Tier" },
    $inc: { maximum_nominees_allowed: 3 }
  }
);

// ------------------------------------------------------------------------------
// 6. UPDATE: updateMany
// Updates status of all demonstration categories.
// ------------------------------------------------------------------------------
db.award_categories.updateMany(
  { category_id: { $regex: "^CAT_CRUD_DEMO_" } },
  {
    $set: { current_status: "Pending Governance Review" }
  }
);

// ------------------------------------------------------------------------------
// 7. DELETE: deleteOne
// Removes a single demo category.
// ------------------------------------------------------------------------------
db.award_categories.deleteOne({ category_id: "CAT_CRUD_DEMO_01" });

// ------------------------------------------------------------------------------
// 8. DELETE: deleteMany
// Removes all remaining demonstration categories matching prefix.
// ------------------------------------------------------------------------------
db.award_categories.deleteMany({ category_id: { $regex: "^CAT_CRUD_DEMO_" } });
