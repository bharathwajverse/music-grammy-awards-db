# Second Normal Form (2NF) Specification & Transformation

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 9 — Schema Normalization Proofs  
> **Document**: Second Normal Form (2NF) Formal Definition, Partial Functional Dependency Identification, Lossless Decomposition, and Dependency Preservation Proofs  
> **Status**: Completed  
> **Theoretical Framework**: E.F. Codd (1971) / Elmasri & Navathe (*Fundamentals of Database Systems*, 7th Edition, Chapter 14)  
> **Related Artifacts**:  
> - 1NF Baseline: [`normalization/1nf.md`](./1nf.md)  
> - 3NF Transformation: [`normalization/3nf.md`](./3nf.md)  
> - Functional Dependencies: [`normalization/functional-dependencies.md`](./functional-dependencies.md)  
> - Normalization Summary: [`normalization/normalization-summary.md`](./normalization-summary.md)  

---

## 1. Formal Theoretical Definition of Second Normal Form (2NF)

According to E.F. Codd (1971):
> A relation schema $R$ is in **Second Normal Form (2NF)** if and only if it is in **First Normal Form (1NF)** and **every non-prime attribute $A \in R$ is fully functionally dependent on every candidate key $K$ of $R$**.

### 1.1. Core Mathematical Definitions:
1. **Full Functional Dependency**: A functional dependency $X \to Y$ is a *full functional dependency* if removal of any attribute $A$ from $X$ means that the dependency does not hold any longer:
   $$\forall A \in X, \quad (X - \{A\}) \not\to Y$$
2. **Partial Functional Dependency**: A dependency $X \to Y$ is a *partial dependency* if there exists some attribute $A \in X$ such that $(X - \{A\}) \to Y$. That is:
   $$X' \subset K \quad\text{and}\quad X' \to Y \quad (\text{where } Y \notin \text{Prime}(R))$$
3. **2NF Criterion**: A relation is in 2NF if it contains **zero partial dependencies of non-prime attributes on any candidate key**.

> **Note**: Any relation schema whose candidate keys are all single-attribute (simple) keys is **automatically in 2NF**, because no proper subset of a single attribute exists. 2NF violations occur exclusively in relations possessing composite candidate keys.

---

## 2. The 1NF Starting Structure ($\mathcal{R}_{\text{1NF\_FLAT}}$)

The baseline relation resulting from First Normal Form atomicity flattening is:

$$\mathcal{R}_{\text{1NF\_FLAT}}(\underline{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{creator\_id}, \text{credit\_role}},$$
$$\text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{venue\_name}, \text{city}, \text{state}, \text{max\_seating\_capacity}, \text{primary\_network},$$
$$\text{category\_name}, \text{standard\_short\_code}, \text{field\_id}, \text{field\_name},$$
$$\text{work\_title}, \text{work\_type}, \text{commercial\_release\_date}, \text{label\_id}, \text{label\_name},$$
$$\text{creator\_legal\_name}, \text{stage\_name}, \text{country\_of\_citizenship}, \text{contribution\_percentage},$$
$$\text{nomination\_id}, \text{ballot\_slot\_order}, \text{is\_winner\_flag})$$

### 2.1. Candidate Keys for $\mathcal{R}_{\text{1NF\_FLAT}}$:
- Primary Candidate Key:
  $$K_1 = \{ \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{creator\_id}, \text{credit\_role} \}$$
- Alternate Candidate Key:
  $$K_2 = \{ \text{nomination\_id}, \text{creator\_id}, \text{credit\_role} \}$$

### 2.2. Prime Attributes:
$$\text{Prime}(\mathcal{R}_{\text{1NF\_FLAT}}) = \{ \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{creator\_id}, \text{credit\_role}, \text{nomination\_id} \}$$

### 2.3. Non-Prime Attributes:
All remaining 24 attributes ($\text{edition\_number}, \text{venue\_id}, \text{venue\_name}, \text{category\_name}, \text{work\_title}, \text{stage\_name}, \text{contribution\_percentage}, \dots$).

---

## 3. Identification of 2NF Violations (Partial Dependencies)

We audit all non-prime attributes against proper subsets of candidate keys $K_1$ and $K_2$:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   PARTIAL DEPENDENCY VIOLATION AUDIT                                   │
├─────┬────────────────────────────────────────────────┬──────────────────────────┬──────────────────────┤
│ No. │ Partial Dependency (X → Y)                     │ Proper Subset of Key (X) │ Non-Prime Dependent  │
├─────┼────────────────────────────────────────────────┼──────────────────────────┼──────────────────────┤
│ P1  │ ceremony_id → edition_number, ceremony_date,   │ {ceremony_id} ⊂ K_1      │ edition_number,      │
│     │ broadcast_year, venue_id, primary_network      │                          │ venue_id, etc.       │
├─────┼────────────────────────────────────────────────┼──────────────────────────┼──────────────────────┤
│ P2  │ category_id → category_name,                   │ {category_id} ⊂ K_1      │ category_name,       │
│     │ standard_short_code, field_id                  │                          │ field_id, etc.       │
├─────┼────────────────────────────────────────────────┼──────────────────────────┼──────────────────────┤
│ P3  │ work_id → work_title, work_type,               │ {work_id} ⊂ K_1          │ work_title,          │
│     │ commercial_release_date, label_id              │                          │ label_id, etc.       │
├─────┼────────────────────────────────────────────────┼──────────────────────────┼──────────────────────┤
│ P4  │ creator_id → creator_legal_name, stage_name,   │ {creator_id} ⊂ K_1, K_2  │ creator_legal_name,  │
│     │ country_of_citizenship                         │                          │ stage_name, etc.     │
├─────┼────────────────────────────────────────────────┼──────────────────────────┼──────────────────────┤
│ P5  │ ceremony_id, category_id, work_id →            │ {ceremony, cat, wrk} ⊂   │ ballot_slot_order,   │
│     │ ballot_slot_order, is_winner_flag              │ K_1                      │ is_winner_flag       │
├─────┼────────────────────────────────────────────────┼──────────────────────────┼──────────────────────┤
│ P6  │ nomination_id → ballot_slot_order,             │ {nomination_id} ⊂ K_2    │ ballot_slot_order,   │
│     │ is_winner_flag, ceremony_id, category_id, work │                          │ is_winner_flag       │
└─────┴────────────────────────────────────────────────┴──────────────────────────┴──────────────────────┘
```

Only **one** non-prime attribute is fully dependent on the entire composite key:
$$\{ \text{nomination\_id}, \text{creator\_id}, \text{credit\_role} \} \to \text{contribution\_percentage}$$

All other non-prime attributes violate 2NF!

### 3.1. Concrete Operational Anomalies Caused by Partial Dependencies:
- **Redundancy Anomaly**: The Album of the Year title `"Renaissance"` is stored repeatedly for every single credited producer, mixing engineer, songwriter, and arranger associated with the album (over 40 duplicate rows).
- **Insertion Anomaly**: If the Recording Academy establishes a new category (`CAT_AFROBEATS_ALBUM`) before receiving any certified nominations or creator submissions, that category cannot be inserted into $\mathcal{R}_{\text{1NF\_FLAT}}$ because $\text{work\_id}$, $\text{creator\_id}$, and $\text{credit\_role}$ would be NULL, violating Entity Integrity.
- **Deletion Anomaly**: If all craft credits for an independent record are temporarily withdrawn during an eligibility audit, deleting the rows deletes the existence of the ceremony telecast itself if no other nominations are recorded in that slice.

---

## 4. 2NF Decomposition Transformation

To eliminate all partial dependencies, we apply **2NF Projection Decomposition**:
For each partial dependency $X \to Y$, we remove $Y$ from the composite relation and create a new relation $R_{XY}(X, Y)$ with $X$ as primary key.

### 4.1. Decomposed 2NF Relational Schema:

1. **`ceremonies_2nf`**:
   $$\text{ceremonies\_2nf}(\underline{\text{ceremony\_id}}, \text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{venue\_name}, \text{city}, \text{state}, \text{max\_seating\_capacity}, \text{primary\_network})$$
   - Key: $\text{ceremony\_id}$ (Simple Key $\implies$ automatically 2NF).

2. **`award_categories_2nf`**:
   $$\text{award\_categories\_2nf}(\underline{\text{category\_id}}, \text{category\_name}, \text{standard\_short\_code}, \text{field\_id}, \text{field\_name})$$
   - Key: $\text{category\_id}$ (Simple Key $\implies$ automatically 2NF).

3. **`nominated_works_2nf`**:
   $$\text{nominated\_works\_2nf}(\underline{\text{work\_id}}, \text{work\_title}, \text{work\_type}, \text{commercial\_release\_date}, \text{label\_id}, \text{label\_name})$$
   - Key: $\text{work\_id}$ (Simple Key $\implies$ automatically 2NF).

4. **`creators_2nf`**:
   $$\text{creators\_2nf}(\underline{\text{creator\_id}}, \text{creator\_legal\_name}, \text{stage\_name}, \text{country\_of\_citizenship})$$
   - Key: $\text{creator\_id}$ (Simple Key $\implies$ automatically 2NF).

5. **`nomination_entries_2nf`**:
   $$\text{nomination\_entries\_2nf}(\underline{\text{nomination\_id}}, \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{ballot\_slot\_order}, \text{is\_winner\_flag})$$
   - Candidate Keys: $\{\text{nomination\_id}\}$ and $\{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}\}$.
   - Non-prime attributes $\text{ballot\_slot\_order}$ and $\text{is\_winner\_flag}$ depend on the *entire* candidate key.

6. **`nomination_credits_2nf`**:
   $$\text{nomination\_credits\_2nf}(\underline{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}}, \text{contribution\_percentage})$$
   - Composite Key: $\{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}\}$.
   - Non-prime attribute $\text{contribution\_percentage}$ depends on all three attributes. Fully functionally dependent!

---

## 5. Formal Proofs of Decomposition Validity

### 5.1. Lossless-Join Decomposition Proof (Heath's Theorem)
A binary decomposition of relation $R$ into $R_1$ and $R_2$ is **guaranteed lossless** if and only if the intersection of their attribute sets forms a superkey of at least one of the decomposed relations:
$$(R_1 \cap R_2) \to (R_1 - R_2) \in F^+ \quad\lor\quad (R_1 \cap R_2) \to (R_2 - R_1) \in F^+$$

#### Proof for $\mathcal{R}_{\text{1NF\_FLAT}} \implies \text{nomination\_entries\_2nf} \bowtie \text{nomination\_credits\_2nf}$:
1. Let $R_1 = \text{nomination\_entries\_2nf}$ and $R_2 = \text{nomination\_credits\_2nf}$.
2. Common attributes:
   $$R_1 \cap R_2 = \{ \text{nomination\_id} \}$$
3. Attributes in $R_1 - R_2$:
   $$R_1 - R_2 = \{ \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{ballot\_slot\_order}, \text{is\_winner\_flag} \}$$
4. From functional dependency set $F$, we have:
   $$\text{nomination\_id} \to \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{ballot\_slot\_order}, \text{is\_winner\_flag}$$
5. Therefore:
   $$(R_1 \cap R_2) \to (R_1 - R_2) \in F^+$$
6. $\text{nomination\_id}$ is a candidate key of $R_1$.

$$\therefore \text{ The decomposition is guaranteed Lossless!}$$

---

### 5.2. Dependency Preservation Proof
A decomposition $D = \{ R_1, R_2, \dots, R_k \}$ is **dependency-preserving** if the union of the projections of the functional dependencies onto each relation preserves the original dependency closure:
$$\left( \bigcup_{i=1}^k \pi_{R_i}(F) \right)^+ = F^+$$

#### Verification across Decomposed Relations:
- $\pi_{\text{ceremonies}}(F)$ preserves $FD_1: \text{ceremony\_id} \to \text{edition\_number}, \text{ceremony\_date}, \dots$
- $\pi_{\text{categories}}(F)$ preserves $FD_3: \text{category\_id} \to \text{category\_name}, \dots$
- $\pi_{\text{works}}(F)$ preserves $FD_5: \text{work\_id} \to \text{work\_title}, \dots$
- $\pi_{\text{creators}}(F)$ preserves $FD_7: \text{creator\_id} \to \text{stage\_name}, \dots$
- $\pi_{\text{nominations}}(F)$ preserves $FD_8: \text{nomination\_id} \to \text{ceremony\_id}, \dots$ and $FD_9: \{\text{ceremony}, \text{cat}, \text{work}\} \to \text{nomination\_id}$
- $\pi_{\text{credits}}(F)$ preserves $FD_{10}: \{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}\} \to \text{contribution\_percentage}$

Every dependency in the original set $F$ is directly verifiable within an individual decomposed relation without requiring multi-table joins.

$$\therefore \text{ The 2NF decomposition is 100\% Dependency-Preserving!}$$

---

## 6. Remaining Violations: The Need for 3NF

Although all relations in Section 4 satisfy Second Normal Form, they still contain **Transitive Dependencies**:
- In $\text{ceremonies\_2nf}$: $\text{ceremony\_id} \to \text{venue\_id}$ and $\text{venue\_id} \to \text{venue\_name}, \text{city}, \text{max\_seating\_capacity}$.
- In $\text{nominated\_works\_2nf}$: $\text{work\_id} \to \text{label\_id}$ and $\text{label\_id} \to \text{label\_name}$.
- In $\text{award\_categories\_2nf}$: $\text{category\_id} \to \text{field\_id}$ and $\text{field\_id} \to \text{field\_name}$.

These transitive dependencies violate **Third Normal Form (3NF)** and will be decomposed in the next stage.
