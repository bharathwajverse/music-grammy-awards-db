# Database Boundaries & Distributed Domain Architecture

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Document**: Multi-Database Partitioning, Domain Encapsulation & Inter-Database Reference Topology  
> **Status**: Frozen / Baseline Specification (Phase 1 Requirements Freeze)  
> **Version Control**: Git / GitHub (`bharathwajverse/music-grammy-awards-db`)  

---

## 1. System Partitioning Rationale

The **GRAMMY Awards Information & Analytics System** deliberately avoids the monolithic "single database" anti-pattern in favor of a distributed multi-database architecture comprising **five discrete MongoDB databases**.

### Core Architecture Drivers:
1. **Academic Multi-Database Simulation**: Mirrors real-world enterprise architectures where distinct business domains (e.g., event operations, governance/compliance, intake/auditing, honors, and master talent directories) operate independent database clusters maintained by dedicated domain engineering teams.
2. **Domain Isolation & Bounded Contexts**: Enforces Domain-Driven Design (DDD) principles. Operational nomination intake does not pollute historical event logs, nor do mutable voting rules compromise the immutable master records of historical winners.
3. **Independent Scaling & Tiered Workloads**: High-velocity read traffic during telecasts (viewership ratings and live winner announcements) can scale horizontally without placing lock contention on back-office voter screening and accounting audit tables.
4. **Team Member Accountability**: Each member of the five-person team holds autonomous administrative ownership over their assigned schema and data pipeline while collaborating via standardized foreign reference interfaces.

---

## 2. Distributed Database Landscape

```
                        ┌────────────────────────────────────────────────────────┐
                        │      MongoDB Atlas Cluster (cluster0.xhjfpv2)          │
                        └──────────────────────────┬─────────────────────────────┘
                                                   │
         ┌─────────────────────┬───────────────────┼───────────────────┬─────────────────────┐
         ▼                     ▼                   ▼                   ▼                     ▼
┌─────────────────┐   ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   ┌─────────────────┐
│grammy_history_db│   │grammy_categories│ │grammy_nomination│ │grammy_winners_db│   │grammy_creators_ │
│                 │   │      _db        │ │      s_db       │ │                 │   │       db        │
│(Member 1 Scope) │   │(Member 2 Scope) │ │(Member 3 Scope) │ │(Member 4 Scope) │   │(Member 5 Scope) │
├─────────────────┤   ├─────────────────┤ ├─────────────────┤ ├─────────────────┤   ├─────────────────┤
│• ceremonies     │   │• award_fields   │ │• nomination_entr│ │• winner_records │   │• artists        │
│• venues         │   │• award_categorie│ │• nominated_works│ │• big_four_sweeps│   │• producers      │
│• telecasts      │   │• category_lineag│ │• nomination_cred│ │• record_breakers│   │• audio_engineers│
│• viewership     │   │• eligibility_rul│ │• submissions    │ │• speeches       │   │• songwriters    │
│• hosts          │   │• voting_rules   │ │• screening_batch│ │• trophy_tracking│   │• arrangers      │
│• milestones     │   │• category_quotas│ │• tied_nomination│ │• consecutive_win│   │• record_labels  │
│• eras           │   │• craft_credit_de│ │• audit_logs     │ │• hall_of_fame   │   │• musical_groups │
│• leadership     │   │• discontinued_ca│ │• genres         │ │• posthumous_awar│   │• group_members  │
│• media_accred   │   │• merged_split_hi│ │• first_time_nom │ │• win_benchmarks │   │• collaborations │
│• lifetime_honors│   │• special_merit  │ │• multi_packages │ │• press_releases │   │• discographies  │
└─────────────────┘   └─────────────────┘ └─────────────────┘ └─────────────────┘   └─────────────────┘
```

---

## 3. Detailed Database Boundaries & Collection Catalogs

### 3.1. Database 1: `grammy_history_db` (Lead: Member 1)
- **Domain Scope**: Event logistics, temporal milestones, venue geography, broadcast television metrics, and Academy governance history.
- **Invariants**:
  - Contains NO creative work titles, audio engineer credits, or nomination ballots.
  - Acts as the temporal and spatial anchor for the entire system through `ceremony_id` and `venue_id`.
- **Collections**:
  1. `ceremonies` (`CEREMONY_{NNN}`): Master ceremony editions, dates, broadcast years, and operational summaries.
  2. `venues` (`VEN_{SLUG}`): Physical locations (Crypto.com Arena, Madison Square Garden) with seating capacities and geo-coordinates.
  3. `telecast_broadcasters` (`TCAST_{SLUG}`): Networks and digital broadcast agreements (CBS, ABC, NBC).
  4. `viewership_ratings` (`RAT_{CEREMONY}`): Nielsen household ratings, viewer volume, demographic breakdowns.
  5. `ceremony_hosts` (`HOST_{CEREMONY}_{SEQ}`): Master of ceremonies records, monologue times, performance receptions.
  6. `historic_milestones` (`MLS_{SLUG}`): Landmark moments (first satellite telecast, first rap performance).
  7. `timeline_historical_eras` (`ERA_{SLUG}`): Defined historical epochs (e.g., Vinyl Era, CD Boom, Digital Streaming Era).
  8. `academy_leadership` (`LEAD_{SLUG}`): Recording Academy presidents, trustees, and operational reforms.
  9. `press_media_accreditations` (`MED_{CEREMONY}_{SEQ}`): Press room and red carpet media organization passes.
  10. `lifetime_achievement_honors` (`LTA_{SLUG}`): Non-competitive Special Merit honors presented during ceremonies.

### 3.2. Database 2: `grammy_categories_db` (Lead: Member 2)
- **Domain Scope**: Award taxonomy, category genealogical trees, qualification rules, and voting quotas.
- **Invariants**:
  - Contains NO specific nominee names or ceremony winners.
  - Defines the formal rules and limits that govern whether a submission is legally permitted to exist.
- **Collections**:
  1. `award_fields` (`FLD_{SLUG}`): Broad genre clusters (General Field, Pop, Rock, Classical, Jazz).
  2. `award_categories` (`CAT_{SLUG}`): Specific award categories (Album of the Year, Best New Artist).
  3. `category_lineage` (`LIN_{SLUG}`): Historical category parentage, name changes, and evolution trees.
  4. `eligibility_rules` (`ELIG_{SLUG}`): Formal criteria (release windows, minimum playing times, track counts).
  5. `voting_procedures` (`VOTE_{SLUG}`): Procedural rules for nomination round and final round member balloting.
  6. `category_quotas_limits` (`QTA_{SLUG}`): Quantitative caps on submissions, member ballots, and nominees.
  7. `craft_credit_definitions` (`CRF_{SLUG}`): Academy thresholds for which craft roles receive statuettes (e.g., $\ge 33\%$ AOTY rule).
  8. `discontinued_categories` (`DISC_{SLUG}`): Deprecated or retired award categories with retirement rationales.
  9. `merged_split_history` (`MSH_{SLUG}`): Structural history of category fusions and divisions.
  10. `special_merit_categories` (`SMC_{SLUG}`): Governance specifications for honorary and non-competitive awards.

### 3.3. Database 3: `grammy_nominations_db` (Lead: Member 3)
- **Domain Scope**: Raw and screened submissions, nomination ballots, nominated works, and granular craft credit rosters.
- **Invariants**:
  - Contains NO assumptions about who won; records solely that an entry was officially nominated.
  - Represents the largest transactional footprint in the system.
- **Collections**:
  1. `nomination_entries` (`NOM_{CEREMONY}_{CAT}_{SEQ}`): Canonical nomination ballot positions.
  2. `nominated_works` (`WRK_{SLUG}`): Master recording records with UPC/ISRC metadata and release dates.
  3. `nomination_credits` (`CRED_{NOM}_{SEQ}`): Granular credit mappings allocating roles to creative participants.
  4. `submission_batches` (`SUB_{BATCH}_{SEQ}`): Record label and member submission intake batches.
  5. `voter_screening_batches` (`SCR_{BATCH}_{SEQ}`): First-round screening committee category audits.
  6. `tied_nominations` (`TIE_{CEREMONY}_{CAT}`): Documented ballot ties producing expanded nominee rosters.
  7. `nomination_audit_logs` (`AUD_{LOG}_{SEQ}`): Accounting firm ballot verification and certification records.
  8. `genre_classifications` (`GCL_{SLUG}`): Multi-genre taxonomy tagging applied to nominated works.
  9. `first_time_nominees` (`FTN_{CRT}_{CEREMONY}`): Maiden career nomination tracking entries.
  10. `multi_nomination_packages` (`MNP_{CEREMONY}_{WRK}`): Cross-category nomination portfolio groupings for single works.

### 3.4. Database 4: `grammy_winners_db` (Lead: Member 4)
- **Domain Scope**: Confirmed award winners, historical records, physical trophy fulfillment, and acceptance speeches.
- **Invariants**:
  - Every winner record MUST map to a valid `nomination_id` established in `grammy_nominations_db`.
  - Maintains verified celebration records, trophy tracking, and historical statistical sweeps.
- **Collections**:
  1. `winner_records` (`WIN_{NOMINATION_ID}`): Official verified winner records.
  2. `big_four_sweeps` (`SWP_{CEREMONY}_{CRT}`): Historical general field sweeps (Christopher Cross, Billie Eilish).
  3. `record_breakers` (`RBRK_{SLUG}`): All-time historical GRAMMY record benchmarks (e.g., Beyoncé 32 wins).
  4. `acceptance_speeches` (`SPCH_{WIN_ID}`): Acceptance speech transcripts, runtimes, and dedication topics.
  5. `trophy_tracking` (`TRP_{SERIAL_NO}`): Physical statuette manufacturing, metallurgical specs, engraving, shipment.
  6. `consecutive_winners` (`CSW_{CAT}_{CRT}`): Multi-year consecutive victory streaks.
  7. `hall_of_fame_inductions` (`HOF_{SLUG}`): Historic recordings inducted into the GRAMMY Hall of Fame.
  8. `posthumous_awards` (`PST_{WIN_ID}`): Posthumous honors accepted by surviving family or estate trustees.
  9. `historic_win_benchmarks` (`BMK_{SLUG}`): Longitudinal genre and category historical victory averages.
  10. `winner_press_releases` (`WPR_{CEREMONY}_{SEQ}`): Official Academy press bulletins issued upon victory announcement.

### 3.5. Database 5: `grammy_creators_db` (Lead: Member 5)
- **Domain Scope**: Master entity directory of artists, technical practitioners, ensembles, and commercial record labels.
- **Invariants**:
  - Pure entity registry. Does NOT store award nominations or trophy ownership directly.
  - Serves as the single source of truth for creator identities across the entire system.
- **Collections**:
  1. `artists` (`CRT_ART_{SLUG}`): Performing solo vocalists and instrumentalists.
  2. `producers` (`CRT_PRD_{SLUG}`): Record producers and vocal producers.
  3. `audio_engineers` (`CRT_ENG_{SLUG}`): Tracking, mixing, mastering, and immersive spatial audio engineers.
  4. `songwriters_composers` (`CRT_SNG_{SLUG}`): Composers and lyricists with PRO registration data.
  5. `arrangers_conductors` (`CRT_ARR_{SLUG}`): Orchestrators, arrangers, and conductors.
  6. `record_labels` (`LBL_{SLUG}`): Commercial record companies, imprints, and distribution groups.
  7. `musical_groups` (`GRP_{SLUG}`): Performing bands, duos, orchestras, and vocal groups.
  8. `group_memberships` (`MBR_{GRP}_{CRT}`): Relational membership tenures linking artists to groups.
  9. `creator_collaborations` (`COL_{CRT1}_{CRT2}`): Recurrent artistic and production partnerships.
  10. `creator_discographies` (`DISC_{CRT}_{SLUG}`): Master release catalogs associated with creators.

---

## 4. Universal Identifier Scheme & Cross-Database Foreign References

Cross-database referential integrity is preserved using deterministic, standardized keys:

| Key Category | Regex Format Pattern | Canonical Example | Primary Definition Database | Referenced Across Databases |
| :--- | :--- | :--- | :--- | :--- |
| **Ceremony ID** | `^CEREMONY_[0-9]{3}$` | `CEREMONY_065` | `grammy_history_db` | `grammy_categories_db`, `grammy_nominations_db`, `grammy_winners_db` |
| **Category ID** | `^CAT_[A-Z0-9_]+$` | `CAT_ALBUM_OF_THE_YEAR` | `grammy_categories_db` | `grammy_nominations_db`, `grammy_winners_db` |
| **Field ID** | `^FLD_[A-Z0-9_]+$` | `FLD_GENERAL_FIELD` | `grammy_categories_db` | `grammy_categories_db`, `grammy_nominations_db` |
| **Nomination ID**| `^NOM_[0-9]{3}_[A-Z0-9_]+_[0-9]{2}$` | `NOM_065_AOTY_01` | `grammy_nominations_db` | `grammy_winners_db` |
| **Winner ID** | `^WIN_NOM_[0-9]{3}_[A-Z0-9_]+_[0-9]{2}$` | `WIN_NOM_065_AOTY_01` | `grammy_winners_db` | `grammy_winners_db` (Speeches, Trophies) |
| **Work ID** | `^WRK_[A-Z0-9_]+$` | `WRK_RENAISSANCE_2022`| `grammy_nominations_db` | `grammy_winners_db`, `grammy_creators_db` |
| **Creator ID** | `^CRT_[A-Z0-9_]+$` | `CRT_BEYONCE_KNOWLES` | `grammy_creators_db` | `grammy_history_db`, `grammy_nominations_db`, `grammy_winners_db` |
| **Label ID** | `^LBL_[A-Z0-9_]+$` | `LBL_COLUMBIA_RECORDS`| `grammy_creators_db` | `grammy_nominations_db` |
| **Venue ID** | `^VEN_[A-Z0-9_]+$` | `VEN_CRYPTO_COM_ARENA`| `grammy_history_db` | `grammy_history_db` (Ceremonies) |

---

## 5. Cross-Boundary Data Flow & Inter-Database Query Topology

Because MongoDB Atlas does not support zero-cost foreign keys across discrete database boundaries, data federation follows three disciplined access patterns:

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 Client Application                     │
                  │             (Python / Aggregation Engine)              │
                  └──────┬────────────────────┬────────────────────┬───────┘
                         │                    │                    │
          1. Direct Read │     2. Application │     3. Cross-DB    │
             Query       │        Level Join  │        Lookup      │
                         ▼                    ▼                    ▼
                ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
                │grammy_history_db│  │grammy_nominations│  │  grammy_winners │
                │                 │  │       _db       │  │       _db       │
                └─────────────────┘  └────────┬────────┘  └────────┬────────┘
                                              │                    │
                                              │ Resolves Creator ID│
                                              ▼                    ▼
                                     ┌──────────────────────────────────────┐
                                     │         grammy_creators_db           │
                                     │        (Master Entity Hub)           │
                                     └──────────────────────────────────────┘
```

1. **Application-Level Joins (Client-Side Composition)**: For cross-database workflows (e.g., retrieving the artist profile for a specific winner record), the application executes targeted primary key lookups using indexed fields (`crt_id`, `nomination_id`).
2. **Denormalized Projection (Strategic Inlining)**: High-frequency display fields (such as `artist_name` and `category_name`) are strategically denormalized as immutable snapshots inside nomination and winner documents, completely avoiding cross-database lookups during routine report rendering.
3. **ETL Cross-Validation Pipelines**: Automated validation test suites connect to all five databases concurrently, extracting key sets and asserting 100% referential integrity across the system graph.
