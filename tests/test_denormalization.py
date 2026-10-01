"""Test suite for Phase 10: Denormalization Decisions & Embed vs. Reference Architecture.

Validates that all required denormalization artifacts exist, have rigorous depth,
contain all required decision fields (8-point criteria), cover all 5 databases,
and provide comprehensive anti-pattern and consistency frameworks.
"""

from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
DENORMALIZATION_DIR = REPO_ROOT / "denormalization"

REQUIRED_DENORMALIZATION_FILES = [
    "decisions.md",
    "embed-vs-reference.md",
]

DECISION_EVALUATION_FIELDS = [
    "original normalized structure",
    "mongodb structure",
    "embed or reference",
    "reason",
    "read/write implications",
    "redundancy introduced",
    "consistency risk",
    "validation strategy",
]

TARGET_DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db",
]

EMBED_VS_REF_CONCEPTS = [
    "16 mb",
    "cardinality",
    "bounded",
    "anti-pattern",
    "unbounded array",
    "over-referencing",
    "change stream",
    "jsonschema",
    "transaction",
]


@pytest.mark.parametrize("filename", REQUIRED_DENORMALIZATION_FILES)
def test_denormalization_artifacts_exist_and_substantial(filename):
    """Verify that all Phase 10 denormalization artifacts exist and have substantive size."""
    file_path = DENORMALIZATION_DIR / filename
    assert file_path.exists(), f"Missing required denormalization artifact: {file_path}"
    assert file_path.stat().st_size > 10000, f"Artifact {filename} is too brief or incomplete (<10KB)"


@pytest.mark.parametrize("field", DECISION_EVALUATION_FIELDS)
def test_decisions_contain_all_required_evaluation_criteria(field):
    """Verify that decisions.md systematically covers all 8 evaluation dimensions."""
    content = (DENORMALIZATION_DIR / "decisions.md").read_text(encoding="utf-8").lower()
    assert field in content, f"Required decision dimension '{field}' missing from decisions.md"


@pytest.mark.parametrize("db_name", TARGET_DATABASES)
def test_decisions_cover_all_five_databases(db_name):
    """Verify that denormalization decisions span across all 5 project databases."""
    content = (DENORMALIZATION_DIR / "decisions.md").read_text(encoding="utf-8")
    assert db_name in content, f"Database '{db_name}' not addressed in decisions.md"


@pytest.mark.parametrize("concept", EMBED_VS_REF_CONCEPTS)
def test_embed_vs_ref_covers_architectural_concepts(concept):
    """Verify that embed-vs-reference.md covers core architectural principles."""
    content = (DENORMALIZATION_DIR / "embed-vs-reference.md").read_text(encoding="utf-8").lower()
    assert concept in content, f"Concept '{concept}' missing from embed-vs-reference.md"


def test_decisions_catalog_completeness():
    """Verify that multiple concrete decisions are enumerated with formal structure."""
    content = (DENORMALIZATION_DIR / "decisions.md").read_text(encoding="utf-8")
    for i in range(1, 13):
        assert f"Decision {i}:" in content, f"Decision {i} missing from decisions catalog"


def test_embed_vs_ref_includes_decision_rubric_and_matrix():
    """Verify that embed-vs-reference.md includes decision rubric rules and matrix."""
    content = (DENORMALIZATION_DIR / "embed-vs-reference.md").read_text(encoding="utf-8")
    assert "Rule 1: Cardinality Boundedness Test" in content
    assert "Rule 2: Access Pattern & Query Coupling Test" in content
    assert "Rule 3: Read-to-Write Ratio & Update Velocity Test" in content
    assert "Rule 4: Lifecycle & Ownership Coupling Test" in content
    assert "Rule 5: Cross-Database Boundary Constraint" in content
    assert "Extended Reference" in content
    assert "Strict Embedding" in content
    assert "Strict Referencing" in content
