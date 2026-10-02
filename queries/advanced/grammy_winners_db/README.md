# Advanced MongoDB Queries: `grammy_winners_db`

> **Database Scope**: `grammy_winners_db` (Member 4: Winners)  
> **Collections Targeted**: `winner_records`, `acceptance_speeches`, `consecutive_winners`, `winner_press_releases`, `hall_of_fame_inductions`  
> **Academic Phase**: Phase 19 — Advanced Queries & Operators (ADBMS Module 10)  
> **Script File**: [`advanced_queries.js`](advanced_queries.js)

---

## 1. Domain & Academic Rationale

`grammy_winners_db` records the pinnacle honors of the Recording Academy. The dataset features statuette allocation counts, live telecast broadcast orders, acceptance speech parameters (durations, playoff interruptions, acknowledged entities), consecutive category streaks, and historic Hall of Fame inductions.

Querying this collection demonstrates compound multikey indexing over acknowledged entity arrays (`individuals_acknowledged`), press wire syndication lists (`syndication_wire_distribution`), compound boolean filters (`$and`, `$or`, `$not`), and projection models.

---

## 2. Demonstrated Query Operators & Clauses

| Operator / Clause | Query Description | Target Collection | Relational Algebra Representation |
| :--- | :--- | :--- | :--- |
| **`$eq`** | Trophies presented live on telecast | `winner_records` | $\sigma_{presented\_live = true}(winner\_records)$ |
| **`$ne`** | Presentations with non-unitary statuettes | `winner_records` | $\sigma_{statuettes \ne 1}(winner\_records)$ |
| **`$gt`** | Speeches lasting $>95$ seconds | `acceptance_speeches` | $\sigma_{duration > 95}(acceptance\_speeches)$ |
| **`$gte`** | Consecutive winning streaks $\ge 3$ years | `consecutive_winners` | $\sigma_{streak \ge 3}(consecutive\_winners)$ |
| **`$lt`** | Historic recordings released prior to 1945 | `hall_of_fame_inductions` | $\sigma_{year < 1945}(inductions)$ |
| **`$lte`** | Concise speeches lasting $\le 96$ seconds | `acceptance_speeches` | $\sigma_{duration \le 96}(acceptance\_speeches)$ |
| **`$in`** | Streaks in General Field categories | `consecutive_winners` | $\sigma_{category \in \{Record, Album, Song\}}(consecutive\_winners)$ |
| **`$nin`** | Statuette counts outside [1, 2] | `winner_records` | $\sigma_{statuettes \notin \{1, 2\}}(winner\_records)$ |
| **`$and`** | Live broadcast presentation AND speech delivered | `winner_records` | $\sigma_{(live = true) \land (speech = true)}(winner\_records)$ |
| **`$or`** | Playoff music interrupted OR socio-political theme | `acceptance_speeches` | $\sigma_{(playoff = true) \lor (social = true)}(acceptance\_speeches)$ |
| **`$not`** | Inverted streak length: NOT $< 2$ years | `consecutive_winners` | $\sigma_{\neg (streak < 2)}(consecutive\_winners)$ |
| **`arrays` (Containment)** | Speeches acknowledging "Family" | `acceptance_speeches` | $\sigma_{'Family' \in acknowledged}(acceptance\_speeches)$ |
| **`arrays` (`$all`)** | Speeches acknowledging BOTH Label and Fans | `acceptance_speeches` | $\sigma_{\{'Record\ Label', 'Fans'\} \subseteq acknowledged}(acceptance\_speeches)$ |
| **`arrays` (`$size`)** | Speeches with exactly 4 acknowledged entities | `acceptance_speeches` | $\sigma_{|acknowledged| = 4}(acceptance\_speeches)$ |
| **`arrays` (Index `.0`)** | Positional match on 1st acknowledged entity | `acceptance_speeches` | $\sigma_{acknowledged[0] = 'Record\ Label'}(acceptance\_speeches)$ |
| **`embedded docs`** | License audit search via dot notation (`_source_provenance`) | `winner_records` | Dot notation query on `_source_provenance.license_type` |
| **Cursor Clauses** | Compound sort, skip, limit, projection pipeline | `winner_records` | $\lambda_{4}(\delta_{2}(\tau_{statuettes \downarrow, id \uparrow}(\pi(winner\_records))))$ |

---

## 3. Query Listings & Code Samples

### 3.1 Array Query Operations on `acceptance_speeches`

```javascript
// Array Containment
db.acceptance_speeches.find(
  { individuals_acknowledged: "Family" },
  { _id: 0, speech_id: 1, individuals_acknowledged: 1 }
);

// Array $all: Requires both listed entities
db.acceptance_speeches.find(
  { individuals_acknowledged: { $all: ["Record Label", "Fans"] } },
  { _id: 0, speech_id: 1, individuals_acknowledged: 1 }
);

// Array $size: Exact cardinality
db.acceptance_speeches.find(
  { individuals_acknowledged: { $size: 4 } },
  { _id: 0, speech_id: 1, individuals_acknowledged: 1 }
);

// Array Positional Index Match (.0)
db.acceptance_speeches.find(
  { "individuals_acknowledged.0": "Record Label" },
  { _id: 0, speech_id: 1, "individuals_acknowledged.0": 1 }
);
```

### 3.2 Complex Logical and Comparison Operations

```javascript
// Compound $and with boolean flags
db.winner_records.find(
  {
    $and: [
      { presented_live_on_telecast: { $eq: true } },
      { acceptance_speech_delivered: { $eq: true } }
    ]
  },
  { _id: 0, winner_record_id: 1, winning_work_id: 1, trophy_statuettes_awarded_count: 1 }
);

// $or disjunction across speech delivery conditions
db.acceptance_speeches.find(
  {
    $or: [
      { playoff_music_interrupted: { $eq: true } },
      { social_political_message_flag: { $eq: true } }
    ]
  },
  { _id: 0, speech_id: 1, playoff_music_interrupted: 1, social_political_message_flag: 1 }
);
```

### 3.3 Embedded Document Operations (`_source_provenance`)

```javascript
// Dot-notation query filtering on nested license_type field
db.winner_records.find(
  { "_source_provenance.license_type": { $regex: "Public Domain" } },
  { _id: 0, winner_record_id: 1, "_source_provenance.license_type": 1, "_source_provenance.source_id": 1 }
).limit(5);
```


---

## 4. Execution via `mongosh`

```bash
mongosh "$MONGODB_URI" queries/advanced/grammy_winners_db/advanced_queries.js
```
