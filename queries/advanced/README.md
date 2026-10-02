# Advanced MongoDB Queries Suite

> **Course**: Advanced Database Management Systems (ADBMS)  
> **Curriculum Module**: Module 10 — Advanced Query Operators, Multikey Indexing & Complex Expressions  
> **Academic Phase**: Phase 19 — Advanced MongoDB Queries  
> **Status Date**: October 2026  
> **Engine**: MongoDB Atlas (`Cluster0`) / MongoDB Shell (`mongosh`)  
> **Databases Covered**: All 5 Approved Databases (`grammy_history_db`, `grammy_categories_db`, `grammy_nominations_db`, `grammy_winners_db`, `grammy_creators_db`)

---

## 1. Executive Summary & Curriculum Alignment

Phase 19 establishes the advanced document querying layer of the **GRAMMY Awards Information & Analytics System**. Designed in accordance with Module 10 of the Advanced DBMS curriculum, this suite demonstrates the expressive capabilities of MongoDB's JSON/BSON document model, moving beyond basic point CRUD queries into complex conditional filtering, set membership, multikey array processing, compound boolean logic, and deep hierarchical document navigation.

Every query in this repository executes exclusively against **certified, loaded production data** on MongoDB Atlas (ingested from `data/validated/`), adhering strictly to the architectural guarantee: **zero invented facts, zero mock artifacts**.

---

## 2. Mandatory Query Operators & Clauses Reference

Phase 19 rigorously demonstrates, documents, and verifies all 17 mandatory query operators and cursor clauses:

| Classification | Operator / Clause | Mathematical / Relational Equivalent | Functional Definition |
| :--- | :--- | :--- | :--- |
| **Comparison** | **`$eq`** | $R.A = v$ | Matches values that are strictly equal to a specified value. |
| **Comparison** | **`$ne`** | $R.A \ne v$ | Matches all values that are not equal to a specified value. |
| **Comparison** | **`$gt`** | $R.A > v$ | Matches values that are strictly greater than a specified value. |
| **Comparison** | **`$gte`** | $R.A \ge v$ | Matches values that are greater than or equal to a specified value. |
| **Comparison** | **`$lt`** | $R.A < v$ | Matches values that are strictly less than a specified value. |
| **Comparison** | **`$lte`** | $R.A \le v$ | Matches values that are less than or equal to a specified value. |
| **Comparison** | **`$in`** | $R.A \in \{v_1, v_2, \dots\}$ | Matches any of the values specified in an array. |
| **Comparison** | **`$nin`** | $R.A \notin \{v_1, v_2, \dots\}$ | Matches none of the values specified in an array. |
| **Logical** | **`$and`** | $C_1 \land C_2 \land \dots$ | Joins query clauses with a logical AND; returns documents that match all clauses. |
| **Logical** | **`$or`** | $C_1 \lor C_2 \lor \dots$ | Joins query clauses with a logical OR; returns documents that match at least one clause. |
| **Logical** | **`$not`** | $\neg(C)$ | Inverts the effect of a query expression; returns documents that do not match the clause. |
| **Cursor Clause** | **`sort`** | $\tau_{A \uparrow, B \downarrow}(R)$ | Controls the deterministic order of documents returned by a query. |
| **Cursor Clause** | **`limit`** | $\lambda_k(R)$ | Restricts the maximum number of documents returned by the cursor. |
| **Cursor Clause** | **`skip`** | $\delta_m(R)$ | Bypasses the first $m$ documents returned by the cursor (for pagination). |
| **Cursor Clause** | **`projection`** | $\pi_{A_1, A_2}(R)$ | Specifies or restricts fields to return, suppressing unneeded attributes and `_id`. |
| **Complex Type** | **`arrays`** | $v \in R.Array$ / $|R.Arr|=k$ | Operates on array attributes (`containment`, `$all`, `$size`, `$elemMatch`, index `.0`). |
| **Complex Type** | **`embedded docs`** | $R.SubDoc.Attr = v$ | Uses dot notation to query nested subdocuments (`_source_provenance`). |

---

## 3. Directory Layout & Database Allocations

The advanced query suite is organized into dedicated subdirectories per database alongside unified master execution files:

```
queries/advanced/
├── README.md                           <- Master Phase 19 Documentation & Syllabus Index
├── master_advanced_queries.js          <- Unified executable script covering all 5 databases
├── grammy_history_db/                  <- Member 1: Ceremonies, Telecasts, Venues, Ratings
│   ├── advanced_queries.js             <- Standalone executable JS query script
│   └── README.md                       <- Database-specific academic query documentation
├── grammy_categories_db/               <- Member 2: Categories, Fields, Restructuring Events
│   ├── advanced_queries.js             <- Standalone executable JS query script
│   └── README.md                       <- Database-specific academic query documentation
├── grammy_nominations_db/              <- Member 3: Nominations, Works, Ties, Classifications
│   ├── advanced_queries.js             <- Standalone executable JS query script
│   └── README.md                       <- Database-specific academic query documentation
├── grammy_winners_db/                  <- Member 4: Winners, Speeches, Streaks, Hall of Fame
│   ├── advanced_queries.js             <- Standalone executable JS query script
│   └── README.md                       <- Database-specific academic query documentation
└── grammy_creators_db/                 <- Member 5: Artists, Songwriters, Musical Groups
    ├── advanced_queries.js             <- Standalone executable JS query script
    └── README.md                       <- Database-specific academic query documentation
```

---

## 4. Query Demonstrations Across Databases

### 4.1 `grammy_history_db` (Member 1: History)
- **`$eq`**: Matches telecasts broadcast on CBS (`{ primary_network: { $eq: "CBS" } }`).
- **`$ne`**: Venues situated outside Los Angeles proper (`{ city: { $ne: "Los Angeles" } }`).
- **`$gt` & `$gte`**: Modern telecasts post-2010 (`$gt`) and viewership ratings $\ge 20.0$M (`$gte`).
- **`$lt` & `$lte`**: Early ceremonies before 1970 (`$lt`) and inaugural decade editions $\le 10$ (`$lte`).
- **`$in` & `$nin`**: Venue city set containment and network exclusions.
- **`$and`, `$or`, `$not`**: Multi-predicate broadcast queries and award total negations.
- **Cursor Methods**: Page 2 retrieval using `.sort({ broadcast_year: -1 }).skip(5).limit(5)`.
- **Embedded Documents**: Traversal of `_source_provenance.source_id` via dot notation.

### 4.2 `grammy_categories_db` (Member 2: Categories)
- **`$eq` & `$ne`**: General field categories vs genre craft categories.
- **`$gt` & `$gte`**: Fields with $>4$ categories and expanded slates $\ge 8$ nominees.
- **`$in` & `$nin`**: Core genre fields (Pop, Rock, R&B) vs specialized fields.
- **Arrays**:
  - **Containment**: Matching predecessor category ID in `source_category_ids`.
  - **`$all`**: Verifying presence of both male and female legacy IDs in restructured awards.
  - **`$size`**: Filtering consolidation events with exact array length of 2.
  - **Index `.0`**: Matching the first predecessor element in the array via dot notation.

### 4.3 `grammy_nominations_db` (Member 3: Nominations)
- **`$eq` & `$ne`**: Winning entries (`is_winner_flag: true`) vs non-winning finalists.
- **`$gt` & `$gte`**: Multi-nomination packages exceeding 4 nominations and modern 2020+ slates.
- **Arrays**:
  - **Containment**: Ballots containing specific nomination ID in `tied_nomination_ids`.
  - **`$all`**: Ballots containing multiple designated tied nominations simultaneously.
  - **`$size`**: Resolving ballots with exact slate size of 2 tied contenders.
  - **`$elemMatch`**: Querying `secondary_genre_tags` using regex patterns (`^Adult`).

### 4.4 `grammy_winners_db` (Member 4: Winners)
- **`$eq` & `$ne`**: Live telecast presentations and multi-statuette collaborative wins.
- **`$gt` & `$gte`**: Speeches exceeding 95 seconds and winning streaks spanning $\ge 3$ years.
- **Arrays**:
  - **Containment**: Speeches acknowledging "Family" in `individuals_acknowledged`.
  - **`$all`**: Speeches acknowledging both "Record Label" and "Fans".
  - **`$size`**: Speeches with exactly 4 acknowledged entities.
  - **Press Syndication**: Finding releases distributed via "Associated Press".

### 4.5 `grammy_creators_db` (Member 5: Creators/Music)
- **`$eq` & `$ne`**: US domestic artists vs international recording artists.
- **`$gt` & `$gte`**: Songwriters with $>120$ registered works and artists active from 1950.
- **`$in` & `$nin`**: PRO affiliations (ASCAP, BMI) and non-mainstream genre artists.
- **Compound Logic**: Solo artists debuted post-1950 (`$and`), active quartets (`$or`).

---

## 5. Execution & Verification

### 5.1 Automated Live Verification Script
To execute automated verification against MongoDB Atlas:

```bash
python scripts/advanced/run_all_advanced_queries.py
```

### 5.2 Automated Pytest Suite
To execute the comprehensive automated test suite (schema, documentation, live Atlas execution):

```bash
pytest tests/test_advanced_queries.py -v
```

### 5.3 Interactive MongoDB Shell (`mongosh`)
To run the full suite interactively via `mongosh`:

```bash
mongosh "$MONGODB_URI" queries/advanced/master_advanced_queries.js
```
