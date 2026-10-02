"""
=============================================================================
Phase 29 & 30 Test Suite: Presentation Slide Deck & Viva Handbook Verification
=============================================================================
Course: Advanced Database Management Systems (ADBMS)
Module: Capstone Presentation & Defense (Phases 29 & 30)
Files Verified:
  - presentation/grammy-presentation.md
  - presentation/demo_walkthrough_script.md
  - docs/viva-preparation.md
=============================================================================
"""

import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

PRESENTATION_FILE = REPO_ROOT / "presentation" / "grammy-presentation.md"
WALKTHROUGH_FILE = REPO_ROOT / "presentation" / "demo_walkthrough_script.md"
VIVA_FILE = REPO_ROOT / "docs" / "viva-preparation.md"


def test_presentation_file_exists_and_is_non_empty():
    """Verifies that presentation/grammy-presentation.md exists and is substantive."""
    assert PRESENTATION_FILE.exists(), "presentation/grammy-presentation.md does not exist!"
    content = PRESENTATION_FILE.read_text(encoding="utf-8")
    assert len(content) > 5000, "Presentation content is too short or empty!"


def test_presentation_has_marp_headers_and_slide_separators():
    """Verifies slide formatting with Marp frontmatter and slide separators."""
    content = PRESENTATION_FILE.read_text(encoding="utf-8")
    assert "marp: true" in content, "Missing Marp header in presentation slide deck!"
    separators = content.count("\n---\n")
    assert separators >= 19, f"Expected at least 19 slide separators, found {separators}"


REQUIRED_SLIDE_TITLES = [
    ("Slide 1", ["Title", "GRAMMY Awards Information & Analytics System"]),
    ("Slide 2", ["Problem", "The Database Challenges"]),
    ("Slide 3", ["Objectives", "Engineering & Theoretical Goals"]),
    ("Slide 4", ["Real-World Data", "Authoritative Acquisition"]),
    ("Slide 5", ["Architecture", "Distributed Microservice"]),
    ("Slide 6", ["Five Dedicated Databases", "Autonomous Physical Storage"]),
    ("Slide 7", ["EER", "Enhanced Entity-Relationship Constructs"]),
    ("Slide 8", ["Relational Model", "Relational Algebra"]),
    ("Slide 9", ["Normalization", "1NF to 5NF"]),
    ("Slide 10", ["MongoDB Document Modeling", "JSON Schema"]),
    ("Slide 11", ["Data Statistics", "5,190"]),
    ("Slide 12", ["CRUD", "Operations Architecture"]),
    ("Slide 13", ["Advanced Querying", "Capabilities"]),
    ("Slide 14", ["Aggregation", "Multi-Stage Analytical"]),
    ("Slide 15", ["Transactions", "Concurrency"]),
    ("Slide 16", ["Storage", "Recovery"]),
    ("Slide 17", ["Validation", "Quality Assurance"]),
    ("Slide 18", ["Results", "System Achievements"]),
    ("Slide 19", ["Limitations", "Technical Constraints"]),
    ("Slide 20", ["Conclusion", "Future Scope"]),
]


@pytest.mark.parametrize("slide_num, keywords", REQUIRED_SLIDE_TITLES)
def test_all_20_slides_present_in_presentation(slide_num, keywords):
    """Verifies that all 20 required slide topics are explicitly present."""
    content = PRESENTATION_FILE.read_text(encoding="utf-8")
    assert f"# {slide_num}:" in content, f"Missing header for {slide_num} in presentation!"
    for kw in keywords:
        assert kw.lower() in content.lower(), f"Keyword '{kw}' missing from {slide_num}!"


def test_presentation_grounded_in_actual_project_data():
    """Verifies that presentation references actual project counts, databases, and metrics."""
    content = PRESENTATION_FILE.read_text(encoding="utf-8")
    assert "5,190" in content, "Presentation must reference actual document count (5,190)!"
    assert "grammy_history_db" in content
    assert "grammy_categories_db" in content
    assert "grammy_nominations_db" in content
    assert "grammy_winners_db" in content
    assert "grammy_creators_db" in content
    assert "WiredTiger" in content
    assert "Snappy" in content
    assert "32.9%" in content
    assert "629" in content
    assert "AtlasError 8000" in content
    assert "73.42" in content


def test_demo_walkthrough_script_exists_and_covers_all_slides():
    """Verifies that presentation/demo_walkthrough_script.md exists and covers all 20 slides."""
    assert WALKTHROUGH_FILE.exists(), "presentation/demo_walkthrough_script.md is missing!"
    content = WALKTHROUGH_FILE.read_text(encoding="utf-8")
    for i in range(1, 21):
        assert f"Slide {i}:" in content or f"Slide {i} " in content, f"Walkthrough missing Slide {i} script!"
    assert "Live Demonstration Protocol" in content


def test_viva_file_exists_and_is_comprehensive():
    """Verifies that docs/viva-preparation.md exists and is substantive."""
    assert VIVA_FILE.exists(), "docs/viva-preparation.md does not exist!"
    content = VIVA_FILE.read_text(encoding="utf-8")
    assert len(content) > 15000, "Viva preparation document is insufficiently detailed!"


def test_five_member_viva_responsibility_matrix():
    """Verifies that the five-member viva responsibility matrix exists with all 5 members."""
    content = VIVA_FILE.read_text(encoding="utf-8")
    assert "Five-Member Viva Responsibility & Defense Matrix" in content
    for member_idx in range(1, 6):
        assert f"Member {member_idx}" in content, f"Member {member_idx} missing from responsibility matrix!"
    assert "grammy_history_db" in content
    assert "grammy_categories_db" in content
    assert "grammy_nominations_db" in content
    assert "grammy_winners_db" in content
    assert "grammy_creators_db" in content


def test_viva_basic_questions_count():
    """Verifies that Section 1 contains all 50 basic viva questions (Q1 to Q50)."""
    content = VIVA_FILE.read_text(encoding="utf-8")
    assert "Section 1: 50 Basic Viva Questions & Answers" in content
    for q_idx in range(1, 51):
        assert f"#### Q{q_idx}:" in content, f"Basic question Q{q_idx} missing!"


def test_viva_intermediate_questions_count():
    """Verifies that Section 2 contains all 50 intermediate viva questions (Q51 to Q100)."""
    content = VIVA_FILE.read_text(encoding="utf-8")
    assert "Section 2: 50 Intermediate Viva Questions & Answers" in content
    for q_idx in range(51, 101):
        assert f"#### Q{q_idx}:" in content, f"Intermediate question Q{q_idx} missing!"


def test_viva_advanced_questions_count():
    """Verifies that Section 3 contains all 30 advanced viva questions (Q101 to Q130)."""
    content = VIVA_FILE.read_text(encoding="utf-8")
    assert "Section 3: 30 Advanced Viva Questions & Answers" in content
    for q_idx in range(101, 131):
        assert f"#### Q{q_idx}:" in content, f"Advanced question Q{q_idx} missing!"


TOPIC_QUESTION_SECTIONS = [
    ("Section 4: Dedicated Questions on Conceptual EER Modeling", range(131, 141)),
    ("Section 5: Dedicated Questions on Functional Dependencies & Normalization", range(141, 151)),
    ("Section 6: Dedicated Questions on MongoDB Document Modeling", range(151, 161)),
    ("Section 7: Dedicated Questions on Aggregation Pipelines", range(161, 171)),
    ("Section 8: Dedicated Questions on Multi-Document ACID Transactions", range(171, 181)),
    ("Section 9: Dedicated Questions on Concurrency Control & Serializability", range(181, 191)),
    ("Section 10: Dedicated Questions on Physical Storage Architecture & RAID", range(191, 201)),
    ("Section 11: Dedicated Questions on Crash Recovery & ARIES", range(201, 211)),
    ("Section 12: Dedicated Questions on Data Sources & Ingestion", range(211, 221)),
    ("Section 13: Dedicated Questions on Licensing & Provenance", range(221, 231)),
]


@pytest.mark.parametrize("section_title, q_range", TOPIC_QUESTION_SECTIONS)
def test_viva_topic_sections_and_questions(section_title, q_range):
    """Verifies that all 10 topic-specific question groups 4–13 exist with valid questions."""
    content = VIVA_FILE.read_text(encoding="utf-8")
    assert section_title in content, f"Topic section '{section_title}' missing!"
    for q_idx in q_range:
        assert f"#### Q{q_idx}:" in content, f"Topic question Q{q_idx} missing in '{section_title}'!"


def test_viva_answers_contain_project_facts():
    """Verifies that answers are substantive and explicitly use real project facts."""
    content = VIVA_FILE.read_text(encoding="utf-8")
    assert "**Answer**:" in content
    assert "5,190" in content
    assert "WiredTiger" in content
    assert "Snappy" in content
    assert "73.42" in content
    assert "Feist Publications" in content
    assert "ARIES" in content
    assert "Strict 2PL" in content
    assert "relational division" in content.lower()


PROJECT_STATUS_FILE = REPO_ROOT / "docs" / "project-status.md"
PHASE_MATRIX_FILE = REPO_ROOT / "docs" / "final-audit" / "30-phase-completion-matrix.csv"
REQ_MATRIX_FILE = REPO_ROOT / "docs" / "final-audit" / "requirements-compliance-matrix.csv"


def test_project_status_and_audit_completion():
    """Verifies that project status and final audit matrices formally record Phase 29 and 30 completed."""
    assert PROJECT_STATUS_FILE.exists(), "docs/project-status.md is missing!"
    status_content = PROJECT_STATUS_FILE.read_text(encoding="utf-8")
    assert "Phase 29" in status_content, "Phase 29 missing from project status!"
    assert "Phase 30" in status_content, "Phase 30 missing from project status!"
    assert "30/30" in status_content or "30 of 30" in status_content, "Project status must record 30/30 phases complete!"
    assert "Phases 1 through 30 Fully Completed" in status_content

    assert PHASE_MATRIX_FILE.exists(), "30-phase-completion-matrix.csv is missing!"
    phase_content = PHASE_MATRIX_FILE.read_text(encoding="utf-8")
    assert "Phase 29,Final Project Presentation & Slide Deck,Slide deck (presentation/); executive summary slides; system demo video walkthrough,COMPLETE" in phase_content
    assert "Phase 30,Viva Voce Defense Preparation & Exam Questions,Viva voce preparation guide; theoretical defense Q&A across 10 modules; examiner defense notes,COMPLETE" in phase_content

    assert REQ_MATRIX_FILE.exists(), "requirements-compliance-matrix.csv is missing!"
    req_content = REQ_MATRIX_FILE.read_text(encoding="utf-8")
    assert "REQ-31,Presentation,Final presentation slides and project walkthrough video,Slide deck and video presentation artifacts,PASS" in req_content
    assert "REQ-32,Viva preparation,Oral defense questions; examiner answers; syllabus review,Viva voce question bank and academic defense notes,PASS" in req_content

