# Project Requirements Specification: GRAMMY Awards Information & Analytics System

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Document**: Functional, Non-Functional, and Academic Requirements Baseline  
> **Status**: Frozen / Baseline Specification (Phase 1 Requirements Freeze)  
> **Version Control**: Git / GitHub (`bharathwajverse/music-grammy-awards-db`)  

---

## 1. Project Objective

The primary objective of the **GRAMMY Awards Information & Analytics System** is to design, model, validate, implement, and analyze an enterprise-grade, distributed database system managing the complete historical, artistic, operational, and statistical corpus of the Recording Academy’s Annual GRAMMY Awards (1959–Present).

The system serves both as:
1. **An Advanced Academic DBMS Benchmark**: Providing a rigorous, verifiable platform to demonstrate all ten syllabus modules—spanning relational algebra, Enhanced Entity-Relationship (EER) modeling, mathematical functional dependencies, Boyce-Codd Normal Form (BCNF), 4NF/5NF proofs, multi-document ACID transactions, Strict Two-Phase Locking (Strict 2PL), WiredTiger storage internals, log-based Write-Ahead Recovery (WAL), and distributed NoSQL aggregation pipelines.
2. **A Production-Grade Domain Analytics System**: Delivering a referentially unified, query-optimized information repository capable of resolving complex cross-domain queries regarding musical creators, category lineages, multi-credit craft contributions, ceremony telecast viewership, and historical record sweeps.

---

## 2. Problem Statement

Historical award systems within the creative arts present fundamental database engineering challenges that expose the limitations of naive relational architectures and unstructured document stores:
- **Extreme Domain Complexity & Non-Atomic Craft Credits**: A single GRAMMY nomination (e.g., *Album of the Year*) associates hundreds of discrete creative participants (primary vocalists, featured artists, producers, recording engineers, mixing engineers, mastering engineers, and songwriters). Relational normalization produces deep join explosions across dozens of tables, inducing severe performance bottlenecks.
- **Dynamic Category Lineages & Temporal Schema Drift**: Award categories undergo continuous evolutionary lifecycle changes—merging, splitting, renaming, restructuring eligibility criteria, and being discontinued across six decades. Flat relational schemas fail to capture category lineage trees without extensive nullability and redundant foreign keys.
- **Data Fragmentation & Licensing Opacity**: Public award data is notoriously dispersed across heterogeneous web repositories, unofficial scrapers, and raw spreadsheets, frequently riddled with transcription errors, lack of provenance, and undocumented copyright licenses.
- **Academic Rigor vs. Application Illusion**: Typical academic database projects often simulate unrealistic mock data or shallow CRUD apps that do not test enterprise DBMS capabilities such as concurrency deadlocks, slotted-page storage fragmentation, crash recovery replay, or multi-stage aggregation optimization.

The **GRAMMY Awards Information & Analytics System** resolves these challenges by introducing a disciplined, multi-database architecture backed by real-world factual data, formal normalization proofs, deterministic universal identifiers, and automated schema validation.

---

## 3. Five-Member Team Structure

The project enforces an egalitarian, five-member engineering team structure. Each team member functions as the principal database administrator and domain architect for one dedicated MongoDB database:

```
                               ┌────────────────────────────────────────────────────────┐
                               │     GRAMMY Awards Information & Analytics System       │
                               │                (Integrated DBMS)                       │
                               └──────────────────────────┬─────────────────────────────┘
                                                          │
          ┌───────────────────────┬───────────────────────┼───────────────────────┬───────────────────────┐
          │                       │                       │                       │                       │
          ▼                       ▼                       ▼                       ▼                       ▼
    Member 1 Scope          Member 2 Scope          Member 3 Scope          Member 4 Scope          Member 5 Scope
 ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
 │ grammy_history_db   │ │ grammy_categories_db│ │grammy_nominations_db│ │  grammy_winners_db  │ │  grammy_creators_db │
 │                     │ │                     │ │                     │ │                     │ │                     │
 │ • Ceremonies        │ │ • Award Fields      │ │ • Nominated Works   │ │ • Winner Records    │ │ • Artists           │
 │ • Venues            │ │ • Categories        │ │ • Nomination Entries│ │ • Big Four Sweeps   │ │ • Producers         │
 │ • Telecasts/Ratings │ │ • Lineage Trees     │ │ • Craft Credits     │ │ • Record Breakers   │ │ • Audio Engineers   │
 │ • Broadcast Hosts   │ │ • Eligibility Rules │ │ • Submissions       │ │ • Acceptance Speech │ │ • Songwriters       │
 │ • Milestones/Eras   │ │ • Voting Rules      │ │ • Screening Batches │ │ • Trophy Logistics  │ │ • Record Labels     │
 └─────────────────────┘ └─────────────────────┘ └─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

Each team member is personally accountable for:
1. Designing the EER conceptual model, relational DDL, and BSON document schema for their domain.
2. Authoring functional dependencies, normalization proofs, and denormalization justifications for their collections.
3. Ingesting, transforming, and validating certified data meeting all numerical quotas.
4. Implementing syllabus-aligned CRUD operations, advanced queries, and aggregation pipelines.
5. Coordinating cross-database referential integrity with peer members through standardized global IDs.

---

## 4. Five Databases Architecture

The system topology consists of five distinct, logically separated databases hosted on MongoDB Atlas:

| Database ID | Database Name | Lead Engineer | Primary Architectural Purpose |
| :---: | :--- | :---: | :--- |
| **DB-01** | `grammy_history_db` | Member 1 | Encapsulates ceremony events, geographic venues, broadcast telecasts, Nielsen ratings, hosts, historical eras, and academy leadership. |
| **DB-02** | `grammy_categories_db` | Member 2 | Models award taxonomies, genre fields, category mergers/splits, discontinued categories, eligibility windows, voting rules, and balloting limits. |
| **DB-03** | `grammy_nominations_db` | Member 3 | Ingests the core nomination entries, creative submission batches, voter screening committees, nominated tracks/albums, and multi-participant credits. |
| **DB-04** | `grammy_winners_db` | Member 4 | Records verified victorious entries, historic records, Big Four sweeps, acceptance speeches, trophy manufacturing/tracking, and Hall of Fame honors. |
| **DB-05** | `grammy_creators_db` | Member 5 | Maintains master entity records for individuals and organizations—artists, producers, audio engineers, composers, musical groups, and record labels. |

---

## 5. Numerical Requirements & Hard Quotas

To ensure depth, academic validity, and meaningful DBMS testing, the system enforces non-negotiable numerical thresholds across all five databases:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 MANDATORY SYSTEM QUOTAS                                │
├──────────────────────────────┬─────────────────────────────┬───────────────────────────┤
│ Metric                       │ Minimum Requirement         │ System-Wide Total         │
├──────────────────────────────┼─────────────────────────────┼───────────────────────────┤
│ Dedicated Databases          │ 1 per member                │ 5 Databases               │
│ Collections per Database     │ Minimum 10 collections      │ Minimum 50 Collections    │
│ Documents per Collection     │ Minimum 50 documents        │ Minimum 2,500 Documents   │
│ Meaningful Fields per Doc    │ Minimum 10 typed attributes │ Minimum 500 Unique Fields │
└──────────────────────────────┴─────────────────────────────┴───────────────────────────┘
```

### Quota Rules:
1. **Meaningful Field Rule**: Fields must represent domain properties (e.g., `ceremony_id`, `running_time_minutes`, `viewership_share`, `sample_rate_khz`, `voting_round`). Synthetic counter fields (`dummy_1`, `field_2`) or trivial timestamps (`created_at`, `updated_at`) do not count toward satisfying the 10-field quota.
2. **Document Volume Rule**: Every single collection must contain at least 50 valid documents. Collections with 49 or fewer documents fail automated compliance.
3. **No Empty / Dummy Collections**: Every collection must serve an explicit function defined in the system data dictionary and conceptual EER model.

---

## 6. Academic Syllabus Requirements (Modules 1–10)

The project serves as an end-to-end academic implementation benchmark for the Advanced DBMS curriculum:

* **Module 1: Relational Query Languages & EER Modeling**:
  - Full EER conceptual modeling incorporating subclasses, superclasses, disjoint/overlapping specialization, generalization, aggregation, and union categories.
  - Translation of EER models into relational DDL schemas with primary/foreign keys and check constraints.
  - Formal relational algebra expressions ($\sigma, \pi, \cup, \cap, -, \times, \bowtie, \rho, \div$) solving complex analytical questions.
* **Module 2: Functional Dependencies & Schema Refinement (1NF, 2NF)**:
  - Formal specification of functional dependencies ($X \rightarrow Y$), Armstrong's Axioms, attribute closures ($X^+$), and minimal covers ($F_{min}$).
  - Decomposition of non-atomic attributes to 1NF and removal of partial key dependencies on composite candidate keys to 2NF.
* **Module 3: Higher Normal Forms (3NF, BCNF, 4NF, 5NF) & Denormalization**:
  - Mathematical decomposition of transitive dependencies to 3NF and BCNF with lossless-join proofs and dependency-preservation evaluations.
  - Identification and handling of multivalued dependencies ($X \twoheadrightarrow Y$) in 4NF and join dependencies ($\bowtie$) in 5NF.
  - Rigorous, academic justification for denormalizing BCNF relations into embedded BSON structures in MongoDB.
* **Module 4: Transactions, ACID Properties & Schedules**:
  - Demonstration of multi-document ACID transactions across MongoDB collections using client sessions.
  - Formal schedule analysis, conflict serializability proofs, and serialization precedence graph generation.
  - Transaction state machine modeling (Active $\rightarrow$ Partially Committed $\rightarrow$ Committed / Aborted).
* **Module 5: Concurrency Control & Deadlock Handling**:
  - Implementation and testing of Strict Two-Phase Locking (Strict 2PL) to prevent dirty reads, non-repeatable reads, and lost updates.
  - Simulation of timestamp ordering protocols and deadlock detection using Wait-For-Graphs (WFG) with cycle detection algorithms.
* **Module 6: Storage Architecture, RAID & File Organization**:
  - In-depth analysis of disk block layouts, fixed vs. variable record structures, slotted-page architectures, and WiredTiger leaf-page compression.
  - Quantitative RAID level tradeoff evaluations (RAID 0, 1, 5, 10) for high-throughput ballot ingest vs. historical analytics.
  - Exploration of database system catalogs, data dictionaries, and storage sizing metadata.
* **Module 7: Recovery Concepts & Disaster Resilience**:
  - Practical evaluation of Write-Ahead Logging (WAL) and WiredTiger write journals through crash simulation and journal replay.
  - Comparative analysis of shadow paging vs. in-place logging with checkpoints.
  - Automated disaster recovery drills demonstrating full and point-in-time recovery (`mongodump` / `mongorestore`) under specified RPO/RTO SLAs.
* **Module 8: NoSQL Foundations & MongoDB Architecture**:
  - CAP and PACELC theorem positioning of MongoDB replica sets.
  - Architectural evaluation of MongoDB Atlas cluster topology, shard keys, WiredTiger cache sizing, and MongoDB Compass profiling.
* **Module 9: MongoDB CRUD Operations & Import/Export**:
  - Production-ready CRUD suite executing advanced filtering, array manipulation, and projection.
  - Scripted, schema-validated bulk data import and export pipelines (`mongoimport`, `mongoexport`, and Python BSON streaming).
* **Module 10: Advanced Aggregations & Query Optimization**:
  - Multi-stage aggregation pipelines utilizing `$match`, `$project`, `$group`, `$unwind`, `$lookup`, `$facet`, and `$bucketAuto`.
  - Multikey, compound, and partial indexes benchmarked via `explain("executionStats")` to achieve zero COLLSCAN executions on critical paths.

---

## 7. Data Requirements

1. **Real-World Authenticity**: All award facts (ceremony numbers, dates, categories, nominees, winners, artist names, work titles) must represent historical reality. Synthetic or generated dummy records for factual domain entities are strictly prohibited.
2. **Fact vs. Metric Distinction**: Primary source facts (e.g., "Adele won Album of the Year at the 59th Annual GRAMMY Awards") must be cleanly partitioned from derived analytical metrics (e.g., "Win-to-nomination conversion ratio = 84.6%"). Derived metrics must be computed via documented aggregation pipelines.
3. **Temporal Coverage**: The dataset must span the modern era of the GRAMMY Awards (with key coverage from 1959 through 2024), ensuring long-term longitudinal analysis across changing category formats.

---

## 8. Source Requirements

All external data utilized in this system must follow a strict hierarchy of trust:
1. **Tier 1 (Official Recording Academy Sources)**: Official GRAMMY.com award databases, ceremony programs, press announcements, and eligibility rulebooks.
2. **Tier 2 (Reputable Structured Repositories)**: Verified, open-access academic and data science repositories (e.g., curated Kaggle datasets with verifiable origins, MusicBrainz open database, Discogs open API dumps).
3. **Tier 3 (Authoritative Music Industry Publications)**: Billboard chart archives, Nielsen telecast viewership records, and Library of Congress national recording registries.

For every external dataset ingested, the system requires a logged record containing:
- Formal source name and organization.
- Exact source URL or repository URI.
- Specific dataset title and release version/snapshot date.
- Explicit license classification (CC-BY, CC0, ODC-By, Open Data, or Custom Academic).
- Required attribution statement.
- Academic compatibility assessment.
- Known domain limitations and data hygiene caveats.
- List of system collections populated or informed by the source.

---

## 9. Licensing & Intellectual Property Compliance

1. **No Assumed Permission**: Public accessibility on the web or Kaggle does NOT grant automatic permission. Every dataset must have its license terms explicitly parsed and audited.
2. **Ambiguity Resolution Protocol**: If an external dataset lacks a clear license or contains ambiguous terms, it must be flagged as `UNDER_REVIEW` and excluded from production loading until human review confirms academic fair-use compatibility.
3. **Zero Proprietary Infringement**: No confidential, paywalled, or proprietary trade-secret data may be ingested into the repository.
4. **Attribution Manifest**: An open-source attribution ledger must be published and maintained in [`docs/data_sources_and_licensing.md`](../data_sources_and_licensing.md).

---

## 10. Validation Requirements

1. **Automated Schema Compliance**: Every collection must have a formal JSON Schema draft defining required fields, BSON data types, string constraints, and numeric ranges.
2. **Pre-Flight Validation Harness**: An automated Python test suite (`scripts/validation/validate_system.py`) must validate all documents against their respective schemas prior to database insertion.
3. **Deterministic Global Identifiers**: Entity references must utilize standardized ID formats:
   - Ceremonies: `CEREMONY_{NNN}`
   - Categories: `CAT_{SLUG}`
   - Nominations: `NOM_{CEREMONY}_{CAT}_{SEQ}`
   - Winners: `WIN_{NOMINATION_ID}`
   - Creators: `CRT_{SLUG}`
   - Works: `WRK_{SLUG}`
   - Labels: `LBL_{SLUG}`
   - Venues: `VEN_{SLUG}`
4. **Referential Integrity Audits**: Automated cross-database tests must verify that foreign keys in child collections resolve to legitimate parent primary keys across database boundaries.
5. **Continuous Integration (CI)**: GitHub Actions workflows must execute full test suites on every push to ensure zero regression.

---

## 11. Security & Secrets Management Requirements

1. **Zero Secret Exposure**: Passwords, API keys, and MongoDB Atlas connection strings must never be committed to Git or pushed to remote repositories.
2. **Strict Environment Segregation**: Credentials must reside exclusively in local, uncommitted `.env` files.
3. **Repository Exclusion Enforcements**: The repository's [`.gitignore`](../../.gitignore) must enforce exclusion of `.env`, `.env.*`, `*.pem`, `*.key`, virtual environments, and intermediate database dumps.
4. **Automated Leak Detection**: Regular git tree scans (`git grep`) and pre-commit checks must be executed to ensure zero accidental credential leakage.

---

## 12. Human Approval Checkpoints & Phase Governance

The project strictly adheres to phased execution governance. Transition from one phase to the next requires explicit human review and authorization:

```
[Phase 1: Requirements Freeze] ──(Approval Checkpoint)──► [Phase 2: Source Verification]
         │                                                            │
(Approval Checkpoint)                                        (Approval Checkpoint)
         ▼                                                            ▼
[Phase 3: EER Modeling]       ──(Approval Checkpoint)──► [Phase 4: Relational Model]
         │                                                            │
(Approval Checkpoint)                                        (Approval Checkpoint)
         ▼                                                            ▼
[Phase 5: Normalization]      ──(Approval Checkpoint)──► [Phase 6: MongoDB Document Model]
         │                                                            │
(Approval Checkpoint)                                        (Approval Checkpoint)
         ▼                                                            ▼
[Phase 7: Database Deploy]    ──(Approval Checkpoint)──► [Phase 8: Validation & CRUD]
         │                                                            │
(Approval Checkpoint)                                        (Approval Checkpoint)
         ▼                                                            ▼
[Phase 9: Advanced Aggregations] ──(Approval)──► [Phase 10: Final Presentation & Defense]
```

### Protocol Invariant:
At the conclusion of each phase:
- Completed deliverables must be reported with direct markdown file links.
- Unresolved issues and technical risks must be declared.
- The agent must **STOP** and await explicit user command before performing any action in the subsequent phase.
