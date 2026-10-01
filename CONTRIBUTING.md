# Contributing to the GRAMMY Awards Information & Analytics System

Welcome to the **GRAMMY Awards Information & Analytics System** project! This repository represents an academic DBMS collaboration among five team members.

---

## 1. Team Responsibility Matrix

| Member | Assigned Database | Primary Modules | Domain Focus |
| :--- | :--- | :--- | :--- |
| **Member 1** | `grammy_history_db` | Module 1 & 6 | Ceremonies, venues, telecasts, ratings, hosts, milestones |
| **Member 2** | `grammy_categories_db` | Module 2 & 3 | Fields, categories, lineage, eligibility, voting procedures |
| **Member 3** | `grammy_nominations_db` | Module 4 & 5 | Nomination entries, works, credits, submissions, audits |
| **Member 4** | `grammy_winners_db` | Module 7 & 9 | Winners, Big Four sweeps, record breakers, speeches, trophies |
| **Member 5** | `grammy_creators_db` | Module 8 & 10 | Artists, producers, engineers, songwriters, labels, groups |

---

## 2. Development Workflow & Git Rules

1. **Branching Model**:
   - `main`: Production-ready, fully validated codebase.
   - Feature branches: `feature/<member>-<module>` (e.g., `feature/m1-history-queries`).
2. **Never Commit Secrets**:
   - Always copy `.env.example` to `.env`.
   - Never commit connection strings, passwords, or Atlas URIs to git.
3. **Data Integrity**:
   - Never generate or fabricate fake data. All data must originate from verified sources (Recording Academy archives, MusicBrainz CC0, or verified open datasets).
   - Ensure all collections contain $\ge 50$ documents and $\ge 10$ meaningful domain fields.
4. **Mandatory Pre-Commit Checks**:
   - Run unit and schema tests before committing:
     ```powershell
     pytest tests -v
     python scripts/validation/validate_system.py
     ```
   - Ensure 100% of test cases pass.
