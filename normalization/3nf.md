# Third Normal Form (3NF) Specification & Transformation

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 9 — Schema Normalization Proofs  
> **Document**: Third Normal Form (3NF) Formal Definition, Transitive Dependency Analysis, 3NF Synthesis Decomposition, Lossless Join Proofs, and Dependency Preservation  
> **Status**: Completed  
> **Theoretical Framework**: E.F. Codd (1971) / Elmasri & Navathe (*Fundamentals of Database Systems*, 7th Edition, Chapters 14 & 15)  
> **Related Artifacts**:  
> - 2NF Baseline: [`normalization/2nf.md`](./2nf.md)  
> - BCNF Transformation: [`normalization/bcnf.md`](./bcnf.md)  
> - Functional Dependencies: [`normalization/functional-dependencies.md`](./functional-dependencies.md)  
> - Normalization Summary: [`normalization/normalization-summary.md`](./normalization-summary.md)  

---

## 1. Formal Theoretical Definition of Third Normal Form (3NF)

According to E.F. Codd (1971):
> A relation schema $R$ is in **Third Normal Form (3NF)** with respect to a set of functional dependencies $F$ if and only if it is in **Second Normal Form (2NF)** and **no non-prime attribute is transitively dependent on any candidate key**.

### 1.1. General Definition of 3NF:
A relation schema $R$ is in 3NF if, for every non-trivial functional dependency $X \to A \in F^+$, at least one of the following conditions holds:
1. $X$ is a **superkey** of $R$, **OR**
2. $A$ is a **prime attribute** of $R$ (i.e., $A$ is a member of some candidate key of $R$).

### 1.2. Transitive Functional Dependency:
A functional dependency $X \to Z$ is a *transitive dependency* if there exists an attribute set $Y$ such that:
$$X \to Y, \quad Y \not\to X, \quad Y \to Z$$
where:
- $X$ is a candidate key,
- $Y$ is not a candidate key (nor a superkey), and
- $Z$ is a non-prime attribute ($Z \notin \text{Prime}(R)$) with $Z \not\subseteq Y$.

---

## 2. The 2NF Starting Structures

From the 2NF normalization stage in [`normalization/2nf.md`](./2nf.md), consider the three key relations that satisfy 2NF but retain transitive dependencies:

### 2.1. Relation 1: `ceremonies_2nf`
$$\text{ceremonies\_2nf}(\underline{\text{ceremony\_id}}, \text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{venue\_name}, \text{city}, \text{state}, \text{max\_seating\_capacity}, \text{primary\_network})$$
- Primary Key: $\text{ceremony\_id}$
- Prime Attributes: $\{\text{ceremony\_id}\}$
- Non-Prime Attributes: All remaining 9 attributes.

### 2.2. Relation 2: `nominated_works_2nf`
$$\text{nominated\_works\_2nf}(\underline{\text{work\_id}}, \text{work\_title}, \text{work\_type}, \text{commercial\_release\_date}, \text{label\_id}, \text{label\_name}, \text{parent\_music\_group})$$
- Primary Key: $\text{work\_id}$
- Prime Attributes: $\{\text{work\_id}\}$
- Non-Prime Attributes: All remaining 6 attributes.

### 2.3. Relation 3: `award_categories_2nf`
$$\text{award\_categories\_2nf}(\underline{\text{category\_id}}, \text{category\_name}, \text{standard\_short\_code}, \text{field\_id}, \text{field\_name}, \text{field\_abbreviation})$$
- Primary Key: $\text{category\_id}$
- Prime Attributes: $\{\text{category\_id}\}$
- Non-Prime Attributes: All remaining 5 attributes.

---

## 3. Identification of 3NF Violations (Transitive Dependencies)

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   TRANSITIVE DEPENDENCY VIOLATION AUDIT                                │
├─────┬──────────────────────┬──────────────────────────────────────────┬────────────────────────────────┤
│ No. │ 2NF Relation         │ Transitive Dependency Chain (X → Y → Z)  │ Violation Rationale            │
├─────┼──────────────────────┼──────────────────────────────────────────┼────────────────────────────────┤
│ T1  │ ceremonies_2nf       │ ceremony_id → venue_id                   │ venue_id is NOT a superkey;    │
│     │                      │ venue_id → venue_name, city, capacity    │ venue_name, city, capacity are │
│     │                      │ venue_id ↛ ceremony_id                   │ NOT prime attributes.          │
├─────┼──────────────────────┼──────────────────────────────────────────┼────────────────────────────────┤
│ T2  │ nominated_works_2nf  │ work_id → label_id                       │ label_id is NOT a superkey;    │
│     │                      │ label_id → label_name, parent_group      │ label_name, parent_group are   │
│     │                      │ label_id ↛ work_id                       │ NOT prime attributes.          │
├─────┼──────────────────────┼──────────────────────────────────────────┼────────────────────────────────┤
│ T3  │ award_categories_2nf │ category_id → field_id                   │ field_id is NOT a superkey;    │
│     │                      │ field_id → field_name, abbreviation      │ field_name, abbreviation are   │
│     │                      │ field_id ↛ category_id                   │ NOT prime attributes.          │
└─────┴──────────────────────┴──────────────────────────────────────────┴────────────────────────────────┘
```

### 3.1. Concrete Operational Anomalies Caused by Transitive Dependencies:
1. **Redundancy & Storage Waste**:
   Crypto.com Arena's seating capacity ($20,000$), street address, and host city are repeated across 21 ceremonies. For an archive with 67 ceremonies, venue metadata is duplicated dozens of times.
2. **Update Anomaly**:
   If Columbia Records changes its corporate parent from "Sony Music Entertainment" to an independent entity, every single nominated work ever released by Columbia Records must be located and updated across thousands of historical records.
3. **Insertion Anomaly**:
   A newly constructed music venue (e.g., Intuit Dome in Inglewood) cannot be added to the database until the Recording Academy contracts and stages an actual telecast ceremony there.
4. **Deletion Anomaly**:
   If the sole ceremony hosted at a historic hotel ballroom (e.g., Beverly Hilton in 1959) is removed for archival re-indexing, all physical data concerning that historic venue is permanently deleted from the database.

---

## 4. 3NF Decomposition (Bernstein Synthesis Algorithm)

To eliminate all transitive dependencies, we apply the **Bernstein 3NF Synthesis Algorithm** (formulated by Philip A. Bernstein, 1976):
For each transitive dependency $X \to Y$ and $Y \to Z$:
1. Create a relation with attributes $Y \cup Z$ with $Y$ as primary key.
2. Retain $X \cup Y$ in the original relation, where $Y$ acts as a foreign key referencing the newly created relation.

### 4.1. Decomposed 3NF Schemas:

#### Case 1: Decomposing `ceremonies_2nf`
- **`venues`**:
  $$\text{venues}(\underline{\text{venue\_id}}, \text{venue\_name}, \text{city}, \text{state}, \text{max\_seating\_capacity})$$
  - Functional Dependency: $\text{venue\_id} \to \text{venue\_name}, \text{city}, \text{state}, \text{max\_seating\_capacity}$.
  - Determinant $\text{venue\_id}$ is a **superkey**. $\implies$ **3NF Satisfied**.
- **`ceremonies`**:
  $$\text{ceremonies}(\underline{\text{ceremony\_id}}, \text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{primary\_network})$$
  - Functional Dependency: $\text{ceremony\_id} \to \text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{primary\_network}$.
  - Determinant $\text{ceremony\_id}$ is a **superkey**. $\implies$ **3NF Satisfied**.

---

#### Case 2: Decomposing `nominated_works_2nf`
- **`record_labels`**:
  $$\text{record\_labels}(\underline{\text{label\_id}}, \text{label\_name}, \text{parent\_music\_group})$$
  - Functional Dependency: $\text{label\_id} \to \text{label\_name}, \text{parent\_music\_group}$.
  - Determinant $\text{label\_id}$ is a **superkey**. $\implies$ **3NF Satisfied**.
- **`nominated_works`**:
  $$\text{nominated\_works}(\underline{\text{work\_id}}, \text{work\_title}, \text{work\_type}, \text{commercial\_release\_date}, \text{label\_id})$$
  - Functional Dependency: $\text{work\_id} \to \text{work\_title}, \text{work\_type}, \text{commercial\_release\_date}, \text{label\_id}$.
  - Determinant $\text{work\_id}$ is a **superkey**. $\implies$ **3NF Satisfied**.

---

#### Case 3: Decomposing `award_categories_2nf`
- **`award_fields`**:
  $$\text{award\_fields}(\underline{\text{field\_id}}, \text{field\_name}, \text{field\_abbreviation})$$
  - Functional Dependency: $\text{field\_id} \to \text{field\_name}, \text{field\_abbreviation}$.
  - Determinant $\text{field\_id}$ is a **superkey**. $\implies$ **3NF Satisfied**.
- **`award_categories`**:
  $$\text{award\_categories}(\underline{\text{category\_id}}, \text{category\_name}, \text{standard\_short\_code}, \text{field\_id})$$
  - Functional Dependency: $\text{category\_id} \to \text{category\_name}, \text{standard\_short\_code}, \text{field\_id}$.
  - Determinant $\text{category\_id}$ is a **superkey**. $\implies$ **3NF Satisfied**.

---

## 5. Formal Proofs of Decomposition Validity

### 5.1. Lossless-Join Decomposition Proof
We verify Heath's Theorem for the decomposition of `ceremonies_2nf` into $R_1 = \text{ceremonies}$ and $R_2 = \text{venues}$:
1. Shared attributes:
   $$R_1 \cap R_2 = \{ \text{venue\_id} \}$$
2. Attributes exclusive to $R_2$:
   $$R_2 - R_1 = \{ \text{venue\_name}, \text{city}, \text{state}, \text{max\_seating\_capacity} \}$$
3. Dependency check:
   $$\text{venue\_id} \to \text{venue\_name}, \text{city}, \text{state}, \text{max\_seating\_capacity} \in F^+$$
4. Because $(R_1 \cap R_2) \to (R_2 - R_1)$ holds, the natural join:
   $$\text{ceremonies} \bowtie_{\text{venue\_id}} \text{venues} \equiv \text{ceremonies\_2nf}$$
   is **guaranteed to be Lossless**. Zero spurious tuples can be produced.

The identical proof holds for $\text{nominated\_works} \bowtie_{\text{label\_id}} \text{record\_labels}$ and $\text{award\_categories} \bowtie_{\text{field\_id}} \text{award\_fields}$.

---

### 5.2. Dependency Preservation Proof
Let $F$ be the set of dependencies on the undecomposed schema:
- Dependency $\text{ceremony\_id} \to \text{venue\_id}$ is embedded in $\text{ceremonies}$.
- Dependency $\text{venue\_id} \to \text{venue\_name}, \text{city}, \text{capacity}$ is embedded in $\text{venues}$.
- Transitive dependency $\text{ceremony\_id} \to \text{venue\_name}$ is logically implied by transitivity ($F^+$).
- Dependency $\text{category\_id} \to \text{field\_id}$ is preserved in $\text{award\_categories}$.
- Dependency $\text{field\_id} \to \text{field\_name}$ is preserved in $\text{award\_fields}$.
- Dependency $\text{work\_id} \to \text{label\_id}$ is preserved in $\text{nominated\_works}$.
- Dependency $\text{label\_id} \to \text{label\_name}$ is preserved in $\text{record\_labels}$.

$$\bigcup \pi_{R_i}(F) \equiv F^+$$

Every functional dependency in the original schema is enforceable locally on a single relation without computing joins.

$$\therefore \text{ The 3NF decomposition is 100\% Dependency-Preserving!}$$

---

## 6. Keys and Dependencies Summary in 3NF

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   3NF RELATIONAL SPECIFICATION SUMMARY                                 │
├─────────────────────┬──────────────────────┬──────────────────────┬────────────────────────────────────┤
│ 3NF Relation Name   │ Primary Key (PK)     │ Foreign Key(s) (FK)  │ Canonical Functional Dependencies  │
├─────────────────────┼──────────────────────┼──────────────────────┼────────────────────────────────────┤
│ venues              │ venue_id             │ None                 │ venue_id → venue_name, city, cap   │
│ ceremonies          │ ceremony_id          │ venue_id → venues    │ ceremony_id → edition, venue_id    │
│ award_fields        │ field_id             │ None                 │ field_id → field_name, abbrev      │
│ award_categories    │ category_id          │ field_id → fields    │ category_id → cat_name, field_id   │
│ record_labels       │ label_id             │ None                 │ label_id → label_name, parent_grp  │
│ nominated_works     │ work_id              │ label_id → labels    │ work_id → work_title, label_id     │
│ creators            │ creator_id           │ None                 │ creator_id → stage_name, country   │
│ nomination_entries  │ nomination_id        │ ceremony, cat, work  │ nomination_id → cer, cat, work     │
│ nomination_credits  │ credit_id            │ nom_id, creator_id   │ credit_id → contribution_pct       │
└─────────────────────┴──────────────────────┴──────────────────────┴────────────────────────────────────┘
```

All 9 decomposed core relations satisfy **Third Normal Form (3NF)** with zero transitive dependencies.
