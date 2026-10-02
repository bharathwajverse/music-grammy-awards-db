# Advanced MongoDB Queries: `grammy_categories_db`

> **Database Scope**: `grammy_categories_db` (Member 2: Categories)  
> **Collections Targeted**: `award_categories`, `award_fields`, `merged_split_history`, `eligibility_rules`  
> **Academic Phase**: Phase 19 — Advanced Queries & Operators (ADBMS Module 10)  
> **Script File**: [`advanced_queries.js`](advanced_queries.js)

---

## 1. Domain & Academic Rationale

`grammy_categories_db` models the structural taxonomy of the Grammy Awards: official category hierarchies, genre fields (General, Pop, Rock, R&B, Jazz, etc.), nomination slate limits (5 vs 8 nominees), and the historical consolidation and splitting of categories over time.

In Module 10 of Advanced DBMS, this database illustrates multikey indexing over array attributes (`source_category_ids`), array set semantics (`$all`, `$size`, element containment, and positional index matching `.0`), along with standard comparison and compound boolean expressions.

---

## 2. Demonstrated Query Operators & Clauses

| Operator / Clause | Query Description | Target Collection | Relational Algebra Representation |
| :--- | :--- | :--- | :--- |
| **`$eq`** | Match General Field categories | `award_categories` | $\sigma_{field\_id = 'FLD\_GENERAL'}(award\_categories)$ |
| **`$ne`** | Filter non-general craft categories | `award_categories` | $\sigma_{is\_general\_field \ne true}(award\_categories)$ |
| **`$gt`** | Fields housing $>4$ active categories | `award_fields` | $\sigma_{active\_categories\_count > 4}(award\_fields)$ |
| **`$gte`** | Categories with expanded slate $\ge 8$ nominees | `award_categories` | $\sigma_{maximum\_nominees\_allowed \ge 8}(award\_categories)$ |
| **`$lt`** | Foundational categories inaugurated in editions $< 5$ | `award_categories` | $\sigma_{inaugural\_edition < 5}(award\_categories)$ |
| **`$lte`** | Categories with standard slate limit $\le 5$ | `award_categories` | $\sigma_{maximum\_nominees\_allowed \le 5}(award\_categories)$ |
| **`$in`** | Categories in Pop, Rock, or R&B fields | `award_categories` | $\sigma_{field\_id \in \{'FLD\_POP', 'FLD\_ROCK', 'FLD\_R\_AND\_B'\}}(award\_categories)$ |
| **`$nin`** | Categories outside General and Pop fields | `award_categories` | $\sigma_{field\_id \notin \{'FLD\_GENERAL', 'FLD\_POP'\}}(award\_categories)$ |
| **`$and`** | Active categories with expanded slates | `award_categories` | $\sigma_{(status = 'Active') \land (nominees \ge 8)}(award\_categories)$ |
| **`$or`** | Flagship categories (Record or Album of the Year) | `award_categories` | $\sigma_{(code = 'RECORD\_OF\_TH') \lor (code = 'ALBUM\_OF\_THE')}(award\_categories)$ |
| **`$not`** | Inverted range: NOT $> 5$ nominees | `award_categories` | $\sigma_{\neg (maximum\_nominees\_allowed > 5)}(award\_categories)$ |
| **`arrays` (Containment)** | Restructuring events containing predecessor ID | `merged_split_history` | $\sigma_{'LEGACY\_CAT\_MALE\_0' \in source\_category\_ids}(merged\_split\_history)$ |
| **`arrays` (`$all`)** | Events containing BOTH predecessor IDs | `merged_split_history` | $\sigma_{\{'LEGACY\_CAT\_MALE\_0', 'LEGACY\_CAT\_FEMALE\_0'\} \subseteq source\_category\_ids}(merged\_split\_history)$ |
| **`arrays` (`$size`)** | Events with exactly 2 predecessor categories | `merged_split_history` | $\sigma_{|source\_category\_ids| = 2}(merged\_split\_history)$ |
| **`arrays` (Index `.0`)** | Positional match on 1st predecessor element | `merged_split_history` | $\sigma_{source\_category\_ids[0] = 'LEGACY\_CAT\_MALE\_0'}(merged\_split\_history)$ |
| **`embedded docs`** | Provenance verification via dot notation | `award_categories` | $\sigma_{\_source\_provenance.provenance\_tier = 'PRIMARY OFFICIAL SOURCE'}(award\_categories)$ |
| **Cursor Clauses** | Multi-attribute sorting, skip, limit, projection | `award_categories` | $\lambda_{4}(\delta_{2}(\tau_{nominees \downarrow, edition \uparrow}(\pi(award\_categories))))$ |

---

## 3. Query Listings & Code Samples

### 3.1 Array Query Operations on `merged_split_history`

```javascript
// Array Containment
db.merged_split_history.find(
  { source_category_ids: "LEGACY_CAT_MALE_0" },
  { _id: 0, event_id: 1, restructuring_type: 1, source_category_ids: 1 }
);

// Array $all: Requires both elements to be present in the array
db.merged_split_history.find(
  { source_category_ids: { $all: ["LEGACY_CAT_MALE_0", "LEGACY_CAT_FEMALE_0"] } },
  { _id: 0, event_id: 1, primary_category_id: 1, source_category_ids: 1 }
);

// Array $size: Exact cardinality check
db.merged_split_history.find(
  { source_category_ids: { $size: 2 } },
  { _id: 0, event_id: 1, effective_year: 1 }
);

// Array Positional Index Match (.0)
db.merged_split_history.find(
  { "source_category_ids.0": "LEGACY_CAT_MALE_0" },
  { _id: 0, event_id: 1, source_category_ids: 1 }
);
```

### 3.2 Complex Logical and Comparison Operations

```javascript
// Compound $and conjunction
db.award_categories.find(
  {
    $and: [
      { current_status: { $eq: "Active" } },
      { maximum_nominees_allowed: { $gte: 8 } }
    ]
  },
  { _id: 0, category_id: 1, official_category_name: 1, maximum_nominees_allowed: 1 }
);

// $or disjunction across short codes
db.award_categories.find(
  {
    $or: [
      { standard_short_code: { $eq: "RECORD_OF_TH" } },
      { standard_short_code: { $eq: "ALBUM_OF_THE" } }
    ]
  },
  { _id: 0, category_id: 1, official_category_name: 1 }
);
```

### 3.3 Embedded Document Provenance Verification

```javascript
db.award_categories.find(
  { "_source_provenance.provenance_tier": { $eq: "PRIMARY OFFICIAL SOURCE" } },
  { _id: 0, category_id: 1, official_category_name: 1, "_source_provenance.source_name": 1 }
).limit(3);
```

---

## 4. Execution via `mongosh`

```bash
mongosh "$MONGODB_URI" queries/advanced/grammy_categories_db/advanced_queries.js
```
