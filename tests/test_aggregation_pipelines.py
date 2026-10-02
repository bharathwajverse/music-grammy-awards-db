"""
=============================================================================
Test Suite: Phase 20 — MongoDB Aggregation Pipelines & Analytics
=============================================================================
Academic Phase: Phase 20 — Aggregation Framework
Course Module: Module 10 — Advanced Query & Aggregation Framework

Verifies:
  1. Aggregation directory structure and script completeness.
  2. Implementation of all 7 mandatory operators:
     $match, $group, $sort, $project, $count, $lookup, $unwind
  3. Implementation of all 7 mandatory analytical queries:
     - Nominations per artist
     - Wins per artist
     - Wins by category
     - Nominations by year
     - Category trends
     - Artists appearing in multiple categories
     - Multi-time winners
  4. Compliance with strict DERIVED labeling policy.
  5. Live execution of aggregation pipelines on MongoDB Atlas.
=============================================================================
"""

import sys
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

AGGREGATION_DIR = REPO_ROOT / "queries" / "aggregation"
AGGREGATION_REPORT_FILE = REPO_ROOT / "docs" / "aggregation-report.md"

MANDATORY_OPERATORS = [
    "$match",
    "$group",
    "$sort",
    "$project",
    "$count",
    "$lookup",
    "$unwind",
]

MANDATORY_EXAMPLES = [
    ("01_nominations_per_artist.js", "nominations per artist"),
    ("02_wins_per_artist.js", "wins per artist"),
    ("03_wins_by_category.js", "wins by category"),
    ("04_nominations_by_year.js", "nominations by year"),
    ("05_category_trends.js", "category trends"),
    ("06_artists_in_multiple_categories.js", "multiple categories"),
    ("07_multi_time_winners.js", "multi-time winners"),
]


def test_aggregation_directory_and_master_script_exist():
    """Verify that queries/aggregation directory and core files exist."""
    assert AGGREGATION_DIR.exists(), f"Directory missing: {AGGREGATION_DIR}"
    assert AGGREGATION_DIR.is_dir()

    master_js = AGGREGATION_DIR / "aggregation_pipelines.js"
    assert master_js.exists(), "aggregation_pipelines.js missing"
    assert len(master_js.read_text(encoding="utf-8")) > 2000

    readme = AGGREGATION_DIR / "README.md"
    assert readme.exists(), "queries/aggregation/README.md missing"
    assert len(readme.read_text(encoding="utf-8")) > 1500


@pytest.mark.parametrize("script_name,description", MANDATORY_EXAMPLES)
def test_mandatory_pipeline_scripts_exist(script_name: str, description: str):
    """Verify that individual scripts for each analytical inquiry exist."""
    script_path = AGGREGATION_DIR / script_name
    assert script_path.exists(), f"Pipeline script {script_name} missing for {description}"
    content = script_path.read_text(encoding="utf-8")
    assert len(content) > 500
    assert "DERIVED" in content, f"Script {script_name} must contain DERIVED label"


def test_supplementary_pipeline_scripts_exist():
    """Verify supplementary pipeline scripts 08, 09, 10 exist."""
    supp_scripts = [
        "08_speech_acknowledgments_distribution.js",
        "09_venue_ceremony_analytics.js",
        "10_category_restructure_analytics.js",
    ]
    for s in supp_scripts:
        p = AGGREGATION_DIR / s
        assert p.exists(), f"Supplementary script {s} missing"
        assert "DERIVED" in p.read_text(encoding="utf-8")


def test_all_mandatory_operators_present_in_master_script():
    """Verify that all 7 required aggregation operators are demonstrated in master script."""
    master_js = AGGREGATION_DIR / "aggregation_pipelines.js"
    content = master_js.read_text(encoding="utf-8")
    for op in MANDATORY_OPERATORS:
        assert op in content, f"Mandatory operator '{op}' missing in {master_js}"


def test_derived_labeling_compliance():
    """Verify that computed results are strictly labeled as DERIVED."""
    master_js = AGGREGATION_DIR / "aggregation_pipelines.js"
    content = master_js.read_text(encoding="utf-8")
    assert "DERIVED_total_nominations" in content
    assert "DERIVED_total_wins" in content
    assert "DERIVED_total_historical_wins" in content
    assert "DERIVED_career_wins_count" in content
    assert "DERIVED_distinct_categories_count" in content
    assert '"DERIVED"' in content or "'DERIVED'" in content


def test_aggregation_readme_is_comprehensive():
    """Verify queries/aggregation/README.md documents all operators and examples."""
    readme = AGGREGATION_DIR / "README.md"
    content = readme.read_text(encoding="utf-8")
    for op in MANDATORY_OPERATORS:
        assert op in content, f"Operator '{op}' not documented in README"
    assert "Nominations per artist" in content or "nominations per artist" in content.lower()
    assert "Wins per artist" in content or "wins per artist" in content.lower()
    assert "Wins by category" in content or "wins by category" in content.lower()
    assert "Nominations by year" in content or "nominations by year" in content.lower()
    assert "Category trends" in content or "category trends" in content.lower()
    assert "multiple categories" in content.lower()
    assert "multi-time winners" in content.lower()
    assert "DERIVED" in content


def test_aggregation_report_exists_and_complete():
    """Verify docs/aggregation-report.md exists, is complete, and contains verification details."""
    assert AGGREGATION_REPORT_FILE.exists(), f"Report file missing: {AGGREGATION_REPORT_FILE}"
    report = AGGREGATION_REPORT_FILE.read_text(encoding="utf-8")
    assert len(report) > 3000, "Aggregation report is too short"
    for op in MANDATORY_OPERATORS:
        assert op in report, f"Operator '{op}' not documented in report"
    assert "DERIVED" in report
    assert "grammy_nominations_db" in report
    assert "grammy_winners_db" in report
    assert "grammy_categories_db" in report
    assert "grammy_history_db" in report


def test_live_aggregation_pipeline_execution():
    """Execute live analytical aggregation pipelines against MongoDB Atlas."""
    from scripts.aggregation.run_all_aggregations import run_all_aggregations

    summary = run_all_aggregations()
    assert summary["pipelines_executed"] >= 7
    assert summary["pipelines_passed"] == summary["pipelines_executed"]

    # Verify all 7 mandatory operators were verified live
    for op in MANDATORY_OPERATORS:
        assert op in summary["operators_verified"]

    # Verify required analytical examples produced non-empty DERIVED outputs
    p1 = summary["pipeline_results"]["01_nominations_per_artist"]
    assert p1["DERIVED_total_nominations"] >= 1
    assert p1["DERIVED_calculation_status"] == "DERIVED"

    p2 = summary["pipeline_results"]["02_wins_per_artist"]
    assert p2["DERIVED_total_wins"] >= 1
    assert p2["DERIVED_calculation_status"] == "DERIVED"

    p3 = summary["pipeline_results"]["03_wins_by_category"]
    assert p3["DERIVED_total_historical_wins"] >= 1
    assert p3["DERIVED_calculation_status"] == "DERIVED"

    p4 = summary["pipeline_results"]["04_nominations_by_year"]
    assert p4["DERIVED_total_nominations"] >= 1
    assert p4["DERIVED_calculation_status"] == "DERIVED"

    p5 = summary["pipeline_results"]["05_category_trends"]
    assert p5["DERIVED_nominations_count"] >= 1
    assert p5["DERIVED_calculation_status"] == "DERIVED"

    p6 = summary["pipeline_results"]["06_artists_in_multiple_categories"]
    assert p6["DERIVED_distinct_categories_count"] > 1
    assert p6["DERIVED_calculation_status"] == "DERIVED"

    p7 = summary["pipeline_results"]["07_multi_time_winners"]
    assert p7["DERIVED_career_wins_count"] > 1
    assert p7["DERIVED_calculation_status"] == "DERIVED"
