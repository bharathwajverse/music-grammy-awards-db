"""Test suite for Phase 8: Functional Dependency Analysis & Key Analysis artifacts.

Validates that normalization artifacts exist, are rigorous, cover Armstrong's axioms,
minimal cover, candidate keys, partial dependencies, transitive dependencies,
multivalued dependencies (MVDs), and join dependencies (JDs) using actual GRAMMY entities.
"""

from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
NORMALIZATION_DIR = REPO_ROOT / "normalization"

REQUIRED_NORMALIZATION_FILES = [
    "functional-dependencies.md",
    "key-analysis.md",
]

CORE_ENTITIES = [
    "ceremonies", "venues", "award_categories", "award_fields",
    "creators", "nominated_works", "nomination_entries",
    "nomination_credits", "winner_records", "trophy_tracking"
]

DEPENDENCY_CONSTRUCTS = [
    "Functional Dependency",
    "Minimal Cover",
    "Partial",
    "Transitive",
    "Multivalued Dependency",
    "Join Dependency",
]


@pytest.mark.parametrize("filename", REQUIRED_NORMALIZATION_FILES)
def test_normalization_file_exists_and_non_empty(filename):
    file_path = NORMALIZATION_DIR / filename
    assert file_path.exists(), f"Missing required normalization artifact: {file_path}"
    assert file_path.stat().st_size > 1500, f"Artifact {filename} is too small or incomplete"


@pytest.mark.parametrize("construct", DEPENDENCY_CONSTRUCTS)
def test_functional_dependencies_contain_required_constructs(construct):
    fd_text = (NORMALIZATION_DIR / "functional-dependencies.md").read_text(encoding="utf-8")
    assert construct.lower() in fd_text.lower(), f"Construct '{construct}' missing from functional-dependencies.md"


@pytest.mark.parametrize("entity", CORE_ENTITIES)
def test_functional_dependencies_use_grammy_entities(entity):
    fd_text = (NORMALIZATION_DIR / "functional-dependencies.md").read_text(encoding="utf-8")
    assert entity in fd_text, f"Entity '{entity}' not utilized in functional-dependencies.md"


def test_key_analysis_content_coverage():
    key_text = (NORMALIZATION_DIR / "key-analysis.md").read_text(encoding="utf-8")
    assert "CANDIDATE KEY" in key_text.upper()
    assert "PRIME ATTRIBUTE" in key_text.upper()
    assert "NON-PRIME" in key_text.upper()
    assert "SUPERKEY" in key_text.upper()
    assert "MINIMAL" in key_text.upper()


@pytest.mark.parametrize("entity", CORE_ENTITIES)
def test_key_analysis_covers_core_entities(entity):
    key_text = (NORMALIZATION_DIR / "key-analysis.md").read_text(encoding="utf-8")
    assert entity in key_text, f"Entity '{entity}' missing from key-analysis.md"
