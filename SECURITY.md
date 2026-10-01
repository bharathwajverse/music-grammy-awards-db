# Security Policy

## Academic Security & Secrets Management

The **GRAMMY Awards Information & Analytics System** enforces strict security hygiene:

1. **Zero Plaintext Secrets**:
   - Connection strings containing MongoDB Atlas credentials must reside exclusively in local `.env` files.
   - The `.gitignore` file enforces that `.env` is never indexed or committed to version control.
   - A sanitized `.env.example` file is provided as a configuration template.

2. **Reporting Security Concerns**:
   - If sensitive credentials or connection URIs are inadvertently committed, immediately revoke the Atlas database user credentials from the MongoDB Atlas Security console and regenerate the credentials.
