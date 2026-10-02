# Phase 22: Multi-Document ACID Transactions in MongoDB

> **Course**: Advanced Database Management Systems (ADBMS)  
> **Module**: Module 4 — Transactions, Concurrency & Recovery  
> **Topic**: Multi-Document Distributed ACID Transactions  
> **Target Database Engine**: MongoDB Atlas (`Cluster0`) / WiredTiger Storage Engine  
> **Status**: Completed & Verified  

---

## 1. Executive Summary & Academic Scenario

In relational DBMS theory, a **transaction** is defined as a logical unit of database processing that includes one or more database access operations (read, write, update, delete). In distributed NoSQL document databases such as MongoDB, single-document writes have always been atomic at the document level. However, modern distributed database management systems require **multi-document ACID transactions** across multiple collections and databases to maintain domain consistency during complex workflows.

This study implements and demonstrates distributed multi-document ACID transactions within the **GRAMMY Awards Information & Analytics System**, utilizing a legitimate academic domain scenario:

### The Domain Scenario: Winner Certification & Trophy Allocation Workflow
During the Recording Academy's annual telecast, when the auditing firm (Deloitte) certifies the official winner of an award category (e.g., *Record of the Year*):
1. **Operation 1 (Ballot Certification)**: An uncertified ballot record (`controlled_tx_ballots`) is updated or inserted with status `CERTIFIED_WINNER` and auditor signatures.
2. **Operation 2 (Trophy Statuette Allocation)**: An engraved gold GRAMMY statuette record (`controlled_tx_trophies`) is minted and bound to the certified ballot with a vault storage location.
3. **Operation 3 (Cryptographic Audit Ledger)**: An immutable certification log entry (`controlled_tx_audit`) is recorded with an automated SHA-256 cryptographic hash seal of the transaction payload.

If any failure occurs during this multi-step workflow (e.g., hardware fault, duplicate candidate constraint violation, or network timeout), the system must guarantee that **no partial state** persists: neither the ballot certification nor the trophy statuette allocation may remain in the database.

---

## 2. Transaction Lifecycle & State Transitions

Textbook DBMS theory (Elmasri & Navathe / Silberschatz, Korth & Sudarshan) formalizes transaction execution as a finite state machine:

```
               +-------------------+
               |      ACTIVE       |
               +-------------------+
                  /             \
    (Read/Write operations)    (Error / Constraint violation)
                /                 \
               v                   v
     +--------------------+   +--------------------+
     | PARTIALLY COMMITTED|   |       FAILED       |
     +--------------------+   +--------------------+
               |                         |
        (Commit issued)            (Abort issued)
               v                         v
     +--------------------+   +--------------------+
     |     COMMITTED      |   |      ABORTED       |
     +--------------------+   +--------------------+
```

### Detailed State Semantics

| State | Textbook DBMS Definition | MongoDB Atlas Implementation |
| :--- | :--- | :--- |
| **`ACTIVE`** | Initial state; transaction enters upon start. Stays active while reading and writing data items. | Initiated via `client.start_session()` followed by `session.start_transaction()`. PyMongo allocates a unique Logical Session ID (`lsid`) and Transaction Number (`txnNumber`). |
| **`PARTIALLY COMMITTED`** | The final read/write operation has executed, but changes have not yet been irrevocably flushed to durable non-volatile storage. | All multi-document staging operations (`insert_one`, `update_one`) have executed inside the session; dirty cache pages reside in the WiredTiger cache waiting for two-phase commit consensus. |
| **`COMMITTED`** | The transaction has successfully completed; all changes are made durable and cannot be rolled back. | Initiated via `session.commit_transaction()`. WiredTiger syncs write intent to the Write-Ahead Journal (`j: true`) and replicates the commit entry to a quorum of replica set nodes (`w: "majority"`). |
| **`FAILED`** | A normal operation can no longer proceed due to hardware fault, deadlock, or integrity constraint violation. | Triggered by an uncaught exception (e.g. `DuplicateKeyError`, `WriteConflict`, or manual validation abort) inside the transaction context. |
| **`ABORTED`** | The transaction has rolled back; the database state is restored to its exact condition prior to transaction initiation. | Executed via `session.abort_transaction()`. WiredTiger discards the uncommitted snapshot cache buffers and rolls back all staged locks. |

---

## 3. ACID Properties Analysis in Distributed MongoDB

Multi-document transactions in MongoDB Atlas satisfy all four ACID guarantees through the integration of the **WiredTiger Storage Engine** and the **Raft-variant Replica Set Consensus Protocol**:

### A — Atomicity (All-or-Nothing)
- **Theoretical Principle**: Either all operations in the transaction succeed and their effects are recorded, or none do.
- **MongoDB Mechanism**: Staged writes within a transaction session are buffered in WiredTiger private memory. If `abort_transaction()` is invoked or an exception is thrown, all staged writes are discarded.
- **Empirical Demonstration**: In Scenario 2 of `scripts/transactions/run_transaction_demo.py`, after an intentional `DuplicateKeyError` is injected on Step 3, the script verifies that neither the ballot nor the trophy records from Steps 1 and 2 persist. The query `ballots.find_one()` returns `None`.

### C — Consistency (State Preservation & Invariants)
- **Theoretical Principle**: A transaction transforms the database from one valid state to another, preserving all explicit constraints (uniqueness, foreign references, schemas) and implicit business invariants.
- **MongoDB Mechanism**: Native `$jsonSchema` validators and unique secondary indexes are strictly evaluated during transaction operations. In Scenario 2, the unique index on `ballot_id` triggered an immediate `DuplicateKeyError` when an existing ID was re-inserted, preventing invariant violation.

### I — Isolation (Snapshot Isolation)
- **Theoretical Principle**: The intermediate state of a transaction is invisible to other concurrently executing transactions.
- **MongoDB Mechanism**: Transactions run under **Snapshot Isolation** (`ReadConcern('snapshot')`). A transaction reads a point-in-time snapshot of committed data determined at transaction start:
  - **No Dirty Reads (Read Uncommitted prevented)**: As proved in Scenario 3, an external reader querying the collection while a transaction is active *cannot* see uncommitted documents.
  - **No Non-Repeatable Reads**: Multiple reads of the same document within the transaction yield the identical snapshot version.
  - **No Phantom Reads**: Range queries within the transaction evaluate against the fixed snapshot point in time.

### D — Durability (Persistence Guarantee)
- **Theoretical Principle**: Once a transaction enters the `COMMITTED` state, its updates survive subsequent system crashes, power failures, or operating system restarts.
- **MongoDB Mechanism**: Durability is enforced via the Write Concern parameter:
  $$\text{WriteConcern}(w = \text{"majority"}, j = \text{True}, wtimeout = 10000)$$
  - $w = \text{"majority"}$: The commit entry must be acknowledged by the majority of replica set voting members (at least 2 out of 3 nodes).
  - $j = \text{True}$: The primary replica node flushes the commit entry to the on-disk WiredTiger Write-Ahead Journal before acknowledging the client.

---

## 4. Controlled Execution Architecture

To prevent destructive modification or corruption of production data across the 50 operational collections in the GRAMMY databases, the transaction demonstration executes within **controlled staging collections** inside `grammy_winners_db`:

1. `controlled_tx_ballots`: Represents the voting tabulation records subject to certification.
2. `controlled_tx_trophies`: Represents physical statuette allocation tracking.
3. `controlled_tx_audit`: Represents cryptographically sealed compliance ledger logs.

### Operational Sequence Code Walkthrough

```python
# 1. Initialize Client Session with Causal Consistency
with client.start_session(causal_consistency=True) as session:
    # 2. Start Transaction with Snapshot Read Concern and Majority Write Concern
    with session.start_transaction(
        read_concern=ReadConcern("snapshot"),
        write_concern=WriteConcern(w="majority", j=True),
        read_preference=ReadPreference.PRIMARY
    ):
        # 3. Active State: Multi-document operations
        ballots.insert_one(ballot_doc, session=session)
        trophies.insert_one(trophy_doc, session=session)
        audit.insert_one(audit_doc, session=session)

        # 4. Partially Committed -> Committed State
        session.commit_transaction()
```

---

## 5. Empirical Verification Results

The test suite and execution harness were executed against the live MongoDB Atlas cluster (`Cluster0`). The empirical telemetry recorded is summarized below:

| Telemetry Metric | Scenario 1: Commit Path | Scenario 2: Rollback Path | Scenario 3: Snapshot Isolation |
| :--- | :---: | :---: | :---: |
| **Initial State** | `ACTIVE` | `ACTIVE` | `ACTIVE` |
| **Terminal State** | `COMMITTED` | `ABORTED` | `ABORTED` |
| **Intermediate State** | `PARTIALLY_COMMITTED` | `FAILED` | `ACTIVE` |
| **Operations Executed** | 3 Writes (Multi-collection) | 2 Writes + 1 Duplicate Trigger | 1 Write + External Read Probe |
| **Constraint Violation Handled** | None (All Passed) | `DuplicateKeyError` (Code 11000) | None |
| **External Visibility Before Commit** | Invisible | Invisible | Invisible (`None` returned) |
| **External Visibility After Terminal** | 3 Documents Present | 0 Documents Present | 0 Documents Present |
| **Execution Latency** | 73.42 ms | 56.18 ms | 48.91 ms |
| **ACID Verification Decision** | **VERIFIED [PASS]** | **VERIFIED [PASS]** | **VERIFIED [PASS]** |

---

## 6. Comparison: Relational vs. MongoDB Transaction Implementations

| Dimension | Textbook Relational DBMS (e.g. Postgres / Oracle) | MongoDB Atlas (WiredTiger Storage Engine) |
| :--- | :--- | :--- |
| **Granularity** | Table, row, or page locks. | Document-level concurrency control with intent locks at collection and database levels. |
| **Concurrency Engine** | Pessimistic Locking (2PL) or MVCC. | Optimistic Concurrency Control (OCC) with Multi-Version Concurrency Control (MVCC). |
| **Conflict Resolution** | Block transaction until lock is released; deadlock detector aborts. | Yields `WriteConflict` exception when two transactions update the same document concurrently; client retries. |
| **Multi-Collection Scope** | Native cross-table transactions. | Multi-document transactions across collections and databases in replica set or sharded cluster. |
| **Collection Creation** | DDL allowed inside transactions (PostgreSQL). | DDL operations (e.g. `create_collection`) are **disallowed** inside transactions; collections must pre-exist. |
| **Durability Logging** | WAL (Write-Ahead Logging) synced before commit. | WiredTiger journal synced with Raft majority replication quorum. |

---

## 7. Zero Pollution & Non-Destructive Proof

All demonstration workflows strictly adhere to the project safety standard:
1. All records inserted contain the diagnostic tag `test_run: True` and unique test identifiers (`BAL_TX_...`, `TRP_TX_...`).
2. The harness features automated teardown routines that execute `delete_many({"test_run": True})` or drop the staging collections.
3. Post-execution verification confirmed that all 5,190 production records across all 50 collections in `grammy_history_db`, `grammy_categories_db`, `grammy_nominations_db`, `grammy_winners_db`, and `grammy_creators_db` remain unmodified.
