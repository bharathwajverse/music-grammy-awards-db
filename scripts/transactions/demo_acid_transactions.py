"""
Module 4: Multi-Document ACID Transactions Demonstration
=========================================================
Demonstrates transaction management in MongoDB Atlas using client sessions:
- Atomicity, Consistency, Isolation, Durability
- Transaction lifecycle states (Active -> Partially Committed -> Committed / Aborted)
- Multi-collection rollback on artificial constraint failure
"""

import os
import sys
import pymongo
from dotenv import load_dotenv

load_dotenv()

def run_acid_transaction_demo():
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri or "username:password" in uri:
        print("[NOTE] MONGODB_ATLAS_URI not set. Demonstrating ACID transaction logic in offline mode.")
        print_theoretical_acid_lifecycle()
        return

    client = pymongo.MongoClient(uri)
    db_noms = client["grammy_nominations_db"]
    db_win = client["grammy_winners_db"]

    print("\n--- Starting Multi-Document ACID Transaction ---")
    with client.start_session() as session:
        with session.start_transaction():
            try:
                # Step 1: Insert new nomination entry under transaction session
                nom_doc = {
                    "nomination_id": "NOM_067_TEST_TXN_01",
                    "ceremony_id": "CEREMONY_067",
                    "category_id": "CAT_AOTY",
                    "work_id": "WRK_TEST_ALBUM",
                    "nomination_year": 2025,
                    "entry_billing_title": "ACID Test Album",
                    "primary_artist_id": "CRT_TEST_ARTIST",
                    "is_winner_flag": True,
                    "ballot_slot_order": 1,
                    "auditor_validation_code": "TXN_AUDIT_PASS",
                    "created_timestamp": "2025-02-15T00:00:00Z"
                }
                db_noms.nomination_entries.insert_one(nom_doc, session=session)
                print(">> [TXN STEP 1]: Nomination entry inserted into grammy_nominations_db.")

                # Step 2: Insert corresponding winner record
                win_doc = {
                    "winner_record_id": "WIN_NOM_067_TEST_TXN_01",
                    "nomination_id": "NOM_067_TEST_TXN_01",
                    "ceremony_id": "CEREMONY_067",
                    "category_id": "CAT_AOTY",
                    "winning_work_id": "WRK_TEST_ALBUM",
                    "primary_artist_id": "CRT_TEST_ARTIST",
                    "broadcast_presentation_order": 1,
                    "presented_live_on_telecast": True,
                    "acceptance_speech_delivered": True,
                    "trophy_statuettes_awarded_count": 1,
                    "verified_timestamp": "2025-02-15T23:00:00Z"
                }
                db_win.winner_records.insert_one(win_doc, session=session)
                print(">> [TXN STEP 2]: Winner record inserted into grammy_winners_db.")

                # Commit transaction
                session.commit_transaction()
                print(">> [COMMITTED]: Both records committed atomically across collections.")
            except Exception as e:
                session.abort_transaction()
                print(f">> [ABORTED]: Transaction rolled back atomically: {e}")

def print_theoretical_acid_lifecycle():
    print("""
    Transaction Lifecycle States in MongoDB / DBMS:
    
    [Active]
       |
       v (Execute operations: insert, update)
    [Partially Committed]
       |
       +---> (Commit command issued & synced to WiredTiger journal) ---> [Committed]
       |
       v (Failure or abort requested)
    [Failed] ---> (Rollback uncommitted changes) ---> [Aborted]
    
    ACID Guarantees:
    - Atomicity: Both nomination and winner inserts succeed together, or neither takes effect.
    - Consistency: Enforces schema validation and deterministic ID resolution throughout.
    - Isolation: Snapshot isolation prevents dirty reads from concurrent ballot queries.
    - Durability: Changes persisted to WiredTiger Write-Ahead Journal before commit acknowledgement.
    """)

if __name__ == "__main__":
    run_acid_transaction_demo()
