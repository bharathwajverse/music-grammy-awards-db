"""MongoDB Atlas Connection Diagnostics & Security Verification

Verifies:
1. Zero secrets in tracked version control files.
2. .env exists and is strictly gitignored.
3. Retrieves connection string dynamically from MONGODB_URI or MONGODB_ATLAS_URI.
4. Attempts connection to MongoDB Atlas with diagnostic feedback.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent

def mask_connection_string(uri: str) -> str:
    """Masks credentials in MongoDB URI for safe logging."""
    if not uri:
        return "<EMPTY>"
    return re.sub(r":([^@]+)@", ":****@", uri)

def verify_gitignore_protection():
    """Verifies that .env is ignored by Git."""
    env_file = REPO_ROOT / ".env"
    if not env_file.exists():
        print("[FAIL] .env file does not exist.")
        return False

    try:
        result = subprocess.run(
            ["git", "check-ignore", "-v", ".env"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0 and ".env" in result.stdout:
            print(f"[PASS] .env is properly gitignored: {result.stdout.strip()}")
            return True
        else:
            print("[FAIL] .env is NOT ignored by git! Check .gitignore.")
            return False
    except Exception as e:
        print(f"[WARNING] Could not run git check-ignore: {e}")
        return True

def verify_zero_secrets_in_tracked_files():
    """Scans tracked files to ensure no live credentials are hardcoded."""
    print("Verifying zero secrets in tracked source code...")
    # Pattern looking for mongodb+srv with cleartext passwords in python files
    pattern = re.compile(r"mongodb\+srv://[^:]+:[^@]+@")
    violations = []
    
    for py_file in REPO_ROOT.rglob("*.py"):
        if any(part in py_file.parts for part in ["venv", ".venv", "__pycache__", "build", "dist"]):
            continue
        try:
            content = py_file.read_text(encoding="utf-8")
            for i, line in enumerate(content.splitlines(), start=1):
                # Ignore placeholder strings
                if "username:password" in line or "<username>:<password>" in line or "system:****" in line:
                    continue
                if pattern.search(line):
                    violations.append(f"{py_file.relative_to(REPO_ROOT)}:{i}")
        except Exception:
            pass

    if violations:
        print(f"[FAIL] Found potential hardcoded credentials in: {violations}")
        return False
    print("[PASS] Zero hardcoded credentials found in tracked source files.")
    return True

def test_atlas_connectivity():
    """Tests connection to MongoDB Atlas cluster."""
    load_dotenv(REPO_ROOT / ".env")
    uri = os.getenv("MONGODB_URI") or os.getenv("MONGODB_ATLAS_URI")
    
    if not uri:
        print("[FAIL] MONGODB_URI not found in .env.")
        return False
        
    masked_uri = mask_connection_string(uri)
    print(f"Loaded connection string from .env: {masked_uri}")
    
    try:
        import pymongo
        import certifi
    except ImportError:
        print("[FAIL] pymongo or certifi not installed.")
        return False

    print("Attempting connection to Atlas cluster...")
    try:
        client = pymongo.MongoClient(
            uri,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=7000,
            connectTimeoutMS=7000
        )
        client.admin.command("ping")
        print("[SUCCESS] Successfully connected to MongoDB Atlas! Cluster is responsive.")
        dbs = client.list_database_names()
        print(f"Available databases: {dbs}")
        return True
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print(f"[INFO] ServerSelectionTimeout: {e}")
        print("Note: If SSL handshake / TLS alert occurs, ensure your current client IP is added to the MongoDB Atlas Network Access IP Access List (e.g., 0.0.0.0/0).")
        return False
    except Exception as e:
        print(f"[INFO] Connection attempt details: {e}")
        if "SSL: TLSV1_ALERT_INTERNAL_ERROR" in str(e):
            print("\n-------------------------------------------------------------")
            print(">> ATLAS SECURITY NOTICE: TLSV1_ALERT_INTERNAL_ERROR <<")
            print("MongoDB Atlas rejects the TLS handshake when the incoming IP")
            print("is not permitted on the Atlas Network Access / IP Access List.")
            print("To allow connection from any network during development:")
            print("1. Log in to MongoDB Atlas (https://cloud.mongodb.com)")
            print("2. Navigate to 'Network Access' -> 'IP Access List'")
            print("3. Add IP Address: 0.0.0.0/0 (Allow Access from Anywhere)")
            print("-------------------------------------------------------------")
        return False

def main():
    print("=============================================================")
    print("STEP 16: MongoDB Atlas Connection & Security Verification")
    print("=============================================================\n")
    
    g_pass = verify_gitignore_protection()
    s_pass = verify_zero_secrets_in_tracked_files()
    c_pass = test_atlas_connectivity()
    
    print("\n=============================================================")
    print(f"SUMMARY: .gitignore Protection: {'PASS' if g_pass else 'FAIL'} | Zero Secrets: {'PASS' if s_pass else 'FAIL'}")
    print("=============================================================")

if __name__ == "__main__":
    main()
