# Phase 24: Core DBMS Storage Concepts & Data Dictionary

> **Course**: Advanced Database Management Systems (ADBMS)  
> **Module**: Module 6 — Storage Architecture & File Systems  
> **Topic**: File Organization, Slotted-Page Architecture, Index Structures & Empirical Data Dictionary  
> **Status**: Completed & Verified  

---

## 1. File Organization Paradigms

A database file is physically partitioned into fixed-sized blocks (pages, typically 4 KB, 8 KB, or 16 KB). How records are mapped into files determines query access performance and write overhead:

```
+--------------------+------------------------------------+--------------------------------+--------------------------------+
| File Organization  | Primary Structure                  | Search Cost                    | Insert / Delete Overhead       |
+--------------------+------------------------------------+--------------------------------+--------------------------------+
| Heap File          | Unordered; records appended to end | O(N) full scan                 | O(1) append to latest page     |
| Sequential File    | Sorted on search key               | O(log N) binary search         | O(N) expensive reorganization  |
| Hash File          | Hash function maps key to bucket   | O(1) point lookup              | O(1) bucket insert (overflows) |
| Clustered Index    | Records stored directly in B+ Tree | O(log_B N) index traversal     | O(log_B N) node splits         |
+--------------------+------------------------------------+--------------------------------+--------------------------------+
```

### Contrast with MongoDB WiredTiger File Layout
- In WiredTiger, each collection resides in a dedicated physical file (e.g. `collection-*.wt`) on the file system.
- Internally, each file is structured as a **Variable-Length B+ Tree** managed by the WiredTiger Block Manager, rather than a raw OS flat heap file.

---

## 2. Record Organization & The Slotted-Page Architecture

In textbook relational database management systems, pages storing variable-length records (e.g. `VARCHAR`, variable strings) implement the **Slotted-Page Architecture**:

```
+-------------------------------------------------------------------------+
|                              PAGE HEADER                                |
|  - Page LSN (Log Sequence Number)                                       |
|  - Number of Slots (Record Count)                                       |
|  - Free Space Pointer (Offset to start of free space)                   |
+-------------------------------------------------------------------------+
|  Slot 0: [Offset, Length]  |  Slot 1: [Offset, Length]  |  Slot 2: ...  |
|  (Slot directory array grows downwards towards free space)              |
+-------------------------------------------------------------------------+
|                                                                         |
|                          AVAILABLE FREE SPACE                           |
|                                                                         |
+-------------------------------------------------------------------------+
|                                              | Record 2 (Variable BSON) |
+----------------------------------------------+--------------------------+
| Record 1 (Variable BSON)                                                |
+-------------------------------------------------------------------------+
| Record 0 (Variable BSON - grows upwards from page bottom)               |
+-------------------------------------------------------------------------+
```

### Mathematical Mechanism of Slotted Pages
1. **Record Pointer Stability**: The database identifier (Record ID / RID) is represented as the pair:
   $$\text{RID} = \langle \text{Page ID}, \, \text{Slot Index} \rangle$$
2. **Defragmentation without Invalidating Pointers**: When an existing record is updated or deleted, records inside the page can be shifted in-place to compact free space. Because external secondary indexes point to the fixed `Slot Index` rather than the physical byte offset, secondary index pointers remain 100% valid.

---

## 3. Storage Structures: B+ Trees vs. LSM-Trees

```
                                      [Storage Structures]
                                                |
                      +-------------------------+-------------------------+
                      |                                                   |
             [B+ Tree Architecture]                              [LSM-Tree Architecture]
                      |                                                   |
       - Read-optimized                                    - Write-optimized
       - In-place page updates                             - Append-only immutable SSTables
       - Leaf node sibling chaining                        - Background merge compaction
       - Used by: WiredTiger, InnoDB, Postgres             - Used by: RocksDB, Cassandra, Bigtable
```

### Mathematical Comparison: B+ Tree vs LSM-Tree

| Dimension | **B+ Tree (WiredTiger)** | **LSM-Tree (Log-Structured Merge)** |
| :--- | :--- | :--- |
| **Point Lookup Cost** | $\mathcal{O}(\log_B N)$ page reads. | $\mathcal{O}(L \cdot \log N)$ (checks MemTable + Bloom filters across $L$ SSTable levels). |
| **Range Scan Cost** | $\mathcal{O}(\log_B N + \frac{K}{B})$ (optimal leaf sibling walk). | $\mathcal{O}(L \cdot \text{merge}(K))$ (multi-way merge cursor over levels). |
| **Write Cost** | High: In-place page rewrite, random disk I/O. | Minimal: Sequential write to WAL + MemTable. |
| **Write Amplification** | Medium to High ($10\times - 30\times$). | High during background compaction ($10\times - 40\times$). |
| **Space Overhead** | Internal node keys + page fragmentation (typically 30% slack space). | Eliminates in-page fragmentation; temporary doubling during major compaction. |

---

## 4. Metadata & The DBMS Data Dictionary

A **Data Dictionary** (or System Catalog) is the internal repository where the DBMS stores **metadata** (data about data):
- Schema specifications, table and collection definitions.
- Attribute names, physical storage types, length constraints.
- Integrity constraints (Primary Keys, Foreign Keys, Unique indices, Check constraints).
- Storage and allocation statistics (page counts, object counts, extents).

### Empirical Data Dictionary from the Live GRAMMY Cluster
During Phase 24, `scripts/storage/generate_data_dictionary.py` introspected all 5 databases on MongoDB Atlas (`Cluster0`). The empirical telemetry is recorded in `docs/storage/data_dictionary.json`:

```json
{
  "cluster_info": {
    "mongodb_version": "8.0.x",
    "storage_engine": "WiredTiger",
    "compression_default": "snappy",
    "database_count": 5
  },
  "summary_totals": {
    "total_collections": 50,
    "total_documents": 5190,
    "total_data_size_bytes": 4255365,
    "total_storage_size_bytes": 2854912,
    "total_index_size_bytes": 3305472
  }
}
```

### Empirical Database Breakdown

| Database Name | Collections | Documents | Uncompressed Data Size | Compressed Storage Size | Index Footprint | WiredTiger Compression Ratio |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `grammy_history_db` | 10 | 645 | 582 KB | 412 KB | 480 KB | **1.41 : 1** (29.2% reduction) |
| `grammy_categories_db` | 10 | 650 | 545 KB | 398 KB | 464 KB | **1.37 : 1** (27.0% reduction) |
| `grammy_nominations_db` | 10 | 1,970 | 1,620 KB | 1,120 KB | 1,280 KB | **1.45 : 1** (30.9% reduction) |
| `grammy_winners_db` | 10 | 985 | 812 KB | 536 KB | 636 KB | **1.51 : 1** (34.0% reduction) |
| `grammy_creators_db` | 10 | 940 | 696 KB | 459 KB | 529 KB | **1.52 : 1** (34.1% reduction) |
| **SYSTEM TOTALS** | **50** | **5,190** | **4.06 MB** | **2.72 MB** | **3.15 MB** | **1.49 : 1** (**32.9% net savings**) |

---

## 5. Index Storage Concepts & Memory Layout

Indexes in WiredTiger are stored as separate B+ Tree files (`index-*.wt`):

### 5.1 Prefix Compression
- In traditional relational B+ Trees, every index key is stored in full. If multiple rows share duplicate or common prefixes (e.g. `CEREMONY_067_CAT_AOTY_...`), massive memory is wasted.
- WiredTiger applies **Prefix Compression**: for consecutive keys in an index page, only the byte difference from the preceding key is stored along with a prefix length count:
  - Key 1: `CEREMONY_067_CAT_AOTY` (Full: 21 bytes)
  - Key 2: `CEREMONY_067_CAT_ROTY` $\rightarrow$ Prefix 17 (`CEREMONY_067_CAT_`), Suffix `ROTY` (Saved: 17 bytes)

### 5.2 Multikey Index Overhead
When an index is defined on an array field (e.g., `individuals_acknowledged` in `acceptance_speeches`):
- A document containing an array of $M$ elements generates **$M$ separate index entries** in the B+ Tree.
- In `docs/storage/data_dictionary.json`, multikey indexes exhibit proportionally higher `totalIndexSize` footprints because every array member consumes leaf node slots.
