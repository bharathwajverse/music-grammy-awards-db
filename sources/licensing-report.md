# Formal Licensing Audit & Verification Report

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 3 — Source and License Verification  
> **Document**: Intellectual Property, Copyright Analysis, License Verification & Collection Mapping  
> **Status**: Completed  
> **Author**: Legal Compliance & Database Architecture Team  
> **Version Control**: Git / GitHub (`bharathwajverse/music-grammy-awards-db`)  

---

## 1. Executive Summary & Legal Framework

This report provides the exhaustive legal and licensing audit for all candidate data sources identified during Phase 2. Every candidate source has been audited against relevant copyright jurisprudence, database directives, open data licenses, and university academic fair-use guidelines.

### Guiding Legal Precedents & Standards:
1. **Factual Compilations (*Feist Publications, Inc. v. Rural Telephone Service Co.*, 499 U.S. 340 (1991))**:
   Under United States copyright law, raw historical facts, names, dates, award titles, and ceremony locations are not copyrightable subject matter. While creative selection and arrangement may receive thin copyright protection, factual data points themselves exist in the public domain.
2. **Academic Fair Use (17 U.S.C. § 107)**:
   The ingestion, querying, and structural demonstration of historical award data within an accredited non-profit higher education database curriculum constitutes transformative academic research with zero commercial market impairment.
3. **Open Data Standard (Creative Commons & Open Data Commons)**:
   Sources licensed under CC0, CC BY 4.0, or CC BY-NC 4.0 are honored strictly according to their license terms, ensuring full attribution where required and enforcing non-commercial boundaries.
4. **Zero Assumed Permission Policy**:
   No dataset is presumed free simply because it is accessible via the web or hosted on Kaggle. Repositories without explicit licenses are quarantined as `NEEDS_REVIEW`.

---

## 2. Audit Decision Classifications

Every discovered source receives one of four formal determinations:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                             AUDIT DECISION CLASSIFICATIONS                             │
├────────────────────────────┬───────────────────────────────────────────────────────────┤
│ Determination              │ Operational Rule in System                                │
├────────────────────────────┼───────────────────────────────────────────────────────────┤
│ APPROVED                   │ Fully certified for database ingestion; permissive license│
│                            │ (e.g., CC0, Public Domain) with no attribution mandate.   │
├────────────────────────────┼───────────────────────────────────────────────────────────┤
│ APPROVED_WITH_ATTRIBUTION  │ Certified for academic ingestion; requires mandatory      │
│                            │ citation and provenance logging in system documentation.  │
├────────────────────────────┼───────────────────────────────────────────────────────────┤
│ NEEDS_REVIEW               │ Quarantined. Lacks explicit license or has ambiguous terms.│
│                            │ Excluded from production pipeline until audit resolution. │
├────────────────────────────┼───────────────────────────────────────────────────────────┤
│ NOT_APPROVED               │ Rejected. Restrictive proprietary terms, commercial paywall│
│                            │ or legal prohibition against academic redistribution.     │
└────────────────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Source-by-Source Legal Audits

### 3.1. Source SRC-01: Official Recording Academy Award Database
- **Source Name**: The Recording Academy (National Academy of Recording Arts and Sciences)
- **URL**: `https://www.grammy.com/awards`
- **Location of Terms / License**: Website Terms of Service (`https://www.recordingacademy.com/terms-of-service`) & US Copyright Compendium.
- **Exact License / Legal Basis**: Public Domain Historical Facts (*Feist* doctrine) / Educational Fair Use (17 U.S.C. § 107).
- **Mandatory Attribution Requirements**:
  > *"Historical GRAMMY award facts and ceremony records compiled from official Recording Academy archives (grammy.com)."*
- **Academic Compatibility**: **Fully Compatible**. Educational database modeling represents core fair use.
- **Contractual & Legal Restrictions**:
  - Prohibits commercial redistribution and commercial automated scraping for competitive products.
  - The trademark "GRAMMY®" and official award statuette imagery cannot be used for commercial endorsement.
- **Technical & Domain Limitations**:
  - No direct bulk download button.
  - Craft credits (recording engineers, mastering engineers) are occasionally presented in composite text strings rather than normalized tables.
- **Audit Decision**: **`APPROVED_WITH_ATTRIBUTION`**

---

### 3.2. Source SRC-02: Official Recording Academy Rules & Voting Guidelines
- **Source Name**: Recording Academy Governance & Awards Department
- **URL**: `https://www.grammy.com/rules-voting-process`
- **Location of Terms / License**: Awards Rules & Guidelines Annual Documentation.
- **Exact License / Legal Basis**: Regulatory Rule Specifications / Educational Fair Use (17 U.S.C. § 107).
- **Mandatory Attribution Requirements**:
  > *"Award category eligibility, voting procedures, and craft credit quotas sourced from official Recording Academy Award Rules & Guidelines."*
- **Academic Compatibility**: **Fully Compatible**.
- **Contractual & Legal Restrictions**:
  - Proprietary trade secrets (individual member ballots, vote counts, confidential committee deliberations) are never published and must not be simulated as factual.
- **Technical & Domain Limitations**:
  - Historical rule adjustments prior to the 50th ceremony must be verified against retrospective literature.
- **Audit Decision**: **`APPROVED_WITH_ATTRIBUTION`**

---

### 3.3. Source SRC-03: MusicBrainz Core Database
- **Source Name**: MetaBrainz Foundation
- **URL**: `https://musicbrainz.org` (Data Licensing Documentation: `https://musicbrainz.org/doc/MusicBrainz_Database/Download`)
- **Location of Terms / License**: Legal notices located at `/doc/About/Data_License`.
- **Exact License / Legal Basis**: **Creative Commons CC0 1.0 Universal (Public Domain Dedication)** for all Core Data (artists, releases, release groups, recordings, works, labels, and relationships).
- **Mandatory Attribution Requirements**:
  - CC0 waives all attribution rights worldwide.
  - Academic Best Practice Citation: *"Metadata provided by MusicBrainz (MetaBrainz Foundation), dedicated to the public domain under CC0 1.0."*
- **Academic Compatibility**: **Fully Compatible**. Unrestricted global academic research use.
- **Contractual & Legal Restrictions**:
  - Unauthenticated live REST API requests must not exceed 1 request per second and must supply a unique, meaningful `User-Agent`. Bulk operations must utilize static database dumps.
- **Technical & Domain Limitations**:
  - MusicBrainz tracks musical discographies, not GRAMMY voting tallies.
- **Audit Decision**: **`APPROVED`**

---

### 3.4. Source SRC-04: Wikidata Knowledge Graph
- **Source Name**: Wikimedia Foundation
- **URL**: `https://www.wikidata.org` (Query Service: `https://query.wikidata.org`)
- **Location of Terms / License**: Site footer and terms: `https://www.wikidata.org/wiki/Wikidata:Main_Page` under "Licensing".
- **Exact License / Legal Basis**: **Creative Commons CC0 1.0 Universal Public Domain Dedication**.
- **Mandatory Attribution Requirements**:
  - No legal attribution required under CC0. Citation maintained in project source registry.
- **Academic Compatibility**: **Fully Compatible**. Unrestricted.
- **Contractual & Legal Restrictions**:
  - SPARQL endpoint enforce a 60-second execution timeout; bulk graph extractions should utilize filtered JSON/TSV dumps.
- **Technical & Domain Limitations**:
  - Crowd-sourced entries require cross-verification against official Academy archives for edge-case award categories.
- **Audit Decision**: **`APPROVED`**

---

### 3.5. Source SRC-05: Kaggle — "The Grammy Awards" (Robyn Ritchie / unanimad)
- **Source Name**: Kaggle Community Contributor (Robyn Ritchie / `unanimad`)
- **URL**: `https://www.kaggle.com/datasets/unanimad/grammy-awards`
- **Location of Terms / License**: Dataset Overview sidebar under "License".
- **Exact License / Legal Basis**: **CC0: Public Domain** (Explicitly chosen by dataset author upon upload).
- **Mandatory Attribution Requirements**:
  - None legally mandated. Attribution recorded: *"Grammy Awards dataset compiled by Robyn Ritchie on Kaggle, released under CC0."*
- **Academic Compatibility**: **Fully Compatible**.
- **Contractual & Legal Restrictions**: None.
- **Technical & Domain Limitations**:
  - Coverage ends at the 61st Annual GRAMMY Awards (2019). Lacks 2020–2025 ceremonies.
- **Audit Decision**: **`APPROVED`**

---

### 3.6. Source SRC-06: Kaggle — "Grammy Award Nominees and Winners, 1958-2024" (KenmoreToast)
- **Source Name**: Kaggle Contributor (KenmoreToast)
- **URL**: `https://www.kaggle.com/datasets/unanimad/grammy-awards` / `kenmoretoast/grammy-award-nominees-and-winners`
- **Location of Terms / License**: Dataset Metadata Card under "License".
- **Exact License / Legal Basis**: **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.
- **Mandatory Attribution Requirements**:
  > *"Grammy Award Nominees and Winners (1958-2024) dataset compiled by KenmoreToast on Kaggle, used under CC BY-NC 4.0."*
- **Academic Compatibility**: **Fully Compatible for Academic / Educational Use**.
- **Contractual & Legal Restrictions**:
  - **Non-Commercial Restriction**: This dataset can NEVER be packaged into a commercial SaaS, monetized API, or commercial product. Since this project is an academic university DBMS coursework project, CC BY-NC 4.0 is 100% compliant.
- **Technical & Domain Limitations**:
  - Composite credit strings combine artists and producers in freeform text requiring regex tokenization.
- **Audit Decision**: **`APPROVED_WITH_ATTRIBUTION`**

---

### 3.7. Source SRC-07: Kaggle — "Grammy Awards 2025" (Iskander Lou)
- **Source Name**: Kaggle Contributor (Iskander Lou)
- **URL**: `https://www.kaggle.com/datasets/iskanderlou/grammy-awards-2025`
- **Location of Terms / License**: Kaggle Dataset Card "Metadata" $\rightarrow$ "License".
- **Exact License / Legal Basis**: **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
- **Mandatory Attribution Requirements**:
  > *"Grammy Awards 2025 dataset compiled by Iskander Lou on Kaggle, licensed under CC BY 4.0."*
- **Academic Compatibility**: **Fully Compatible**.
- **Contractual & Legal Restrictions**:
  - Requires clear attribution, link to the license, and indication of changes made.
- **Technical & Domain Limitations**:
  - Covers only the 67th Annual GRAMMY Awards (2025).
- **Audit Decision**: **`APPROVED_WITH_ATTRIBUTION`**

---

### 3.8. Source SRC-08: Nielsen Media Research / Historical Broadcaster Archives
- **Source Name**: Nielsen Media Research / Historical Variety Broadcast Archives
- **URL**: `https://www.nielsen.com` / `https://www.variety.com`
- **Location of Terms / License**: Historical Press Announcements & Public Television Ratings Records.
- **Exact License / Legal Basis**: Factual Television Historical Ratings / Educational Fair Use (17 U.S.C. § 107).
- **Mandatory Attribution Requirements**:
  > *"Historical television viewership metrics and Nielsen ratings compiled from Nielsen Media Research public press releases and broadcaster logs."*
- **Academic Compatibility**: **Fully Compatible**.
- **Contractual & Legal Restrictions**:
  - Real-time commercial Nielsen streaming telemetry is proprietary; historical summary facts are public record.
- **Technical & Domain Limitations**:
  - Pre-1970 broadcasts lack fine-grained demographic cohort metrics (18–49 age bracket).
- **Audit Decision**: **`APPROVED_WITH_ATTRIBUTION`**

---

### 3.9. Source SRC-09: GitHub — `reisanar/datasets/grammyDB.csv`
- **Source Name**: GitHub Repository `reisanar/datasets`
- **URL**: `https://raw.githubusercontent.com/reisanar/datasets/master/grammyDB.csv`
- **Location of Terms / License**: Inspected GitHub repository root: `https://github.com/reisanar/datasets`.
- **Exact License / Legal Basis**: **NO LICENSE FILE FOUND IN REPOSITORY**.
- **Legal Assessment**: Under GitHub Terms of Service and standard copyright law, the absence of an open source license (such as MIT, Apache, or CC) means the author retains full exclusive copyright. While the repository is publicly accessible, public visibility does not confer redistribution rights.
- **Attribution Requirements**: Cites author `reisanar`.
- **Academic Compatibility**: Ambiguous. Educational fair use may apply, but violates the project's strict open-data verification mandate.
- **Audit Decision**: **`NEEDS_REVIEW`**  
  > [!WARNING]
  > **Quarantine Order**: `reisanar/datasets/grammyDB.csv` is quarantined and barred from production ingestion. Its historical rows are fully superseded by the verified CC0 dataset `SRC-05` (`unanimad/grammy-awards`) and primary source `SRC-01`.

---

### 3.10. Source SRC-10: GRAMMY System Analytical Engine (Internal Computations)
- **Source Name**: GRAMMY Awards Information & Analytics System Engineering Team
- **URL**: `g:/Projects/grammy-advanced-dbms/scripts/`
- **Location of Terms / License**: Root repository [`LICENSE`](../../LICENSE) (MIT License).
- **Exact License / Legal Basis**: **MIT License / Original Coursework Synthesis**.
- **Mandatory Attribution Requirements**: System documentation attribution.
- **Academic Compatibility**: **Fully Compatible**. Author-owned code and algorithmic transformations.
- **Audit Decision**: **`APPROVED`**

---

## 4. Complete Source-to-Collection Mapping (All 50 Collections)

The following master mapping connects every verified data source to each of the 50 collections across the five distributed databases:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        MASTER SOURCE-TO-COLLECTION MAPPING                             │
├───────────────────────┬──────────────────────────────┬──────────────────┬──────────────┤
│ Database Name         │ Collection Name              │ Supporting Source│ Audit Status │
├───────────────────────┼──────────────────────────────┼──────────────────┼──────────────┤
│ grammy_history_db     │ ceremonies                   │ SRC-01, SRC-05   │ APPROVED     │
│ grammy_history_db     │ venues                       │ SRC-01, SRC-04   │ APPROVED     │
│ grammy_history_db     │ telecast_broadcasters        │ SRC-08           │ APPR_W_ATTR  │
│ grammy_history_db     │ viewership_ratings           │ SRC-08           │ APPR_W_ATTR  │
│ grammy_history_db     │ ceremony_hosts               │ SRC-01, SRC-08   │ APPROVED     │
│ grammy_history_db     │ historic_milestones          │ SRC-01, SRC-04   │ APPROVED     │
│ grammy_history_db     │ timeline_historical_eras     │ SRC-10, SRC-01   │ APPROVED     │
│ grammy_history_db     │ academy_leadership           │ SRC-01, SRC-10   │ APPR_W_ATTR  │
│ grammy_history_db     │ press_media_accreditations   │ SRC-08, SRC-01   │ APPR_W_ATTR  │
│ grammy_history_db     │ lifetime_achievement_honors  │ SRC-01, SRC-04   │ APPROVED     │
├───────────────────────┼──────────────────────────────┼──────────────────┼──────────────┤
│ grammy_categories_db  │ award_fields                 │ SRC-01, SRC-02   │ APPROVED     │
│ grammy_categories_db  │ award_categories             │ SRC-01, SRC-07   │ APPROVED     │
│ grammy_categories_db  │ category_lineage             │ SRC-01, SRC-02   │ APPROVED     │
│ grammy_categories_db  │ eligibility_rules            │ SRC-02           │ APPR_W_ATTR  │
│ grammy_categories_db  │ voting_procedures            │ SRC-02           │ APPR_W_ATTR  │
│ grammy_categories_db  │ category_quotas_limits       │ SRC-02, SRC-10   │ APPROVED     │
│ grammy_categories_db  │ craft_credit_definitions     │ SRC-02           │ APPR_W_ATTR  │
│ grammy_categories_db  │ discontinued_categories      │ SRC-01, SRC-02   │ APPROVED     │
│ grammy_categories_db  │ merged_split_history         │ SRC-01, SRC-10   │ APPROVED     │
│ grammy_categories_db  │ special_merit_categories     │ SRC-01, SRC-02   │ APPR_W_ATTR  │
├───────────────────────┼──────────────────────────────┼──────────────────┼──────────────┤
│ grammy_nominations_db │ nomination_entries           │ SRC-01, SRC-06   │ APPROVED     │
│ grammy_nominations_db │ nominated_works              │ SRC-01, SRC-03   │ APPROVED     │
│ grammy_nominations_db │ nomination_credits           │ SRC-01, SRC-03   │ APPROVED     │
│ grammy_nominations_db │ submission_batches           │ SRC-02, SRC-10   │ APPROVED     │
│ grammy_nominations_db │ voter_screening_batches      │ SRC-02, SRC-10   │ APPROVED     │
│ grammy_nominations_db │ tied_nominations             │ SRC-01, SRC-06   │ APPROVED     │
│ grammy_nominations_db │ nomination_audit_logs        │ SRC-02, SRC-10   │ APPROVED     │
│ grammy_nominations_db │ genre_classifications        │ SRC-03, SRC-10   │ APPROVED     │
│ grammy_nominations_db │ first_time_nominees          │ SRC-06, SRC-10   │ APPROVED     │
│ grammy_nominations_db │ multi_nomination_packages    │ SRC-10           │ APPROVED     │
├───────────────────────┼──────────────────────────────┼──────────────────┼──────────────┤
│ grammy_winners_db     │ winner_records               │ SRC-01, SRC-06   │ APPROVED     │
│ grammy_winners_db     │ big_four_sweeps              │ SRC-01, SRC-10   │ APPROVED     │
│ grammy_winners_db     │ record_breakers              │ SRC-01, SRC-10   │ APPROVED     │
│ grammy_winners_db     │ acceptance_speeches          │ SRC-01, SRC-08   │ APPR_W_ATTR  │
│ grammy_winners_db     │ trophy_tracking              │ SRC-01, SRC-10   │ APPROVED     │
│ grammy_winners_db     │ consecutive_winners          │ SRC-06, SRC-10   │ APPROVED     │
│ grammy_winners_db     │ hall_of_fame_inductions      │ SRC-01, SRC-04   │ APPROVED     │
│ grammy_winners_db     │ posthumous_awards            │ SRC-01, SRC-04   │ APPROVED     │
│ grammy_winners_db     │ historic_win_benchmarks      │ SRC-10           │ APPROVED     │
│ grammy_winners_db     │ winner_press_releases        │ SRC-01, SRC-10   │ APPR_W_ATTR  │
├───────────────────────┼──────────────────────────────┼──────────────────┼──────────────┤
│ grammy_creators_db    │ artists                      │ SRC-03, SRC-04   │ APPROVED     │
│ grammy_creators_db    │ producers                    │ SRC-03           │ APPROVED     │
│ grammy_creators_db    │ audio_engineers              │ SRC-03           │ APPROVED     │
│ grammy_creators_db    │ songwriters_composers        │ SRC-03           │ APPROVED     │
│ grammy_creators_db    │ arrangers_conductors         │ SRC-03           │ APPROVED     │
│ grammy_creators_db    │ record_labels                │ SRC-03           │ APPROVED     │
│ grammy_creators_db    │ musical_groups               │ SRC-03, SRC-04   │ APPROVED     │
│ grammy_creators_db    │ group_memberships            │ SRC-03, SRC-04   │ APPROVED     │
│ grammy_creators_db    │ creator_collaborations       │ SRC-03, SRC-10   │ APPROVED     │
│ grammy_creators_db    │ creator_discographies        │ SRC-03           │ APPROVED     │
└───────────────────────┴──────────────────────────────┴──────────────────┴──────────────┘
```

---

## 5. Audit Conclusions & Phase 3 Sign-Off

1. **All 50 collections** are mapped to legally sound, academically compatible data sources.
2. **Zero copyright violations**: Quarantined `SRC-09` (`reisanar/datasets/grammyDB.csv`) as `NEEDS_REVIEW` due to lack of a license file, eliminating legal vulnerability by relying on verified CC0 sets (`SRC-05`) and official archives (`SRC-01`).
3. **Phase Boundary Preserved**: No MongoDB database was deployed, and no bulk data was imported during Phase 3.
4. **Next Step**: Awaiting user approval to proceed to Phase 4 (Enhanced Entity-Relationship Modeling).
