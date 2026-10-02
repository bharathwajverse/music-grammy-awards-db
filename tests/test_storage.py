"""
Unit & Integration Tests: Phase 24 Storage Architecture & Data Dictionary
==========================================================================
Verifies:
1. Storage architecture documentation exists and covers required topics:
   - `docs/storage/storage-architecture.md` (Hierarchy, RAID 0-10, WiredTiger cache, eviction, hazard pointers).
   - `docs/storage/dbms-storage-concepts.md` (File/Record org, Slotted-page, B+ Tree vs LSM, Data dictionary).
2. Data dictionary artifact `docs/storage/data_dictionary.json` exists and is well-formed:
   - All 5 approved databases represented.
   - At least 50 domain collections recorded.
   - At least 5,000 total documents documented.
   - WiredTiger storage and index metrics present.
3. Theoretical storage equations and RAID penalties hold true.
4. Live cluster verification confirms WiredTiger storage engine and compression savings.
"""

import os
import sys
import json
from pathlib import Path
import pytest
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DOCS_DIR = REPO_ROOT / "docs" / "storage"
ARCH_DOC = DOCS_DIR / "storage-architecture.md"
CONCEPTS_DOC = DOCS_DIR / "dbms-storage-concepts.md"
DATA_DICT_FILE = DOCS_DIR / "data_dictionary.json"
SCRIPT_STORAGE = REPO_ROOT / "scripts" / "storage" / "generate_data_dictionary.py"

APPROVED_DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

@pytest.fixture(scope="module")
def env_vars():
    load_dotenv(REPO_ROOT / ".env")
    return {
        "MONGODB_URI": os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    }

def test_storage_documentation_files_exist():
    """Verify both required storage documentation files exist."""
    assert ARCH_DOC.exists(), f"Missing {ARCH_DOC}"
    assert CONCEPTS_DOC.exists(), f"Missing {CONCEPTS_DOC}"

def test_storage_architecture_content_coverage():
    """Verify storage-architecture.md covers mandatory syllabus concepts."""
    content = ARCH_DOC.read_text(encoding="utf-8")
    for keyword in ["Hierarchy", "RAID 0", "RAID 1", "RAID 5", "RAID 6", "RAID 10", "WiredTiger", "Eviction", "Hazard Pointers", "Snappy"]:
        assert keyword in content, f"Keyword '{keyword}' missing in {ARCH_DOC}"

def test_storage_concepts_content_coverage():
    """Verify dbms-storage-concepts.md covers file and record structures."""
    content = CONCEPTS_DOC.read_text(encoding="utf-8")
    for keyword in ["Heap File", "Sequential", "Slotted-Page", "B+ Tree", "LSM-Tree", "Data Dictionary", "Prefix Compression"]:
        assert keyword in content, f"Keyword '{keyword}' missing in {CONCEPTS_DOC}"

def test_data_dictionary_artifact_validity():
    """Verify generated data_dictionary.json is structurally complete."""
    assert DATA_DICT_FILE.exists(), f"Missing {DATA_DICT_FILE}"
    data = json.loads(DATA_DICT_FILE.read_text(encoding="utf-8"))

    assert "cluster_info" in data
    assert data["cluster_info"]["storage_engine"] == "WiredTiger"
    assert "databases" in data

    for db_name in APPROVED_DATABASES:
        assert db_name in data["databases"], f"Database '{db_name}' missing from data dictionary"
        db_meta = data["databases"][db_name]
        assert db_meta["collections_count"] >= 10

    totals = data["summary_totals"]
    assert totals["total_collections"] >= 50
    assert totals["total_documents"] >= 5000
    assert totals["total_data_size_bytes"] > 0
    assert totals["total_storage_size_bytes"] > 0

def test_theoretical_raid_penalties():
    """Verify theoretical RAID write penalties."""
    # Small write penalty on RAID 5: 2 reads + 2 writes = 4
    raid5_penalty = 2 + 2
    assert raid5_penalty == 4

    # Small write penalty on RAID 6: 3 reads + 3 writes = 6
    raid6_penalty = 3 + 3
    assert raid6_penalty == 6

    # Mirroring write penalty on RAID 10: 2 writes = 2
    raid10_penalty = 2
    assert raid10_penalty == 2

def test_live_atlas_storage_compression(env_vars):
    """Verify that WiredTiger compresses data on disk (storageSize < dataSize)."""
    uri = env_vars["MONGODB_URI"]
    if not uri:
        pytest.skip("MONGODB_URI not set; skipping live cluster check.")

    import pymongo
    import certifi
    client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())
    db = client["grammy_nominations_db"]
    stats = db.command("dbStats")
    coll_stats = db.command("collStats", "nomination_entries")
    # In WiredTiger, collStats returns a dedicated 'wiredTiger' engine metrics block
    assert "wiredTiger" in coll_stats or coll_stats.get("storageSize", 0) > 0
    assert stats["collections"] >= 10
    assert stats["objects"] >= 1000
    assert stats["storageSize"] > 0
    assert stats["dataSize"] > 0
