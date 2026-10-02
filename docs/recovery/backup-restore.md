# Phase 25: Log-Based Recovery, Shadow Paging & Atlas Backup Systems

> **Course**: Advanced Database Management Systems (ADBMS)  
> **Module**: Module 7 — Database Recovery Techniques & Disaster Recovery  
> **Topic**: Write-Ahead Logging (WAL), ARIES Algorithm, Shadow Paging & MongoDB Backup Engine  
> **Status**: Completed & Verified  

---

## 1. Mathematical Foundations of Log-Based Recovery

Log-based recovery systems maintain an append-only sequential record of all database mutations on non-volatile stable storage, termed the **Transaction Log** (or Write-Ahead Log / WAL).

### 1.1 The Write-Ahead Logging (WAL) Invariants
To guarantee Atomicity and Durability (ACID), a DBMS must enforce two fundamental rules:

1. **The Write-Ahead Rule (Undo Rule)**:
   A dirty database buffer page containing modified data item $X$ cannot be flushed to non-volatile disk storage until the log record containing the before-image (old value) of $X$ has been written to stable storage:
   $$\text{DiskWrite}(\text{DataPage}(X)) \implies \text{LogFlush}(\text{LogRecord}(X.\text{old\_value}))$$
2. **The Commit Rule (Redo Rule)**:
   A transaction cannot enter the `COMMITTED` state until all log records associated with its operations (including the `[commit]` log record) have been flushed to stable storage:
   $$\text{TransactionCommit}(T_i) \implies \text{LogFlush}(\text{LogRecord}(T_i.\text{commit}))$$

---

## 2. The ARIES Recovery Algorithm (Mohan et al.)

**ARIES** (*Algorithms for Recovery and Isolation Exploiting Semantics*) is the foundational state-of-the-art recovery algorithm implemented in modern enterprise database engines (DB2, SQL Server, PostgreSQL):

```
       Log Start
           |
           v
       [Checkpoint] -------------------> (Analysis Phase scans forward)
           |                                     |
           v                                     v
       [Oldest recLSN] ----------------> (Redo Phase scans forward)
           |                                     |
           v                                     v
       [CRASH POINT] <------------------ (Undo Phase scans backward)
```

### The Three Phases of ARIES:

#### Phase 1: Analysis Phase
- **Direction**: Scans log **forward** from the most recent checkpoint record to the point of system failure.
- **Objectives**:
  1. Reconstruct the **Transaction Table** (identifying all active transactions that did not commit before the crash, known as the *Loser Set*).
  2. Reconstruct the **Dirty Page Table (DPT)**, tracking all buffer pages modified in memory that were not flushed to disk before the crash, and identifying the smallest Log Sequence Number ($\text{recLSN}$) among them.

#### Phase 2: Redo Phase ("Repeating History")
- **Direction**: Scans log **forward** from the smallest $\text{recLSN}$ identified in the DPT up to the crash point.
- **Rule**: Reapplies the logged operations of **ALL** transactions (including active, committed, and aborted transactions) to restore the exact memory and disk state at the instant of the crash.
- **Idempotency**: If a page's on-disk `pageLSN` is greater than or equal to the log record's `LSN`, the page was already written to disk before the crash; the redo operation is safely skipped.

#### Phase 3: Undo Phase
- **Direction**: Scans log **backward** from the crash point.
- **Rule**: Undoes all operations performed by the uncommitted active transactions (*Loser Set*) in reverse chronological order.
- **Compensation Log Records (CLRs)**: When an undo operation is executed, ARIES writes a special `CLR` to the log containing an `UndoNextLSN` pointer. If the system crashes *during* the recovery process, the recovery manager reads the `CLR` and never repeats the already undone action, guaranteeing bounded recovery time.

---

## 3. Checkpointing Architectures

To prevent log files from growing indefinitely and to bound crash recovery time, the DBMS periodically performs **checkpoints**:

```
+--------------------------+------------------------------------+--------------------------------+
| Checkpoint Mechanism     | Operating Behavior                 | System Performance Impact      |
+--------------------------+------------------------------------+--------------------------------+
| Strict (Quiescent)       | Freezes all active transactions,   | High latency spikes; pauses    |
| Checkpoint               | flushes all dirty pages to disk    | transaction processing         |
+--------------------------+------------------------------------+--------------------------------+
| Non-Quiescent (Fuzzy)    | Writes active Transaction Table    | Zero transaction pauses;       |
| Checkpoint               | and DPT to log without freezing    | asynchronous dirty page flush  |
+--------------------------+------------------------------------+--------------------------------+
```

WiredTiger executes **Fuzzy Checkpoints** every 60 seconds by default, producing an immutable, point-in-time snapshot of the database on disk without blocking concurrent client reads or writes.

---

## 4. Shadow Paging Architecture

**Shadow Paging** is an alternative recovery architecture that avoids write-ahead logging by maintaining two separate page tables:

```
                  +---------------------------+
                  |  DATABASE ROOT POINTER    |
                  +---------------------------+
                                |
               +----------------+----------------+
               |                                 |
               v                                 v
    +--------------------+              +--------------------+
    | CURRENT PAGE TABLE |              | SHADOW PAGE TABLE  |
    +--------------------+              +--------------------+
      Page 1 -> Disk Block 10            Page 1 -> Disk Block 10
      Page 2 -> Disk Block 25 (NEW)      Page 2 -> Disk Block 20 (OLD)
      Page 3 -> Disk Block 30            Page 3 -> Disk Block 30
```

### Operational Mechanism:
1. During transaction execution, reads access disk pages via the **Current Page Table**.
2. When a page is modified, the DBMS allocates an unused physical disk block (Block 25) instead of overwriting the original block (Block 20). The Current Page Table is updated to point to the new block, while the **Shadow Page Table** retains the pointer to the unmodified block.
3. **Commit**: The Database Root Pointer is atomically switched to point to the Current Page Table.
4. **Crash Recovery**: If a crash occurs before commit, the database pointer simply defaults to the Shadow Page Table; all changes made by the uncommitted transaction are discarded instantly with zero undo logging.

### Inherent Disadvantages of Shadow Paging:
- **Severe Page Fragmentation**: Modifying pages relocates them to random physical blocks, completely destroying sequential read clustering.
- **High Memory Overhead**: Duplicating page tables for large databases incurs excessive RAM usage.
- **Concurrent Write Inefficiency**: Synchronizing multiple concurrent write transactions across shared page tables creates severe mutex contention.

---

## 5. MongoDB & Atlas Backup and Restore Capabilities

MongoDB combines low-level storage engine durability with cloud-scale snapshot orchestration:

### 5.1 WiredTiger Write-Ahead Journaling
- **Directory**: Stored on disk under `journal/` as pre-allocated 100 MB write-ahead log files (`WiredTigerLog.*`).
- **Sync Interval**: Buffers are flushed to disk every **100 milliseconds** by default, or immediately upon transactions specifying `j: true`.
- **Crash Recovery**: On startup following an unexpected crash or power loss, WiredTiger automatically reads the journal records since the last 60-second checkpoint, executing a fast redo sequence in under 3 seconds.

### 5.2 Logical Backups: `mongodump` and `mongorestore`
- **Utility**: Produces portable binary BSON archives along with JSON collection metadata.
- **Command Syntax**:
  ```bash
  # Logical archive export with metadata
  mongodump --uri="mongodb+srv://..." --archive="grammy_backup.gz" --gzip
  
  # Lossless restore
  mongorestore --uri="mongodb+srv://..." --archive="grammy_backup.gz" --gzip --drop
  ```

### 5.3 Atlas Cloud Continuous Backups & PITR
- **Underlying Mechanism**: Takes storage volume snapshots (EBS / NVMe snapshots) coupled with a continuous stream of the database **oplog**.
- **Point-in-Time Recovery (PITR)**: Enables database administrators to restore the cluster to any exact second within the retention window (typically 7–35 days) by applying the nearest base snapshot and rolling forward the continuous oplog stream to the precise target millisecond.
