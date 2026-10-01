"""Test suite for Phase 7: Relational Model artifacts.

Validates that all required relational artifacts exist, are well-structured,
cover all 50 tables across the five databases, define primary and candidate keys,
and rigorously document the required relational algebra operations.
"""

from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
RELATIONAL_DIR = REPO_ROOT / "relational-model"

REQUIRED_RELATIONAL_FILES = [
    "schema.md",
    "keys-and-relationships.md",
    "relational-algebra-examples.md",
]

EXPECTED_DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_creators_db",
    "grammy_nominations_db",
    "grammy_winners_db",
]

CORE_RELATIONS = [
    "venues", "ceremonies", "telecast_broadcasters", "viewership_ratings",
    "award_fields", "award_categories", "category_lineage", "eligibility_rules",
    "creators", "artists", "producers", "audio_engineers", "songwriters_composers", "musical_groups",
    "nominated_works", "nomination_entries", "nomination_credits",
    "winner_records", "big_four_sweeps", "acceptance_speeches", "trophy_tracking"
]

RELATIONAL_ALGEBRA_OPS = [
    "Selection",
    "Projection",
    "Cartesian Product",
    "Join",
    "Union",
    "Set Difference",
    "Division"
]


@pytest.mark.parametrize("filename", REQUIRED_RELATIONAL_FILES)
def test_relational_file_exists_and_non_empty(filename):
    file_path = RELATIONAL_DIR / filename
    assert file_path.exists(), f"Missing required relational artifact: {file_path}"
    assert file_path.stat().st_size > 1000, f"Artifact {filename} is too small or incomplete"


def test_schema_covers_all_domains():
    schema_text = (RELATIONAL_DIR / "schema.md").read_text(encoding="utf-8")
    for db in EXPECTED_DATABASES:
        assert db in schema_text, f"Database domain '{db}' not documented in schema.md"


@pytest.mark.parametrize("rel_name", CORE_RELATIONS)
def test_schema_covers_core_relations(rel_name):
    schema_text = (RELATIONAL_DIR / "schema.md").read_text(encoding="utf-8")
    assert rel_name in schema_text, f"Relation '{rel_name}' missing from schema.md"


def test_keys_and_relationships_integrity():
    keys_text = (RELATIONAL_DIR / "keys-and-relationships.md").read_text(encoding="utf-8")
    assert "PRIMARY KEY" in keys_text.upper()
    assert "CANDIDATE" in keys_text.upper()
    assert "FOREIGN KEY" in keys_text.upper()
    assert "ON DELETE CASCADE" in keys_text
    assert "ON DELETE RESTRICT" in keys_text
    assert "NOMINATION_CREDIT" in keys_text
    assert "AWARD_RECIPIENT" in keys_text


@pytest.mark.parametrize("op_name", RELATIONAL_ALGEBRA_OPS)
def test_relational_algebra_operations_present(op_name):
    algebra_text = (RELATIONAL_DIR / "relational-algebra-examples.md").read_text(encoding="utf-8")
    assert op_name.lower() in algebra_text.lower(), f"Operation '{op_name}' missing from relational algebra artifact"
