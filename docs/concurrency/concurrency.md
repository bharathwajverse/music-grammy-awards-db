# Phase 23: Concurrency Control in Advanced DBMS & MongoDB

> **Course**: Advanced Database Management Systems (ADBMS)  
> **Module**: Module 5 — Concurrency Control & Isolation Protocols  
> **Topic**: Concurrency Mechanisms, Lock Hierarchies, Timestamp Protocols & WiredTiger MVCC  
> **Status**: Completed & Verified  

---

## 1. Executive Summary & Problem Formulation

In a multi-user enterprise database system, multiple transactions execute concurrently to maximize CPU and I/O resource utilization and minimize query response time. However, uncontrolled interleaved execution of operations gives rise to three classical DBMS concurrency anomalies:

1. **Lost Update Anomaly ($W_1(X) \rightarrow W_2(X)$)**: Two transactions read the same data item and compute new values; one transaction's write overwrites the other's without incorporating its changes.
2. **Dirty Read Anomaly / Temporary Update ($W_1(X) \rightarrow R_2(X) \rightarrow \text{Abort}_1$)**: Transaction $T_2$ reads a data item modified by uncommitted transaction $T_1$, which subsequently aborts.
3. **Unrepeatable Read Anomaly ($R_1(X) \rightarrow W_2(X) \rightarrow R_1(X)$)**: Transaction $T_1$ reads data item $X$; transaction $T_2$ modifies or deletes $X$ and commits; $T_1$ reads $X$ again and observes a different value.
4. **Phantom Read Anomaly**: Transaction $T_1$ reads a set of rows/documents satisfying a predicate; $T_2$ inserts new records matching that predicate; $T_1$ re-executes the predicate read and discovers new "phantom" records.

This document analyzes formal DBMS concurrency control theory (Locking, 2PL, Timestamp Ordering) and systematically contrasts textbook relational implementations with MongoDB Atlas and the **WiredTiger Storage Engine**.

---

## 2. Formal Lock-Based Protocols & Lock Hierarchies

### 2.1 Basic Lock Types
In classical DBMS theory, data items are protected by locks:
- **Shared Lock ($S$)**: Granted for read-only access. Multiple transactions can hold concurrent $S$ locks on the same resource ($S$ is compatible with $S$).
- **Exclusive Lock ($X$)**: Granted for write access. Only one transaction can hold an $X$ lock; all other requests are blocked ($X$ is conflicting with all modes).

### 2.2 Multiple Granularity Locking (MGL) & Intent Locks
To allow locking at different hierarchical granularities (Database $\rightarrow$ Collection/Table $\rightarrow$ Document/Row) without scanning children:
- **Intent Shared ($IS$)**: Indicates explicit intent to acquire $S$ locks at a finer granularity lower in the tree.
- **Intent Exclusive ($IX$)**: Indicates explicit intent to acquire $X$ locks at a finer granularity lower in the tree.
- **Shared Intent Exclusive ($SIX$)**: The subtree is locked in $S$ mode for reading, with intent to acquire $X$ locks on specific sub-nodes.

#### Rigorous Lock Compatibility Matrix

| Requested Mode $\downarrow$ \ Held Mode $\rightarrow$ | **$IS$** | **$IX$** | **$S$** | **$SIX$** | **$X$** |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$IS$** | **Compatible** | **Compatible** | **Compatible** | **Compatible** | Conflict |
| **$IX$** | **Compatible** | **Compatible** | Conflict | Conflict | Conflict |
| **$S$** | **Compatible** | Conflict | **Compatible** | Conflict | Conflict |
| **$SIX$** | **Compatible** | Conflict | Conflict | Conflict | Conflict |
| **$X$** | Conflict | Conflict | Conflict | Conflict | Conflict |

---

## 3. Two-Phase Locking (2PL) Variants

Two-Phase Locking guarantees **Conflict Serializability** by partitioning lock acquisition and release into two non-overlapping phases:

1. **Growing Phase**: The transaction may acquire locks, but cannot release any lock.
2. **Shrinking Phase**: The transaction may release locks, but cannot acquire any new lock.

```
       [Lock Acquisition]             [Lock Release]
             Growing Phase               Shrinking Phase
       -------------------------> Lock <-------------------------
                                 Point
```

### 2PL Variants Comparison

| Protocol Variant | Rules & Requirements | Guarantees | Cascading Rollbacks? |
| :--- | :--- | :--- | :---: |
| **Basic 2PL** | Locks acquired in Growing Phase; released in Shrinking Phase. | Conflict Serializability. | **Yes** (Subject to cascading aborts if $T_1$ aborts after releasing lock). |
| **Strict 2PL (S2PL)** | All Exclusive ($X$) locks must be held until the transaction commits or aborts. | Conflict Serializability + Strictness. | **No** (Cascadeless schedule guaranteed). |
| **Rigorous 2PL (R2PL)** | **All** locks (both Shared $S$ and Exclusive $X$) must be held until commit or abort. | Conflict Serializability + Strictness + Commit-order serializability. | **No** (Most restrictive; zero cascading aborts). |

---

## 4. Timestamp Ordering Protocols

Instead of locking data items, **Timestamp-Based Concurrency Control** assigns each transaction $T_i$ a unique monotonically increasing timestamp $\text{TS}(T_i)$ upon arrival:

Each data item $Q$ maintains two timestamps:
- $\text{W-timestamp}(Q)$: Largest timestamp of any transaction that successfully wrote $Q$.
- $\text{R-timestamp}(Q)$: Largest timestamp of any transaction that successfully read $Q$.

### 4.1 Basic Timestamp Ordering (BTO) Rules
1. **Transaction $T_i$ issues $\text{read}(Q)$**:
   - If $\text{TS}(T_i) < \text{W-timestamp}(Q)$: $T_i$ needs to read a value of $Q$ that was already overwritten. $T_i$ is **rejected and aborted**.
   - If $\text{TS}(T_i) \ge \text{W-timestamp}(Q)$: The read is executed, and $\text{R-timestamp}(Q) = \max(\text{R-timestamp}(Q), \text{TS}(T_i))$.
2. **Transaction $T_i$ issues $\text{write}(Q)$**:
   - If $\text{TS}(T_i) < \text{R-timestamp}(Q)$: The value produced by $T_i$ was needed earlier, but has already been read. $T_i$ is **rejected and aborted**.
   - If $\text{TS}(T_i) < \text{W-timestamp}(Q)$: $T_i$ is attempting to write an obsolete value. $T_i$ is **rejected and aborted**.
   - Otherwise: The write is executed, and $\text{W-timestamp}(Q) = \text{TS}(T_i)$.

### 4.2 Thomas Write Rule (Optimization)
If $\text{TS}(T_i) < \text{W-timestamp}(Q)$ during a $\text{write}(Q)$ operation:
- Instead of aborting $T_i$, the system simply **ignores (discards) the write**.
- **Theoretical Justification**: Any subsequent read will see the value written by a transaction with a higher timestamp; thus, $T_i$'s write is obsolete and its omission is view-serializable.

---

## 5. MongoDB & WiredTiger Implementation Architecture

MongoDB departs radically from monolithic textbook RDBMS locking by utilizing **Multi-Version Concurrency Control (MVCC)** inside the WiredTiger storage engine:

### 5.1 Document-Level Concurrency & Intent Latches
- MongoDB uses multiple granularity locking at the Global, Database, and Collection levels:
  - Global Lock: Protects administrative operations (e.g., shutdown, repair).
  - Database Lock: `IS` / `IX` for normal operations.
  - Collection Lock: `IS` for queries, `IX` for document updates.
- **Document Level**: At the individual document level, WiredTiger does **NOT** maintain heavy lock tables. Instead, WiredTiger uses in-memory version chains and hazard pointers (lock-free concurrency).

### 5.2 WiredTiger Execution Tickets
To prevent operating system thread starvation and CPU cache trashing under heavy concurrent workloads:
- WiredTiger enforces a **Ticket System**:
  - Default Read Tickets: **128 concurrent read slots**.
  - Default Write Tickets: **128 concurrent write slots**.
- When 128 concurrent write operations are executing, additional write operations queue outside the storage engine rather than acquiring locks and degrading memory latency.

### 5.3 Optimistic Concurrency Control (OCC) & WriteConflict Handling
In multi-document transactions:
1. Operations execute against private in-memory snapshot buffers.
2. If two concurrent transactions attempt to modify the same document simultaneously, WiredTiger detects the collision and raises a **`WriteConflict` exception** (code 112) or attaches the `TransientTransactionError` label.
3. Rather than holding blocking exclusive locks indefinitely, MongoDB relies on client retry loops with exponential backoff:

```python
for attempt in range(max_retries):
    try:
        with client.start_session() as s:
            with s.start_transaction(read_concern=ReadConcern("snapshot")):
                # Transaction logic
                s.commit_transaction()
                break
    except (WriteConflictError, OperationFailure) as exc:
        time.sleep(backoff_jitter(attempt))
```

---

## 6. Comparison: ANSI SQL vs. MongoDB Isolation Levels

| ANSI SQL Isolation Level | Dirty Reads Allowed? | Non-Repeatable Reads? | Phantom Reads? | Equivalent MongoDB Read Concern |
| :--- | :---: | :---: | :---: | :--- |
| **Read Uncommitted** | **Yes** | **Yes** | **Yes** | Not supported for transactions (WiredTiger never allows dirty reads). |
| **Read Committed** | No | **Yes** | **Yes** | `readConcern: "local"` or `"majority"` (reads committed data). |
| **Repeatable Read** | No | No | **Yes** | `readConcern: "snapshot"` (transaction level). |
| **Serializable** | No | No | No | `readConcern: "snapshot"` + `writeConcern: "majority"` + optimistic retry loops. |
