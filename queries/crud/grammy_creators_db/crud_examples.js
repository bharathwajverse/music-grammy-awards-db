// ==============================================================================
// Database: grammy_creators_db
// Collection: artists
// Phase 18: Documented CRUD Operations
// Demonstrating: insertOne, insertMany, find, findOne, updateOne, updateMany,
//                deleteOne, deleteMany, filtering, and projection
// ==============================================================================

const db = db.getSiblingDB("grammy_creators_db");

// ------------------------------------------------------------------------------
// 1. CREATE: insertOne
// Inserts a single artist document conforming to strict $jsonSchema rules.
// ------------------------------------------------------------------------------
db.artists.insertOne({
  _id: "CRT_CRUD_DEMO_01",
  artist_id: "CRT_CRUD_DEMO_01",
  full_legal_name: "Demo Vanguard Ensemble Group",
  stage_name: "Demo Vanguard Ensemble",
  primary_musical_genre: "Pop / Vocal",
  birth_or_formation_date: "2005-06-20",
  country_of_citizenship: "United States",
  active_career_start_year: 2020,
  is_group_ensemble_flag: true,
  musicbrainz_artist_gid: "b7132962-d922-4a0e-9477-88981d330001",
  official_website_url: "https://musicbrainz.org/artist/b7132962-d922-4a0e-9477-88981d330001",
  biography_overview: "Demo Vanguard Ensemble Group is an acclaimed experimental pop recording ensemble.",
  _source_provenance: {
    source_id: "SRC-03",
    source_name: "MetaBrainz Foundation MusicBrainz Registry",
    license_type: "CC0: Public Domain / Open Data",
    provenance_tier: "PRIMARY OPEN DATA REGISTRY"
  }
});

// ------------------------------------------------------------------------------
// 2. CREATE: insertMany
// Inserts multiple artist documents in an atomic batch.
// ------------------------------------------------------------------------------
db.artists.insertMany([
  {
    _id: "CRT_CRUD_DEMO_02",
    artist_id: "CRT_CRUD_DEMO_02",
    full_legal_name: "Aura Symphony Project",
    stage_name: "Aura Symphony Collective",
    primary_musical_genre: "Classical Crossover",
    birth_or_formation_date: "2010-09-15",
    country_of_citizenship: "United Kingdom",
    active_career_start_year: 2022,
    is_group_ensemble_flag: true,
    musicbrainz_artist_gid: "c8142962-d922-4a0e-9477-88981d330002",
    official_website_url: "https://musicbrainz.org/artist/c8142962-d922-4a0e-9477-88981d330002",
    biography_overview: "Aura Symphony Collective is an international classical crossover performance group.",
    _source_provenance: { source_id: "SRC-03", source_name: "MetaBrainz Foundation" }
  },
  {
    _id: "CRT_CRUD_DEMO_03",
    artist_id: "CRT_CRUD_DEMO_03",
    full_legal_name: "Neon Rhythm Productions",
    stage_name: "Neon Rhythm Syndicate",
    primary_musical_genre: "R&B / Soul",
    birth_or_formation_date: "1998-04-12",
    country_of_citizenship: "United States",
    active_career_start_year: 2018,
    is_group_ensemble_flag: false,
    musicbrainz_artist_gid: "d9152962-d922-4a0e-9477-88981d330003",
    official_website_url: "https://musicbrainz.org/artist/d9152962-d922-4a0e-9477-88981d330003",
    biography_overview: "Neon Rhythm Syndicate is a contemporary urban soul and R&B music producer and solo artist.",
    _source_provenance: { source_id: "SRC-03", source_name: "MetaBrainz Foundation" }
  }
]);

// ------------------------------------------------------------------------------
// 3. READ: find (Filtering with $gte, $in and Field Projection)
// Finds artists active since 1950 from specified countries.
// ------------------------------------------------------------------------------
db.artists.find(
  {
    active_career_start_year: { $gte: 1950 },
    country_of_citizenship: { $in: ["United States", "Canada", "United Kingdom"] }
  },
  {
    _id: 0,
    artist_id: 1,
    stage_name: 1,
    primary_musical_genre: 1,
    active_career_start_year: 1,
    country_of_citizenship: 1
  }
).sort({ active_career_start_year: 1 }).limit(10);

// ------------------------------------------------------------------------------
// 4. READ: findOne (Exact match with Projection)
// Queries a specific historic creator.
// ------------------------------------------------------------------------------
db.artists.findOne(
  { artist_id: "CRT_HENRY_MANCINI_0001" },
  {
    _id: 0,
    artist_id: 1,
    stage_name: 1,
    primary_musical_genre: 1,
    country_of_citizenship: 1,
    active_career_start_year: 1
  }
);

// ------------------------------------------------------------------------------
// 5. UPDATE: updateOne
// Updates biography overview for milestone celebrations on demo record.
// ------------------------------------------------------------------------------
db.artists.updateOne(
  { artist_id: "CRT_CRUD_DEMO_01" },
  {
    $set: {
      biography_overview: "Updated biography overview for demo ensemble celebrating milestone achievements."
    }
  }
);

// ------------------------------------------------------------------------------
// 6. UPDATE: updateMany
// Updates country of citizenship on all demonstration artists.
// ------------------------------------------------------------------------------
db.artists.updateMany(
  { artist_id: { $regex: "^CRT_CRUD_DEMO_" } },
  {
    $set: { country_of_citizenship: "International" }
  }
);

// ------------------------------------------------------------------------------
// 7. DELETE: deleteOne
// Removes a single demonstration artist document.
// ------------------------------------------------------------------------------
db.artists.deleteOne({ artist_id: "CRT_CRUD_DEMO_01" });

// ------------------------------------------------------------------------------
// 8. DELETE: deleteMany
// Removes all remaining demonstration artists matching prefix.
// ------------------------------------------------------------------------------
db.artists.deleteMany({ artist_id: { $regex: "^CRT_CRUD_DEMO_" } });
