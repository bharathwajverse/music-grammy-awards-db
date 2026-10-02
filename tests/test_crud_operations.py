"""
Unit & Integration Tests: Phase 18 MongoDB CRUD Operations Verification
========================================================================
Verifies:
1. `queries/crud/<database>/` directories exist for all 5 approved databases.
2. `crud_examples.js` and `README.md` exist in each directory.
3. All 8 operations are documented and present in each file:
   - insertOne, insertMany, find, findOne, updateOne, updateMany, deleteOne, deleteMany.
4. Filtering and projection operations are demonstrated.
5. Master report `docs/crud-report.md` exists and is comprehensive.
6. Live execution harness passes against MongoDB Atlas with clean state restoration.
"""

import os
import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
CRUD_QUERIES_DIR = REPO_ROOT / "queries" / "crud"
CRUD_REPORT_FILE = REPO_ROOT / "docs" / "crud-report.md"

APPROVED_DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

MANDATORY_OPERATIONS = [
    "insertOne",
    "insertMany",
    "find",
    "findOne",
    "updateOne",
    "updateMany",
    "deleteOne",
    "deleteMany"
]

@pytest.fixture(scope="module")
def env_vars():
    load_dotenv(REPO_ROOT / ".env")
    return {
        "MONGODB_URI": os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    }

def test_crud_directories_exist():
    """Verify that each approved database has a dedicated crud folder."""
    assert CRUD_QUERIES_DIR.exists(), f"Directory not found: {CRUD_QUERIES_DIR}"
    for db_name in APPROVED_DATABASES:
        db_dir = CRUD_QUERIES_DIR / db_name
        assert db_dir.exists(), f"Database CRUD directory missing: {db_dir}"
        assert db_dir.is_dir()

def test_crud_example_files_exist():
    """Verify that each database directory contains crud_examples.js and README.md."""
    for db_name in APPROVED_DATABASES:
        db_dir = CRUD_QUERIES_DIR / db_name
        js_file = db_dir / "crud_examples.js"
        md_file = db_dir / "README.md"
        assert js_file.exists(), f"Missing crud_examples.js for {db_name}"
        assert md_file.exists(), f"Missing README.md for {db_name}"
        assert js_file.stat().st_size > 500, f"crud_examples.js for {db_name} is too small"
        assert md_file.stat().st_size > 500, f"README.md for {db_name} is too small"

@pytest.mark.parametrize("db_name", APPROVED_DATABASES)
def test_all_eight_operations_in_js(db_name: str):
    """Verify that all 8 CRUD operations are implemented in crud_examples.js."""
    js_file = CRUD_QUERIES_DIR / db_name / "crud_examples.js"
    content = js_file.read_text(encoding="utf-8")
    for op in MANDATORY_OPERATIONS:
        assert f".{op}(" in content, f"Operation '{op}' missing in {js_file}"

@pytest.mark.parametrize("db_name", APPROVED_DATABASES)
def test_all_eight_operations_in_readme(db_name: str):
    """Verify that all 8 CRUD operations are documented in README.md."""
    md_file = CRUD_QUERIES_DIR / db_name / "README.md"
    content = md_file.read_text(encoding="utf-8")
    for op in MANDATORY_OPERATIONS:
        assert op in content, f"Operation '{op}' not documented in {md_file}"

@pytest.mark.parametrize("db_name", APPROVED_DATABASES)
def test_filtering_and_projection_demonstrated(db_name: str):
    """Verify that filtering operators and projection are demonstrated."""
    js_file = CRUD_QUERIES_DIR / db_name / "crud_examples.js"
    content = js_file.read_text(encoding="utf-8")
    # Must contain projection suppressing _id or projecting specific fields
    assert "_id: 0" in content, f"Projection suppressing _id missing in {js_file}"
    # Must contain filtering operators ($gte, $lte, $lt, $in, $and, etc.)
    has_filter_op = any(op in content for op in ["$gte", "$lte", "$lt", "$in", "$and", "$or"])
    assert has_filter_op, f"No comparison/logical filter operators found in {js_file}"

def test_crud_report_exists_and_complete():
    """Verify that docs/crud-report.md exists and covers all requirements."""
    assert CRUD_REPORT_FILE.exists(), f"Report file missing: {CRUD_REPORT_FILE}"
    report = CRUD_REPORT_FILE.read_text(encoding="utf-8")
    assert len(report) > 2000, "CRUD report is suspiciously short"
    for db_name in APPROVED_DATABASES:
        assert db_name in report, f"Database '{db_name}' not mentioned in CRUD report"
    for op in MANDATORY_OPERATIONS:
        assert op in report, f"Operation '{op}' not mentioned in CRUD report"
    assert "Filtering" in report
    assert "Projection" in report

def test_live_crud_suite_execution(env_vars):
    """Executes the live CRUD verification suite against MongoDB Atlas."""
    if not env_vars.get("MONGODB_URI"):
        pytest.skip("MONGODB_URI not available; skipping live cluster execution")
    
    from scripts.crud.run_all_crud_examples import run_crud_suite
    results = run_crud_suite()
    assert len(results) == 5, f"Expected 5 database results, got {len(results)}"
    for db_name in APPROVED_DATABASES:
        assert db_name in results, f"Result missing for {db_name}"
        assert results[db_name]["status"] == "PASSED", f"CRUD failed for {db_name}"
        assert results[db_name]["clean_state_restored"] is True, f"Clean state not restored for {db_name}"
        assert results[db_name]["filtering_verified"] is True
        assert results[db_name]["projection_verified"] is True
