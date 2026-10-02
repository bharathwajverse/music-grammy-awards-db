# Advanced MongoDB Queries: `grammy_nominations_db`

> **Database Scope**: `grammy_nominations_db` (Member 3: Nominations)  
> **Collections Targeted**: `nomination_entries`, `tied_nominations`, `genre_classifications`, `multi_nomination_packages`  
> **Academic Phase**: Phase 19 — Advanced Queries & Operators (ADBMS Module 10)  
> **Script File**: [`advanced_queries.js`](advanced_queries.js)

---

## 1. Domain & Academic Rationale

`grammy_nominations_db` captures the comprehensive nomination records of the Grammy Awards. Query requirements feature boolean status filtering (`is_winner_flag`), cardinality thresholds on nomination volume, array queries on tied ballots (`tied_nomination_ids`), element matching with regular expressions on secondary genre tags (`secondary_genre_tags`), and projection pipelines suppressing system keys.

---

## 2. Demonstrated Query Operators & Clauses

| Operator / Clause | Query Description | Target Collection | Relational Algebra Representation |
| :--- | :--- | :--- | :--- |
| **`$eq`** | Confirmed winning nominations | `nomination_entries` | $\sigma_{is\_winner\_flag = true}(nomination\_entries)$ |
| **`$ne`** | Non-winning finalist entries | `nomination_entries` | $\sigma_{is\_winner\_flag \ne true}(nomination\_entries)$ |
| **`$gt`** | Multi-nominees with $>4$ nominations | `multi_nomination_packages` | $\sigma_{total\_nominations\_count > 4}(multi\_nomination\_packages)$ |
| **`$gte`** | Nominations from cycle $\ge 2020$ | `nomination_entries` | $\sigma_{nomination\_year \ge 2020}(nomination\_entries)$ |
| **`$lt`** | Historic entries preceding 1965 | `nomination_entries` | $\sigma_{nomination\_year < 1965}(nomination\_entries)$ |
| **`$lte`** | Top-ranked nominees (rank $\le 2$) | `multi_nomination_packages` | $\sigma_{leading\_nominee\_rank \le 2}(multi\_nomination\_packages)$ |
| **`$in`** | Entries in the Big Three categories | `nomination_entries` | $\sigma_{category\_id \in \{Record, Album, Song\}}(nomination\_entries)$ |
| **`$nin`** | Genre tags outside Pop and Rock | `genre_classifications` | $\sigma_{primary\_genre\_tag \notin \{Pop, Rock\}}(genre\_classifications)$ |
| **`$and`** | Winning entries between 1959–1965 | `nomination_entries` | $\sigma_{(year \ge 1959) \land (year \le 1965) \land (winner = true)}(entries)$ |
| **`$or`** | Winner = true OR Ballot Slot = 1 | `nomination_entries` | $\sigma_{(winner = true) \lor (slot = 1)}(entries)$ |
| **`$not`** | Inverted threshold: NOT $< 5$ nominations | `multi_nomination_packages` | $\sigma_{\neg (total\_nominations < 5)}(packages)$ |
| **`arrays` (Containment)** | Ties containing specific nomination ID | `tied_nominations` | $\sigma_{'NOM\_001...' \in tied\_nomination\_ids}(tied\_nominations)$ |
| **`arrays` (`$all`)** | Ties containing both designated nominations | `tied_nominations` | $\sigma_{\{id_1, id_2\} \subseteq tied\_nomination\_ids}(tied\_nominations)$ |
| **`arrays` (`$size`)** | Ties with exact array length of 2 | `tied_nominations` | $\sigma_{|tied\_nomination\_ids| = 2}(tied\_nominations)$ |
| **`arrays` (`$elemMatch`)** | Array elements satisfying regex `^Adult` | `genre_classifications` | $\sigma_{\exists tag \in secondary\_genre\_tags: tag \sim '^Adult'}(genre\_classifications)$ |
| **`arrays` (Index `.0`)** | Positional match on 1st element of array | `tied_nominations` | $\sigma_{tied\_nomination\_ids[0] = 'NOM\_001...'}(tied\_nominations)$ |
| **`embedded docs`** | Provenance verification via dot notation | `nomination_entries` | $\sigma_{\_source\_provenance.source\_id = 'SRC-01'}(nomination\_entries)$ |
| **Cursor Clauses** | Sort, skip, limit, projection pipeline | `nomination_entries` | $\lambda_{4}(\delta_{3}(\tau_{year \downarrow, slot \uparrow}(\pi(nomination\_entries))))$ |

---

## 3. Query Listings & Code Samples

### 3.1 Array Query Operations on `tied_nominations` and `genre_classifications`

```javascript
// Array Containment
db.tied_nominations.find(
  { tied_nomination_ids: "NOM_001_RECORD_OF__0000" },
  { _id: 0, tie_id: 1, category_id: 1, tied_nomination_ids: 1 }
);

// Array $all: Contains both specified nomination identifiers
db.tied_nominations.find(
  { tied_nomination_ids: { $all: ["NOM_001_RECORD_OF__0000", "NOM_001_ALBUM_OF_T_0001"] } },
  { _id: 0, tie_id: 1, category_id: 1, tied_nomination_ids: 1 }
);

// Array $size: Exact element count
db.tied_nominations.find(
  { tied_nomination_ids: { $size: 2 } },
  { _id: 0, tie_id: 1, tied_nomination_ids: 1 }
);

// Array $elemMatch: Matches nested array element matching regex
db.genre_classifications.find(
  { secondary_genre_tags: { $elemMatch: { $regex: "^Adult" } } },
  { _id: 0, classification_id: 1, work_id: 1, secondary_genre_tags: 1 }
);
```

### 3.2 Complex Logical and Comparison Operations

```javascript
// Compound $and with range and boolean condition
db.nomination_entries.find(
  {
    $and: [
      { nomination_year: { $gte: 1959 } },
      { nomination_year: { $lte: 1965 } },
      { is_winner_flag: { $eq: true } }
    ]
  },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, nomination_year: 1 }
).sort({ nomination_year: 1 });
```

### 3.3 Embedded Document Operations (`_source_provenance`)

```javascript
db.nomination_entries.find(
  { "_source_provenance.source_id": { $eq: "SRC-01" } },
  { _id: 0, nomination_id: 1, entry_billing_title: 1, "_source_provenance.source_name": 1 }
).limit(3);
```

---

## 4. Execution via `mongosh`

```bash
mongosh "$MONGODB_URI" queries/advanced/grammy_nominations_db/advanced_queries.js
```
