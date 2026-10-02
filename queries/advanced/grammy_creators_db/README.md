# Advanced MongoDB Queries: `grammy_creators_db`

> **Database Scope**: `grammy_creators_db` (Member 5: Creators/Music)  
> **Collections Targeted**: `artists`, `songwriters_composers`, `musical_groups`, `creator_collaborations`  
> **Academic Phase**: Phase 19 — Advanced Queries & Operators (ADBMS Module 10)  
> **Script File**: [`advanced_queries.js`](advanced_queries.js)

---

## 1. Domain & Academic Rationale

`grammy_creators_db` models the individual musicians, songwriters, producers, audio engineers, and performing ensembles that produce Grammy-honored recordings. Real data queries encompass citizenship filtering, catalog sizes (`registered_works_count`), performance rights organization affiliations (ASCAP, BMI), musical group structures (Quartet vs Trio), and carrier debut dates.

Under Module 10, queries against `grammy_creators_db` test composite filters, index-backed sorting, string array non-containment (`$nin`), and nested provenance resolution.

---

## 2. Demonstrated Query Operators & Clauses

| Operator / Clause | Query Description | Target Collection | Relational Algebra Representation |
| :--- | :--- | :--- | :--- |
| **`$eq`** | Domestic recording artists (US citizenship) | `artists` | $\sigma_{citizenship = 'United\ States'}(artists)$ |
| **`$ne`** | International recording artists (non-US) | `artists` | $\sigma_{citizenship \ne 'United\ States'}(artists)$ |
| **`$gt`** | Songwriters with $>120$ registered works | `songwriters_composers` | $\sigma_{registered\_works > 120}(songwriters)$ |
| **`$gte`** | Artists active from 1950 onward | `artists` | $\sigma_{career\_start \ge 1950}(artists)$ |
| **`$lt`** | Early pioneer artists active before 1955 | `artists` | $\sigma_{career\_start < 1955}(artists)$ |
| **`$lte`** | Musical groups formed on or before 1965 | `musical_groups` | $\sigma_{formation\_year \le 1965}(musical\_groups)$ |
| **`$in`** | PRO affiliation in ASCAP or BMI | `songwriters_composers` | $\sigma_{pro \in \{'ASCAP', 'BMI'\}}(songwriters)$ |
| **`$nin`** | Artists outside mainstream Pop and Rock | `artists` | $\sigma_{genre \notin \{Pop, Rock\}}(artists)$ |
| **`$and`** | Solo artists who debuted from 1950 onward | `artists` | $\sigma_{(career\_start \ge 1950) \land (is\_group = false)}(artists)$ |
| **`$or`** | Active groups OR Quartet ensemble structure | `musical_groups` | $\sigma_{(is\_active = true) \lor (structure = 'Quartet')}(musical\_groups)$ |
| **`$not`** | Inverted threshold: NOT $< 100$ works | `songwriters_composers` | $\sigma_{\neg (works < 100)}(songwriters)$ |
| **`embedded docs`** | Provenance verification via dot notation | `artists` | $\sigma_{\_source\_provenance.provenance\_tier = 'PRIMARY OFFICIAL SOURCE'}(artists)$ |
| **Cursor Clauses** | Sort, skip, limit, projection pipeline | `artists` | $\lambda_{4}(\delta_{2}(\tau_{career\_start \uparrow, stage\_name \uparrow}(\pi(artists))))$ |

---

## 3. Query Listings & Code Samples

### 3.1 Comparison Operations

```javascript
// Domestic vs International equality/inequality
db.artists.find(
  { country_of_citizenship: { $eq: "United States" } },
  { _id: 0, artist_id: 1, full_legal_name: 1, country_of_citizenship: 1 }
).limit(3);

db.artists.find(
  { country_of_citizenship: { $ne: "United States" } },
  { _id: 0, artist_id: 1, full_legal_name: 1, country_of_citizenship: 1 }
).limit(3);
```

### 3.2 Complex Logical and Set Operations

```javascript
// Compound $and: Career start >= 1950 AND solo artist
db.artists.find(
  {
    $and: [
      { active_career_start_year: { $gte: 1950 } },
      { is_group_ensemble_flag: { $eq: false } }
    ]
  },
  { _id: 0, artist_id: 1, stage_name: 1, active_career_start_year: 1 }
);

// $or disjunction across ensemble status and structure
db.musical_groups.find(
  {
    $or: [
      { current_activity_status: { $eq: true } },
      { ensemble_structure_type: { $eq: "Quartet" } }
    ]
  },
  { _id: 0, group_id: 1, group_name: 1, current_activity_status: 1 }
);
```

### 3.3 Embedded Document Provenance Verification

```javascript
db.artists.find(
  { "_source_provenance.source_id": { $eq: "SRC-03" } },
  { _id: 0, artist_id: 1, stage_name: 1, "_source_provenance.source_name": 1 }
).limit(3);
```

---

## 4. Execution via `mongosh`

```bash
mongosh "$MONGODB_URI" queries/advanced/grammy_creators_db/advanced_queries.js
```
