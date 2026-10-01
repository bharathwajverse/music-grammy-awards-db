# Master Project Instructions: GRAMMY Awards Information & Analytics System

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Architecture**: 5 Distributed MongoDB Databases | 50 Collections (10 per DB) | 50+ Documents per Collection | 10+ Meaningful Fields per Document  
> **Team Scope**: 5 Group Members  

---

## 1. Core Operating Principles

1. **Academic Database Standard**: Treat this project as a rigorous academic DBMS project, not merely as a software application.
2. **Phase Authorization**: Work **only** on the currently authorized phase. Never jump ahead or automatically proceed to another major phase.
3. **Architecture Stability**: Never silently change the architecture or global identifier schemes.
4. **Data Authenticity**: Never fabricate factual GRAMMY data. All factual award information must originate from official Recording Academy sources or verified open datasets.
5. **Licensing Rigor**: Never assume a dataset is licensed merely because it is publicly accessible. Maintain complete provenance logs (Source, URL, dataset name, license, attribution, limitations, usage status).
6. **Identifier Consistency**: Maintain deterministic universal identifiers across all five databases (`CEREMONY_{NNN}`, `CAT_{SLUG}`, `NOM_{...}`, `WRK_{...}`, `CRT_{...}`, `LBL_{...}`, `VEN_{...}`).
7. **Fact vs. Metric Distinction**: Clearly distinguish primary source facts from calculated or derived statistical aggregates.
8. **Zero Secret Exposure**: Never expose credentials, passwords, or connection strings in code or version control. Use `.env` with strict `.gitignore` enforcement.
9. **Review Checkpoints**: Before major implementation changes, create a reviewable artifact. Stop at every approval checkpoint and wait for explicit human review.
10. **Numerical Quotas**:
    - Every database must contain at least 10 collections (50 total).
    - Every collection must contain at least 50 legitimate documents (2,500+ total).
    - Every document must contain at least 10 meaningful, typed domain attributes.

---

## 2. Phase Protocol

### At the Beginning of Every Phase:
- **State the Current Phase**: Name and phase number.
- **State Its Objective**: Academic and technical goal.
- **State What You Are Allowed to Do**: Exact authorized actions.
- **State What You Are Not Allowed to Do**: Explicit boundaries.
- **State Expected Deliverables**: Files, schemas, tests, reports.

### At the End of Every Phase:
- **Report Completed Work**: Concrete actions taken.
- **Report Files/Artifacts Created**: Clickable file links.
- **Report Unresolved Issues**: Open questions and blockers.
- **Report Risks**: Potential threats and mitigation steps.
- **Report What Remains**: Upcoming milestones.
- **STOP and Wait for Approval**: Await explicit user authorization.
