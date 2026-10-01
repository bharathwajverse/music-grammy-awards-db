# Module 3: Higher Normal Forms (3NF, BCNF, 4NF, 5NF) & Decomposition Proofs

This document presents the formal mathematical proofs for decomposing relational schemas through Third Normal Form (3NF), Boyce-Codd Normal Form (BCNF), Fourth Normal Form (4NF), and Fifth Normal Form (5NF), accompanied by lossless-join and dependency-preservation proofs.

---

## 1. Third Normal Form (3NF)

### 1.1 Definition:
A relation $R$ is in 3NF with respect to a set of functional dependencies $F$ if and only if:
1. $R$ is in 2NF.
2. For every non-trivial functional dependency $X \to A \in F^+$, at least one of the following holds:
   - $X$ is a superkey of $R$, **OR**
   - $A$ is a prime attribute (i.e., $A$ is a member of some candidate key of $R$).

### 1.2 Transitive Dependency Violation Analysis:
Consider the relation:
$$R_{\text{cat}}(\text{category\_id}, \text{official\_category\_name}, \text{field\_id}, \text{field\_name})$$

Candidate Key: $\text{category\_id}$
Functional Dependencies:
1. $\text{category\_id} \to \text{field\_id}$
2. $\text{field\_id} \to \text{field\_name}$

From (1) and (2), we derive the transitive dependency:
$$\text{category\_id} \to \text{field\_name}$$

In $\text{field\_id} \to \text{field\_name}$:
- $\text{field\_id}$ is NOT a superkey of $R_{\text{cat}}$.
- $\text{field\_name}$ is NOT a prime attribute.

This violates 3NF.

### 1.3 3NF Decomposition:
We decompose $R_{\text{cat}}$ into:
1. $R_{\text{category}}(\underline{\text{category\_id}}, \text{official\_category\_name}, \text{field\_id})$ (Key: $\text{category\_id}$)
2. $R_{\text{field}}(\underline{\text{field\_id}}, \text{field\_name})$ (Key: $\text{field\_id}$)

In both relations, every determinant is a superkey. Therefore, both relations satisfy 3NF.

---

## 2. Boyce-Codd Normal Form (BCNF)

### 2.1 Definition:
A relation $R$ is in BCNF if for every non-trivial functional dependency $X \to A \in F^+$, $X$ is a **superkey** of $R$.
*(BCNF eliminates the exception where $A$ is permitted to be a prime attribute).*

### 2.2 Case Study: The Ceremony Ballot Tabulation Relation
Consider an accounting tabulation relation where auditors from accounting firms (PwC / Deloitte) certify categories:
$$R_{\text{audit}}(\text{ceremony\_id}, \text{category\_id}, \text{lead\_auditor\_name})$$

Rules:
- For each ceremony and category, there is exactly one lead auditor:
  $$\text{ceremony\_id}, \text{category\_id} \to \text{lead\_auditor\_name}$$
- Each lead auditor is assigned to supervise at most one ceremony, but may audit multiple categories within that ceremony:
  $$\text{lead\_auditor\_name} \to \text{ceremony\_id}$$

Candidate Keys:
1. $K_1 = \{ \text{ceremony\_id}, \text{category\_id} \}$
2. $K_2 = \{ \text{lead\_auditor\_name}, \text{category\_id} \}$

Prime Attributes: $\text{ceremony\_id}, \text{category\_id}, \text{lead\_auditor\_name}$.

#### Evaluating 3NF vs BCNF:
In $\text{lead\_auditor\_name} \to \text{ceremony\_id}$:
- $\text{lead\_auditor\_name}$ is NOT a superkey (it cannot determine $\text{category\_id}$).
- However, $\text{ceremony\_id}$ is a prime attribute (part of $K_1$).
- Therefore, $R_{\text{audit}}$ is in **3NF**.
- **However, it is NOT in BCNF** because $\text{lead\_auditor\_name}$ is not a superkey.

#### BCNF Decomposition:
Decompose $R_{\text{audit}}$ into:
1. $R_{a1}(\underline{\text{lead\_auditor\_name}}, \text{ceremony\_id})$ (Key: $\text{lead\_auditor\_name}$)
2. $R_{a2}(\underline{\text{lead\_auditor\_name}, \text{category\_id}})$ (Key: $\{\text{lead\_auditor\_name}, \text{category\_id}\}$)

Both relations are strictly in BCNF.

---

## 3. Lossless-Join & Dependency Preservation Proofs

### 3.1 Lossless-Join Decomposition Theorem:
A decomposition of $R$ into $R_1$ and $R_2$ is **lossless** with respect to $F$ if and only if:
$$(R_1 \cap R_2) \to (R_1 - R_2) \in F^+ \quad\text{OR}\quad (R_1 \cap R_2) \to (R_2 - R_1) \in F^+$$
*(i.e., the common attributes must form a superkey of at least one of the decomposed relations).*

#### Proof for $R_{\text{cat}} \to R_{\text{category}} \cup R_{\text{field}}$:
- $R_{\text{category}} \cap R_{\text{field}} = \{ \text{field\_id} \}$
- $R_{\text{field}} - R_{\text{category}} = \{ \text{field\_name} \}$
- From $F$, $\text{field\_id} \to \text{field\_name} \in F^+$.
- Because $\{ \text{field\_id} \} \to \{ \text{field\_name} \}$, the condition holds.
- **Conclusion**: The decomposition is **guaranteed lossless**.

### 3.2 Dependency Preservation:
A decomposition $D = \{ R_1, R_2, \dots, R_k \}$ is **dependency-preserving** if:
$$\left( \bigcup_{i=1}^k \pi_{R_i}(F) \right)^+ = F^+$$

In the decomposition $R_{\text{cat}} \to R_{\text{category}} \cup R_{\text{field}}$:
- $\pi_{R_{\text{category}}}(F)$ preserves $\text{category\_id} \to \text{field\_id}$.
- $\pi_{R_{\text{field}}}(F)$ preserves $\text{field\_id} \to \text{field\_name}$.
- All original dependencies are preserved without requiring a cross-table join.

---

## 4. Fourth Normal Form (4NF) & Multivalued Dependencies

### 4.1 Definition:
A multivalued dependency (MVD) $X \twoheadrightarrow Y$ holds on $R$ if, given values for $X$, the set of values for $Y$ is independent of the values of the remaining attributes $R - (X \cup Y)$.

A relation $R$ is in **4NF** with respect to a set of MVDs $M$ if, for every non-trivial MVD $X \twoheadrightarrow Y \in M^+$, $X$ is a **superkey** of $R$.

### 4.2 Case Study: Independent Multivalued Attributes in Creator Profiling
Consider an artist profile relation:
$$R_{\text{artist}}(\text{creator\_id}, \text{subgenre}, \text{record\_label\_affil})$$

An artist (e.g., Quincy Jones or Paul McCartney) performs across multiple independent musical subgenres (Jazz, Pop, Soundtrack) and simultaneously works with multiple independent record labels (Epic, Columbia, Parlophone).
- Knowledge of a creator's subgenre imparts zero information about their contracted record label.
- Therefore, the following non-trivial MVDs hold:
  1. $\text{creator\_id} \twoheadrightarrow \text{subgenre}$
  2. $\text{creator\_id} \twoheadrightarrow \text{record\_label\_affil}$

Candidate Key: $\{ \text{creator\_id}, \text{subgenre}, \text{record\_label\_affil} \}$

In $\text{creator\_id} \twoheadrightarrow \text{subgenre}$:
- $\text{creator\_id}$ is NOT a superkey.
- This creates massive tuple redundancy (Cartesian product of genres $\times$ labels).

#### 4NF Decomposition:
Decompose $R_{\text{artist}}$ into:
1. $R_{\text{genre}}(\underline{\text{creator\_id}, \text{subgenre}})$
2. $R_{\text{label}}(\underline{\text{creator\_id}, \text{record\_label\_affil}})$

In both relations, the left-hand side is a superkey of the respective projection. Both relations are strictly in **4NF**.

---

## 5. Fifth Normal Form (5NF / Project-Join Normal Form)

### 5.1 Definition:
A relation $R$ is in **5NF** (or Project-Join Normal Form, PJNF) if and only if every non-trivial join dependency $\bowtie[R_1, R_2, \dots, R_k]$ on $R$ is implied by the candidate keys of $R$.

### 5.2 Case Study: Ternary Association in Collaborative Production
Consider a ternary relation tracking which producers produce tracks for artists on specific record labels:
$$R_{\text{collab}}(\text{producer\_id}, \text{artist\_id}, \text{label\_id})$$

Suppose the following industry constraint holds:
*"Whenever producer $P$ produces for artist $A$, and artist $A$ is signed to label $L$, and producer $P$ is contracted by label $L$, then producer $P$ produces for artist $A$ on label $L$."*

This introduces a cyclic join dependency:
$$\bowtie[\;(\text{producer\_id}, \text{artist\_id}),\; (\text{artist\_id}, \text{label\_id}),\; (\text{producer\_id}, \text{label\_id})\;]$$

This join dependency cannot be factored into two 4NF components without causing spurious tuples upon a binary join; it can only be reconstructed losslessly by a three-way join.

#### 5NF Decomposition:
Decompose $R_{\text{collab}}$ into three binary projections:
1. $R_1(\underline{\text{producer\_id}, \text{artist\_id}})$
2. $R_2(\underline{\text{artist\_id}, \text{label\_id}})$
3. $R_3(\underline{\text{producer\_id}, \text{label\_id}})$

Now, the relation cannot be decomposed further without loss. This decomposition satisfies **5NF**.
