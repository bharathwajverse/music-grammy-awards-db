# CRUD Documentation: `grammy_history_db`

> **Database**: `grammy_history_db`  
> **Target Collection**: `ceremonies`  
> **Domain Responsibility**: Member 1 (History Data)  
> **Phase**: PHASE 18 — CRUD OPERATIONS  

This document details the complete MongoDB CRUD operation catalog for `grammy_history_db.ceremonies`, including atomic insertions, multi-document writes, complex filtering, projections, atomic updates, and deterministic deletions.

---

## 1. Create Operations

### A. `insertOne`
Inserts a single ceremony document adhering strictly to the native `$jsonSchema` validator:
```javascript
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
```
- **Return**: `{ acknowledged: true, insertedId: "CEREMONY_CRUD_DEMO_01" }`
- **Validation**: Enforced at `validationLevel: strict`.

### B. `insertMany`
Inserts multiple ceremony documents in a single atomic network roundtrip:
```javascript
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
    _source_provenance: { source_id: "SRC-01", source_name: "Recording Academy" }
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
    _source_provenance: { source_id: "SRC-01", source_name: "Recording Academy" }
  }
]);
```
- **Return**: `{ acknowledged: true, insertedIds: { "0": "CEREMONY_CRUD_DEMO_02", "1": "CEREMONY_CRUD_DEMO_03" } }`

---

## 2. Read Operations with Filtering & Projection

### A. `find` (Range Filtering & Field Projection)
Demonstrates multi-condition filtering with `$gte`, `$lte`, and `$in`, combined with an explicit projection suppressing `_id`:
```javascript
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
```
- **Filter**: `broadcast_year` in `[2000, 2024]` AND `primary_network` in `["CBS", "NBC"]`.
- **Projection**: Excludes `_id` (0) and projects 6 domain attributes (1).

### B. `findOne` (Exact Equality Match & Selective Projection)
Retrieves the inaugural GRAMMY ceremony document:
```javascript
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
```

---

## 3. Update Operations

### A. `updateOne`
Performs an atomic in-place modification of fields using `$set` and numeric increment with `$inc`:
```javascript
db.ceremonies.updateOne(
  { ceremony_id: "CEREMONY_CRUD_DEMO_01" },
  {
    $set: { host_city: "Las Vegas", primary_network: "Paramount+" },
    $inc: { total_awards_presented: 2 }
  }
);
```
- **Return**: `{ acknowledged: true, matchedCount: 1, modifiedCount: 1 }`

### B. `updateMany`
Performs a multi-document update on records matching a regex prefix:
```javascript
db.ceremonies.updateMany(
  { ceremony_id: { $regex: "^CEREMONY_CRUD_DEMO_" } },
  {
    $set: { "venue_id": "VEN_TEMPORARY_STAGING" }
  }
);
```
- **Return**: `{ acknowledged: true, matchedCount: 3, modifiedCount: 3 }`

---

## 4. Delete Operations

### A. `deleteOne`
Removes a specific document by its primary key:
```javascript
db.ceremonies.deleteOne({ ceremony_id: "CEREMONY_CRUD_DEMO_01" });
```
- **Return**: `{ acknowledged: true, deletedCount: 1 }`

### B. `deleteMany`
Cleans up all remaining temporary demonstration documents matching the filter criteria:
```javascript
db.ceremonies.deleteMany({ ceremony_id: { $regex: "^CEREMONY_CRUD_DEMO_" } });
```
- **Return**: `{ acknowledged: true, deletedCount: 2 }`
