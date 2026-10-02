# Phase 23: Deadlock Theory, Detection Algorithms & Resolution

> **Course**: Advanced Database Management Systems (ADBMS)  
> **Module**: Module 5 — Concurrency Control & Isolation Protocols  
> **Topic**: Deadlock Characterization, Wait-For Graphs, Prevention Protocols & WiredTiger Handling  
> **Status**: Completed & Verified  

---

## 1. Mathematical Definition of Deadlock

A **deadlock** in a database management system is an operating condition in which two or more concurrent transactions are in a simultaneous blocked state, each waiting for an exclusive data lock held by another transaction in the set, such that none of the transactions can make forward progress without external intervention:

$$\exists \, \{T_1, T_2, \dots, T_k\} \quad \text{such that } T_i \text{ is waiting for a lock held by } T_{(i \bmod k) + 1} \quad \forall \, i \in \{1, \dots, k\}$$

### The 4 Necessary Coffman Conditions
A deadlock can arise if and only if all four conditions hold simultaneously (Coffman et al., 1971):
1. **Mutual Exclusion**: Resources (records, pages) are held in exclusive, non-shareable mode ($X$-lock).
2. **Hold and Wait**: Transactions currently holding resources can request and wait for additional resources.
3. **No Preemption**: A resource cannot be forcibly confiscated from a transaction; it must be released voluntarily by the holder upon commit or abort.
4. **Circular Wait**: A closed chain of transactions exists where each waits for a resource held by the next.

---

## 2. Deadlock Prevention Strategies

Deadlock prevention protocols ensure at design-time or transaction-initiation time that at least one of the four Coffman conditions can never be satisfied.

### 2.1 Conservative Two-Phase Locking (C2PL)
- A transaction must declare and acquire **all required locks simultaneously** before it begins executing its first operation.
- If even a single lock is unavailable, the transaction acquires *none* and waits.
- **Eliminates**: Condition 2 (Hold and Wait).
- **Drawbacks**: Requires complete prior knowledge of all read/write sets (impossible for interactive queries); drastically reduces concurrent throughput.

### 2.2 Timestamp-Based Prevention Protocols (Rosenkrantz et al.)
Assigns each transaction $T_i$ a unique arrival timestamp $\text{TS}(T_i)$. When transaction $T_i$ requests a lock held by $T_j$:

```
                             [Ti requests lock held by Tj]
                                           |
                    +----------------------+----------------------+
                    |                                             |
             (Wait-Die Policy)                             (Wound-Wait Policy)
                    |                                             |
          TS(Ti) < TS(Tj) ?                             TS(Ti) < TS(Tj) ?
          (Ti is older)                                 (Ti is older)
         /             \                               /             \
       YES              NO                           YES              NO
        |                |                            |                |
     [Ti WAITS]      [Ti DIES]                   [Ti WOUNDS Tj]    [Ti WAITS]
                  (Ti is aborted)               (Tj is aborted)
```

#### Comparison: Wait-Die vs. Wound-Wait

| Attribute | **Wait-Die Protocol** | **Wound-Wait Protocol** |
| :--- | :--- | :--- |
| **Philosophy** | **Non-preemptive**: Older transactions wait; younger transactions die. | **Preemptive**: Older transactions wound (preempt) younger ones; younger wait. |
| **Starvation Prevention** | High priority: Aborted younger transactions restart with **original timestamp**, eventually becoming oldest. | High priority: Older transactions preempt younger ones immediately, minimizing waiting. |
| **Aborts Frequency** | Higher abort rate (younger transactions repeatedly abort when conflicting with older). | Lower abort rate (younger transactions wait unless preempted by an active older transaction). |
| **In-flight Work** | Discards young work. | Discards young work only when older needs resource immediately. |

---

## 3. Deadlock Detection via Wait-For Graphs (WFG)

If a system allows transactions to wait without prevention, it must run periodic **Deadlock Detection**.

### 3.1 Directed Wait-For Graph (WFG) Construction
A directed graph $G = (V, E)$ maintained by the lock manager:
- Vertices $V$: Set of all active transactions.
- Directed Edge $T_i \rightarrow T_j$: Transaction $T_i$ is blocked waiting for transaction $T_j$ to release a lock.

```
       +--------+      waits for Lock(Y)      +--------+
       |   T1   | --------------------------> |   T2   |
       +--------+                             +--------+
           ^                                      |
           |          waits for Lock(X)           |
           +--------------------------------------+
```

### 3.2 Cycle Detection Algorithm
Cycles in $G$ are detected using Depth-First Search (DFS) tracking visited vertices and recursion stacks:
- **Time Complexity**: $\mathcal{O}(|V| + |E|)$.
- **Detection Frequency**: Invoked periodically (e.g. every 500ms - 2000ms) or whenever a lock request exceeds a configured timeout.

---

## 4. Deadlock Recovery & Victim Selection

Once a cycle is identified, the system must break the cycle by choosing one or more **victim transactions** to abort.

### 4.1 Victim Selection Heuristics
The lock manager evaluates a cost function to minimize system disruption:
1. **Age / Elapsed Time**: Favor aborting younger transactions with less elapsed CPU time.
2. **Progress / Work Done**: Favor transactions that have executed fewer operations and modified fewer blocks.
3. **Number of Locks Held**: Transactions holding few locks release fewer dependencies.
4. **Cascading Impact**: Avoid selecting transactions whose abort might trigger cascading aborts in non-strict systems.

### 4.2 Starvation Handling
If the victim selection algorithm repeatedly picks the same unlucky transaction, that transaction suffers **starvation**.
- **Remedy**: Every time a transaction is aborted due to deadlock, its restart retains its **original creation timestamp**. As it ages, it is guaranteed to become the oldest transaction in the system, immunizing it from future victim aborts.

---

## 5. MongoDB & WiredTiger Deadlock Architecture

Textbook relational database management systems maintain global lock dependency graphs across thousands of rows. How does MongoDB handle this differently?

### 5.1 Why Traditional Deadlocks Are Eliminated in Single Operations
1. **Document-Level Latches**: In individual CRUD operations (`updateOne`, `insertMany`), MongoDB does not acquire multi-document locking chains. Document modifications are atomic single-record operations within WiredTiger cache pages.
2. **Intent Locks at Collection Level**: MongoDB uses intent locks (`IS`, `IX`) on collections. Two concurrent updates to different documents in the same collection both acquire `IX` locks simultaneously. Because `IX` is compatible with `IX` (see matrix in `concurrency.md`), **zero blocking occurs** at the collection level.

### 5.2 Multi-Document Transaction Deadlock Handling: Fast-Fail OCC
In multi-document transactions:
1. **No Long-Lived Blocking**: Rather than permitting transactions to wait indefinitely in a queue and constructing a distributed WFG, WiredTiger enforces strict lock acquisition timeouts:
   $$\text{maxTransactionLockRequestTimeoutMillis} = 5 \text{ ms (default)}$$
2. **Fast-Fail on Contention**: If Transaction $T_2$ attempts to modify a document modified by Transaction $T_1$, WiredTiger immediately rejects $T_2$'s lock request after 5ms with a `WriteConflict` exception.
3. **Client-Side Exponential Backoff**: Instead of deep cycle-breaking inside the database kernel, MongoDB shifts resolution to the driver layer: $T_2$ aborts, rolls back its memory buffers, backs off with jitter, and restarts cleanly.
