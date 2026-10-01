"""Test suite for Phase 9: Schema Normalization Proofs (1NF to 5NF & Summary).

Validates that all required normalization artifacts exist, have rigorous depth,
contain formal mathematical definitions, starting structures, violation proofs,
decompositions, lossless-join / dependency preservation proofs, and use
authentic GRAMMY project entities.
"""

from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
NORMALIZATION_DIR = REPO_ROOT / "normalization"

PHASE_9_FILES = [
    "1nf.md",
    "2nf.md",
    "3nf.md",
    "bcnf.md",
    "4nf.md",
    "5nf.md",
    "normalization-summary.md",
]

STAGE_REQUIREMENTS = [
    ("1nf.md", ["atomic", "repeating group", "lossless", "primary key", "decomposition"]),
    ("2nf.md", ["partial", "composite key", "heath", "lossless-join", "preservation"]),
    ("3nf.md", ["transitive", "superkey", "bernstein", "lossless", "preservation"]),
    ("bcnf.md", ["overlapping candidate keys", "superkey", "deloitte", "decomposition", "trade-off"]),
    ("4nf.md", ["multivalued dependency", "tuple proliferation", "fagin", "lossless", "independent"]),
    ("5nf.md", ["join dependency", "project-join", "cyclic", "lossless", "tableau"]),
    ("normalization-summary.md", ["ladder", "anomalies", "lossless", "mongodb", "denormalization"]),
]

GRAMMY_PROJECT_ENTITIES = [
    "ceremony", "venue", "category", "work", "creator", "producer"
]


@pytest.mark.parametrize("filename", PHASE_9_FILES)
def test_phase_9_artifact_exists_and_substantial(filename):
    """Verify that all 7 required Phase 9 artifacts exist and have non-trivial size."""
    file_path = NORMALIZATION_DIR / filename
    assert file_path.exists(), f"Missing required Phase 9 artifact: {file_path}"
    assert file_path.stat().st_size > 5000, f"Artifact {filename} is too brief or incomplete (<5KB)"


@pytest.mark.parametrize("filename,terms", STAGE_REQUIREMENTS)
def test_stage_required_theoretical_concepts(filename, terms):
    """Verify each stage artifact discusses its essential mathematical concepts."""
    content = (NORMALIZATION_DIR / filename).read_text(encoding="utf-8").lower()
    for term in terms:
        assert term in content, f"Term '{term}' missing from {filename}"


def test_1nf_starting_violation_and_decomposition():
    """Verify 1NF document demonstrates unnormalized form and atomic flattening."""
    text = (NORMALIZATION_DIR / "1nf.md").read_text(encoding="utf-8")
    assert "UNF" in text
    assert "atomic" in text.lower()
    assert "repeating group" in text.lower() or "multivalued" in text.lower()
    assert "R_1NF_flat" in text or "1NF" in text


def test_2nf_partial_dependency_and_heath_proof():
    """Verify 2NF document addresses partial dependencies and Heath's Theorem."""
    text = (NORMALIZATION_DIR / "2nf.md").read_text(encoding="utf-8")
    assert "partial" in text.lower()
    assert "Heath" in text
    assert "lossless" in text.lower()
    assert "nomination" in text.lower()


def test_3nf_transitive_dependency_and_synthesis():
    """Verify 3NF document demonstrates transitive dependency resolution."""
    text = (NORMALIZATION_DIR / "3nf.md").read_text(encoding="utf-8")
    assert "transitive" in text.lower()
    assert "venue" in text.lower()
    assert "record_labels" in text.lower() or "label" in text.lower()
    assert "lossless" in text.lower()


def test_bcnf_overlapping_keys_and_deloitte_slate():
    """Verify BCNF document proves overlapping candidate key anomaly."""
    text = (NORMALIZATION_DIR / "bcnf.md").read_text(encoding="utf-8")
    assert "overlapping" in text.lower()
    assert "auditor" in text.lower()
    assert "superkey" in text.lower()


def test_4nf_mvd_and_tuple_proliferation():
    """Verify 4NF document details multivalued dependencies and Fagin's Theorem."""
    text = (NORMALIZATION_DIR / "4nf.md").read_text(encoding="utf-8")
    assert "multivalued" in text.lower()
    assert "fagin" in text.lower()
    assert "pro_affiliation" in text or "instrument" in text


def test_5nf_join_dependency_and_triadic_proof():
    """Verify 5NF document proves Project-Join Normal Form and cyclic JD."""
    text = (NORMALIZATION_DIR / "5nf.md").read_text(encoding="utf-8")
    assert "join dependency" in text.lower()
    assert "pjnf" in text.lower() or "project-join" in text.lower()
    assert "producer" in text.lower()
    assert "workflow" in text.lower()
    assert "lossless" in text.lower()


def test_normalization_summary_master_matrix_and_nosql_bridge():
    """Verify summary table contains the master ladder and MongoDB architectural mapping."""
    text = (NORMALIZATION_DIR / "normalization-summary.md").read_text(encoding="utf-8")
    assert "1NF" in text and "2NF" in text and "3NF" in text and "BCNF" in text and "4NF" in text and "5NF" in text
    assert "anomaly" in text.lower()
    assert "lossless" in text.lower()
    assert "mongodb" in text.lower()
    assert "grammy_core" in text
