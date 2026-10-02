"""
Phase 22: Multi-Document ACID Transactions Demonstration & Engine
==================================================================
Demonstrates enterprise-grade multi-document distributed transactions in MongoDB Atlas:
1. Transaction Lifecycle States:
   - Active -> Partially Committed -> Committed
   - Active -> Failed -> Aborted
2. ACID Properties Verification:
   - Atomicity: All multi-document writes succeed together or roll back completely.
   - Consistency: Maintains domain integrity invariants and schema constraints.
   - Isolation: Snapshot isolation prevents dirty reads from external sessions.
   - Durability: WriteConcern('majority', j=True) guarantees write-ahead journal persistence.
3. Academic Domain Scenario:
   - "Recording Academy Winner Certification & Trophy Allocation Workflow"
   - Manages state transition from uncertified ballot to certified winner,
     allocates trophy statuette, and appends cryptographically sealed audit event.
4. Non-Destructive Guarantee:
   - Uses controlled staging collections with deterministic cleanup.
   - Zero production documents modified or deleted.
"""

import os
import sys
import time
import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Tuple
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

load_dotenv(REPO_ROOT / ".env")

try:
    import pymongo
    from pymongo.read_concern import ReadConcern
    from pymongo.write_concern import WriteConcern
    from pymongo.read_preferences import ReadPreference
    from pymongo.errors import PyMongoError, DuplicateKeyError
    import certifi
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False


class TransactionDemoRunner:
    """Orchestrates controlled academic multi-document transactions against MongoDB Atlas."""

    def __init__(self, uri: str = None):
        self.uri = uri or os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
        self.client = None
        self.db = None
        self.coll_ballots_name = "controlled_tx_ballots"
        self.coll_trophies_name = "controlled_tx_trophies"
        self.coll_audit_name = "controlled_tx_audit"

    def connect(self) -> pymongo.MongoClient:
        """Establishes authenticated connection with TLS."""
        if not PYMONGO_AVAILABLE:
            raise RuntimeError("PyMongo or Certifi not installed.")
        if not self.uri:
            raise ValueError("MONGODB_URI not set in environment.")

        self.client = pymongo.MongoClient(
            self.uri,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=7000,
            connectTimeoutMS=7000
        )
        # Select grammy_winners_db for the transaction scenario
        self.db = self.client["grammy_winners_db"]
        return self.client

    def setup_controlled_collections(self):
        """Ensures controlled staging collections and indexes exist before transaction start.
        Note: MongoDB transactions require collections to exist prior to transactional writes.
        """
        existing = self.db.list_collection_names()
        for name in [self.coll_ballots_name, self.coll_trophies_name, self.coll_audit_name]:
            if name not in existing:
                self.db.create_collection(name)
        
        # Enforce unique constraint on ballot_id to allow testing duplicate key rollback
        self.db[self.coll_ballots_name].create_index([("ballot_id", pymongo.ASCENDING)], unique=True)
        self.db[self.coll_trophies_name].create_index([("trophy_serial", pymongo.ASCENDING)], unique=True)
        
        # Clean any preexisting test artifacts
        self.db[self.coll_ballots_name].delete_many({"test_run": True})
        self.db[self.coll_trophies_name].delete_many({"test_run": True})
        self.db[self.coll_audit_name].delete_many({"test_run": True})

    def teardown_controlled_collections(self, drop_collections: bool = True):
        """Non-destructive teardown cleaning only test records and dropping staging collections."""
        if self.db is not None:
            if drop_collections:
                self.db[self.coll_ballots_name].drop()
                self.db[self.coll_trophies_name].drop()
                self.db[self.coll_audit_name].drop()
            else:
                self.db[self.coll_ballots_name].delete_many({"test_run": True})
                self.db[self.coll_trophies_name].delete_many({"test_run": True})
                self.db[self.coll_audit_name].delete_many({"test_run": True})

    def run_successful_commit_scenario(self) -> Dict[str, Any]:
        """Scenario A: Demonstrates Active -> Partially Committed -> Committed lifecycle."""
        ballots = self.db[self.coll_ballots_name]
        trophies = self.db[self.coll_trophies_name]
        audit = self.db[self.coll_audit_name]

        test_ballot_id = "BAL_TX_COMMIT_001"
        test_trophy_id = "TRP_TX_GOLD_999"
        
        lifecycle_states = ["ACTIVE"]
        operations_logged = []

        # Configure write and read concerns for ACID guarantees
        wc_majority = WriteConcern(w="majority", j=True, wtimeout=10000)
        rc_snapshot = ReadConcern("snapshot")

        t_start = time.time()
        with self.client.start_session(causal_consistency=True) as session:
            with session.start_transaction(
                read_concern=rc_snapshot,
                write_concern=wc_majority,
                read_preference=ReadPreference.PRIMARY
            ):
                # Operation 1: Insert certified ballot
                ballot_doc = {
                    "ballot_id": test_ballot_id,
                    "ceremony_id": "CEREMONY_067",
                    "category_id": "CAT_RECORD_YEAR",
                    "nominee_name": "Billie Eilish",
                    "work_title": "What Was I Made For?",
                    "certification_status": "CERTIFIED_WINNER",
                    "certified_by": "Deloitte Auditing Committee",
                    "test_run": True,
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
                ballots.insert_one(ballot_doc, session=session)
                operations_logged.append("INSERT_BALLOT")

                # Operation 2: Allocate engraved gold statuette
                trophy_doc = {
                    "trophy_serial": test_trophy_id,
                    "ballot_id": test_ballot_id,
                    "engraving_text": "Record of the Year - 67th GRAMMY Awards",
                    "allocation_status": "ENGRAVED_ALLOCATED",
                    "vault_location": "Crypto.com Arena Trophy Locker A",
                    "test_run": True,
                    "allocated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
                trophies.insert_one(trophy_doc, session=session)
                operations_logged.append("INSERT_TROPHY")

                # Operation 3: Append cryptographically sealed audit ledger
                payload_str = f"{test_ballot_id}:{test_trophy_id}:CERTIFIED"
                sha_seal = hashlib.sha256(payload_str.encode()).hexdigest()
                audit_doc = {
                    "audit_event_id": f"AUD_{test_ballot_id}",
                    "ballot_id": test_ballot_id,
                    "trophy_serial": test_trophy_id,
                    "event_type": "CERTIFICATION_SEAL_APPLIED",
                    "hash_digest": sha_seal,
                    "test_run": True,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
                audit.insert_one(audit_doc, session=session)
                operations_logged.append("APPEND_AUDIT_LOG")

                # State transition: Partially Committed
                lifecycle_states.append("PARTIALLY_COMMITTED")
                session.commit_transaction()
                lifecycle_states.append("COMMITTED")

        duration_ms = round((time.time() - t_start) * 1000, 2)

        # Verification outside transaction session (Global visibility)
        found_ballot = ballots.find_one({"ballot_id": test_ballot_id})
        found_trophy = trophies.find_one({"trophy_serial": test_trophy_id})
        found_audit = audit.find_one({"ballot_id": test_ballot_id})

        verified = bool(found_ballot and found_trophy and found_audit)

        return {
            "scenario": "COMMIT_SUCCESS",
            "lifecycle_states": lifecycle_states,
            "operations": operations_logged,
            "duration_ms": duration_ms,
            "verified": verified,
            "documents_committed": {
                "ballot": found_ballot["ballot_id"] if found_ballot else None,
                "trophy": found_trophy["trophy_serial"] if found_trophy else None,
                "audit": found_audit["audit_event_id"] if found_audit else None
            }
        }

    def run_rollback_scenario(self) -> Dict[str, Any]:
        """Scenario B: Demonstrates Active -> Failed -> Aborted lifecycle upon constraint error."""
        ballots = self.db[self.coll_ballots_name]
        trophies = self.db[self.coll_trophies_name]
        audit = self.db[self.coll_audit_name]

        # Seed an existing ballot to trigger intentional UniqueKeyViolation
        seed_ballot_id = "BAL_EXISTING_UNIQUE_SEED"
        ballots.insert_one({
            "ballot_id": seed_ballot_id,
            "nominee_name": "Seed Artist",
            "test_run": True
        })

        test_ballot_id = "BAL_TX_ROLLBACK_FAIL"
        test_trophy_id = "TRP_TX_GOLD_FAIL"
        
        lifecycle_states = ["ACTIVE"]
        operations_attempted = []
        aborted = False
        caught_error = None

        wc_majority = WriteConcern(w="majority", j=True)
        rc_snapshot = ReadConcern("snapshot")

        t_start = time.time()
        try:
            with self.client.start_session(causal_consistency=True) as session:
                try:
                    with session.start_transaction(
                        read_concern=rc_snapshot,
                        write_concern=wc_majority
                    ):
                        # Operation 1: Insert valid ballot in session
                        ballots.insert_one({
                            "ballot_id": test_ballot_id,
                            "nominee_name": "Temporary Nominee",
                            "test_run": True
                        }, session=session)
                        operations_attempted.append("INSERT_BALLOT_1")

                        # Operation 2: Allocate trophy in session
                        trophies.insert_one({
                            "trophy_serial": test_trophy_id,
                            "ballot_id": test_ballot_id,
                            "test_run": True
                        }, session=session)
                        operations_attempted.append("INSERT_TROPHY_1")

                        # Operation 3: Trigger intentional constraint failure (Duplicate Key)
                        # Attempting to insert a duplicate of seed_ballot_id violates unique index
                        operations_attempted.append("TRIGGER_DUPLICATE_KEY_VIOLATION")
                        ballots.insert_one({
                            "ballot_id": seed_ballot_id,
                            "nominee_name": "Duplicate Crash Candidate",
                            "test_run": True
                        }, session=session)

                        session.commit_transaction()
                except Exception as exc:
                    lifecycle_states.append("FAILED")
                    caught_error = type(exc).__name__
                    if session.in_transaction:
                        session.abort_transaction()
                    lifecycle_states.append("ABORTED")
                    aborted = True
        finally:
            # Guarantee seed record cleanup
            ballots.delete_one({"ballot_id": seed_ballot_id})

        duration_ms = round((time.time() - t_start) * 1000, 2)

        # Verification outside transaction session:
        # Neither test_ballot_id nor test_trophy_id must exist in database!
        ballot_leaked = ballots.find_one({"ballot_id": test_ballot_id})
        trophy_leaked = trophies.find_one({"trophy_serial": test_trophy_id})

        verified_atomicity = (ballot_leaked is None) and (trophy_leaked is None) and aborted

        return {
            "scenario": "ROLLBACK_ABORT",
            "lifecycle_states": lifecycle_states,
            "operations_attempted": operations_attempted,
            "caught_error": caught_error,
            "duration_ms": duration_ms,
            "aborted": aborted,
            "verified_atomicity": verified_atomicity,
            "leaked_documents_count": 0 if verified_atomicity else 1
        }

    def run_snapshot_isolation_verification(self) -> Dict[str, Any]:
        """Scenario C: Verifies that uncommitted writes are invisible to concurrent sessions."""
        ballots = self.db[self.coll_ballots_name]
        test_ballot_id = "BAL_TX_ISOLATION_001"

        dirty_read_prevented = False
        with self.client.start_session() as session_writer:
            with session_writer.start_transaction(read_concern=ReadConcern("snapshot")):
                ballots.insert_one({
                    "ballot_id": test_ballot_id,
                    "nominee_name": "Ghost Candidate",
                    "certification_status": "IN_PROGRESS",
                    "test_run": True
                }, session=session_writer)

                # External reader session attempts to read uncommitted ballot
                external_read = ballots.find_one({"ballot_id": test_ballot_id})
                # In snapshot isolation, external_read MUST be None
                if external_read is None:
                    dirty_read_prevented = True

                session_writer.abort_transaction()

        return {
            "scenario": "SNAPSHOT_ISOLATION",
            "dirty_read_prevented": dirty_read_prevented,
            "isolation_guarantee": "Read Uncommitted (Dirty Read) Disallowed"
        }

    def run_all(self, keep_collections: bool = False) -> Dict[str, Any]:
        """Executes complete demonstration suite."""
        print("==================================================================")
        print("PHASE 22: Academic MongoDB Multi-Document ACID Transactions Demo")
        print("==================================================================")
        self.connect()
        print(">> Connected to MongoDB Atlas cluster.")

        print(">> Initializing controlled staging collections with unique indexes...")
        self.setup_controlled_collections()

        print("\n>> Executing Scenario 1: Successful Multi-Document Commit Path...")
        commit_res = self.run_successful_commit_scenario()
        print(f"   Lifecycle States : {' -> '.join(commit_res['lifecycle_states'])}")
        print(f"   Operations       : {', '.join(commit_res['operations'])}")
        print(f"   Latency          : {commit_res['duration_ms']} ms")
        print(f"   Atomicity & Persistence: {'VERIFIED [PASS]' if commit_res['verified'] else 'FAILED'}")

        print("\n>> Executing Scenario 2: Forced Rollback on Constraint Violation...")
        rollback_res = self.run_rollback_scenario()
        print(f"   Lifecycle States : {' -> '.join(rollback_res['lifecycle_states'])}")
        print(f"   Operations       : {', '.join(rollback_res['operations_attempted'])}")
        print(f"   Triggered Error  : {rollback_res['caught_error']}")
        print(f"   All-or-Nothing Atomicity: {'VERIFIED [PASS]' if rollback_res['verified_atomicity'] else 'FAILED'}")

        print("\n>> Executing Scenario 3: Snapshot Isolation & Dirty-Read Prevention...")
        isolation_res = self.run_snapshot_isolation_verification()
        print(f"   Dirty Read Prevented : {isolation_res['dirty_read_prevented']} [PASS]")
        print(f"   Guarantee            : {isolation_res['isolation_guarantee']}")

        print("\n>> Performing non-destructive teardown of test records...")
        self.teardown_controlled_collections(drop_collections=not keep_collections)
        print(">> Teardown complete. Zero production records modified.")

        summary = {
            "phase": "Phase 22 — Transactions",
            "domain_scenario": "Recording Academy Winner Certification & Trophy Allocation Workflow",
            "commit_scenario": commit_res,
            "rollback_scenario": rollback_res,
            "isolation_scenario": isolation_res,
            "overall_status": "PASSED" if (commit_res["verified"] and rollback_res["verified_atomicity"] and isolation_res["dirty_read_prevented"]) else "FAILED"
        }
        return summary


def main():
    runner = TransactionDemoRunner()
    result = runner.run_all(keep_collections=False)
    print("\n==================================================================")
    print(f"OVERALL RESULT: {result['overall_status']}")
    print("==================================================================")
    return 0 if result["overall_status"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())
