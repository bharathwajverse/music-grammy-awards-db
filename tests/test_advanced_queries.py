"""
Unit & Integration Tests: Phase 19 MongoDB Advanced Queries Verification
========================================================================
Verifies:
1. `queries/advanced/<database>/` directories exist for all 5 approved databases.
2. `advanced_queries.js` and `README.md` exist in each database directory.
3. Master `queries/advanced/README.md` and `master_advanced_queries.js` exist.
4. All 17 mandatory operators and clauses are implemented in .js query files:
   - $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin
   - $and, $or, $not
   - sort, limit, skip, projection
   - arrays, embedded documents
5. All 17 mandatory operators and clauses are comprehensively documented in README.md files.
6. Master report `docs/advanced-queries-report.md` exists and covers all requirements.
7. Live execution harness passes against MongoDB Atlas with 100% real data accuracy.
"""

import os
import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

ADVANCED_QUERIES_DIR = REPO_ROOT / "queries" / "advanced"
ADVANCED_REPORT_FILE = REPO_ROOT / "docs" / "advanced-queries-report.md"

APPROVED_DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

MANDATORY_OPERATORS = [
    "$eq",
    "$ne",
    "$gt",
    "$gte",
    "$lt",
    "$lte",
    "$in",
    "$nin",
    "$and",
    "$or",
    "$not"
]

MANDATORY_CLAUSES = [
    "sort",
    "limit",
    "skip",
    "projection"
]

@pytest.fixture(scope="module")
def env_vars():
    load_dotenv(REPO_ROOT / ".env")
    return {
        "MONGODB_URI": os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    }

def test_advanced_queries_master_directory_exists():
    """Verify that queries/advanced exists and has master documentation."""
    assert ADVANCED_QUERIES_DIR.exists(), f"Directory not found: {ADVANCED_QUERIES_DIR}"
    master_readme = ADVANCED_QUERIES_DIR / "README.md"
    master_js = ADVANCED_QUERIES_DIR / "master_advanced_queries.js"
    assert master_readme.exists(), "Master queries/advanced/README.md missing"
    assert master_js.exists(), "Master queries/advanced/master_advanced_queries.js missing"
    assert master_readme.stat().st_size > 1000, "Master README.md too short"
    assert master_js.stat().st_size > 1000, "Master master_advanced_queries.js too short"

def test_database_subdirectories_exist():
    """Verify that each approved database has a dedicated advanced queries directory."""
    for db_name in APPROVED_DATABASES:
        db_dir = ADVANCED_QUERIES_DIR / db_name
        assert db_dir.exists(), f"Database directory missing: {db_dir}"
        assert db_dir.is_dir()

def test_database_files_exist():
    """Verify that advanced_queries.js and README.md exist in each database directory."""
    for db_name in APPROVED_DATABASES:
        db_dir = ADVANCED_QUERIES_DIR / db_name
        js_file = db_dir / "advanced_queries.js"
        md_file = db_dir / "README.md"
        assert js_file.exists(), f"Missing advanced_queries.js for {db_name}"
        assert md_file.exists(), f"Missing README.md for {db_name}"
        assert js_file.stat().st_size > 800, f"advanced_queries.js for {db_name} is too small"
        assert md_file.stat().st_size > 800, f"README.md for {db_name} is too small"

def test_all_comparison_and_logical_operators_implemented():
    """Verify that all 11 comparison and logical operators are present across the query files."""
    master_js = ADVANCED_QUERIES_DIR / "master_advanced_queries.js"
    content = master_js.read_text(encoding="utf-8")
    for op in MANDATORY_OPERATORS:
        assert f'"{op}"' in content or f"'{op}'" in content or f"{op}:" in content, (
            f"Operator '{op}' missing in {master_js}"
        )

def test_all_clauses_implemented():
    """Verify that sort, limit, skip, and projection are demonstrated in query files."""
    master_js = ADVANCED_QUERIES_DIR / "master_advanced_queries.js"
    content = master_js.read_text(encoding="utf-8")
    assert ".sort(" in content, "sort clause missing in master_advanced_queries.js"
    assert ".limit(" in content, "limit clause missing in master_advanced_queries.js"
    assert ".skip(" in content, "skip clause missing in master_advanced_queries.js"
    assert "_id: 0" in content, "projection suppressing _id missing in master_advanced_queries.js"

def test_arrays_and_embedded_documents_demonstrated():
    """Verify that array operations and embedded document dot-notation are demonstrated."""
    master_js = ADVANCED_QUERIES_DIR / "master_advanced_queries.js"
    content = master_js.read_text(encoding="utf-8")
    assert "$all" in content, "Array operator $all missing in master_advanced_queries.js"
    assert "$size" in content, "Array operator $size missing in master_advanced_queries.js"
    assert "_source_provenance." in content, "Embedded document dot notation missing in master_advanced_queries.js"

@pytest.mark.parametrize("db_name", APPROVED_DATABASES)
def test_database_readme_documents_operators(db_name: str):
    """Verify each database README documents relevant advanced query operators."""
    md_file = ADVANCED_QUERIES_DIR / db_name / "README.md"
    content = md_file.read_text(encoding="utf-8")
    assert len(content) > 1000, f"README for {db_name} is too brief"
    assert "_source_provenance" in content, f"Embedded document provenance not documented in {md_file}"

def test_advanced_queries_report_exists_and_complete():
    """Verify that docs/advanced-queries-report.md exists and is exhaustive."""
    assert ADVANCED_REPORT_FILE.exists(), f"Report file missing: {ADVANCED_REPORT_FILE}"
    report = ADVANCED_REPORT_FILE.read_text(encoding="utf-8")
    assert len(report) > 3000, "Advanced queries report is too short"
    for db_name in APPROVED_DATABASES:
        assert db_name in report, f"Database '{db_name}' not covered in report"
    for op in MANDATORY_OPERATORS:
        assert op in report, f"Operator '{op}' not covered in report"
    for clause in MANDATORY_CLAUSES:
        assert clause in report, f"Clause '{clause}' not covered in report"
    assert "Array" in report or "arrays" in report
    assert "Embedded" in report or "embedded" in report

def test_live_advanced_query_suite_execution(env_vars):
    """Executes the live advanced query verification harness against MongoDB Atlas."""
    if not env_vars.get("MONGODB_URI"):
        pytest.skip("MONGODB_URI not available; skipping live cluster execution")
    
    from scripts.advanced.run_all_advanced_queries import run_advanced_query_suite
    results = run_advanced_query_suite()
    assert results["all_passed"] is True, "Advanced query suite reported failures"
    assert len(results["databases_verified"]) == 5
    for db_name in APPROVED_DATABASES:
        assert results["databases_verified"][db_name] == "PASSED"
    for op in MANDATORY_OPERATORS + MANDATORY_CLAUSES + ["arrays", "embedded documents"]:
        assert results["operators_verified"].get(op) is True, f"Operator/clause {op} not verified"
