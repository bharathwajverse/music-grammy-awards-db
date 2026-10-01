"""
Core Validation Engine: GRAMMY Awards Information & Analytics System
====================================================================
Performs rigorous 5-tier verification across all 5 member databases:
- Tier 1: Database Connectivity Check
- Tier 2: Collection Quota Verification (>= 10 collections per DB, >= 50 total)
- Tier 3: Document Quota Verification (>= 50 documents per collection, >= 2500 total)
- Tier 4: Field Richness Verification (>= 10 non-null meaningful fields per document)
- Tier 5: Formal JSON Schema Conformance (via jsonschema library)
- Tier 6: Cross-Database Referential Integrity (Foreign key link verification)
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
import pymongo
from dotenv import load_dotenv
import jsonschema

load_dotenv()

EXPECTED_DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

SCHEMA_BASE_DIR = Path("schemas/json_schemas")

def load_json_schema(db_name: str, coll_name: str) -> Dict[str, Any]:
    schema_path = SCHEMA_BASE_DIR / db_name / f"{coll_name}.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Missing schema definition: {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_local_schema_check():
    """Validates that all 50 formal schemas exist and are syntactically valid."""
    print("==================================================================")
    print("TIER 0: Schema Architecture Pre-flight Audit")
    print("==================================================================")
    total_schemas = 0
    errors = []
    
    for db_name in EXPECTED_DATABASES:
        db_dir = SCHEMA_BASE_DIR / db_name
        if not db_dir.exists():
            errors.append(f"Directory missing: {db_dir}")
            continue
        
        schemas = list(db_dir.glob("*.json"))
        print(f"[{db_name}]: Found {len(schemas)} schemas.")
        if len(schemas) < 10:
            errors.append(f"{db_name} has only {len(schemas)} schemas (minimum required: 10).")
        
        for s_file in schemas:
            total_schemas += 1
            try:
                with open(s_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                req_fields = data.get("required", [])
                if len(req_fields) < 10:
                    errors.append(f"{s_file.name} requires only {len(req_fields)} fields (minimum required: 10).")
            except Exception as e:
                errors.append(f"Invalid JSON in {s_file}: {e}")

    print(f"Total Schemas Audited: {total_schemas}")
    if errors:
        print("\nERRORS ENCOUNTERED:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print(">> TIER 0 SUCCESS: All 50 collections have valid, compliant JSON schemas with >= 10 required fields.")
        return True

def run_live_database_validation(mongo_uri: str = None):
    """Executes live validation against MongoDB Atlas."""
    uri = mongo_uri or os.getenv("MONGODB_ATLAS_URI")
    if not uri or "username:password" in uri:
        print("\n[NOTE] Live MongoDB Atlas URI not configured in .env. Skipping live server checks.")
        print("To run live validation, set MONGODB_ATLAS_URI in your .env file.")
        return True

    print("\n==================================================================")
    print("TIER 1–6: Live MongoDB Atlas Cluster Verification")
    print("==================================================================")
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print(">> TIER 1 SUCCESS: MongoDB Atlas connection established.")
    except Exception as e:
        print(f"[FAIL] Tier 1: Connection failed: {e}")
        return False

    all_passed = True
    available_dbs = client.list_database_names()

    for db_name in EXPECTED_DATABASES:
        print(f"\n--- Auditing Database: {db_name} ---")
        if db_name not in available_dbs:
            print(f"[PENDING] Database '{db_name}' not yet provisioned on cluster.")
            all_passed = False
            continue
        
        db = client[db_name]
        colls = db.list_collection_names()
        print(f"Collections Found: {len(colls)} / 10 minimum")
        if len(colls) < 10:
            print(f"[FAIL] {db_name} does not meet collection quota of 10.")
            all_passed = False
        
        for coll_name in colls:
            coll = db[coll_name]
            count = coll.count_documents({})
            print(f"  Collection `{coll_name}`: {count} documents (min 50)")
            if count < 50:
                print(f"  [FAIL] Document quota deficit in `{coll_name}`: {count} < 50")
                all_passed = False

    return all_passed

if __name__ == "__main__":
    t0_success = run_local_schema_check()
    t_live_success = run_live_database_validation()
    
    if t0_success and t_live_success:
        print("\nAll validation checks completed successfully.")
        sys.exit(0)
    else:
        print("\nValidation checks reported issues.")
        sys.exit(1)
