# Relational Keys, Constraints & Relationship Mappings

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 7 — Relational Model  
> **Document**: Comprehensive Key Classifications, Referential Integrity Matrix, Referential Actions, and Advanced EER-to-Relational Structural Mappings  
> **Status**: Completed  
> **Theoretical Framework**: Elmasri & Navathe (*Fundamentals of Database Systems*, 7th Edition, Chapters 5, 8 & 9)  
> **Related Artifacts**:  
> - Relational Schema Catalog: [`relational-model/schema.md`](./schema.md)  
> - Relational Algebra Queries: [`relational-model/relational-algebra-examples.md`](./relational-algebra-examples.md)  
> - Conceptual EER Model: [`docs/eer-design.md`](../docs/eer-design.md)  

---

## 1. Formal Theoretical Definitions of Relational Keys

In relational database theory (Codd 1970; Elmasri & Navathe 2016):

1. **Superkey ($SK$)**:
   A set of attributes $SK \subseteq R$ such that no two distinct tuples in any valid relation state $r(R)$ have the same values for $SK$:
   $$\forall t_1, t_2 \in r(R), \quad t_1 \neq t_2 \implies t_1[SK] \neq t_2[SK]$$

2. **Candidate Key ($CK$)**:
   A minimal superkey. A superkey $CK$ is a candidate key if no proper subset of $CK$ is also a superkey:
   $$\forall A \in CK, \quad (CK - \{A\}) \text{ is not a superkey of } R$$

3. **Primary Key ($PK$)**:
   The candidate key designated by the database designer as the principal identifier for tuples within the relation:
   $$\forall t \in r(R), \quad t[PK] \neq \text{NULL}$$

4. **Alternate Key ($AK$)**:
   Any candidate key of relation $R$ that has not been chosen as the primary key. In SQL implementations, alternate keys are enforced using `UNIQUE NOT NULL` constraints.

5. **Foreign Key ($FK$)**:
   A set of attributes $FK \subseteq R_1$ that references the candidate key (typically primary key) $PK \subseteq R_2$, enforcing referential integrity:
   $$\forall t_1 \in r(R_1), \quad t_1[FK] = \text{NULL} \quad \lor \quad \exists t_2 \in r(R_2) \text{ such that } t_1[FK] = t_2[PK]$$

---

## 2. Complete Primary and Candidate Key Registry

The following table provides the exhaustive key catalog for all 50 relations across the five domain databases:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              PRIMARY & CANDIDATE KEY SPECIFICATION MATRIX                                   │
├─────────────────────────┬────────────────────────────────┬──────────────────────┬───────────────────────────┤
│ Domain Database         │ Relation Name                  │ Primary Key (PK)     │ Candidate / Alternate Keys│
├─────────────────────────┼────────────────────────────────┼──────────────────────┼───────────────────────────┤
│ grammy_history_db       │ venues                         │ venue_id             │ venue_name                │
│                         │ ceremonies                     │ ceremony_id          │ edition_number            │
│                         │ telecast_broadcasters          │ broadcast_id         │ (ceremony_id, network)    │
│                         │ viewership_ratings             │ rating_id            │ ceremony_id               │
│                         │ ceremony_hosts                 │ host_record_id       │ (ceremony_id, host_name)  │
│                         │ historic_milestones            │ milestone_id         │ (ceremony_id, title)      │
│                         │ academy_leadership             │ leadership_id        │ (officer_name, role, year)│
│                         │ timeline_historical_eras       │ era_id               │ era_name                  │
│                         │ press_media_accreditations     │ accreditation_id     │ (ceremony_id, media_org)  │
│                         │ lifetime_achievement_honors    │ honor_id             │ (honoree_name, year)      │
├─────────────────────────┼────────────────────────────────┼──────────────────────┼───────────────────────────┤
│ grammy_categories_db    │ award_fields                   │ field_id             │ field_name                │
│                         │ award_categories               │ category_id          │ official_category_name    │
│                         │ category_lineage               │ lineage_id           │ (category_id, edition)    │
│                         │ eligibility_rules              │ rule_id              │ (category_id, edition)    │
│                         │ voting_procedures              │ procedure_id         │ (category_id, round_no)   │
│                         │ discontinued_categories        │ discontinued_id      │ category_name             │
│                         │ category_quotas_limits         │ quota_id             │ (category_id, edition)    │
│                         │ special_merit_categories       │ special_merit_id     │ award_title               │
│                         │ craft_credit_definitions       │ craft_def_id         │ (category_id, craft_role) │
│                         │ merged_split_history           │ event_id             │ (primary_cat_id, year)    │
├─────────────────────────┼────────────────────────────────┼──────────────────────┼───────────────────────────┤
│ grammy_creators_db      │ creators                       │ creator_id           │ musicbrainz_gid           │
│                         │ artists                        │ creator_id           │ stage_name                │
│                         │ producers                      │ producer_id          │ creator_id                │
│                         │ audio_engineers                │ engineer_id          │ creator_id                │
│                         │ songwriters_composers          │ songwriter_id        │ (creator_id, ipi_cae_id)  │
│                         │ arrangers_conductors           │ arranger_id          │ creator_id                │
│                         │ record_labels                  │ label_id             │ label_corporate_name      │
│                         │ musical_groups                 │ group_id             │ group_name, mb_group_gid  │
│                         │ group_memberships              │ membership_id        │ (group_id, creator_id)    │
│                         │ creator_collaborations         │ collaboration_id     │ (creator1, creator2, year)│
├─────────────────────────┼────────────────────────────────┼──────────────────────┼───────────────────────────┤
│ grammy_nominations_db   │ nominated_works                │ work_id              │ isrc_code, upc_barcode    │
│                         │ nomination_entries             │ nomination_id        │ (ceremony_id, cat, work)  │
│                         │ nomination_credits             │ credit_id            │ (nom_id, creator, role)   │
│                         │ submission_batches             │ batch_id             │ (ceremony_id, batch_code) │
│                         │ genre_classifications          │ classification_id    │ (work_id, submitted_field)│
│                         │ first_time_nominees            │ first_nom_id         │ nomination_id             │
│                         │ tied_nominations               │ tie_id               │ (ceremony_id, category_id)│
│                         │ multi_nomination_packages      │ package_id           │ (ceremony_id, creator_id) │
│                         │ voter_screening_batches        │ screening_batch_id   │ (ceremony_id, field_id)   │
│                         │ nomination_audit_logs          │ audit_id             │ nomination_id             │
├─────────────────────────┼────────────────────────────────┼──────────────────────┼───────────────────────────┤
│ grammy_winners_db       │ winner_records                 │ winner_record_id     │ nomination_id             │
│                         │ big_four_sweeps                │ sweep_id             │ (ceremony_id, creator_id) │
│                         │ record_breakers                │ record_id            │ (metric_name, year)       │
│                         │ acceptance_speeches            │ speech_id            │ winner_record_id          │
│                         │ trophy_tracking                │ trophy_id            │ statuette_serial_number   │
│                         │ consecutive_winners            │ streak_id            │ (creator_id, category_id) │
│                         │ posthumous_awards              │ posthumous_id        │ winner_record_id          │
│                         │ historic_win_benchmarks        │ benchmark_id         │ benchmark_title           │
│                         │ hall_of_fame_inductions        │ induction_id         │ (work_title, year)        │
│                         │ winner_press_releases          │ release_id           │ (ceremony_id, headline)   │
└─────────────────────────┴────────────────────────────────┴──────────────────────┴───────────────────────────┘
```

---

## 3. Comprehensive Foreign Key Matrix & Referential Actions

Referential integrity guarantees that relationships between relations remain valid. Each foreign key defines explicit referential actions for update and deletion:
- `ON DELETE RESTRICT / NO ACTION`: Prevents deletion of the referenced tuple if child records exist (used for mission-critical audit trails, ceremonies, and categories).
- `ON DELETE CASCADE`: Automatically cascades deletion of parent records to child dependent records (used for weak entities and dependent associative records).
- `ON DELETE SET NULL`: Sets foreign key columns to NULL when parent record is deleted (used for optional references, such as historical predecessor categories).
- `ON UPDATE CASCADE`: Cascades any modifications to primary key values across all referencing foreign keys.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            FOREIGN KEY & REFERENTIAL ACTION MATRIX                                              │
├──────────────────────────────┬────────────────────────────┬─────────────────────────────┬───────────────────────────┬───────────┤
│ Source Relation              │ Foreign Key Column(s)      │ Referenced Relation         │ Target Column             │ On Delete │
├──────────────────────────────┼────────────────────────────┼─────────────────────────────┼───────────────────────────┼───────────┤
│ ceremonies                   │ venue_id                   │ venues                      │ venue_id                  │ RESTRICT  │
│ telecast_broadcasters        │ ceremony_id                │ ceremonies                  │ ceremony_id               │ CASCADE   │
│ viewership_ratings           │ ceremony_id                │ ceremonies                  │ ceremony_id               │ CASCADE   │
│ ceremony_hosts               │ ceremony_id                │ ceremonies                  │ ceremony_id               │ CASCADE   │
│ ceremony_hosts               │ creator_id                 │ creators (DB5)              │ creator_id                │ SET NULL  │
│ historic_milestones          │ ceremony_id                │ ceremonies                  │ ceremony_id               │ CASCADE   │
│ award_categories             │ field_id                   │ award_fields                │ field_id                  │ RESTRICT  │
│ category_lineage             │ category_id                │ award_categories            │ category_id               │ CASCADE   │
│ eligibility_rules            │ category_id                │ award_categories            │ category_id               │ CASCADE   │
│ voting_procedures            │ category_id                │ award_categories            │ category_id               │ CASCADE   │
│ category_quotas_limits       │ category_id                │ award_categories            │ category_id               │ CASCADE   │
│ craft_credit_definitions     │ category_id                │ award_categories            │ category_id               │ CASCADE   │
│ group_memberships            │ group_id                   │ musical_groups              │ group_id                  │ CASCADE   │
│ group_memberships            │ creator_id                 │ creators                    │ creator_id                │ CASCADE   │
│ producers                    │ creator_id                 │ creators                    │ creator_id                │ CASCADE   │
│ audio_engineers              │ creator_id                 │ creators                    │ creator_id                │ CASCADE   │
│ songwriters_composers        │ creator_id                 │ creators                    │ creator_id                │ CASCADE   │
│ arrangers_conductors         │ creator_id                 │ creators                    │ creator_id                │ CASCADE   │
│ nominated_works              │ primary_label_id           │ record_labels (DB5)         │ label_id                  │ RESTRICT  │
│ nomination_entries           │ ceremony_id                │ ceremonies (DB1)            │ ceremony_id               │ RESTRICT  │
│ nomination_entries           │ category_id                │ award_categories (DB2)      │ category_id               │ RESTRICT  │
│ nomination_entries           │ work_id                    │ nominated_works             │ work_id                   │ RESTRICT  │
│ nomination_entries           │ primary_artist_id          │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ nomination_credits           │ nomination_id              │ nomination_entries          │ nomination_id             │ CASCADE   │
│ nomination_credits           │ creator_id                 │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ submission_batches           │ ceremony_id                │ ceremonies (DB1)            │ ceremony_id               │ RESTRICT  │
│ submission_batches           │ submitting_label_id        │ record_labels (DB5)         │ label_id                  │ RESTRICT  │
│ genre_classifications        │ work_id                    │ nominated_works             │ work_id                   │ CASCADE   │
│ genre_classifications        │ submitted_field_id         │ award_fields (DB2)          │ field_id                  │ RESTRICT  │
│ genre_classifications        │ assigned_field_id          │ award_fields (DB2)          │ field_id                  │ RESTRICT  │
│ first_time_nominees          │ nomination_id              │ nomination_entries          │ nomination_id             │ CASCADE   │
│ first_time_nominees          │ creator_id                 │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ first_time_nominees          │ breakout_work_id           │ nominated_works             │ work_id                   │ RESTRICT  │
│ tied_nominations             │ ceremony_id                │ ceremonies (DB1)            │ ceremony_id               │ RESTRICT  │
│ tied_nominations             │ category_id                │ award_categories (DB2)      │ category_id               │ RESTRICT  │
│ multi_nomination_packages    │ ceremony_id                │ ceremonies (DB1)            │ ceremony_id               │ RESTRICT  │
│ multi_nomination_packages    │ creator_id                 │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ voter_screening_batches      │ ceremony_id                │ ceremonies (DB1)            │ ceremony_id               │ RESTRICT  │
│ voter_screening_batches      │ field_id                   │ award_fields (DB2)          │ field_id                  │ RESTRICT  │
│ voter_screening_batches      │ panel_chair_creator_id     │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ nomination_audit_logs        │ nomination_id              │ nomination_entries          │ nomination_id             │ RESTRICT  │
│ winner_records               │ nomination_id              │ nomination_entries (DB3)    │ nomination_id             │ RESTRICT  │
│ winner_records               │ ceremony_id                │ ceremonies (DB1)            │ ceremony_id               │ RESTRICT  │
│ winner_records               │ category_id                │ award_categories (DB2)      │ category_id               │ RESTRICT  │
│ winner_records               │ winning_work_id            │ nominated_works (DB3)       │ work_id                   │ RESTRICT  │
│ winner_records               │ primary_artist_id          │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ big_four_sweeps              │ ceremony_id                │ ceremonies (DB1)            │ ceremony_id               │ RESTRICT  │
│ big_four_sweeps              │ creator_id                 │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ big_four_sweeps              │ aoty_nomination_id         │ nomination_entries (DB3)    │ nomination_id             │ RESTRICT  │
│ big_four_sweeps              │ roty_nomination_id         │ nomination_entries (DB3)    │ nomination_id             │ RESTRICT  │
│ big_four_sweeps              │ soty_nomination_id         │ nomination_entries (DB3)    │ nomination_id             │ RESTRICT  │
│ big_four_sweeps              │ bna_nomination_id          │ nomination_entries (DB3)    │ nomination_id             │ RESTRICT  │
│ record_breakers              │ winner_record_id           │ winner_records              │ winner_record_id          │ SET NULL  │
│ record_breakers              │ creator_id                 │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ acceptance_speeches          │ winner_record_id           │ winner_records              │ winner_record_id          │ CASCADE   │
│ acceptance_speeches          │ primary_speaker_creator_id │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ trophy_tracking              │ winner_record_id           │ winner_records              │ winner_record_id          │ RESTRICT  │
│ trophy_tracking              │ recipient_creator_id       │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ consecutive_winners          │ creator_id                 │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ consecutive_winners          │ category_id                │ award_categories (DB2)      │ category_id               │ RESTRICT  │
│ posthumous_awards            │ winner_record_id           │ winner_records              │ winner_record_id          │ CASCADE   │
│ posthumous_awards            │ deceased_creator_id        │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ historic_win_benchmarks      │ pioneering_creator_id      │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ historic_win_benchmarks      │ most_recent_qualifier_id   │ creators (DB5)              │ creator_id                │ RESTRICT  │
│ winner_press_releases        │ ceremony_id                │ ceremonies (DB1)            │ ceremony_id               │ CASCADE   │
└──────────────────────────────┴────────────────────────────┴─────────────────────────────┴───────────────────────────┴───────────┘
```

---

## 4. Mapping Advanced EER Constructs to Relations

### 4.1. Mapping Overlapping Specialization: `CREATOR` Hierarchy
In Phase 6, the `CREATOR` entity was defined with an **Overlapping ($o$), Total Specialization** constraint across five subclasses:
$$\text{CREATOR} = \text{ARTIST} \cup \text{PRODUCER} \cup \text{AUDIO\_ENGINEER} \cup \text{SONGWRITER} \cup \text{ARRANGER}$$
where a single creator may concurrently exist in multiple roles.

#### Relational Implementation (Option 8B: Multiple Relations with Superclass Key):
1. **Superclass Relation**:
   `creators` holds all common attributes (`creator_id`, `full_legal_name`, `country_of_citizenship`, `active_career_start_year`, `musicbrainz_gid`).
2. **Subclass Relations**:
   Each subclass is mapped into a separate relation containing only subclass-specific attributes, using `creator_id` as both primary key and foreign key referencing `creators(creator_id)`:
   - `artists(creator_id, stage_name, primary_musical_genre, ...)`
   - `producers(producer_id, creator_id, primary_production_genre, studio_location, ...)`
   - `audio_engineers(engineer_id, creator_id, specialization, facility, atmos_flag, ...)`
   - `songwriters_composers(songwriter_id, creator_id, pro_affiliation, ipi_id, ...)`
   - `arrangers_conductors(arranger_id, creator_id, discipline, resident_orchestra, ...)`
3. **Academic Justification**:
   - Avoids excessive null values that would occur if all attributes were merged into a single table.
   - Allows a creator (such as Paul McCartney or Quincy Jones) to exist in all five subclass relations simultaneously without violating functional dependencies or 3NF.

### 4.2. Mapping Disjoint Specialization: `WORK` Hierarchy
The `WORK` entity was modeled with a **Disjoint ($d$), Total Specialization** into `TRACK_RECORDING`, `ALBUM_RECORDING`, and `MUSIC_VIDEO`.

#### Relational Implementation:
- Implemented within `nominated_works` using a **Type Attribute Discriminator** (`work_type` $\in \{\text{'Album'}, \text{'Single/Track'}, \text{'Video'}, \text{'Box Set'}\}$).
- Specific media attributes (`duration_total_seconds`, `track_count`, `isrc_code`, `upc_barcode`) are governed by conditional domain check constraints, preserving single-table identity across heterogeneous ballot categories while eliminating table joins for common nomination lookups.

### 4.3. Mapping Conceptual Aggregation: `NOMINATION_CREDIT`
In EER theory, conceptual aggregation models an entire relationship between entities as an aggregated entity that can subsequently participate in higher-order relationships:
$$\text{NOMINATION\_CREDIT} = \text{AGGREGATE}(\text{CREATOR}, \text{WORK}, \text{AWARD\_CATEGORY})$$

#### Relational Implementation:
1. `nomination_credits` is established as an independent first-class relation:
   - Primary Key: `credit_id` (e.g., `CRD_065_AOTY_BEYONCE_PROD`)
   - Foreign Keys: `nomination_id REFERENCES nomination_entries` and `creator_id REFERENCES creators`
   - Attributes: `credit_role`, `contribution_percentage`, `work_contribution_summary`, `is_lead_performer`
2. Downstream Relationships of the Aggregated Entity:
   - **Auditing**: `nomination_audit_logs` references `nomination_entries` and indirectly verifies credits.
   - **Trophy Quotas**: `trophy_tracking` links directly to elevated winners and verifies whether `nomination_credits.contribution_percentage` meets the statutory threshold ($\ge 33\%$ for Album of the Year) to issue physical golden statuettes.

### 4.4. Mapping Categories / Union Types: `AWARD_RECIPIENT`
In EER modeling, a category or union type represents a collection of objects that is the union of different entity types with distinct primary keys:
$$\text{AWARD\_RECIPIENT} \subseteq (\text{ARTIST} \cup \text{MUSICAL\_GROUP})$$

#### Relational Implementation:
1. `winner_records` maps the recipient through `primary_artist_id` referencing `creators(creator_id)`.
2. When the recipient is an ensemble, `creators.is_group_ensemble_flag` is set to `TRUE`, and a cross-reference is maintained to `musical_groups.group_id` via `group_memberships`.
3. In presentation and analytical queries, a unified relational view `v_award_recipients` executes a union query across `artists` and `musical_groups` to project a homogeneous recipient identity.

---

## 5. Logical vs. Physical Referential Boundaries

Because this Advanced DBMS architecture distributes data across **five physically separate MongoDB databases** in Phase 8, the relational model defines two tiers of referential integrity:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                           CROSS-DATABASE INTEGRITY ARCHITECTURE                             │
├──────────────────────────┬─────────────────────────────┬────────────────────────────────────┤
│ Tier                     │ Scope                       │ Enforcement Mechanism              │
├──────────────────────────┼─────────────────────────────┼────────────────────────────────────┤
│ Intra-Database Integrity │ Single Database boundary    │ DBMS Primary / Foreign Key DDL     │
│ (Physical Relational)    │ (e.g., within DB1, DB2, etc)│ Strict ON DELETE / ON UPDATE rules │
├──────────────────────────┼─────────────────────────────┼────────────────────────────────────┤
│ Inter-Database Integrity │ Cross-Database boundaries   │ Logical foreign key UUID matching  │
│ (Distributed Polyglot)   │ (e.g., DB3 -> DB1, DB5)     │ Pre-commit validation scripts      │
│                          │                             │ Automated CI/CD pytest test suite  │
└──────────────────────────┴─────────────────────────────┴────────────────────────────────────┘
```

1. **Intra-Database Relationships**:
   - `ceremonies` $\leftrightarrow$ `venues`, `viewership_ratings`, `telecast_broadcasters` (All inside `grammy_history_db`).
   - `award_fields` $\leftrightarrow$ `award_categories` $\leftrightarrow$ `eligibility_rules` (All inside `grammy_categories_db`).
   - Fully enforced by standard SQL engine foreign key constraints.

2. **Inter-Database Logical Bridges**:
   - `nomination_entries.ceremony_id` $\rightarrow$ references `grammy_history_db.ceremonies(ceremony_id)`.
   - `nomination_entries.category_id` $\rightarrow$ references `grammy_categories_db.award_categories(category_id)`.
   - `nomination_entries.primary_artist_id` $\rightarrow$ references `grammy_creators_db.creators(creator_id)`.
   - `winner_records.nomination_id` $\rightarrow$ references `grammy_nominations_db.nomination_entries(nomination_id)`.
   - Enforced by automated Python validation pipeline (`scripts/validation/validate_schemas.py`) and verified by existing pytest suite (`tests/test_dataset_validation.py::test_cross_database_referential_integrity`).
