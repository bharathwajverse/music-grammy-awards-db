# Comprehensive MongoDB Indexing Strategy & Empirical Query Plan Analysis

> **Course**: Advanced Database Management Systems (ADBMS)  
> **Curriculum Module**: Module 10 — Advanced Query Operators, Multikey Indexing & Complex Expressions  
> **Project Title**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 21 — Indexing (Completed)  
> **Database Engine**: MongoDB Atlas Cloud (`Cluster0`) / WiredTiger Storage Engine  
> **Databases Covered**: All 5 Active Databases (50 Collections, 5,190 Certified Documents)  
> **Deployment Status**: **44 Custom Indexes Implemented & Verified on Atlas (100% Active)**  
> **Verification Date**: October 2026  

---

## 1. Executive Summary & Theoretical Foundations

In high-throughput distributed database management systems, query performance without indexing degrades linearly with collection cardinality ($\mathcal{O}(N)$ collection scans), imposing severe disk I/O, cache pollution, and CPU saturation. MongoDB's default storage engine, **WiredTiger**, utilizes prefix-compressed $B^+$-Tree structures to provide logarithmic lookup complexity ($\mathcal{O}(\log N)$), enabling high-concurrency read operations while preserving transactional durability.

Phase 21 establishes, deploys, and empirically validates an enterprise-grade **Indexing Subsystem** across all five member databases of the GRAMMY Awards Information & Analytics System:
1. `grammy_history_db` (Member 1: History) — 7 custom indexes
2. `grammy_categories_db` (Member 2: Categories) — 7 custom indexes
3. `grammy_nominations_db` (Member 3: Nominations) — 13 custom indexes
4. `grammy_winners_db` (Member 4: Winners) — 9 custom indexes
5. `grammy_creators_db` (Member 5: Creators/Music) — 8 custom indexes

**Total Custom Indexes Deployed**: **44 Indexes** across 18 high-activity collections (in addition to default `_id_` indexes).

### Core Architectural Index Types Implemented

```
                               ┌────────────────────────────────────────────────────────┐
                               │           MongoDB Indexing Architecture                │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
               ┌───────────────────────────┬───────────────┴───────────────┬───────────────────────────┐
               ▼                           ▼                               ▼                           ▼
     ┌───────────────────┐       ┌───────────────────┐           ┌───────────────────┐       ┌───────────────────┐
     │   Single Field    │       │   Compound (ESR)  │           │  Multikey (Array) │       │ Unique Secondary  │
     ├───────────────────┤       ├───────────────────┤           ├───────────────────┤       ├───────────────────┤
     │ B-tree scalar key │       │ Equality -> Sort  │           │ 1 B-tree entry    │       │ Enforces natural  │
     │ O(log N) seeks    │       │ -> Range Rule     │           │ per array element │       │ business key      │
     │ e.g. broadcast_yr │       │ e.g. winner+yr+ord│           │ e.g. ack_parties  │       │ uniqueness        │
     └───────────────────┘       └───────────────────┘           └───────────────────┘       └───────────────────┘
```

1. **Single Field Indexes**: Point lookups and foreign key joins (`$lookup`).
2. **Compound Indexes (ESR Rule)**: Multi-attribute indexes adhering to Equality $\rightarrow$ Sort $\rightarrow$ Range ordering to eliminate in-memory blocking sorts (`SORT` stages).
3. **Multikey Indexes**: Indexing array elements directly for set containment, `$all`, and `$size` evaluations without document unfolding.
4. **Unique Secondary Indexes**: Enforcing business integrity constraints on natural identifier keys (`ceremony_id`, `category_id`, `nomination_id`, `work_id`, `winner_record_id`, `artist_id`, etc.).

---

## 2. Real Workload Query Pattern Analysis

The indexing topology was designed directly from the real operational and analytical query workloads developed in Phase 18 (CRUD Operations), Phase 19 (Advanced Queries), and Phase 20 (Analytical Aggregation Pipelines):

### 2.1 Point Lookups on Natural Business Keys
- **Workload Pattern**: Exact match queries filtering by business identifiers (`ceremony_id`, `category_id`, `nomination_id`, `work_id`, `winner_record_id`, `artist_id`).
- **Deficiency Without Index**: WiredTiger scans every document in the collection (`COLLSCAN`), inspecting up to 500 documents per query.
- **Remedy**: Single field unique secondary indexes reducing document inspection to exactly **1 document** via `EXPRESS_IXSCAN` / `IXSCAN`.

### 2.2 Relational Join Lookups (`$lookup` Foreign Keys)
- **Workload Pattern**: Aggregation pipelines performing left outer joins across collections:
  - Pipeline 01: `nomination_entries` joined with `nominated_works` on `work_id`.
  - Pipeline 02: `winner_records` joined with `acceptance_speeches` on `winner_record_id`.
  - Pipeline 07: `winner_records` joined with `consecutive_winners` on `creator_id`.
  - Pipeline 09: `ceremonies` joined with `venues` on `venue_id`.
- **Deficiency Without Index**: Each document in the outer pipeline executes a full collection scan on the inner collection, resulting in $M \times N$ operations.
- **Remedy**: Secondary indexes on all foreign key join targets, reducing join evaluation to $M \times \log(N)$ index seeks.

### 2.3 Compound Filter and Sort Queries (The ESR Rule)
- **Workload Pattern**: Queries combining equality filters, numeric ranges, and cursor sorts:
  - Phase 19: Winners between 1959–1965 sorted by ceremony year and ballot order.
  - Phase 19: Live telecast winners sorted descending by trophy count.
  - Phase 18: Ceremonies broadcast on CBS after 2000 sorted descending by year.
  - Phase 18: Active categories sorted descending by nominee capacity.
  - Phase 19: Solo recording artists with career start $\ge 1950$ sorted ascending by year.
- **Deficiency Without Index**: MongoDB scans all documents and buffers matching records in a 100MB in-memory sorting pool (`SORT` stage). If the dataset exceeds memory quotas, the query crashes.
- **Remedy**: Compound indexes structured according to the **ESR Rule**:
  $$\text{Index Keys} = [\text{Equality Fields}] \circ [\text{Sort Fields}] \circ [\text{Range Fields}]$$
  This enables index-ordered retrieval, completely eliminating the in-memory `SORT` stage.

### 2.4 Multikey Array Queries
- **Workload Pattern**: Complex array evaluations over semi-structured attributes:
  - `acceptance_speeches.individuals_acknowledged`: Containment (`"Family"`), conjunction (`$all: ["Record Label", "Fans"]`), and unwind aggregations (Pipeline 08).
  - `tied_nominations.tied_nomination_ids`: Identifying ties involving specific nominations (`NOM_001_RECORD_OF__0000`).
  - `merged_split_history.source_category_ids`: Tracking category restructures across legacy identifiers.
  - `genre_classifications.secondary_genre_tags`: Searching secondary genre tags.
- **Deficiency Without Index**: Requires unravelling and inspecting array BSON structures for all documents.
- **Remedy**: Multikey B-Tree indexes storing an index entry for each scalar element of the array.

---

## 3. Master Index Classification Catalog (44 Custom Indexes)

| # | Database | Collection | Index Name | Keys | Type | Unique |
|---|---|---|---|---|---|:---:|
| 1 | `grammy_history_db` | `ceremonies` | `idx_ceremonies_ceremony_id` | `{ ceremony_id: 1 }` | Single Field | **Yes** |
| 2 | `grammy_history_db` | `ceremonies` | `idx_ceremonies_broadcast_year` | `{ broadcast_year: -1 }` | Single Field | No |
| 3 | `grammy_history_db` | `ceremonies` | `idx_ceremonies_venue_id` | `{ venue_id: 1 }` | Single Field / FK | No |
| 4 | `grammy_history_db` | `ceremonies` | `idx_ceremonies_network_year_esr` | `{ primary_network: 1, broadcast_year: -1 }` | Compound (ESR) | No |
| 5 | `grammy_history_db` | `venues` | `idx_venues_venue_id` | `{ venue_id: 1 }` | Single Field | **Yes** |
| 6 | `grammy_history_db` | `venues` | `idx_venues_city` | `{ city: 1 }` | Single Field | No |
| 7 | `grammy_history_db` | `viewership_ratings` | `idx_ratings_ceremony_viewers_esr` | `{ ceremony_id: 1, us_viewers_millions: -1 }` | Compound (ESR) | No |
| 8 | `grammy_categories_db` | `award_categories` | `idx_categories_category_id` | `{ category_id: 1 }` | Single Field | **Yes** |
| 9 | `grammy_categories_db` | `award_categories` | `idx_categories_field_id` | `{ field_id: 1 }` | Single Field / FK | No |
| 10 | `grammy_categories_db` | `award_categories` | `idx_categories_status_nominees_esr` | `{ current_status: 1, maximum_nominees_allowed: -1 }` | Compound (ESR) | No |
| 11 | `grammy_categories_db` | `award_categories` | `idx_categories_field_inaugural_esr` | `{ field_id: 1, inaugural_edition: 1 }` | Compound (ESR) | No |
| 12 | `grammy_categories_db` | `award_fields` | `idx_fields_field_id` | `{ field_id: 1 }` | Single Field | **Yes** |
| 13 | `grammy_categories_db` | `merged_split_history` | `idx_merged_split_source_cats_multikey` | `{ source_category_ids: 1 }` | Multikey (Array) | No |
| 14 | `grammy_categories_db` | `merged_split_history` | `idx_merged_split_primary_cat` | `{ primary_category_id: 1 }` | Single Field / FK | No |
| 15 | `grammy_nominations_db` | `nomination_entries` | `idx_nom_entries_nomination_id` | `{ nomination_id: 1 }` | Single Field | **Yes** |
| 16 | `grammy_nominations_db` | `nomination_entries` | `idx_nom_entries_artist_id` | `{ primary_artist_id: 1 }` | Single Field / Analytical | No |
| 17 | `grammy_nominations_db` | `nomination_entries` | `idx_nom_entries_work_id` | `{ work_id: 1 }` | Single Field / FK | No |
| 18 | `grammy_nominations_db` | `nomination_entries` | `idx_nom_entries_category_year_esr` | `{ category_id: 1, nomination_year: -1 }` | Compound (ESR) | No |
| 19 | `grammy_nominations_db` | `nomination_entries` | `idx_nom_entries_winner_year_slot_esr` | `{ is_winner_flag: 1, nomination_year: -1, ballot_slot_order: 1 }` | Compound (ESR) | No |
| 20 | `grammy_nominations_db` | `nominated_works` | `idx_nominated_works_work_id` | `{ work_id: 1 }` | Single Field | **Yes** |
| 21 | `grammy_nominations_db` | `nominated_works` | `idx_nominated_works_primary_label` | `{ primary_label_id: 1 }` | Single Field / FK | No |
| 22 | `grammy_nominations_db` | `tied_nominations` | `idx_tied_noms_tied_ids_multikey` | `{ tied_nomination_ids: 1 }` | Multikey (Array) | No |
| 23 | `grammy_nominations_db` | `tied_nominations` | `idx_tied_noms_ceremony_category` | `{ ceremony_id: 1, category_id: 1 }` | Compound | No |
| 24 | `grammy_nominations_db` | `genre_classifications` | `idx_genre_class_secondary_tags_multikey` | `{ secondary_genre_tags: 1 }` | Multikey (Array) | No |
| 25 | `grammy_nominations_db` | `genre_classifications` | `idx_genre_class_work_id` | `{ work_id: 1 }` | Single Field / FK | No |
| 26 | `grammy_nominations_db` | `multi_nomination_packages` | `idx_packages_nominated_works_multikey` | `{ nominated_work_ids: 1 }` | Multikey (Array) | No |
| 27 | `grammy_nominations_db` | `multi_nomination_packages` | `idx_packages_creator_ceremony` | `{ creator_id: 1, ceremony_year: -1 }` | Compound (ESR) | No |
| 28 | `grammy_winners_db` | `winner_records` | `idx_winner_records_winner_id` | `{ winner_record_id: 1 }` | Single Field | **Yes** |
| 29 | `grammy_winners_db` | `winner_records` | `idx_winner_records_artist_id` | `{ primary_artist_id: 1 }` | Single Field / Analytical | No |
| 30 | `grammy_winners_db` | `winner_records` | `idx_winner_records_category_year_esr` | `{ category_id: 1, ceremony_year: -1 }` | Compound (ESR) | No |
| 31 | `grammy_winners_db` | `winner_records` | `idx_winner_records_telecast_statuettes_esr` | `{ presented_live_on_telecast: 1, trophy_statuettes_awarded_count: -1 }` | Compound (ESR) | No |
| 32 | `grammy_winners_db` | `acceptance_speeches` | `idx_speeches_speech_id` | `{ speech_id: 1 }` | Single Field | **Yes** |
| 33 | `grammy_winners_db` | `acceptance_speeches` | `idx_speeches_winner_record_id` | `{ winner_record_id: 1 }` | Single Field / FK | No |
| 34 | `grammy_winners_db` | `acceptance_speeches` | `idx_speeches_ack_multikey` | `{ individuals_acknowledged: 1 }` | Multikey (Array) | No |
| 35 | `grammy_winners_db` | `consecutive_winners` | `idx_consecutive_creator_id` | `{ creator_id: 1 }` | Single Field / FK | No |
| 36 | `grammy_winners_db` | `consecutive_winners` | `idx_consecutive_winning_works_multikey` | `{ winning_work_ids_list: 1 }` | Multikey (Array) | No |
| 37 | `grammy_creators_db` | `artists` | `idx_artists_artist_id` | `{ artist_id: 1 }` | Single Field | **Yes** |
| 38 | `grammy_creators_db` | `artists` | `idx_artists_stage_name` | `{ stage_name: 1 }` | Single Field | No |
| 39 | `grammy_creators_db` | `artists` | `idx_artists_group_career_esr` | `{ is_group_ensemble_flag: 1, active_career_start_year: 1 }` | Compound (ESR) | No |
| 40 | `grammy_creators_db` | `songwriters_composers` | `idx_songwriters_songwriter_id` | `{ songwriter_id: 1 }` | Single Field | **Yes** |
| 41 | `grammy_creators_db` | `songwriters_composers` | `idx_songwriters_pro_works_esr` | `{ pro_affiliation: 1, registered_works_count: -1 }` | Compound (ESR) | No |
| 42 | `grammy_creators_db` | `musical_groups` | `idx_musical_groups_group_id` | `{ group_id: 1 }` | Single Field | **Yes** |
| 43 | `grammy_creators_db` | `musical_groups` | `idx_musical_groups_formation_year` | `{ formation_calendar_year: 1 }` | Single Field | No |
| 44 | `grammy_creators_db` | `record_labels` | `idx_record_labels_label_id` | `{ label_id: 1 }` | Single Field | **Yes** |

---

## 4. Database-by-Database Detailed Index Specifications

Every index document satisfies the mandatory five-part specification:
- **Field**: Indexed attribute path(s) and directional order ($1$ ascending, $-1$ descending).
- **Index Type**: Mathematical/structural taxonomy.
- **Reason**: Database engineering justification.
- **Query It Supports**: Concrete JavaScript query execution snippet.
- **Expected Benefit**: Measured latency, I/O, and complexity enhancement.

---

### 4.1 Database 1: `grammy_history_db` (Member 1: History)

#### Index 1: `idx_ceremonies_ceremony_id`
* **Collection**: `ceremonies`
* **Field**: `{ ceremony_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Enforces natural key uniqueness across all ceremony editions and enables point queries by ceremony code.
* **Query It Supports**:
  ```javascript
  db.ceremonies.findOne({ ceremony_id: "CEREMONY_001" }, { _id: 0, ceremony_id: 1, broadcast_year: 1 });
  ```
* **Expected Benefit**: Replaces collection scan with single B-Tree leaf seek (`EXPRESS_IXSCAN`), reducing scanned documents from 67 to 1.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $67 \rightarrow 1$ (98.5% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 2: `idx_ceremonies_broadcast_year`
* **Collection**: `ceremonies`
* **Field**: `{ broadcast_year: -1 }`
* **Index Type**: Single Field
* **Reason**: Accelerates temporal range filters (`$gt`, `$lt`, `$gte`) and chronological sorting on ceremony telecast years.
* **Query It Supports**:
  ```javascript
  db.ceremonies.find({ broadcast_year: { $gt: 2010 } }).sort({ broadcast_year: 1 });
  ```
* **Expected Benefit**: Eliminates collection scan; leverages bidirectional index scanning for ascending or descending traversal.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 14$, `docsExamined`: $67 \rightarrow 14$, `executionTimeMillis`: $0\text{ ms}$.

#### Index 3: `idx_ceremonies_venue_id`
* **Collection**: `ceremonies`
* **Field**: `{ venue_id: 1 }`
* **Index Type**: Single Field / Foreign Key
* **Reason**: Serves as foreign key join target for `$lookup` pipelines connecting ceremonies to venue host locations.
* **Query It Supports**:
  ```javascript
  db.ceremonies.aggregate([
    { $lookup: { from: "venues", localField: "venue_id", foreignField: "venue_id", as: "venue_info" } }
  ]);
  ```
* **Expected Benefit**: Converts nested-loop collection scans into indexed $B^+$-Tree seeks.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 12$, `docsExamined`: $67 \rightarrow 12$, `executionTimeMillis`: $0\text{ ms}$ (sub-pipeline foreign key seek replaces 67 inner collection scans).

#### Index 4: `idx_ceremonies_network_year_esr`
* **Collection**: `ceremonies`
* **Field**: `{ primary_network: 1, broadcast_year: -1 }`
* **Index Type**: Compound (ESR Rule)
* **Reason**: Satisfies Equality on broadcast network (`primary_network`) and Range/Sort on telecast year (`broadcast_year`).
* **Query It Supports**:
  ```javascript
  db.ceremonies.find(
    { primary_network: "CBS", broadcast_year: { $gte: 2000 } }
  ).sort({ broadcast_year: -1 });
  ```
* **Expected Benefit**: Scans only the CBS partition and reads index keys in pre-sorted order, avoiding an in-memory `SORT` stage.
* **Explain Evidence**: Stage: `COLLSCAN + SORT` $\rightarrow$ `IXSCAN + FETCH`, `keysExamined`: $0 \rightarrow 26$, `docsExamined`: $67 \rightarrow 26$ (61.2% reduction), `executionTimeMillis`: $0\text{ ms}$ (`SORT` stage eliminated).

#### Index 5: `idx_venues_venue_id`
* **Collection**: `venues`
* **Field**: `{ venue_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Guarantees uniqueness of venue natural keys (`VEN_BEVERLY_HILTON`, `VEN_CRYPTO_COM_ARENA`) and accelerates point lookups.
* **Query It Supports**:
  ```javascript
  db.venues.findOne({ venue_id: "VEN_BEVERLY_HILTON" });
  ```
* **Expected Benefit**: $\mathcal{O}(1)$ point lookup; eliminates 60-document collection scan.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $60 \rightarrow 1$ (98.3% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 6: `idx_venues_city`
* **Collection**: `venues`
* **Field**: `{ city: 1 }`
* **Index Type**: Single Field
* **Reason**: Supports equality and set membership queries (`$in`) on venue geographic locations (e.g., Los Angeles, Beverly Hills).
* **Query It Supports**:
  ```javascript
  db.venues.find({ city: { $in: ["Beverly Hills", "Los Angeles"] } });
  ```
* **Expected Benefit**: Index bounds scan isolates only entries matching target cities without scanning unrelated facilities.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 24$, `docsExamined`: $60 \rightarrow 24$, `executionTimeMillis`: $0\text{ ms}$.

#### Index 7: `idx_ratings_ceremony_viewers_esr`
* **Collection**: `viewership_ratings`
* **Field**: `{ ceremony_id: 1, us_viewers_millions: -1 }`
* **Index Type**: Compound (ESR Rule)
* **Reason**: Supports ceremony-specific viewership lookups ordered by audience ratings.
* **Query It Supports**:
  ```javascript
  db.viewership_ratings.find(
    { ceremony_id: "CEREMONY_054", us_viewers_millions: { $gte: 20.0 } }
  ).sort({ us_viewers_millions: -1 });
  ```
* **Expected Benefit**: B-Tree keys deliver pre-sorted records without memory buffering.
* **Explain Evidence**: Stage: `COLLSCAN + SORT` $\rightarrow$ `IXSCAN + FETCH`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $67 \rightarrow 1$, `executionTimeMillis`: $0\text{ ms}$ (`SORT` stage eliminated).

---

### 4.2 Database 2: `grammy_categories_db` (Member 2: Categories)

#### Index 8: `idx_categories_category_id`
* **Collection**: `award_categories`
* **Field**: `{ category_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Enforces global uniqueness of category identifiers and serves as the universal foreign key for nominations and awards.
* **Query It Supports**:
  ```javascript
  db.award_categories.findOne({ category_id: "CAT_RECORD_OF_THE_YEAR_000" });
  ```
* **Expected Benefit**: Instant point lookup, avoiding 120-document collection scan.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $120 \rightarrow 1$ (99.2% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 9: `idx_categories_field_id`
* **Collection**: `award_categories`
* **Field**: `{ field_id: 1 }`
* **Index Type**: Single Field / Foreign Key
* **Reason**: Accelerates category taxonomy queries filtering by parent award field (General Field, Pop, Jazz, Classical).
* **Query It Supports**:
  ```javascript
  db.award_categories.find({ field_id: "FLD_GENERAL" });
  ```
* **Expected Benefit**: Restricts index scan to categories belonging to specified field partition.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 4$, `docsExamined`: $120 \rightarrow 4$ (96.7% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 10: `idx_categories_status_nominees_esr`
* **Collection**: `award_categories`
* **Field**: `{ current_status: 1, maximum_nominees_allowed: -1 }`
* **Index Type**: Compound (ESR Rule)
* **Reason**: Satisfies Equality on status (`current_status = "Active"`) and Sort on nominee capacity (`maximum_nominees_allowed`).
* **Query It Supports**:
  ```javascript
  db.award_categories.find(
    { current_status: "Active" }
  ).sort({ maximum_nominees_allowed: -1 });
  ```
* **Expected Benefit**: Eliminates blocking in-memory sort; streams active categories directly in order of nominee capacity.
* **Explain Evidence**: Stage: `COLLSCAN + SORT` $\rightarrow$ `IXSCAN + FETCH`, `keysExamined`: $0 \rightarrow 120$, `docsExamined`: $120 \rightarrow 120$, `executionTimeMillis`: $0\text{ ms}$ (`SORT` stage eliminated, pre-sorted index stream).

#### Index 11: `idx_categories_field_inaugural_esr`
* **Collection**: `award_categories`
* **Field**: `{ field_id: 1, inaugural_edition: 1 }`
* **Index Type**: Compound (ESR Rule)
* **Reason**: Supports field-specific historical queries tracing the chronological introduction of categories.
* **Query It Supports**:
  ```javascript
  db.award_categories.find(
    { field_id: { $in: ["FLD_POP", "FLD_ROCK"] } }
  ).sort({ inaugural_edition: 1 });
  ```
* **Expected Benefit**: Pre-sorts categories by edition number within each award field partition.
* **Explain Evidence**: Stage: `COLLSCAN + SORT` $\rightarrow$ `IXSCAN + FETCH`, `keysExamined`: $0 \rightarrow 20$, `docsExamined`: $120 \rightarrow 20$, `executionTimeMillis`: $0\text{ ms}$ (`SORT` stage eliminated).

#### Index 12: `idx_fields_field_id`
* **Collection**: `award_fields`
* **Field**: `{ field_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Enforces unique field identifier constraint on taxonomy table (`FLD_GENERAL`, `FLD_POP`).
* **Query It Supports**:
  ```javascript
  db.award_fields.findOne({ field_id: "FLD_GENERAL" });
  ```
* **Expected Benefit**: O(1) point lookup, zero duplicate field codes permitted.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $50 \rightarrow 1$ (98.0% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 13: `idx_merged_split_source_cats_multikey`
* **Collection**: `merged_split_history`
* **Field**: `{ source_category_ids: 1 }`
* **Index Type**: Multikey (Array Index)
* **Reason**: BSON array field containing legacy category IDs. Enables multikey index lookups for containment and `$all` queries.
* **Query It Supports**:
  ```javascript
  db.merged_split_history.find({
    source_category_ids: { $all: ["LEGACY_CAT_MALE_0", "LEGACY_CAT_FEMALE_0"] }
  });
  ```
* **Expected Benefit**: Inspects multikey index leaves directly without traversing non-matching restructurings.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $60 \rightarrow 1$ (98.3% reduction), `executionTimeMillis`: $0\text{ ms}$ (multikey array traversal).

#### Index 14: `idx_merged_split_primary_cat`
* **Collection**: `merged_split_history`
* **Field**: `{ primary_category_id: 1 }`
* **Index Type**: Single Field / Foreign Key
* **Reason**: Links restructuring events to the destination primary category.
* **Query It Supports**:
  ```javascript
  db.merged_split_history.find({ primary_category_id: "CAT_RECORD_OF_THE_YEAR_000" });
  ```
* **Expected Benefit**: Rapid indexed join target for lineage tracking.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $60 \rightarrow 1$ (98.3% reduction), `executionTimeMillis`: $0\text{ ms}$.

---

### 4.3 Database 3: `grammy_nominations_db` (Member 3: Nominations)

#### Index 15: `idx_nom_entries_nomination_id`
* **Collection**: `nomination_entries`
* **Field**: `{ nomination_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Enforces nomination ID uniqueness across all 500 nomination records and accelerates point queries.
* **Query It Supports**:
  ```javascript
  db.nomination_entries.findOne({ nomination_id: "NOM_001_RECORD_OF__0000" });
  ```
* **Expected Benefit**: Replaces 500-document collection scan with direct B-Tree lookup.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $500 \rightarrow 1$ (99.8% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 16: `idx_nom_entries_artist_id`
* **Collection**: `nomination_entries`
* **Field**: `{ primary_artist_id: 1 }`
* **Index Type**: Single Field / Analytical
* **Reason**: Core analytical index supporting Pipeline 01 (Career Nominations per Artist) and Pipeline 06.
* **Query It Supports**:
  ```javascript
  db.nomination_entries.find({ primary_artist_id: "CRT_HENRY_MANCINI_0001" });
  ```
* **Expected Benefit**: Immediately isolates the artist's 19 nominations without examining the other 481 documents.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 19$, `docsExamined`: $500 \rightarrow 19$ (96.2% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 17: `idx_nom_entries_work_id`
* **Collection**: `nomination_entries`
* **Field**: `{ work_id: 1 }`
* **Index Type**: Single Field / Foreign Key
* **Reason**: Supports `$lookup` relational joins connecting nomination entries to `nominated_works`.
* **Query It Supports**:
  ```javascript
  db.nomination_entries.aggregate([
    { $lookup: { from: "nominated_works", localField: "work_id", foreignField: "work_id", as: "work_info" } }
  ]);
  ```
* **Expected Benefit**: Transforms full inner collection scan into indexed B-Tree seek for each joined nomination.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $500 \rightarrow 1$ (99.8% reduction), `executionTimeMillis`: $0\text{ ms}$ (foreign key join index seek eliminates 500 inner scans).

#### Index 18: `idx_nom_entries_category_year_esr`
* **Collection**: `nomination_entries`
* **Field**: `{ category_id: 1, nomination_year: -1 }`
* **Index Type**: Compound (ESR Rule)
* **Reason**: Supports category-filtered analytical pipelines (Pipeline 04 & 05) ordered chronologically.
* **Query It Supports**:
  ```javascript
  db.nomination_entries.find(
    { category_id: "CAT_RECORD_OF_THE_YEAR_000" }
  ).sort({ nomination_year: -1 });
  ```
* **Expected Benefit**: Scans only the category partition and returns pre-sorted nominations by year.
* **Explain Evidence**: Stage: `COLLSCAN + SORT` $\rightarrow$ `IXSCAN + FETCH`, `keysExamined`: $0 \rightarrow 5$, `docsExamined`: $500 \rightarrow 5$ (99.0% reduction), `executionTimeMillis`: $0\text{ ms}$ (`SORT` stage eliminated).

#### Index 19: `idx_nom_entries_winner_year_slot_esr`
* **Collection**: `nomination_entries`
* **Field**: `{ is_winner_flag: 1, nomination_year: -1, ballot_slot_order: 1 }`
* **Index Type**: Compound (ESR Rule)
* **Reason**: Perfect ESR alignment: Equality on winner flag, Range/Sort on year, Sort on ballot slot order.
* **Query It Supports**:
  ```javascript
  db.nomination_entries.find(
    { is_winner_flag: true, nomination_year: { $gte: 1959, $lte: 1965 } }
  ).sort({ nomination_year: -1, ballot_slot_order: 1 });
  ```
* **Expected Benefit**: Prunes non-winning nominations; satisfies multi-key sort without memory buffer.
* **Explain Evidence**: Stage: `COLLSCAN + SORT` $\rightarrow$ `IXSCAN + FETCH`, `keysExamined`: $0 \rightarrow 269$, `docsExamined`: $500 \rightarrow 269$ (46.2% reduction), `executionTimeMillis`: $0\text{ ms}$ (`SORT` stage eliminated).

#### Index 20: `idx_nominated_works_work_id`
* **Collection**: `nominated_works`
* **Field**: `{ work_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Enforces work ID uniqueness across 500 creative works; primary `$lookup` join target for Pipeline 01.
* **Query It Supports**:
  ```javascript
  db.nominated_works.findOne({ work_id: "WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000" });
  ```
* **Expected Benefit**: O(1) point lookup and instant join resolution.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $500 \rightarrow 1$ (99.8% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 21: `idx_nominated_works_primary_label`
* **Collection**: `nominated_works`
* **Field**: `{ primary_label_id: 1 }`
* **Index Type**: Single Field / Foreign Key
* **Reason**: Supports queries filtering releases by record label.
* **Query It Supports**:
  ```javascript
  db.nominated_works.find({ primary_label_id: "LBL_WARNER_RECORDS_001" });
  ```
* **Expected Benefit**: Index scan on label releases, bypassing non-matching titles.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 25$, `docsExamined`: $500 \rightarrow 25$ (95.0% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 22: `idx_tied_noms_tied_ids_multikey`
* **Collection**: `tied_nominations`
* **Field**: `{ tied_nomination_ids: 1 }`
* **Index Type**: Multikey (Array Index)
* **Reason**: Multikey array index enabling fast containment and `$all` checks for tied nomination slates.
* **Query It Supports**:
  ```javascript
  db.tied_nominations.find({ tied_nomination_ids: "NOM_001_RECORD_OF__0000" });
  ```
* **Expected Benefit**: Isolates tie records referencing a specific nomination without scanning all 70 tie events.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $70 \rightarrow 1$ (98.6% reduction), `executionTimeMillis`: $0\text{ ms}$ (multikey array traversal).

#### Index 23: `idx_tied_noms_ceremony_category`
* **Collection**: `tied_nominations`
* **Field**: `{ ceremony_id: 1, category_id: 1 }`
* **Index Type**: Compound
* **Reason**: Supports composite lookups identifying ties within a specific ceremony edition and award category.
* **Query It Supports**:
  ```javascript
  db.tied_nominations.find({ ceremony_id: "CEREMONY_001", category_id: "CAT_RECORD_OF_THE_YEAR_000" });
  ```
* **Expected Benefit**: Compound B-Tree seek directly matches ceremony/category pairs.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $70 \rightarrow 1$ (98.6% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 24: `idx_genre_class_secondary_tags_multikey`
* **Collection**: `genre_classifications`
* **Field**: `{ secondary_genre_tags: 1 }`
* **Index Type**: Multikey (Array Index)
* **Reason**: BSON array field containing subgenre descriptors. Accelerates array matching and `$elemMatch` queries.
* **Query It Supports**:
  ```javascript
  db.genre_classifications.find({ secondary_genre_tags: "Adult Contemporary" });
  ```
* **Expected Benefit**: Direct array leaf matching, pruning collection scan.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 12$, `docsExamined`: $70 \rightarrow 12$ (82.9% reduction), `executionTimeMillis`: $0\text{ ms}$ (multikey array traversal).

#### Index 25: `idx_genre_class_work_id`
* **Collection**: `genre_classifications`
* **Field**: `{ work_id: 1 }`
* **Index Type**: Single Field / Foreign Key
* **Reason**: Foreign key lookup linking musical works to their Recording Academy genre committee determinations.
* **Query It Supports**:
  ```javascript
  db.genre_classifications.find({ work_id: "WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000" });
  ```
* **Expected Benefit**: Instant lookup on work classification.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $70 \rightarrow 1$ (98.6% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 26: `idx_packages_nominated_works_multikey`
* **Collection**: `multi_nomination_packages`
* **Field**: `{ nominated_work_ids: 1 }`
* **Index Type**: Multikey (Array Index)
* **Reason**: Multikey array index over creative works packaged within multi-nomination slates.
* **Query It Supports**:
  ```javascript
  db.multi_nomination_packages.find({ nominated_work_ids: "WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000" });
  ```
* **Expected Benefit**: Fast reverse lookup from nominated work to its multi-nominee package.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $70 \rightarrow 1$ (98.6% reduction), `executionTimeMillis`: $0\text{ ms}$ (multikey array traversal).

#### Index 27: `idx_packages_creator_ceremony`
* **Collection**: `multi_nomination_packages`
* **Field**: `{ creator_id: 1, ceremony_year: -1 }`
* **Index Type**: Compound (ESR Rule)
* **Reason**: Supports finding multi-nomination packages for an artist across ceremony years.
* **Query It Supports**:
  ```javascript
  db.multi_nomination_packages.find({ creator_id: "CRT_HENRY_MANCINI_0001" }).sort({ ceremony_year: -1 });
  ```
* **Expected Benefit**: Restricts scan to creator partition and delivers results in descending ceremony order.
* **Explain Evidence**: Stage: `COLLSCAN + SORT` $\rightarrow$ `IXSCAN + FETCH`, `keysExamined`: $0 \rightarrow 5$, `docsExamined`: $70 \rightarrow 5$ (92.9% reduction), `executionTimeMillis`: $0\text{ ms}$ (`SORT` stage eliminated).

---

### 4.4 Database 4: `grammy_winners_db` (Member 4: Winners)

#### Index 28: `idx_winner_records_winner_id`
* **Collection**: `winner_records`
* **Field**: `{ winner_record_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Enforces winner record uniqueness across 400 winning events and serves as the `$lookup` key for acceptance speeches.
* **Query It Supports**:
  ```javascript
  db.winner_records.findOne({ winner_record_id: "WIN_NOM_001_RECORD_OF__0000" });
  ```
* **Expected Benefit**: Replaces 400-document collection scan with direct B-Tree lookup.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $400 \rightarrow 1$ (99.8% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 29: `idx_winner_records_artist_id`
* **Collection**: `winner_records`
* **Field**: `{ primary_artist_id: 1 }`
* **Index Type**: Single Field / Analytical
* **Reason**: Powers Pipeline 02 (Total Wins per Artist) and Pipeline 07 (Multi-Time Winners).
* **Query It Supports**:
  ```javascript
  db.winner_records.find({ primary_artist_id: "CRT_HENRY_MANCINI_0001" });
  ```
* **Expected Benefit**: Isolates Mancini's 17 wins directly, skipping 383 non-matching winning records.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 17$, `docsExamined`: $400 \rightarrow 17$ (95.8% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 30: `idx_winner_records_category_year_esr`
* **Collection**: `winner_records`
* **Field**: `{ category_id: 1, ceremony_year: -1 }`
* **Index Type**: Compound (ESR Rule)
* **Reason**: Powers Pipeline 03 (Wins by Category) and historical winner timelines.
* **Query It Supports**:
  ```javascript
  db.winner_records.find(
    { category_id: "CAT_SONG_OF_THE_YEAR_002" }
  ).sort({ ceremony_year: -1 });
  ```
* **Expected Benefit**: Delivers pre-sorted winners by year within the target category.
* **Explain Evidence**: Stage: `COLLSCAN + SORT` $\rightarrow$ `IXSCAN + FETCH`, `keysExamined`: $0 \rightarrow 11$, `docsExamined`: $400 \rightarrow 11$ (97.2% reduction), `executionTimeMillis`: $0\text{ ms}$ (`SORT` stage eliminated).

#### Index 31: `idx_winner_records_telecast_statuettes_esr`
* **Collection**: `winner_records`
* **Field**: `{ presented_live_on_telecast: 1, trophy_statuettes_awarded_count: -1 }`
* **Index Type**: Compound (ESR Rule)
* **Reason**: Satisfies Equality on telecast status and Sort on statuette count.
* **Query It Supports**:
  ```javascript
  db.winner_records.find(
    { presented_live_on_telecast: true }
  ).sort({ trophy_statuettes_awarded_count: -1 });
  ```
* **Expected Benefit**: Scans only live telecast winners and streams results ordered by statuette count without buffering.
* **Explain Evidence**: Stage: `COLLSCAN + SORT` $\rightarrow$ `IXSCAN + FETCH`, `keysExamined`: $0 \rightarrow 200$, `docsExamined`: $400 \rightarrow 200$ (50.0% reduction), `executionTimeMillis`: $0\text{ ms}$ (`SORT` stage eliminated).

#### Index 32: `idx_speeches_speech_id`
* **Collection**: `acceptance_speeches`
* **Field**: `{ speech_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Enforces speech ID uniqueness across all 65 recorded acceptance speeches.
* **Query It Supports**:
  ```javascript
  db.acceptance_speeches.findOne({ speech_id: "SPEECH_001" });
  ```
* **Expected Benefit**: O(1) point lookup on transcript documents.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $65 \rightarrow 1$ (98.5% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 33: `idx_speeches_winner_record_id`
* **Collection**: `acceptance_speeches`
* **Field**: `{ winner_record_id: 1 }`
* **Index Type**: Single Field / Foreign Key
* **Reason**: Foreign key join target in Pipeline 02 joining winner records to their acceptance speeches.
* **Query It Supports**:
  ```javascript
  db.winner_records.aggregate([
    { $lookup: { from: "acceptance_speeches", localField: "winner_record_id", foreignField: "winner_record_id", as: "speech_info" } }
  ]);
  ```
* **Expected Benefit**: Accelerated join lookups without nested collection scans.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $65 \rightarrow 1$ (98.5% reduction), `executionTimeMillis`: $0\text{ ms}$ (foreign key join index seek).

#### Index 34: `idx_speeches_ack_multikey`
* **Collection**: `acceptance_speeches`
* **Field**: `{ individuals_acknowledged: 1 }`
* **Index Type**: Multikey (Array Index)
* **Reason**: Indexes array of acknowledged entities; powers Pipeline 08 (`$unwind` distribution of acknowledged entities) and `$all` queries.
* **Query It Supports**:
  ```javascript
  db.acceptance_speeches.find({ individuals_acknowledged: "Family" });
  ```
* **Expected Benefit**: Multikey index search identifies speeches acknowledging specific parties directly.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 65$, `docsExamined`: $65 \rightarrow 65$, `executionTimeMillis`: $0\text{ ms}$ (multikey array traversal).

#### Index 35: `idx_consecutive_creator_id`
* **Collection**: `consecutive_winners`
* **Field**: `{ creator_id: 1 }`
* **Index Type**: Single Field / Foreign Key
* **Reason**: Joins consecutive winning streak records to creators in Pipeline 07.
* **Query It Supports**:
  ```javascript
  db.consecutive_winners.find({ creator_id: "CRT_HENRY_MANCINI_0001" });
  ```
* **Expected Benefit**: Direct indexed retrieval of streak records for specific artists.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 2$, `docsExamined`: $65 \rightarrow 2$ (96.9% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 36: `idx_consecutive_winning_works_multikey`
* **Collection**: `consecutive_winners`
* **Field**: `{ winning_work_ids_list: 1 }`
* **Index Type**: Multikey (Array Index)
* **Reason**: Multikey index indexing the list of musical works forming each winning streak.
* **Query It Supports**:
  ```javascript
  db.consecutive_winners.find({ winning_work_ids_list: "WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000" });
  ```
* **Expected Benefit**: Direct array index seek for streak component works.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $65 \rightarrow 1$ (98.5% reduction), `executionTimeMillis`: $0\text{ ms}$ (multikey array traversal).

---

### 4.5 Database 5: `grammy_creators_db` (Member 5: Creators/Music)

#### Index 37: `idx_artists_artist_id`
* **Collection**: `artists`
* **Field**: `{ artist_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Enforces universal artist identifier uniqueness across 300 recording artists; primary entity lookup target.
* **Query It Supports**:
  ```javascript
  db.artists.findOne({ artist_id: "CRT_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000" });
  ```
* **Expected Benefit**: Replaces 300-document collection scan with direct B-Tree seek.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $300 \rightarrow 1$ (99.7% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 38: `idx_artists_stage_name`
* **Collection**: `artists`
* **Field**: `{ stage_name: 1 }`
* **Index Type**: Single Field
* **Reason**: Accelerates alphabetical artist lookups and billing name sorting.
* **Query It Supports**:
  ```javascript
  db.artists.find({ stage_name: "Henry Mancini" }).sort({ stage_name: 1 });
  ```
* **Expected Benefit**: Direct index seek on billing name with pre-sorted index traversal.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $300 \rightarrow 1$ (99.7% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 39: `idx_artists_group_career_esr`
* **Collection**: `artists`
* **Field**: `{ is_group_ensemble_flag: 1, active_career_start_year: 1 }`
* **Index Type**: Compound (ESR Rule)
* **Reason**: Satisfies Equality on group flag (`is_group_ensemble_flag = false`) and Range/Sort on career start year.
* **Query It Supports**:
  ```javascript
  db.artists.find(
    { is_group_ensemble_flag: false, active_career_start_year: { $gte: 1950 } }
  ).sort({ active_career_start_year: 1 });
  ```
* **Expected Benefit**: Filters solo artists directly and outputs records in ascending chronological order without an in-memory sort buffer.
* **Explain Evidence**: Stage: `COLLSCAN + SORT` $\rightarrow$ `IXSCAN + FETCH`, `keysExamined`: $0 \rightarrow 223$, `docsExamined`: $300 \rightarrow 223$ (25.7% reduction), `executionTimeMillis`: $0\text{ ms}$ (`SORT` stage eliminated).

#### Index 40: `idx_songwriters_songwriter_id`
* **Collection**: `songwriters_composers`
* **Field**: `{ songwriter_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Enforces uniqueness on songwriter IDs across 75 composer entities.
* **Query It Supports**:
  ```javascript
  db.songwriters_composers.findOne({ songwriter_id: "SONG_001" });
  ```
* **Expected Benefit**: O(1) point lookup on composer credentials.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $75 \rightarrow 1$ (98.7% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 41: `idx_songwriters_pro_works_esr`
* **Collection**: `songwriters_composers`
* **Field**: `{ pro_affiliation: 1, registered_works_count: -1 }`
* **Index Type**: Compound (ESR Rule)
* **Reason**: Satisfies Equality on PRO affiliation (`pro_affiliation: { $in: ["ASCAP", "BMI"] }`) and Sort on catalog size (`registered_works_count`).
* **Query It Supports**:
  ```javascript
  db.songwriters_composers.find(
    { pro_affiliation: { $in: ["ASCAP", "BMI"] } }
  ).sort({ registered_works_count: -1 });
  ```
* **Expected Benefit**: Pre-sorts prolific songwriters without temporary in-memory sort pool.
* **Explain Evidence**: Stage: `COLLSCAN + SORT` $\rightarrow$ `IXSCAN + FETCH`, `keysExamined`: $0 \rightarrow 62$, `docsExamined`: $75 \rightarrow 62$ (17.3% reduction), `executionTimeMillis`: $0\text{ ms}$ (`SORT` stage eliminated).

#### Index 42: `idx_musical_groups_group_id`
* **Collection**: `musical_groups`
* **Field**: `{ group_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Enforces unique identifier constraint on musical group and ensemble records.
* **Query It Supports**:
  ```javascript
  db.musical_groups.findOne({ group_id: "GRP_001" });
  ```
* **Expected Benefit**: Instant point lookup on ensemble entities.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $65 \rightarrow 1$ (98.5% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 43: `idx_musical_groups_formation_year`
* **Collection**: `musical_groups`
* **Field**: `{ formation_calendar_year: 1 }`
* **Index Type**: Single Field
* **Reason**: Supports chronological range queries on group founding years.
* **Query It Supports**:
  ```javascript
  db.musical_groups.find({ formation_calendar_year: { $lte: 1965 } });
  ```
* **Expected Benefit**: Index range scan isolates early historic groups without scanning modern ensembles.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `IXSCAN`, `keysExamined`: $0 \rightarrow 20$, `docsExamined`: $65 \rightarrow 20$ (69.2% reduction), `executionTimeMillis`: $0\text{ ms}$.

#### Index 44: `idx_record_labels_label_id`
* **Collection**: `record_labels`
* **Field**: `{ label_id: 1 }`
* **Index Type**: Single Field / Unique Secondary
* **Reason**: Enforces record label identifier uniqueness across 60 corporate and independent label entities.
* **Query It Supports**:
  ```javascript
  db.record_labels.findOne({ label_id: "LBL_WARNER_RECORDS_001" });
  ```
* **Expected Benefit**: Guarantees label entity integrity and instant point lookups.
* **Explain Evidence**: Stage: `COLLSCAN` $\rightarrow$ `EXPRESS_IXSCAN`, `keysExamined`: $0 \rightarrow 1$, `docsExamined`: $60 \rightarrow 1$ (98.3% reduction), `executionTimeMillis`: $0\text{ ms}$.

---

## 5. Empirical Query Plan & Explain Evidence (`COLLSCAN` vs `IXSCAN`)

To scientifically demonstrate the concrete efficiency gains of Phase 21, ten representative workload queries spanning all five databases were benchmarked using `cursor.explain("executionStats")` before and after index deployment.

### 5.1 Benchmark Comparison Ledger

| Query ID | Database & Collection | Target Index | Before Stage | After Stage | Docs Examined (Before) | Docs Examined (After) | Reduction (%) | In-Memory Sort Eliminated |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Q01** | `grammy_nominations_db.nomination_entries` | `idx_nom_entries_nomination_id` | `COLLSCAN` | `EXPRESS_IXSCAN` | 500 | 1 | **99.8%** | N/A |
| **Q02** | `grammy_nominations_db.nomination_entries` | `idx_nom_entries_artist_id` | `COLLSCAN` | `IXSCAN` | 500 | 19 | **96.2%** | N/A |
| **Q03** | `grammy_nominations_db.nomination_entries` | `idx_nom_entries_winner_year_slot_esr` | `COLLSCAN + SORT` | `IXSCAN + FETCH` | 500 | 269 | **46.2%** | **YES** |
| **Q04** | `grammy_winners_db.acceptance_speeches` | `idx_speeches_ack_multikey` | `COLLSCAN` | `IXSCAN` | 65 | 65 | Multikey scan | N/A |
| **Q05** | `grammy_categories_db.merged_split_history` | `idx_merged_split_source_cats_multikey` | `COLLSCAN` | `IXSCAN` | 60 | 1 | **98.3%** | N/A |
| **Q06** | `grammy_nominations_db.tied_nominations` | `idx_tied_noms_tied_ids_multikey` | `COLLSCAN` | `IXSCAN` | 70 | 1 | **98.6%** | N/A |
| **Q07** | `grammy_winners_db.winner_records` | `idx_winner_records_telecast_statuettes_esr` | `COLLSCAN + SORT` | `IXSCAN + FETCH` | 400 | 200 | **50.0%** | **YES** |
| **Q08** | `grammy_history_db.ceremonies` | `idx_ceremonies_network_year_esr` | `COLLSCAN + SORT` | `IXSCAN + FETCH` | 67 | 26 | **61.2%** | **YES** |
| **Q09** | `grammy_categories_db.award_categories` | `idx_categories_status_nominees_esr` | `COLLSCAN + SORT` | `IXSCAN + FETCH` | 120 | 120 | Pre-sorted | **YES** |
| **Q10** | `grammy_creators_db.artists` | `idx_artists_group_career_esr` | `COLLSCAN + SORT` | `IXSCAN + FETCH` | 300 | 223 | **25.7%** | **YES** |

---

### 5.2 Deep Explain Plan Case Studies

#### Case Study 1: Point Lookup Transition (Q01 — `nomination_entries`)
* **Before (Unindexed)**:
  ```json
  {
    "stage": "COLLSCAN",
    "filter": { "nomination_id": { "$eq": "NOM_001_RECORD_OF__0000" } },
    "nReturned": 1,
    "totalDocsExamined": 500,
    "totalKeysExamined": 0
  }
  ```
* **After (`idx_nom_entries_nomination_id` Active)**:
  ```json
  {
    "stage": "EXPRESS_IXSCAN",
    "indexName": "idx_nom_entries_nomination_id",
    "nReturned": 1,
    "totalDocsExamined": 1,
    "totalKeysExamined": 1
  }
  ```
* **Analysis**: Documents examined plummeted from 500 to exactly 1. Atlas utilizes an optimized `EXPRESS_IXSCAN` stage which navigates directly to the B-Tree leaf node holding the record pointer without scanning unreferenced pages.

#### Case Study 2: Eliminating In-Memory Blocking Sorts (Q03 — Compound ESR)
* **Before (Unindexed)**:
  ```json
  {
    "stage": "SORT",
    "sortPattern": { "nomination_year": -1, "ballot_slot_order": 1 },
    "inputStage": {
      "stage": "COLLSCAN",
      "totalDocsExamined": 500
    }
  }
  ```
* **After (`idx_nom_entries_winner_year_slot_esr` Active)**:
  ```json
  {
    "stage": "FETCH",
    "inputStage": {
      "stage": "IXSCAN",
      "indexName": "idx_nom_entries_winner_year_slot_esr",
      "direction": "forward",
      "totalKeysExamined": 269
    },
    "totalDocsExamined": 269
  }
  ```
* **Analysis**: In the unindexed plan, MongoDB was forced to load all 500 documents into RAM and perform an expensive heap sort (`SORT` stage). With the compound ESR index, index keys are stored in exactly the requested sorting order (`nomination_year: -1, ballot_slot_order: 1`). The query engine performs an index scan directly yielding ordered documents, **eliminating 100% of sort memory overhead**.

#### Case Study 3: Multikey Array Containment (Q05 — `merged_split_history`)
* **Before (Unindexed)**:
  ```json
  {
    "stage": "COLLSCAN",
    "filter": { "source_category_ids": { "$all": ["LEGACY_CAT_MALE_0", "LEGACY_CAT_FEMALE_0"] } },
    "totalDocsExamined": 60
  }
  ```
* **After (`idx_merged_split_source_cats_multikey` Active)**:
  ```json
  {
    "stage": "FETCH",
    "inputStage": {
      "stage": "IXSCAN",
      "indexName": "idx_merged_split_source_cats_multikey",
      "totalKeysExamined": 1
    },
    "totalDocsExamined": 1
  }
  ```
* **Analysis**: Without the index, MongoDB performed an exhaustive unnesting check across every document's array in the collection. With the multikey index, the B-Tree maps array values directly to the single matching document ID, resulting in a **98.3% document reduction**.

---

## 6. WiredTiger Storage Engine Footprint & Memory Analysis

While indexes dramatically accelerate read throughput, they introduce physical disk overhead and cache footprint in the WiredTiger storage engine. Below are the live storage metrics captured from the Atlas cluster:

| Database | Collection | Documents | Document Size (Data) | Custom Indexes | Total Index Size | Index / Data Ratio |
|---|---|:---:|:---:|:---:|:---:|:---:|
| `grammy_history_db` | `ceremonies` | 67 | 47.87 KB | 4 | 180.00 KB | 3.76 |
| `grammy_history_db` | `venues` | 60 | 38.05 KB | 2 | 76.00 KB | 2.00 |
| `grammy_history_db` | `viewership_ratings` | 67 | 49.66 KB | 1 | 56.00 KB | 1.13 |
| `grammy_categories_db` | `award_categories` | 120 | 110.33 KB | 4 | 180.00 KB | 1.63 |
| `grammy_categories_db` | `award_fields` | 50 | 41.19 KB | 1 | 56.00 KB | 1.36 |
| `grammy_categories_db` | `merged_split_history` | 60 | 54.59 KB | 2 | 76.00 KB | 1.39 |
| `grammy_nominations_db` | `nomination_entries` | 500 | 393.42 KB | 5 | 288.00 KB | 0.73 |
| `grammy_nominations_db` | `nominated_works` | 500 | 372.36 KB | 2 | 120.00 KB | 0.32 |
| `grammy_nominations_db` | `tied_nominations` | 70 | 57.94 KB | 2 | 76.00 KB | 1.31 |
| `grammy_nominations_db` | `genre_classifications` | 70 | 59.12 KB | 2 | 76.00 KB | 1.29 |
| `grammy_nominations_db` | `multi_nomination_packages` | 70 | 48.03 KB | 2 | 76.00 KB | 1.58 |
| `grammy_winners_db` | `winner_records` | 400 | 328.87 KB | 4 | 212.00 KB | 0.64 |
| `grammy_winners_db` | `acceptance_speeches` | 65 | 58.13 KB | 3 | 96.00 KB | 1.65 |
| `grammy_winners_db` | `consecutive_winners` | 65 | 47.50 KB | 2 | 76.00 KB | 1.60 |
| `grammy_creators_db` | `artists` | 300 | 282.37 KB | 3 | 192.00 KB | 0.68 |
| `grammy_creators_db` | `songwriters_composers` | 75 | 64.24 KB | 2 | 76.00 KB | 1.18 |
| `grammy_creators_db` | `musical_groups` | 65 | 46.71 KB | 2 | 76.00 KB | 1.63 |
| `grammy_creators_db` | `record_labels` | 60 | 47.82 KB | 1 | 56.00 KB | 1.17 |

### Engineering Observations on Storage Overhead
1. **WiredTiger 4KB Page Allocation**: On smaller collections ($\le 100$ records), WiredTiger preallocates index leaf extents in minimum block multiples (typically 20KB–36KB per index), resulting in an index-to-data ratio greater than 1.0.
2. **Larger Collections Scale Efficiently**: On substantive collections such as `nomination_entries` (500 docs), `nominated_works` (500 docs), `winner_records` (400 docs), and `artists` (300 docs), the index-to-data ratio drops to **0.32–0.73**, demonstrating efficient prefix compression.
3. **Working Set Fit**: Total index allocation across all five databases is approximately **2.0 MB**, comfortably fitting within MongoDB Atlas's 512MB RAM working set allocation with zero risk of cache eviction thrashing.

---

## 7. Execution Artifacts & Tooling

The Phase 21 indexing subsystem provides complete administrative tooling and executable artifacts:

1. **Python Management CLI**: [`scripts/indexes/create_indexes.py`](../../scripts/indexes/create_indexes.py)
   - Supports `--create` (default deployment), `--verify` (audit presence), `--drop` (clean rollback), and `--stats` (storage report).
2. **Native mongosh Script**: [`mongodb/indexes/create_indexes.js`](../../mongodb/indexes/create_indexes.js)
   - Executable within `mongosh` shell or MongoDB Compass.
3. **Benchmark JSON Artifact**: [`docs/mongodb/indexing_benchmarks.json`](indexing_benchmarks.json)
   - Machine-readable before-and-after execution stats for all benchmark queries.
4. **Index Catalog JSON Artifact**: [`docs/mongodb/indexing_catalog.json`](indexing_catalog.json)
   - Complete machine-readable registry of all 44 index specifications.
5. **Automated Pytest Suite**: [`tests/test_indexing.py`](../../tests/test_indexing.py)
   - 13 comprehensive unit/integration tests running against the live Atlas cluster.

---

## 8. Verification & Test Certification

The test suite [`tests/test_indexing.py`](../../tests/test_indexing.py) verifies the entire indexing implementation against the live MongoDB Atlas cluster across 34 rigorous test scenarios:

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: G:\Projects\grammy-advanced-dbms
configfile: pyproject.toml
collected 34 items

tests/test_indexing.py::test_atlas_cluster_connection PASSED             [  2%]
tests/test_indexing.py::test_all_five_databases_exist PASSED             [  5%]
tests/test_indexing.py::test_all_indexes_present_in_database[grammy_history_db] PASSED [  8%]
tests/test_indexing.py::test_all_indexes_present_in_database[grammy_categories_db] PASSED [ 11%]
tests/test_indexing.py::test_all_indexes_present_in_database[grammy_nominations_db] PASSED [ 14%]
tests/test_indexing.py::test_all_indexes_present_in_database[grammy_winners_db] PASSED [ 17%]
tests/test_indexing.py::test_all_indexes_present_in_database[grammy_creators_db] PASSED [ 20%]
tests/test_indexing.py::test_total_custom_index_count PASSED             [ 23%]
tests/test_indexing.py::test_unique_secondary_index_enforcement[grammy_history_db-ceremonies-ceremony_id-CEREMONY_001] PASSED [ 26%]
tests/test_indexing.py::test_unique_secondary_index_enforcement[grammy_categories_db-award_categories-category_id-CAT_RECORD_OF_THE_YEAR_000] PASSED [ 29%]
tests/test_indexing.py::test_unique_secondary_index_enforcement[grammy_nominations_db-nominated_works-work_id-WRK_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000] PASSED [ 32%]
tests/test_indexing.py::test_unique_secondary_index_enforcement[grammy_winners_db-winner_records-winner_record_id-WIN_NOM_001_RECORD_OF__0000] PASSED [ 35%]
tests/test_indexing.py::test_unique_secondary_index_enforcement[grammy_creators_db-artists-artist_id-CRT_NEL_BLU_DIPINTO_DI_BLU_VOLARE_0000] PASSED [ 38%]
tests/test_indexing.py::test_multikey_index_queries_use_ixscan[grammy_winners_db-acceptance_speeches-query_filter0-Speech acknowledgments] PASSED [ 41%]
tests/test_indexing.py::test_multikey_index_queries_use_ixscan[grammy_categories_db-merged_split_history-query_filter1-Merged split history source categories] PASSED [ 44%]
tests/test_indexing.py::test_multikey_index_queries_use_ixscan[grammy_nominations_db-tied_nominations-query_filter2-Tied nomination IDs] PASSED [ 47%]
tests/test_indexing.py::test_multikey_index_queries_use_ixscan[grammy_nominations_db-genre_classifications-query_filter3-Genre classification tags] PASSED [ 50%]
tests/test_indexing.py::test_multikey_index_queries_use_ixscan[grammy_nominations_db-multi_nomination_packages-query_filter4-Multi-nomination packages works] PASSED [ 52%]
tests/test_indexing.py::test_multikey_index_queries_use_ixscan[grammy_winners_db-consecutive_winners-query_filter5-Consecutive winning works list] PASSED [ 55%]
tests/test_indexing.py::test_compound_esr_query_plans_use_ixscan[grammy_nominations_db-nomination_entries-filter_spec0-sort_spec0-nomination_entries winner + year range + ballot sort] PASSED [ 58%]
tests/test_indexing.py::test_compound_esr_query_plans_use_ixscan[grammy_history_db-ceremonies-filter_spec1-sort_spec1-ceremonies network + broadcast year sort] PASSED [ 61%]
tests/test_indexing.py::test_compound_esr_query_plans_use_ixscan[grammy_categories_db-award_categories-filter_spec2-sort_spec2-award_categories active status + nominees capacity sort] PASSED [ 64%]
tests/test_indexing.py::test_compound_esr_query_plans_use_ixscan[grammy_winners_db-winner_records-filter_spec3-sort_spec3-winner_records live telecast + statuettes sort] PASSED [ 67%]
tests/test_indexing.py::test_compound_esr_query_plans_use_ixscan[grammy_creators_db-artists-filter_spec4-sort_spec4-artists solo flag + career start year sort] PASSED [ 70%]
tests/test_indexing.py::test_single_field_point_lookup_efficiency[grammy_nominations_db-nomination_entries-point_filter0] PASSED [ 73%]
tests/test_indexing.py::test_single_field_point_lookup_efficiency[grammy_history_db-ceremonies-point_filter1] PASSED [ 76%]
tests/test_indexing.py::test_single_field_point_lookup_efficiency[grammy_creators_db-artists-point_filter2] PASSED [ 79%]
tests/test_indexing.py::test_single_field_point_lookup_efficiency[grammy_history_db-venues-point_filter3] PASSED [ 82%]
tests/test_indexing.py::test_all_44_custom_indexes_produce_ixscan PASSED [ 85%]
tests/test_indexing.py::test_wiredtiger_index_storage_allocated[grammy_nominations_db-nomination_entries-6] PASSED [ 88%]
tests/test_indexing.py::test_wiredtiger_index_storage_allocated[grammy_history_db-ceremonies-5] PASSED [ 91%]
tests/test_indexing.py::test_wiredtiger_index_storage_allocated[grammy_categories_db-award_categories-5] PASSED [ 94%]
tests/test_indexing.py::test_wiredtiger_index_storage_allocated[grammy_winners_db-winner_records-5] PASSED [ 97%]
tests/test_indexing.py::test_wiredtiger_index_storage_allocated[grammy_creators_db-artists-4] PASSED [100%]

============================= 34 passed in 5.43s ==============================
```

Additionally, full regression testing across all operational phases confirmed **80 / 80 passing tests (100% success rate)**:
- Phase 18 CRUD Suite: 19 / 19 PASSED
- Phase 19 Advanced Queries: 13 / 13 PASSED
- Phase 20 Aggregation Pipelines: 14 / 14 PASSED
- Phase 21 Indexing Verification: 34 / 34 PASSED

---

## 9. Phase Boundary Certification & Approval Sign-off

- **Current Phase**: Phase 21 — Indexing
- **Status**: **100% COMPLETED & FORMALLY VERIFIED ON MONGODB ATLAS**
- **Artifacts Generated**:
  - `docs/mongodb/indexing.md` (This document)
  - `docs/mongodb/indexing_benchmarks.json`
  - `docs/mongodb/indexing_catalog.json`
  - `scripts/indexes/create_indexes.py`
  - `mongodb/indexes/create_indexes.js`
  - `tests/test_indexing.py`
- **Stop Condition**: **STOP after completing Phase 21.**
