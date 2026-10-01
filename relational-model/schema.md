# Relational Schema Specification

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 7 — Relational Model  
> **Document**: Comprehensive Relational Schema Definition, Attribute Dictionaries, Domain Constraints, and Normal Form Classification  
> **Status**: Completed  
> **Theoretical Framework**: Elmasri & Navathe (*Fundamentals of Database Systems*, 7th Edition, Chapters 5, 8 & 9) / Codd's Relational Model (1970)  
> **Related Artifacts**:  
> - Keys & Referential Integrity: [`relational-model/keys-and-relationships.md`](./keys-and-relationships.md)  
> - Relational Algebra Implementations: [`relational-model/relational-algebra-examples.md`](./relational-algebra-examples.md)  
> - Reference SQL DDL: [`schemas/relational_ddl/relational_reference_schema.sql`](../schemas/relational_ddl/relational_reference_schema.sql)  
> - Conceptual EER Model: [`docs/eer-design.md`](../docs/eer-design.md)  

---

## 1. Executive Summary & Relational Model Foundations

The relational model represents the logical database design derived directly from the approved **Phase 6 Conceptual Enhanced Entity-Relationship (EER)** model. It maps all 50 conceptual entities, specializations, aggregations, and union types across the five core operational domains into a formal, normalized set of relations.

### 1.1. Formal Relational Model Definitions
According to E.F. Codd (1970) and Elmasri & Navathe (2016):
- **Relation Schema $R(A_1, A_2, \dots, A_n)$**: A named set of attributes where each attribute $A_i$ is defined over an underlying domain $dom(A_i)$.
- **Relation State $r(R)$**: A mathematical relation of degree $n$ defined on domains $dom(A_1), dom(A_2), \dots, dom(A_n)$, representing a subset of the Cartesian product:
  $$r(R) \subseteq dom(A_1) \times dom(A_2) \times \dots \times dom(A_n)$$
- **Tuple $t$**: An ordered $n$-tuple of values $t = \langle v_1, v_2, \dots, v_n \rangle$ where each $v_i \in dom(A_i)$ or $v_i$ is $\text{NULL}$ (when permitted).
- **Entity Integrity Constraint**: If attribute $PK$ is the primary key of relation $R$, then for no tuple $t \in r(R)$ may $t[PK]$ contain a null value:
  $$\forall t \in r(R), \quad t[PK] \neq \text{NULL}$$
- **Referential Integrity Constraint**: If a relation schema $R_1$ contains a foreign key $FK$ that references the primary key $PK$ of relation schema $R_2$, then for every tuple $t_1 \in r(R_1)$, either $t_1[FK] = \text{NULL}$ or there exists a tuple $t_2 \in r(R_2)$ such that $t_1[FK] = t_2[PK]$.

---

## 2. EER-to-Relational Mapping Methodology

The conversion from the Conceptual EER Model into the normalized relational model follows the canonical 7-step mapping algorithm of Elmasri & Navathe (Chapter 9), extended with Steps 8 and 9 for advanced constructs:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           EER-TO-RELATIONAL TRANSFORMATION PIPELINE                             │
├──────┬─────────────────────────────┬────────────────────────────────────────────────────────────┤
│ Step │ EER Construct               │ Relational Transformation Mechanism                        │
├──────┼─────────────────────────────┼────────────────────────────────────────────────────────────┤
│ 1    │ Regular Strong Entities     │ Relation with all simple attributes; PK mapped directly.   │
│ 2    │ Weak Entities               │ Relation with owner PK + partial key as composite PK.      │
│ 3    │ Binary 1:1 Relationships    │ Foreign key approach with UNIQUE constraint on FK side.    │
│ 4    │ Binary 1:N Relationships    │ Foreign key posted to the relation on the N-side.          │
│ 5    │ Binary M:N Relationships    │ Associative relation with composite PK (FK1 + FK2).        │
│ 6    │ Multivalued Attributes      │ Decomposed into dedicated child tables with composite PK.  │
│ 7    │ Specialization Hierarchies  │                                                            │
│      │ - Overlapping (o) CREATOR   │ Multiple tables sharing superclass PK (artists, etc.).     │
│      │ - Disjoint (d) WORK         │ Partitioned tables with shared PK or media discriminator.  │
│ 8    │ Conceptual Aggregation      │ Elevated to first-class relation (nomination_credits).     │
│ 9    │ Union Types (Categories)    │ Unified relation with surrogate key & polymorphic type.    │
└──────┴─────────────────────────────┴────────────────────────────────────────────────────────────┘
```

---

## 3. Global Relation Catalog Across All Five Databases

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                         GLOBAL RELATIONAL SCHEMA SUMMARY (50 TABLES)                          │
├──────────────────────┬────────────────────────────────┬───────────────────────────────────────┤
│ Domain Database      │ Relation Name                  │ Primary Key (PK)                      │
├──────────────────────┼────────────────────────────────┼───────────────────────────────────────┤
│ grammy_history_db    │ venues                         │ venue_id                              │
│ (History & Ops)      │ ceremonies                     │ ceremony_id                           │
│                      │ telecast_broadcasters          │ broadcast_id                          │
│                      │ viewership_ratings             │ rating_id                             │
│                      │ ceremony_hosts                 │ host_record_id                        │
│                      │ historic_milestones            │ milestone_id                          │
│                      │ academy_leadership             │ leadership_id                         │
│                      │ timeline_historical_eras       │ era_id                                │
│                      │ press_media_accreditations     │ accreditation_id                      │
│                      │ lifetime_achievement_honors    │ honor_id                              │
├──────────────────────┼────────────────────────────────┼───────────────────────────────────────┤
│ grammy_categories_db │ award_fields                   │ field_id                              │
│ (Categories & Rules) │ award_categories               │ category_id                           │
│                      │ category_lineage               │ lineage_id                            │
│                      │ eligibility_rules              │ rule_id                               │
│                      │ voting_procedures              │ procedure_id                          │
│                      │ discontinued_categories        │ discontinued_id                       │
│                      │ category_quotas_limits         │ quota_id                              │
│                      │ special_merit_categories       │ special_merit_id                      │
│                      │ craft_credit_definitions       │ craft_def_id                          │
│                      │ merged_split_history           │ event_id                              │
├──────────────────────┼────────────────────────────────┼───────────────────────────────────────┤
│ grammy_creators_db   │ creators                       │ creator_id                            │
│ (Creators & Labels)  │ artists                        │ creator_id                            │
│                      │ producers                      │ producer_id (or creator_id)           │
│                      │ audio_engineers                │ engineer_id (or creator_id)           │
│                      │ songwriters_composers          │ songwriter_id (or creator_id)         │
│                      │ arrangers_conductors           │ arranger_id (or creator_id)           │
│                      │ record_labels                  │ label_id                              │
│                      │ musical_groups                 │ group_id                              │
│                      │ group_memberships              │ membership_id                         │
│                      │ creator_collaborations         │ collaboration_id                      │
├──────────────────────┼────────────────────────────────┼───────────────────────────────────────┤
│ grammy_nominations_db│ nominated_works                │ work_id                               │
│ (Nominations/Ballots)│ nomination_entries             │ nomination_id                         │
│                      │ nomination_credits             │ credit_id                             │
│                      │ submission_batches             │ batch_id                              │
│                      │ genre_classifications          │ classification_id                     │
│                      │ first_time_nominees            │ first_nom_id                          │
│                      │ tied_nominations               │ tie_id                                │
│                      │ multi_nomination_packages      │ package_id                            │
│                      │ voter_screening_batches        │ screening_batch_id                    │
│                      │ nomination_audit_logs          │ audit_id                              │
├──────────────────────┼────────────────────────────────┼───────────────────────────────────────┤
│ grammy_winners_db    │ winner_records                 │ winner_record_id                      │
│ (Winners & Trophies) │ big_four_sweeps                │ sweep_id                              │
│                      │ record_breakers                │ record_id                             │
│                      │ acceptance_speeches            │ speech_id                             │
│                      │ trophy_tracking                │ trophy_id                             │
│                      │ consecutive_winners            │ streak_id                             │
│                      │ posthumous_awards              │ posthumous_id                         │
│                      │ historic_win_benchmarks        │ benchmark_id                          │
│                      │ hall_of_fame_inductions        │ induction_id                          │
│                      │ winner_press_releases          │ release_id                            │
└──────────────────────┴────────────────────────────────┴───────────────────────────────────────┘
```

---

## 4. Domain 1: History & Operations Domain (`grammy_history_db`)

### 4.1. Relation: `venues`
- **Formal Notation**: $\text{venues}(\underline{\text{venue\_id}}, \text{venue\_name}, \text{venue\_type}, \text{street\_address}, \text{city}, \text{state}, \text{postal\_code}, \text{max\_seating\_capacity}, \text{first\_hosted\_year}, \text{total\_ceremonies\_hosted})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `venue_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Unique alphanumeric venue code (e.g., `VEN_CRYPTO_COM_ARENA`) |
| `venue_name` | `VARCHAR(128)` | NOT NULL | None | Official commercial facility name |
| `venue_type` | `VARCHAR(64)` | NOT NULL | Enum: Arena, Theater, Auditorium, Hotel Ballroom | Architecture classification of facility |
| `street_address` | `VARCHAR(255)` | NULL | None | Physical street address |
| `city` | `VARCHAR(64)` | NOT NULL | None | Host municipality |
| `state` | `VARCHAR(32)` | NOT NULL | None | State, province, or federal district |
| `postal_code` | `VARCHAR(16)` | NULL | None | Postal routing zip code |
| `max_seating_capacity` | `INT` | NULL | `CHECK (max_seating_capacity > 0)` | Maximum audience seating capacity |
| `first_hosted_year` | `INT` | NULL | `CHECK (first_hosted_year >= 1958)` | Earliest year the venue staged the telecast |
| `total_ceremonies_hosted` | `INT` | NOT NULL | `DEFAULT 0, CHECK (>= 0)` | Cumulative telecast count held at venue |

### 4.2. Relation: `ceremonies`
- **Formal Notation**: $\text{ceremonies}(\underline{\text{ceremony\_id}}, \text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{eligibility\_period\_start}, \text{eligibility\_period\_end}, \text{host\_city}, \text{venue\_id}, \text{primary\_network}, \text{total\_awards\_presented}, \text{created\_at})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `ceremony_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Canonical ceremony identifier (e.g., `CEREMONY_065`) |
| `edition_number` | `INT` | NOT NULL | **UNIQUE**, `CHECK (> 0)` | Sequential edition number (e.g., 65 for 65th Annual) |
| `ceremony_date` | `DATE` | NOT NULL | ISO-8601 Date | Telecast live event date |
| `broadcast_year` | `INT` | NOT NULL | `CHECK (>= 1959)` | Calendar year of telecast broadcast |
| `eligibility_period_start`| `DATE` | NOT NULL | ISO-8601 Date | Start date of eligibility evaluation window |
| `eligibility_period_end` | `DATE` | NOT NULL | `CHECK (end >= start)` | Cutoff date for commercial eligibility |
| `host_city` | `VARCHAR(64)` | NOT NULL | None | Metropolitan city hosting ceremony |
| `venue_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `venues(venue_id)` | Venue location identifier |
| `primary_network` | `VARCHAR(32)` | NOT NULL | Enum: CBS, NBC, ABC, Syndication | Primary television broadcast rights holder |
| `total_awards_presented` | `INT` | NOT NULL | `CHECK (> 0)` | Total competitive + honorary statuettes awarded |
| `created_at` | `TIMESTAMP` | NOT NULL | `DEFAULT CURRENT_TIMESTAMP` | Audit record insertion timestamp |

### 4.3. Relation: `telecast_broadcasters`
- **Formal Notation**: $\text{telecast\_broadcasters}(\underline{\text{broadcast\_id}}, \text{ceremony\_id}, \text{network\_name}, \text{country\_code}, \text{broadcast\_start\_time\_utc}, \text{scheduled\_duration\_minutes}, \text{executive\_producer}, \text{director\_name}, \text{parental\_advisory\_rating}, \text{hd\_4k\_feed\_enabled})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `broadcast_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Unique telecast contract broadcast key |
| `ceremony_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `ceremonies(ceremony_id)` | Associated telecast ceremony |
| `network_name` | `VARCHAR(64)` | NOT NULL | None | Commercial television network name |
| `country_code` | `CHAR(2)` | NOT NULL | `DEFAULT 'US'` | ISO 3166-1 alpha-2 sovereign territory code |
| `broadcast_start_time_utc`| `TIMESTAMP` | NOT NULL | UTC Timestamp | Official airtime kickoff |
| `scheduled_duration_minutes`| `INT` | NOT NULL | `CHECK (> 0)` | Planned program length |
| `executive_producer` | `VARCHAR(128)` | NOT NULL | None | Lead showrunner producing the live telecast |
| `director_name` | `VARCHAR(128)` | NOT NULL | None | Multi-camera television director |
| `parental_advisory_rating` | `VARCHAR(16)` | NOT NULL | TV-14, TV-PG, TV-G | FCC television parental guidance rating |
| `hd_4k_feed_enabled` | `BOOLEAN` | NOT NULL | `DEFAULT TRUE` | Ultra-high definition feed transmission status |

### 4.4. Relation: `viewership_ratings` (Weak Entity Mapped)
- **Formal Notation**: $\text{viewership\_ratings}(\underline{\text{rating\_id}}, \text{ceremony\_id}, \text{us\_viewers\_millions}, \text{household\_rating\_pct}, \text{household\_share\_pct}, \text{demo\_18\_49\_rating}, \text{peak\_viewers\_millions}, \text{peak\_broadcast\_segment}, \text{digital\_streaming\_views\_millions}, \text{measurement\_agency})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `rating_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Unique rating audit identifier |
| `ceremony_id` | `VARCHAR(32)` | NOT NULL | **UNIQUE, FOREIGN KEY** $\rightarrow$ `ceremonies(ceremony_id)` | Identifying ceremony relationship |
| `us_viewers_millions` | `NUMERIC(5,2)` | NOT NULL | `CHECK (>= 0)` | Average live+same day US viewers |
| `household_rating_pct` | `NUMERIC(4,2)` | NOT NULL | `CHECK (>= 0)` | Percentage of all US households tuned |
| `household_share_pct` | `NUMERIC(4,2)` | NOT NULL | `CHECK (>= 0)` | Percentage of television sets in use |
| `demo_18_49_rating` | `NUMERIC(4,2)` | NOT NULL | `CHECK (>= 0)` | Key commercial demographic rating point |
| `peak_viewers_millions` | `NUMERIC(5,2)` | NULL | `CHECK (peak >= avg)` | Maximum instantaneous viewer peak |
| `peak_broadcast_segment` | `VARCHAR(128)` | NULL | None | Telecast performance segment during peak |
| `digital_streaming_views_millions`| `NUMERIC(5,2)` | NOT NULL | `DEFAULT 0.0` | Digital Paramount+/CBS app OTT live streams |
| `measurement_agency` | `VARCHAR(64)` | NOT NULL | `DEFAULT 'Nielsen Media Research'` | Accredited rating auditing authority |

### 4.5. Relation: `ceremony_hosts`
- **Formal Notation**: $\text{ceremony\_hosts}(\underline{\text{host\_record\_id}}, \text{ceremony\_id}, \text{creator\_id}, \text{host\_name}, \text{monologue\_minutes}, \text{is\_solo\_host}, \text{performance\_open\_flag}, \text{emmy\_nominated\_for\_show}, \text{compensation\_tier}, \text{notes})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `host_record_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Unique hosting appearance identifier |
| `ceremony_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `ceremonies(ceremony_id)` | Staged ceremony edition |
| `creator_id` | `VARCHAR(32)` | NULL | **FOREIGN KEY** $\rightarrow$ `creators(creator_id)` | Pointer to master talent directory (DB5) |
| `host_name` | `VARCHAR(128)` | NOT NULL | None | Public billed name of master of ceremonies |
| `monologue_minutes` | `INT` | NOT NULL | `CHECK (>= 0)` | Duration of introductory standup/speech |
| `is_solo_host` | `BOOLEAN` | NOT NULL | `DEFAULT TRUE` | False if ensemble co-hosted |
| `performance_open_flag` | `BOOLEAN` | NOT NULL | `DEFAULT FALSE` | True if host delivered a musical performance |
| `emmy_nominated_for_show`| `BOOLEAN` | NOT NULL | `DEFAULT FALSE` | Primetime Emmy Outstanding Variety Special nomination |
| `compensation_tier` | `VARCHAR(32)` | NOT NULL | Standard SAG-AFTRA scale classification | Union compensation bracket tier |
| `notes` | `TEXT` | NULL | None | Anecdotes or archival context |

### 4.6. Relations: `historic_milestones`, `academy_leadership`, `timeline_historical_eras`, `press_media_accreditations`, `lifetime_achievement_honors`
- Defined in full alignment with [`schemas/relational_ddl/relational_reference_schema.sql`](../schemas/relational_ddl/relational_reference_schema.sql), enforcing 10+ meaningful fields, rigorous check constraints, and referential integrity to `ceremonies` and `creators`.

---

## 5. Domain 2: Categories & Taxonomy Domain (`grammy_categories_db`)

### 5.1. Relation: `award_fields`
- **Formal Notation**: $\text{award\_fields}(\underline{\text{field\_id}}, \text{field\_name}, \text{field\_abbreviation}, \text{field\_description}, \text{inaugural\_ceremony\_edition}, \text{current\_active\_status}, \text{active\_categories\_count}, \text{specialist\_committee\_jurisdiction}, \text{field\_curator\_role}, \text{last\_bylaw\_revision\_year})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `field_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Canonical field key (e.g., `FLD_GENERAL_FIELD`, `FLD_POP`) |
| `field_name` | `VARCHAR(64)` | NOT NULL | **UNIQUE** | Formal genre field title |
| `field_abbreviation` | `VARCHAR(16)` | NOT NULL | Code identifier (e.g., `GEN`, `POP`, `ROC`, `RAP`) | Compact field acronym |
| `field_description` | `TEXT` | NOT NULL | None | Scope of musical traditions enclosed |
| `inaugural_ceremony_edition`| `INT` | NOT NULL | `CHECK (> 0)` | Ceremony edition when field was recognized |
| `current_active_status`| `BOOLEAN` | NOT NULL | `DEFAULT TRUE` | Active voting status in current cycle |
| `active_categories_count`| `INT` | NOT NULL | `DEFAULT 0, CHECK (>= 0)` | Subordinate active categories tally |
| `specialist_committee_jurisdiction`| `VARCHAR(128)` | NOT NULL | None | Craft screening committee oversight body |
| `field_curator_role` | `VARCHAR(64)` | NOT NULL | None | Academy executive trustee overseeing genre |
| `last_bylaw_revision_year`| `INT` | NULL | `CHECK (>= 1958)` | Year field boundaries were last updated |

### 5.2. Relation: `award_categories` (Superclass Mapped)
- **Formal Notation**: $\text{award\_categories}(\underline{\text{category\_id}}, \text{field\_id}, \text{official\_category\_name}, \text{standard\_short\_code}, \text{inaugural\_edition}, \text{is\_general\_field}, \text{current\_status}, \text{maximum\_nominees\_allowed}, \text{voting\_tier\_access}, \text{trophy\_statuette\_eligibility\_rule}, \text{entry\_fee\_tier})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `category_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Category code (e.g., `CAT_ALBUM_OF_THE_YEAR`) |
| `field_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `award_fields(field_id)` | Containing genre field reference |
| `official_category_name`| `VARCHAR(128)` | NOT NULL | **UNIQUE** | Legal Grammy category title on ballots |
| `standard_short_code` | `VARCHAR(32)` | NOT NULL | Code (e.g., `AOTY`, `ROTY`, `SOTY`, `BNA`) | Standard abbreviated shorthand code |
| `inaugural_edition` | `INT` | NOT NULL | `CHECK (> 0)` | First ceremony edition presented |
| `is_general_field` | `BOOLEAN` | NOT NULL | `DEFAULT FALSE` | True if open to all voting members (Big Four) |
| `current_status` | `VARCHAR(32)` | NOT NULL | `DEFAULT 'Active'` (Active, Retired, Suspended) | Present operational status |
| `maximum_nominees_allowed`| `INT` | NOT NULL | `DEFAULT 5, CHECK (>= 3)` | Maximum slots on final ballot (5, 8, 10) |
| `voting_tier_access` | `VARCHAR(64)` | NOT NULL | All Members, Specialist Peer Review | Electorate eligibility classification |
| `trophy_statuette_eligibility_rule`| `VARCHAR(128)` | NOT NULL | Bylaw rule for physical statuette awards | Criteria for physical Grammy conferral |
| `entry_fee_tier` | `VARCHAR(32)` | NOT NULL | Member-Free, Label Tier 1, Label Tier 2 | Academy submission fee schedule |

### 5.3. Relations: `eligibility_rules`, `voting_procedures`, `category_lineage`, `category_quotas_limits`, `discontinued_categories`, `special_merit_categories`, `craft_credit_definitions`, `merged_split_history`
- Modeled to capture the complete governance, lineage restructuring, and ballot quota algorithms of the Academy, with explicit foreign keys to `award_categories(category_id)`.

---

## 6. Domain 3: Creators & Labels Domain (`grammy_creators_db`)

### 6.1. Relation: `creators` (Superclass Mapped)
- **Formal Notation**: $\text{creators}(\underline{\text{creator\_id}}, \text{full\_legal\_name}, \text{stage\_name}, \text{primary\_musical\_genre}, \text{birth\_or\_formation\_date}, \text{country\_of\_citizenship}, \text{active\_career\_start\_year}, \text{is\_group\_ensemble\_flag}, \text{musicbrainz\_gid}, \text{official\_website\_url}, \text{biography\_overview})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `creator_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Canonical creator identifier (e.g., `CRT_BEYONCE_KNOWLES`) |
| `full_legal_name` | `VARCHAR(128)` | NOT NULL | None | Legal birth/corporate name of practitioner |
| `stage_name` | `VARCHAR(128)` | NULL | None | Billed professional performance alias |
| `primary_musical_genre`| `VARCHAR(64)` | NULL | None | Primary artistic musical tradition |
| `birth_or_formation_date`| `DATE` | NULL | ISO-8601 Date | Date of birth (or legal ensemble founding) |
| `country_of_citizenship`| `VARCHAR(64)` | NOT NULL | None | Sovereign nationality for world music quotas |
| `active_career_start_year`| `INT` | NULL | `CHECK (>= 1920)` | First professional commercial release year |
| `is_group_ensemble_flag`| `BOOLEAN` | NOT NULL | `DEFAULT FALSE` | True if multi-person musical collective |
| `musicbrainz_gid` | `CHAR(36)` | NULL | **UNIQUE**, UUID format | Open-source linked authority key |
| `official_website_url` | `VARCHAR(255)` | NULL | None | Official verified web portal |
| `biography_overview` | `TEXT` | NULL | None | Archival biographical abstract |

### 6.2. Relations: Overlapping Subclasses of `CREATOR`
Following Elmasri & Navathe Algorithm 8 for **Overlapping Specialization**:
- $\text{artists}(\underline{\text{creator\_id}}, \text{vocal\_range}, \text{primary\_instrument}, \text{solo\_billing\_tier}, \text{hall\_of\_fame\_eligible\_year})$
- $\text{producers}(\underline{\text{producer\_id}}, \text{creator\_id}, \text{primary\_production\_genre}, \text{headquarters\_studio\_location}, \text{analog\_digital\_workflow\_preference}, \dots)$
- $\text{audio\_engineers}(\underline{\text{engineer\_id}}, \text{creator\_id}, \text{engineering\_specialization}, \text{primary\_mastering\_facility}, \text{dolby\_atmos\_certified\_status}, \dots)$
- $\text{songwriters\_composers}(\underline{\text{songwriter\_id}}, \text{creator\_id}, \text{pro\_affiliation}, \text{ipi\_cae\_identifier}, \text{music\_publisher\_company}, \dots)$
- $\text{arrangers\_conductors}(\underline{\text{arranger\_id}}, \text{creator\_id}, \text{arrangement\_discipline}, \text{resident\_orchestra\_ensemble}, \text{union\_musicians\_local}, \dots)$

### 6.3. Relations: `record_labels`, `musical_groups`, `group_memberships`, `creator_collaborations`
- `group_memberships` maps the $M:N$ tenure between `creators` and `musical_groups`.

---

## 7. Domain 4: Nominations & Ballots Domain (`grammy_nominations_db`)

### 7.1. Relation: `nominated_works` (Superclass Mapped)
- **Formal Notation**: $\text{nominated\_works}(\underline{\text{work\_id}}, \text{work\_type}, \text{work\_title}, \text{commercial\_release\_date}, \text{primary\_label\_id}, \text{isrc\_code}, \text{upc\_barcode}, \text{duration\_total\_seconds}, \text{track\_count}, \text{parental\_advisory\_flag}, \text{language\_iso\_code})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `work_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Canonical master catalog key (e.g., `WRK_RENAISSANCE_2022`) |
| `work_type` | `VARCHAR(32)` | NOT NULL | Enum: Album, Single/Track, Video, Box Set | Physical medium classification |
| `work_title` | `VARCHAR(255)` | NOT NULL | None | Official release title |
| `commercial_release_date`| `DATE` | NOT NULL | ISO-8601 Date | Initial commercial public release date |
| `primary_label_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `record_labels(label_id)` | Releasing record company (DB5) |
| `isrc_code` | `VARCHAR(32)` | NULL | Unique Track ISRC standard | International Standard Recording Code |
| `upc_barcode` | `VARCHAR(32)` | NULL | Barcode standard | Universal Product Code (Albums) |
| `duration_total_seconds`| `INT` | NOT NULL | `CHECK (> 0)` | Total runtime in seconds |
| `track_count` | `INT` | NOT NULL | `DEFAULT 1, CHECK (>= 1)` | Total audio tracks on album |
| `parental_advisory_flag`| `BOOLEAN` | NOT NULL | `DEFAULT FALSE` | Explicit lyrics content advisory |
| `language_iso_code` | `CHAR(2)` | NOT NULL | `DEFAULT 'en'` | ISO 639-1 dominant language |

### 7.2. Relation: `nomination_entries`
- **Formal Notation**: $\text{nomination\_entries}(\underline{\text{nomination\_id}}, \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{nomination\_year}, \text{entry\_billing\_title}, \text{primary\_artist\_id}, \text{is\_winner\_flag}, \text{ballot\_slot\_order}, \text{auditor\_validation\_code}, \text{created\_timestamp})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `nomination_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Certified nomination ID (e.g., `NOM_065_AOTY_01`) |
| `ceremony_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `ceremonies(ceremony_id)` | Staging ceremony edition (DB1) |
| `category_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `award_categories(category_id)` | Competing award category (DB2) |
| `work_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `nominated_works(work_id)` | Master creative entry |
| `nomination_year` | `INT` | NOT NULL | `CHECK (>= 1959)` | Calendar year of ceremony ballot |
| `entry_billing_title` | `VARCHAR(255)` | NOT NULL | None | Official printed title on the ballot |
| `primary_artist_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `creators(creator_id)` | Lead credited recording artist (DB5) |
| `is_winner_flag` | `BOOLEAN` | NOT NULL | `DEFAULT FALSE` | True if elevated to winner record |
| `ballot_slot_order` | `INT` | NOT NULL | `CHECK (> 0)` | Alphabetical slot on voting paper/screen |
| `auditor_validation_code`| `VARCHAR(64)` | NOT NULL | Deloitte certified token | Cryptographic ballot tally signoff |
| `created_timestamp` | `TIMESTAMP` | NOT NULL | `DEFAULT CURRENT_TIMESTAMP` | Initial tabulation record creation time |
| *Composite Constraint* | None | - | **UNIQUE** (`ceremony_id`, `category_id`, `work_id`) | Prevent duplicate nominations in one category |

### 7.3. Relation: `nomination_credits` (Conceptual Aggregation Mapped)
- **Formal Notation**: $\text{nomination\_credits}(\underline{\text{credit\_id}}, \text{nomination\_id}, \text{creator\_id}, \text{credit\_role}, \text{credit\_billing\_rank}, \text{work\_contribution\_summary}, \text{contribution\_percentage}, \text{is\_lead\_performer}, \text{is\_producer\_credit}, \text{academy\_verified\_status})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `credit_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Unique aggregated credit identifier |
| `nomination_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `nomination_entries(nomination_id)` | Parent nomination entry |
| `creator_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `creators(creator_id)` | Credited talent individual (DB5) |
| `credit_role` | `VARCHAR(64)` | NOT NULL | Enum: Producer, Engineer, Songwriter, Artist | Specific craft contribution role |
| `credit_billing_rank` | `INT` | NOT NULL | `DEFAULT 1` | Official priority order on ballot citation |
| `work_contribution_summary`| `VARCHAR(128)`| NOT NULL | None | Specific tracks produced or engineered |
| `contribution_percentage`| `NUMERIC(5,2)` | NOT NULL | `DEFAULT 0.0, CHECK (0 to 100)` | Playing time contribution percentage |
| `is_lead_performer` | `BOOLEAN` | NOT NULL | `DEFAULT FALSE` | True if primary headline artist |
| `is_producer_credit` | `BOOLEAN` | NOT NULL | `DEFAULT FALSE` | True if eligible under Producer/Engineer rules |
| `academy_verified_status`| `BOOLEAN` | NOT NULL | `DEFAULT TRUE` | Craft committee audit verification passed |
| *Composite Constraint* | None | - | **UNIQUE** (`nomination_id`, `creator_id`, `credit_role`) | No duplicate identical roles for one creator |

### 7.4. Relations: `submission_batches`, `genre_classifications`, `first_time_nominees`, `tied_nominations`, `multi_nomination_packages`, `voter_screening_batches`, `nomination_audit_logs`
- Full tabular definitions enforcing intake batches, first-round screening, ties, and Deloitte auditing.

---

## 8. Domain 5: Winners & Trophies Domain (`grammy_winners_db`)

### 8.1. Relation: `winner_records`
- **Formal Notation**: $\text{winner\_records}(\underline{\text{winner\_record\_id}}, \text{nomination\_id}, \text{ceremony\_id}, \text{category\_id}, \text{winning\_work\_id}, \text{primary\_artist\_id}, \text{broadcast\_presentation\_order}, \text{presented\_live\_on\_telecast}, \text{acceptance\_speech\_delivered}, \text{trophy\_statuettes\_awarded\_count}, \text{verified\_timestamp})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `winner_record_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Canonical winner record key |
| `nomination_id` | `VARCHAR(32)` | NOT NULL | **UNIQUE, FOREIGN KEY** $\rightarrow$ `nomination_entries` | Associated elevated nomination (DB3) |
| `ceremony_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `ceremonies(ceremony_id)` | Ceremony staging the win (DB1) |
| `category_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `award_categories(category_id)`| Won category (DB2) |
| `winning_work_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `nominated_works(work_id)` | Victorious master work (DB3) |
| `primary_artist_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `creators(creator_id)` | Headline artist recipient (DB5) |
| `broadcast_presentation_order`| `INT` | NOT NULL | `CHECK (> 0)` | Presentation sequence during show |
| `presented_live_on_telecast`| `BOOLEAN` | NOT NULL | `DEFAULT TRUE` | False if awarded at Premiere Ceremony |
| `acceptance_speech_delivered`| `BOOLEAN` | NOT NULL | `DEFAULT TRUE` | True if live speech delivered from stage |
| `trophy_statuettes_awarded_count`| `INT` | NOT NULL | `CHECK (>= 1)` | Physical gold statuettes authorized |
| `verified_timestamp` | `TIMESTAMP` | NOT NULL | `DEFAULT CURRENT_TIMESTAMP` | Official Deloitte envelope confirmation time |

### 8.2. Relation: `trophy_tracking`
- **Formal Notation**: $\text{trophy\_tracking}(\underline{\text{trophy\_id}}, \text{winner\_record\_id}, \text{recipient\_creator\_id}, \text{statuette\_serial\_number}, \text{engraved\_billing\_text}, \text{manufacturing\_foundry\_name}, \text{grammium\_alloy\_specification}, \text{gold\_plating\_thickness\_microns}, \text{dispatch\_shipment\_date}, \text{custody\_receipt\_hash})$
- **Attribute Dictionary**:

| Attribute Name | Domain / Data Type | Nullability | Constraints / Defaults | Domain Semantics |
| :--- | :--- | :---: | :--- | :--- |
| `trophy_id` | `VARCHAR(32)` | NOT NULL | **PRIMARY KEY** | Unique statuette inventory key |
| `winner_record_id` | `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `winner_records` | Parent elevated victory |
| `recipient_creator_id`| `VARCHAR(32)` | NOT NULL | **FOREIGN KEY** $\rightarrow$ `creators(creator_id)` | Physical statuette recipient (DB5) |
| `statuette_serial_number`| `VARCHAR(64)` | NOT NULL | **UNIQUE** | Inscribed physical serial identifier |
| `engraved_billing_text`| `TEXT` | NOT NULL | None | Precision engraving text on brass plate |
| `manufacturing_foundry_name`| `VARCHAR(128)`| NOT NULL | `DEFAULT 'Billings Artworks'` | Foundry casting the statuette |
| `grammium_alloy_specification`| `VARCHAR(64)`| NOT NULL | Zinc-based custom alloy specification | Custom metallurgic alloy formulation |
| `gold_plating_thickness_microns`| `NUMERIC(4,2)`| NOT NULL | `DEFAULT 5.0, CHECK (> 0)` | 24-karat gold plating layer depth |
| `dispatch_shipment_date`| `DATE` | NULL | ISO-8601 Date | Date statuette shipped to recipient |
| `custody_receipt_hash`| `VARCHAR(64)` | NULL | Courier delivery verification digest | Signature cryptographic delivery receipt |

### 8.3. Relations: `big_four_sweeps`, `record_breakers`, `acceptance_speeches`, `consecutive_winners`, `posthumous_awards`, `historic_win_benchmarks`, `hall_of_fame_inductions`, `winner_press_releases`
- Model derived analytics (Big Four sweeps, all-time record breakers), historical milestones (Hall of Fame), acceptance speeches, and media distribution.

---

## 9. Normal Form Analysis & Verification

Each of the 50 relations is structured in **Third Normal Form (3NF)** and **Boyce-Codd Normal Form (BCNF)**:

1. **First Normal Form (1NF)**:
   - All attribute values are atomic across their domains.
   - Multivalued attributes identified in Phase 6 (e.g., creator instruments, ceremony co-hosts, work genres) are either modeled in separate associative relations (`group_memberships`, `craft_credit_definitions`, `genre_classifications`) or structured as typed scalar fields before MongoDB denormalization.
2. **Second Normal Form (2NF)**:
   - Every relation is in 1NF.
   - Every non-prime attribute is fully functionally dependent on the entire primary key. In relations with composite primary keys (`group_memberships` with candidate key `(group_id, creator_id)`, or `nomination_entries` with alternate key `(ceremony_id, category_id, work_id)`), no non-prime attribute depends on a proper subset of the key.
3. **Third Normal Form (3NF)**:
   - Every relation is in 2NF.
   - No non-prime attribute is transitively dependent on the primary key ($X \rightarrow Y \rightarrow Z$). Attributes representing derived statistics (e.g., total career wins, viewership ratings) are decoupled from operational ballot records.
4. **Boyce-Codd Normal Form (BCNF)**:
   - For every non-trivial functional dependency $X \rightarrow Y$, $X$ is a superkey of the relation.
