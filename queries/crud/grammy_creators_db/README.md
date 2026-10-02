# CRUD Documentation: `grammy_creators_db`

> **Database**: `grammy_creators_db`  
> **Target Collection**: `artists`  
> **Domain Responsibility**: Member 5 (Creator/Music Data)  
> **Phase**: PHASE 18 — CRUD OPERATIONS  

This document details the complete MongoDB CRUD operation catalog for `grammy_creators_db.artists`.

---

## 1. Create Operations

### A. `insertOne`
Inserts a single artist document conforming strictly to the native `$jsonSchema` validator:
```javascript
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
```

### B. `insertMany`
Inserts multiple artist documents in an atomic batch:
```javascript
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
```

---

## 2. Read Operations with Filtering & Projection

### A. `find` (Numeric Comparison `$gte`, Set Inclusion `$in`, Projection)
```javascript
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
```

### B. `findOne`
```javascript
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
```

---

## 3. Update Operations

### A. `updateOne`
```javascript
db.artists.updateOne(
  { artist_id: "CRT_CRUD_DEMO_01" },
  {
    $set: {
      biography_overview: "Updated biography overview for demo ensemble celebrating milestone achievements."
    }
  }
);
```

### B. `updateMany`
```javascript
db.artists.updateMany(
  { artist_id: { $regex: "^CRT_CRUD_DEMO_" } },
  {
    $set: { country_of_citizenship: "International" }
  }
);
```

---

## 4. Delete Operations

### A. `deleteOne`
```javascript
db.artists.deleteOne({ artist_id: "CRT_CRUD_DEMO_01" });
```

### B. `deleteMany`
```javascript
db.artists.deleteMany({ artist_id: { $regex: "^CRT_CRUD_DEMO_" } });
```
