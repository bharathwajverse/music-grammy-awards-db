"""
Unit Tests: JSON Schema Conformance & Syntax Validation
========================================================
Validates that every one of the 50 schema files is a valid JSON document
and conforms to JSON Schema Draft-07 syntax.
"""

import json
from pathlib import Path
import pytest
from jsonschema import Draft7Validator

SCHEMA_BASE_DIR = Path("schemas/json_schemas")

def get_all_schema_files():
    return list(SCHEMA_BASE_DIR.glob("*/*.json"))

@pytest.mark.parametrize("schema_file", get_all_schema_files(), ids=lambda f: f.as_posix())
def test_json_schema_validity(schema_file):
    with open(schema_file, "r", encoding="utf-8") as f:
        schema = json.load(f)
    
    # Assert Draft-7 schema validation passes without schema syntax errors
    Draft7Validator.check_schema(schema)
    assert schema.get("type") == "object"
    assert "properties" in schema
    assert "required" in schema
    assert len(schema["properties"]) >= 10
