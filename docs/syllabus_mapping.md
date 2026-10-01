# Curriculum Syllabus Mapping (Modules 1–10)

This document provides a detailed mapping between the ten modules of the Advanced Database Management Systems syllabus and the concrete academic deliverables, theoretical models, code artifacts, and analytical queries in the **GRAMMY Awards Information & Analytics System**.

---

## Module 1: Relational Query Languages, Relational Algebra & EER Modeling
- **Syllabus Topics**:
  - Relational query languages, relational algebra ($\sigma, \pi, \cup, \cap, -, \times, \bowtie, \rho, \div$).
  - EER modeling: subclasses, superclasses, inheritance, specialization (overlapping vs disjoint), generalization, aggregation, categories/union types, naming conventions.
- **Project Deliverables**:
  1. **EER Conceptual Model**: [`docs/eer_diagrams/conceptual_eer_spec.md`](docs/eer_diagrams/conceptual_eer_spec.md).
  2. **Relational Schema Translation**: Mapping EER entities and inheritance hierarchies into equivalent relational DDL ([`schemas/relational_ddl/relational_reference_schema.sql`](schemas/relational_ddl/relational_reference_schema.sql)).
  3. **Formal Relational Algebra Suite**: 10 formal algebraic expressions with step-by-step query trees demonstrating selection ($\sigma$), projection ($\pi$), equijoin ($\bowtie$), Cartesian product ($\times$), set difference ($-$), and division ($\div$) to answer questions such as *"Find creators who have won in every category within the Pop field"*.

---

## Module 2: Functional Dependencies & Schema Refinement (1NF, 2NF)
- **Syllabus Topics**:
  - Functional dependencies (FDs), Armstrong's Axioms (reflexivity, augmentation, transitivity, pseudo-transitivity, union, decomposition).
  - Closure of attribute sets ($X^+$), minimal cover ($F_{min}$), candidate key derivation.
  - 1NF (atomic domains) and 2NF (elimination of partial functional dependencies on composite keys).
- **Project Deliverables**:
  1. **Formal FD Specification**: Mathematical formulation of 25+ functional dependencies governing the flat/unnormalized GRAMMY awards dataset.
  2. **1NF Transformation**: Identifying non-atomic attributes (e.g., comma-separated credits, composite billing lines) and normalizing to first normal form.
  3. **2NF Decomposition**: Identifying partial key dependencies in composite key relations like `NOMINATION_CREDIT(nomination_id, creator_id, work_id)` and proving full functional dependency decomposition.

---

## Module 3: Higher Normal Forms (3NF, BCNF, 4NF, 5NF) & Justified Denormalization
- **Syllabus Topics**:
  - 3NF (transitive dependency removal), Boyce-Codd Normal Form (BCNF: strict superkey condition for every determinant).
  - Multivalued dependencies ($X \twoheadrightarrow Y$) and Fourth Normal Form (4NF).
  - Join dependencies ($\bowtie[R_1, \dots, R_k]$) and Fifth Normal Form (5NF / Project-Join Normal Form).
  - Lossless-join decomposition algorithms and dependency preservation.
  - Controlled and justified denormalization.
- **Project Deliverables**:
  1. **BCNF Decomposition**: Mathematical proof decomposing transitive dependencies (e.g., `category_id -> field_id` and `venue_id -> city, state`) into BCNF relations while evaluating dependency preservation.
  2. **4NF & 5NF Analysis**: Identification of independent multi-valued dependencies (e.g., an artist having multiple independent genres and multiple independent record labels) and projection-join dependencies.
  3. **Academic Denormalization Rationale**: Comprehensive analysis justifying why specific BCNF relations are strategically denormalized into embedded BSON documents in MongoDB to eliminate multi-table network joins for high-velocity query patterns.

---

## Module 4: Transactions, ACID Properties & Schedules
- **Syllabus Topics**:
  - Concept of transactions, ACID properties (Atomicity, Consistency, Isolation, Durability).
  - Transaction lifecycle and state transitions (Active, Partially Committed, Committed, Failed, Aborted).
  - Schedules: serial schedules, non-serial schedules, conflict serializability, view serializability, precedence/serialization graphs.
- **Project Deliverables**:
  1. **Multi-Document ACID Transactions**: Python implementation using MongoDB client sessions (`start_session()`, `session.start_transaction()`, `commit_transaction()`, `abort_transaction()`) demonstrating atomic nomination submission and audit verification.
  2. **Conflict Serializability Proof**: Precedence graphs constructed from simulated concurrent read/write schedules on ballot counters, proving conflict-equivalence to a serial schedule.
  3. **Transaction State Machine**: Formal state transition diagram logging transaction failure handling and rollback mechanisms.

---

## Module 5: Concurrency Control & Deadlock Handling
- **Syllabus Topics**:
  - Shared locks ($S$) and Exclusive locks ($X$), Lock conversion.
  - Strict Two-Phase Locking (Strict 2PL) protocol guaranteeing conflict serializability and avoiding cascading aborts.
  - Timestamp ordering protocols (Thomas Write Rule).
  - Deadlock prevention (Wait-Die, Wound-Wait) and Deadlock detection (Wait-For-Graphs, cycle detection algorithms).
- **Project Deliverables**:
  1. **Concurrency Simulator**: Multi-threaded Python test harness executing concurrent ticket votes on award categories under Strict 2PL.
  2. **Wait-For-Graph (WFG) Engine**: Programmatic cycle detection algorithm detecting deadlocks in resource allocation graphs.
  3. **WiredTiger Concurrency Diagnostics**: Monitoring lock latencies, read tickets, and write tickets using `serverStatus().wiredTiger.concurrentTransactions`.

---

## Module 6: Storage Architecture, RAID & File Organization
- **Syllabus Topics**:
  - Storage hierarchies, disk block allocation, RAID architectures (RAID 0, 1, 5, 10) evaluating reliability vs performance.
  - Fixed-length vs variable-length records, slotted-page architecture, block headers.
  - File organization: heap files, sorted files, hashed files, B+ Trees.
  - Metadata, system catalogs, and data dictionaries.
- **Project Deliverables**:
  1. **Slotted-Page Storage Analysis**: Mathematical calculation of byte-level page packing, record pointer offsets, and fragmentation in WiredTiger 4KB/32KB leaf pages.
  2. **RAID Topology Tradeoff Study**: Performance and fault-tolerance modeling for high-throughput ballot ingest comparing RAID 10 vs RAID 5.
  3. **System Catalog Exploration**: Automated script querying MongoDB internal metadata (`system.views`, `collStats`, index sizes, storage sizing).

---

## Module 7: Recovery Concepts, Logging & Disaster Resilience
- **Syllabus Topics**:
  - Failure classifications (Transaction failure, System crash, Catastrophic media failure).
  - Write-Ahead Logging (WAL), Log records: $\langle T, X, V_{old}, V_{new} \rangle$, Undo and Redo operations.
  - Checkpoint strategies (Strict vs Fuzzy Checkpoints).
  - Shadow paging vs In-place update with logging.
  - Backup strategies, point-in-time recovery, and catastrophic failure recovery.
- **Project Deliverables**:
  1. **MongoDB Journaling & WAL Drill**: Practical experiment validating durability by killing active MongoDB process during writes and inspecting WiredTiger journal replay.
  2. **Automated Backup & Restore Suite**: Scripted execution of full and incremental backups using `mongodump` and point-in-time restoration via `mongorestore`.
  3. **Disaster Recovery Playbook**: Step-by-step catastrophic recovery plan with target RPO (Recovery Point Objective) and RTO (Recovery Time Objective).

---

## Module 8: NoSQL Foundations, MongoDB Architecture & Atlas
- **Syllabus Topics**:
  - NoSQL paradigms (Key-Value, Columnar, Graph, Document).
  - CAP Theorem (Consistency, Availability, Partition Tolerance) and PACELC theorem.
  - MongoDB Architecture: WiredTiger engine, BSON serialization, memory-mapped files, write concern and read concern.
  - Replica sets (Primary, Secondaries, Raft-like election algorithm, heartbeat mechanics).
  - Sharding architecture (mongos routing, config database, shard keys, chunk migrations).
  - Cloud deployment: MongoDB Atlas and MongoDB Compass GUI.
- **Project Deliverables**:
  1. **Distributed Architecture Document**: Theoretical analysis of MongoDB Atlas 3-node replica sets under CAP/PACELC constraints.
  2. **WiredTiger Eviction & Cache Benchmark**: Profiling cache usage and compression algorithms (Snappy vs zlib).
  3. **MongoDB Compass Profiling**: Visual schema analysis, index usage reports, and document distribution graphs.

---

## 9. Module 9: MongoDB CRUD & Management
- **Syllabus Topics**:
  - Database, collection, and document management.
  - CRUD operations: `insertOne`, `insertMany`, `find`, `updateOne`, `updateMany`, `replaceOne`, `deleteOne`, `deleteMany`.
  - Filter operators (`$eq`, `$gt`, `$gte`, `$in`, `$regex`), logical operators (`$and`, `$or`, `$not`, `$nor`), element operators (`$exists`, `$type`).
  - Import and export tools (`mongoimport`, `mongoexport`).
- **Project Deliverables**:
  1. **Comprehensive CRUD Demonstration Suite**: Python script testing complete CRUD lifecycle across all 5 databases.
  2. **Bulk Ingestion Pipeline**: High-throughput insertion using `bulkWrite` with ordered and unordered execution semantics.
  3. **Export/Import Validation**: Verified data dumps reproducing collections from raw JSON exports.

---

## 10. Module 10: Advanced Querying & Aggregation Framework
- **Syllabus Topics**:
  - MongoDB Aggregation Framework: Pipeline architecture.
  - Stages: `$match`, `$project`, `$group`, `$sort`, `$limit`, `$skip`, `$unwind`, `$lookup`, `$facet`, `$bucket`, `$addFields`, `$replaceRoot`.
  - Array operations: `$elemMatch`, `$filter`, `$map`, `$reduce`, `$size`.
  - Indexing: Single field, compound indexes, multikey indexes, text indexes.
  - Query optimization and benchmarking via `explain("executionStats")`.
- **Project Deliverables**:
  1. **15 Advanced Analytical Pipelines**: Cross-collection and cross-category multi-stage aggregation queries answering complex domain questions:
     - Top artists with highest win-to-nomination conversion ratios across 30+ years.
     - Longitudinal analysis of genre field proliferation.
     - Producer credit concentration in Album of the Year winners.
     - Multi-faceted analysis (`$facet`) of telecast ratings correlated with award categories.
  2. **Index Optimization Benchmarks**: Comparing execution statistics (COLLSCAN vs IXSCAN, `totalDocsExamined` vs `nReturned`) before and after applying compound indexes.
