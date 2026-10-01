# Candidate Key Analysis & Attribute Prime Classification

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 8 — Functional Dependency Analysis  
> **Document**: Rigorous Mathematical Derivation of Candidate Keys, Attribute Closures, Prime/Non-Prime Classifications, and Key Redundancy Audits across all 50 Domain Relations  
> **Status**: Completed  
> **Theoretical Framework**: Elmasri & Navathe (*Fundamentals of Database Systems*, 7th Edition, Chapters 14 & 15) / Codd (1970, 1972)  
> **Related Artifacts**:  
> - Functional Dependency Analysis: [`normalization/functional-dependencies.md`](./functional-dependencies.md)  
> - Relational Schema Catalog: [`relational-model/schema.md`](../relational-model/schema.md)  
> - Keys & Referential Integrity: [`relational-model/keys-and-relationships.md`](../relational-model/keys-and-relationships.md)  

---

## 1. Formal Mathematical Definitions of Relational Keys

In relational database theory:

### 1.1. Superkey ($SK$)
Let $R(A_1, A_2, \dots, A_n)$ be a relation schema with functional dependency set $F$.
A subset of attributes $SK \subseteq R$ is a **Superkey** of $R$ if the attribute closure of $SK$ with respect to $F$ contains all attributes of $R$:
$$SK^+ = R$$
Equivalently:
$$\forall t_1, t_2 \in r(R), \quad t_1 \neq t_2 \implies t_1[SK] \neq t_2[SK]$$

---

### 1.2. Candidate Key ($CK$)
A subset of attributes $CK \subseteq R$ is a **Candidate Key** of $R$ if:
1. **Sufficiency**: $CK$ is a superkey ($CK^+ = R$), and
2. **Minimality (Irreducibility)**: No proper subset of $CK$ is a superkey:
   $$\forall A \in CK, \quad (CK - \{A\})^+ \neq R$$

---

### 1.3. Primary Key ($PK$) & Alternate Key ($AK$)
- **Primary Key ($PK$)**: The specific candidate key chosen by the database designer as the principal tuple identifier. By the **Entity Integrity Rule**, no attribute of the primary key may contain a null value:
  $$\forall t \in r(R), \quad t[PK] \neq \text{NULL}$$
- **Alternate Key ($AK$)**: Any candidate key of $R$ that is not designated as the primary key. In SQL implementations, alternate keys are enforced using `UNIQUE NOT NULL` constraints.

---

### 1.4. Prime vs. Non-Prime Attributes
- **Prime Attribute**: An attribute $A \in R$ is **prime** if $A$ is a member of *at least one* candidate key of $R$:
  $$\text{Prime}(R) = \{ A \in R \mid \exists CK \in \text{CandidateKeys}(R) \text{ such that } A \in CK \}$$
- **Non-Prime Attribute**: An attribute $A \in R$ is **non-prime** if it does not appear in any candidate key of $R$:
  $$\text{NonPrime}(R) = R - \text{Prime}(R)$$

This distinction is mathematically vital:
- **2NF** prohibits partial dependencies of *non-prime* attributes on candidate keys.
- **3NF** permits dependencies $X \to A$ where $X$ is not a superkey *if and only if* $A$ is a *prime* attribute.
- **BCNF** eliminates the prime attribute exemption, requiring $X$ to be a superkey for *all* non-trivial dependencies.

---

## 2. Systematic Candidate Key Derivation Algorithm

To determine all candidate keys of a relation schema $R$ under functional dependency set $F$, we employ the **Attribute Partitioning & Closure Search Algorithm**:

```text
Algorithm: FindAllCandidateKeys(R, F)
Input: Relation schema R, Minimal Cover F
Output: CandidateKeys (Set of minimal keys)

1. Partition R into four disjoint subsets based on attribute positions in F:
   - L (Left-Only): Attributes that appear only on the left-hand side of dependencies in F.
   - R (Right-Only): Attributes that appear only on the right-hand side of dependencies in F.
   - B (Both): Attributes that appear on both left and right sides of dependencies in F.
   - N (Neither): Attributes that do not appear anywhere in F.

2. Mandatory Core Key:
   K_core := L ∪ N;

3. Check Core Key Closure:
   if ComputeAttributeClosure(K_core, F) = R then
       return { K_core };  // K_core is the unique, minimal candidate key!
   end if;

4. Combinatorial Search with Set B:
   CandidateKeys := ∅;
   for size := 1 to |B| do
       for each subset S ⊆ B of cardinality 'size' do
           Candidate := K_core ∪ S;
           if ComputeAttributeClosure(Candidate, F) = R then
               // Verify minimality against already found candidate keys
               if not (∃ K ∈ CandidateKeys such that K ⊂ Candidate) then
                   CandidateKeys := CandidateKeys ∪ { Candidate };
               end if;
           end if;
       end for;
   end for;
   return CandidateKeys;
```

---

## 3. Universal Schema ($\mathcal{U}_{GRAMMY}$) Key Derivation

Consider the monolithic flat relation representing the entire GRAMMY operational domain:

$$\mathcal{U}_{GRAMMY}(\text{ceremony\_id}, \text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{venue\_name}, \text{venue\_city}, \text{venue\_capacity}, \text{network\_name}, \text{us\_viewers\_millions},$$
$$\text{category\_id}, \text{category\_name}, \text{field\_id}, \text{field\_name}, \text{work\_id}, \text{work\_title}, \text{work\_type}, \text{release\_date}, \text{label\_id}, \text{label\_name},$$
$$\text{creator\_id}, \text{creator\_legal\_name}, \text{stage\_name}, \text{creator\_country}, \text{credit\_role}, \text{contribution\_pct}, \text{nomination\_id}, \text{ballot\_slot}, \text{is\_winner}, \text{statuette\_serial})$$

### 3.1. Attribute Partitioning:
- **Left-Only ($L$)**: $\{\text{credit\_role}\}$ (No dependency produces a credit role).
- **Right-Only ($R$)**: $\{\text{ceremony\_date}, \text{venue\_name}, \text{venue\_city}, \text{venue\_capacity}, \text{network\_name}, \text{us\_viewers\_millions}, \text{category\_name}, \text{field\_name}, \text{work\_title}, \text{work\_type}, \text{release\_date}, \text{label\_name}, \text{creator\_legal\_name}, \text{stage\_name}, \text{creator\_country}, \text{ballot\_slot}, \text{is\_winner}, \text{contribution\_pct}\}$.
- **Both ($B$)**: $\{\text{ceremony\_id}, \text{edition\_number}, \text{venue\_id}, \text{category\_id}, \text{field\_id}, \text{work\_id}, \text{label\_id}, \text{creator\_id}, \text{nomination\_id}, \text{statuette\_serial}\}$.
- **Neither ($N$)**: $\emptyset$.

### 3.2. Closure Evaluation:
1. **Core Key**: $K_0 = L \cup N = \{\text{credit\_role}\}$.
   $$\{\text{credit\_role}\}^+ = \{\text{credit\_role}\} \neq \mathcal{U}_{GRAMMY}$$
2. Adding attributes from $B$:
   - Test $K_1 = \{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}\}$:
     - $\text{nomination\_id}^+ \implies \{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{ballot\_slot}, \text{is\_winner}\}$
     - $\text{ceremony\_id}^+ \implies \{\text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{network\_name}, \text{us\_viewers\_millions}\}$
     - $\text{venue\_id}^+ \implies \{\text{venue\_name}, \text{venue\_city}, \text{venue\_capacity}\}$
     - $\text{category\_id}^+ \implies \{\text{category\_name}, \text{field\_id}\}$
     - $\text{field\_id}^+ \implies \{\text{field\_name}\}$
     - $\text{work\_id}^+ \implies \{\text{work\_title}, \text{work\_type}, \text{release\_date}, \text{label\_id}\}$
     - $\text{label\_id}^+ \implies \{\text{label\_name}\}$
     - $\text{creator\_id}^+ \implies \{\text{creator\_legal\_name}, \text{stage\_name}, \text{creator\_country}\}$
     - $\{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}\}^+ \implies \text{contribution\_pct}$
   - Because all attributes in $\mathcal{U}_{GRAMMY}$ (except optional physical trophy serial) are derived, and no proper subset of $K_1$ determines all attributes:
     $$CK_1 = \{ \text{nomination\_id}, \text{creator\_id}, \text{credit\_role} \}$$
3. Alternate Candidate Key (Substituting natural keys):
   - Because $\{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}\} \to \text{nomination\_id}$:
     $$CK_2 = \{ \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{creator\_id}, \text{credit\_role} \}$$
   - Because $\text{edition\_number} \leftrightarrow \text{ceremony\_id}$:
     $$CK_3 = \{ \text{edition\_number}, \text{category\_id}, \text{work\_id}, \text{creator\_id}, \text{credit\_role} \}$$

### 3.3. Prime vs. Non-Prime Attributes of $\mathcal{U}_{GRAMMY}$:
- **Prime Attributes**: $\{\text{nomination\_id}, \text{ceremony\_id}, \text{edition\_number}, \text{category\_id}, \text{work\_id}, \text{creator\_id}, \text{credit\_role}\}$.
- **Non-Prime Attributes**: All other 23 attributes ($\text{venue\_name}, \text{work\_title}, \text{stage\_name}, \dots$).

---

## 4. In-Depth Key Analysis for All 5 Database Domains

Below is the exhaustive, mathematical key derivation for all 50 relations in the normalized schema:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       GLOBAL 50-RELATION CANDIDATE KEY DIRECTORY                                       │
├──────────────────────┬────────────────────────────────┬──────────────────────────────┬─────────────────────────────────┤
│ Domain Database      │ Relation Name                  │ Primary Key (PK)             │ Alternate Candidate Keys (AK)   │
├──────────────────────┼────────────────────────────────┼──────────────────────────────┼─────────────────────────────────┤
│ grammy_history_db    │ venues                         │ venue_id                     │ venue_name                      │
│                      │ ceremonies                     │ ceremony_id                  │ edition_number                  │
│                      │ telecast_broadcasters          │ broadcast_id                 │ (ceremony_id, network_name)     │
│                      │ viewership_ratings             │ rating_id                    │ ceremony_id                     │
│                      │ ceremony_hosts                 │ host_record_id               │ (ceremony_id, host_name)        │
│                      │ historic_milestones            │ milestone_id                 │ (ceremony_id, milestone_title)  │
│                      │ academy_leadership             │ leadership_id                │ (officer_name, role, start_yr)  │
│                      │ timeline_historical_eras       │ era_id                       │ era_name                        │
│                      │ press_media_accreditations     │ accreditation_id             │ (ceremony_id, media_org_name)   │
│                      │ lifetime_achievement_honors    │ honor_id                     │ (honoree_name, ceremony_edition)│
├──────────────────────┼────────────────────────────────┼──────────────────────────────┼─────────────────────────────────┤
│ grammy_categories_db │ award_fields                   │ field_id                     │ field_name                      │
│                      │ award_categories               │ category_id                  │ official_category_name          │
│                      │ category_lineage               │ lineage_id                   │ (category_id, effective_edition)│
│                      │ eligibility_rules              │ rule_id                      │ (category_id, effective_edition)│
│                      │ voting_procedures              │ procedure_id                 │ (category_id, voting_round_no)  │
│                      │ discontinued_categories        │ discontinued_id              │ category_name                   │
│                      │ category_quotas_limits         │ quota_id                     │ (category_id, ceremony_edition) │
│                      │ special_merit_categories       │ special_merit_id             │ award_title                     │
│                      │ craft_credit_definitions       │ craft_def_id                 │ (category_id, craft_role_name)  │
│                      │ merged_split_history           │ event_id                     │ (primary_category_id, eff_year) │
├──────────────────────┼────────────────────────────────┼──────────────────────────────┼─────────────────────────────────┤
│ grammy_creators_db   │ creators                       │ creator_id                   │ musicbrainz_gid                 │
│                      │ artists                        │ creator_id                   │ stage_name                      │
│                      │ producers                      │ producer_id                  │ creator_id                      │
│                      │ audio_engineers                │ engineer_id                  │ creator_id                      │
│                      │ songwriters_composers          │ songwriter_id                │ (creator_id, ipi_cae_identifier)│
│                      │ arrangers_conductors           │ arranger_id                  │ creator_id                      │
│                      │ record_labels                  │ label_id                     │ label_corporate_name            │
│                      │ musical_groups                 │ group_id                     │ group_name, mb_group_gid        │
│                      │ group_memberships              │ membership_id                │ (group_id, creator_id)          │
│                      │ creator_collaborations         │ collaboration_id             │ (lead_id, collab_id, year)      │
├──────────────────────┼────────────────────────────────┼──────────────────────────────┼─────────────────────────────────┤
│ grammy_nominations_db│ nominated_works                │ work_id                      │ isrc_code, upc_barcode          │
│                      │ nomination_entries             │ nomination_id                │ (ceremony_id, cat_id, work_id)  │
│                      │ nomination_credits             │ credit_id                    │ (nom_id, creator_id, role)      │
│                      │ submission_batches             │ batch_id                     │ (ceremony_id, reconcil_hash)    │
│                      │ genre_classifications          │ classification_id            │ (work_id, submitted_field_id)   │
│                      │ first_time_nominees            │ first_nom_id                 │ nomination_id                   │
│                      │ tied_nominations               │ tie_id                       │ (ceremony_id, category_id)      │
│                      │ multi_nomination_packages      │ package_id                   │ (ceremony_id, creator_id)       │
│                      │ voter_screening_batches        │ screening_batch_id           │ (ceremony_id, field_id)         │
│                      │ nomination_audit_logs          │ audit_id                     │ nomination_id                   │
├──────────────────────┼────────────────────────────────┼──────────────────────────────┼─────────────────────────────────┤
│ grammy_winners_db    │ winner_records                 │ winner_record_id             │ nomination_id                   │
│                      │ big_four_sweeps                │ sweep_id                     │ (ceremony_id, creator_id)       │
│                      │ record_breakers                │ record_id                    │ (record_metric_name, est_year)  │
│                      │ acceptance_speeches            │ speech_id                    │ winner_record_id                │
│                      │ trophy_tracking                │ trophy_id                    │ statuette_serial_number         │
│                      │ consecutive_winners            │ streak_id                    │ (creator_id, cat_id, start_ed)  │
│                      │ posthumous_awards              │ posthumous_id                │ winner_record_id                │
│                      │ historic_win_benchmarks        │ benchmark_id                 │ benchmark_title                 │
│                      │ hall_of_fame_inductions        │ induction_id                 │ (inducted_work_title, year)     │
│                      │ winner_press_releases          │ release_id                   │ (ceremony_id, release_headline) │
└──────────────────────┴────────────────────────────────┴──────────────────────────────┴─────────────────────────────────┘
```

---

## 5. Detailed Mathematical Proofs for Key Relations

### 5.1. `ceremonies` (Domain 1: History & Operations)
- **Schema**: $\text{ceremonies}(\text{ceremony\_id}, \text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{eligibility\_start}, \text{eligibility\_end}, \text{host\_city}, \text{venue\_id}, \text{network}, \text{total\_awards}, \text{created\_at})$
- **Applicable FDs**:
  1. $\text{ceremony\_id} \to \text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \dots$
  2. $\text{edition\_number} \to \text{ceremony\_id}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \dots$
- **Candidate Key Proof**:
  - $\text{ceremony\_id}^+ = \text{ceremonies}$ (Minimality: Proper subset $\emptyset^+ = \emptyset \neq \text{ceremonies}$).
  - $\text{edition\_number}^+ = \text{ceremonies}$ (Minimality: Proper subset $\emptyset^+ = \emptyset \neq \text{ceremonies}$).
- **Candidate Keys**: $CK_1 = \{\text{ceremony\_id}\}$, $CK_2 = \{\text{edition\_number}\}$.
- **Designation**: Primary Key = $\text{ceremony\_id}$; Alternate Key = $\text{edition\_number}$.
- **Prime Attributes**: $\{\text{ceremony\_id}, \text{edition\_number}\}$.
- **Non-Prime Attributes**: $\{\text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{network}, \text{host\_city}, \dots\}$.

---

### 5.2. `nomination_entries` (Domain 4: Nominations & Ballots)
- **Schema**: $\text{nomination\_entries}(\text{nomination\_id}, \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{nomination\_year}, \text{entry\_billing\_title}, \text{primary\_artist\_id}, \text{is\_winner\_flag}, \text{ballot\_slot\_order}, \text{auditor\_validation\_code}, \text{created\_timestamp})$
- **Applicable FDs**:
  1. $\text{nomination\_id} \to \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{nomination\_year}, \text{entry\_billing\_title}, \text{primary\_artist\_id}, \text{is\_winner\_flag}, \dots$
  2. $\text{ceremony\_id}, \text{category\_id}, \text{work\_id} \to \text{nomination\_id}, \text{entry\_billing\_title}, \text{primary\_artist\_id}, \dots$
- **Candidate Key Proof**:
  - $\text{nomination\_id}^+ = \text{nomination\_entries}$ (Single attribute, immediately minimal).
  - $\{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}\}^+ = \text{nomination\_entries}$.
    - Test $\{\text{ceremony\_id}, \text{category\_id}\}^+$: does not include $\text{work\_id}$.
    - Test $\{\text{category\_id}, \text{work\_id}\}^+$: does not include $\text{ceremony\_id}$.
    - Test $\{\text{ceremony\_id}, \text{work\_id}\}^+$: does not include $\text{category\_id}$.
    - Hence, $\{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}\}$ is minimal.
- **Candidate Keys**: $CK_1 = \{\text{nomination\_id}\}$, $CK_2 = \{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}\}$.
- **Designation**: Primary Key = $\text{nomination\_id}$; Alternate Key = $\{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}\}$.
- **Prime Attributes**: $\{\text{nomination\_id}, \text{ceremony\_id}, \text{category\_id}, \text{work\_id}\}$.
- **Non-Prime Attributes**: $\{\text{entry\_billing\_title}, \text{primary\_artist\_id}, \text{is\_winner\_flag}, \text{ballot\_slot\_order}, \dots\}$.

---

### 5.3. `nomination_credits` (Domain 4: Aggregation Unit)
- **Schema**: $\text{nomination\_credits}(\text{credit\_id}, \text{nomination\_id}, \text{creator\_id}, \text{credit\_role}, \text{credit\_billing\_rank}, \text{work\_contribution\_summary}, \text{contribution\_percentage}, \text{is\_lead\_performer}, \text{is\_producer\_credit}, \text{academy\_verified\_status})$
- **Applicable FDs**:
  1. $\text{credit\_id} \to \text{nomination\_id}, \text{creator\_id}, \text{credit\_role}, \text{contribution\_percentage}, \dots$
  2. $\text{nomination\_id}, \text{creator\_id}, \text{credit\_role} \to \text{credit\_id}, \text{contribution\_percentage}, \dots$
- **Candidate Key Proof**:
  - $\text{credit\_id}^+ = \text{nomination\_credits}$ (Surrogate primary key).
  - $\{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}\}^+ = \text{nomination\_credits}$.
    - A nomination entry has multiple creators; a creator may participate in multiple craft roles on the same entry (e.g., Producer and Sound Engineer).
    - No two-attribute subset determines the entire relation.
- **Candidate Keys**: $CK_1 = \{\text{credit\_id}\}$, $CK_2 = \{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}\}$.
- **Designation**: Primary Key = $\text{credit\_id}$; Alternate Key = $\{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}\}$.
- **Prime Attributes**: $\{\text{credit\_id}, \text{nomination\_id}, \text{creator\_id}, \text{credit\_role}\}$.
- **Non-Prime Attributes**: $\{\text{credit\_billing\_rank}, \text{work\_contribution\_summary}, \text{contribution\_percentage}, \text{is\_lead\_performer}, \dots\}$.

---

### 5.4. `winner_records` (Domain 5: Winners & Trophies)
- **Schema**: $\text{winner\_records}(\text{winner\_record\_id}, \text{nomination\_id}, \text{ceremony\_id}, \text{category\_id}, \text{winning\_work\_id}, \text{primary\_artist\_id}, \text{presentation\_order}, \text{live\_telecast}, \text{speech\_delivered}, \text{statuettes\_count}, \text{verified\_timestamp})$
- **Applicable FDs**:
  1. $\text{winner\_record\_id} \to \text{nomination\_id}, \text{ceremony\_id}, \dots$
  2. $\text{nomination\_id} \to \text{winner\_record\_id}, \text{ceremony\_id}, \dots$ (Each nomination can win at most once).
- **Candidate Key Proof**:
  - $\text{winner\_record\_id}^+ = \text{winner\_records}$.
  - $\text{nomination\_id}^+ = \text{winner\_records}$ (Since each elevated winner corresponds to exactly one nomination).
- **Candidate Keys**: $CK_1 = \{\text{winner\_record\_id}\}$, $CK_2 = \{\text{nomination\_id}\}$.
- **Designation**: Primary Key = $\text{winner\_record\_id}$; Alternate Key = $\text{nomination\_id}$.
- **Prime Attributes**: $\{\text{winner\_record\_id}, \text{nomination\_id}\}$.
- **Non-Prime Attributes**: $\{\text{ceremony\_id}, \text{category\_id}, \text{winning\_work\_id}, \text{primary\_artist\_id}, \text{presentation\_order}, \dots\}$.

---

### 5.5. `trophy_tracking` (Domain 5: Physical Statuettes)
- **Schema**: $\text{trophy\_tracking}(\text{trophy\_id}, \text{winner\_record\_id}, \text{recipient\_creator\_id}, \text{statuette\_serial\_number}, \text{engraved\_billing\_text}, \text{manufacturing\_foundry}, \text{alloy\_spec}, \text{gold\_plating\_microns}, \text{dispatch\_date}, \text{custody\_receipt\_hash})$
- **Applicable FDs**:
  1. $\text{trophy\_id} \to \text{statuette\_serial\_number}, \text{winner\_record\_id}, \dots$
  2. $\text{statuette\_serial\_number} \to \text{trophy\_id}, \text{winner\_record\_id}, \dots$
- **Candidate Keys**: $CK_1 = \{\text{trophy\_id}\}$, $CK_2 = \{\text{statuette\_serial\_number}\}$.
- **Designation**: Primary Key = $\text{trophy\_id}$; Alternate Key = $\text{statuette\_serial\_number}$.
- **Prime Attributes**: $\{\text{trophy\_id}, \text{statuette\_serial\_number}\}$.
- **Non-Prime Attributes**: $\{\text{winner\_record\_id}, \text{recipient\_creator\_id}, \text{engraved\_billing\_text}, \text{dispatch\_date}, \dots\}$.

---

## 6. Normal Form Classification Summary Across Relations

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              RELATION NORMAL FORM VERIFICATION MATRIX                                  │
├────────────────────────┬──────────────────────┬──────────────────────┬─────────────────────────────────┤
│ Relation Name          │ Highest Normal Form  │ Dependency Basis     │ Anomalies Eliminated            │
├────────────────────────┼──────────────────────┼──────────────────────┼─────────────────────────────────┤
│ venues                 │ BCNF / 3NF           │ venue_id superkey    │ Insertion, Update, Deletion     │
│ ceremonies             │ BCNF / 3NF           │ ceremony_id superkey │ Ceremony repetition anomalies   │
│ award_fields           │ BCNF / 3NF           │ field_id superkey    │ Field description redundancy    │
│ award_categories       │ BCNF / 3NF           │ category_id superkey │ Category naming conflicts       │
│ creators               │ BCNF / 3NF           │ creator_id superkey  │ Artist bio repetition           │
│ record_labels          │ BCNF / 3NF           │ label_id superkey    │ Label headquarters redundancy   │
│ musical_groups         │ BCNF / 3NF           │ group_id superkey    │ Band origin city redundancy     │
│ group_memberships      │ BCNF / 4NF           │ (group, creator) key │ M:N tenure cross-product        │
│ nominated_works        │ BCNF / 3NF           │ work_id superkey     │ Work duration/release conflicts │
│ nomination_entries     │ BCNF / 3NF           │ nomination_id superkey│ Ballot slot anomalies           │
│ nomination_credits     │ BCNF / 4NF           │ credit_id superkey   │ Multi-talent craft credit splits│
│ winner_records         │ BCNF / 3NF           │ winner_record_id SK  │ Unverified winner elevations    │
│ trophy_tracking        │ BCNF / 3NF           │ trophy_id superkey   │ Statuette serial duplication    │
└────────────────────────┴──────────────────────┴──────────────────────┴─────────────────────────────────┘
```
