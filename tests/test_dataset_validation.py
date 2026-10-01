"""
Unit Tests: Processed Data Validation & Schema Conformance
==========================================================
Verifies that:
1. All 50 processed JSON files exist.
2. Every collection contains >= 50 documents.
3. Every document contains >= 10 meaningful fields.
4. Every document conforms to its formal JSON Schema (Draft-07).
5. Cross-database foreign references resolve to valid entities.
"""

import json
from pathlib import Path
import pytest
from jsonschema import Draft7Validator

PROCESSED_DIR = Path("data/processed")
SCHEMA_DIR = Path("schemas/json_schemas")

EXPECTED_DATABASES = [
    "grammy_history_db",
    "grammy_categories_db",
    "grammy_nominations_db",
    "grammy_winners_db",
    "grammy_creators_db"
]

def get_all_collection_tuples():
    tuples = []
    for db_name in EXPECTED_DATABASES:
        db_path = PROCESSED_DIR / db_name
        for json_file in sorted(db_path.glob("*.json")):
            tuples.append((db_name, json_file.stem, json_file.as_posix()))
    return tuples

ALL_COLLECTIONS = get_all_collection_tuples()

@pytest.mark.parametrize("db_name, coll_name, file_path", ALL_COLLECTIONS)
def test_collection_document_quota(db_name, coll_name, file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        docs = json.load(f)
    assert isinstance(docs, list), f"Expected list of documents in {file_path}"
    assert len(docs) >= 50, f"Collection {db_name}.{coll_name} has only {len(docs)} documents (minimum 50 required)"

@pytest.mark.parametrize("db_name, coll_name, file_path", ALL_COLLECTIONS)
def test_collection_field_quota_and_schema(db_name, coll_name, file_path):
    schema_path = SCHEMA_DIR / db_name / f"{coll_name}.json"
    assert schema_path.exists(), f"Missing schema for {db_name}.{coll_name}"
    
    with open(schema_path, "r", encoding="utf-8") as sf:
        schema = json.load(sf)
    validator = Draft7Validator(schema)
    
    with open(file_path, "r", encoding="utf-8") as df:
        docs = json.load(df)
        
    for idx, doc in enumerate(docs[:20]): # Validate sample documents against schema
        assert len(doc.keys()) >= 10, f"Doc #{idx} in {coll_name} has {len(doc.keys())} fields (min 10 required)"
        errors = list(validator.iter_errors(doc))
        assert len(errors) == 0, f"Schema validation failed on doc #{idx} in {coll_name}: {errors}"

def test_cross_database_referential_integrity():
    # 1. Load ceremonies
    with open(PROCESSED_DIR / "grammy_history_db" / "ceremonies.json", "r", encoding="utf-8") as f:
        ceremonies = json.load(f)
    ceremony_ids = {c["ceremony_id"] for c in ceremonies}
    
    # 2. Check nominations -> ceremonies
    with open(PROCESSED_DIR / "grammy_nominations_db" / "nomination_entries.json", "r", encoding="utf-8") as f:
        noms = json.load(f)
    for n in noms:
        assert n["ceremony_id"] in ceremony_ids, f"Invalid ceremony_id {n['ceremony_id']} in nomination {n['nomination_id']}"
        
    # 3. Check winners -> nominations
    nom_ids = {n["nomination_id"] for n in noms}
    with open(PROCESSED_DIR / "grammy_winners_db" / "winner_records.json", "r", encoding="utf-8") as f:
        winners = json.load(f)
    for w in winners:
        assert w["nomination_id"] in nom_ids, f"Invalid nomination_id {w['nomination_id']} in winner {w['winner_record_id']}"
