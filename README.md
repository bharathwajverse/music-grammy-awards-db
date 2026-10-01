# GRAMMY Awards Information & Analytics System

[![Academic Project](https://img.shields.io/badge/Course-Advanced%20DBMS-blue.svg)](#)
[![Database](https://img.shields.io/badge/Database-MongoDB%20Atlas-green.svg)](#)
[![Architecture](https://img.shields.io/badge/Architecture-5%20Distributed%20Databases-orange.svg)](#)
[![Collections](https://img.shields.io/badge/Collections-50%20Collections-purple.svg)](#)
[![Syllabus](https://img.shields.io/badge/Modules-10%20Modules%20Demonstrated-brightgreen.svg)](#)

An enterprise-grade, distributed academic DBMS project modeling, ingesting, validating, and analyzing the complete historical and operational corpus of the **National Academy of Recording Arts and Sciences (Recording Academy) GRAMMY Awards (1959–Present)**.

---

## 1. System Overview

The **GRAMMY Awards Information & Analytics System** partitions the entire GRAMMY domain into **five separate, referentially unified MongoDB databases**, each designed and maintained by one of the five group members.

| Member | Database Name | Domain Scope | Collections | Min. Documents / Coll | Min. Fields / Doc |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Member 1** | `grammy_history_db` | Ceremonies, venues, telecasts, ratings, hosts, milestones, eras, accreditations | 10 | 50+ | 10+ |
| **Member 2** | `grammy_categories_db` | Fields, categories, historical lineage, eligibility rules, voting rules, quotas | 10 | 50+ | 10+ |
| **Member 3** | `grammy_nominations_db` | Nomination entries, works, credits, submissions, screening, tied ballots, audits | 10 | 50+ | 10+ |
| **Member 4** | `grammy_winners_db` | Winners, Big Four sweeps, record breakers, speeches, trophies, streaks, benchmarks | 10 | 50+ | 10+ |
| **Member 5** | `grammy_creators_db` | Artists, producers, engineers, songwriters, arrangers, record labels, groups | 10 | 50+ | 10+ |
| **Total** | **5 Databases** | **Integrated GRAMMY Awards Analytics System** | **50** | **2,500+ Total** | **500+ Total Fields** |

---

## 2. Core Academic Syllabus Mapping (Modules 1–10)

This project is explicitly structured to demonstrate all 10 modules of the Advanced DBMS curriculum:

1. **Module 1**: Relational Query Languages, Relational Algebra ($\sigma, \pi, \cup, \cap, -, \times, \bowtie, \rho, \div$), EER Modeling, Specialization, Generalization, Aggregation, and Union Types.
2. **Module 2**: Functional Dependencies, Armstrong's Axioms, Minimal Cover ($F_{min}$), Schema Refinement, 1NF, and 2NF.
3. **Module 3**: 3NF, BCNF, 4NF (Multivalued Dependencies $X \twoheadrightarrow Y$), 5NF (Join Dependencies $\bowtie$), Lossless-Join Decomposition, and Justified Denormalization.
4. **Module 4**: Transactions, Multi-Document ACID Transactions, Transaction Lifecycle & States, Serial Schedules, Conflict and View Serializability.
5. **Module 5**: Concurrency Control, Shared & Exclusive Locks, Strict 2-Phase Locking (S2PL), Timestamp Ordering Protocols, Wait-For-Graphs, and Deadlock Handling.
6. **Module 6**: Storage Architecture, RAID Levels (0, 1, 5, 10), Record Layouts (Fixed vs Variable), Slotted-Page Organization, B-Tree Indexes, and System Data Dictionaries.
7. **Module 7**: Recovery Concepts, Write-Ahead Logging (WAL / Journaling), Shadow Paging vs Log Recovery, Fuzzy Checkpoints, and Catastrophic Disaster Recovery.
8. **Module 8**: NoSQL Foundations, CAP Theorem, WiredTiger Architecture, MongoDB Atlas Cluster Topology, and MongoDB Compass Visualization.
9. **Module 9**: MongoDB CRUD Operations, Projection, Filter Operators, Bulk Operations, and Database Import/Export (`mongoimport`/`mongoexport`).
10. **Module 10**: Advanced Aggregation Pipelines (`$match`, `$project`, `$group`, `$unwind`, `$lookup`, `$facet`), Array Operators (`$elemMatch`, `$filter`), Multikey & Compound Indexes, and `explain("executionStats")` Optimization.

---

## 3. Global Deterministic Identifier Scheme

Referential integrity across all five distributed databases is maintained using deterministic global identifiers:

- `CEREMONY_{NNN}`: e.g., `CEREMONY_065` (65th Annual GRAMMY Awards, 2023)
- `CAT_{SLUG}`: e.g., `CAT_AOTY` (Album of the Year)
- `FLD_{SLUG}`: e.g., `FLD_GENERAL` (General Field)
- `WRK_{SLUG}`: e.g., `WRK_RENAISSANCE_2022` (Musical Work / Album)
- `NOM_{CEREMONY}_{CAT}_{SEQ}`: e.g., `NOM_065_AOTY_01` (Nomination Entry)
- `WIN_{NOMINATION_ID}`: e.g., `WIN_NOM_065_AOTY_01` (Winner Record)
- `CRT_{SLUG}`: e.g., `CRT_BEYONCE_001` (Creator / Performer / Producer)
- `LBL_{SLUG}`: e.g., `LBL_COLUMBIA_001` (Record Label)
- `VEN_{SLUG}`: e.g., `VEN_CRYPTO_LA` (Crypto.com Arena)

---

## 4. Documentation & Verification Roadmap

Detailed architectural design documents are maintained in [`docs/`](docs/):
- **System Architecture**: [`docs/architecture/system_topology.md`](docs/architecture/system_topology.md)
- **Data Dictionary (50 Collections)**: [`docs/architecture/data_dictionary.md`](docs/architecture/data_dictionary.md)
- **Conceptual EER Specification**: [`docs/eer_diagrams/conceptual_eer_spec.md`](docs/eer_diagrams/conceptual_eer_spec.md)
- **Data Provenance & Licensing**: [`docs/data_sources_and_licensing.md`](docs/data_sources_and_licensing.md)
- **Curriculum Syllabus Mapping**: [`docs/syllabus_mapping.md`](docs/syllabus_mapping.md)

---

## 5. Security & Academic Integrity Guidelines

1. **Zero Secrets in Git**: Never commit `.env` or plain text connection strings. Use `.env.example` as a template.
2. **Authentic Data Only**: No synthetic or fabricated dummy data. All information originates from official Recording Academy archives, verified CC0/CC-BY datasets, or MusicBrainz open data.
3. **Phased Execution**: Every phase requires automated schema validation and human checkpoint approval before advancing.
