# Comprehensive Viva Voce Preparation Guide & Examination Handbook

> **Course**: Advanced Database Management Systems (ADBMS) — Graduate Capstone  
> **System Title**: GRAMMY Awards Information & Analytics System  
> **Target Engine**: MongoDB Atlas (`Cluster0`) & WiredTiger Engine  
> **Verification Status**: **100% Certified** across 670 Automated Tests (629 baseline + 41 capstone verification)  
> **Authors**: Five-Member Distributed Database Team (Members 1–5)  
> **Scope**: Master Question Bank (230 Project-Grounded Questions & Model Answers) + Five-Member Viva Responsibility Matrix  

---

# Table of Contents
1. [Five-Member Viva Responsibility & Defense Matrix](#five-member-viva-responsibility--defense-matrix)
2. [Section 1: 50 Basic Viva Questions & Answers](#section-1-50-basic-viva-questions--answers)
3. [Section 2: 50 Intermediate Viva Questions & Answers](#section-2-50-intermediate-viva-questions--answers)
4. [Section 3: 30 Advanced Viva Questions & Answers](#section-3-30-advanced-viva-questions--answers)
5. [Section 4: Dedicated Questions on Conceptual EER Modeling](#section-4-dedicated-questions-on-conceptual-eer-modeling)
6. [Section 5: Dedicated Questions on Functional Dependencies & Normalization](#section-5-dedicated-questions-on-functional-dependencies--normalization)
7. [Section 6: Dedicated Questions on MongoDB Document Modeling](#section-6-dedicated-questions-on-mongodb-document-modeling)
8. [Section 7: Dedicated Questions on Aggregation Pipelines](#section-7-dedicated-questions-on-aggregation-pipelines)
9. [Section 8: Dedicated Questions on Multi-Document ACID Transactions](#section-8-dedicated-questions-on-multi-document-acid-transactions)
10. [Section 9: Dedicated Questions on Concurrency Control & Serializability](#section-9-dedicated-questions-on-concurrency-control--serializability)
11. [Section 10: Dedicated Questions on Physical Storage Architecture & RAID](#section-10-dedicated-questions-on-physical-storage-architecture--raid)
12. [Section 11: Dedicated Questions on Crash Recovery & ARIES](#section-11-dedicated-questions-on-crash-recovery--aries)
13. [Section 12: Dedicated Questions on Data Sources & Ingestion](#section-12-dedicated-questions-on-data-sources--ingestion)
14. [Section 13: Dedicated Questions on Licensing & Provenance](#section-13-dedicated-questions-on-licensing--provenance)

---

# Five-Member Viva Responsibility & Defense Matrix

| Team Member | Database Assigned | Collection Portfolio | Primary Syllabus Modules | Key Defense Specialties | Target Scripts & Test Artifacts |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Member 1** | `grammy_history_db` | `ceremonies`, `venues`, `telecast_broadcasters`, `viewership_ratings`, `ceremony_hosts`, `historic_milestones`, `timeline_historical_eras`, `academy_leadership`, `press_media_accreditations`, `lifetime_achievement_honors` | **Module 6**: Storage Architecture & RAID<br>**Module 7**: Recovery Concepts, WAL, ARIES | - Physical block layout & Slotted-Page architecture<br>- RAID 0/1/5/6/10 write penalty equations<br>- WiredTiger Snappy compression (32.9% savings)<br>- Write-Ahead Logging & 3 phases of ARIES<br>- Bitwise crash drill restoration (SHA-256 parity) | `scripts/storage/generate_data_dictionary.py`<br>`scripts/recovery/controlled_recovery_drill.py`<br>`tests/test_storage.py`<br>`tests/test_recovery.py` |
| **Member 2** | `grammy_categories_db` | `award_fields`, `award_categories`, `category_lineage`, `eligibility_rules`, `voting_procedures`, `category_quotas_limits`, `craft_credit_definitions`, `discontinued_categories`, `merged_split_history`, `special_merit_categories` | **Module 1**: Relational Algebra & EER<br>**Module 2**: FDs, Armstrong's Axioms, 1NF/2NF | - Conceptual EER modeling & weak entities<br>- Specialization hierarchies & categories/unions<br>- Conceptual aggregation modeling<br>- Functional dependency closure sets ($F^+$)<br>- Minimal Cover ($F_{min}$) derivation algorithms | `docs/eer-design.md`<br>`relational-model/`<br>`tests/test_relational_model.py`<br>`tests/test_functional_dependencies.py` |
| **Member 3** | `grammy_nominations_db` | `nomination_entries`, `nominated_works`, `nomination_credits`, `submission_batches`, `voter_screening_batches`, `tied_nominations`, `nomination_audit_logs`, `genre_classifications`, `first_time_nominees`, `multi_nomination_packages` | **Module 4**: ACID Transactions & Sessions<br>**Module 5**: Concurrency Control & Deadlocks | - Multi-document ACID transactions on replica sets<br>- Snapshot isolation & write concern majority<br>- Strict 2PL locking protocols & lock tables<br>- Wait-For Graph (WFG) cycle detection<br>- OCC collision handling vs. WiredTiger MVCC | `scripts/transactions/run_transaction_demo.py`<br>`scripts/concurrency/simulate_concurrency.py`<br>`tests/test_transactions.py`<br>`tests/test_concurrency.py` |
| **Member 4** | `grammy_winners_db` | `winner_records`, `big_four_sweeps`, `record_breakers`, `acceptance_speeches`, `trophy_tracking`, `consecutive_winners`, `hall_of_fame_inductions`, `posthumous_awards`, `historic_win_benchmarks`, `winner_press_releases` | **Module 9**: MongoDB CRUD & Advanced Querying<br>**Module 10**: Aggregation & Index Optimization | - High-selectivity CRUD operations & projections<br>- Complex operators (`$elemMatch`, `$in`, `$regex`)<br>- Compound B+ tree indexes & ESR rule<br>- Explain plan analysis (`COLLSCAN` to `IXSCAN`)<br>- Multi-stage aggregations (`$facet`, `$bucketAuto`) | `scripts/indexes/verify_indexes.py`<br>`queries/crud/`<br>`queries/advanced/`<br>`queries/aggregation/`<br>`tests/test_indexing.py`<br>`tests/test_aggregation_pipelines.py` |
| **Member 5** | `grammy_creators_db` | `artists`, `producers`, `audio_engineers`, `songwriters_composers`, `arrangers_conductors`, `record_labels`, `musical_groups`, `group_memberships`, `creator_collaborations`, `creator_discographies` | **Module 3**: 3NF, BCNF, 4NF, 5NF & Denormalization<br>**Cross-DB Integration**: Join Federation | - Lossless join BCNF decomposition proofs<br>- Multivalued dependencies (4NF) & PJNF (5NF)<br>- Justified denormalization under 16 MB limit<br>- Server-side `$lookup` limits (`AtlasError 8000`)<br>- Application-level distributed joins in PyMongo | `scripts/integration/cross_database_validation.py`<br>`docs/integration.md`<br>`tests/test_normalization_proofs.py`<br>`tests/test_cross_database.py` |

---

# Section 1: 50 Basic Viva Questions & Answers

#### Q1: What is the primary objective of this project?
**Answer**: To engineer an enterprise-scale, distributed database system for the Recording Academy's GRAMMY Awards (1959–present), bridging foundational relational DBMS theory (EER, 1NF–5NF, relational algebra, ARIES, 2PL) with modern distributed NoSQL paradigms (MongoDB Atlas, WiredTiger MVCC, multi-document ACID transactions).

#### Q2: Which database engine is used in this project?
**Answer**: MongoDB Atlas (`Cluster0`, a 3-node replica set on AWS `us-east-1`) running the WiredTiger storage engine with Snappy block compression.

#### Q3: Why is the system partitioned into five databases instead of a single database?
**Answer**: To enforce microservice domain boundaries, separation of concerns, and team member ownership across historical events (`grammy_history_db`), taxonomy bylaws (`grammy_categories_db`), nomination workflows (`grammy_nominations_db`), certified winners (`grammy_winners_db`), and creator directories (`grammy_creators_db`).

#### Q4: How many total collections and documents exist across the system?
**Answer**: Exactly 50 collections (10 per database) and 5,190 schema-validated documents, certified via `scripts/audit/final_audit.py` and `docs/storage/data_dictionary.json`.

#### Q5: What is the document quota per collection, and did every collection satisfy it?
**Answer**: The academic quota is a minimum of 50 documents per collection. All 50 collections satisfy this, holding between 50 and 500 documents.

#### Q6: What is the field count requirement per document?
**Answer**: The requirement is a minimum of 10 meaningful domain fields per document. Our documents contain 12 to 13 fields across all 50 collections.

#### Q7: What are the names of the five databases?
**Answer**: `grammy_history_db`, `grammy_categories_db`, `grammy_nominations_db`, `grammy_winners_db`, and `grammy_creators_db`.

#### Q8: How many tests exist in the automated test suite and what is the pass rate?
**Answer**: 629 automated pytest tests spanning 24 test suites for Phases 1–28, expanding to 670 passing tests across 25 test suites with the Phase 29–30 capstone verification suite, achieving a 100% pass rate.


#### Q9: What is the purpose of the `_source_provenance` subdocument?
**Answer**: It guarantees 100% data auditability and lineage tracking on every document, recording `source_id`, `source_name`, `license_type`, `provenance_tier`, `attribution`, and `acquired_timestamp`.

#### Q10: What primary sources provided data for this project?
**Answer**: The Recording Academy official archives (`grammy.com`), Kaggle Grammy Awards Dataset (Robyn Ritchie), MetaBrainz MusicBrainz (`musicbrainz.org`), Nielsen Media Research, and Wikimedia Wikidata.

#### Q11: What legal doctrine protects the factual award data in this project?
**Answer**: The United States Supreme Court doctrine in *Feist Publications, Inc. v. Rural Telephone Service Co.* (499 U.S. 340), which establishes that historical and factual data cannot be copyrighted.

#### Q12: Under what license are the Kaggle and MusicBrainz data incorporated?
**Answer**: Creative Commons Zero 1.0 Universal (CC0) and open database fair use.

#### Q13: What is an EER diagram?
**Answer**: An Enhanced Entity-Relationship diagram that extends traditional ER models with specialization, generalization, categorizations (union types), and conceptual aggregation.

#### Q14: Name one weak entity in our EER model and its identifying owner entity.
**Answer**: `VIEWERSHIP_RATING` in `grammy_history_db` is a weak entity, identified through its identifying relationship with the strong parent entity `CEREMONY`.

#### Q15: What is a specialization hierarchy in our EER design?
**Answer**: `CREATOR` is generalized into `INDIVIDUAL_CREATOR` and `ORGANIZATIONAL_CREATOR` with disjoint $[d]$ and total $[t]$ constraints.

#### Q16: What is a union type (category) in our EER model?
**Answer**: `AWARD_RECIPIENT = ARTIST \cup MUSICAL_GROUP`, allowing either a solo human artist or a multi-member group to be credited as a legal award winner.

#### Q17: What is conceptual aggregation in EER?
**Answer**: Treating a relationship between multiple entities as a higher-level composite entity. We modeled $\text{AGGREGATE}(\text{CREATOR}, \text{WORK}, \text{AWARD\_CATEGORY})$, which in turn participates in the `NOMINATION_CREDIT` relationship.

#### Q18: What are the seven fundamental operations of Relational Algebra?
**Answer**: Selection ($\sigma$), Projection ($\pi$), Cartesian Product ($\times$), Set Union ($\cup$), Set Difference ($-$), Natural Join ($\bowtie$), and Relational Division ($\div$).

#### Q19: Which complex query did we formulate using Relational Division ($\div$)?
**Answer**: Finding all creators who have earned nominations in *all* Big Four General Field categories: $\pi_{\text{creator\_id}, \text{category\_id}}(\text{NOMINATION\_CREDITS}) \div \pi_{\text{category\_id}}(\text{BIG\_FOUR\_CATEGORIES})$.

#### Q20: What is a Functional Dependency (FD)?
**Answer**: A constraint between two sets of attributes $X$ and $Y$ in relation $R$, denoted $X \rightarrow Y$, stating that if two tuples agree on $X$, they must agree on $Y$.

#### Q21: What are Armstrong's Axioms?
**Answer**: The sound and complete inference rules for FDs: Reflexivity ($Y \subseteq X \implies X \rightarrow Y$), Augmentation ($X \rightarrow Y \implies XZ \rightarrow YZ$), and Transitivity ($X \rightarrow Y \wedge Y \rightarrow Z \implies X \rightarrow Z$).

#### Q22: What is a Minimal Cover ($F_{min}$)?
**Answer**: A canonical equivalent set of functional dependencies where every RHS is a single attribute, no LHS has extraneous attributes, and no dependency is redundant.

#### Q23: Define First Normal Form (1NF).
**Answer**: A relation is in 1NF if and only if all domain attribute values are atomic (indivisible scalars) and there are no repeating groups or composite arrays.

#### Q24: Define Second Normal Form (2NF).
**Answer**: A relation is in 2NF if it is in 1NF and every non-prime attribute is fully functionally dependent on the primary key (no partial key dependencies).

#### Q25: Define Third Normal Form (3NF).
**Answer**: A relation is in 3NF if it is in 2NF and for every non-trivial FD $X \rightarrow A$, either $X$ is a superkey or $A$ is a prime attribute (no transitive dependencies).

#### Q26: Define Boyce-Codd Normal Form (BCNF).
**Answer**: A relation is in BCNF if for every non-trivial functional dependency $X \rightarrow Y$, the determinant $X$ is a superkey.

#### Q27: Define Fourth Normal Form (4NF).
**Answer**: A relation is in 4NF if it is in BCNF and for every non-trivial Multivalued Dependency $X \twoheadrightarrow Y$, $X$ is a superkey.

#### Q28: Define Fifth Normal Form (5NF / Project-Join Normal Form).
**Answer**: A relation is in 5NF if every non-trivial join dependency $\bowtie[R_1, R_2, \dots, R_k]$ in $R$ is implied by the candidate keys of $R$.

#### Q29: What is controlled denormalization?
**Answer**: The deliberate, academically justified introduction of redundancy into physical document schemas (e.g., embedding artist stage names into nomination records) to eliminate multi-table joins and optimize read throughput.

#### Q30: What is the maximum document size in MongoDB?
**Answer**: 16 Megabytes (16,777,216 bytes) in BSON representation.

#### Q31: How do we prevent documents from exceeding the 16 MB BSON limit?
**Answer**: By referencing unbounded 1:N relationships (such as thousands of nominations per ceremony) using universal string foreign keys rather than embedding them as unbounded arrays.

#### Q32: What is `$jsonSchema` validation in MongoDB?
**Answer**: A server-side collection validator that enforces structural constraints, mandatory fields, BSON data types, regex patterns, and numeric ranges on every write operation.

#### Q33: What is the deterministic regex format for `ceremony_id`?
**Answer**: `^CEREMONY_\d{3}$` (e.g., `CEREMONY_001`, `CEREMONY_065`).

#### Q34: What is the deterministic regex format for `artist_id`?
**Answer**: `^CRT_[A-Z0-9_]+$` (e.g., `CRT_STEVIE_WONDER`, `CRT_TAYLOR_SWIFT`).

#### Q35: What is the deterministic regex format for `category_id`?
**Answer**: `^CAT_[A-Z0-9_]+$` (e.g., `CAT_ALBUM_OF_THE_YEAR`, `CAT_RECORD_OF_THE_YEAR`).

#### Q36: What is the difference between an embedded and a referenced relationship in MongoDB?
**Answer**: Embedded relationships store related data directly inside parent documents as nested subdocuments or arrays (optimizing single-document atomic reads). Referenced relationships store the primary key of another document, requiring a join or secondary lookup.

#### Q37: What is an index scan (`IXSCAN`) versus a collection scan (`COLLSCAN`)?
**Answer**: A `COLLSCAN` reads every document in a collection sequentially from storage. An `IXSCAN` traverses a B+ tree index structure directly to locate matching document record IDs, drastically reducing disk I/O.

#### Q38: How many custom indexes were created in our project?
**Answer**: 44 custom indexes active on MongoDB Atlas, eliminating `COLLSCAN` across all benchmark queries.

#### Q39: What is the ESR rule in MongoDB indexing?
**Answer**: Equality, Sort, Range. Compound index fields should be ordered with exact equality fields first, sort fields second, and range filter fields last.

#### Q40: What are ACID properties in database transactions?
**Answer**: Atomicity (all-or-nothing), Consistency (state transitions respect constraints), Isolation (concurrent operations do not interfere), and Durability (committed data persists across crashes).

#### Q41: Does MongoDB support multi-document ACID transactions?
**Answer**: Yes, MongoDB has supported multi-document ACID transactions across replica sets since version 4.0, managed via client sessions.

#### Q42: What read concern and write concern are used in our ACID transaction demo?
**Answer**: `ReadConcern("snapshot")` and `WriteConcern(w="majority", j=True)`.

#### Q43: What is Two-Phase Locking (2PL)?
**Answer**: A concurrency control protocol guaranteeing conflict serializability where a transaction acquires locks during a growing phase and releases them during a shrinking phase without acquiring new locks.

#### Q44: What is Strict 2PL?
**Answer**: A variant of 2PL where all exclusive (X) locks held by a transaction are held until the transaction terminates (commit or abort), preventing cascading aborts.

#### Q45: What is a Wait-For Graph (WFG)?
**Answer**: A directed graph $G = (V, E)$ where vertices represent active transactions and edges $T_i \rightarrow T_j$ indicate that $T_i$ is waiting for a lock held by $T_j$. A cycle in the WFG indicates a deadlock.

#### Q46: What storage engine does MongoDB use in our deployment?
**Answer**: WiredTiger storage engine.

#### Q47: What compression algorithm is enabled by default in WiredTiger collection storage?
**Answer**: Snappy block compression (with prefix compression for B+ tree index keys).

#### Q48: What is Write-Ahead Logging (WAL)?
**Answer**: A recovery fundamental requiring that log records describing database updates must be written to non-volatile storage before the corresponding dirty data pages are flushed to disk.

#### Q49: What does the ARIES recovery algorithm stand for?
**Answer**: Algorithm for Recovery and Isolation Exploiting Semantics.

#### Q50: How are secrets and database credentials managed in our project repository?
**Answer**: Cluster credentials reside exclusively in a local `.env` file that is strictly gitignored. Only sanitized `.env.example` templates are tracked, ensuring zero cleartext credentials in Git history.

---

# Section 2: 50 Intermediate Viva Questions & Answers

#### Q51: How did the team resolve the MongoDB Atlas M0 cross-database `$lookup` limitation?
**Answer**: Atlas free-tier M0 clusters disallow cross-database `$lookup` aggregations (`AtlasError 8000`). We engineered application-level distributed join federation in PyMongo: fetching batch foreign keys and querying peer collections via `$in` clauses over secondary B+ tree indexes in $< 15\text{ ms}$.

#### Q52: What was the measured referential integrity outcome of our cross-database audit?
**Answer**: 100% referential closure across all 11 cross-database foreign key pathways, with exactly 0 orphan records verified by `scripts/integration/cross_database_validation.py`.

#### Q53: Explain the difference between Basic 2PL, Strict 2PL, and Rigorous 2PL.
**Answer**: In Basic 2PL, locks can be released anytime in the shrinking phase. In Strict 2PL, exclusive (X) locks are held until commit/abort, eliminating cascading aborts. In Rigorous 2PL, *both* shared (S) and exclusive (X) locks are held until transaction termination, guaranteeing strict serializability.

#### Q54: What is Multiple Granularity Locking (MGL)?
**Answer**: A hierarchical locking protocol that allows locking at different levels of granularity (database, collection, document). It uses intention locks (IS, IX, SIX) on higher levels to signal intentions before locking child nodes with S or X locks.

#### Q55: Is an Intention Exclusive (IX) lock compatible with an Intention Shared (IS) lock?
**Answer**: Yes, IX and IS locks are compatible. They allow concurrent transactions to access different subordinate documents within the same collection.

#### Q56: What deadlock victim selection policies were analyzed in Module 5?
**Answer**: Wait-Die (non-preemptive, older waits, younger dies) and Wound-Wait (preemptive, older wounds/aborts younger, younger waits).

#### Q57: How does WiredTiger avoid table-level locks during concurrent writes?
**Answer**: WiredTiger uses lock-free Multi-Version Concurrency Control (MVCC) and document-level allocation with hazard pointers. When two transactions modify the same document, WiredTiger detects a `WriteConflict` and returns an error for the application to retry.

#### Q58: What is the empirical latency of our multi-document ACID transaction commit?
**Answer**: 73.42 milliseconds across three collections on our Atlas replica set, certified in `tests/test_transactions.py`.

#### Q59: What happens during our ACID transaction rollback scenario?
**Answer**: We simulate an intentional duplicate key collision on the audit ledger. The transaction aborts via PyMongo session, rolling back modifications in `controlled_tx_ballots` and `controlled_tx_trophies` with zero orphan state.

#### Q60: Explain the three phases of the ARIES recovery algorithm.
**Answer**:
1. **Analysis Phase**: Scans WAL forward from the last checkpoint to identify active transactions (Transaction Table) and dirty pages (Dirty Page Table).
2. **Redo Phase**: "Repeats history" by scanning forward to re-apply all logged updates, including those of aborted transactions.
3. **Undo Phase**: Scans backward from the crash point, rolling back the actions of active (loser) transactions and logging Compensation Log Records (CLRs).

#### Q61: What is a Compensation Log Record (CLR) in ARIES?
**Answer**: A log record written during the Undo phase that records the undoing of an operation. CLRs are never undone, preventing infinite loops during repeated crashes during recovery.

#### Q62: What is the Write-Ahead Undo Rule?
**Answer**: The undo log record must be written to non-volatile disk before the corresponding dirty data page is written to disk, ensuring uncommitted updates can always be rolled back.

#### Q63: What is the Commit Redo Rule?
**Answer**: All redo log records for a transaction must be flushed to disk before the transaction's commit request is acknowledged to the client, guaranteeing durability.

#### Q64: What is the difference between Strict Checkpointing and Non-Quiescent (Fuzzy) Checkpointing?
**Answer**: Strict checkpointing freezes all transaction processing and flushes all dirty pages to disk. Fuzzy checkpointing flushes dirty pages in the background without halting transactions, recording active transactions and dirty page state in the checkpoint record.

#### Q65: How often does WiredTiger take periodic fuzzy checkpoints?
**Answer**: Every 60 seconds by default, or when 2 GB of journal data has accumulated.

#### Q66: What was the empirical compression ratio achieved by WiredTiger on our data?
**Answer**: A 32.9% reduction in physical storage footprint: 4.06 MB uncompressed BSON was compressed to 2.72 MB on disk via Snappy block compression.

#### Q67: What is the slotted-page architecture?
**Answer**: A page storage layout where a page contains a header with an array of slot pointers (offset and length) growing from the top down, while variable-length records grow from the bottom up. This guarantees stable Record IDs (`page_number:slot_index`) despite record relocations or defragmentation.

#### Q68: Calculate the write penalty for RAID 5.
**Answer**: A small random write in RAID 5 requires 4 I/O operations: read old data, read old parity, write new data, write new parity ($P_{new} = D_{old} \oplus D_{new} \oplus P_{old}$).

#### Q69: Calculate the write penalty for RAID 6 and RAID 10.
**Answer**: RAID 6 requires 6 I/O operations (2 reads and 2 writes for dual parity P and Q). RAID 10 requires 2 I/O operations (1 write to the primary disk and 1 write to the mirrored disk).

#### Q70: Why is RAID 10 preferred over RAID 5 for transaction log (WAL) volumes?
**Answer**: RAID 10 has a write penalty of only 2 I/Os without parity calculation latency, whereas RAID 5 suffers a 4 I/O penalty, creating a severe bottleneck for sequential write-intensive WAL journals.

#### Q71: What is the cache hit ratio formula, and what is our target ratio?
**Answer**: $\text{Hit Ratio} = \frac{\text{Cache Hits}}{\text{Cache Hits} + \text{Cache Misses}}$. Our target is $\ge 99.5\%$, ensuring nearly all read operations are served directly from RAM without disk block reads.

#### Q72: Explain the memory hierarchy latency scaling factors from L1 cache to magnetic disk.
**Answer**: L1 cache access takes $\approx 1\text{ ns}$, RAM takes $\approx 100\text{ ns}$, SSD takes $\approx 100\text{ }\mu\text{s}$, and HDD takes $\approx 10\text{ ms}$. Moving from L1 cache to disk represents a scale factor of $10^7$ ($10\text{ million times slower}$).

#### Q73: What is a B+ tree and why is it preferred over a binary search tree for DBMS indexes?
**Answer**: A B+ tree is a self-balancing, multi-way search tree with high fan-out where all keys reside in leaf nodes, linked via sibling pointers for efficient range scans. Its high fan-out minimizes disk block I/Os compared to deep binary search trees.

#### Q74: What is the difference between a B+ tree and an LSM (Log-Structured Merge) Tree?
**Answer**: B+ trees update data in-place and are optimized for read-heavy workloads with predictable index lookups. LSM trees buffer writes in memory (MemTable) and append them sequentially to disk (SSTables) with background compaction, optimizing write-heavy workloads at the expense of read latency.

#### Q75: How does WiredTiger utilize Hazard Pointers?
**Answer**: Hazard pointers provide lock-free reader concurrency by allowing reader threads to mark in-memory pages they are reading, preventing the eviction server from evicting or reclaiming the page until the read completes.

#### Q76: What is the BCNF decomposition algorithm and does it always preserve functional dependencies?
**Answer**: It iteratively decomposes a relation $R$ violating BCNF on $X \rightarrow Y$ into $R_1(X \cup Y)$ and $R_2(R - Y)$. It is guaranteed to be lossless join, but it does NOT always preserve functional dependencies (unlike 3NF decomposition which preserves both).

#### Q77: What is the difference between Conflict Serializability and View Serializability?
**Answer**: A schedule is conflict serializable if it can be transformed into a serial schedule by swapping non-conflicting adjacent operations (verified in polynomial time via Precedence Graph cycle detection). View serializability is less restrictive but testing for view serializability is NP-complete.

#### Q78: What are the two conflicting operations in transaction schedules?
**Answer**: Two operations conflict if they belong to different transactions, access the exact same data item, and at least one of the operations is a write ($W$).

#### Q79: What is the Precedence Graph (Serialization Graph)?
**Answer**: A directed graph whose nodes are transactions, with an edge $T_i \rightarrow T_j$ if an operation of $T_i$ precedes and conflicts with an operation of $T_j$. If the graph contains no cycles, the schedule is conflict serializable.

#### Q80: What is the Thomas Write Rule?
**Answer**: A timestamp ordering rule that ignores obsolete write operations: if transaction $T$ attempts to write $X$ with timestamp $TS(T) < \text{write\_timestamp}(X)$, the write is ignored rather than aborting $T$, preserving view serializability.

#### Q81: What is the Coffman condition set for deadlocks?
**Answer**: Four necessary conditions: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait.

#### Q82: How does our concurrency simulation script demonstrate zero Lost Updates?
**Answer**: 10 concurrent worker threads execute 100 rapid atomic increment updates (`$inc`) against a shared document counter in `grammy_winners_db`. The final counter matches exactly 100, proving atomic serialization without lost increments.

#### Q83: Explain the difference between `$push` and `$addToSet` in MongoDB updates.
**Answer**: `$push` appends an element to an array regardless of whether it already exists (allowing duplicates). `$addToSet` treats the array as a mathematical set, adding the element only if it does not already exist.

#### Q84: How does our project implement optimistic concurrency control (OCC)?
**Answer**: By including a document `version` number in update criteria (`{"_id": doc_id, "version": current_version}`) and incrementing it atomically (`{"$inc": {"version": 1}}`). If another write modified the document, the update matches 0 documents and triggers an application retry.

#### Q85: What is the purpose of the `$facet` aggregation stage?
**Answer**: `$facet` executes multiple aggregation sub-pipelines within a single pipeline stage over the exact same input documents, enabling multi-dimensional analytics (e.g., genre distributions and rating stats) in a single roundtrip.

#### Q86: What is the purpose of the `$bucketAuto` stage?
**Answer**: It automatically partitions input documents into a specified number of contiguous buckets based on a specified field, attempting to evenly distribute documents across buckets.

#### Q87: Explain the query optimization achieved by our 44 custom indexes.
**Answer**: Transitioned 100% of benchmark queries from collection scans (`COLLSCAN`) to B+ tree index scans (`IXSCAN`), reducing `docsExamined` from 500 documents down to 1 document for point lookups (a 99.8% reduction in disk I/O).

#### Q88: What is a Multikey Index in MongoDB?
**Answer**: An index created on an array field. MongoDB creates an index entry for every single element in the array, enabling efficient querying of nested array elements.

#### Q89: What is the difference between MongoDB's `mongodump` and continuous Cloud Backups?
**Answer**: `mongodump` produces a logical BSON snapshot of collections at a specific point in time. Continuous cloud backups stream the cluster oplog (operations log) to allow Point-in-Time Recovery (PITR) to any second within the retention window.

#### Q90: What is Recovery Time Objective (RTO) and Recovery Point Objective (RPO)?
**Answer**: RTO is the maximum acceptable duration of system downtime after a failure ($RTO \le 30\text{ s}$ via automatic 3-node replica set failover). RPO is the maximum acceptable data loss measured in time ($RPO \le 1\text{ s}$ via `majority` write concern journaling).

#### Q91: What is the role of an associative junction relation in relational mapping?
**Answer**: It decomposes an M:N relationship into two 1:N relationships using foreign keys referencing the two participating entities (e.g., `creator_collaborations` mapping pairs of collaborating creators).

#### Q92: What is the identifying relationship of a weak entity?
**Answer**: A relationship that links a weak entity to its owner entity, providing the owner's primary key to form the composite key of the weak entity.

#### Q93: Why did we deprecate `edition_id` in favor of `ceremony_id`?
**Answer**: `edition_id` was a legacy redundant field. We standardized all foreign key pathways to use the deterministic canonical identifier `ceremony_id` (`^CEREMONY_\d{3}$`), eliminating confusion and passing strict audit checks.

#### Q94: What is the purpose of `scripts/audit/final_audit.py`?
**Answer**: It is an automated compliance engine that programmatically validates all 8 architectural and academic mandates across live Atlas databases (database counts, quotas, fields, provenance, keys, orphans, and syllabus coverage).

#### Q95: What is the significance of the 7 deterministic shared identifiers in our system?
**Answer**: They provide immutable, regex-validated universal business keys (`ceremony_id`, `venue_id`, `category_id`, `nomination_id`, `artist_id`, `work_id`, `winner_record_id`) that bind the five autonomous databases into a unified logical data fabric without ad-hoc key formats.

#### Q96: What is the purpose of `tests/final-audit-report.md`?
**Answer**: It is the certified empirical audit report generated by Phase 27 certifying a 100% PASS evaluation across all architectural and academic quotas.

#### Q97: What is the difference between a covered query and an uncovered query?
**Answer**: A covered query is an index scan where all queried fields and projected fields are present in the index itself, allowing MongoDB to return results directly from the index without loading documents from disk (`docsExamined = 0`).

#### Q98: What is the impact of unindexed array sorts in MongoDB?
**Answer**: If a sort cannot use an index, MongoDB must load all documents into memory and sort them in RAM, which fails if the memory usage exceeds the 32 MB sort memory limit.

#### Q99: What is the purpose of `scripts/storage/generate_data_dictionary.py`?
**Answer**: It introspects all 50 collections across the five live Atlas databases, extracting exact document counts, data sizes, storage sizes, compression ratios, and schema attributes into `docs/storage/data_dictionary.json`.

#### Q100: What is the final readiness verdict of the GRAMMY DBMS project?
**Answer**: 100% Certified Complete, satisfying all 30 project lifecycle phases and 10 graduate ADBMS syllabus modules with 670 passing tests (including 629 core DBMS engine tests and 41 presentation/viva capstone verification tests).


---

# Section 3: 30 Advanced Viva Questions & Answers

#### Q101: Explain why the relational division operator ($\div$) is algebraically complete and how it is implemented in SQL vs. Relational Algebra.
**Answer**: Relational division $R(A, B) \div S(B)$ identifies all tuples in $\pi_A(R)$ whose associated $B$ values include all tuples in $S$. In relational algebra, it is defined using projection, Cartesian product, and set difference: $R \div S = \pi_A(R) - \pi_A((\pi_A(R) \times S) - R)$. In SQL, it is typically expressed using double-negated correlated subqueries (`NOT EXISTS ... NOT EXISTS`) or grouping with a `COUNT(DISTINCT)` condition matching the cardinality of $S$.

#### Q102: Formulate the mathematical proof that our BCNF decomposition of `nomination_entries` is lossless.
**Answer**: A decomposition of relation $R$ into $R_1$ and $R_2$ is lossless join with respect to $F$ if and only if $R_1 \cap R_2 \rightarrow R_1 \in F^+$ or $R_1 \cap R_2 \rightarrow R_2 \in F^+$. In our schema, $R_1 \cap R_2 = \{\text{nomination\_id}\}$. Because $\text{nomination\_id}$ is a candidate key for `nomination_entries`, $\text{nomination\_id} \rightarrow R_1$, proving the intersection is a superkey of $R_1$. Hence, the natural join reconstructs the original relation with zero spurious tuples.

#### Q103: Explain the theoretical foundation of Multivalued Dependencies (MVD) in 4NF and identify an MVD that exists in creator management.
**Answer**: An MVD $X \twoheadrightarrow Y$ holds on $R(X, Y, Z)$ if for any two tuples $t_1, t_2$ with $t_1[X] = t_2[X]$, there exists a tuple $t_3$ with $t_3[X] = t_1[X]$, $t_3[Y] = t_1[Y]$, and $t_3[Z] = t_2[Z]$. In `creator_talents(creator_id, musical_skill, spoken_language)`, a creator's skills are independent of the languages they speak: $\text{creator\_id} \twoheadrightarrow \text{musical\_skill}$ and $\text{creator\_id} \twoheadrightarrow \text{spoken\_language}$. Storing these in a single relation forces a Cartesian product of tuples. Decomposing into `creator_skills(creator_id, musical_skill)` and `creator_languages(creator_id, spoken_language)` satisfies 4NF.

#### Q104: Prove that a relation with only two attributes is always in BCNF.
**Answer**: Let $R(A, B)$. The only possible non-trivial FDs are $A \rightarrow B$ or $B \rightarrow A$. If $A \rightarrow B$, $A$ determines all attributes of $R$, so $A$ is a superkey and $R$ is in BCNF. If $B \rightarrow A$, $B$ is a superkey. If both hold, both are candidate keys. If neither holds, only trivial FDs exist, which also satisfies BCNF. Therefore, any binary relation is unconditionally in BCNF.

#### Q105: How does MongoDB Atlas enforce Snapshot Isolation during multi-document transactions?
**Answer**: MongoDB uses WiredTiger's storage-level MVCC timestamp engine. When a transaction starts with `ReadConcern("snapshot")`, WiredTiger establishes a read timestamp. The transaction reads committed document versions corresponding exactly to that timestamp, ignoring subsequent writes by other transactions. When writing, if another transaction has committed a modification to the same document after the read timestamp, a `WriteConflict` is raised, forcing an abort and rollback.

#### Q106: Why does application-level join federation violate ACID consistency across separate databases in the absence of a Two-Phase Commit (2PC) coordinator?
**Answer**: While single-database operations in MongoDB Atlas are ACID-compliant, cross-database writes executed by client-side scripts do not participate in a single unified distributed transaction coordinator. If a script updates `grammy_nominations_db` and then fails before updating `grammy_winners_db`, the system enters an inconsistent intermediate state. To mitigate this without 2PC overhead, our system relies on deterministic idempotency and compensating write handlers.

#### Q107: Analyze the trade-offs of WiredTiger's in-memory page eviction triggers (80% dirty, 20% clean, 95% aggressive).
**Answer**: WiredTiger allocates 50% of RAM (minus 1 GB) for its cache. When cache usage reaches 80% dirty or 20% clean thresholds, background eviction worker threads flush dirty pages to disk and evict clean pages. If cache pressure reaches 95%, application client threads are conscripted into performing synchronous page eviction, severely increasing query latency to protect the engine from out-of-memory crashes.

#### Q108: Why does MongoDB WiredTiger avoid cascading aborts without holding shared locks until the end of transactions?
**Answer**: WiredTiger utilizes multi-version concurrency control (MVCC). Readers read historical snapshot versions from the rollback segment / cache without acquiring shared locks. Because readers never read uncommitted dirty data written by active transactions, an abort of a writing transaction does not invalidate any reader's state, naturally eliminating cascading aborts.

#### Q109: Explain why Project-Join Normal Form (5NF) requires all join dependencies to be implied by candidate keys.
**Answer**: A join dependency $\bowtie[R_1, R_2, \dots, R_k]$ states that $R$ can be losslessly reconstructed by joining its projections $R_1, \dots, R_k$. If a join dependency exists that is not implied by candidate keys, decomposing $R$ into these projections eliminates cyclic redundancy. 5NF guarantees that no further non-loss decomposition is possible, eliminating all remaining multi-attribute cyclic join anomalies.

#### Q110: Detail the exact mathematical mechanism of the ARIES "Repeating History" paradigm during Redo.
**Answer**: During Redo, ARIES scans the log forward starting from the minimum `RecLSN` in the Dirty Page Table (the oldest unwritten page update). For every log record with LSN $\ge \text{RecLSN}$, it inspects the page on disk. If the page's `pageLSN < LSN`, the logged update is re-applied and `pageLSN` is updated to `LSN`. This re-establishes the exact physical memory state that existed at the instant of the crash, including actions of transactions that subsequently aborted.

#### Q111: Contrast Shadow Paging with Write-Ahead Logging in terms of disk I/O and storage fragmentation.
**Answer**: Shadow paging maintains two page tables (current and shadow). Updates write new data to newly allocated disk pages, updating the current page table. At commit, the current page table pointer is written atomically to disk. While shadow paging avoids undo logging and redo recovery overhead, it destroys physical page clustering (causing severe disk fragmentation) and requires complex garbage collection of obsolete disk pages, making WAL far superior for high-performance DBMS engines.

#### Q112: In our EER diagram, why is `AWARD_RECIPIENT` modeled as a Category (Union Type) rather than a Generalization?
**Answer**: Generalization models subclasses that share the same superclass identity ($E_1, E_2 \subset E$). A Category (Union Type) models a single entity set that is a subset of the *union* of distinct entity types with different primary keys ($U \subset E_1 \cup E_2$). `AWARD_RECIPIENT` must encompass solo individual `ARTIST` entities (keyed by `artist_id`) and multi-member `MUSICAL_GROUP` entities (keyed by `group_id`). Since their key structures and domain attributes differ, a union type is mathematically required.

#### Q113: How does the WiredTiger storage engine store B+ tree index keys and what is prefix compression?
**Answer**: WiredTiger stores index keys in contiguous memory blocks. Prefix compression stores each index key as a prefix length matching the preceding key followed by the unique suffix bytes (e.g., storing `CEREMONY_001` and `CEREMONY_002` stores the common prefix `CEREMONY_00` once). This drastically reduces index memory footprint and increases B+ tree fan-out.

#### Q114: How does our system guarantee that multi-contributor credits do not suffer from the 16 MB document size limit?
**Answer**: By decoupling credits from `nominated_works`. Instead of embedding hundreds of producers, engineers, and songwriters into a single `nominated_work` document, each credit is stored as an autonomous document in `nomination_credits` referencing `nomination_id` and `creator_id`. This normalized referencing architecture guarantees $O(1)$ document size scaling.

#### Q115: What is the exact mathematical consequence of a cyclic Wait-For Graph in terms of serializability?
**Answer**: A cycle $T_1 \rightarrow T_2 \rightarrow \dots \rightarrow T_k \rightarrow T_1$ in a Wait-For Graph indicates that no topological sort exists for the transaction schedule. Because conflict serializability requires an acyclic precedence graph, a cyclic dependency indicates that no equivalent serial schedule can be formed without aborting at least one transaction to break the cycle.

#### Q116: Explain how our test harness verifies bitwise SHA-256 state parity in the crash recovery drill.
**Answer**: Prior to corruption injection, `scripts/recovery/controlled_recovery_drill.py` serializes the canonical state of target collections into deterministic, key-sorted BSON dumps and computes a SHA-256 cryptographic hash. Following corruption injection and automated point-in-time restore, the dump and hash are recomputed. Parity is proven when $\text{SHA256}(\text{pre\_crash}) \equiv \text{SHA256}(\text{post\_restore})$.

#### Q117: What is the difference between a sparse index and a partial index in MongoDB?
**Answer**: A sparse index only indexes documents that contain the indexed field (ignoring documents where the field is missing). A partial index is more expressive: it uses a filter expression (`partialFilterExpression`) to index only documents that satisfy specific conditional criteria (e.g., `{"is_winner": True}`), reducing index size and write overhead.

#### Q118: How does MongoDB execute an aggregation pipeline that begins with a `$match` followed by a `$sort` when a compound index exists?
**Answer**: The MongoDB query optimizer pushes the `$match` and `$sort` stages down into the WiredTiger storage engine as a single combined `IXSCAN`. If the index matches the ESR pattern (equality on match fields, sort on sort fields), documents are streamed directly from the B+ tree in pre-sorted order, avoiding memory allocation.

#### Q119: Analyze why 3NF decomposition preserves dependencies while BCNF decomposition may not.
**Answer**: 3NF relaxes BCNF by permitting non-trivial dependencies $X \rightarrow A$ where $A$ is a prime attribute (part of a candidate key). This relaxation allows 3NF synthesis algorithms to add a relation schema containing all attributes of any unrepresented functional dependency, guaranteeing both lossless join and dependency preservation. BCNF disallows prime attribute exceptions, so forcing determinant superkeys can split dependency attributes across relations.

#### Q120: How does the system handle concurrent read-write contention in `scripts/concurrency/simulate_concurrency.py`?
**Answer**: The script spawns 10 concurrent threads executing atomic `$inc` updates with exponential backoff and jitter retry loops catching `WriteConflict` exceptions. This ensures that optimistic transaction collisions are resolved cleanly without blocking threads or losing updates.

#### Q121: What is the difference between physical logging, logical logging, and physiological logging?
**Answer**: Physical logging records before-and-after bit images of disk pages. Logical logging records high-level operations (e.g., "Insert tuple into table"). Physiological logging (used by modern DBMSs including ARIES) logs physical page addresses with logical operation descriptions within that page, achieving compact log size with deterministic recovery.

#### Q122: In a distributed multi-database architecture, why is natural key uniqueness critical across independent databases?
**Answer**: In the absence of a global relational catalog enforcing distributed uniqueness constraints, independent databases must rely on deterministic universal key formatting (`^CRT_[A-Z0-9_]+$`). If two databases generate colliding keys for different entities, application-level joins produce corrupted, cross-wired entities.

#### Q123: Explain the role of the Write Concern `w="majority"` in preventing dirty reads and rollback anomalies during network partitions.
**Answer**: `w="majority"` requires that a write be acknowledged by a majority of replica set nodes before returning success. If a network partition creates a transient minority primary, writes to that primary will never be acknowledged. When the partition heals and a new primary is elected, unacknowledged writes on the old primary are discarded, preventing dirty reads and phantom commits.

#### Q124: What is the exact relationship between B+ tree node split frequency and disk block fill factors?
**Answer**: When a B+ tree node reaches capacity, it splits into two nodes, each approximately 50% full. Higher insert volumes with random keys trigger frequent node splits, lowering the average fill factor ($\approx 67\%$) and increasing tree depth. Sequential key insertion (like our deterministic IDs) achieves higher fill factors ($\approx 90\%+$), minimizing node splits and I/O overhead.

#### Q125: What is the difference between View Serializability and Conflict Serializability regarding Blind Writes?
**Answer**: Blind writes (writing an attribute without reading it first) allow schedules to be view serializable that are not conflict serializable. Because blind writes do not establish read-write ordering dependencies, their execution order can be rearranged in view equivalence without changing final database state.

#### Q126: How does the system ensure zero secret leakage in CI/CD and version control?
**Answer**: By enforcing pre-commit hooks, `.gitignore` rules targeting `.env` and credential files, automated regex scanning for connection URI strings, and unit tests in `tests/test_environment_and_secrets.py` that verify `.env` is untracked in Git.

#### Q127: Why does relational division require both the dividend and divisor to be projected down prior to division?
**Answer**: Relational division $R \div S$ mathematically requires that the attribute set of $S$ is a proper subset of $R$: $\text{attr}(S) \subset \text{attr}(R)$. If extra attributes are left in $R$ or $S$, the division condition evaluates across non-relevant attributes, yielding an empty relation or incorrect quotient tuples.

#### Q128: Explain how WiredTiger's checkpointing ensures database consistency without flushing every committed transaction immediately to disk.
**Answer**: Committed transactions flush their log records to the Write-Ahead Journal (`WiredTigerLog.*`), which is sequential and fast. The actual in-memory dirty data pages are lazily flushed every 60 seconds during checkpoints. In the event of a crash, the checkpoint establishes the base state, and the sequential journal replays transactions committed since the checkpoint.

#### Q129: What is the computational complexity of detecting cycles in a Wait-For Graph?
**Answer**: Using Depth-First Search (DFS) or Tarjan's strongly connected components algorithm, the time complexity of cycle detection is $O(|V| + |E|)$, where $|V|$ is the number of active transactions and $|E|$ is the number of lock wait dependencies.

#### Q130: Why is our capstone project considered an enterprise DBMS implementation rather than a routine web CRUD application?
**Answer**: Because it implements and validates all 10 modules of the graduate DBMS curriculum: formal EER specialization and union types, mathematical relational algebra with division, 1NF–5NF normalization proofs, multi-document ACID transactions, 2PL and MVCC concurrency, physical storage layout with Snappy compression, ARIES recovery with SHA-256 crash drills, 44 custom indexes with explain plan analysis, and distributed cross-database join federation.

---

# Section 4: Dedicated Questions on Conceptual EER Modeling

#### Q131: What is the distinction between an entity type, entity set, and value set in our EER model?
**Answer**: An entity type is the conceptual schema definition (e.g., `CEREMONY`). An entity set is the collection of all entity instances stored in the database (e.g., all 67 ceremonies in `grammy_history_db`). A value set is the allowable domain of values for an attribute (e.g., integers 1959–2030 for `broadcast_year`).

#### Q132: Explain the specialization hierarchy of `CREATOR` in our EER diagram.
**Answer**: `CREATOR` is generalized as a superclass with two subclasses: `INDIVIDUAL_CREATOR` and `ORGANIZATIONAL_CREATOR`. The constraint is disjoint $[d]$ (a creator cannot be both an individual human and a corporate entity) and total $[t]$ (every creator must belong to one of these two classes). Furthermore, `INDIVIDUAL_CREATOR` specializes into overlapping $[o]$ subclasses: `ARTIST`, `PRODUCER`, `AUDIO_ENGINEER`, and `SONGWRITER`, allowing an individual (e.g., Stevie Wonder) to hold multiple craft roles.

#### Q133: Why is `VIEWERSHIP_RATING` classified as a weak entity?
**Answer**: A weak entity does not possess a primary key formed exclusively from its own attributes. `VIEWERSHIP_RATING` cannot exist without an associated `CEREMONY`. Its primary key is composite, formed by combining the foreign key `ceremony_id` of parent `CEREMONY` with its partial key (discriminator) `rating_id`.

#### Q134: How is conceptual aggregation represented in our EER schema?
**Answer**: In awards modeling, a credit is not merely an association between a creator and a work; it is associated with a specific award category. We model $\text{AGGREGATE}(\text{CREATOR}, \text{WORK}, \text{AWARD\_CATEGORY})$ as a composite higher-level entity, which then participates in the relationship with `NOMINATION_CREDIT`.

#### Q135: What is the difference between total participation and partial participation in our EER model?
**Answer**: Total participation (double line) requires every entity instance to participate in the relationship (e.g., every `WINNER_RECORD` must participate in an identifying relationship with exactly one `NOMINATION_ENTRY`). Partial participation (single line) allows instances to exist without the relationship (e.g., a `CEREMONY` may exist before any `HISTORIC_MILESTONE` is recorded for it).

#### Q136: How does our EER design handle recursive (self-referencing) relationships?
**Answer**: In `grammy_categories_db.category_lineage`, a category can reference its ancestor category through a recursive relationship `SUPERVISES` / `DERIVED_FROM`, modeling the evolutionary ancestry of split and renamed categories.

#### Q137: Explain the category union type `AWARD_RECIPIENT = ARTIST \cup MUSICAL_GROUP`.
**Answer**: This represents a selective union where an award recipient can be either an individual `ARTIST` or an ensemble `MUSICAL_GROUP`. It allows polymorphic credit assignment without requiring duplicate foreign key attributes in winner records.

#### Q138: What are composite attributes and multivalued attributes in our conceptual model, and how were they resolved?
**Answer**: A composite attribute (e.g., `venue_address` composed of street, city, state, zip) was flattened into scalar atomic attributes. Multivalued attributes (e.g., multiple secondary genres for an artist) were decomposed into independent child entities or normalized associative relations.

#### Q139: Why does our EER diagram avoid ternary relationships in favor of binary relationships with associative entities?
**Answer**: Ternary relationships often obscure cardinality constraints and create ambiguity during relational mapping. By reifying the ternary relationship into an associative entity (e.g., `nomination_credits`), we retain precise 1:N cardinality constraints and explicit attribute assignment.

#### Q140: Where are the formal EER diagram files located in the repository?
**Answer**: The raw XML vector source is located at `eer/grammy-eer.drawio`, the rendered image is at `eer/grammy-eer.png`, and the theoretical documentation is in `docs/eer-design.md`.

---

# Section 5: Dedicated Questions on Functional Dependencies & Normalization

#### Q141: What functional dependencies exist on `ceremonies`?
**Answer**: $\text{ceremony\_id} \rightarrow \{\text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{primary\_network}, \text{total\_awards\_presented}\}$.

#### Q142: Demonstrate the derivation of an FD using Transitivity.
**Answer**: Given $X \rightarrow Y$ ($\text{nomination\_id} \rightarrow \text{work\_id}$) and $Y \rightarrow Z$ ($\text{work\_id} \rightarrow \text{release\_date}$), Armstrong's Transitivity Axiom states that $X \rightarrow Z$ holds ($\text{nomination\_id} \rightarrow \text{release\_date}$).

#### Q143: How is the attribute closure $X^+$ computed?
**Answer**: Initialize $X^+ = X$. Repeatedly iterate through all FDs $Y \rightarrow Z \in F$; if $Y \subseteq X^+$, then $X^+ = X^+ \cup Z$. Terminate when no new attributes are added. The resulting set $X^+$ contains all attributes functionally determined by $X$.

#### Q144: How did we derive the Minimal Cover ($F_{min}$) for `award_categories`?
**Answer**:
1. Decomposed RHS attributes so all FDs have singleton RHS: $X \rightarrow \{A_1, A_2\} \implies X \rightarrow A_1, X \rightarrow A_2$.
2. Eliminated extraneous LHS attributes by testing if $(X - \{A\})^+ \supseteq Z$.
3. Pruned redundant dependencies by testing if $F - \{f\} \models f$.

#### Q145: Why was `nomination_credits` not in 2NF before decomposition?
**Answer**: The composite candidate key is $\{\text{nomination\_id}, \text{creator\_id}, \text{craft\_role}\}$. If attributes like `creator_legal_name` were included, they would depend only on $\text{creator\_id}$ (a proper subset of the candidate key), constituting a partial key dependency violating 2NF. Decomposing `creator_legal_name` into `artists` resolved this violation.

#### Q146: Give an example of a 3NF transitive dependency violation and its resolution.
**Answer**: In an un-normalized ceremony table: $\text{ceremony\_id} \rightarrow \text{venue\_id}$ and $\text{venue\_id} \rightarrow \text{venue\_capacity}$. Because $\text{venue\_capacity}$ is non-prime and $\text{venue\_id}$ is not a superkey, this violates 3NF. It was decomposed into `ceremonies(ceremony_id, venue_id, ...)` and `venues(venue_id, venue_capacity, ...)`.

#### Q147: Explain the BCNF decomposition of `winner_records`.
**Answer**: If a non-trivial dependency $X \rightarrow Y$ exists where $X$ is not a superkey, the relation $R$ is split into $R_1(X \cup Y)$ and $R_2(R - Y)$. For `winner_records`, every functional dependency originates from $\text{winner\_record\_id}$ or $\text{nomination\_id}$, both of which are candidate keys. Thus, `winner_records` natively satisfies BCNF.

#### Q148: What is a Multivalued Dependency (MVD) and how does 4NF resolve it?
**Answer**: An MVD $X \twoheadrightarrow Y$ means the presence of $Y$ values is independent of other attributes $Z$ for a given $X$. 4NF decomposes relations with non-trivial MVDs into separate relations, preventing the explosive combinatorial tuple expansion required to represent independent multivalued facts.

#### Q149: What is the formal definition of a Join Dependency in 5NF?
**Answer**: A relation $R$ satisfies the join dependency $\bowtie[R_1, R_2, \dots, R_k]$ if and only if $R = \pi_{R_1}(R) \bowtie \pi_{R_2}(R) \bowtie \dots \bowtie \pi_{R_k}(R)$. 5NF requires that every such join dependency is implied by the candidate keys of $R$.

#### Q150: What performance benchmarks justified our controlled denormalization?
**Answer**: Querying certified winners with artist biography and ceremony details under pure 3NF required joining 4 tables, taking $\approx 125\text{ ms}$. Embedding `stage_name` and `ceremony_year` into `winner_records` reduced lookup latency to $\approx 15\text{ ms}$ (an 88% speedup).

---

# Section 6: Dedicated Questions on MongoDB Document Modeling

#### Q151: How do MongoDB documents represent 1:N relationships?
**Answer**: Either through embedded arrays of subdocuments (bounded 1:N, where $N$ is small and fixed, e.g., craft credit specifications) or through normalized foreign key references (unbounded 1:N, where $N$ can grow into thousands, e.g., nominations in a ceremony).

#### Q152: Why is the hybrid document design superior to pure embedding in our domain?
**Answer**: Pure embedding would cause documents to exceed MongoDB's 16 MB limit and create massive document growth during updates, triggering expensive in-place document moves on disk. The hybrid design embeds bounded metadata while referencing unbounded collections.

#### Q153: Where are the official `$jsonSchema` validation files stored in the repository?
**Answer**: Under `schemas/json_schemas/` partitioned across five subdirectories corresponding to the five databases (e.g., `schemas/json_schemas/grammy_history_db/ceremonies.json`).

#### Q154: How does MongoDB enforce data types in `$jsonSchema`?
**Answer**: Using the `bsonType` property, specifying types such as `"string"`, `"int"`, `"double"`, `"bool"`, `"date"`, and `"object"`.

#### Q155: What regex pattern is enforced on `winner_record_id`?
**Answer**: `^WIN_[A-Z0-9_]+$` (e.g., `WIN_065_AOTY_01`).

#### Q156: How does MongoDB handle missing attributes when `$jsonSchema` is active?
**Answer**: Attributes specified in the `required` array cannot be omitted on insert or update. Non-required attributes can be omitted unless `additionalProperties: false` is configured.

#### Q157: What is the difference between BSON and JSON?
**Answer**: JSON is a text-based data format supporting strings, numbers, booleans, arrays, and objects. BSON (Binary JSON) is a binary serialization format that extends JSON with additional data types (int32, int64, double, date, binary, decimal128) and enables fast traversal.

#### Q158: What is an ObjectId in MongoDB and why did our system use deterministic natural IDs instead?
**Answer**: An `ObjectId` is a 12-byte default BSON identifier containing timestamp, machine ID, process ID, and increment counter. We adopted deterministic natural string keys (`CEREMONY_065`, `CRT_TAYLOR_SWIFT`) to guarantee human-readable cross-database join stability and prevent duplicate ingestion.

#### Q159: What is the purpose of the `_id` field in MongoDB collections?
**Answer**: `_id` is the mandatory primary key for every MongoDB document. If not provided, MongoDB automatically generates an `ObjectId`. In our collections, we explicitly assign our deterministic natural string IDs directly to `_id`.

#### Q160: What test verifies that all 50 collections enforce valid JSON schemas?
**Answer**: `tests/test_schema_validity.py`, which validates every JSON schema against draft-07 and verifies schema deployment on Atlas.

---

# Section 7: Dedicated Questions on Aggregation Pipelines

#### Q161: What is the MongoDB Aggregation Pipeline?
**Answer**: A multi-stage data processing framework where documents pass through a sequence of transformation stages (e.g., `$match`, `$group`, `$sort`, `$project`) to compute aggregated metrics.

#### Q162: What is the function of the `$match` stage?
**Answer**: It filters documents in the pipeline using MongoDB query operators, reducing the volume of documents passed to downstream stages. When placed at the pipeline start, it can utilize B+ tree indexes.

#### Q163: How does `$group` work in an aggregation pipeline?
**Answer**: It groups input documents by a specified identifier expression (`_id`) and applies accumulator expressions (`$sum`, `$avg`, `$min`, `$max`, `$push`, `$addToSet`) to compute aggregate values for each group.

#### Q164: What is the difference between `$push` and `$addToSet` in a `$group` stage?
**Answer**: `$push` adds an expression value to an array for every document in the group (preserving duplicates). `$addToSet` adds the value only if it is not already present in the array (eliminating duplicates).

#### Q165: How does the `$unwind` stage function?
**Answer**: It deconstructs an array field from input documents, outputting one document for each element of the array. This allows downstream stages to group or filter individual array elements.

#### Q166: Explain our historical victory distribution aggregation pipeline.
**Answer**: It filters winners (`$match: {"is_winner": True}`), groups by `primary_artist_id`, calculates `total_wins` using `{"$sum": 1}`, collects distinct categories won via `{"$addToSet": "$category_id"}`, filters for artists with $\ge 5$ wins, and sorts in descending order.

#### Q167: What is the purpose of `$project` in an aggregation pipeline?
**Answer**: It reshapes documents, specifying which fields to include, exclude, or rename, and allows computing new derived fields using arithmetic or string expressions.

#### Q168: How does the `$lookup` stage function for same-database joins?
**Answer**: It performs a left outer join to an un-sharded collection in the *same* database, matching `localField` with `foreignField` and outputting matching documents as a new array attribute.

#### Q169: Why can `$lookup` not be used across our five databases on Atlas M0?
**Answer**: MongoDB Atlas M0 free-tier clusters prohibit server-side cross-database `$lookup` operations, raising `AtlasError 8000: Cross-database $lookup is not supported on this cluster tier`.

#### Q170: Where are our automated aggregation tests located?
**Answer**: In `tests/test_aggregation_pipelines.py`, verifying complex multi-stage pipelines, `$facet` operations, and data transformations.

---

# Section 8: Dedicated Questions on Multi-Document ACID Transactions

#### Q171: What is a multi-document ACID transaction session in PyMongo?
**Answer**: A client session opened via `client.start_session()` that coordinates multiple read and write operations across collections within a `session.start_transaction()` block, guaranteeing all-or-nothing execution.

#### Q172: What collections participate in our controlled transaction demonstration?
**Answer**: Three collections in `grammy_winners_db`: `controlled_tx_ballots` (ballot certification), `controlled_tx_trophies` (statuette inventory allocation), and `controlled_tx_audit` (accounting audit ledger).

#### Q173: What is Snapshot Isolation?
**Answer**: An isolation level where a transaction observes a consistent snapshot of the database taken at its start timestamp. It guarantees zero dirty reads, zero non-repeatable reads, and zero phantom reads.

#### Q174: What is the role of Write Concern in transactions?
**Answer**: It specifies the acknowledgment level required from replica set nodes before a write is deemed committed. `WriteConcern(w="majority", j=True)` guarantees durability across a majority of nodes with disk journaling.

#### Q175: What is the role of Read Concern in transactions?
**Answer**: It specifies the consistency level of data read by the transaction. `ReadConcern("snapshot")` ensures reads reflect the point-in-time snapshot established at the transaction's start.

#### Q176: How does our transaction script simulate a rollback?
**Answer**: It executes operations 1 and 2 successfully, and then injects a simulated duplicate key insertion on the unique primary key of `controlled_tx_audit`. This raises a `DuplicateKeyError`, triggering the exception handler which calls `session.abort_transaction()`.

#### Q177: What was the verified state of the database after the simulated rollback?
**Answer**: Exactly zero documents were persisted in any of the three collections, proving complete transactional atomicity without state leakage.

#### Q178: What is the empirical latency of our transaction commit?
**Answer**: 73.42 milliseconds across the three collections on our live Atlas replica set.

#### Q179: Can a MongoDB transaction span multiple databases on Atlas?
**Answer**: In dedicated Atlas clusters (M10+), transactions can span multiple databases within the same cluster. On M0 shared clusters, multi-database transactions are constrained, which is why our controlled ACID demo executes within `grammy_winners_db`.

#### Q180: Where is the executable transaction script and report located?
**Answer**: The script is at `scripts/transactions/run_transaction_demo.py`, the master report is at `docs/transactions/transaction-demo.md`, and tests are in `tests/test_transactions.py`.

---

# Section 9: Dedicated Questions on Concurrency Control & Serializability

#### Q181: What is a Lost Update anomaly and how does our simulation prevent it?
**Answer**: A Lost Update occurs when two concurrent transactions read the same data and simultaneously write updates, causing one update to overwrite the other. Our system prevents it using atomic `$inc` operators and OCC version checks.

#### Q182: What lock types exist in Multiple Granularity Locking (MGL)?
**Answer**: Shared (S), Exclusive (X), Intention Shared (IS), Intention Exclusive (IX), and Shared Intention Exclusive (SIX).

#### Q183: Explain the lock compatibility rule for SIX locks.
**Answer**: A SIX lock grants shared access to the entire subtree while intending to hold exclusive locks on specific subordinate items. It is compatible only with IS locks; it conflicts with IX, S, SIX, and X locks.

#### Q184: How does our Wait-For Graph (WFG) implementation detect deadlocks?
**Answer**: It represents active transactions as vertices and lock dependencies as directed edges. It executes Depth-First Search (DFS) to identify back-edges, which indicate cycles (deadlocks).

#### Q185: Explain the Wait-Die deadlock prevention policy.
**Answer**: When transaction $T_i$ requests a lock held by $T_j$: if $T_i$ is older than $T_j$ ($TS(T_i) < TS(T_j)$), $T_i$ is allowed to wait. If $T_i$ is younger, $T_i$ dies (aborts and restarts with its original timestamp).

#### Q186: Explain the Wound-Wait deadlock prevention policy.
**Answer**: When transaction $T_i$ requests a lock held by $T_j$: if $T_i$ is older than $T_j$, $T_i$ wounds (aborts) $T_j$ and seizes the lock. If $T_i$ is younger, $T_i$ is allowed to wait.

#### Q187: How many execution tickets does WiredTiger configure for concurrent operations?
**Answer**: 128 concurrent read execution tickets and 128 concurrent write execution tickets.

#### Q188: What exception does MongoDB raise when concurrent writes collide under OCC?
**Answer**: `WriteConflict` (error code 112), which signals the application to back off and retry the transaction.

#### Q189: How many concurrent threads and updates were tested in our concurrency harness?
**Answer**: 10 concurrent worker threads executing 100 rapid atomic increment updates, achieving zero Lost Updates.

#### Q190: Where are the concurrency scripts and documentation files located?
**Answer**: Script: `scripts/concurrency/simulate_concurrency.py`; Docs: `docs/concurrency/concurrency.md`, `docs/concurrency/serializability.md`, `docs/concurrency/deadlocks.md`; Tests: `tests/test_concurrency.py`.

---

# Section 10: Dedicated Questions on Physical Storage Architecture & RAID

#### Q191: What is the hardware latency hierarchy analyzed in Module 6?
**Answer**: CPU Register ($< 1\text{ ns}$), L1 Cache ($\approx 1\text{ ns}$), L2/L3 Cache ($3\text{--}10\text{ ns}$), Main Memory / RAM ($\approx 100\text{ ns}$), NVMe SSD ($\approx 100\text{ }\mu\text{s}$), and Magnetic HDD ($\approx 10\text{ ms}$).

#### Q192: What is the significance of the Slotted-Page architecture in DBMS storage?
**Answer**: It decouples logical record identification from physical byte offsets on disk. By addressing records through a slot pointer table at the page head, records can be shifted or defragmented without modifying external foreign keys.

#### Q193: What are the primary disk organization schemes and which one does WiredTiger use?
**Answer**: Heap files, Sequential sorted files, Hashing files, and B+ tree indexed files. WiredTiger uses B+ tree indexed files with slotted pages for its underlying table storage.

#### Q194: What is RAID 0 and what is its primary weakness?
**Answer**: Block-level striping without redundancy. It provides high read/write throughput but zero fault tolerance; a failure of any single disk results in total data loss.

#### Q195: What is RAID 1 and what is its storage efficiency?
**Answer**: Disk mirroring. Every block is written to two or more identical disks. Its storage efficiency is $50\%$ (requires $2N$ raw disk capacity for $N$ usable capacity).

#### Q196: Explain the parity calculation in RAID 5.
**Answer**: RAID 5 stripes data and single parity across all disks. Parity is computed using bitwise XOR: $P = D_1 \oplus D_2 \oplus \dots \oplus D_{n-1}$. Any single missing disk can be reconstructed by XORing the surviving data disks with parity.

#### Q197: What is RAID 6 and why was it created?
**Answer**: RAID 6 extends RAID 5 by computing two independent parity blocks (P and Q) using Reed-Solomon coding, allowing the array to survive the simultaneous failure of any two disks.

#### Q198: What is RAID 10 (1+0)?
**Answer**: A stripe of mirrors. Disks are paired as RAID 1 mirrors, and the mirrored pairs are striped using RAID 0. It combines the high fault tolerance and fast write performance of mirroring with the high bandwidth of striping.

#### Q199: What were the exact storage metrics recorded in our empirical data dictionary?
**Answer**: 5,190 documents, 4.06 MB uncompressed data, 2.72 MB compressed storage (32.9% savings), and 3.15 MB index size across 44 custom indexes.

#### Q200: Where are the physical storage documentation and scripts located?
**Answer**: Introspection Script: `scripts/storage/generate_data_dictionary.py`; Data Dictionary: `docs/storage/data_dictionary.json`; Master Docs: `docs/storage/storage-architecture.md`, `docs/storage/dbms-storage-concepts.md`; Tests: `tests/test_storage.py`.

---

# Section 11: Dedicated Questions on Crash Recovery & ARIES

#### Q201: What is the primary function of Write-Ahead Logging (WAL) in database crash recovery?
**Answer**: To guarantee the atomicity and durability of transactions by ensuring that log records describing state transitions are flushed to non-volatile disk before dirty data pages are written to disk.

#### Q202: What are the two fundamental invariants of WAL?
**Answer**:
1. **Write-Ahead Undo Rule**: Log records must be written before dirty data is written to disk.
2. **Commit Redo Rule**: All log records for a committed transaction must be on disk before commit completion is acknowledged.

#### Q203: What tables are constructed during the ARIES Analysis Phase?
**Answer**:
1. **Transaction Table**: Active transactions at crash time and their `lastLSN`.
2. **Dirty Page Table (DPT)**: In-memory dirty pages and the earliest `RecLSN` that caused them to become dirty.

#### Q204: Why does ARIES "repeat history" during the Redo Phase?
**Answer**: To re-establish the exact physical database state that existed at the moment of failure, ensuring that concurrent operations, locks, and even operations of aborted transactions are accurately positioned before rollback begins.

#### Q205: What is the function of the Undo Phase in ARIES?
**Answer**: To roll back the effects of all active transactions that did not commit before the crash ("losers"), moving backward through the log and writing Compensation Log Records (CLRs).

#### Q206: Why do Compensation Log Records (CLRs) contain an `UndoNextLSN` pointer?
**Answer**: To bypass log records that have already been undone. If the system crashes during the Undo phase, recovery resumes from `UndoNextLSN` rather than re-undoing previously undone operations.

#### Q207: How does MongoDB implement WAL on disk?
**Answer**: Via the WiredTiger journal, written as sequential pre-allocated log files (`WiredTigerLog.*`) of up to 100 MB each in the database directory.

#### Q208: What is Point-in-Time Recovery (PITR) in MongoDB Atlas?
**Answer**: A continuous backup mechanism that combines periodic cluster snapshots with continuous streaming of the replica set oplog, allowing restoration of cluster state to any arbitrary second.

#### Q209: Detail the execution of our controlled disaster recovery drill.
**Answer**: We executed `scripts/recovery/controlled_recovery_drill.py`: captured a baseline SHA-256 hash of collection state, injected simulated rogue corruption into target documents, executed an automated point-in-time restore, and proved 100% bitwise SHA-256 parity.

#### Q210: Where is the disaster recovery documentation and drill code located?
**Answer**: Script: `scripts/recovery/controlled_recovery_drill.py`; Plan: `docs/recovery/recovery-plan.md`; Concepts: `docs/recovery/backup-restore.md`; Runbooks: `docs/recovery/failure-scenarios.md`; Tests: `tests/test_recovery.py`.

---

# Section 12: Dedicated Questions on Data Sources & Ingestion

#### Q211: How many historical ceremony editions are captured in our database?
**Answer**: 67 ceremony editions, spanning the 1st Annual GRAMMY Awards in 1959 to the 67th Annual GRAMMY Awards in 2025.

#### Q212: How were historical nomination records sourced and validated?
**Answer**: Extracted from the Kaggle Grammy Awards dataset (Robyn Ritchie), cross-referenced against the official Recording Academy archives (`grammy.com`), cleaned of encoding artifacts, and formatted into standardized JSON documents.

#### Q213: What canonical creator identifiers are used in `grammy_creators_db`?
**Answer**: MusicBrainz Artist Identifiers (`MBID` / GID) mapped to deterministic primary keys (`CRT_{STAGE_NAME}`).

#### Q214: How were physical venue locations geocoded?
**Answer**: Venue coordinates, capacities, and addresses were extracted from Wikidata and Wikimedia Foundation records.

#### Q215: What Nielsen ratings attributes are stored in `viewership_ratings`?
**Answer**: Total viewers in millions, household rating, 18–49 demographic share, and peak quarter-hour audience.

#### Q216: How did the ETL pipeline enforce schema validation during data processing?
**Answer**: Python processing scripts validated transformed records against Draft-07 JSON schemas before writing output artifacts to `data/processed/` and `data/validated/`.

#### Q217: What was the purpose of the pre-flight validation script?
**Answer**: `scripts/validation/validate_schemas.py` performed automated dry-run validation against live Atlas schema validators to catch syntax, type, or regex errors prior to bulk cluster ingestion.

#### Q218: How does the system handle historical ceremonies held across two venues simultaneously?
**Answer**: Early ceremonies (e.g., the 1st Annual GRAMMY Awards held simultaneously at the Beverly Hilton in Los Angeles and the Park Sheraton in New York) are modeled with primary venue references and linked secondary hosting records.

#### Q219: Why was synthetic template generation utilized for auxiliary administrative collections?
**Answer**: While historical nominations and winners are factual records, auxiliary collections (e.g., press media accreditations, audit logs, trophy serial numbers) lacked public archives. Structured templates were used to fulfill the strict academic quota of 50 documents per collection.

#### Q220: Where are the data acquisition and source manifests documented?
**Answer**: In `docs/data_acquisition_report.md`, `docs/data_sources_and_licensing.md`, and `sources/data-sources-manifest.md`.

---

# Section 13: Dedicated Questions on Licensing & Provenance

#### Q221: What is the holding of *Feist Publications v. Rural Telephone Service* and how does it apply here?
**Answer**: The Supreme Court ruled that purely factual compilations lacking original creative expression cannot be copyrighted. Factual names, dates, award categories, and historical outcomes are non-copyrightable facts in the public domain.

#### Q222: What does CC0 1.0 Universal licensing signify?
**Answer**: Creative Commons Zero waives all copyright and related rights worldwide, placing the dataset into the public domain for unrestricted academic or commercial use.

#### Q223: Under what legal provision are Recording Academy rulebook bylaws analyzed?
**Answer**: Under Educational Fair Use (17 U.S.C. § 107), which allows non-profit educational and academic research use of excerpts without infringing copyright.

#### Q224: What attributes are included in the mandatory `_source_provenance` subdocument?
**Answer**:
```json
{
  "_source_provenance": {
    "source_id": "SRC-01",
    "source_name": "Recording Academy Official Archives",
    "source_url": "https://www.grammy.com",
    "license_type": "Public Domain / Factual Information",
    "provenance_tier": "Primary Authoritative",
    "attribution": "National Academy of Recording Arts and Sciences",
    "acquired_timestamp": "2026-10-02T10:00:00Z"
  }
}
```

#### Q225: What percentage of documents in our database carry `_source_provenance`?
**Answer**: Exactly 100% of all 5,190 documents across all 50 collections.

#### Q226: How does the system verify license compliance in automated testing?
**Answer**: `tests/test_raw_data_acquisition.py` and `tests/test_final_audit.py` inspect sample documents across collections to ensure valid licensing declarations.

#### Q227: Can factual sports or music awards outcomes be proprietary under database laws in the US?
**Answer**: No. Unlike the European Union Database Directive, United States copyright law does not recognize a "sweat of the brow" doctrine; facts remain free for public academic analysis.

#### Q228: What is a provenance tier in our metadata?
**Answer**: A classification of source reliability: Tier 1 (Primary Authoritative: `grammy.com`), Tier 2 (Curated Open Repositories: Kaggle, MusicBrainz), Tier 3 (Secondary Public Records: Nielsen, Billboard, Variety).

#### Q229: What happens if an ingested record lacks source provenance during ETL?
**Answer**: The validation pipeline rejects the record and halts ingestion with a `ProvenanceValidationError`.

#### Q230: Where is the complete licensing matrix maintained?
**Answer**: In `docs/data_sources_and_licensing.md` and certified in `tests/final-audit-report.md`.
