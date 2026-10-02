// ==============================================================================
// Database: grammy_history_db
// Collection: ceremonies
// Phase 18: Documented CRUD Operations
// Demonstrating: insertOne, insertMany, find, findOne, updateOne, updateMany,
//                deleteOne, deleteMany, filtering, and projection
// ==============================================================================

const db = db.getSiblingDB("grammy_history_db");

// ------------------------------------------------------------------------------
// 1. CREATE: insertOne
// Inserts a single ceremony document adhering to strict $jsonSchema validation.
// ------------------------------------------------------------------------------
db.ceremonies.insertOne({
  _id: "CEREMONY_CRUD_DEMO_01",
  ceremony_id: "CEREMONY_CRUD_DEMO_01",
  edition_number: 99,
  ceremony_date: "2057-02-15",
  broadcast_year: 2057,
  eligibility_period_start: "2055-10-01",
  eligibility_period_end: "2056-09-30",
  host_city: "Los Angeles",
  venue_id: "VEN_STAPLES_CRYPTO_ARENA",
  primary_network: "CBS",
  total_awards_presented: 84,
  created_at: "2057-01-01T00:00:00Z",
  _source_provenance: {
    source_id: "SRC-01",
    source_name: "Recording Academy (NARAS) Official Archive",
    license_type: "Public Domain Historical Facts / Educational Fair Use",
    provenance_tier: "PRIMARY OFFICIAL SOURCE"
  }
});

// ------------------------------------------------------------------------------
// 2. CREATE: insertMany
// Inserts multiple ceremony documents in a single atomic batch.
// ------------------------------------------------------------------------------
db.ceremonies.insertMany([
  {
    _id: "CEREMONY_CRUD_DEMO_02",
    ceremony_id: "CEREMONY_CRUD_DEMO_02",
    edition_number: 100,
    ceremony_date: "2058-02-14",
    broadcast_year: 2058,
    eligibility_period_start: "2056-10-01",
    eligibility_period_end: "2057-09-30",
    host_city: "New York",
    venue_id: "VEN_MADISON_SQUARE_GARDEN",
    primary_network: "CBS",
    total_awards_presented: 86,
    created_at: "2058-01-01T00:00:00Z",
    _source_provenance: {
      source_id: "SRC-01",
      source_name: "Recording Academy (NARAS) Official Archive",
      license_type: "Public Domain Historical Facts / Educational Fair Use"
    }
  },
  {
    _id: "CEREMONY_CRUD_DEMO_03",
    ceremony_id: "CEREMONY_CRUD_DEMO_03",
    edition_number: 101,
    ceremony_date: "2059-02-16",
    broadcast_year: 2059,
    eligibility_period_start: "2057-10-01",
    eligibility_period_end: "2058-09-30",
    host_city: "Nashville",
    venue_id: "VEN_NASHVILLE_AUDITORIUM",
    primary_network: "NBC",
    total_awards_presented: 88,
    created_at: "2059-01-01T00:00:00Z",
    _source_provenance: {
      source_id: "SRC-01",
      source_name: "Recording Academy (NARAS) Official Archive",
      license_type: "Public Domain Historical Facts / Educational Fair Use"
    }
  }
]);

// ------------------------------------------------------------------------------
// 3. READ: find (with Filtering and Projection)
// Filters ceremonies by broadcast year range ($gte, $lte) and network ($in).
// Projects specific domain fields while suppressing internal _id.
// ------------------------------------------------------------------------------
db.ceremonies.find(
  {
    broadcast_year: { $gte: 2000, $lte: 2024 },
    primary_network: { $in: ["CBS", "NBC"] }
  },
  {
    _id: 0,
    ceremony_id: 1,
    edition_number: 1,
    broadcast_year: 1,
    host_city: 1,
    primary_network: 1,
    total_awards_presented: 1
  }
).sort({ broadcast_year: -1 }).limit(5);

// ------------------------------------------------------------------------------
// 4. READ: findOne (with Filtering and Projection)
// Queries a single ceremony by unique natural key and projects telecast data.
// ------------------------------------------------------------------------------
db.ceremonies.findOne(
  { ceremony_id: "CEREMONY_001" },
  {
    _id: 0,
    ceremony_id: 1,
    edition_number: 1,
    ceremony_date: 1,
    host_city: 1,
    primary_network: 1
  }
);

// ------------------------------------------------------------------------------
// 5. UPDATE: updateOne
// Updates host city and increments total awards on demo record.
// ------------------------------------------------------------------------------
db.ceremonies.updateOne(
  { ceremony_id: "CEREMONY_CRUD_DEMO_01" },
  {
    $set: { host_city: "Las Vegas", primary_network: "Paramount+" },
    $inc: { total_awards_presented: 2 }
  }
);

// ------------------------------------------------------------------------------
// 6. UPDATE: updateMany
// Updates all demonstration ceremonies using regex filter and sets status flag.
// ------------------------------------------------------------------------------
db.ceremonies.updateMany(
  { ceremony_id: { $regex: "^CEREMONY_CRUD_DEMO_" } },
  {
    $set: { "venue_id": "VEN_TEMPORARY_STAGING" }
  }
);

// ------------------------------------------------------------------------------
// 7. DELETE: deleteOne
// Removes a single demonstration ceremony by primary identifier.
// ------------------------------------------------------------------------------
db.ceremonies.deleteOne({ ceremony_id: "CEREMONY_CRUD_DEMO_01" });

// ------------------------------------------------------------------------------
// 8. DELETE: deleteMany
// Cleans up remaining demonstration documents matching regex pattern.
// ------------------------------------------------------------------------------
db.ceremonies.deleteMany({ ceremony_id: { $regex: "^CEREMONY_CRUD_DEMO_" } });
