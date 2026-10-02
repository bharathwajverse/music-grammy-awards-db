# Phase 23: Serializability Theory & Precedence Graph Analysis

> **Course**: Advanced Database Management Systems (ADBMS)  
> **Module**: Module 5 — Concurrency Control & Isolation Protocols  
> **Topic**: Conflict Serializability, View Serializability & Precedence Graphs  
> **Status**: Completed & Verified  

---

## 1. Mathematical Foundations of Serializability

In database systems, a **schedule** (or history) $S$ represents the chronological execution sequence of operations from a set of concurrent transactions $\{T_1, T_2, \dots, T_n\}$, preserving the individual transaction operation orders.

- **Serial Schedule**: A schedule where operations of each transaction execute consecutively without interleaving (e.g. $T_1$ completes entirely before $T_2$ starts). Serial schedules are guaranteed to leave the database in a consistent state.
- **Serializable Schedule**: A concurrent interleaved schedule that produces the identical database state and output as some valid serial execution of those transactions.

---

## 2. Conflict Serializability

### 2.1 Conflicting Operations
Two operations $o_i$ and $o_j$ in a schedule $S$ are said to **conflict** if and only if all three conditions hold:
1. They belong to different transactions ($i \neq j$).
2. They access the exact same data item $Q$.
3. At least one of the operations is a write ($\text{write}(Q)$).

Hence, three conflict pairs exist:
- **$\text{Read}_i(Q) \rightarrow \text{Write}_j(Q)$** (Anti-dependency / Unrepeatable read hazard)
- **$\text{Write}_i(Q) \rightarrow \text{Read}_j(Q)$** (Flow-dependency / Dirty read hazard)
- **$\text{Write}_i(Q) \rightarrow \text{Write}_j(Q)$** (Output-dependency / Lost update hazard)

Two read operations ($\text{Read}_i(Q)$ and $\text{Read}_j(Q)$) **never conflict** because reading does not mutate state.

### 2.2 Conflict Equivalence
Schedule $S$ is **conflict equivalent** to schedule $S'$ if $S$ can be transformed into $S'$ via a finite sequence of non-conflicting adjacent operation swaps.

### 2.3 Precedence Graph (Serialization Graph)
A **Precedence Graph** $G = (V, E)$ is a directed graph where:
- The vertices $V$ correspond to the transactions participating in the schedule.
- A directed edge $T_i \rightarrow T_j$ exists if there is an operation $o_i \in T_i$ that precedes and conflicts with an operation $o_j \in T_j$.

### 2.4 Fundamental Conflict Serializability Theorem
$$\text{A schedule } S \text{ is conflict serializable} \iff \text{its precedence graph } G(S) \text{ contains no directed cycles.}$$

If $G(S)$ is acyclic, an equivalent serial schedule is directly obtained by performing a **topological sort** on $G(S)$.

---

## 3. Concrete Academic Case Study: GRAMMY Award Operations

Let us examine two concurrent transactions executing against the GRAMMY operational database:
- **Transaction $T_1$ (Auditor Ballot Certification)**:
  $$r_1(\text{Ballot}_A) \rightarrow w_1(\text{Ballot}_A) \rightarrow r_1(\text{Tally}_X) \rightarrow w_1(\text{Tally}_X) \rightarrow c_1$$
- **Transaction $T_2$ (Trophy Allocation & Broadcast Order)**:
  $$r_2(\text{Ballot}_A) \rightarrow w_2(\text{Ballot}_A) \rightarrow r_2(\text{Statuette}_Y) \rightarrow w_2(\text{Statuette}_Y) \rightarrow c_2$$

### Scenario 1: Conflict Serializable Interleaved Schedule ($S_{\text{valid}}$)

```
Time | Transaction T1                | Transaction T2
-----+-------------------------------+-------------------------------
t1   | Read(Ballot_A)                | 
t2   | Write(Ballot_A)               | 
t3   |                               | Read(Ballot_A)
t4   | Read(Tally_X)                 | 
t5   | Write(Tally_X)                | 
t6   | Commit                        | 
t7   |                               | Write(Ballot_A)
t8   |                               | Read(Statuette_Y)
t9   |                               | Write(Statuette_Y)
t10  |                               | Commit
```

#### Precedence Graph Analysis:
- At $t_2$, $w_1(\text{Ballot}_A)$ executes. At $t_3$, $r_2(\text{Ballot}_A)$ executes. This creates edge: **$T_1 \rightarrow T_2$**.
- At $t_2$, $w_1(\text{Ballot}_A)$ executes. At $t_7$, $w_2(\text{Ballot}_A)$ executes. This confirms edge: **$T_1 \rightarrow T_2$**.
- There are no operations from $T_2$ preceding conflicting operations in $T_1$.
- Graph $G$: $\{T_1 \rightarrow T_2\}$ is **acyclic**.
- **Conclusion**: Schedule $S_{\text{valid}}$ is **conflict serializable**, with equivalent serial order $\langle T_1, T_2 \rangle$.

---

### Scenario 2: Non-Serializable Schedule ($S_{\text{cycle}}$)

```
Time | Transaction T1                | Transaction T2
-----+-------------------------------+-------------------------------
t1   | Read(Ballot_A)                | 
t2   |                               | Read(Tally_X)
t3   |                               | Write(Tally_X)
t4   | Read(Tally_X)                 | 
t5   | Write(Ballot_A)               | 
t6   |                               | Read(Ballot_A)
t7   | Commit                        | 
t8   |                               | Commit
```

#### Precedence Graph Analysis:
- Conflict 1: $w_2(\text{Tally}_X)$ at $t_3$ precedes $r_1(\text{Tally}_X)$ at $t_4$. This creates directed edge: **$T_2 \rightarrow T_1$**.
- Conflict 2: $w_1(\text{Ballot}_A)$ at $t_5$ precedes $r_2(\text{Ballot}_A)$ at $t_6$. This creates directed edge: **$T_1 \rightarrow T_2$**.
- Graph $G$: Contains directed cycle $T_1 \rightarrow T_2 \rightarrow T_1$.
- **Conclusion**: Schedule $S_{\text{cycle}}$ is **NON-SERIALIZABLE**. It introduces a cycle of dependencies where each transaction observes partial, inconsistent results from the other.

---

## 4. View Serializability

View serializability is a strictly weaker condition than conflict serializability: every conflict serializable schedule is view serializable, but not vice-versa.

### 4.1 Conditions for View Equivalence
Two schedules $S$ and $S'$ over the same transaction set are **view equivalent** if:
1. **Initial Read**: For each data item $Q$, if $T_i$ reads the initial value of $Q$ in $S$, then $T_i$ must read the initial value of $Q$ in $S'$.
2. **Read-From**: If $T_i$ reads the value of $Q$ written by $T_j$ in $S$, then $T_i$ must read the value of $Q$ written by $T_j$ in $S'$.
3. **Final Write**: For each data item $Q$, if $T_i$ performs the final write on $Q$ in $S$, then $T_i$ must perform the final write on $Q$ in $S'$.

### 4.2 Blind Writes & Computational Complexity
- When a schedule contains no **blind writes** (writing a data item without reading it first), View Serializability is identical to Conflict Serializability.
- **Theorem**: Testing whether an arbitrary schedule $S$ is View Serializable is **NP-Complete** (Papadimitriou, 1979). Consequently, practical DBMS engines enforce Conflict Serializability (via 2PL, Timestamping, or MVCC snapshot validation) rather than attempting to test view serializability at runtime.

---

## 5. MongoDB Serializability Enforcement

In MongoDB Atlas, how are non-serializable interleavings prevented?

1. **Snapshot Isolation**:
   Transactions execute against a consistent point-in-time snapshot established when the first operation runs. Read operations do not acquire shared locks; instead, they read older MVCC document versions created before the snapshot timestamp.
2. **Logical Time & Causal Consistency (`clusterTime`)**:
   MongoDB utilizes a distributed hybrid logical clock (HLC). Every response carries an unsigned 64-bit integer timestamp (`operationTime` / `clusterTime`). Causal consistency sessions guarantee causal relationships:
   - Read-your-writes
   - Monotonic reads
   - Monotonic writes
   - Writes-follow-reads
3. **First-Committer-Wins Policy**:
   If Transaction $T_1$ and $T_2$ both read snapshot version $V_0$ of a document and both attempt to write $V_1$ and $V_1'$, the first transaction to execute `commit_transaction()` succeeds. The second transaction encounters a `WriteConflict` and must roll back, eliminating the lost update anomaly and maintaining serializable behavior.
