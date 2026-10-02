# Phase 24: Enterprise Storage Architecture & WiredTiger Storage Engine

> **Course**: Advanced Database Management Systems (ADBMS)  
> **Module**: Module 6 — Storage Architecture & File Systems  
> **Topic**: Memory Hierarchy, RAID Arrays & WiredTiger Internal Storage Engine  
> **Status**: Completed & Verified  

---

## 1. Physical Memory & Storage Hierarchy

Modern database management systems are engineered around the physical constraints of the memory hierarchy. Disk access is orders of magnitude slower than semiconductor main memory; consequently, DBMS buffer management, page layouts, and eviction policies are designed to minimize disk I/O operations.

```
       +------------------------------------+  ~ 0.5 - 1 ns
       |          CPU Registers             |  < 1 KB
       +------------------------------------+
       |          L1 / L2 / L3 Cache        |  ~ 1 - 20 ns, up to 64 MB
       +------------------------------------+
       |       Main Memory (DRAM)           |  ~ 50 - 100 ns, 16 GB - 1 TB
       +------------------------------------+
       |   Non-Volatile Flash (NVMe SSD)    |  ~ 10 - 100 µs, 1 TB - 10 TB
       +------------------------------------+
       |     Magnetic Hard Disk (HDD)       |  ~ 5 - 10 ms, 4 TB - 24 TB
       +------------------------------------+
       |    Optical / Magnetic Tape Cold    |  ~ Seconds to Minutes, Petabytes
       +------------------------------------+
```

### Access Latency Scale Factor (The "Human Scale" Metaphor)
If 1 CPU clock cycle (0.3 ns) is scaled to 1 second:
- **L1 Cache reference (1 ns)**: ~ 3 seconds.
- **Main Memory DRAM reference (100 ns)**: ~ 5 minutes.
- **NVMe SSD random read (50 µs)**: ~ 1.9 days.
- **Magnetic HDD seek (10 ms)**: ~ 12 months (1 year).

Because fetching an unbuffered page from a mechanical disk or remote block volume takes the equivalent of a full year relative to CPU execution, the primary design goal of database storage engines is maximizing **Cache Hit Ratio**:

$$\text{Cache Hit Ratio} = \frac{\text{Pages Read from Memory Cache}}{\text{Total Page Requests}} \times 100\% \ge 99.5\%$$

---

## 2. Redundant Array of Independent Disks (RAID)

Enterprise database servers organize secondary storage into **RAID arrays** to combine multiple physical disk drives into a single logical volume, achieving performance scaling via data striping and fault tolerance via parity or mirroring.

```
+------------+-------------------------+--------------------+---------------------+----------------------+
| RAID Level | Architecture Scheme     | Storage Efficiency | Fault Tolerance     | Write Penalty        |
+------------+-------------------------+--------------------+---------------------+----------------------+
| RAID 0     | Pure Striping           | 100% (n / n)       | 0 disks (None)      | None (1 I/O)         |
| RAID 1     | Pure Mirroring          | 50% (1 / 2)        | 1 disk per mirror   | 2 I/Os (Dual write)  |
| RAID 5     | Distributed Parity      | (n - 1) / n        | 1 disk failure      | 4 I/Os (2R + 2W)     |
| RAID 6     | Dual Distributed Parity | (n - 2) / n        | 2 disk failures     | 6 I/Os (3R + 3W)     |
| RAID 10    | Striped Mirrors (1 + 0) | 50% (n / 2)        | Up to n/2 disks     | 2 I/Os               |
+------------+-------------------------+--------------------+---------------------+----------------------+
```

### Mathematical Formulations of RAID Levels

#### 1. RAID 5 Parity Calculation
Data blocks $D_1, D_2, \dots, D_{n-1}$ are striped across $n-1$ disks, and parity $P$ is written to disk $n$:
$$P = D_1 \oplus D_2 \oplus \dots \oplus D_{n-1}$$
If disk $k$ fails, the missing data $D_k$ is reconstructed by XOR-ing the surviving data blocks with the parity block:
$$D_k = D_1 \oplus \dots \oplus D_{k-1} \oplus D_{k+1} \oplus \dots \oplus D_{n-1} \oplus P$$
- **RAID 5 Small Write Penalty**: Updating a single block $D_k \rightarrow D_k'$ requires reading old data and old parity, computing new parity $P' = P \oplus D_k \oplus D_k'$, and writing new data and new parity ($2 \text{ reads} + 2 \text{ writes} = 4 \text{ physical I/Os}$).

#### 2. RAID 6 Dual Parity
RAID 6 utilizes two independent parity blocks: $P$ (standard horizontal XOR parity) and $Q$ (Reed-Solomon Galois Field $\text{GF}(2^8)$ code or diagonal parity). It survives simultaneous failure of any 2 disks in the array.

#### 3. Enterprise Recommendation for Database Workloads
For transaction-intensive database workloads (such as MongoDB Atlas under heavy write traffic), **RAID 10** is the industry standard because it eliminates the read-modify-write parity penalty of RAID 5/6 while providing optimal read throughput via multi-spindle striping.

---

## 3. MongoDB WiredTiger Storage Engine Architecture

MongoDB replaced the legacy MMAPv1 engine with **WiredTiger**, an advanced, cache-centric, lock-free storage engine designed specifically for modern multi-core servers and high-density NVMe storage.

```
+-----------------------------------------------------------------------------------+
|                           MongoDB Query Execution Engine                          |
+-----------------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------------+
|                           WiredTiger In-Memory Cache                              |
|  - In-memory B+ Trees (Uncompressed BSON documents)                               |
|  - Hazard Pointers (Lock-free concurrent page access)                             |
|  - Lookaside Table / History Store (MVCC past versions)                           |
+-----------------------------------------------------------------------------------+
          |                                                       |
          | (Periodic Eviction Server)                            | (Write-Ahead Log)
          v                                                       v
+------------------------------------+                 +----------------------------+
|     WiredTiger Block Manager       |                 |  WiredTiger Journal (WAL)  |
|  - Block allocation & defragment   |                 |  - Append-only write log   |
|  - Snappy / zlib / zstd compress   |                 |  - Checkpoint sync (60s)   |
+------------------------------------+                 +----------------------------+
                  |                                                   |
                  v                                                   v
+-----------------------------------------------------------------------------------+
|                          Physical Storage (Disk / SSD)                            |
|  - Collection files: collection-*.wt                                              |
|  - Index files: index-*.wt                                                        |
+-----------------------------------------------------------------------------------+
```

### 3.1 WiredTiger In-Memory Cache Architecture
- **Default Cache Sizing**:
  $$\text{Cache Size} = \max\left(0.5 \times (\text{Total RAM} - 1\text{ GB}), \, 256\text{ MB}\right)$$
- **Format in Cache**: Documents reside in the cache in **uncompressed BSON representation**. This eliminates CPU decompression overhead on repeated cache hits.
- **Hazard Pointers**: WiredTiger employs hazard pointers to achieve lock-free concurrent reads: when a query thread reads an in-memory B-tree page, it publishes a hazard pointer. The background eviction server verifies hazard pointer lists before evicting or reorganizing any memory page, preventing dangling pointer segmentation faults without blocking reader threads with mutexes.

### 3.2 Cache Eviction Server Triggers
Background eviction worker threads continuously monitor dirty and total cache consumption:
1. **Normal Eviction**: Begins when cache usage reaches **80%** of capacity.
2. **Aggressive Eviction**: Begins when dirty (unwritten) pages reach **20%** of cache.
3. **Application Thread Throttling**: If cache reaches **95%** or dirty pages reach **90%**, client operations are throttled, forcing client worker threads to assist with page evictions before accepting new writes.

### 3.3 Block Manager & Compression Algorithms
When dirty pages are flushed from the cache to the file system, the **Block Manager** writes variable-length blocks:
- **Snappy Compression (Default for Collections)**: Optimized for CPU performance with moderate compression ratios (~50% footprint reduction).
- **Prefix Compression (Default for Indexes)**: Strips redundant prefix keys from B+ Tree index entries, dramatically reducing index memory footprints.
- **zlib / zstd (High Density Option)**: Delivers superior compression ratios (~70% reduction) at the expense of higher CPU decompression latency.
