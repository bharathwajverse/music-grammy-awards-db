# Oral Presentation & Live Demonstration Walkthrough Script

> **Course**: Advanced Database Management Systems (ADBMS) — Graduate Capstone  
> **System**: GRAMMY Awards Information & Analytics System  
> **Document**: Formal Oral Defense Script & Live Demonstration Protocol  
> **Presentation Duration**: 20 Minutes (15 min Presentation + 5 min Live Demo)  
> **Team Structure**: Five-Member Distributed Database Team (Members 1–5)  

---

## 1. Presentation Overview & Time Allocation Matrix

| Slide # | Slide Title | Speaking Member | Target Time | Key Emphasis / Script Cue |
| :---: | :--- | :---: | :---: | :--- |
| **1** | Title & Introduction | Member 1 | 0:00 – 0:45 | System scope, 5 databases, 50 collections, 5,190 docs |
| **2** | Problem Statement | Member 1 | 0:45 – 1:30 | Heterogeneity, microservice boundaries, join explosion |
| **3** | Project Objectives | Member 1 | 1:30 – 2:15 | Modules 1–10 syllabus alignment, quotas, integrity |
| **4** | Real-World Data & Provenance | Member 2 | 2:15 – 3:00 | Recording Academy archives, Kaggle, MusicBrainz, CC0 |
| **5** | System Architecture | Member 2 | 3:00 – 3:45 | Distributed data fabric, universal IDs, join federation |
| **6** | Five Dedicated Databases | Member 2 | 3:45 – 4:30 | 5-member ownership, collection portfolios, doc counts |
| **7** | Conceptual EER Design | Member 3 | 4:30 – 5:15 | Generalization, union types, conceptual aggregation |
| **8** | Relational Model & Relational Algebra | Member 3 | 5:15 – 6:00 | 50 schemas, relational algebra, relational division ($\div$) |
| **9** | Normalization & Denormalization | Member 3 | 6:00 – 6:45 | 1NF–5NF proofs, BCNF algorithm, latency trade-offs |
| **10** | MongoDB Document Modeling | Member 4 | 6:45 – 7:30 | Hybrid design, embedding vs referencing, `$jsonSchema` |
| **11** | Comprehensive Data Statistics | Member 4 | 7:30 – 8:15 | 5,190 docs, 4.06 MB uncompressed, 2.72 MB compressed |
| **12** | CRUD Operations Architecture | Member 4 | 8:15 – 9:00 | Type safety, projections, atomic updates, audit logs |
| **13** | Advanced Querying Capabilities | Member 4 | 9:00 – 9:45 | `$elemMatch`, ESR rule, complex compound filters |
| **14** | Complex Aggregation Pipelines | Member 5 | 9:45 – 10:30 | Multi-stage pipelines, `$facet`, `$bucketAuto` |
| **15** | Transactions & Concurrency Control | Member 5 | 10:30 – 11:15 | Multi-doc ACID commit/rollback (73.42ms), MVCC, 2PL |
| **16** | Physical Storage & Crash Recovery | Member 5 | 11:15 – 12:00 | WiredTiger Slotted-Page, Snappy (32.9%), ARIES drill |
| **17** | Comprehensive Validation & QA | Member 1 | 12:00 – 12:45 | 629 passing pytest tests, 0 orphans, 44 custom indexes |
| **18** | Empirical Results & Achievements | Member 1 | 12:45 – 13:30 | IXSCAN benchmarks, 99.8% docsExamined reduction |
| **19** | System Limitations | Member 1 | 13:30 – 14:15 | Atlas M0 constraints, data sparsity, template records |
| **20** | Conclusion & Future Scope | Member 1 | 14:15 – 15:00 | Synthesis, M10 scaling, GraphQL federation, Kafka stream |
| **DEMO** | Live Atlas & Terminal Demonstration | All Members | 15:00 – 20:00 | Execution of live PyMongo queries, ACID demo, pytest |

---

## 2. Slide-by-Slide Verbal Defense Script

### Slide 1: Title (Member 1)
> *"Good morning, respected professors and evaluation committee members. Today, our team is proud to present the capstone defense of our graduate Advanced Database Management Systems project: the **GRAMMY Awards Information & Analytics System**.*  
> *Rather than developing a superficial web application, our project addresses a distributed, enterprise-scale data engineering challenge: modeling, ingesting, normalizing, querying, and analyzing the 67-year institutional lifecycle of the Recording Academy from 1959 to the present.*  
> *Our implementation spans **five autonomous MongoDB databases**, comprising **50 collections**, **5,190 schema-validated documents**, and **44 custom B+ tree indexes** deployed on MongoDB Atlas and certified against all 10 syllabus modules with 629 automated tests."*

### Slide 2: Problem Statement (Member 1)
> *"Modeling institutional music award governance introduces four fundamental database engineering challenges.*  
> *First is **Domain Heterogeneity and Polymorphism**: creative works are collaborative networks of lead performers, producers, arrangers, and audio engineers. In relational databases, resolving full credit rosters requires 8 or more table joins, leading to catastrophic join explosion. In naive NoSQL models, unconstrained arrays lead to document bloat.*  
> *Second is **Microservice Boundaries**: macro ceremony operations, award taxonomies, nomination balloting, winner verification, and creator discographies must operate in isolated databases. Yet on multi-tenant cloud tiers like MongoDB Atlas M0, cross-database `$lookup` operations are prohibited by the engine.*  
> *Third, we face the classic tension between **Strict Normalization vs. Analytical Read Performance**; and fourth, the requirement for **Multi-Document ACID Atomicity** under high-scrutiny ballot certification."*

### Slide 3: Project Objectives (Member 1)
> *"To address these challenges, we formulated five core engineering objectives aligned directly with the Advanced DBMS syllabus.*  
> *We aimed to partition the domain into five autonomous databases satisfying all quotas; construct formal conceptual EER models with advanced generalization hierarchies; provide mathematical proofs for 1NF through 5NF alongside controlled denormalization; implement multi-document ACID transactions with snapshot isolation; evaluate physical storage mechanics and crash recovery algorithms; and engineer application-level join federation executing in under 15 milliseconds.*  
> *I will now hand over to Member 2 to discuss our data provenance and architectural partitioning."*

### Slide 4: Real-World Data & Provenance (Member 2)
> *"Thank you, Member 1. Every document in our database is grounded in empirical reality. We acquired our data from five authoritative sources: the official Recording Academy archives at `grammy.com`, the curated Kaggle Grammy Awards dataset spanning 1958 through 2024, the MetaBrainz MusicBrainz database for canonical creator identifiers and artist MBIDs, Nielsen Media Research for broadcast ratings, and Wikidata for venue geolocation.*  
> *To guarantee legal and academic compliance, all factual award outcomes are utilized under the non-copyrightable factual principles established in Feist v. Rural. Open datasets conform to CC0 1.0 Universal, and institutional rulebooks are analyzed under Educational Fair Use (17 U.S.C. § 107).*  
> *Crucially, 100% of our 5,190 documents contain an immutable `_source_provenance` subdocument recording source IDs, licensing classes, and acquisition timestamps, ensuring complete auditability."*

### Slide 5: System Architecture (Member 2)
> *"Our physical architecture mirrors a distributed microservice data fabric hosted on MongoDB Atlas (`Cluster0`, AWS `us-east-1`).*  
> *As shown in the architecture diagram, the five databases operate independently. The central nomination engine in `grammy_nominations_db` references macro ceremonies in `grammy_history_db`, category taxonomy rules in `grammy_categories_db`, and master artist records in `grammy_creators_db`. Official verified outcomes flow into `grammy_winners_db`.*  
> *Because Atlas M0 throws `AtlasError 8000` when executing server-side cross-database `$lookup` pipelines, we designed an enterprise application-level distributed join federation engine in PyMongo. By querying indexed deterministic identifiers using `$in` batches, we achieve cross-database joins in under 15 milliseconds while maintaining zero orphan references."*

### Slide 6: Five Dedicated Databases (Member 2)
> *"The system is partitioned across our five team members, each holding dedicated ownership of one database:*  
> *Member 1 leads `grammy_history_db` with 10 collections and 645 documents covering ceremonies, venues, and ratings.*  
> *Member 2 leads `grammy_categories_db` with 10 collections and 650 documents governing award fields, category lineages, and voting rules.*  
> *Member 3 leads `grammy_nominations_db` with 10 collections and 1,990 documents managing nominated works and craft credits.*  
> *Member 4 leads `grammy_winners_db` with 10 collections and 985 documents certifying winners and statuette logistics.*  
> *Member 5 leads `grammy_creators_db` with 10 collections and 920 documents cataloging creators, audio engineers, and record labels.*  
> *In total, our system maintains exactly 50 collections and 5,190 schema-validated documents, with every document containing 12 to 13 rich domain fields, far exceeding project requirements. Member 3 will now present our theoretical modeling."*

### Slide 7: Conceptual EER Design (Member 3)
> *"Thank you, Member 2. In Module 1, we formulated a formal Enhanced Entity-Relationship schema adhering strictly to Elmasri & Navathe standards.*  
> *Our EER model incorporates advanced constructs: strong entities like `CEREMONY`, `VENUE`, and `WORK`; weak entities such as `VIEWERSHIP_RATING` identified via `CEREMONY`; and a two-tier specialization hierarchy where `CREATOR` is generalized into `INDIVIDUAL_CREATOR` and `ORGANIZATIONAL_CREATOR` with disjoint and total constraints, while `INDIVIDUAL_CREATOR` specializes into overlapping roles: `ARTIST`, `PRODUCER`, `AUDIO_ENGINEER`, and `SONGWRITER`.*  
> *We also modeled category union types—where `AWARD_RECIPIENT` is the union of `ARTIST` and `MUSICAL_GROUP`—and conceptual aggregation, where the composite relationship of creator, work, and category is treated as a higher-level aggregate entity associated with nomination credits."*

### Slide 8: Relational Model & Relational Algebra (Member 3)
> *"We translated our conceptual model into 50 formal relational schemas, preserving foreign keys and associative relations for many-to-many relationships.*  
> *We formulated and verified all seven fundamental operations of relational algebra. Most notably, we formulated Relational Division ($\div$) to solve the classic complex query: 'Find all creators who have earned nominations across all Big Four General Field categories.'*  
> *By dividing the projection of creator IDs and category IDs from `NOMINATION_CREDITS` by the projection of category IDs from `BIG_FOUR_CATEGORIES`, our relational expression mathematically isolates this elite cohort without requiring nested procedural loops."*

### Slide 9: Normalization & Controlled Denormalization (Member 3)
> *"In Modules 2 and 3, we analyzed functional dependencies using Armstrong's Axioms to derive attribute closures and compute minimal covers ($F_{min}$).*  
> *We developed rigorous mathematical proofs showing step-by-step progression through 1NF, 2NF, 3NF, BCNF, 4NF, and 5NF.*  
> *However, database theory also teaches us that pure BCNF decomposition forces join-heavy workloads that degrade read performance. For our read-intensive analytics, an 8-table join took over 300 milliseconds. We therefore implemented an academically justified controlled denormalization strategy: embedding immutable biographical strings into nomination entries and caching pre-computed aggregate counts. This reduced analytical query latency by 88% while remaining safely within MongoDB's 16 MB document limit. Member 4 will now discuss our document modeling and data access layer."*

### Slide 10: MongoDB Document Modeling & JSON Schema (Member 4)
> *"Thank you, Member 3. In Module 8, we translated our normalized model into high-performance BSON document schemas.*  
> *We adopted a hybrid document modeling approach: embedding tightly-coupled, bounded 1:1 and 1:N relations—such as source provenance metadata and craft credit role specifications—to guarantee atomic single-document reads; while referencing unbounded 1:N relations—such as the hundreds of nominations per ceremony—using universal deterministic string IDs.*  
> *To enforce enterprise-grade data hygiene, we deployed strict server-side `$jsonSchema` validators across all 50 collections on MongoDB Atlas, validating BSON data types, numerical ranges, and regex patterns on every write."*

### Slide 11: Comprehensive Data Statistics (Member 4)
> *"Our physical database footprint demonstrates rigorous engineering discipline.*  
> *Across the five databases, our live cluster hosts 5,190 validated documents. `grammy_nominations_db` represents the largest operational volume with 1,990 documents, followed by `grammy_winners_db` with 985 documents.*  
> *Live introspection of our WiredTiger storage engine revealed 4.06 megabytes of uncompressed BSON data, compressed down to 2.72 megabytes on disk via Snappy—delivering a 32.9% net storage savings. Our 44 custom B+ tree indexes occupy 3.15 megabytes, ensuring all key query pathways remain resident in memory."*

### Slide 12: CRUD Operations Architecture (Member 4)
> *"Our data access layer implements standardized, type-safe CRUD operations across all collections.*  
> *Create operations enforce schema pre-validation and catch duplicate key collisions on natural business keys. Read operations utilize selective projections to return only required attributes over the network. Update operations leverage atomic operators like `$set`, `$inc`, and `$addToSet` alongside document versioning for optimistic concurrency control. Delete operations execute referential pre-checks and record tombstone audit records to prevent accidental orphan creation."*

### Slide 13: Advanced Querying Capabilities (Member 4)
> *"In Module 9, we developed an extensive suite of advanced queries.*  
> *We implemented complex multi-condition filters combining `$and`, `$or`, and `$in`, as well as precise array inspection using `$elemMatch` to query multi-contributor credits.*  
> *Critically, all advanced queries were engineered to adhere to the Equality, Sort, Range (ESR) indexing guideline, ensuring that MongoDB resolves filters and sorts directly from index keys without memory-intensive sort stages. Member 5 will now discuss our transactions, concurrency, storage, and recovery."*

### Slide 14: Complex Aggregation Pipelines (Member 5)
> *"Thank you, Member 4. In Module 10, we engineered multi-stage analytical aggregation pipelines.*  
> *Our pipelines combine `$match`, `$group`, `$sort`, `$project`, and `$unwind` to calculate historical victory distributions, multi-category sweeps, and running averages.*  
> *Furthermore, we leveraged `$facet` and `$bucketAuto` to generate multi-dimensional analytical dashboards in a single database roundtrip, simultaneously aggregating genre distributions and partitioning historical eras into temporal buckets."*

### Slide 15: Transactions & Concurrency Control (Member 5)
> *"In Modules 4 and 5, we addressed transaction processing and concurrency control.*  
> *We implemented multi-document ACID transactions using PyMongo sessions with `ReadConcern("snapshot")` and `WriteConcern("majority")`.*  
> *We demonstrated this via an official Winner Certification Workflow spanning ballots, trophies, and audit ledgers. Successful commits completed in 73.42 milliseconds. When we injected a simulated duplicate key error, the transaction rolled back 100% of mutations with zero orphan records.*  
> *For concurrency, we modeled classical Strict 2PL and Wait-For Graph (WFG) cycle detection, and contrasted them with WiredTiger's internal lock-free document MVCC and optimistic conflict retry logic. In a live simulation with 10 concurrent threads executing 100 atomic updates, our system achieved exactly zero Lost Updates."*

### Slide 16: Physical Storage & Crash Recovery (Member 5)
> *"In Modules 6 and 7, we evaluated physical storage architecture and database recovery.*  
> *We analyzed memory hierarchy latencies, slotted-page record layout, B+ tree leaf chaining, and RAID write penalties, proving why RAID 10's 2 I/O penalty is superior to RAID 5's 4 I/O penalty for write-heavy logging.*  
> *For recovery, we formalized Write-Ahead Logging and the three phases of ARIES: Analysis, Redo Repeating History, and Undo with Compensation Log Records.*  
> *We executed a controlled disaster recovery drill on our Atlas cluster, injecting corruption into collection state and performing an automated restore. Post-restore verification proved 100% bitwise SHA-256 state parity. Member 1 will now conclude our presentation."*

### Slide 17: Comprehensive Validation & Quality Assurance (Member 1)
> *"Thank you, Member 5. Our system's reliability is proven by an automated test suite comprising 24 test files and 629 passing pytest tests with a 100% pass rate.*  
> *Our test suite verifies every facet of the system: schema validation, quota compliance, Armstrong's Axioms minimal covers, 1NF–5NF proofs, ACID commit/rollback, WFG cycle detection, Snappy compression, ARIES recovery parity, and cross-database referential closure.*  
> *Every single test passes deterministically on our live cluster."*

### Slide 18: Empirical Results & System Achievements (Member 1)
> *"The empirical achievements of our project speak for themselves.*  
> *We deployed 5 autonomous databases and 50 collections hosting 5,190 documents. We achieved 100% referential integrity with zero orphan records across 11 inter-database relationships.*  
> *Our 44 custom indexes transitioned 100% of benchmark queries from `COLLSCAN` to `IXSCAN`, slashing documents examined by up to 99.8%. Multi-document ACID commits execute in 73.42 milliseconds, Snappy compression delivers 32.9% storage savings, and distributed cross-database joins resolve in under 15 milliseconds."*

### Slide 19: System Limitations (Member 1)
> *"In the spirit of rigorous academic honesty, we explicitly document our system's boundaries.*  
> *First, MongoDB Atlas M0 shared cluster limits storage to 512 MB and disallows native cross-database `$lookup`, requiring application-level join federation.*  
> *Second, early historical ceremonies (1959–1965) feature sparse viewership ratings and secondary craft credit documentation in surviving archives.*  
> *Third, application-level joins provide eventual consistency but lack distributed Two-Phase Commit across disparate databases.*  
> *Finally, while all primary entities are authentic historical facts, auxiliary administrative collections utilize structured template instances to fulfill our strict 50-document quota."*

### Slide 20: Conclusion & Future Scope (Member 1)
> *"In conclusion, the GRAMMY Awards Information & Analytics System demonstrates a complete, mathematically grounded, and enterprise-tested DBMS implementation spanning all 10 modules of the graduate curriculum.*  
> *Our future roadmap envisions migrating to a dedicated Atlas M10+ replica set with sharding, deploying an Apollo GraphQL Federation layer for unified cross-database querying, and integrating MongoDB Change Streams with Apache Kafka for real-time ballot tabulation.*  
> *We will now transition to our live system demonstration and welcome questions from the evaluation committee. Thank you."*

---

## 3. Live Demonstration Protocol (5 Minutes)

### Step 1: Automated Test Suite Execution (60 Seconds)
- Run `python -m pytest` from terminal in project root.
- Highlight: 629+ tests passing in ~35 seconds with zero failures across all 10 modules.

### Step 2: Live Cluster Introspection (60 Seconds)
- Open MongoDB Compass or run `python scripts/storage/generate_data_dictionary.py`.
- Verify the 5 databases, 50 collections, and 5,190 schema-validated documents.

### Step 3: Application-Level Cross-Database Join (60 Seconds)
- Execute `python scripts/integration/cross_database_validation.py`.
- Demonstrate: 4 real-world federated joins executing in $< 15\text{ ms}$ with 0 orphan records.

### Step 4: Multi-Document ACID Transaction Demo (60 Seconds)
- Run `python scripts/transactions/run_transaction_demo.py`.
- Demonstrate: Commit scenario in ~73 ms across 3 collections; followed by rollback scenario verifying zero state leakage.

### Step 5: Indexing Optimization & Explain Plan (60 Seconds)
- Run `python scripts/indexes/verify_indexes.py`.
- Demonstrate: Explain plan output showing `IXSCAN` execution and 99.8% reduction in `docsExamined`.
