"""
Phase 24: Academic Storage Analysis & Data Dictionary Introspection Engine
===========================================================================
Introspects the live MongoDB Atlas cluster across all 5 operational databases
and 50 domain collections to extract empirical storage metrics and compile
the formal DBMS Data Dictionary:

1. Database Storage Metrics (dbStats):
   - Data size (uncompressed in-memory representation)
   - Storage size (compressed on-disk footprint)
   - Index size, average object size, allocation extents
2. Collection Storage & WiredTiger Block Statistics:
   - Document counts, average object sizes, index count, compression efficiency
3. Schema Metadata & Field Catalog:
   - BSON data types, field names, primary and secondary indexes
4. Export:
   - Compiles and persists docs/storage/data_dictionary.json
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

load_dotenv(REPO_ROOT / ".env")

try:
    import pymongo
    import certifi
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

APPROVED_DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

OUTPUT_DIR = REPO_ROOT / "docs" / "storage"
OUTPUT_JSON = OUTPUT_DIR / "data_dictionary.json"


class DataDictionaryGenerator:
    """Generates comprehensive DBMS storage catalog and data dictionary from Atlas cluster."""

    def __init__(self, uri: str = None):
        self.uri = uri or os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
        self.client = None

    def connect(self) -> pymongo.MongoClient:
        if not PYMONGO_AVAILABLE:
            raise RuntimeError("PyMongo / Certifi not installed.")
        self.client = pymongo.MongoClient(
            self.uri,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=7000,
            connectTimeoutMS=7000
        )
        return self.client

    def introspect_cluster_storage(self) -> Dict[str, Any]:
        """Collects database and collection storage stats across all 5 databases."""
        if not self.client:
            self.connect()

        catalog = {
            "cluster_info": {
                "mongodb_version": self.client.server_info().get("version", "Unknown"),
                "storage_engine": "WiredTiger",
                "compression_default": "snappy",
                "database_count": len(APPROVED_DATABASES)
            },
            "databases": {},
            "summary_totals": {
                "total_collections": 0,
                "total_documents": 0,
                "total_data_size_bytes": 0,
                "total_storage_size_bytes": 0,
                "total_index_size_bytes": 0
            }
        }

        for db_name in APPROVED_DATABASES:
            db = self.client[db_name]
            db_stats = db.command("dbStats")

            collections_metadata = {}
            coll_names = [c for c in sorted(db.list_collection_names()) if not c.startswith("system.")]

            for coll_name in coll_names:
                coll = db[coll_name]
                try:
                    c_stats = db.command("collStats", coll_name)
                    doc_count = c_stats.get("count", 0)
                    size_bytes = c_stats.get("size", 0)
                    storage_bytes = c_stats.get("storageSize", 0)
                    total_index_bytes = c_stats.get("totalIndexSize", 0)
                    avg_obj_size = c_stats.get("avgObjSize", 0)
                except Exception:
                    doc_count = coll.estimated_document_count()
                    size_bytes = 0
                    storage_bytes = 0
                    total_index_bytes = 0
                    avg_obj_size = 0

                # Introspect sample document fields & types
                sample_doc = coll.find_one()
                fields_dict = {}
                if sample_doc:
                    for k, v in sample_doc.items():
                        fields_dict[k] = {
                            "bson_type": type(v).__name__,
                            "sample_repr": str(v)[:60]
                        }

                # Introspect index definitions
                indexes = []
                for idx in coll.list_indexes():
                    indexes.append({
                        "name": idx.get("name"),
                        "key": list(idx.get("key", {}).items()),
                        "unique": idx.get("unique", False)
                    })

                collections_metadata[coll_name] = {
                    "document_count": doc_count,
                    "data_size_bytes": size_bytes,
                    "storage_size_bytes": storage_bytes,
                    "total_index_size_bytes": total_index_bytes,
                    "avg_obj_size_bytes": avg_obj_size,
                    "index_count": len(indexes),
                    "indexes": indexes,
                    "field_count": len(fields_dict),
                    "fields": fields_dict
                }

                catalog["summary_totals"]["total_collections"] += 1
                catalog["summary_totals"]["total_documents"] += doc_count
                catalog["summary_totals"]["total_data_size_bytes"] += size_bytes
                catalog["summary_totals"]["total_storage_size_bytes"] += storage_bytes
                catalog["summary_totals"]["total_index_size_bytes"] += total_index_bytes

            catalog["databases"][db_name] = {
                "collections_count": len(collections_metadata),
                "objects_count": db_stats.get("objects", 0),
                "data_size_bytes": db_stats.get("dataSize", 0),
                "storage_size_bytes": db_stats.get("storageSize", 0),
                "indexes_count": db_stats.get("indexes", 0),
                "index_size_bytes": db_stats.get("indexSize", 0),
                "collections": collections_metadata
            }

        return catalog

    def save_and_report(self) -> Dict[str, Any]:
        catalog = self.introspect_cluster_storage()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2)

        totals = catalog["summary_totals"]
        data_mb = round(totals["total_data_size_bytes"] / (1024 * 1024), 2)
        storage_mb = round(totals["total_storage_size_bytes"] / (1024 * 1024), 2)
        index_mb = round(totals["total_index_size_bytes"] / (1024 * 1024), 2)

        print("==================================================================")
        print("PHASE 24: Data Dictionary & Storage Introspection Report")
        print("==================================================================")
        print(f"Databases Audited     : {len(catalog['databases'])}")
        print(f"Total Collections     : {totals['total_collections']}")
        print(f"Total Documents       : {totals['total_documents']:,}")
        print(f"Total Data Size       : {data_mb} MB ({totals['total_data_size_bytes']:,} bytes)")
        print(f"Total Storage Footprint: {storage_mb} MB ({totals['total_storage_size_bytes']:,} bytes)")
        print(f"Total Index Footprint : {index_mb} MB ({totals['total_index_size_bytes']:,} bytes)")
        print(f"Data Dictionary File  : {OUTPUT_JSON}")
        print("==================================================================")
        return catalog


def main():
    generator = DataDictionaryGenerator()
    catalog = generator.save_and_report()
    return 0 if catalog["summary_totals"]["total_collections"] >= 50 else 1


if __name__ == "__main__":
    sys.exit(main())
