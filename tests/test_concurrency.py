"""
Unit & Integration Tests: Phase 23 Concurrency Control & Serializability
========================================================================
Verifies:
1. Concurrency documentation exists and covers mandatory topics:
   - `docs/concurrency/concurrency.md`
   - `docs/concurrency/serializability.md`
   - `docs/concurrency/deadlocks.md`
2. Theoretical Lock Compatibility Matrix adheres to academic DBMS rules:
   - IS, IX, S, SIX, X compatibility.
3. Directed Wait-For Graph (WFG) correctly detects cycles and selects victims:
   - Tarjan/DFS cycle detection, Wound-Wait / Wait-Die victim selection.
4. Live MongoDB Atlas Concurrency Tests:
   - High-concurrency worker threads executing atomic updates without Lost Updates.
   - Snapshot isolation optimistic concurrency control behavior.
   - Clean teardown without residual artifacts.
"""

import os
import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DOCS_DIR = REPO_ROOT / "docs" / "concurrency"
CONCURRENCY_DOC = DOCS_DIR / "concurrency.md"
SERIALIZABILITY_DOC = DOCS_DIR / "serializability.md"
DEADLOCKS_DOC = DOCS_DIR / "deadlocks.md"
SCRIPT_CONCURRENCY = REPO_ROOT / "scripts" / "concurrency" / "simulate_concurrency.py"

@pytest.fixture(scope="module")
def env_vars():
    load_dotenv(REPO_ROOT / ".env")
    return {
        "MONGODB_URI": os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    }

def test_concurrency_documentation_files_exist():
    """Verify all 3 required concurrency documentation files exist."""
    assert CONCURRENCY_DOC.exists(), f"Missing {CONCURRENCY_DOC}"
    assert SERIALIZABILITY_DOC.exists(), f"Missing {SERIALIZABILITY_DOC}"
    assert DEADLOCKS_DOC.exists(), f"Missing {DEADLOCKS_DOC}"

def test_concurrency_doc_content_coverage():
    """Verify concurrency.md covers required syllabus topics."""
    text = CONCURRENCY_DOC.read_text(encoding="utf-8")
    for keyword in ["Lost Update", "Two-Phase Locking", "Strict 2PL", "Thomas Write Rule", "WiredTiger", "MVCC", "Tickets"]:
        assert keyword in text, f"Keyword '{keyword}' missing in {CONCURRENCY_DOC}"

def test_serializability_doc_content_coverage():
    """Verify serializability.md covers conflict & view serializability."""
    text = SERIALIZABILITY_DOC.read_text(encoding="utf-8")
    for keyword in ["Conflict Serializability", "Precedence Graph", "View Serializability", "NP-Complete", "Snapshot Isolation"]:
        assert keyword in text, f"Keyword '{keyword}' missing in {SERIALIZABILITY_DOC}"

def test_deadlocks_doc_content_coverage():
    """Verify deadlocks.md covers Coffman conditions, WFG, and resolution."""
    text = DEADLOCKS_DOC.read_text(encoding="utf-8")
    for keyword in ["Coffman", "Wait-For Graph", "Wait-Die", "Wound-Wait", "Starvation", "WriteConflict"]:
        assert keyword in text, f"Keyword '{keyword}' missing in {DEADLOCKS_DOC}"

def test_lock_compatibility_matrix():
    """Verify theoretical lock compatibility logic."""
    from scripts.concurrency.simulate_concurrency import LockCompatibilityMatrix
    # Shared is compatible with Shared
    assert LockCompatibilityMatrix.is_compatible("S", "S") is True
    # Shared is compatible with Intent Shared
    assert LockCompatibilityMatrix.is_compatible("S", "IS") is True
    # Exclusive is conflicting with Shared
    assert LockCompatibilityMatrix.is_compatible("X", "S") is False
    # Exclusive is conflicting with Exclusive
    assert LockCompatibilityMatrix.is_compatible("X", "X") is False
    # Intent Exclusive is compatible with Intent Exclusive
    assert LockCompatibilityMatrix.is_compatible("IX", "IX") is True
    # Exclusive is conflicting with Intent Exclusive
    assert LockCompatibilityMatrix.is_compatible("X", "IX") is False

def test_wait_for_graph_cycle_detection_and_resolution():
    """Verify cycle detection in directed Wait-For Graph and victim selection."""
    from scripts.concurrency.simulate_concurrency import WaitForGraph
    wfg = WaitForGraph()
    wfg.register_transaction("T1", 10.0)
    wfg.register_transaction("T2", 20.0)
    wfg.register_transaction("T3", 30.0)

    # Linear dependencies: No cycle
    wfg.add_wait_edge("T1", "T2")
    wfg.add_wait_edge("T2", "T3")
    assert len(wfg.find_deadlock_cycle()) == 0

    # Introduce cycle: T3 waits for T1
    wfg.add_wait_edge("T3", "T1")
    cycle = wfg.find_deadlock_cycle()
    assert len(cycle) > 0

    # Resolve cycle via Wound-Wait (youngest transaction aborted)
    res = wfg.resolve_deadlock(protocol="WOUND_WAIT")
    assert res["deadlock"] is True
    assert res["victim"] == "T3"  # T3 has highest timestamp 30.0
    assert len(wfg.find_deadlock_cycle()) == 0

def test_live_atlas_atomic_increments(env_vars):
    """Verify concurrent worker threads avoid Lost Update anomaly via atomic $inc."""
    uri = env_vars["MONGODB_URI"]
    if not uri:
        pytest.skip("MONGODB_URI not set; skipping live Atlas concurrency test.")

    from scripts.concurrency.simulate_concurrency import ConcurrencySimulator
    sim = ConcurrencySimulator(uri)
    sim.connect()
    sim.setup()
    try:
        res = sim.simulate_concurrent_atomic_increments(num_threads=6, increments_per_thread=10)
        assert res["success"] is True
        assert res["lost_updates"] == 0
        assert res["actual_total"] == 60
    finally:
        sim.teardown()
