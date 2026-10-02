# GRAMMY Awards Information & Analytics System

[![ADBMS System Validation CI](https://github.com/bharathwajverse/music-grammy-awards-db/actions/workflows/ci.yml/badge.svg)](https://github.com/bharathwajverse/music-grammy-awards-db/actions)
[![Academic Project](https://img.shields.io/badge/Course-Advanced%20DBMS-blue.svg)](#)
[![Database](https://img.shields.io/badge/Database-MongoDB%20Atlas-green.svg)](#)
[![Architecture](https://img.shields.io/badge/Architecture-5%20Distributed%20Databases-orange.svg)](#)
[![Collections](https://img.shields.io/badge/Collections-50%20Collections-purple.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](#)

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
| **Total** | **5 Databases** | **Integrated GRAMMY Awards Analytics System** | **50** | **4,500+ Ingested** | **500+ Typed Fields** |

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

## 4. Standard Project Directory Structure

```text
├── docs/                     # Architecture, instructions, data dictionary, status tracking
├── research/                 # Academic DBMS background research & citations
├── sources/                  # Dataset provenance records & licensing metadata
├── eer/                      # Conceptual EER diagrams & specialization models
├── relational-model/         # Relational schema translations & integrity constraints
├── normalization/            # Functional dependencies, NF proofs & denormalization strategies
├── mongodb/                  # MongoDB document models & Atlas connection configs
├── data/
│   ├── raw/                  # Pristine source data (strictly gitignored)
│   ├── processed/            # Processed JSON documents across 50 collections
│   └── validated/            # Production validated documents ready for cluster
├── scripts/
│   ├── processing/           # Extraction, transformation, and ID assignment scripts
│   └── validation/           # Schema, typing, and numerical quota validators
├── queries/
│   ├── crud/                 # Basic CRUD queries & filter operations
│   ├── advanced/             # Complex boolean, regex, array & logical operators
│   └── aggregation/          # Multi-stage aggregation pipelines ($group, $lookup, $facet)
├── tests/                    # Automated pytest test suites & schema verification
└── presentation/             # Final presentation slides, demos & system reports
```

---

## 5. Quick Start & Setup

### Prerequisites
- Python 3.11+
- Git
- MongoDB Atlas account (for cloud deployment) or MongoDB Compass (for local exploration)

### Clone & Install
```bash
git clone https://github.com/bharathwajverse/music-grammy-awards-db.git
cd music-grammy-awards-db

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Validation & Tests
```bash
# Pre-flight schema validation across all 50 collections
python scripts/validation/validate_system.py

# Run full pytest regression suite (162 tests)
pytest tests -v
```

### Run Syllabus Demonstrations
```bash
# Module 4: ACID Transactions
python scripts/transactions/demo_acid_transactions.py

# Module 5: Concurrency Control & Deadlock Handling
python scripts/concurrency/simulate_concurrent_voting.py

# Module 7: Log-Based Recovery & Backups
python scripts/recovery/backup_and_restore_drill.py

# Module 9: CRUD Demonstrations
python queries/basic_crud/crud_demonstration_suite.py

# Module 10: Advanced Aggregations & Query Plans
python queries/advanced_aggregation/module_10_pipelines.py
```

### Deploy to MongoDB Atlas
```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env and supply your MONGODB_URI or MONGODB_ATLAS_URI

# Verify Atlas connection & zero-secrets security compliance
python scripts/test_atlas_connection.py

# Ingest all 50 collections into MongoDB Atlas
python scripts/etl/load_atlas_databases.py
```

---

## 6. Documentation & Technical Specifications

Detailed design documents are maintained in [`docs/`](docs/):
- **Current Project Status & Roadmap**: [`docs/project-status.md`](docs/project-status.md)
- **Master Project Instructions**: [`docs/MASTER_PROJECT_INSTRUCTIONS.md`](docs/MASTER_PROJECT_INSTRUCTIONS.md)
- **Requirements Specifications**:
  - [Project Requirements Baseline](docs/requirements/project-requirements.md)
  - [Formal Acceptance Criteria](docs/requirements/acceptance-criteria.md)
  - [Team Responsibilities & Work Breakdown](docs/requirements/team-responsibilities.md)
  - [Database Boundaries & Partitioning](docs/requirements/database-boundaries.md)
- **Data Research & Provenance (Phases 2 & 3)**:
  - [Data Source Discovery Catalog](research/source-discovery.md)
  - [50-Collection Data Coverage Matrix](research/data-coverage-matrix.md)
  - [Master Source Register (CSV)](sources/source-register.csv)
  - [Formal Licensing & IP Audit Report](sources/licensing-report.md)
- **Collection Feasibility Analysis (Phase 4)**:
  - [Proposed 50 Collections Feasibility Specification](schemas/proposed-collections.md)
  - [Collection Feasibility Matrix (CSV)](schemas/collection-feasibility-matrix.csv)
- **System Architecture (Phase 5)**:
  - [Master System Architecture Specification](docs/architecture/system-architecture.md)
  - [End-to-End Data Flow & Validation Pipeline](docs/architecture/data-flow.md)
  - [Database Boundaries & Domain Encapsulation](docs/architecture/database-boundaries.md)
  - [System Topology Architecture](docs/architecture/system_topology.md)
- **Conceptual EER Modeling (Phase 6)**:
  - [Comprehensive EER Design Specification](docs/eer-design.md)
  - [EER Conceptual Model Diagram (PNG)](eer/grammy-eer.png)
  - [EER Source Draw.io File](eer/grammy-eer.drawio)
  - [Conceptual EER Theoretical Spec](docs/eer_diagrams/conceptual_eer_spec.md)
- **Relational Model & Relational Algebra (Phase 7)**:
  - [Relational Schema Catalog (50 Tables)](relational-model/schema.md)
  - [Primary, Candidate & Foreign Keys Matrix](relational-model/keys-and-relationships.md)
  - [Formal Relational Algebra Query Specifications & Trees](relational-model/relational-algebra-examples.md)
  - [Relational Reference DDL Schema](schemas/relational_ddl/relational_reference_schema.sql)
- **Functional Dependency & Key Analysis (Phase 8)**:
  - [Functional Dependencies & Dependency Theory](normalization/functional-dependencies.md)
  - [Candidate Keys & Prime Attribute Analysis](normalization/key-analysis.md)
- **Schema Normalization Proofs (Phase 9)**:
  - [First Normal Form (1NF) Specification & Transformation](normalization/1nf.md)
  - [Second Normal Form (2NF) Partial Dependencies & Heath's Theorem](normalization/2nf.md)
  - [Third Normal Form (3NF) Transitive Dependencies & Bernstein Synthesis](normalization/3nf.md)
  - [Boyce-Codd Normal Form (BCNF) Overlapping Keys & Auditor Slate](normalization/bcnf.md)
  - [Fourth Normal Form (4NF) Multivalued Dependencies & Fagin's Theorem](normalization/4nf.md)
  - [Fifth Normal Form (5NF/PJNF) Join Dependencies & Triadic Lossless Join](normalization/5nf.md)
  - [Master Normalization Summary & NoSQL Denormalization Synthesis](normalization/normalization-summary.md)
- **Physical Schema Denormalization (Phase 10)**:
  - [MongoDB Denormalization Decisions Catalog (12 Architecture Decisions)](denormalization/decisions.md)
  - [Embedding vs. Referencing Decision Framework & Anti-Pattern Prevention](denormalization/embed-vs-reference.md)
- **MongoDB Document Model & Validators (Phase 11)**:
  - [Master MongoDB Document Model Architecture](docs/mongodb-design.md)
  - [Master Collection Specifications Catalog (All 50 Collections)](mongodb/collection-specifications/README.md)
  - [Physical MongoDB Collection Validators Directory](mongodb/schema/README.md)
- **Data Provenance & Licensing**: [`docs/data_sources_and_licensing.md`](docs/data_sources_and_licensing.md)
- **Curriculum Syllabus Mapping**: [`docs/syllabus_mapping.md`](docs/syllabus_mapping.md)

---

## 7. License & Academic Integrity

- **License**: Released under the [MIT License](LICENSE).
- **Zero Secrets Policy**: Credentials must never be pushed to version control. See [`SECURITY.md`](SECURITY.md).
- **Academic Standards**: Real-world factual data only; no synthetic or fabricated information. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

