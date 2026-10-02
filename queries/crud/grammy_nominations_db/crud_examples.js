// ==============================================================================
// Database: grammy_nominations_db
// Collection: nomination_entries
// Phase 18: Documented CRUD Operations
// Demonstrating: insertOne, insertMany, find, findOne, updateOne, updateMany,
//                deleteOne, deleteMany, filtering, and projection
// ==============================================================================

const db = db.getSiblingDB("grammy_nominations_db");

// ------------------------------------------------------------------------------
// 1. CREATE: insertOne
// Inserts a single nomination entry conforming to strict $jsonSchema rules.
// ------------------------------------------------------------------------------
db.nomination_entries.insertOne({
  _id: "NOM_CRUD_DEMO_01",
  nomination_id: "NOM_CRUD_DEMO_01",
  ceremony_id: "CEREMONY_066",
  category_id: "CAT_RECORD_OF_THE_YEAR_000",
  work_id: "WRK_FLOWERS_0001",
  nomination_year: 2024,
  entry_billing_title: "Flowers (Demo Master Entry)",
  primary_artist_id: "CRT_MILEY_CYRUS_0001",
  is_winner_flag: false,
  ballot_slot_order: 1,
  auditor_validation_code: "DELOITTE-AUDIT-VALID-2024-DEMO1",
  created_timestamp: "2024-01-10T12:00:00Z",
  _source_provenance: {
    source_id: "SRC-01",
    source_name: "Recording Academy (NARAS) Official Archive",
    license_type: "Public Domain Historical Facts / Educational Fair Use",
    provenance_tier: "PRIMARY OFFICIAL SOURCE"
  }
});

// ------------------------------------------------------------------------------
// 2. CREATE: insertMany
// Inserts multiple nomination entries in an atomic batch.
// ------------------------------------------------------------------------------
db.nomination_entries.insertMany([
  {
    _id: "NOM_CRUD_DEMO_02",
    nomination_id: "NOM_CRUD_DEMO_02",
    ceremony_id: "CEREMONY_066",
    category_id: "CAT_ALBUM_OF_THE_YEAR_001",
    work_id: "WRK_MIDNIGHTS_0002",
    nomination_year: 2024,
    entry_billing_title: "Midnights (Demo Album Entry)",
    primary_artist_id: "CRT_TAYLOR_SWIFT_0002",
    is_winner_flag: true,
    ballot_slot_order: 2,
    auditor_validation_code: "DELOITTE-AUDIT-VALID-2024-DEMO2",
    created_timestamp: "2024-01-10T12:05:00Z",
    _source_provenance: { source_id: "SRC-01", source_name: "Recording Academy" }
  },
  {
    _id: "NOM_CRUD_DEMO_03",
    nomination_id: "NOM_CRUD_DEMO_03",
    ceremony_id: "CEREMONY_066",
    category_id: "CAT_SONG_OF_THE_YEAR_002",
    work_id: "WRK_WHAT_WAS_I_MADE_FOR_0003",
    nomination_year: 2024,
    entry_billing_title: "What Was I Made For? (Demo Song Entry)",
    primary_artist_id: "CRT_BILLIE_EILISH_0003",
    is_winner_flag: true,
    ballot_slot_order: 3,
    auditor_validation_code: "DELOITTE-AUDIT-VALID-2024-DEMO3",
    created_timestamp: "2024-01-10T12:10:00Z",
    _source_provenance: { source_id: "SRC-01", source_name: "Recording Academy" }
  }
]);

// ------------------------------------------------------------------------------
// 3. READ: find (Filtering with $and, $gt, and Field Projection)
// Finds winning entries from year >= 2000 with ballot slot <= 3.
// ------------------------------------------------------------------------------
db.nomination_entries.find(
  {
    $and: [
      { is_winner_flag: true },
      { nomination_year: { $gte: 2000 } },
      { ballot_slot_order: { $lte: 3 } }
    ]
  },
  {
    _id: 0,
    nomination_id: 1,
    entry_billing_title: 1,
    nomination_year: 1,
    category_id: 1,
    is_winner_flag: 1,
    ballot_slot_order: 1
  }
).sort({ nomination_year: -1 }).limit(10);

// ------------------------------------------------------------------------------
// 4. READ: findOne (Exact match with Projection)
// Queries a specific nomination entry.
// ------------------------------------------------------------------------------
db.nomination_entries.findOne(
  { nomination_id: "NOM_001_RECORD_OF__0000" },
  {
    _id: 0,
    nomination_id: 1,
    entry_billing_title: 1,
    primary_artist_id: 1,
    category_id: 1,
    is_winner_flag: 1
  }
);

// ------------------------------------------------------------------------------
// 5. UPDATE: updateOne
// Promotes demo entry to winner and updates audit token.
// ------------------------------------------------------------------------------
db.nomination_entries.updateOne(
  { nomination_id: "NOM_CRUD_DEMO_01" },
  {
    $set: {
      is_winner_flag: true,
      auditor_validation_code: "DELOITTE-AUDIT-WINNER-CONFIRMED-DEMO"
    }
  }
);

// ------------------------------------------------------------------------------
// 6. UPDATE: updateMany
// Updates ballot order and sets audit remarks on all demo entries.
// ------------------------------------------------------------------------------
db.nomination_entries.updateMany(
  { nomination_id: { $regex: "^NOM_CRUD_DEMO_" } },
  {
    $set: { entry_billing_title: "Audited Demonstration Entry" }
  }
);

// ------------------------------------------------------------------------------
// 7. DELETE: deleteOne
// Removes a single demo nomination.
// ------------------------------------------------------------------------------
db.nomination_entries.deleteOne({ nomination_id: "NOM_CRUD_DEMO_01" });

// ------------------------------------------------------------------------------
// 8. DELETE: deleteMany
// Removes all remaining demonstration nominations matching regex prefix.
// ------------------------------------------------------------------------------
db.nomination_entries.deleteMany({ nomination_id: { $regex: "^NOM_CRUD_DEMO_" } });
