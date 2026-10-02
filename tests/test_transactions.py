"""
Unit & Integration Tests: Phase 22 MongoDB Multi-Document ACID Transactions
============================================================================
Verifies:
1. Documentation `docs/transactions/transaction-demo.md` exists and covers:
   - Transaction start, Operations, Commit, Rollback, ACID properties, Transaction states.
2. Script `scripts/transactions/run_transaction_demo.py` exists and is structured properly.
3. Live MongoDB Atlas Multi-Document Transaction execution:
   - Successful commit path across multiple collections.
   - Forced rollback / abort on constraint violation (Atomicity verification).
   - Snapshot isolation preventing dirty reads.
   - Non-destructive execution with zero pollution of production data.
"""

import os
import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DOCS_TX_FILE = REPO_ROOT / "docs" / "transactions" / "transaction-demo.md"
SCRIPT_TX_FILE = REPO_ROOT / "scripts" / "transactions" / "run_transaction_demo.py"

@pytest.fixture(scope="module")
def env_vars():
    load_dotenv(REPO_ROOT / ".env")
    return {
        "MONGODB_URI": os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    }

def test_transaction_documentation_exists_and_covers_requirements():
    """Verify that transaction-demo.md exists and contains all required sections."""
    assert DOCS_TX_FILE.exists(), f"File missing: {DOCS_TX_FILE}"
    content = DOCS_TX_FILE.read_text(encoding="utf-8")

    required_keywords = [
        "ACTIVE",
        "PARTIALLY COMMITTED",
        "COMMITTED",
        "FAILED",
        "ABORTED",
        "Atomicity",
        "Consistency",
        "Isolation",
        "Durability",
        "start_transaction",
        "commit_transaction",
        "abort_transaction",
        "Snapshot Isolation",
        "WiredTiger"
    ]
    for kw in required_keywords:
        assert kw in content, f"Required keyword '{kw}' missing from {DOCS_TX_FILE}"

def test_transaction_script_exists():
    """Verify that run_transaction_demo.py exists and can be imported."""
    assert SCRIPT_TX_FILE.exists(), f"Script missing: {SCRIPT_TX_FILE}"
    from scripts.transactions.run_transaction_demo import TransactionDemoRunner
    assert TransactionDemoRunner is not None

def test_live_atlas_transaction_commit_scenario(env_vars):
    """Verify multi-document transaction commit succeeds on live cluster."""
    uri = env_vars["MONGODB_URI"]
    if not uri:
        pytest.skip("MONGODB_URI not set; skipping live Atlas transaction test.")

    from scripts.transactions.run_transaction_demo import TransactionDemoRunner
    runner = TransactionDemoRunner(uri)
    runner.connect()
    runner.setup_controlled_collections()
    try:
        res = runner.run_successful_commit_scenario()
        assert res["verified"] is True
        assert res["scenario"] == "COMMIT_SUCCESS"
        assert res["lifecycle_states"] == ["ACTIVE", "PARTIALLY_COMMITTED", "COMMITTED"]
        assert len(res["operations"]) == 3
    finally:
        runner.teardown_controlled_collections()

def test_live_atlas_transaction_rollback_scenario(env_vars):
    """Verify transaction rollback preserves atomicity on constraint violation."""
    uri = env_vars["MONGODB_URI"]
    if not uri:
        pytest.skip("MONGODB_URI not set; skipping live Atlas transaction test.")

    from scripts.transactions.run_transaction_demo import TransactionDemoRunner
    runner = TransactionDemoRunner(uri)
    runner.connect()
    runner.setup_controlled_collections()
    try:
        res = runner.run_rollback_scenario()
        assert res["aborted"] is True
        assert res["verified_atomicity"] is True
        assert res["leaked_documents_count"] == 0
        assert "FAILED" in res["lifecycle_states"]
        assert "ABORTED" in res["lifecycle_states"]
    finally:
        runner.teardown_controlled_collections()

def test_live_atlas_snapshot_isolation(env_vars):
    """Verify that uncommitted writes are not visible externally (Snapshot Isolation)."""
    uri = env_vars["MONGODB_URI"]
    if not uri:
        pytest.skip("MONGODB_URI not set; skipping live Atlas transaction test.")

    from scripts.transactions.run_transaction_demo import TransactionDemoRunner
    runner = TransactionDemoRunner(uri)
    runner.connect()
    runner.setup_controlled_collections()
    try:
        res = runner.run_snapshot_isolation_verification()
        assert res["dirty_read_prevented"] is True
    finally:
        runner.teardown_controlled_collections()
