# Module 2: Functional Dependencies, Schema Refinement & 1NF/2NF

This document details the mathematical derivation of functional dependencies (FDs), attribute closures, minimal covers, candidate key determination, and normal form transformations (1NF and 2NF) for the **GRAMMY Awards Information & Analytics System**.

---

## 1. Initial Universal Relation: The Unnormalized GRAMMY Flat Schema

Consider the flat, unnormalized relation representing raw GRAMMY telecast and nomination data before database normalization:

$$\mathcal{R}(\text{ceremony\_id}, \text{edition}, \text{ceremony\_date}, \text{venue\_id}, \text{venue\_name}, \text{venue\_city}, \text{venue\_cap}, \text{category\_id}, \text{cat\_name}, \text{field\_id}, \text{field\_name}, \text{work\_id}, \text{work\_title}, \text{artist\_id}, \text{artist\_name}, \text{artist\_country}, \text{label\_id}, \text{label\_name}, \text{credit\_role}, \text{is\_winner}, \text{rating\_millions})$$

---

## 2. Formal Functional Dependency Set ($F$)

Based on the real-world domain semantics of the Recording Academy, the following functional dependencies hold:

1. $FD_1: \text{ceremony\_id} \to \text{edition}, \text{ceremony\_date}, \text{venue\_id}, \text{rating\_millions}$
2. $FD_2: \text{edition} \to \text{ceremony\_id}, \text{ceremony\_date}, \text{venue\_id}$
3. $FD_3: \text{venue\_id} \to \text{venue\_name}, \text{venue\_city}, \text{venue\_cap}$
4. $FD_4: \text{category\_id} \to \text{cat\_name}, \text{field\_id}$
5. $FD_5: \text{field\_id} \to \text{field\_name}$
6. $FD_6: \text{work\_id} \to \text{work\_title}, \text{label\_id}$
7. $FD_7: \text{label\_id} \to \text{label\_name}$
8. $FD_8: \text{artist\_id} \to \text{artist\_name}, \text{artist\_country}$
9. $FD_9: \text{ceremony\_id}, \text{category\_id}, \text{work\_id} \to \text{artist\_id}, \text{is\_winner}$
10. $FD_{10}: \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{artist\_id}, \text{credit\_role} \to \text{is\_winner}$

---

## 3. Armstrong's Axioms & Attribute Closures

### 3.1 Axioms Applied:
1. **Reflexivity**: If $Y \subseteq X$, then $X \to Y$.
2. **Augmentation**: If $X \to Y$, then $XZ \to YZ$.
3. **Transitivity**: If $X \to Y$ and $Y \to Z$, then $X \to Z$.
4. **Decomposition**: If $X \to YZ$, then $X \to Y$ and $X \to Z$.
5. **Union**: If $X \to Y$ and $X \to Z$, then $X \to YZ$.
6. **Pseudo-transitivity**: If $X \to Y$ and $WY \to Z$, then $WX \to Z$.

### 3.2 Computation of Attribute Closures:

#### Closure of $\text{ceremony\_id}^+$:
$$\text{ceremony\_id}^+ = \{ \text{ceremony\_id}, \text{edition}, \text{ceremony\_date}, \text{venue\_id}, \text{rating\_millions}, \text{venue\_name}, \text{venue\_city}, \text{venue\_cap} \}$$
*(Derived via Transitivity through $\text{venue\_id} \to \text{venue\_name, city, cap}$)*.

#### Closure of $\text{work\_id}^+$:
$$\text{work\_id}^+ = \{ \text{work\_id}, \text{work\_title}, \text{label\_id}, \text{label\_name} \}$$
*(Derived via Transitivity through $\text{label\_id} \to \text{label\_name}$)*.

#### Candidate Key Determination for $\mathcal{R}$:
To determine the candidate key of the universal relation $\mathcal{R}$, we calculate the closure of the composite attribute set:
$$K = \{ \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{credit\_role} \}$$

$$K^+ = \mathcal{R}$$

Because no proper subset of $K$ determines all attributes in $\mathcal{R}$, $K = \{ \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{credit\_role} \}$ is a **minimal candidate key**.

---

## 4. Minimal Cover ($F_{min}$) Derivation

A set of functional dependencies $F_{min}$ is in minimal cover if:
1. Every dependency in $F_{min}$ has a single attribute on its right-hand side (canonical form).
2. No attribute on the left-hand side of any dependency is extraneous.
3. No dependency in $F_{min}$ is redundant.

### Step 1: Right-Hand Side Decomposition
- $\text{ceremony\_id} \to \text{edition}$
- $\text{ceremony\_id} \to \text{ceremony\_date}$
- $\text{ceremony\_id} \to \text{venue\_id}$
- $\text{ceremony\_id} \to \text{rating\_millions}$
- $\text{venue\_id} \to \text{venue\_name}$
- $\text{venue\_id} \to \text{venue\_city}$
- $\text{venue\_id} \to \text{venue\_cap}$
- $\text{category\_id} \to \text{cat\_name}$
- $\text{category\_id} \to \text{field\_id}$
- $\text{field\_id} \to \text{field\_name}$
- $\text{work\_id} \to \text{work\_title}$
- $\text{work\_id} \to \text{label\_id}$
- $\text{label\_id} \to \text{label\_name}$
- $\text{artist\_id} \to \text{artist\_name}$
- $\text{artist\_id} \to \text{artist\_country}$
- $\text{ceremony\_id}, \text{category\_id}, \text{work\_id} \to \text{artist\_id}$
- $\text{ceremony\_id}, \text{category\_id}, \text{work\_id} \to \text{is\_winner}$

### Step 2: Elimination of Extraneous Attributes
Consider $FD_{10}: \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{artist\_id}, \text{credit\_role} \to \text{is\_winner}$.
Because $\text{ceremony\_id}, \text{category\_id}, \text{work\_id} \to \text{is\_winner}$, both $\text{artist\_id}$ and $\text{credit\_role}$ are extraneous on the LHS.
Thus, $FD_{10}$ is simplified to $\text{ceremony\_id}, \text{category\_id}, \text{work\_id} \to \text{is\_winner}$, which is already present.

### Step 3: Elimination of Redundant Dependencies
Testing each remaining dependency shows that deleting any one reduces the closure set.
Hence, the decomposed set is the **Minimal Cover** ($F_{min}$).

---

## 5. Schema Refinement: 1NF and 2NF Transformations

### 5.1 First Normal Form (1NF)
- **Definition**: A relation is in 1NF if and only if all domain values are atomic (indivisible) and there are no repeating groups or multivalued arrays.
- **Violation in Raw Data**: In historical archives, credits are often grouped into a single non-atomic string:
  `credited_creators: "Beyoncé Knowles (Vocals, Producer), The-Dream (Songwriter), Mike Dean (Mixing)"`.
- **1NF Resolution**: Decompose into discrete atomic tuple entries with atomic domains:
  - `creator_id`: atomic string
  - `credit_role`: atomic string
  - `contribution_pct`: atomic numeric

### 5.2 Second Normal Form (2NF)
- **Definition**: A relation is in 2NF if and only if it is in 1NF and **no non-prime attribute is partially dependent on any candidate key** (i.e., every non-prime attribute must be fully functionally dependent on every candidate key).

#### Violation in $\mathcal{R}$:
Candidate key: $\{ \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{credit\_role} \}$
- Non-prime attributes $\text{venue\_name}, \text{venue\_city}$ depend on $\text{venue\_id}$, which depends on $\text{ceremony\_id}$ (a proper subset of the key).
- Non-prime attribute $\text{work\_title}$ depends on $\text{work\_id}$ (a proper subset of the key).
- Non-prime attribute $\text{cat\_name}$ depends on $\text{category\_id}$ (a proper subset of the key).

These are **partial functional dependencies**.

#### 2NF Decomposition:
To achieve 2NF, we decompose $\mathcal{R}$ into relations where non-prime attributes depend on the entire key:
1. $R_1(\underline{\text{ceremony\_id}}, \text{edition}, \text{ceremony\_date}, \text{venue\_id}, \text{rating\_millions})$
2. $R_2(\underline{\text{venue\_id}}, \text{venue\_name}, \text{venue\_city}, \text{venue\_cap})$
3. $R_3(\underline{\text{category\_id}}, \text{cat\_name}, \text{field\_id})$
4. $R_4(\underline{\text{field\_id}}, \text{field\_name})$
5. $R_5(\underline{\text{work\_id}}, \text{work\_title}, \text{label\_id})$
6. $R_6(\underline{\text{label\_id}}, \text{label\_name})$
7. $R_7(\underline{\text{artist\_id}}, \text{artist\_name}, \text{artist\_country})$
8. $R_8(\underline{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}}, \text{artist\_id}, \text{is\_winner})$
9. $R_9(\underline{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{artist\_id}, \text{credit\_role}})$

Every relation $R_1$ through $R_9$ satisfies 2NF.
