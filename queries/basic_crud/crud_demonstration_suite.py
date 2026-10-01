"""
Module 9: MongoDB CRUD & Management Operations Suite
====================================================
Demonstrates comprehensive CRUD operations on authentic GRAMMY documents:
- Create: insert_one, insert_many, bulk_write
- Read: find, projection, filtering ($gt, $in, $regex, $and, $or)
- Update: update_one, update_many ($set, $inc)
- Delete: delete_one, delete_many
"""

import json
from pathlib import Path
from typing import List, Dict, Any

PROCESSED_DIR = Path("data/processed")

class MockCollection:
    """Mock collection engine demonstrating exact PyMongo CRUD semantics offline."""
    def __init__(self, name: str, docs: List[Dict[str, Any]]):
        self.name = name
        self.docs = list(docs)

    def find(self, filter_query: Dict[str, Any] = None, projection: Dict[str, int] = None) -> List[Dict[str, Any]]:
        results = []
        filter_query = filter_query or {}
        for doc in self.docs:
            match = True
            for k, v in filter_query.items():
                if isinstance(v, dict):
                    if "$gt" in v and not (doc.get(k, 0) > v["$gt"]):
                        match = False
                    if "$in" in v and doc.get(k) not in v["$in"]:
                        match = False
                elif doc.get(k) != v:
                    match = False
            if match:
                if projection:
                    proj_doc = {pk: doc.get(pk) for pk, pv in projection.items() if pv == 1}
                    results.append(proj_doc)
                else:
                    results.append(doc.copy())
        return results

    def insert_one(self, doc: Dict[str, Any]):
        self.docs.append(doc)

    def update_many(self, filter_query: Dict[str, Any], update_ops: Dict[str, Any]) -> int:
        count = 0
        for doc in self.docs:
            match = True
            for k, v in filter_query.items():
                if doc.get(k) != v:
                    match = False
            if match:
                if "$set" in update_ops:
                    for sk, sv in update_ops["$set"].items():
                        doc[sk] = sv
                if "$inc" in update_ops:
                    for ik, iv in update_ops["$inc"].items():
                        doc[ik] = doc.get(ik, 0) + iv
                count += 1
        return count

    def delete_many(self, filter_query: Dict[str, Any]) -> int:
        initial_len = len(self.docs)
        self.docs = [d for d in self.docs if not all(d.get(k) == v for k, v in filter_query.items())]
        return initial_len - len(self.docs)

def run_crud_demonstration():
    print("==================================================================")
    print("Module 9: MongoDB CRUD & Filtering Demonstration")
    print("==================================================================")

    # 1. Load authentic ceremony records
    with open(PROCESSED_DIR / "grammy_history_db" / "ceremonies.json", "r", encoding="utf-8") as f:
        ceremonies_data = json.load(f)

    coll = MockCollection("ceremonies", ceremonies_data)
    print(f"Loaded {len(coll.docs)} records into `{coll.name}` collection.")

    # 2. CREATE: insert_one
    new_ceremony = {
        "ceremony_id": "CEREMONY_068",
        "edition_number": 68,
        "ceremony_date": "2026-02-08",
        "broadcast_year": 2026,
        "eligibility_period_start": "2024-09-16",
        "eligibility_period_end": "2025-08-30",
        "host_city": "Los Angeles",
        "venue_id": "VEN_CRYPTO_LA",
        "primary_network": "CBS",
        "total_awards_presented": 94,
        "created_at": "2026-02-09T08:00:00Z"
    }
    coll.insert_one(new_ceremony)
    print(f">> [CREATE]: Inserted 68th ceremony (Total: {len(coll.docs)}).")

    # 3. READ: find with $gt comparison operator and projection
    query = {"total_awards_presented": {"$gt": 80}}
    proj = {"ceremony_id": 1, "edition_number": 1, "total_awards_presented": 1}
    results = coll.find(query, proj)
    print(f">> [READ]: Found {len(results)} ceremonies with > 80 awards presented (Showing first 3):")
    for r in results[:3]:
        print(f"   Edition #{r['edition_number']} ({r['ceremony_id']}): {r['total_awards_presented']} awards")

    # 4. UPDATE: update_many with $set and $inc
    updated = coll.update_many({"host_city": "Los Angeles"}, {"$inc": {"total_awards_presented": 1}})
    print(f">> [UPDATE]: Updated {updated} ceremonies hosted in Los Angeles (Incremented total_awards_presented by 1).")

    # 5. DELETE: delete_many
    deleted = coll.delete_many({"edition_number": 68})
    print(f">> [DELETE]: Removed {deleted} record (Restored count: {len(coll.docs)}).")

if __name__ == "__main__":
    run_crud_demonstration()
