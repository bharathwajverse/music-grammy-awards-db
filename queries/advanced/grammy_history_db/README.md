# Advanced MongoDB Queries: `grammy_history_db`

> **Database Scope**: `grammy_history_db` (Member 1: History)  
> **Collections Targeted**: `ceremonies`, `venues`, `viewership_ratings`, `ceremony_hosts`  
> **Academic Phase**: Phase 19 — Advanced Queries & Operators (ADBMS Module 10)  
> **Script File**: [`advanced_queries.js`](advanced_queries.js)

---

## 1. Domain & Academic Rationale

`grammy_history_db` encapsulates the operational and historical evolution of the Recording Academy's Grammy Awards ceremonies from 1959 to the present. Querying this database involves temporal constraints, broadcast network comparisons, venue seating capacities, and audited viewership ratings.

Under Module 10 of Advanced DBMS, queries must demonstrate rigorous predicate selectivity, optimal cursor pipelining (`sort`, `skip`, `limit`), index utilization, projection efficiency (reducing WiredTiger cache pressure), and hierarchical traversal of embedded audit structures (`_source_provenance`).

---

## 2. Demonstrated Query Operators & Clauses

| Operator / Clause | Query Description | Target Collection | Relational Algebra Representation |
| :--- | :--- | :--- | :--- |
| **`$eq`** | Match ceremonies broadcast on CBS | `ceremonies` | $\sigma_{primary\_network = 'CBS'}(ceremonies)$ |
| **`$ne`** | Filter venues outside Los Angeles proper | `venues` | $\sigma_{city \ne 'Los\ Angeles'}(venues)$ |
| **`$gt`** | Telecasts broadcast strictly after 2010 | `ceremonies` | $\sigma_{broadcast\_year > 2010}(ceremonies)$ |
| **`$gte`** | Telecasts with Nielsen ratings $\ge 20.0$ million | `viewership_ratings` | $\sigma_{us\_viewers\_millions \ge 20.0}(viewership\_ratings)$ |
| **`$lt`** | Golden era telecasts broadcast before 1970 | `ceremonies` | $\sigma_{broadcast\_year < 1970}(ceremonies)$ |
| **`$lte`** | The inaugural decade of ceremonies ($\le 10$) | `ceremonies` | $\sigma_{edition\_number \le 10}(ceremonies)$ |
| **`$in`** | Venues located in Beverly Hills or Los Angeles | `venues` | $\sigma_{city \in \{'Beverly\ Hills', 'Los\ Angeles'\}}(venues)$ |
| **`$nin`** | Telecasts excluding commercial syndicates | `ceremonies` | $\sigma_{primary\_network \notin \{'ABC', 'FOX'\}}(ceremonies)$ |
| **`$and`** | CBS broadcasts between 1980–2000 with $>80$ awards | `ceremonies` | $\sigma_{(year \ge 1980) \land (net = 'CBS') \land (awards > 80)}(ceremonies)$ |
| **`$or`** | Arena-scale capacity ($\ge 10,000$) OR Beverly Hills | `venues` | $\sigma_{(capacity \ge 10000) \lor (city = 'Beverly\ Hills')}(venues)$ |
| **`$not`** | Negated predicate: Total awards NOT $< 50$ | `ceremonies` | $\sigma_{\neg (total\_awards < 50)}(ceremonies)$ |
| **`sort`** | Chronological descending sort on broadcast year | `ceremonies` | $\tau_{broadcast\_year \downarrow}(ceremonies)$ |
| **`limit` / `skip`** | Deterministic pagination (page 2, items 6–10) | `ceremonies` | $\lambda_{5}(\delta_{5}(ceremonies))$ |
| **`projection`** | Inclusion of domain keys and `_id: 0` suppression | `ceremonies` | $\pi_{ceremony\_id, broadcast\_year, host\_city}(ceremonies)$ |
| **`embedded docs`** | Dot-notation query on `_source_provenance` | `ceremonies` | $\sigma_{\_source\_provenance.source\_id = 'SRC-01'}(ceremonies)$ |

---

## 3. Query Listings & Execution Semantics

### 3.1 Comparison Suite (`$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`)

```javascript
// $eq: Exact equality
db.ceremonies.find(
  { primary_network: { $eq: "CBS" } },
  { _id: 0, ceremony_id: 1, edition_number: 1, broadcast_year: 1, primary_network: 1 }
).sort({ broadcast_year: -1 }).limit(3);

// $ne: Inequality
db.venues.find(
  { city: { $ne: "Los Angeles" } },
  { _id: 0, venue_id: 1, venue_name: 1, city: 1, state: 1, max_seating_capacity: 1 }
).sort({ max_seating_capacity: -1 }).limit(3);

// $gte & $lt: Range evaluation
db.ceremonies.find(
  { broadcast_year: { $gte: 1959, $lt: 1970 } },
  { _id: 0, ceremony_id: 1, edition_number: 1, broadcast_year: 1 }
).sort({ edition_number: 1 });
```

### 3.2 Logical Operators (`$and`, `$or`, `$not`)

```javascript
// Compound $and with multi-attribute filtering
db.ceremonies.find(
  {
    $and: [
      { broadcast_year: { $gte: 2000 } },
      { primary_network: { $eq: "CBS" } },
      { total_awards_presented: { $gt: 80 } }
    ]
  },
  { _id: 0, ceremony_id: 1, broadcast_year: 1, total_awards_presented: 1 }
);

// $or disjunction across orthogonal attributes
db.venues.find(
  {
    $or: [
      { max_seating_capacity: { $gte: 10000 } },
      { city: { $eq: "Beverly Hills" } }
    ]
  },
  { _id: 0, venue_name: 1, city: 1, max_seating_capacity: 1 }
);

// $not logical inversion
db.ceremonies.find(
  { total_awards_presented: { $not: { $lt: 50 } } },
  { _id: 0, ceremony_id: 1, edition_number: 1, total_awards_presented: 1 }
);
```

### 3.3 Cursor Methods & Pagination Pipeline

```javascript
// Paging: Sort -> Skip -> Limit -> Project
db.ceremonies.find(
  { broadcast_year: { $gte: 1990 } },
  { _id: 0, ceremony_id: 1, edition_number: 1, broadcast_year: 1, host_city: 1, primary_network: 1 }
)
.sort({ broadcast_year: -1 })
.skip(5)
.limit(5);
```

### 3.4 Embedded Document Traversal via Dot Notation

```javascript
// Direct navigation into _source_provenance subdocument
db.ceremonies.find(
  {
    "_source_provenance.source_id": { $eq: "SRC-01" },
    "_source_provenance.provenance_tier": { $eq: "PRIMARY OFFICIAL SOURCE" }
  },
  { _id: 0, ceremony_id: 1, edition_number: 1, "_source_provenance.source_name": 1, "_source_provenance.provenance_tier": 1 }
).limit(3);
```

---

## 4. Execution via `mongosh`

To execute directly in the MongoDB Shell connected to Atlas:

```bash
mongosh "$MONGODB_URI" queries/advanced/grammy_history_db/advanced_queries.js
```
