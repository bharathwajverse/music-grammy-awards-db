"""Test suite for Phase 11: MongoDB Document Model Design & Validation Schemas.

Validates that all 50 collections across the 5 databases have:
1. Valid MongoDB $jsonSchema definitions in mongodb/schema/<database>/<collection>.json
2. Each schema defines '_id', required fields, and >= 10 meaningful domain fields with BSON types
3. Detailed collection specifications in mongodb/collection-specifications/
4. Comprehensive architectural design guide in docs/mongodb-design.md
5. Full compliance with the approved collection feasibility matrix.
"""

import csv
import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
FEASIBILITY_CSV = REPO_ROOT / "schemas" / "collection-feasibility-matrix.csv"
SCHEMA_DIR = REPO_ROOT / "mongodb" / "schema"
SPEC_DIR = REPO_ROOT / "mongodb" / "collection-specifications"
DESIGN_DOC = REPO_ROOT / "docs" / "mongodb-design.md"

DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db",
]

# Load feasibility matrix entries
with open(FEASIBILITY_CSV, encoding="utf-8") as f:
    FEASIBILITY_ENTRIES = list(csv.DictReader(f))


def test_feasibility_matrix_has_fifty_collections():
    """Verify that the feasibility matrix contains exactly 50 audited collections."""
    assert len(FEASIBILITY_ENTRIES) == 50, f"Expected 50 collections, found {len(FEASIBILITY_ENTRIES)}"


@pytest.mark.parametrize("db_name", DATABASES)
def test_database_schema_directory_exists_with_ten_collections(db_name):
    """Verify that each of the 5 database directories exists and contains 10 schemas."""
    db_dir = SCHEMA_DIR / db_name
    assert db_dir.exists(), f"Missing schema directory for database: {db_dir}"
    json_files = list(db_dir.glob("*.json"))
    assert len(json_files) == 10, f"Database {db_name} must contain 10 schemas, found {len(json_files)}"


@pytest.mark.parametrize("row", FEASIBILITY_ENTRIES)
def test_each_collection_has_valid_mongodb_jsonschema(row):
    """Verify every collection in feasibility matrix has a valid MongoDB $jsonSchema file."""
    db_name = row["database_name"]
    coll_name = row["collection_name"]
    schema_path = SCHEMA_DIR / db_name / f"{coll_name}.json"
    
    assert schema_path.exists(), f"Missing schema file: {schema_path}"
    
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    assert "$jsonSchema" in data, f"Schema in {schema_path} must wrap validator in '$jsonSchema'"
    
    js = data["$jsonSchema"]
    assert js.get("bsonType") == "object", f"Root bsonType must be 'object' in {schema_path}"
    
    props = js.get("properties", {})
    assert len(props) >= 10, f"Collection {coll_name} must have >= 10 fields, found {len(props)}"
    assert "_id" in props, f"Collection {coll_name} must define '_id' property"
    
    req = js.get("required", [])
    assert "_id" in req, f"Collection {coll_name} must require '_id'"
    assert len(req) >= 10, f"Collection {coll_name} must require >= 10 fields, found {len(req)}"


@pytest.mark.parametrize("db_name", DATABASES)
def test_database_specification_markdown_exists_and_substantial(db_name):
    """Verify markdown specifications exist for each database and cover all 10 collections."""
    spec_file = SPEC_DIR / f"{db_name}.md"
    assert spec_file.exists(), f"Missing specification markdown: {spec_file}"
    assert spec_file.stat().st_size > 5000, f"Specification {spec_file.name} is too brief (<5KB)"
    
    content = spec_file.read_text(encoding="utf-8")
    # Verify that all 10 collections for this database are documented
    db_colls = [row["collection_name"] for row in FEASIBILITY_ENTRIES if row["database_name"] == db_name]
    for coll in db_colls:
        assert f"`{coll}`" in content, f"Collection '{coll}' not found in {spec_file.name}"


def test_master_collection_specs_readme_exists():
    """Verify master collection specification README exists and links all databases."""
    readme_path = SPEC_DIR / "README.md"
    assert readme_path.exists(), f"Missing {readme_path}"
    content = readme_path.read_text(encoding="utf-8")
    for db_name in DATABASES:
        assert db_name in content, f"Database {db_name} missing from collection specs README"


def test_master_mongodb_design_document_exists_and_complete():
    """Verify master docs/mongodb-design.md exists, is substantial, and covers key topics."""
    assert DESIGN_DOC.exists(), f"Missing {DESIGN_DOC}"
    assert DESIGN_DOC.stat().st_size > 10000, f"Design document too brief (<10KB)"
    
    content = DESIGN_DOC.read_text(encoding="utf-8").lower()
    assert "feasibility" in content
    assert "bson" in content
    assert "_id" in content
    assert "index" in content
    for db_name in DATABASES:
        assert db_name in content
