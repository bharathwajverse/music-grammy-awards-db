# Module 3: Controlled & Justified Denormalization Strategy

## 1. Academic Rationale: Bridging Relational Normalization to Document Modeling

In classical relational theory (Modules 2 & 3), we decompose schemas into 3NF, BCNF, 4NF, and 5NF to achieve three primary mathematical goals:
1. **Elimination of Update Anomalies** (Insert, Update, Delete).
2. **Elimination of Data Redundancy**.
3. **Preservation of Lossless Joins and Functional Dependencies**.

However, in modern distributed NoSQL systems like **MongoDB** (Modules 8, 9, 10):
- Joins across physically distributed partitions or distinct databases carry high latency, network serialization overhead, and lack global cross-cluster lock managers.
- Document-oriented databases leverage hierarchical, nested data structures (embedded subdocuments and arrays) where data that is **accessed together is stored together** on disk in single contiguous BSON allocations.

Therefore, our system employs **controlled, academically justified denormalization**: we maintain our relational reference schema in strict 3NF/BCNF while selectively denormalizing read-intensive sub-entities into embedded BSON structures.

---

## 2. Decision Matrix: Embedding vs Referencing

We formulate our design using the following engineering and academic criteria:

| Dimension | Embedding Pattern (Denormalized) | Referencing Pattern (Normalized) |
| :--- | :--- | :--- |
| **Relationship Cardinality** | $1:1$ or $1:\text{Few}$ (Bounded arrays $< 100$ items) | $1:\text{Many}$ or $M:N$ (Unbounded or growing collections) |
| **Data Volatility** | Static, archival, or rarely mutated | High-frequency update cycles |
| **Query Access Pattern** | Parent and child always read together in single transaction | Independent query access on child entity |
| **Document Size Boundary** | Must safely fit within WiredTiger 16 MB BSON document limit | Scalable to millions of independent records |

---

## 3. Justified Denormalization Case Studies

### Case Study 1: `nomination_credits` inside `nomination_entries`
- **Relational Normalized Model (BCNF)**: Separate `nomination_credits` table containing individual rows for every producer, engineer, and artist. Querying a single nomination entry requires a SQL `JOIN`.
- **MongoDB Denormalized Document Model**: Embed credits as an array of subdocuments inside `nomination_entries`:
  ```json
  {
    "nomination_id": "NOM_065_AOTY_01",
    "entry_billing_title": "Renaissance",
    "category_id": "CAT_AOTY",
    "credits": [
      { "creator_id": "CRT_BEYONCE_001", "role": "Artist", "is_lead": true },
      { "creator_id": "CRT_THE_DREAM_001", "role": "Producer", "is_lead": false },
      { "creator_id": "CRT_MIKE_DEAN_001", "role": "Mixer", "is_lead": false }
    ]
  }
  ```
- **Academic Justification**:
  1. *Bounded Cardinality*: Album credits are strictly bounded by Recording Academy bylaws (typically 5 to 30 credited individuals per nominated album). This guarantees the document will never approach the 16 MB limit.
  2. *Read Co-locality*: A user or analytical engine querying a nomination entry virtually always needs to inspect who was credited on that nomination.
  3. *Zero Update Anomaly*: Nominations are historical, immutable facts once audited and published. No updates occur post-ceremony, eliminating the risk of update anomalies.

---

### Case Study 2: `viewership_ratings` and `ceremonies`
- **Relational Normalized Model (3NF)**: 1:1 relation between `ceremonies` and `viewership_ratings`.
- **MongoDB Strategy**: Kept as **separate collections** (`ceremonies` and `viewership_ratings`) linked by `ceremony_id`, with optional embedded summary metrics (`us_viewers_millions`) in the ceremony document.
- **Academic Justification**:
  - Ceremony telecast data is fixed at the conclusion of the broadcast, whereas detailed demographic ratings from Nielsen Media Research arrive in staggered post-show audit batches over subsequent weeks.
  - Separating the collection preserves transaction independence during ratings updates without locking the ceremony metadata record.

---

### Case Study 3: Denormalized Descriptive Cache in `winner_records`
- **Relational Normalized Model (BCNF)**: `winner_records` stores only foreign keys: `nomination_id`, `category_id`, `winning_work_id`, `primary_artist_id`.
- **MongoDB Strategy**: Denormalize three immutable display strings directly into `winner_records`:
  - `work_title`: "Renaissance"
  - `artist_display_name`: "Beyoncé"
  - `category_display_name`: "Album of the Year"
- **Academic Justification**:
  - The winner ledger is the most heavily queried collection for public dashboards, historic charts, and press queries.
  - Embedding immutable display strings reduces query execution from an expensive 4-collection distributed aggregation (`$lookup`) down to a single index-scan (`IXSCAN`) on `winner_records`, resulting in orders-of-magnitude reduction in latency.
