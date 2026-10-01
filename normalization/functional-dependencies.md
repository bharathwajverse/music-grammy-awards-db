# Functional Dependency Analysis & Higher-Order Dependency Specifications

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 8 — Functional Dependency Analysis  
> **Document**: Mathematical Derivations of Functional Dependencies (FDs), Attribute Closures, Minimal Cover, Partial & Transitive Dependencies, Multivalued Dependencies (MVDs), and Join Dependencies (JDs)  
> **Status**: Completed  
> **Theoretical Framework**: Elmasri & Navathe (*Fundamentals of Database Systems*, 7th Edition, Chapters 14 & 15) / Codd (1970, 1972) / Fagin (1977, 1979)  
> **Related Artifacts**:  
> - Candidate Key Derivations: [`normalization/key-analysis.md`](./key-analysis.md)  
> - Relational Schema Catalog: [`relational-model/schema.md`](../relational-model/schema.md)  
> - Keys & Referential Integrity: [`relational-model/keys-and-relationships.md`](../relational-model/keys-and-relationships.md)  

---

## 1. Formal Theoretical Framework of Functional Dependencies

In relational database theory (Codd 1970; Elmasri & Navathe 2016):

### 1.1. Formal Definition of Functional Dependency ($X \to Y$)
Let $R(A_1, A_2, \dots, A_n)$ be a relation schema, and let $X, Y \subseteq R$ be subsets of attributes of $R$.
A **Functional Dependency**, denoted by:
$$X \to Y$$
specifies a semantic constraint on possible tuples that may form a relation state $r(R)$. The constraint states that for any two tuples $t_1, t_2 \in r(R)$, if $t_1[X] = t_2[X]$, then $t_1[Y]$ must also equal $t_2[Y]$:
$$\forall t_1, t_2 \in r(R), \quad (t_1[X] = t_2[X]) \implies (t_1[Y] = t_2[Y])$$

- $X$ is referred to as the **determinant** (left-hand side, LHS).
- $Y$ is referred to as the **dependent** (right-hand side, RHS).
- If $Y \subseteq X$, the dependency $X \to Y$ is called **trivial**.
- If $Y \not\subseteq X$, the dependency $X \to Y$ is called **non-trivial**.

---

### 1.2. Armstrong's Axioms for Functional Dependencies
The set of all dependencies logically implied by a given set of functional dependencies $F$ is called the **closure of $F$**, denoted $F^+$. Armstrong's Axioms provide a sound and complete inference system for deriving $F^+$:

1. **Axiom of Reflexivity**:
   $$\text{If } Y \subseteq X, \text{ then } X \to Y$$
2. **Axiom of Augmentation**:
   $$\text{If } X \to Y, \text{ then } XZ \to YZ \quad (\forall Z \subseteq R)$$
3. **Axiom of Transitivity**:
   $$\text{If } X \to Y \text{ and } Y \to Z, \text{ then } X \to Z$$

#### Secondary Inference Rules (Derived from Armstrong's Axioms):
4. **Decomposition (Projectivity) Rule**:
   $$\text{If } X \to YZ, \text{ then } X \to Y \text{ and } X \to Z$$
5. **Union (Additivity) Rule**:
   $$\text{If } X \to Y \text{ and } X \to Z, \text{ then } X \to YZ$$
6. **Pseudotransitivity Rule**:
   $$\text{If } X \to Y \text{ and } WY \to Z, \text{ then } WX \to Z$$

---

### 1.3. Attribute Closure Algorithm ($X^+$)
Given a set of functional dependencies $F$ and a set of attributes $X$, the **attribute closure** $X^+$ with respect to $F$ is the set of all attributes functionally determined by $X$ under $F$:

```text
Algorithm: ComputeAttributeClosure(X, F)
Input: Attribute set X, Functional Dependency set F
Output: X^+ (Attribute closure)

X^+ := X;
repeat
    old_X^+ := X^+;
    for each functional dependency (Y -> Z) in F do
        if Y ⊆ X^+ then
            X^+ := X^+ ∪ Z;
        end if;
    end for;
until (X^+ = old_X^+);
return X^+;
```

---

### 1.4. Minimal Cover Algorithm ($F_{min}$)
A set of functional dependencies $E$ is an **equivalent minimal cover** (canonical cover) for $F$ if $E^+ = F^+$ and:
1. **Standard Form**: Every dependency in $E$ has a single attribute on its right-hand side ($X \to A$).
2. **Left-Reduced**: No attribute $B \in X$ is extraneous on the left-hand side (i.e., $(X - \{B\})^+ \text{ under } E \text{ contains } A$).
3. **Non-Redundant**: No dependency $(X \to A) \in E$ is redundant (i.e., $(E - \{X \to A\})^+ \equiv E^+$).

---

## 2. Universal Unnormalized GRAMMY Schema ($\mathcal{U}_{GRAMMY}$)

To rigorously demonstrate the necessity of functional dependency analysis, consider the monolithic, unnormalized flat relation representing the raw GRAMMY Awards operational log prior to relational normalization:

$$\mathcal{U}_{GRAMMY}(\text{ceremony\_id}, \text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{venue\_name}, \text{venue\_city}, \text{venue\_capacity}, \text{network\_name}, \text{us\_viewers\_millions},$$
$$\text{category\_id}, \text{category\_name}, \text{field\_id}, \text{field\_name}, \text{work\_id}, \text{work\_title}, \text{work\_type}, \text{release\_date}, \text{label\_id}, \text{label\_name},$$
$$\text{creator\_id}, \text{creator\_legal\_name}, \text{stage\_name}, \text{creator\_country}, \text{credit\_role}, \text{contribution\_pct}, \text{nomination\_id}, \text{ballot\_slot}, \text{is\_winner}, \text{statuette\_serial})$$

---

## 3. Real-World Functional Dependencies Across Domain Entities

Based on Recording Academy bylaws, legal contracts, and physical event operations, the following enterprise functional dependencies hold:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 CORE ENTERPRISE FUNCTIONAL DEPENDENCY SET                              │
├─────┬─────────────────────────────────────────────────┬────────────────────────────────────────────────┤
│ ID  │ Functional Dependency (FD)                      │ Business / Academy Operational Semantics       │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD1 │ ceremony_id → edition_number, ceremony_date,    │ Each ceremony uniquely identifies its edition, │
│     │ broadcast_year, venue_id, network_name          │ telecast date, air year, venue, and network.   │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD2 │ edition_number → ceremony_id, broadcast_year    │ Each sequential edition corresponds to one ID. │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD3 │ venue_id → venue_name, venue_city, venue_capacity│ A venue ID uniquely determines its name, host  │
│     │                                                 │ city municipality, and physical max capacity.  │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD4 │ category_id → category_name, field_id           │ Each category belongs to exactly one field.    │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD5 │ field_id → field_name                           │ Each award field ID determines its title.      │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD6 │ work_id → work_title, work_type, release_date,  │ Each master creative work is released by one   │
│     │ label_id                                        │ primary record label on a specific date.       │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD7 │ label_id → label_name                           │ Each label ID uniquely determines corporate.   │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD8 │ creator_id → creator_legal_name, stage_name,    │ Each talent practitioner has fixed legal name, │
│     │ creator_country                                 │ stage alias, and sovereign citizenship.        │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD9 │ nomination_id → ceremony_id, category_id,       │ A certified nomination ballot entry binds a    │
│     │ work_id, creator_id, ballot_slot, is_winner     │ work to a category and ceremony edition.       │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD10│ ceremony_id, category_id, work_id →             │ In a single category at a single ceremony,     │
│     │ nomination_id, creator_id, ballot_slot, is_winner│ a work can appear at most once on the ballot.  │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD11│ nomination_id, creator_id, credit_role →        │ The combination of a nomination, creator, and  │
│     │ contribution_pct                                │ role determines the audited credit percentage. │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD12│ statuette_serial → nomination_id, creator_id    │ Each gold statuette is engraved and issued to  │
│     │                                                 │ exactly one verified winning creator credit.   │
├─────┼─────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│ FD13│ ceremony_id → us_viewers_millions               │ Each ceremony has a unique Nielsen rating.     │
└─────┴─────────────────────────────────────────────────┴────────────────────────────────────────────────┘
```

---

## 4. Minimal Cover ($F_{min}$) Derivation for the GRAMMY Schema

We derive the canonical minimal cover $F_{min}$ for the core enterprise dependencies using the 3-step canonical reduction algorithm:

### Step 1: Right-Hand Side (RHS) Decomposition
Applying the Decomposition Rule ($X \to YZ \implies X \to Y \text{ and } X \to Z$), each dependency is transformed so that its RHS consists of a single attribute:

$$\begin{aligned}
f_1: & \quad \text{ceremony\_id} \to \text{edition\_number} \\
f_2: & \quad \text{ceremony\_id} \to \text{ceremony\_date} \\
f_3: & \quad \text{ceremony\_id} \to \text{broadcast\_year} \\
f_4: & \quad \text{ceremony\_id} \to \text{venue\_id} \\
f_5: & \quad \text{ceremony\_id} \to \text{network\_name} \\
f_6: & \quad \text{ceremony\_id} \to \text{us\_viewers\_millions} \\
f_7: & \quad \text{edition\_number} \to \text{ceremony\_id} \\
f_8: & \quad \text{venue\_id} \to \text{venue\_name} \\
f_9: & \quad \text{venue\_id} \to \text{venue\_city} \\
f_{10}: & \quad \text{venue\_id} \to \text{venue\_capacity} \\
f_{11}: & \quad \text{category\_id} \to \text{category\_name} \\
f_{12}: & \quad \text{category\_id} \to \text{field\_id} \\
f_{13}: & \quad \text{field\_id} \to \text{field\_name} \\
f_{14}: & \quad \text{work\_id} \to \text{work\_title} \\
f_{15}: & \quad \text{work\_id} \to \text{work\_type} \\
f_{16}: & \quad \text{work\_id} \to \text{release\_date} \\
f_{17}: & \quad \text{work\_id} \to \text{label\_id} \\
f_{18}: & \quad \text{label\_id} \to \text{label\_name} \\
f_{19}: & \quad \text{creator\_id} \to \text{creator\_legal\_name} \\
f_{20}: & \quad \text{creator\_id} \to \text{stage\_name} \\
f_{21}: & \quad \text{creator\_id} \to \text{creator\_country} \\
f_{22}: & \quad \text{nomination\_id} \to \text{ceremony\_id} \\
f_{23}: & \quad \text{nomination\_id} \to \text{category\_id} \\
f_{24}: & \quad \text{nomination\_id} \to \text{work\_id} \\
f_{25}: & \quad \text{nomination\_id} \to \text{creator\_id} \\
f_{26}: & \quad \text{nomination\_id} \to \text{ballot\_slot} \\
f_{27}: & \quad \text{nomination\_id} \to \text{is\_winner} \\
f_{28}: & \quad \text{ceremony\_id}, \text{category\_id}, \text{work\_id} \to \text{nomination\_id} \\
f_{29}: & \quad \text{nomination\_id}, \text{creator\_id}, \text{credit\_role} \to \text{contribution\_pct} \\
f_{30}: & \quad \text{statuette\_serial} \to \text{nomination\_id} \\
f_{31}: & \quad \text{statuette\_serial} \to \text{creator\_id}
\end{aligned}$$

---

### Step 2: Elimination of Extraneous Left-Hand Side Attributes
We check composite determinants for extraneous attributes:
1. Consider $f_{29}: \{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}\} \to \text{contribution\_pct}$.
   - Does $\text{nomination\_id}^+$ contain $\text{creator\_id}$?
     $$\text{nomination\_id}^+ = \{ \text{nomination\_id}, \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{creator\_id}, \text{ballot\_slot}, \text{is\_winner}, \dots \}$$
   - Because $f_{25}: \text{nomination\_id} \to \text{creator\_id}$ holds, $\text{creator\_id}$ on the LHS of $f_{29}$ is **extraneous** for the lead artist credit!
   - However, for secondary craft credits (producers, engineers, mixers), multiple distinct creators participate on the same nomination entry. Therefore, in the general credit relationship, $\{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}\}$ is minimal because a single nomination involves many distinct creators. Neither attribute is extraneous.
2. Consider $f_{28}: \{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}\} \to \text{nomination\_id}$.
   - Neither $\{\text{ceremony\_id}, \text{category\_id}\}^+$ nor $\{\text{category\_id}, \text{work\_id}\}^+$ nor $\{\text{ceremony\_id}, \text{work\_id}\}^+$ contains $\text{nomination\_id}$.
   - All three attributes are essential. None is extraneous.

---

### Step 3: Elimination of Redundant Dependencies
We test each dependency $X \to A$ to determine if it can be derived from $F - \{X \to A\}$:
- Test $f_3: \text{edition\_number} \to \text{broadcast\_year}$.
  $$\text{edition\_number}^+ \text{ under } (F - \{f_3\}) = \{\text{edition\_number}, \text{ceremony\_id}, \text{ceremony\_date}, \text{broadcast\_year}, \dots \}$$
  Because $\text{edition\_number} \to \text{ceremony\_id}$ and $\text{ceremony\_id} \to \text{broadcast\_year}$, the direct dependency $\text{edition\_number} \to \text{broadcast\_year}$ is **redundant** and removed.
- Testing all other dependencies confirms that removing any single dependency strictly diminishes the closure set.

$$\therefore F_{min} = \{ f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_{10}, f_{11}, f_{12}, f_{13}, f_{14}, f_{15}, f_{16}, f_{17}, f_{18}, f_{19}, f_{20}, f_{21}, f_{22}, f_{23}, f_{24}, f_{25}, f_{26}, f_{27}, f_{28}, f_{29}, f_{30}, f_{31} \}$$

---

## 5. Partial Functional Dependencies & 2NF Violations

### 5.1. Formal Definition of Partial Functional Dependency
Given a relation schema $R$ with functional dependency set $F$ and a candidate key $K$:
A functional dependency $X \to Y$ is a **Partial Dependency** if:
1. $X$ is a strict proper subset of candidate key $K$ ($X \subset K$), and
2. $Y$ is a **non-prime attribute** (an attribute not belonging to any candidate key of $R$).

A relation schema $R$ is in **Second Normal Form (2NF)** if and only if it is in 1NF and contains **zero partial dependencies**.

---

### 5.2. Concrete GRAMMY Domain Violation in $\mathcal{U}_{GRAMMY}$
Consider the universal unnormalized relation $\mathcal{U}_{GRAMMY}$. Its minimal candidate key is:
$$K = \{ \text{nomination\_id}, \text{creator\_id}, \text{credit\_role} \}$$
(or equivalently $\{ \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{creator\_id}, \text{credit\_role} \}$).

#### Identified Partial Dependencies:
```
┌──────────────────────────────────────────────────┬──────────────────────┬──────────────────────────────┐
│ Partial Functional Dependency (X → Y)            │ Determinant X ⊂ K    │ Non-Prime Dependent Y        │
├──────────────────────────────────────────────────┼──────────────────────┼──────────────────────────────┤
│ nomination_id → ceremony_id, category_id, work_id│ {nomination_id} ⊂ K  │ ceremony_id, category_id, ...│
│ creator_id → stage_name, creator_country         │ {creator_id} ⊂ K     │ stage_name, creator_country  │
│ work_id → work_title, release_date, label_id     │ {nomination_id} ⊂ K* │ work_title, label_id         │
│ category_id → category_name, field_id            │ {nomination_id} ⊂ K* │ category_name, field_id      │
└──────────────────────────────────────────────────┴──────────────────────┴──────────────────────────────┘
* Through transitivity from nomination_id.
```

#### Real-World Operational Anomalies Caused by Partial Dependencies:
1. **Update Anomaly**: If Beyoncé's stage name or legal name changes, and she appears across 88 distinct nomination entries and craft credits, all 88 tuples in $\mathcal{U}_{GRAMMY}$ must be updated. If any row is missed, the database enters an inconsistent state.
2. **Insertion Anomaly**: We cannot record a newly accredited music creator who has not yet received a certified GRAMMY nomination, because the candidate key components $\text{nomination\_id}$ and $\text{credit\_role}$ would be $\text{NULL}$, violating **Entity Integrity**.
3. **Deletion Anomaly**: If a disqualified nomination entry is deleted from the historical ballot log, the creator's biographical metadata (`stage_name`, `creator_country`) is catastrophically lost if they held no other nominations.

---

### 5.3. 2NF Decomposition Resolution
To eliminate all partial dependencies, $\mathcal{U}_{GRAMMY}$ is decomposed into separate relations where every non-prime attribute is fully functionally dependent on the entire primary key:
- `creators`($\underline{\text{creator\_id}}, \text{creator\_legal\_name}, \text{stage\_name}, \text{creator\_country}$)
- `nominated_works`($\underline{\text{work\_id}}, \text{work\_title}, \text{work\_type}, \text{release\_date}, \text{label\_id}$)
- `award_categories`($\underline{\text{category\_id}}, \text{category\_name}, \text{field\_id}$)
- `award_fields`($\underline{\text{field\_id}}, \text{field\_name}$)
- `nomination_entries`($\underline{\text{nomination\_id}}, \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{ballot\_slot}, \text{is\_winner}$)
- `nomination_credits`($\underline{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}}, \text{contribution\_pct}$)
- `winner_records`($\underline{\text{winner\_record\_id}}, \text{nomination\_id}, \text{ceremony\_id}, \text{category\_id}, \text{winning\_work\_id}, \text{primary\_artist\_id}$)
- `trophy_tracking`($\underline{\text{trophy\_id}}, \text{winner\_record\_id}, \text{recipient\_creator\_id}, \text{statuette\_serial\_number}$)

Every resulting relation satisfies **2NF**.

---

## 6. Transitive Functional Dependencies & 3NF Violations

### 6.1. Formal Definition of Transitive Functional Dependency
Given a relation schema $R$ with functional dependency set $F$ and primary key $X$:
A functional dependency $X \to Z$ is a **Transitive Dependency** if there exists an attribute set $Y$ such that:
1. $X \to Y$,
2. $Y \not\to X$ ($Y$ is not a candidate key),
3. $Y \to Z$, and
4. $Z$ is a non-prime attribute and $Z \not\subseteq Y$.

A relation schema $R$ is in **Third Normal Form (3NF)** if and only if it is in 2NF and contains **zero transitive dependencies** (i.e., for every non-trivial dependency $X \to A$, either $X$ is a superkey or $A$ is a prime attribute).

---

### 6.2. Concrete GRAMMY Domain Transitive Dependency Examples

#### Example 6.2.1: Venue Transitivity in Ceremonies
Consider the 2NF relation:
$$R_{ceremony\_venue}(\underline{\text{ceremony\_id}}, \text{edition\_number}, \text{ceremony\_date}, \text{venue\_id}, \text{venue\_name}, \text{venue\_city}, \text{venue\_capacity})$$

- Functional dependencies holding:
  1. $\text{ceremony\_id} \to \text{venue\_id}$
  2. $\text{venue\_id} \to \text{venue\_name}, \text{venue\_city}, \text{venue\_capacity}$
  3. $\text{venue\_id} \not\to \text{ceremony\_id}$ (Crypto.com Arena has hosted Ceremonies 42, 43, 44, ..., 65).
- **Transitive Dependency**:
  $$\text{ceremony\_id} \to \text{venue\_id} \to \text{venue\_name}$$
- **Academic Hazard**: Repeating Crypto.com Arena's seating capacity ($20,000$) across 21 ceremonies wastes storage and introduces update anomalies if the arena undergoes architectural renovations.
- **3NF Resolution**: Decompose into:
  - $\text{ceremonies}(\underline{\text{ceremony\_id}}, \text{edition\_number}, \text{ceremony\_date}, \text{venue\_id})$
  - $\text{venues}(\underline{\text{venue\_id}}, \text{venue\_name}, \text{venue\_city}, \text{venue\_capacity})$

---

#### Example 6.2.2: Record Label Transitivity in Master Works
Consider the 2NF relation:
$$R_{works\_labels}(\underline{\text{work\_id}}, \text{work\_title}, \text{work\_type}, \text{release\_date}, \text{label\_id}, \text{label\_name}, \text{parent\_music\_group})$$

- Functional dependencies holding:
  1. $\text{work\_id} \to \text{label\_id}$
  2. $\text{label\_id} \to \text{label\_name}, \text{parent\_music_group}$
  3. $\text{label\_id} \not\to \text{work\_id}$ (Columbia Records has released thousands of nominated tracks).
- **Transitive Dependency**:
  $$\text{work\_id} \to \text{label\_id} \to \text{label\_name}$$
- **3NF Resolution**: Decompose into:
  - $\text{nominated\_works}(\underline{\text{work\_id}}, \text{work\_title}, \text{work\_type}, \text{release\_date}, \text{label\_id})$
  - $\text{record\_labels}(\underline{\text{label\_id}}, \text{label\_name}, \text{parent\_music\_group})$

---

#### Example 6.2.3: Award Field Transitivity in Categories
Consider the 2NF relation:
$$R_{cat\_fields}(\underline{\text{category\_id}}, \text{category\_name}, \text{standard\_short\_code}, \text{field\_id}, \text{field\_name}, \text{field\_abbreviation})$$

- Functional dependencies holding:
  1. $\text{category\_id} \to \text{field\_id}$
  2. $\text{field\_id} \to \text{field\_name}, \text{field\_abbreviation}$
  3. $\text{field\_id} \not\to \text{category\_id}$ (Pop Field `FLD_POP` contains Pop Solo, Pop Duo/Group, Pop Vocal Album, Dance/Pop).
- **Transitive Dependency**:
  $$\text{category\_id} \to \text{field\_id} \to \text{field\_name}$$
- **3NF Resolution**: Decompose into:
  - $\text{award\_categories}(\underline{\text{category\_id}}, \text{field\_id}, \text{category\_name}, \text{standard\_short\_code})$
  - $\text{award\_fields}(\underline{\text{field\_id}}, \text{field\_name}, \text{field\_abbreviation})$

---

## 7. Multivalued Dependencies (MVDs) & 4NF Analysis

### 7.1. Formal Definition of Multivalued Dependency ($X \twoheadrightarrow Y$)
Introduced by Ronald Fagin (1977):
Let $R$ be a relation schema, and let $X, Y \subseteq R$. The **Multivalued Dependency**:
$$X \twoheadrightarrow Y$$
holds on $R$ if and only if, whenever two tuples $t_1, t_2 \in r(R)$ agree on $X$ ($t_1[X] = t_2[X]$), there exist tuples $t_3, t_4 \in r(R)$ such that:
$$\begin{aligned}
t_3[X] &= t_1[X], & t_3[Y] &= t_1[Y], & t_3[R - (XY)] &= t_2[R - (XY)] \\
t_4[X] &= t_1[X], & t_4[Y] &= t_2[Y], & t_4[R - (XY)] &= t_1[R - (XY)]
\end{aligned}$$

- **Semantic Interpretation**: $X$ multidetermines $Y$ if the set of $Y$-values associated with a given $X$-value is completely independent of the values of the remaining attributes $R - (XY)$.
- If $X \twoheadrightarrow Y$, then by symmetry:
  $$X \twoheadrightarrow (R - XY)$$
  often written as $X \twoheadrightarrow Y \mid Z$ where $Z = R - (XY)$.

---

### 7.2. Fourth Normal Form (4NF) Definition
A relation schema $R$ is in **Fourth Normal Form (4NF)** with respect to a set of dependencies $D$ (containing FDs and MVDs) if and only if:
For every non-trivial multivalued dependency $X \twoheadrightarrow Y$ in $D^+$, $X$ is a **superkey** of $R$.
- A trivial MVD is one where $Y \subseteq X$ or $XY = R$.

---

### 7.3. Real-World GRAMMY MVD Violations and 4NF Decompositions

#### Scenario 7.3.1: Creator Multi-Skills & PRO Affiliations
In the music industry, an artist plays multiple musical instruments (`Vocals`, `Piano`, `Bass`) and possesses multiple independent Performing Rights Organization affiliations or song catalog publishers (`ASCAP`, `BMI`, `PRS`).

Consider the un-decomposed relation:
$$R_{creator\_talents}(\underline{\text{creator\_id}, \text{instrument}, \text{pro\_affiliation}})$$

- **Enterprise Semantic Reality**:
  Beyoncé Knowles (`CRT_BEYONCE_001`) performs on `Vocals` and `Piano`. She licenses works through both `ASCAP` (US) and `PRS` (UK). Her ability to play Piano is completely orthogonal to her licensing through ASCAP.
- **Multivalued Dependencies Holding**:
  $$\text{creator\_id} \twoheadrightarrow \text{instrument} \mid \text{pro\_affiliation}$$
- **Tuple Proliferation (Cross-Product Anomaly)**:

| `creator_id` | `instrument` | `pro_affiliation` |
| :--- | :--- | :--- |
| `CRT_BEYONCE_001` | Vocals | ASCAP |
| `CRT_BEYONCE_001` | Vocals | PRS |
| `CRT_BEYONCE_001` | Piano | ASCAP |
| `CRT_BEYONCE_001` | Piano | PRS |

- **4NF Violation**:
  - The MVD $\text{creator\_id} \twoheadrightarrow \text{instrument}$ is non-trivial.
  - The determinant $\text{creator\_id}$ is **not a superkey** of $R_{creator\_talents}$ (the key is all 3 attributes combined).
- **4NF Lossless Decomposition**:
  Decompose $R_{creator\_talents}$ into two independent binary projections:
  $$R_{instruments}(\underline{\text{creator\_id}, \text{instrument}})$$
  $$R_{pro\_affiliations}(\underline{\text{creator\_id}, \text{pro\_affiliation}})$$
  Both relations satisfy 4NF.

---

#### Scenario 7.3.2: Ceremony Co-Hosts and Corporate Sponsors
Consider the telecast coordination relation:
$$R_{telecast\_coordination}(\underline{\text{ceremony\_id}, \text{co\_host\_name}, \text{corporate\_sponsor}})$$

- At Ceremony 65, Trevor Noah and James Corden co-hosted segments. Official telecast sponsors were Mastercard, Hilton, and Grey Goose.
- The roster of hosts is completely independent of corporate sponsorship contracts.
- **Multivalued Dependency Holding**:
  $$\text{ceremony\_id} \twoheadrightarrow \text{co\_host\_name} \mid \text{corporate\_sponsor}$$
- **4NF Violation**:
  $\text{ceremony\_id}$ is not a superkey. Every host must be repeated for every sponsor ($2 \times 3 = 6$ tuples).
- **4NF Lossless Decomposition**:
  $$R_{hosts}(\underline{\text{ceremony\_id}, \text{co\_host\_name}})$$
  $$R_{sponsors}(\underline{\text{ceremony\_id}, \text{corporate\_sponsor}})$$

---

## 8. Join Dependencies (JDs) & 5NF (Project-Join Normal Form) Analysis

### 8.1. Formal Definition of Join Dependency ($\bowtie[R_1, R_2, \dots, R_m]$)
Introduced by Jorma Rissanen (1977) and Ronald Fagin (1979):
A relation schema $R$ satisfies the **Join Dependency**:
$$\text{JD} = \bowtie[R_1, R_2, \dots, R_m]$$
over attribute sets $R_1, R_2, \dots, R_m$ (where $\bigcup_{i=1}^m R_i = R$) if and only if every valid relation state $r(R)$ is equal to the lossless natural join of its projections onto $R_i$:
$$r(R) = \pi_{R_1}(r(R)) \bowtie \pi_{R_2}(r(R)) \bowtie \dots \bowtie \pi_{R_m}(r(R))$$

- **Significance**: An MVD is simply a 2-way join dependency:
  $$(X \twoheadrightarrow Y) \iff \bowtie[XY, \; X(R - Y)]$$
  A general Join Dependency represents a constraint that cannot be broken down into binary MVDs (an $m$-way cyclic dependency).

---

### 8.2. Fifth Normal Form (5NF / PJNF) Definition
A relation schema $R$ is in **Fifth Normal Form (5NF)**, or **Project-Join Normal Form (PJNF)**, with respect to a set of dependencies $D$ (including FDs, MVDs, and JDs) if and only if:
For every non-trivial join dependency $\bowtie[R_1, R_2, \dots, R_m]$ in $D^+$, **every $R_i$ is a superkey of $R$**.

---

### 8.3. Concrete GRAMMY Domain Join Dependency Scenario

#### The Producer-Category-Acoustic Workflow Triad
In the Recording Academy's Craft and Specialty Committees, consider the triadic regulatory constraint governing sound engineering eligibility across producers, award categories, and audio production workflows:

$$R_{craft\_workflow}(\underline{\text{producer\_id}, \text{category\_id}, \text{workflow\_mode}})$$
where $\text{workflow\_mode} \in \{\text{'Pure Analog Tape'}, \text{'Hybrid Pro Tools'}, \text{'Dolby Atmos Immersive'}\}$.

#### Triadic Rule Semantics (Cyclic Constraint):
1. **Rule 1**: A producer $P$ is certified to produce in category $C$ (e.g., Rick Rubin is approved for *Album of the Year* and *Best Rock Album*).
2. **Rule 2**: A producer $P$ specializes in workflow mode $W$ (e.g., Rick Rubin works in *Pure Analog Tape* and *Hybrid Pro Tools*).
3. **Rule 3**: An award category $C$ permits workflow mode $W$ (e.g., *Best Immersive Audio Album* strictly requires *Dolby Atmos Immersive*; *Best Rock Album* permits *Pure Analog Tape* and *Hybrid Pro Tools*).

#### The 5NF Constraint:
Under Recording Academy bylaws, whenever producer $P$ is certified for category $C$, and producer $P$ works in workflow $W$, and category $C$ permits workflow $W$, then producer $P$ **must be permitted** to submit an entry in category $C$ using workflow $W$.

This constraint corresponds to the non-trivial cyclic **Join Dependency**:
$$\bowtie[\; R_1(\text{producer\_id}, \text{category\_id}), \;\; R_2(\text{category\_id}, \text{workflow\_mode}), \;\; R_3(\text{producer\_id}, \text{workflow\_mode}) \;]$$

#### Why This Cannot Be Decomposed into Binary MVDs:
No individual binary multivalued dependency ($X \twoheadrightarrow Y$) holds because no two attributes are completely independent of the third. The relation is in 4NF because it has **zero non-trivial binary MVDs**; yet, storing all three in one relation causes spurious tuple anomalies if the triadic rule is violated!

#### 5NF Decomposition Resolution:
To eliminate redundancy and ensure lossless join reconstruction, $R_{craft\_workflow}$ is decomposed into **three binary projection tables**:
1. $R_1(\underline{\text{producer\_id}, \text{category\_id}})$
2. $R_2(\underline{\text{category\_id}, \text{workflow\_mode}})$
3. $R_3(\underline{\text{producer\_id}, \text{workflow\_mode}})$

Lossless reconstruction is guaranteed by the join dependency:
$$R_{craft\_workflow} \equiv R_1 \bowtie R_2 \bowtie R_3$$
Because each projection table $R_1, R_2, R_3$ now represents an all-key relation, the schema is in **Fifth Normal Form (5NF)**.

---

## 9. Comprehensive Dependency Summary Matrix

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              DEPENDENCY CLASSIFICATION & RESOLUTION MATRIX                             │
├────────────────────┬──────────────────────┬───────────────────────────────┬────────────────────────────┤
│ Dependency Class   │ Formal Expression    │ GRAMMY Domain Real-World Case │ Normal Form Resolution     │
├────────────────────┼──────────────────────┼───────────────────────────────┼────────────────────────────┤
│ Full Functional    │ X → Y (X minimal)    │ nomination_id → work_id       │ Baseline 1NF               │
│ Dependency         │                      │ category_id → category_name   │ Satisfied in all relations │
├────────────────────┼──────────────────────┼───────────────────────────────┼────────────────────────────┤
│ Partial Functional │ X ⊂ CK ∧ X → Y       │ {nom_id, creator_id}          │ 2NF Decomposition          │
│ Dependency         │ (Y non-prime)        │ creator_id → stage_name       │ creators table separated   │
├────────────────────┼──────────────────────┼───────────────────────────────┼────────────────────────────┤
│ Transitive         │ X → Y ∧ Y → Z        │ ceremony_id → venue_id        │ 3NF Decomposition          │
│ Dependency         │ (Y not superkey)     │ venue_id → venue_capacity     │ venues table separated     │
├────────────────────┼──────────────────────┼───────────────────────────────┼────────────────────────────┤
│ Multivalued        │ X ↠ Y │ Z            │ creator_id ↠ instrument       │ 4NF Decomposition          │
│ Dependency (MVD)   │ (Y, Z independent)   │ creator_id ↠ pro_affiliation  │ 2 separate binary tables   │
├────────────────────┼──────────────────────┼───────────────────────────────┼────────────────────────────┤
│ Join Dependency    │ ⋈[R1, R2, R3]        │ Producer × Category ×         │ 5NF (PJNF) Decomposition   │
│ (JD)               │ (Cyclic triadic)     │ Audio Workflow Mode           │ 3-way projection tables    │
└────────────────────┴──────────────────────┴───────────────────────────────┴────────────────────────────┘
```
