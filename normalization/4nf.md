# Fourth Normal Form (4NF) Specification & Transformation

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 9 — Schema Normalization Proofs  
> **Document**: Fourth Normal Form (4NF) Formal Definition, Multivalued Dependency (MVD) Tuple Proliferation, and Fagin's Lossless 4NF Decomposition Proof  
> **Status**: Completed  
> **Theoretical Framework**: Ronald Fagin (1977) / Elmasri & Navathe (*Fundamentals of Database Systems*, 7th Edition, Chapter 15)  
> **Related Artifacts**:  
> - BCNF Baseline: [`normalization/bcnf.md`](./bcnf.md)  
> - 5NF Transformation: [`normalization/5nf.md`](./5nf.md)  
> - Functional Dependencies: [`normalization/functional-dependencies.md`](./functional-dependencies.md)  
> - Normalization Summary: [`normalization/normalization-summary.md`](./normalization-summary.md)  

---

## 1. Formal Theoretical Definition of Fourth Normal Form (4NF)

Proposed by Ronald Fagin in 1977:
> A relation schema $R$ is in **Fourth Normal Form (4NF)** with respect to a set of dependencies $D$ (consisting of functional dependencies and multivalued dependencies) if and only if, for **every non-trivial multivalued dependency $X \twoheadrightarrow Y \in D^+$**, the determinant $X$ is a **superkey** of $R$.

### 1.1. Core Mathematical Properties of Multivalued Dependencies (MVDs):
1. **Formal Definition**: Let $R$ be a relation schema and $X, Y \subseteq R$. The MVD:
   $$X \twoheadrightarrow Y$$
   holds on $R$ if and only if, for any two tuples $t_1, t_2 \in r(R)$ such that $t_1[X] = t_2[X]$, there exist tuples $t_3, t_4 \in r(R)$ such that:
   $$\begin{aligned}
   t_3[X] &= t_1[X], & t_3[Y] &= t_1[Y], & t_3[R - XY] &= t_2[R - XY] \\
   t_4[X] &= t_1[X], & t_4[Y] &= t_2[Y], & t_4[R - XY] &= t_1[R - XY]
   \end{aligned}$$
2. **Symmetry Property**:
   $$X \twoheadrightarrow Y \iff X \twoheadrightarrow (R - XY)$$
   Denoted as $X \twoheadrightarrow Y \mid Z$ where $Z = R - (XY)$.
3. **Trivial MVD**: An MVD $X \twoheadrightarrow Y$ is *trivial* if:
   - $Y \subseteq X$, **OR**
   - $XY = R$.
4. **Generalization of FDs**: Every functional dependency is a special case of a multivalued dependency:
   $$X \to Y \implies X \twoheadrightarrow Y$$
   An MVD represents a 1-to-many relationship where a given $X$-value is associated with a *set* of $Y$-values that is completely independent of the rest of the attributes.

---

## 2. The BCNF Starting Structure with Independent Multivalued Attributes

A relation can be in **strict BCNF** (having zero non-trivial functional dependencies) and yet suffer from massive data redundancy caused by independent multivalued dependencies.

### 2.1. Case Study: Creator Performance Talents & Performing Rights Affiliations
In the music recording domain, a creative practitioner performs on multiple instruments (`Vocals`, `Piano`, `Bass`) and possesses multiple independent Performing Rights Organization affiliations (`ASCAP`, `BMI`, `PRS`):

$$R_{\text{creator\_talents}}(\text{creator\_id}, \text{performance\_instrument}, \text{pro\_affiliation})$$

### 2.2. Domain Operational Rules:
1. A creator may play multiple musical instruments.
2. A creator may have royalty publishing representation across multiple international PRO organizations.
3. An artist's proficiency with an instrument (e.g., piano) has **zero causal dependency** on which PRO collects their songwriting royalties (e.g., ASCAP vs. PRS).

### 2.3. Keys & Functional Dependencies of $R_{\text{creator\_talents}}$:
- There are **zero non-trivial functional dependencies** ($FD = \emptyset$).
- No single attribute or pair of attributes determines the third attribute.
- Therefore, the **only candidate key** is the composite of all three attributes:
  $$K = \{ \text{creator\_id}, \text{performance\_instrument}, \text{pro\_affiliation} \} \quad (\text{All-Key Relation})$$

> **Critical Theoretical Observation**: Because every determinant in the non-trivial FDs is a superkey (trivially true since $FD = \emptyset$), $R_{\text{creator\_talents}}$ is in **strict BCNF**!

---

## 3. Identification of 4NF Violations (Tuple Proliferation)

Although $R_{\text{creator\_talents}}$ is in BCNF, it contains a non-trivial **Multivalued Dependency**:
$$\text{creator\_id} \twoheadrightarrow \text{performance\_instrument} \mid \text{pro\_affiliation}$$

### 3.1. Demonstration of Cross-Product Tuple Proliferation:
Consider Beyoncé Knowles (`CRT_BEYONCE_001`), who performs on `Vocals` and `Piano`, and is affiliated with `ASCAP` and `PRS`. To maintain the independence of instruments and affiliations, the database must store every combination:

```
┌──────────────────┬────────────────────────┬─────────────────┐
│ creator_id       │ performance_instrument │ pro_affiliation │
├──────────────────┼────────────────────────┼─────────────────┤
│ CRT_BEYONCE_001  │ Vocals                 │ ASCAP           │
│ CRT_BEYONCE_001  │ Vocals                 │ PRS             │
│ CRT_BEYONCE_001  │ Piano                  │ ASCAP           │
│ CRT_BEYONCE_001  │ Piano                  │ PRS             │
└──────────────────┴────────────────────────┴─────────────────┘
```

If Beyoncé later adds `Bass` to her instruments, two new tuples must be inserted:
- $\langle \text{CRT\_BEYONCE\_001}, \text{Bass}, \text{ASCAP} \rangle$
- $\langle \text{CRT\_BEYONCE\_001}, \text{Bass}, \text{PRS} \rangle$

For an artist playing $m$ instruments with $n$ affiliations, the relation stores $m \times n$ tuples!

### 3.2. Why This Violates 4NF:
- The MVD $\text{creator\_id} \twoheadrightarrow \text{performance\_instrument}$ is **non-trivial** because $\text{performance\_instrument} \not\subseteq \{\text{creator\_id}\}$ and $\{\text{creator\_id}, \text{performance\_instrument}\} \neq R_{\text{creator\_talents}}$.
- The determinant $\text{creator\_id}$ is **NOT a superkey** of $R_{\text{creator\_talents}}$ (the key requires all 3 attributes).
- Therefore, $R_{\text{creator\_talents}}$ **violates Fourth Normal Form (4NF)**.

### 3.3. Update & Consistency Hazards:
If Beyoncé revokes her PRS affiliation, all tuples with `PRS` must be deleted across every instrument. If the deletion is executed for `Vocals` but fails for `Piano`, the database enters an illegal state where Beyoncé appears to collect PRS royalties only when performing piano!

---

## 4. 4NF Decomposition Transformation

To eliminate the MVD violation, we apply **Fagin's 4NF Decomposition Algorithm**:
For any relation $R(X, Y, Z)$ violating 4NF due to non-trivial MVD $X \twoheadrightarrow Y \mid Z$:
1. Decompose $R$ into two projection relations:
   $$R_1 = X \cup Y$$
   $$R_2 = X \cup Z$$

Applying this algorithm to $R_{\text{creator\_talents}}$:
- $X = \{ \text{creator\_id} \}$
- $Y = \{ \text{performance\_instrument} \}$
- $Z = \{ \text{pro\_affiliation} \}$

### 4.1. Decomposed 4NF Relations:

1. **`creator_instruments` ($R_1$)**:
   $$\text{creator\_instruments}(\underline{\text{creator\_id}, \text{performance\_instrument}})$$
   - Primary Key: $\{\text{creator\_id}, \text{performance\_instrument}\}$.
   - MVDs: Trivial only ($\text{creator\_id} \twoheadrightarrow \text{performance\_instrument}$ is now trivial because $XY = R_1$).
   - $\implies$ **4NF Satisfied!**

2. **`creator_pro_affiliations` ($R_2$)**:
   $$\text{creator\_pro\_affiliations}(\underline{\text{creator\_id}, \text{pro\_affiliation}})$$
   - Primary Key: $\{\text{creator\_id}, \text{pro\_affiliation}\}$.
   - MVDs: Trivial only.
   - $\implies$ **4NF Satisfied!**

---

## 5. Formal Proofs of Decomposition Validity

### 5.1. Fagin's Lossless 4NF Decomposition Theorem
Ronald Fagin (1977) proved that a decomposition of $R(X, Y, Z)$ into $R_1(X, Y)$ and $R_2(X, Z)$ is **lossless** if and only if the multivalued dependency $X \twoheadrightarrow Y \mid Z$ holds on $R$:
$$R_1 \bowtie R_2 \equiv R \iff X \twoheadrightarrow Y \mid Z$$

#### Proof:
1. By definition, $R_1 = \pi_{X, Y}(R)$ and $R_2 = \pi_{X, Z}(R)$.
2. Let $t = \langle x, y, z \rangle \in R_1 \bowtie R_2$.
3. By the definition of natural join, there must exist $t_1 \in R_1$ with $t_1[X] = x, t_1[Y] = y$, and $t_2 \in R_2$ with $t_2[X] = x, t_2[Z] = z$.
4. By projection, there exist tuples in $R$:
   - $t_a \in R$ such that $t_a[X] = x, t_a[Y] = y, t_a[Z] = z'$
   - $t_b \in R$ such that $t_b[X] = x, t_b[Y] = y', t_b[Z] = z$
5. Since $t_a[X] = t_b[X] = x$, and the MVD $X \twoheadrightarrow Y \mid Z$ holds on $R$, by Fagin's tuple definition there **must exist** a tuple $t_3 \in R$ such that:
   $$t_3[X] = t_a[X] = x, \quad t_3[Y] = t_a[Y] = y, \quad t_3[Z] = t_b[Z] = z$$
6. Therefore, $\langle x, y, z \rangle \in R$, proving that $R_1 \bowtie R_2 \subseteq R$.
7. Since $R \subseteq R_1 \bowtie R_2$ holds trivially by projection, we have:
   $$R_1 \bowtie R_2 = R$$

$$\therefore \text{ The 4NF decomposition is mathematically guaranteed Lossless!}$$

---

## 6. Real-World Storage Efficiency Gain in 4NF

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              STORAGE COMPLEXITY COMPARISON (BCNF VS 4NF)                               │
├───────────────────────────────┬───────────────────────────────┬────────────────────────────────────────┤
│ Metric                        │ Undecomposed BCNF Relation    │ Decomposed 4NF Relations               │
├───────────────────────────────┼───────────────────────────────┼────────────────────────────────────────┤
│ Schema Definition             │ R(creator, inst, pro)         │ R_1(creator, inst) + R_2(creator, pro) │
│ Tuples for m=3, n=3           │ 3 × 3 = 9 tuples              │ 3 + 3 = 6 tuples                       │
│ Tuples for m=10, n=5          │ 10 × 5 = 50 tuples            │ 10 + 5 = 15 tuples                     │
│ Insertion Complexity          │ O(m × n)                      │ O(m + n)                               │
│ Cross-Product Redundancy      │ Severe                        │ Completely Eliminated                  │
└───────────────────────────────┴───────────────────────────────┴────────────────────────────────────────┘
```

All multivalued attributes across the GRAMMY database (instruments, PRO affiliations, ceremony co-hosts, work genres) are partitioned into dedicated 4NF tables, completely eliminating cross-product anomalies.
