# Phase 25: Failure Scenario Taxonomy & Recovery Runbooks

> **Course**: Advanced Database Management Systems (ADBMS)  
> **Module**: Module 7 — Database Recovery Techniques & Disaster Recovery  
> **Topic**: Catastrophic vs Non-Catastrophic Failure Modes & Operational Runbooks  
> **Status**: Completed & Verified  

---

## 1. Academic Taxonomy of Database Failures

Database system failures are classified into two broad theoretical categories based on the survivability of the physical storage medium:

```
                                      [Database Failure Taxonomy]
                                                   |
                     +-----------------------------+-----------------------------+
                     |                                                           |
       [Non-Catastrophic Failures]                                   [Catastrophic Failures]
                     |                                                           |
       - Memory Volatility (Power Loss)                            - Disk Media Head Crash / NVMe Burnout
       - Operating System Crash / Kernel Panic                     - Physical Natural Disaster (Fire / Flood)
       - Process Abort (SIGKILL)                                   - Data Center Infrastructure Outage
       - Network Partition / Packet Loss                           - Malicious Ransomware / Disk Encryption
       - Solved via: WAL, Journaling & Replica Set Elections       - Solved via: Off-site Snapshots, PITR & Replication
```

---

## 2. Failure Scenarios & Operational Runbooks

### Scenario 1: Primary Replica Sudden Crash / Power Outage (Non-Catastrophic)
- **Failure Description**: The host running the Primary MongoDB replica suffers an unexpected power loss or kernel panic while processing live award winner updates.

```
+-----------------------------------------------------------------------------------+
| 1. DETECTION (T = 0s to T = 2s)                                                   |
|    Remaining secondaries miss heartbeats (heartbeatFrequencyMS = 2000 ms).        |
|    Election timeout triggered at 10,000 ms.                                       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 2. ELECTION & FAILOVER (T = 2s to T = 4s)                                         |
|    Secondary 1 and Secondary 2 initiate Raft-variant election.                     |
|    Secondary 1 has newest optime; receives majority vote (2/3); becomes PRIMARY.  |
|    Application drivers transparently redirect write traffic to new Primary.       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 3. RECOVERY OF CRASHED NODE (T = 30s)                                             |
|    Host reboots; mongod process starts.                                           |
|    WiredTiger inspects journal directory: detects uncheckpointed writes.          |
|    Executes fast WAL Redo scan; rolls back in-memory uncommitted buffers.         |
|    Node contacts new Primary; rejoins replica set as SECONDARY; replays oplog.    |
+-----------------------------------------------------------------------------------+
```

- **Data Loss**: **Zero records lost** for all transactions committed with `w: "majority"`.

---

### Scenario 2: Network Partition & Split-Brain Prevention (Non-Catastrophic)
- **Failure Description**: A network switch failure isolates Node 1 (in Availability Zone A) from Node 2 and Node 3 (in Availability Zones B and C).

```
  [AZ-A: Node 1 (Old Primary)]                 [AZ-B: Node 2]        [AZ-C: Node 3]
              |                                       \                    /
        (ISOLATED)                                     \                  /
              |                                         (CONNECTED QUORUM)
   Cannot see majority (1 < 2)                                    |
              |                                        Elects Node 2 as NEW PRIMARY
     STEPS DOWN TO SECONDARY                                      |
  (Rejects client writes)                             (Accepts client writes)
```

- **Split-Brain Immunity**: Node 1 cannot assemble a majority quorum ($> 3/2 = 2$). It automatically **steps down to a read-only secondary**, preventing divergent conflicting writes.
- **Partition Heal**: When the network heals, Node 1 discovers higher election terms, recognizes Node 2 as Primary, and synchronizes missing oplog entries.

---

### Scenario 3: Accidental Bulk Deletion / Human Operator Error (Logical Failure)
- **Failure Description**: At `14:02:15 UTC`, an operator accidentally executes an unconstrained script dropping documents in production collection `winner_records`:
  ```javascript
  // Disastrous operator error:
  db.winner_records.deleteMany({});
  ```

#### Operational Runbook for Point-in-Time Recovery (PITR):
1. **Declare Incident & Freeze Writes**: Immediately revoke write privileges or pause application ingress to prevent cascading changes.
2. **Identify Mutation Timestamp**: Inspect the database audit log or oplog to identify the exact timestamp of the drop operation:
   $$\text{Drop Timestamp } T_{\text{drop}} = \text{2026-10-02T14:02:15.421Z}$$
3. **Execute Atlas Point-in-Time Restore**:
   - In MongoDB Atlas / Cloud Manager, initiate cluster restore to PITR target:
     $$\text{Restore Target} = \text{2026-10-02T14:02:14.000Z} \quad (T_{\text{drop}} - 1.4\text{s})$$
   - The cloud orchestration engine spins up temporary storage, loads the most recent underlying snapshot, and replays oplog operations up to `14:02:14 UTC`.
4. **Export & Reseed Dropped Collection**:
   - Dump the restored collection `winner_records` from the temporary restore node.
   - Restore records losslessly back into production cluster using `mongorestore`.
   - Run verification hash audits to certify collection parity.

---

### Scenario 4: Physical Media Failure / Complete Disk Destruction (Catastrophic)
- **Failure Description**: Physical NVMe SSD array on a replica set member experiences catastrophic controller burnout and is unrecoverable.

#### Operational Runbook for Node Reconstruction:
1. **Cluster Survival**: The 3-node replica set continues operating normally without interruption on the 2 surviving nodes.
2. **Provision Replacement Container / Node**: Cloud infrastructure or system administrator provisions a new server instance with a clean storage volume.
3. **Initial Sync Protocol**:
   - The newly provisioned node starts with an empty data directory and connects to the existing replica set members.
   - The new node initiates **Initial Sync**:
     a) Clones all databases and collections from the Primary.
     b) Builds all collection indexes in background.
     c) Replays all oplog operations that occurred during the cloning window.
4. **Transition to Healthy Secondary**: The node transitions from `STARTUP2` to `SECONDARY` state; full 3-node redundancy is restored without any downtime.
