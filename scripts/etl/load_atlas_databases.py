"""
Database Loader: Ingests Processed GRAMMY Data into MongoDB Atlas
=================================================================
Connects to MongoDB Atlas using MONGODB_ATLAS_URI, connects to the 5
member databases, creates the collections, and performs bulk upserts/inserts
of all authentic records.
"""

import os
import sys
import json
from pathlib import Path
import pymongo
from dotenv import load_dotenv

load_dotenv()

PROCESSED_DIR = Path("data/processed")
DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

def load_data_to_atlas():
    uri = os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    if not uri or "username:password" in uri:
        print("[ERROR] Please configure MONGODB_URI or MONGODB_ATLAS_URI in your .env file with your Atlas credentials.")
        sys.exit(1)

    print("Connecting to MongoDB Atlas Cluster...")
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=10000)
    
    try:
        client.admin.command('ping')
        print(">> Connected successfully to MongoDB Atlas.")
    except Exception as e:
        print(f"[FAIL] Unable to connect to Atlas cluster: {e}")
        sys.exit(1)

    total_inserted = 0
    for db_name in DATABASES:
        print(f"\n=======================================================")
        print(f"Loading Database: {db_name}")
        print(f"=======================================================")
        db = client[db_name]
        db_dir = PROCESSED_DIR / db_name
        
        if not db_dir.exists():
            print(f"[WARNING] No processed data directory found for {db_name}")
            continue

        json_files = sorted(db_dir.glob("*.json"))
        for j_file in json_files:
            coll_name = j_file.stem
            with open(j_file, "r", encoding="utf-8") as f:
                records = json.load(f)
            
            coll = db[coll_name]
            # Clear existing data in collection before fresh load to prevent duplication
            coll.delete_many({})
            if records:
                res = coll.insert_many(records)
                count = len(res.inserted_ids)
                total_inserted += count
                print(f"  - Loaded `{coll_name}`: {count} documents inserted.")

    print(f"\n>> Ingestion complete! Total documents loaded across 5 databases: {total_inserted}")

if __name__ == "__main__":
    load_data_to_atlas()
