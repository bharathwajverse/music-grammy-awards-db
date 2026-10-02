// ==============================================================================
// Database: grammy_winners_db
// Collection: winner_records
// Phase 18: Documented CRUD Operations
// Demonstrating: insertOne, insertMany, find, findOne, updateOne, updateMany,
//                deleteOne, deleteMany, filtering, and projection
// ==============================================================================

const db = db.getSiblingDB("grammy_winners_db");

// ------------------------------------------------------------------------------
// 1. CREATE: insertOne
// Inserts a single winner record conforming to strict $jsonSchema rules.
// ------------------------------------------------------------------------------
db.winner_records.insertOne({
  _id: "WIN_CRUD_DEMO_01",
  winner_record_id: "WIN_CRUD_DEMO_01",
  nomination_id: "NOM_001_RECORD_OF__0000",
  ceremony_id: "CEREMONY_066",
  category_id: "CAT_RECORD_OF_THE_YEAR_000",
  winning_work_id: "WRK_FLOWERS_0001",
  primary_artist_id: "CRT_MILEY_CYRUS_0001",
  broadcast_presentation_order: 12,
  presented_live_on_telecast: true,
  acceptance_speech_delivered: false,
  trophy_statuettes_awarded_count: 2,
  verified_timestamp: "2024-02-04T23:30:00Z",
  _source_provenance: {
    source_id: "SRC-05",
    source_name: "Recording Academy Official Winner Registry",
    license_type: "Public Domain Historical Facts / Educational Fair Use",
    provenance_tier: "PRIMARY OFFICIAL SOURCE"
  }
});

// ------------------------------------------------------------------------------
// 2. CREATE: insertMany
// Inserts multiple winner records in an atomic batch.
// ------------------------------------------------------------------------------
db.winner_records.insertMany([
  {
    _id: "WIN_CRUD_DEMO_02",
    winner_record_id: "WIN_CRUD_DEMO_02",
    nomination_id: "NOM_001_RECORD_OF__0000",
    ceremony_id: "CEREMONY_066",
    category_id: "CAT_ALBUM_OF_THE_YEAR_001",
    winning_work_id: "WRK_MIDNIGHTS_0002",
    primary_artist_id: "CRT_TAYLOR_SWIFT_0002",
    broadcast_presentation_order: 15,
    presented_live_on_telecast: true,
    acceptance_speech_delivered: false,
    trophy_statuettes_awarded_count: 4,
    verified_timestamp: "2024-02-04T23:45:00Z",
    _source_provenance: { source_id: "SRC-05", source_name: "Recording Academy" }
  },
  {
    _id: "WIN_CRUD_DEMO_03",
    winner_record_id: "WIN_CRUD_DEMO_03",
    nomination_id: "NOM_001_RECORD_OF__0000",
    ceremony_id: "CEREMONY_066",
    category_id: "CAT_SONG_OF_THE_YEAR_002",
    winning_work_id: "WRK_WHAT_WAS_I_MADE_FOR_0003",
    primary_artist_id: "CRT_BILLIE_EILISH_0003",
    broadcast_presentation_order: 10,
    presented_live_on_telecast: true,
    acceptance_speech_delivered: false,
    trophy_statuettes_awarded_count: 2,
    verified_timestamp: "2024-02-04T23:15:00Z",
    _source_provenance: { source_id: "SRC-05", source_name: "Recording Academy" }
  }
]);

// ------------------------------------------------------------------------------
// 3. READ: find (Filtering with $gte, $eq and Field Projection)
// Finds winners presented live on telecast with at least 2 statuettes awarded.
// ------------------------------------------------------------------------------
db.winner_records.find(
  {
    presented_live_on_telecast: true,
    trophy_statuettes_awarded_count: { $gte: 2 }
  },
  {
    _id: 0,
    winner_record_id: 1,
    primary_artist_id: 1,
    category_id: 1,
    trophy_statuettes_awarded_count: 1,
    broadcast_presentation_order: 1,
    verified_timestamp: 1
  }
).sort({ broadcast_presentation_order: 1 }).limit(10);

// ------------------------------------------------------------------------------
// 4. READ: findOne (Exact match with Projection)
// Queries a specific historic winner record.
// ------------------------------------------------------------------------------
db.winner_records.findOne(
  { winner_record_id: "WIN_NOM_001_RECORD_OF__0000" },
  {
    _id: 0,
    winner_record_id: 1,
    nomination_id: 1,
    category_id: 1,
    primary_artist_id: 1,
    trophy_statuettes_awarded_count: 1
  }
);

// ------------------------------------------------------------------------------
// 5. UPDATE: updateOne
// Increments statuette count and adjusts presentation order on demo record.
// ------------------------------------------------------------------------------
db.winner_records.updateOne(
  { winner_record_id: "WIN_CRUD_DEMO_01" },
  {
    $inc: { trophy_statuettes_awarded_count: 1 },
    $set: { broadcast_presentation_order: 1 }
  }
);

// ------------------------------------------------------------------------------
// 6. UPDATE: updateMany
// Updates acceptance speech flag on all demonstration winner records.
// ------------------------------------------------------------------------------
db.winner_records.updateMany(
  { winner_record_id: { $regex: "^WIN_CRUD_DEMO_" } },
  {
    $set: { acceptance_speech_delivered: true }
  }
);

// ------------------------------------------------------------------------------
// 7. DELETE: deleteOne
// Removes a single demonstration winner record.
// ------------------------------------------------------------------------------
db.winner_records.deleteOne({ winner_record_id: "WIN_CRUD_DEMO_01" });

// ------------------------------------------------------------------------------
// 8. DELETE: deleteMany
// Removes all remaining demonstration winner records matching regex pattern.
// ------------------------------------------------------------------------------
db.winner_records.deleteMany({ winner_record_id: { $regex: "^WIN_CRUD_DEMO_" } });
