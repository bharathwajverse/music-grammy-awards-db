# Phase 2 — Data Source Research & Discovery

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 2 — Data Source Research  
> **Status**: Completed  
> **Author**: Research & Data Engineering Team  
> **Version Control**: Git / GitHub (`bharathwajverse/music-grammy-awards-db`)  

---

## 1. Executive Summary & Research Methodology

Phase 2 investigates, identifies, and categorizes candidate external data sources to support the complete historical, organizational, and technical modeling of the GRAMMY Awards (1959–Present).

In strict adherence to project instructions, all candidate sources are evaluated according to a three-tier hierarchy:
1. **Tier 1 — PRIMARY OFFICIAL SOURCE**: Official Recording Academy portals, official press bulletins, rules/eligibility guidelines, and television broadcast archives.
2. **Tier 2 — SECONDARY OPEN DATA**: Structured open knowledge graphs and collaborative music databases (MusicBrainz, Wikidata) with explicit machine-readable licenses (CC0, CC-BY).
3. **Tier 3 — SECONDARY OPEN DATA / AUDITED COMMUNITY SETS**: Curated data repositories (Kaggle, GitHub) where the underlying license has been individually verified rather than assumed.
4. **DERIVED DATA**: Analytical aggregations, longitudinal performance ratios, Big Four sweep flags, and credit allocations synthesized deterministically from primary facts via DBMS queries and ETL scripts.

---

## 2. Source Classification Taxonomy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          DATA SOURCE CLASSIFICATION TAXONOMY                           │
├──────────────────────────┬─────────────────────────────────────────────────────────────┤
│ Classification Category  │ Definition & System Usage                                   │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ PRIMARY OFFICIAL SOURCE  │ Authoritative, primary-party historical facts, rules, and   │
│                          │ official results published directly by The Recording Academy│
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ SECONDARY OPEN DATA      │ Publicly accessible, machine-readable datasets with explicit│
│                          │ open licenses (CC0, CC-BY, ODC) from trusted foundations.   │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ DERIVED DATA             │ Computed metrics, aggregations, ratios, and audit flags     │
│                          │ synthesized programmatically from primary source facts.     │
└──────────────────────────┴─────────────────────────────────────────────────────────────┘
```

---

## 3. Discovered Candidate Sources (Detailed Profiles)

### Source 1: Official Recording Academy Award Database
- **Classification**: `PRIMARY OFFICIAL SOURCE`
- **Source Name**: The Recording Academy (National Academy of Recording Arts and Sciences)
- **Exact URL**: `https://www.grammy.com/awards`
- **Dataset / Page Name**: Official GRAMMY Awards Search & Historical Archive
- **Type of Data**: Historical award ceremonies, official winners, official nominees, category titles, ceremony dates, billed artists, and nominated works.
- **Years Covered**: 1958 (1st Annual Awards) – 2025 (67th Annual Awards)
- **Approximate Record Availability**: 67 ceremonies, 550+ categories across time, 25,000+ historical nomination entries, 9,000+ winner records.
- **License**: Public Domain Historical Facts (*Feist Publications v. Rural Telephone Service Co.*, 499 U.S. 340 (1991)) / Educational Fair Use (17 U.S.C. § 107). Recording Academy website terms restrict commercial bulk scraping and trademark use.
- **Attribution Requirements**: "Data compiled from official Recording Academy historical archives (grammy.com)."
- **Academic-Use Compatibility**: Fully Compatible for non-profit academic database teaching and research.
- **Restrictions**: Commercial re-use prohibited; trademark "GRAMMY®" and official imagery cannot be utilized for commercial branding.
- **Limitations**: Historical web interface does not provide a bulk downloadable JSON/CSV; requires API/DOM extraction or cross-verification against open mirrors.
- **Supported Databases & Collections**:
  - `grammy_history_db`: `ceremonies`, `venues`, `historic_milestones`, `lifetime_achievement_honors`
  - `grammy_categories_db`: `award_fields`, `award_categories`, `category_lineage`, `discontinued_categories`
  - `grammy_nominations_db`: `nomination_entries`, `nominated_works`, `tied_nominations`
  - `grammy_winners_db`: `winner_records`, `big_four_sweeps`, `record_breakers`

---

### Source 2: Official Recording Academy Rulebook & Voting Guidelines
- **Classification**: `PRIMARY OFFICIAL SOURCE`
- **Source Name**: The Recording Academy Governance & Awards Department
- **Exact URL**: `https://www.grammy.com/rules-voting-process`
- **Dataset / Page Name**: Awards Rules & Guidelines / Voting Procedures (Annual Manuals)
- **Type of Data**: Procedural voting thresholds, submission rules, eligibility release windows, voting rounds, craft credit percentages (e.g., Album of the Year Producer threshold), and committee review protocols.
- **Years Covered**: Modern Era (2010–2025 editions, with historical retrospective clauses)
- **Approximate Record Availability**: Complete rule specifications for all 11 award fields and 94 active categories.
- **License**: Educational Fair Use / Factual Regulatory Specifications.
- **Attribution Requirements**: "Governance specifications sourced from official Recording Academy Award Rules & Voting Guidelines."
- **Academic-Use Compatibility**: Fully Compatible.
- **Restrictions**: Internal trade secrets and confidential member voting tallies (Deloitte balloting tabulations) are strictly confidential and unpublished.
- **Limitations**: Historical rule changes prior to 1990 must be pieced together from retrospective Academy announcements and musicological literature.
- **Supported Databases & Collections**:
  - `grammy_categories_db`: `eligibility_rules`, `voting_procedures`, `category_quotas_limits`, `craft_credit_definitions`, `special_merit_categories`
  - `grammy_nominations_db`: `submission_batches`, `voter_screening_batches`, `nomination_audit_logs`

---

### Source 3: MusicBrainz Open Music Knowledge Base
- **Classification**: `SECONDARY OPEN DATA`
- **Source Name**: MetaBrainz Foundation
- **Exact URL**: `https://musicbrainz.org` (Data Dumps: `https://musicbrainz.org/doc/MusicBrainz_Database/Download`)
- **Dataset / Page Name**: MusicBrainz Core Database Dump & MusicBrainz API
- **Type of Data**: Comprehensive discographies, artists (birth dates, nationalities, aliases), audio engineers, producers, songwriters, record labels, ISRC track codes, release groups, and album tracklists.
- **Years Covered**: 1900 – Present (global comprehensive coverage)
- **Approximate Record Availability**: 2.3+ million artists, 3.8+ million releases, 28+ million recordings, 100,000+ record labels.
- **License**: **CC0 1.0 Universal Public Domain Dedication** for Core Data (artists, releases, recordings, labels, relationships). Supplementary annotations and wiki documentation under CC BY-NC-SA 3.0.
- **Attribution Requirements**: CC0 requires no legal attribution, but MetaBrainz asks for academic acknowledgment: "Music metadata provided by MusicBrainz (MetaBrainz Foundation)."
- **Academic-Use Compatibility**: Fully Compatible. Unrestricted academic and non-commercial research use.
- **Restrictions**: Public REST API enforced at 1 request per second without authentication, requiring a descriptive `User-Agent` header.
- **Limitations**: Does not contain GRAMMY ceremony voting tallies or proprietary Recording Academy committee meeting notes.
- **Supported Databases & Collections**:
  - `grammy_creators_db`: `artists`, `producers`, `audio_engineers`, `songwriters_composers`, `arrangers_conductors`, `record_labels`, `musical_groups`, `group_memberships`, `creator_collaborations`, `creator_discographies`
  - `grammy_nominations_db`: `nominated_works`, `nomination_credits`

---

### Source 4: Wikidata Music Knowledge Graph
- **Classification**: `SECONDARY OPEN DATA`
- **Source Name**: Wikimedia Foundation
- **Exact URL**: `https://www.wikidata.org` (SPARQL Endpoint: `https://query.wikidata.org`)
- **Dataset / Page Name**: Wikidata Entity Graph (Entities: Q7191 "Grammy Award", Property P166 "award received", Property P1052 "Grammy Awards artist ID")
- **Type of Data**: Graph relations linking creators (QIDs) to award received (P166), ceremony editions, award years, winner status, birthplace coordinates, musical genres, and external identifier cross-walks (Spotify ID, MusicBrainz ID, Discogs ID).
- **Years Covered**: 1959 – 2025
- **Approximate Record Availability**: 100,000+ statements relating to Grammy nominations, wins, and participating artists.
- **License**: **CC0 1.0 Universal Public Domain Dedication** for 100% of structured data.
- **Attribution Requirements**: None legally mandated under CC0; academic citation to Wikidata recommended.
- **Academic-Use Compatibility**: Fully Compatible without conditions.
- **Restrictions**: SPARQL endpoint throttled at 60 seconds query timeout; batch querying requires paginated queries or RDF dump slicing.
- **Limitations**: Crowd-sourced; secondary craft credits (mastering engineers, assistant mixers) can have sparser coverage than primary billing artists.
- **Supported Databases & Collections**:
  - `grammy_creators_db`: `artists`, `musical_groups`, `group_memberships`
  - `grammy_winners_db`: `winner_records`, `big_four_sweeps`, `hall_of_fame_inductions`, `posthumous_awards`
  - `grammy_history_db`: `ceremonies`, `venues`, `ceremony_hosts`

---

### Source 5: Kaggle — "The Grammy Awards" (Robyn Ritchie / unanimad)
- **Classification**: `SECONDARY OPEN DATA`
- **Source Name**: Kaggle Community Contributor (Robyn Ritchie / `unanimad`)
- **Exact URL**: `https://www.kaggle.com/datasets/unanimad/grammy-awards`
- **Dataset / Page Name**: "The Grammy Awards" Dataset (`the_grammy_awards.csv`)
- **Type of Data**: Historical nominations and wins, ceremony numbers, years, categories, nominee titles, artists, and boolean winner flags.
- **Years Covered**: 1958 – 2019 (Historical baseline)
- **Approximate Record Availability**: 4,810 records across 61 ceremonies.
- **License**: **CC0: Public Domain** (explicitly declared on Kaggle dataset card).
- **Attribution Requirements**: CC0 Public Domain dedication; academic citation to dataset creator.
- **Academic-Use Compatibility**: Fully Compatible.
- **Restrictions**: None (Public Domain).
- **Limitations**: Dataset stops at the 61st Annual GRAMMY Awards (2019). Lacks modern ceremonies (2020–2025) and lacks disaggregated audio engineering credits.
- **Supported Databases & Collections**:
  - `grammy_history_db`: `ceremonies`
  - `grammy_categories_db`: `award_categories`
  - `grammy_nominations_db`: `nomination_entries`
  - `grammy_winners_db`: `winner_records`

---

### Source 6: Kaggle — "Grammy Award Nominees and Winners, 1958-2024" (KenmoreToast)
- **Classification**: `SECONDARY OPEN DATA`
- **Source Name**: Kaggle Contributor (KenmoreToast)
- **Exact URL**: `https://www.kaggle.com/datasets/unanimad/grammy-awards` / `kenmoretoast/grammy-award-nominees-and-winners`
- **Dataset / Page Name**: Grammy Award Nominees and Winners, 1958-2024
- **Type of Data**: Web-scraped historical records supplemented by Wikipedia articles; columns include ceremony, release year, category name, nominee work, artist name, and win indicator.
- **Years Covered**: 1958 – 2024 (66 ceremonies)
- **Approximate Record Availability**: 9,500+ nominee and winner rows.
- **License**: **Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**
- **Attribution Requirements**: "Data compiled and scraped by KenmoreToast from Recording Academy archives and Wikipedia, licensed under CC BY-NC 4.0."
- **Academic-Use Compatibility**: Fully Compatible for non-commercial academic research and university teaching.
- **Restrictions**: Commercial exploitation strictly prohibited; derivatives must adhere to non-commercial terms.
- **Limitations**: Raw table mixes credits into unstructured strings; requires regex parsing to disaggregate performers from producers.
- **Supported Databases & Collections**:
  - `grammy_nominations_db`: `nomination_entries`, `first_time_nominees`
  - `grammy_winners_db`: `winner_records`, `consecutive_winners`

---

### Source 7: Kaggle — "Grammy Awards 2025" (Iskander Lou)
- **Classification**: `SECONDARY OPEN DATA`
- **Source Name**: Kaggle Contributor (Iskander Lou)
- **Exact URL**: `https://www.kaggle.com/datasets/iskanderlou/grammy-awards-2025`
- **Dataset / Page Name**: Grammy Awards 2025 (`grammys_2025.csv`)
- **Type of Data**: 67th Annual GRAMMY Awards (2025) full nomination and winner entries, category slugs, works, and participating artists.
- **Years Covered**: 2024 / 2025 (67th Ceremony)
- **Approximate Record Availability**: 450+ rows covering all 94 categories for the 2025 edition.
- **License**: **Creative Commons Attribution 4.0 International (CC BY 4.0)**
- **Attribution Requirements**: "Grammy Awards 2025 dataset provided by Iskander Lou under CC BY 4.0."
- **Academic-Use Compatibility**: Fully Compatible.
- **Restrictions**: Attribution required upon redistribution.
- **Limitations**: Covers only the single 2025 ceremony edition.
- **Supported Databases & Collections**:
  - `grammy_history_db`: `ceremonies` (Edition 67)
  - `grammy_categories_db`: `award_categories` (Current state)
  - `grammy_nominations_db`: `nomination_entries`
  - `grammy_winners_db`: `winner_records`

---

### Source 8: Nielsen Media Research & Historical Telecast Archives
- **Classification**: `PRIMARY OFFICIAL SOURCE / HISTORICAL MEDIA LOGS`
- **Source Name**: Nielsen Media Research / Historical Broadcaster Archives (CBS & NBC Press Releases)
- **Exact URL**: `https://www.nielsen.com` / `https://www.variety.com` (Historical TV Ratings Archive)
- **Dataset / Page Name**: GRAMMY Awards Television Broadcast Viewership & Nielsen Ratings (1970–2024)
- **Type of Data**: Live telecast viewers (millions), household ratings, demographic 18-49 shares, air dates, runtimes, broadcast host names.
- **Years Covered**: 1970 – 2024
- **Approximate Record Availability**: 55 telecast broadcast event records.
- **License**: Public Historical Telecast Facts / Educational Fair Use.
- **Attribution Requirements**: "Television viewership and telecast statistics compiled from Nielsen Media Research historical telecast ratings."
- **Academic-Use Compatibility**: Fully Compatible for non-commercial educational study.
- **Restrictions**: Commercial syndication of real-time Nielsen feeds is proprietary; historical summary facts are public record.
- **Limitations**: Pre-1970 broadcast ratings have spotty demographic granularity.
- **Supported Databases & Collections**:
  - `grammy_history_db`: `telecast_broadcasters`, `viewership_ratings`, `ceremony_hosts`, `press_media_accreditations`

---

### Source 9: GitHub — `reisanar/datasets/grammyDB.csv` (Raw Ingest Archive)
- **Classification**: `SECONDARY OPEN DATA (NEEDS_REVIEW)`
- **Source Name**: GitHub User Repository (`reisanar/datasets`)
- **Exact URL**: `https://raw.githubusercontent.com/reisanar/datasets/master/grammyDB.csv`
- **Dataset / Page Name**: `grammyDB.csv`
- **Type of Data**: Tabular historical nomination and winner records (1958–2019).
- **Years Covered**: 1958 – 2019
- **Approximate Record Availability**: 4,810 records.
- **License**: **NEEDS_REVIEW** (No explicit LICENSE file present in the root of `reisanar/datasets` repository). Under default copyright laws, lack of license implies all rights reserved by the author.
- **Attribution Requirements**: Cites author `reisanar` on GitHub.
- **Academic-Use Compatibility**: Tentative Educational Fair Use, but fails strict open licensing verification.
- **Audit Decision**: Marked **`NEEDS_REVIEW`**; historical facts must be verified against verified CC0 datasets (`unanimad/grammy-awards`) or official `grammy.com` before production certification.
- **Supported Databases & Collections**: Reference benchmark only.

---

## 4. Derived Data Architecture

The system distinguishes primary source facts from derived analytical metrics:

| Derived Analytical Collection | Parent Source Collections | Derivation Methodology & Aggregation Logic |
| :--- | :--- | :--- |
| `big_four_sweeps` (`grammy_winners_db`) | `winner_records`, `award_categories` | Filter winners matching categories `CAT_AOTY`, `CAT_ROTY`, `CAT_SOTY`, `CAT_BNA` grouped by `ceremony_id` and `artist_id` having count = 4. |
| `record_breakers` (`grammy_winners_db`) | `winner_records`, `artists` | Multi-stage pipeline computing lifetime win counts, single-night victory counts, and historical rank ordering. |
| `consecutive_winners` (`grammy_winners_db`) | `winner_records`, `ceremonies` | Window function over consecutive `broadcast_year` partitioned by `category_id` and `artist_id`. |
| `category_quotas_limits` (`grammy_categories_db`)| `nomination_entries` | Aggregated count of nominations per ceremony-category to identify historical quota changes (5 $\rightarrow$ 8 $\rightarrow$ 10). |
| `creator_collaborations` (`grammy_creators_db`)| `nomination_credits` | Pairwise co-occurrence join on `nomination_id` linking collaborating creators across musical works. |

---

## 5. Next Phase Transition

Phase 2 discovery concludes that all 50 collections across the 5 databases are fully covered by authentic, verifiable data sources. Proceed to Phase 3 for detailed license audits and decision registration.
