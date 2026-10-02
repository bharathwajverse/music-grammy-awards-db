"""Test suite for Step 16: Environment Configuration, Atlas Connection & Zero-Secret Security.

Validates that:
1. .env is strictly ignored by Git via .gitignore.
2. .env defines MONGODB_URI and MONGODB_ATLAS_URI.
3. .env.example exists with sanitized placeholders.
4. No cleartext Atlas passwords are committed in tracked repository files.
"""

import os
import re
import subprocess
from pathlib import Path
import pytest
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_gitignore_contains_env():
    """Verify that .gitignore explicitly ignores .env and environment variants."""
    gitignore_path = REPO_ROOT / ".gitignore"
    assert gitignore_path.exists(), ".gitignore file must exist"
    content = gitignore_path.read_text(encoding="utf-8").splitlines()
    assert ".env" in [line.strip() for line in content], ".env must be explicitly listed in .gitignore"


def test_env_is_gitignored():
    """Verify via git check-ignore that .env is not tracked and is ignored."""
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        result = subprocess.run(
            ["git", "check-ignore", "-v", ".env"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False
        )
        assert result.returncode == 0, ".env should be ignored by git"
        assert ".env" in result.stdout, f"Expected .env to match ignore rule, got: {result.stdout}"


def test_env_defines_mongodb_uri():
    """Verify that .env defines MONGODB_URI and MONGODB_ATLAS_URI."""
    env_path = REPO_ROOT / ".env"
    assert env_path.exists(), ".env file must exist in workspace root"
    load_dotenv(env_path)
    
    uri = os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    assert uri is not None, "MONGODB_URI or MONGODB_ATLAS_URI must be defined in .env"
    assert uri.startswith("mongodb+srv://") or uri.startswith("mongodb://"), "URI must have valid MongoDB protocol"


def test_env_example_is_sanitized():
    """Verify that .env.example exists and contains only sanitized placeholders."""
    example_path = REPO_ROOT / ".env.example"
    assert example_path.exists(), ".env.example template must exist"
    content = example_path.read_text(encoding="utf-8")
    assert "MONGODB_URI" in content or "MONGODB_ATLAS_URI" in content
    # Ensure no real system passwords in .env.example
    assert "system:system" not in content, ".env.example must not contain live credentials"


def test_tracked_files_do_not_contain_hardcoded_atlas_passwords():
    """Scan tracked files to ensure no live cluster credentials with system:system are committed."""
    # Run git ls-files to get all tracked files
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True
    )
    tracked_files = [REPO_ROOT / f for f in result.stdout.splitlines() if f.strip()]
    
    # Credentials pattern matching live credentials
    live_cred_pattern = re.compile(r"mongodb\+srv://system:system@cluster0")
    
    violations = []
    for f in tracked_files:
        # Exclude this test file from checking itself
        if f.name == "test_environment_and_secrets.py":
            continue
        try:
            text = f.read_text(encoding="utf-8")
            if live_cred_pattern.search(text):
                violations.append(str(f.relative_to(REPO_ROOT)))
        except Exception:
            pass
            
    assert not violations, f"Live credentials found in tracked files: {violations}"


def test_mongodb_connection_doc_exists_and_is_sanitized():
    """Verify that docs/mongodb/connection.md exists and contains only sanitized config."""
    doc_path = REPO_ROOT / "docs" / "mongodb" / "connection.md"
    assert doc_path.exists(), "docs/mongodb/connection.md must exist for Phase 12"
    
    content = doc_path.read_text(encoding="utf-8")
    # Verify required sections
    assert "Phase 12" in content
    assert "MongoDB Atlas" in content
    assert "Cluster Topology" in content
    assert "Network Security" in content
    assert "Target Logical Databases" in content
    assert "Connectivity Verification" in content
    
    # Verify zero live credentials
    assert "system:system" not in content, "docs/mongodb/connection.md must not contain live credentials"
    assert "mongodb+srv://system:" not in content, "docs/mongodb/connection.md must not expose usernames with passwords"
    
    # Verify safe masking patterns are documented
    assert "<username>:<password>" in content or ":****@" in content

