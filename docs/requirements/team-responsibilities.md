# Team Responsibilities & Work Breakdown: GRAMMY Awards Analytics System

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Document**: Five-Member Ownership Matrix & Academic Work Breakdown  
> **Status**: Frozen / Baseline Specification (Phase 1 Requirements Freeze)  
> **Version Control**: Git / GitHub (`bharathwajverse/music-grammy-awards-db`)  

---

## 1. Team Structure & Division of Labor

The project is structured across **five dedicated team members**, mirroring a distributed enterprise database team. Each member is assigned exclusive ownership of **one dedicated MongoDB database**, comprising at least 10 collections, 50+ documents per collection, and 10+ meaningful fields per document.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        FIVE-MEMBER OWNERSHIP & DATABASE MATRIX                         │
├──────────┬─────────────────────────┬───────────────────────────────┬───────────────────┤
│ Role     │ Database Assigned       │ Core Domain Scope             │ Primary Syllabus  │
│          │                         │                               │ Module Leadership │
├──────────┼─────────────────────────┼───────────────────────────────┼───────────────────┤
│ Member 1 │ `grammy_history_db`     │ Ceremonies, Venues, Telecasts,│ Module 6 (Storage)│
│          │                         │ Ratings, Milestones, Eras     │ Module 7 (Recovery│
├──────────┼─────────────────────────┼───────────────────────────────┼───────────────────┤
│ Member 2 │ `grammy_categories_db`  │ Award Fields, Categories,     │ Module 1 (EER)    │
│          │                         │ Lineage Trees, Voting Rules   │ Module 2 (1NF/2NF)│
├──────────┼─────────────────────────┼───────────────────────────────┼───────────────────┤
│ Member 3 │ `grammy_nominations_db` │ Nominated Works, Credits,     │ Module 4 (ACID)   │
│          │                         │ Submissions, Screening Logs   │ Module 5 (Locking)│
├──────────┼─────────────────────────┼───────────────────────────────┼───────────────────┤
│ Member 4 │ `grammy_winners_db`     │ Winners, Big Four Sweeps,     │ Module 9 (CRUD)   │
│          │                         │ Record Breakers, Trophies     │ Module 10 (Aggreg)│
├──────────┼─────────────────────────┼───────────────────────────────┼───────────────────┤
│ Member 5 │ `grammy_creators_db`    │ Artists, Producers, Engineers,│ Module 3 (BCNF/NF)│
│          │                         │ Labels, Songwriters, Groups   │ Cross-DB Integ.   │
└──────────┴─────────────────────────┴───────────────────────────────┴───────────────────┘
```

---

## 2. Member 1: History & Infrastructure (`grammy_history_db`)

**Domain Focus**: The macroscopic event history, logistics, viewership economics, and operational leadership of the Recording Academy.

### Collection Portfolio (10 Collections):
1. `ceremonies`: Core ceremony editions (edition number, ceremony date, broadcast year, executive producer, duration, total awards presented).
2. `venues`: Physical arenas and theaters hosting ceremonies (venue name, city, state, seating capacity, acoustics profile, geographic coordinates).
3. `telecast_broadcasters`: Television and streaming networks (network name, broadcast contract years, syndication scope, primary transmission format).
4. `viewership_ratings`: Nielsen viewership metrics (total viewers millions, household rating, 18-49 demographic share, peak quarter-hour audience).
5. `ceremony_hosts`: Master of ceremonies data (host individual/duo, opening monologue duration, prior hosting appearances, reception score).
6. `historic_milestones`: Seminal events in GRAMMY history (milestone year, breakthrough category, cultural significance, historical impact category).
7. `timeline_historical_eras`: Chronological eras (Golden Era, Classic Rock, MTV Era, Digital Explosion, Streaming Age with year bounds and characteristics).
8. `academy_leadership`: Trustees, chairpersons, and CEOs of the Recording Academy (officeholder name, tenure dates, institutional reforms enacted).
9. `press_media_accreditations`: Red carpet and press room media credentials (outlet name, media type, press pool category, accredited journalist count).
10. `lifetime_achievement_honors`: Special Merit Lifetime Achievement Awards presented at ceremonies (recipient, award year, citation, career era).

### Primary Syllabus Responsibilities:
- **Module 6 (Storage Architecture & RAID)**: Lead author for disk block allocation analysis, slotted-page calculations, WiredTiger cache sizing, and RAID 0/1/5/10 modeling for historical logs.
- **Module 7 (Recovery Concepts & Catastrophic Resilience)**: Lead author for Write-Ahead Logging (WAL) drills, WiredTiger journal crash simulation, and automated `mongodump` / `mongorestore` disaster recovery playbooks.

---

## 3. Member 2: Governance & Categories (`grammy_categories_db`)

**Domain Focus**: The taxonomic taxonomy, procedural governance, rulebooks, and voting machinery governing GRAMMY awards.

### Collection Portfolio (10 Collections):
1. `award_fields`: Genre umbrella fields (Field ID, field name, description, founding year, supervising craft committee).
2. `award_categories`: Granular award categories (Category ID, official name, field reference, current active status, maximum nominees permitted).
3. `category_lineage`: Historical taxonomy tree tracking ancestry, renames, and evolutions of categories across decades.
4. `eligibility_rules`: Formal rulebook constraints (product release window start/end, minimum running time, percentage of new recordings required).
5. `voting_procedures`: Multi-stage voting protocol definitions (first round balloting, nomination review committees, final round voting algorithms).
6. `category_quotas_limits`: Quantitative rule parameters (max submissions per member, voting caps per field, tie threshold percentages).
7. `craft_credit_definitions`: Official Academy definition of credited roles entitled to receive physical statuettes (e.g., AOTY producer threshold $\ge 33\%$).
8. `discontinued_categories`: Defunct award categories (deactivation year, rationale for deprecation, successor category reference).
9. `merged_split_history`: Structural category reorganizations (merger event dates, split details, pre-merger and post-merger category mappings).
10. `special_merit_categories`: Non-competitive categories (Trustees Award, Technical GRAMMY, Music Educator Award with selection guidelines).

### Primary Syllabus Responsibilities:
- **Module 1 (Relational Languages & EER Modeling)**: Lead author for conceptual EER diagrams (specialization/generalization of competitive vs. special merit categories, union types) and relational algebra queries.
- **Module 2 (Functional Dependencies & 1NF/2NF)**: Lead author for mathematical functional dependencies, attribute closures ($X^+$), and minimal cover ($F_{min}$) across category governance data.

---

## 4. Member 3: Submissions & Nominations (`grammy_nominations_db`)

**Domain Focus**: The core operational engine of the GRAMMYs—intake of creative works, screening committees, formal nominations, and granular craft credits.

### Collection Portfolio (10 Collections):
1. `nomination_entries`: Canonical nomination records (Nomination ID, ceremony, category, work reference, primary billed artist, ballot rank).
2. `nominated_works`: Master creative work records (album title, single title, ISRC/UPC code, release date, track duration, genre classification).
3. `nomination_credits`: Disaggregated creative participant credits for every nomination (creator ID, credited role, contribution percentage, statuette eligibility).
4. `submission_batches`: Pre-nomination intake batches submitted by record labels and academy members (batch ID, submitter org, submission count, status).
5. `voter_screening_batches`: First-round review committee audits determining category placement and eligibility compliance.
6. `tied_nominations`: Historic ballot ties resulting in extended nominee fields (e.g., 6, 8, or 10 nominees per category).
7. `nomination_audit_logs`: Independent accounting firm (Deloitte / PwC) audit certifications of voting results.
8. `genre_classifications`: Multi-dimensional genre tag mappings for submitted musical recordings.
9. `first_time_nominees`: Special tracking collection for breakthrough artists receiving their maiden career nomination.
10. `multi_nomination_packages`: Collections of creative works nominated across multiple discrete categories within the same ceremony.

### Primary Syllabus Responsibilities:
- **Module 4 (Transactions & ACID Properties)**: Lead author for multi-document ACID transactions simulating atomic submission intake and audit ledger updates with rollback handling.
- **Module 5 (Concurrency Control & Deadlock Handling)**: Lead author for multi-threaded concurrency simulations under Strict 2PL and Wait-For-Graph (WFG) cycle detection algorithms.

---

## 5. Member 4: Recognition & Winners (`grammy_winners_db`)

**Domain Focus**: The pinnacle of the award system—verified victory records, historical sweeps, physical trophy logistics, and cultural legacy tracking.

### Collection Portfolio (10 Collections):
1. `winner_records`: Official verified winners for every ceremony and category (Winner ID, nomination ID, category ID, presenter name, victory timestamp).
2. `big_four_sweeps`: Historic milestones tracking victories across the General Field (Album, Record, Song of the Year, and Best New Artist).
3. `record_breakers`: Statistical milestones (most wins in a single night, most lifetime wins, youngest/oldest winner records).
4. `acceptance_speeches`: Transcriptions and metadata of acceptance speeches (speaker, speech duration seconds, key dedications, broadcast censor flags).
5. `trophy_tracking`: Physical statuette logistics (serial number, casting date, metallurgical composition, recipient engraving status, delivery tracking).
6. `consecutive_winners`: Longitudinal tracking of back-to-back victories across consecutive ceremonies.
7. `hall_of_fame_inductions`: Historical recordings inducted into the GRAMMY Hall of Fame (recording title, recording year, induction ceremony).
8. `posthumous_awards`: Awards bestowed after the death of the honoree (recipient, estate representative accepting trophy, date of passing).
9. `historic_win_benchmarks`: Aggregated historical thresholds by genre, decade, and category.
10. `winner_press_releases`: Formal Academy press release announcements and media bulletins distributed upon award presentation.

### Primary Syllabus Responsibilities:
- **Module 9 (MongoDB CRUD Operations & Import/Export)**: Lead author for advanced CRUD operations, array operations, and automated ETL import/export pipelines.
- **Module 10 (Advanced Aggregations & Performance Optimization)**: Lead author for complex multi-stage aggregation pipelines (`$group`, `$lookup`, `$facet`, `$bucketAuto`) and compound/multikey indexing optimization.

---

## 6. Member 5: Creators & Industry Entities (`grammy_creators_db`)

**Domain Focus**: Master entity directories of the creative individuals, technical practitioners, and commercial institutions driving the music industry.

### Collection Portfolio (10 Collections):
1. `artists`: Solo performing vocalists and instrumentalists (Artist ID, legal name, stage name, birth date, nationality, active decades, primary genre).
2. `producers`: Record producers and vocal producers (Producer ID, production credits, studio affiliation, signature sonic techniques).
3. `audio_engineers`: Recording, mixing, mastering, and immersive audio engineers (Engineer ID, technical discipline, DAW environments, studio credits).
4. `songwriters_composers`: Lyricists and melody composers (Songwriter ID, PRO affiliation [ASCAP/BMI/SESAC], catalog size, signature compositions).
5. `arrangers_conductors`: Orchestral arrangers, brass/string arrangers, and conductors (Arranger ID, ensemble specializations, scoring background).
6. `record_labels`: Commercial record companies and imprints (Label ID, parent corporate entity, founding year, headquarters, distribution network).
7. `musical groups`: Duos, bands, choirs, and orchestras (Group ID, founding date, active status, lineup history, primary genre).
8. `group_memberships`: Relational mapping of individual artists into musical groups with joining and departure dates.
9. `creator_collaborations`: Documented recurring creative partnerships across artists, producers, and songwriters.
10. `creator_discographies`: Master catalog of released musical releases associated with credited creators.

### Primary Syllabus Responsibilities:
- **Module 3 (Higher Normal Forms & Justified Denormalization)**: Lead author for 3NF, BCNF, 4NF (multivalued dependencies in creator skillsets), 5NF proofs, and the academic justification for BSON denormalization.
- **Cross-Database Referential Integrity**: System-wide coordinator ensuring consistent usage of universal IDs (`CRT_{...}`, `WRK_{...}`, `LBL_{...}`) across all peer databases.

---

## 7. RACI Accountability Matrix Across Project Lifecycle

```
R = Responsible (Performs the work)
A = Accountable (Final approval & quality sign-off)
C = Consulted (Provides input / domain coordination)
I = Informed (Kept updated on progress)
```

| Lifecycle Phase / Milestone | M1 (History) | M2 (Categories) | M3 (Nominations) | M4 (Winners) | M5 (Creators) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Phase 1: Requirements Freeze** | R | R | R | R | A |
| **Phase 2: Source & Licensing Verification** | R | R | R | R | A |
| **Phase 3: Conceptual EER Modeling** | C | A / R | C | C | C |
| **Phase 4: Relational Model & Relational Algebra** | C | A / R | C | C | C |
| **Phase 5: Functional Dependencies & Normalization**| C | C | C | C | A / R |
| **Phase 6: MongoDB Document Model & Denormalization**| C | C | C | C | A / R |
| **Phase 7: Database Implementation on Atlas** | A / R | R | R | R | R |
| **Phase 8: Data Ingestion & Pre-Flight Validation** | R | R | A / R | R | R |
| **Phase 9: ACID Transactions (Module 4)** | I | I | A / R | I | I |
| **Phase 10: Concurrency Control (Module 5)** | I | I | A / R | I | I |
| **Phase 11: Storage & RAID Modeling (Module 6)** | A / R | I | I | I | I |
| **Phase 12: Recovery & Disaster Resilience (Module 7)**| A / R | I | I | I | I |
| **Phase 13: MongoDB CRUD & Import/Export (Module 9)** | I | I | I | A / R | I |
| **Phase 14: Advanced Aggregations (Module 10)** | I | I | I | A / R | I |
| **Phase 15: Final Testing & Academic Defense** | R | R | R | R | A |

---

## 8. Joint Team Protocols

1. **Deterministic Identifier Rule**: No member may invent an ad-hoc primary key scheme. All keys must conform to the agreed global regex patterns.
2. **Schema Mutability Protocol**: If a member requires a new field in another member's collection to support a foreign key or aggregation pipeline, a schema change request must be reviewed and tested in CI before merging.
3. **Continuous Peer Review**: Every milestone deliverable requires peer review by at least two other team members prior to submission for human user approval.
