"""
Unit & Integration Tests: Phase 25 Database Recovery Techniques & Drills
========================================================================
Verifies:
1. Recovery documentation files exist and cover mandatory topics:
   - `docs/recovery/recovery-plan.md` (RPO, RTO, SLAs, replica set topologies).
   - `docs/recovery/backup-restore.md` (WAL, ARIES, Checkpoints, Shadow Paging, Atlas PITR).
   - `docs/recovery/failure-scenarios.md` (Catastrophic vs non-catastrophic, runbooks).
2. Recovery script `scripts/recovery/controlled_recovery_drill.py` exists and is importable.
3. Deterministic SHA-256 data sealing and corruption detection logic.
4. Live cluster recovery drill execution:
   - Baseline sealing, simulated mutation, point-in-time state recovery, 100% bitwise parity.
   - Non-destructive execution and cleanup.
"""

import os
import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DOCS_DIR = REPO_ROOT / "docs" / "recovery"
PLAN_DOC = DOCS_DIR / "recovery-plan.md"
BACKUP_DOC = DOCS_DIR / "backup-restore.md"
FAILURE_DOC = DOCS_DIR / "failure-scenarios.md"
SCRIPT_RECOVERY = REPO_ROOT / "scripts" / "recovery" / "controlled_recovery_drill.py"

@pytest.fixture(scope="module")
def env_vars():
    load_dotenv(REPO_ROOT / ".env")
    return {
        "MONGODB_URI": os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    }

def test_recovery_documentation_files_exist():
    """Verify all 3 required recovery documentation files exist."""
    assert PLAN_DOC.exists(), f"Missing {PLAN_DOC}"
    assert BACKUP_DOC.exists(), f"Missing {BACKUP_DOC}"
    assert FAILURE_DOC.exists(), f"Missing {FAILURE_DOC}"

def test_recovery_plan_content_coverage():
    """Verify recovery-plan.md covers mandatory SLA and architecture topics."""
    text = PLAN_DOC.read_text(encoding="utf-8")
    for keyword in ["RPO", "RTO", "Replica Set", "Primary", "Secondary", "Oplog", "Election"]:
        assert keyword in text, f"Keyword '{keyword}' missing in {PLAN_DOC}"

def test_backup_restore_content_coverage():
    """Verify backup-restore.md covers WAL, ARIES, Shadow Paging, and PITR."""
    text = BACKUP_DOC.read_text(encoding="utf-8")
    for keyword in ["Write-Ahead", "ARIES", "Analysis", "Redo", "Undo", "Compensation Log", "Shadow Paging", "WiredTiger", "Checkpoints", "mongodump"]:
        assert keyword in text, f"Keyword '{keyword}' missing in {BACKUP_DOC}"

def test_failure_scenarios_content_coverage():
    """Verify failure-scenarios.md covers catastrophic vs non-catastrophic taxonomies."""
    text = FAILURE_DOC.read_text(encoding="utf-8")
    for keyword in ["Catastrophic", "Non-Catastrophic", "Split-Brain", "Initial Sync", "Point-in-Time Recovery"]:
        assert keyword in text, f"Keyword '{keyword}' missing in {FAILURE_DOC}"

def test_recovery_drill_digest_computation():
    """Verify cryptographic SHA-256 seal detects document state mutations."""
    from scripts.recovery.controlled_recovery_drill import ControlledRecoveryDrill
    drill = ControlledRecoveryDrill()

    docs_v1 = [
        {"_id": "D1", "name": "Artist 1", "score": 100},
        {"_id": "D2", "name": "Artist 2", "score": 200}
    ]
    docs_v2 = [
        {"_id": "D1", "name": "Artist 1", "score": 999},  # Mutated
        {"_id": "D2", "name": "Artist 2", "score": 200}
    ]

    h1 = drill.compute_collection_digest(docs_v1)
    h2 = drill.compute_collection_digest(docs_v2)
    assert h1 != h2, "Digest must detect data modification"
    assert len(h1) == 64

def test_live_atlas_controlled_recovery_drill(env_vars):
    """Verify live cluster execution of simulated snapshot, corruption, and restore."""
    uri = env_vars["MONGODB_URI"]
    if not uri:
        pytest.skip("MONGODB_URI not set; skipping live recovery drill test.")

    from scripts.recovery.controlled_recovery_drill import ControlledRecoveryDrill
    drill = ControlledRecoveryDrill(uri)
    drill.connect()
    drill.setup()
    try:
        res = drill.execute_drill()
        assert res["corruption_detected"] is True
        assert res["bit_level_parity_verified"] is True
        assert res["restored_count"] == res["baseline_count"]
        assert res["restored_sha256"] == res["baseline_sha256"]
    finally:
        drill.teardown()
