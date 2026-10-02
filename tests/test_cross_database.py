"""
=============================================================================
Phase 26 Test Suite: Five-Database Cross-Database Integration
=============================================================================
Course: Advanced Database Management Systems (ADBMS)
Module: Module 8/9/10 — Distributed MongoDB Architecture & Multi-Database Joins
Phase: PHASE 26 — FIVE-DATABASE INTEGRATION

Verifies:
  1. All five distinct databases exist and are active on MongoDB Atlas.
  2. All shared identifier formats conform to canonical regular expressions.
  3. Every cross-database foreign reference satisfies 100% referential integrity (0 orphans).
  4. Explicit verification that legacy 'edition_id' is absent from ceremonies.
  5. Application-level cross-database join scenarios execute correctly:
     - Scenario 1: Artist nominations (creators + nominations)
     - Scenario 2: Artist wins with ceremony metadata (winners + creators + history)
     - Scenario 3: Winner records with category taxonomy (winners + categories)
     - Scenario 4: Ceremony winners with hosting venue details (winners + history)
  6. Deliverable documentation and scripts exist on disk.
=============================================================================
"""

import os
import certifi
import pytest
import pymongo
from pathlib import Path
from dotenv import load_dotenv

import sys
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.integration.cross_database_validation import (
    CrossDatabaseIntegrator,
    SYSTEM_DATABASES,
    SHARED_IDENTIFIER_PATTERNS,
)


@pytest.fixture(scope="session")
def integrator():
    """Session fixture initializing the cross-database integrator."""
    load_dotenv(REPO_ROOT / ".env")
    uri = os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    assert uri, "MONGODB_URI must be set in .env"
    client = pymongo.MongoClient(
        uri,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
    )
    return CrossDatabaseIntegrator(client=client)


# -----------------------------------------------------------------------------
# 1. Database Existence & Documentation Verification
# -----------------------------------------------------------------------------

def test_integration_deliverables_exist():
    """Verifies all Phase 26 required deliverable files exist."""
    assert (REPO_ROOT / "docs" / "integration.md").exists(), "docs/integration.md missing!"
    assert (REPO_ROOT / "tests" / "cross-database-validation.md").exists(), "tests/cross-database-validation.md missing!"
    assert (REPO_ROOT / "scripts" / "integration" / "cross_database_validation.py").exists(), "validation script missing!"


def test_all_five_databases_exist(integrator):
    """Verifies that all five separate databases exist on the MongoDB cluster."""
    db_status = integrator.validate_database_existence()
    for db_name, exists in db_status.items():
        assert exists, f"Database '{db_name}' not found on MongoDB Atlas cluster!"


# -----------------------------------------------------------------------------
# 2. Shared Identifier Formats
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("id_name", list(SHARED_IDENTIFIER_PATTERNS.keys()))
def test_shared_identifier_formats(integrator, id_name):
    """Verifies that sample shared IDs in the databases adhere to canonical regex formats."""
    results = integrator.validate_identifier_formats()
    assert id_name in results, f"Missing format check for {id_name}"
    check = results[id_name]
    assert check["valid"], (
        f"Identifier format failure for '{id_name}': sample='{check['sample']}', pattern='{check['pattern']}'"
    )


def test_absence_of_edition_id_in_ceremonies(integrator):
    """Verifies that legacy 'edition_id' field is absent in ceremonies collection.

    The canonical ceremony identifier is 'ceremony_id' (e.g., CEREMONY_028).
    """
    ceremony_with_edition = integrator.history_db.ceremonies.find_one({"edition_id": {"$exists": True}})
    assert ceremony_with_edition is None, "ceremonies collection should NOT contain legacy edition_id field!"


# -----------------------------------------------------------------------------
# 3. Cross-Database Referential Integrity Checks (100% Zero-Orphan Closure)
# -----------------------------------------------------------------------------

def test_ceremony_id_integrity_in_nominations(integrator):
    """Every ceremony_id in nomination_entries must exist in ceremonies."""
    ceremony_pks = set(integrator.history_db.ceremonies.distinct("ceremony_id"))
    nom_fks = set(integrator.nom_db.nomination_entries.distinct("ceremony_id"))
    orphans = nom_fks - ceremony_pks
    assert len(orphans) == 0, f"Orphan ceremony_id values found in nomination_entries: {orphans}"


def test_ceremony_id_integrity_in_winners(integrator):
    """Every ceremony_id in winner_records must exist in ceremonies."""
    ceremony_pks = set(integrator.history_db.ceremonies.distinct("ceremony_id"))
    win_fks = set(integrator.win_db.winner_records.distinct("ceremony_id"))
    orphans = win_fks - ceremony_pks
    assert len(orphans) == 0, f"Orphan ceremony_id values found in winner_records: {orphans}"


def test_venue_id_integrity_in_ceremonies(integrator):
    """Every venue_id in ceremonies must exist in venues."""
    venue_pks = set(integrator.history_db.venues.distinct("venue_id"))
    ceremony_fks = set(integrator.history_db.ceremonies.distinct("venue_id"))
    orphans = ceremony_fks - venue_pks
    assert len(orphans) == 0, f"Orphan venue_id values found in ceremonies: {orphans}"


def test_category_id_integrity_in_nominations(integrator):
    """Every category_id in nomination_entries must exist in award_categories."""
    cat_pks = set(integrator.cat_db.award_categories.distinct("category_id"))
    nom_fks = set(integrator.nom_db.nomination_entries.distinct("category_id"))
    orphans = nom_fks - cat_pks
    assert len(orphans) == 0, f"Orphan category_id values found in nomination_entries: {orphans}"


def test_category_id_integrity_in_winners(integrator):
    """Every category_id in winner_records must exist in award_categories."""
    cat_pks = set(integrator.cat_db.award_categories.distinct("category_id"))
    win_fks = set(integrator.win_db.winner_records.distinct("category_id"))
    orphans = win_fks - cat_pks
    assert len(orphans) == 0, f"Orphan category_id values found in winner_records: {orphans}"


def test_nomination_id_integrity_in_winners(integrator):
    """Every nomination_id in winner_records must exist in nomination_entries."""
    nom_pks = set(integrator.nom_db.nomination_entries.distinct("nomination_id"))
    win_fks = set(integrator.win_db.winner_records.distinct("nomination_id"))
    orphans = win_fks - nom_pks
    assert len(orphans) == 0, f"Orphan nomination_id values found in winner_records: {orphans}"


def test_artist_id_integrity_in_nominations(integrator):
    """Every primary_artist_id in nomination_entries must exist in artists."""
    artist_pks = set(integrator.crt_db.artists.distinct("artist_id"))
    nom_fks = set(integrator.nom_db.nomination_entries.distinct("primary_artist_id"))
    orphans = nom_fks - artist_pks
    assert len(orphans) == 0, f"Orphan primary_artist_id values found in nomination_entries: {orphans}"


def test_artist_id_integrity_in_winners(integrator):
    """Every primary_artist_id in winner_records must exist in artists."""
    artist_pks = set(integrator.crt_db.artists.distinct("artist_id"))
    win_fks = set(integrator.win_db.winner_records.distinct("primary_artist_id"))
    orphans = win_fks - artist_pks
    assert len(orphans) == 0, f"Orphan primary_artist_id values found in winner_records: {orphans}"


def test_work_id_integrity_in_nominations(integrator):
    """Every work_id in nomination_entries must exist in nominated_works."""
    work_pks = set(integrator.nom_db.nominated_works.distinct("work_id"))
    nom_fks = set(integrator.nom_db.nomination_entries.distinct("work_id"))
    orphans = nom_fks - work_pks
    assert len(orphans) == 0, f"Orphan work_id values found in nomination_entries: {orphans}"


def test_winning_work_id_integrity_in_winners(integrator):
    """Every winning_work_id in winner_records must exist in nominated_works."""
    work_pks = set(integrator.nom_db.nominated_works.distinct("work_id"))
    win_fks = set(integrator.win_db.winner_records.distinct("winning_work_id"))
    orphans = win_fks - work_pks
    assert len(orphans) == 0, f"Orphan winning_work_id values found in winner_records: {orphans}"


def test_winner_record_id_integrity_in_trophies(integrator):
    """Every winner_record_id in trophy_tracking must exist in winner_records."""
    win_pks = set(integrator.win_db.winner_records.distinct("winner_record_id"))
    trophy_fks = set(integrator.win_db.trophy_tracking.distinct("winner_record_id"))
    orphans = trophy_fks - win_pks
    assert len(orphans) == 0, f"Orphan winner_record_id values found in trophy_tracking: {orphans}"


# -----------------------------------------------------------------------------
# 4. Cross-Database Analytical Scenarios (Application-Level Joins)
# -----------------------------------------------------------------------------

def test_scenario_1_artist_nominations(integrator):
    """Scenario 1: Join grammy_creators_db and grammy_nominations_db for an artist."""
    result = integrator.scenario_1_nominations_for_artist("CRT_ELLA_FITZGERALD_0002")
    assert "error" not in result, f"Scenario 1 failed with error: {result.get('error')}"
    assert result["artist_name"] == "Ella Fitzgerald"
    assert result["total_nominations"] > 0
    # Check enriched structure
    nom = result["nominations"][0]
    assert "nomination_id" in nom
    assert "work_title" in nom
    assert "category_id" in nom
    assert "ceremony_id" in nom


def test_scenario_2_artist_wins_with_ceremonies(integrator):
    """Scenario 2: Join grammy_winners_db + creators_db + history_db for an artist."""
    result = integrator.scenario_2_wins_for_artist_with_ceremony("CRT_ELLA_FITZGERALD_0002")
    assert "error" not in result, f"Scenario 2 failed with error: {result.get('error')}"
    assert result["artist_name"] == "Ella Fitzgerald"
    assert result["total_wins"] > 0
    # Check enriched ceremony structure
    win = result["wins"][0]
    assert "winner_record_id" in win
    assert "broadcast_year" in win
    assert win["broadcast_year"] >= 1959
    assert "edition_number" in win
    assert "venue_id" in win


def test_scenario_3_category_info_for_winners(integrator):
    """Scenario 3: Join grammy_winners_db + grammy_categories_db."""
    result = integrator.scenario_3_category_info_for_winners(limit=10)
    assert len(result["results"]) == 10
    sample = result["results"][0]
    assert "category_name" in sample
    assert sample["category_name"] != "Unknown Category"
    assert "field_name" in sample
    assert "maximum_nominees_allowed" in sample


def test_scenario_4_venue_details_for_ceremony_winners(integrator):
    """Scenario 4: Join grammy_winners_db + grammy_history_db (ceremonies & venues)."""
    result = integrator.scenario_4_venue_details_for_ceremony_winners(limit=10)
    assert len(result["results"]) == 10
    sample = result["results"][0]
    assert "venue_name" in sample
    assert sample["venue_name"] != "Unknown Venue"
    assert "venue_location" in sample
    assert "broadcast_year" in sample


# -----------------------------------------------------------------------------
# 5. Robustness & Edge-Case Probing (Error paths, Boundaries, Cross-Collection Formats)
# -----------------------------------------------------------------------------

def test_scenario_1_nonexistent_or_invalid_artist(integrator):
    """Probes Scenario 1 with non-existent, empty, and None artist inputs."""
    res_none = integrator.scenario_1_nominations_for_artist(None)
    assert "error" in res_none

    res_empty = integrator.scenario_1_nominations_for_artist("")
    assert "error" in res_empty

    res_spaces = integrator.scenario_1_nominations_for_artist("   ")
    assert "error" in res_spaces

    res_missing = integrator.scenario_1_nominations_for_artist("CRT_NON_EXISTENT_ARTIST_9999")
    assert "error" in res_missing
    assert "not found" in res_missing["error"]


def test_scenario_2_nonexistent_or_invalid_artist(integrator):
    """Probes Scenario 2 with non-existent, empty, and None artist inputs."""
    res_none = integrator.scenario_2_wins_for_artist_with_ceremony(None)
    assert "error" in res_none

    res_empty = integrator.scenario_2_wins_for_artist_with_ceremony("")
    assert "error" in res_empty

    res_missing = integrator.scenario_2_wins_for_artist_with_ceremony("CRT_NON_EXISTENT_ARTIST_9999")
    assert "error" in res_missing
    assert "not found" in res_missing["error"]


def test_scenario_3_ceremony_filter_and_zero_limit(integrator):
    """Probes Scenario 3 with explicit ceremony filtering and boundary limit=0."""
    res_filtered = integrator.scenario_3_category_info_for_winners(limit=5, ceremony_id="CEREMONY_001")
    assert len(res_filtered["results"]) > 0
    for r in res_filtered["results"]:
        assert r["ceremony_id"] == "CEREMONY_001"

    res_zero = integrator.scenario_3_category_info_for_winners(limit=0)
    assert len(res_zero["results"]) == 0
    assert res_zero["sample_size"] == 0


def test_scenario_4_ceremony_filter_and_zero_limit(integrator):
    """Probes Scenario 4 with explicit ceremony filtering and boundary limit=0."""
    res_filtered = integrator.scenario_4_venue_details_for_ceremony_winners(limit=5, ceremony_id="CEREMONY_001")
    assert len(res_filtered["results"]) > 0
    for r in res_filtered["results"]:
        assert r["ceremony_id"] == "CEREMONY_001"

    res_zero = integrator.scenario_4_venue_details_for_ceremony_winners(limit=0)
    assert len(res_zero["results"]) == 0
    assert res_zero["sample_size"] == 0


def test_all_shared_identifiers_in_referencing_collections(integrator):
    """Verifies that 100% of foreign key values in consuming collections conform to canonical regex."""
    nom_ceremonies = integrator.nom_db.nomination_entries.distinct("ceremony_id")
    assert all(SHARED_IDENTIFIER_PATTERNS["ceremony_id"].match(x) for x in nom_ceremonies)

    win_ceremonies = integrator.win_db.winner_records.distinct("ceremony_id")
    assert all(SHARED_IDENTIFIER_PATTERNS["ceremony_id"].match(x) for x in win_ceremonies)

    ceremony_venues = integrator.history_db.ceremonies.distinct("venue_id")
    assert all(SHARED_IDENTIFIER_PATTERNS["venue_id"].match(x) for x in ceremony_venues)

    nom_categories = integrator.nom_db.nomination_entries.distinct("category_id")
    assert all(SHARED_IDENTIFIER_PATTERNS["category_id"].match(x) for x in nom_categories)

    win_categories = integrator.win_db.winner_records.distinct("category_id")
    assert all(SHARED_IDENTIFIER_PATTERNS["category_id"].match(x) for x in win_categories)

    win_nominations = integrator.win_db.winner_records.distinct("nomination_id")
    assert all(SHARED_IDENTIFIER_PATTERNS["nomination_id"].match(x) for x in win_nominations)

    nom_artists = integrator.nom_db.nomination_entries.distinct("primary_artist_id")
    assert all(SHARED_IDENTIFIER_PATTERNS["artist_id"].match(x) for x in nom_artists)

    win_artists = integrator.win_db.winner_records.distinct("primary_artist_id")
    assert all(SHARED_IDENTIFIER_PATTERNS["artist_id"].match(x) for x in win_artists)

    nom_works = integrator.nom_db.nomination_entries.distinct("work_id")
    assert all(SHARED_IDENTIFIER_PATTERNS["work_id"].match(x) for x in nom_works)

    win_works = integrator.win_db.winner_records.distinct("winning_work_id")
    assert all(SHARED_IDENTIFIER_PATTERNS["work_id"].match(x) for x in win_works)

    trophy_winners = integrator.win_db.trophy_tracking.distinct("winner_record_id")
    assert all(SHARED_IDENTIFIER_PATTERNS["winner_record_id"].match(x) for x in trophy_winners)
