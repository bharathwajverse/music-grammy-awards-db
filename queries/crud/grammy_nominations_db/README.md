# CRUD Documentation: `grammy_nominations_db`

> **Database**: `grammy_nominations_db`  
> **Target Collection**: `nomination_entries`  
> **Domain Responsibility**: Member 3 (Nomination Data)  
> **Phase**: PHASE 18 — CRUD OPERATIONS  

This document details the complete MongoDB CRUD operation catalog for `grammy_nominations_db.nomination_entries`.

---

## 1. Create Operations

### A. `insertOne`
Inserts a single nomination entry conforming strictly to the native `$jsonSchema` validator:
```javascript
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
```

### B. `insertMany`
Inserts multiple nomination entries in an atomic batch:
```javascript
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
```

---

## 2. Read Operations with Filtering & Projection

### A. `find` (Compound `$and`, Range Comparison, Projection)
```javascript
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
```

### B. `findOne`
```javascript
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
```

---

## 3. Update Operations

### A. `updateOne`
```javascript
db.nomination_entries.updateOne(
  { nomination_id: "NOM_CRUD_DEMO_01" },
  {
    $set: {
      is_winner_flag: true,
      auditor_validation_code: "DELOITTE-AUDIT-WINNER-CONFIRMED-DEMO"
    }
  }
);
```

### B. `updateMany`
```javascript
db.nomination_entries.updateMany(
  { nomination_id: { $regex: "^NOM_CRUD_DEMO_" } },
  {
    $set: { entry_billing_title: "Audited Demonstration Entry" }
  }
);
```

---

## 4. Delete Operations

### A. `deleteOne`
```javascript
db.nomination_entries.deleteOne({ nomination_id: "NOM_CRUD_DEMO_01" });
```

### B. `deleteMany`
```javascript
db.nomination_entries.deleteMany({ nomination_id: { $regex: "^NOM_CRUD_DEMO_" } });
```
