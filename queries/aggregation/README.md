# Phase 20 — Aggregation Framework & Analytical Pipelines

> **Academic Module**: Module 10 — Advanced Query & Aggregation Framework  
> **Target Databases**: `grammy_nominations_db`, `grammy_winners_db`, `grammy_categories_db`, `grammy_history_db`, `grammy_creators_db`  
> **Master Script**: [`aggregation_pipelines.js`](aggregation_pipelines.js)  
> **Data Integrity Constraint**: Real Project Data Only (Zero Synthetic Facts)  
> **Annotation Standard**: Strict Explicit `DERIVED` Labeling for Computed Analytical Metrics  

---

## 1. Executive Summary & Aggregation Framework Architecture

In advanced database management systems, operational querying retrieves existing tuples, whereas **data analytics and aggregation pipelines** synthesize high-order intelligence, longitudinal trends, and multi-relational statistics. The MongoDB Aggregation Framework models data transformations as a directed, multi-stage processing pipeline ($\mathcal{P} = \langle \sigma_1, \sigma_2, \dots, \sigma_k \rangle$), where document streams flow through discrete stages of filtering, deconstruction, grouping, relational joining, projection, and ordering.

Phase 20 implements meaningful, high-performance analytical queries across the 5 member databases of the **GRAMMY Awards Information & Analytics System**, adhering to strict requirements:
1. **Mandatory Pipeline Operators**: Full demonstration of `$match`, `$group`, `$sort`, `$project`, `$count`, `$lookup`, and `$unwind`.
2. **Mandatory Analytical Suites**: Implementation of the 7 core project analytical queries (Nominations per artist, Wins per artist, Wins by category, Nominations by year, Category trends, Artists appearing in multiple categories, Multi-time winners).
3. **Explicit `DERIVED` Labeling**: In strict compliance with academic data provenance standards, every single calculated metric, statistical summary, or transformed field is explicitly designated and prefixed as `DERIVED` (e.g., `DERIVED_total_nominations`, `DERIVED_career_wins_count`, `DERIVED_calculation_status: "DERIVED"`), clearly delineating derived analytics from authoritative source facts.
4. **Real Project Data**: All pipelines execute directly against the 5,190 validated documents loaded into MongoDB Atlas.

---

## 2. Operator Coverage & Stage Matrix

| MongoDB Stage / Operator | Mathematical / Relational Algebraic Equivalent | Primary Role in Pipeline Stream | Demonstrated In Pipelines |
| :--- | :--- | :--- | :--- |
| **`$match`** | Selection ($\sigma_{\theta}$) | Filters document streams before and after accumulation | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10 |
| **`$group`** | Aggregation ($\gamma_{A, F(B)}$) | Groups documents by key and computes accumulators (`$sum`, `$avg`, `$min`, `$max`, `$addToSet`) | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10 |
| **`$sort`** | Ordering ($\tau_{k}$) | Orders output streams by derived keys (ascending or descending) | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10 |
| **`$project`** | Generalized Projection ($\pi_{E}$) | Reshapes output schema, computes arithmetic expressions, suppresses `_id` | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10 |
| **`$count`** | Cardinality ($\text{COUNT}(\sigma)$) | Computes scalar stream document count without accumulator overhead | 07, 10 |
| **`$lookup`** | Left Outer Join ($\bowtie_{\theta}$) | Executes relational join across intra-database collections | 01, 02, 07, 09 |
| **`$unwind`** | Relational Unnesting ($\mu_{A}$) | Deconstructs array elements into distinct individual document streams | 01, 08, 09, 10 |

---

## 3. Mandatory Analytical Pipelines Catalog

### 3.1 Pipeline 01: Nominations per Artist
- **Script**: [`01_nominations_per_artist.js`](01_nominations_per_artist.js)
- **Database**: `grammy_nominations_db` | **Collection**: `nomination_entries`
- **Join Target**: `nominated_works` (via `$lookup` on `work_id`)
- **Key Operators**: `$match`, `$lookup`, `$unwind`, `$group`, `$project`, `$sort`, `$limit`
- **Calculated Metrics**: `DERIVED_total_nominations`, `DERIVED_earliest_nomination_year`, `DERIVED_latest_nomination_year`, `DERIVED_career_span_years`, `DERIVED_distinct_works_count`, `DERIVED_distinct_categories_count`.
- **Sample Verified Result (Atlas)**:
  ```json
  {
    "artist_id": "CRT_HENRY_MANCINI_0001",
    "artist_billing_name": "The Music From Peter Gunn",
    "DERIVED_total_nominations": 19,
    "DERIVED_earliest_nomination_year": 1959,
    "DERIVED_latest_nomination_year": 1971,
    "DERIVED_career_span_years": 12,
    "DERIVED_distinct_works_count": 13,
    "DERIVED_distinct_categories_count": 12,
    "DERIVED_calculation_status": "DERIVED"
  }
  ```

---

### 3.2 Pipeline 02: Wins per Artist
- **Script**: [`02_wins_per_artist.js`](02_wins_per_artist.js)
- **Database**: `grammy_winners_db` | **Collection**: `winner_records`
- **Join Target**: `acceptance_speeches` (via `$lookup` on `winner_record_id`)
- **Key Operators**: `$match`, `$lookup`, `$group`, `$project`, `$sort`, `$limit`
- **Calculated Metrics**: `DERIVED_total_wins`, `DERIVED_total_statuettes_awarded`, `DERIVED_avg_statuettes_per_win`, `DERIVED_live_telecast_wins`, `DERIVED_speeches_delivered`, `DERIVED_distinct_winning_categories_count`, `DERIVED_distinct_ceremonies_count`.
- **Sample Verified Result (Atlas)**:
  ```json
  {
    "artist_id": "CRT_HENRY_MANCINI_0001",
    "DERIVED_total_wins": 17,
    "DERIVED_total_statuettes_awarded": 22,
    "DERIVED_avg_statuettes_per_win": 1.29,
    "DERIVED_live_telecast_wins": 14,
    "DERIVED_speeches_delivered": 17,
    "DERIVED_distinct_winning_categories_count": 12,
    "DERIVED_distinct_ceremonies_count": 6,
    "DERIVED_calculation_status": "DERIVED"
  }
  ```

---

### 3.3 Pipeline 03: Wins by Category
- **Script**: [`03_wins_by_category.js`](03_wins_by_category.js)
- **Database**: `grammy_winners_db` | **Collection**: `winner_records`
- **Key Operators**: `$match`, `$group`, `$project`, `$sort`, `$limit`
- **Calculated Metrics**: `DERIVED_total_historical_wins`, `DERIVED_cumulative_statuettes`, `DERIVED_telecast_presentations`, `DERIVED_telecast_percentage`, `DERIVED_distinct_winners_count`.
- **Sample Verified Result (Atlas)**:
  ```json
  {
    "category_id": "CAT_RECORD_OF_THE_YEAR_000",
    "DERIVED_total_historical_wins": 14,
    "DERIVED_cumulative_statuettes": 28,
    "DERIVED_telecast_presentations": 14,
    "DERIVED_telecast_percentage": 100.0,
    "DERIVED_distinct_winners_count": 13,
    "DERIVED_calculation_status": "DERIVED"
  }
  ```

---

### 3.4 Pipeline 04: Nominations by Year
- **Script**: [`04_nominations_by_year.js`](04_nominations_by_year.js)
- **Database**: `grammy_nominations_db` | **Collection**: `nomination_entries`
- **Key Operators**: `$match`, `$group`, `$project`, `$sort`
- **Calculated Metrics**: `DERIVED_total_nominations`, `DERIVED_total_winners`, `DERIVED_distinct_categories_count`, `DERIVED_distinct_nominees_count`, `DERIVED_avg_slot_depth`.
- **Sample Verified Result (Atlas)**:
  ```json
  {
    "ceremony_year": 1959,
    "DERIVED_total_nominations": 28,
    "DERIVED_total_winners": 28,
    "DERIVED_distinct_categories_count": 28,
    "DERIVED_distinct_nominees_count": 22,
    "DERIVED_avg_slot_depth": 2.89,
    "DERIVED_calculation_status": "DERIVED"
  }
  ```

---

### 3.5 Pipeline 05: Category Trends Across Decades
- **Script**: [`05_category_trends.js`](05_category_trends.js)
- **Database**: `grammy_nominations_db` | **Collection**: `nomination_entries`
- **Key Operators**: `$match`, `$group` (compound with arithmetic decade bucketing), `$project`, `$sort`
- **Calculated Metrics**: `DERIVED_nominations_count`, `DERIVED_winners_count`, `DERIVED_distinct_artists_count`, `DERIVED_decade_span`.
- **Sample Verified Result (Atlas)**:
  ```json
  {
    "category_id": "CAT_RECORD_OF_THE_YEAR_000",
    "decade_label": "1960s",
    "DERIVED_nominations_count": 10,
    "DERIVED_winners_count": 10,
    "DERIVED_distinct_artists_count": 9,
    "DERIVED_decade_span": "1960 - 1969",
    "DERIVED_calculation_status": "DERIVED"
  }
  ```

---

### 3.6 Pipeline 06: Artists Appearing in Multiple Categories
- **Script**: [`06_artists_in_multiple_categories.js`](06_artists_in_multiple_categories.js)
- **Database**: `grammy_nominations_db` | **Collection**: `nomination_entries`
- **Key Operators**: `$match`, `$group`, `$project`, post-aggregation `$match` (`$gt: 1`), `$sort`, `$limit`
- **Calculated Metrics**: `DERIVED_distinct_categories_count`, `DERIVED_distinct_categories_list`, `DERIVED_distinct_years_count`, `DERIVED_total_nominations`.
- **Sample Verified Result (Atlas)**:
  ```json
  {
    "artist_id": "CRT_HENRY_MANCINI_0001",
    "artist_billing_title": "The Music From Peter Gunn",
    "DERIVED_distinct_categories_count": 12,
    "DERIVED_distinct_years_count": 8,
    "DERIVED_total_nominations": 19,
    "DERIVED_calculation_status": "DERIVED"
  }
  ```

---

### 3.7 Pipeline 07: Multi-Time Winners & Repeat Recipients
- **Script**: [`07_multi_time_winners.js`](07_multi_time_winners.js)
- **Database**: `grammy_winners_db` | **Collection**: `winner_records`
- **Join Target**: `consecutive_winners` (via `$lookup` on `artist_id`)
- **Key Operators**: `$match`, `$group`, post-aggregation `$match`, `$lookup`, `$project`, `$sort`, `$limit`, `$count`
- **Calculated Metrics**: `DERIVED_career_wins_count`, `DERIVED_total_statuettes`, `DERIVED_distinct_ceremonies_count`, `DERIVED_distinct_categories_count`, `DERIVED_has_consecutive_streaks`, `DERIVED_consecutive_streaks_count`, `DERIVED_total_multi_time_winners_count`.
- **Sample Verified Result (Atlas)**:
  ```json
  {
    "artist_id": "CRT_HENRY_MANCINI_0001",
    "DERIVED_career_wins_count": 17,
    "DERIVED_total_statuettes": 22,
    "DERIVED_distinct_ceremonies_count": 6,
    "DERIVED_distinct_categories_count": 12,
    "DERIVED_has_consecutive_streaks": false,
    "DERIVED_consecutive_streaks_count": 0,
    "DERIVED_calculation_status": "DERIVED"
  }
  ```
- **Companion `$count` Stage Output**:
  ```json
  { "DERIVED_total_multi_time_winners_count": 49 }
  ```

---

## 4. Supplementary Domain Analytical Pipelines

### 4.1 Pipeline 08: Acceptance Speech Acknowledgments Distribution
- **Script**: [`08_speech_acknowledgments_distribution.js`](08_speech_acknowledgments_distribution.js)
- **Database**: `grammy_winners_db` | **Collection**: `acceptance_speeches`
- **Demonstrated Operators**: `$match`, `$unwind` (`individuals_acknowledged`), `$group`, `$project`, `$sort`
- **Calculated Metrics**: `DERIVED_acknowledgment_frequency`, `DERIVED_avg_duration_sec`, `DERIVED_distinct_speakers_count`, `DERIVED_speeches_with_social_message`.

### 4.2 Pipeline 09: Venue Hosting & Capacity Analytics
- **Script**: [`09_venue_ceremony_analytics.js`](09_venue_ceremony_analytics.js)
- **Database**: `grammy_history_db` | **Collection**: `ceremonies`
- **Demonstrated Operators**: `$match`, `$lookup` (`venues`), `$unwind`, `$group`, `$project`, `$sort`
- **Calculated Metrics**: `DERIVED_ceremonies_hosted_count`, `DERIVED_earliest_edition`, `DERIVED_latest_edition`, `DERIVED_venue_capacity`.

### 4.3 Pipeline 10: Category Restructure & Lineage Analytics
- **Script**: [`10_category_restructure_analytics.js`](10_category_restructure_analytics.js)
- **Database**: `grammy_categories_db` | **Collection**: `merged_split_history`
- **Demonstrated Operators**: `$match`, `$unwind` (`source_category_ids`), `$group`, `$project`, `$sort`, `$count`
- **Calculated Metrics**: `DERIVED_merged_source_categories_count`, `DERIVED_distinct_sources_count`, `DERIVED_events_count`, `DERIVED_total_source_category_mappings`.

---

## 5. Explicit DERIVED Labeling Standard

In academic database theory and data provenance governance, blurring authoritative source records with aggregated summaries violates traceability. To prevent analytical confusion:
1. **Field-Level Prefixing**: Every output attribute generated through an aggregator (`$sum`, `$avg`, `$min`, `$max`, `$addToSet`, `$size`, `$round`, `$subtract`, `$multiply`, `$divide`, `$concat`) is prefixed with `DERIVED_`.
2. **Metadata Tagging**: Every projection explicitly includes a static metadata assertion: `DERIVED_calculation_status: "DERIVED"`.
3. **Immutability of Source Data**: No aggregation pipeline writes back to primary collections using `$out` or `$merge` without authorization. All analyses run purely as read-only streams.

---

## 6. Execution Instructions

### 6.1 Interactive Execution via `mongosh`
```bash
# Execute master suite across all 5 databases
mongosh "$MONGODB_URI" queries/aggregation/aggregation_pipelines.js

# Execute individual analytical pipeline
mongosh "$MONGODB_URI" queries/aggregation/01_nominations_per_artist.js
mongosh "$MONGODB_URI" queries/aggregation/07_multi_time_winners.js
```

### 6.2 Automated Python Test Runner
```bash
python scripts/aggregation/run_all_aggregations.py
pytest tests/test_aggregation_pipelines.py -v
```
