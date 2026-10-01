# Data-Source Research & Licensing Verification Plan

## 1. Academic Data Integrity Policy

To uphold absolute academic rigor and factual authenticity, this project operates under three foundational data rules:

1. **Zero Data Fabrication**: We strictly prohibit the generation or synthesis of artificial mock data. All records must reflect authentic historical facts of the Recording Academy.
2. **Explicit Provenance Logging**: Every record ingested into the databases must be traceable to a documented primary or secondary public dataset.
3. **Strict Licensing Verification**: No dataset will be integrated into the processing pipeline without explicit verification of open license compatibility (CC0, CC BY 4.0, Public Domain). Any ambiguous license is automatically flagged for review.

---

## 2. Research Plan & Target Sources

### 2.1 Primary Source: Official Recording Academy Archives (`grammy.com`)
- **Domain**: Official Grammy history, complete ceremony listings (1st through 67th awards), definitive nominee and winner rosters, official category rulebooks, and press announcements.
- **Access Protocol**: Public web extraction adhering to robots.txt, rate limited to 2 requests per second with custom user-agent identification.
- **License / Permissions**: Public factual domain. In copyright law (e.g., Feist Publications v. Rural Telephone Service), factual names, historical dates, award winners, and category listings are non-copyrightable facts. Descriptive excerpts are used under academic fair use.

### 2.2 Secondary Source: Verified Open Datasets (Kaggle)
- **Dataset Name**: "The Grammy Awards" (Historical compilation from 1958 to present).
- **Target Verification**: Must verify that the specific dataset version is released under **Creative Commons Zero (CC0: Public Domain)** or **Creative Commons Attribution 4.0 (CC BY 4.0)**.
- **Coverage**: Primary award winners, nominees, ceremony years, and category strings.

### 2.3 Tertiary Source: MusicBrainz Open Database (`musicbrainz.org`)
- **Domain**: Canonical entity metadata for musical creators: legal names, stage names, MusicBrainz Artist GIDs (`MBID`), band membership genealogies, release dates, track lengths, ISRC codes, and record label imprints.
- **License**: **CC0 1.0 Universal (Public Domain)** for core relational metadata tables.
- **Compatibility**: 100% compatible with academic database research.

### 2.4 Quaternary Source: Nielsen Ratings & Broadcast Historical Records
- **Domain**: Telecast viewership figures, household ratings, demographic shares, and venue attendance records.
- **License**: Factual historical metrics reported in public domain press archives (Variety, Billboard, Nielsen public bulletins).

---

## 3. Seven-Point Licensing Verification Rubric

Every candidate dataset evaluated during Phase 3 must be documented using the following formal rubric:

```markdown
### Verification Record: [Dataset Name]
1. **Source Name**: [Publishing organization or platform]
2. **Source URL**: [Direct URL to dataset or API endpoint]
3. **Dataset Name & Version**: [Exact title, release year, version]
4. **License Type**: [CC0, CC BY 4.0, CC BY-NC 4.0, Open Data Commons, Public Domain]
5. **Attribution Requirements**: [Required citation text or author acknowledgement]
6. **Academic Compatibility Assessment**: [Detailed evaluation of compatibility with university coursework]
7. **Supported Collections & Data Scope**: [List of collections populated by this source]
- **Audit Decision**: [APPROVED / QUARANTINED / REJECTED]
- **Audited By**: [Member Name and Date]
```

---

## 4. Initial Audit Log of Candidate Sources

### Source 1: MusicBrainz Open Database
- **Source Name**: MetaBrainz Foundation
- **Source URL**: `https://musicbrainz.org/doc/MusicBrainz_Database`
- **Dataset Name & Version**: MusicBrainz Core Database Dump (Latest)
- **License Type**: **CC0 1.0 Universal (Public Domain)**
- **Attribution Requirements**: None legally required under CC0; academic citation provided in project bibliography.
- **Academic Compatibility Assessment**: Fully compatible. Unrestricted non-commercial academic research use.
- **Supported Collections**:
  - `grammy_creators_db`: `artists`, `producers`, `audio_engineers`, `songwriters_composers`, `musical_groups`, `group_memberships`, `record_labels`.
  - `grammy_nominations_db`: `nominated_works`.
- **Audit Decision**: **APPROVED**

### Source 2: Official Recording Academy Award Database
- **Source Name**: Recording Academy (National Academy of Recording Arts and Sciences)
- **Source URL**: `https://www.grammy.com/awards`
- **Dataset Name & Version**: Official Grammy Awards Archive (1959–2025)
- **License Type**: Public Domain Historical Facts / Educational Fair Use
- **Attribution Requirements**: "Data compiled from official Recording Academy historical archives (grammy.com)."
- **Academic Compatibility Assessment**: Fully compatible. Factual compilations used exclusively for non-profit university education.
- **Supported Collections**:
  - `grammy_history_db`: `ceremonies`, `venues`, `ceremony_hosts`, `historic_milestones`, `lifetime_achievement_honors`.
  - `grammy_categories_db`: `award_fields`, `award_categories`, `category_lineage`, `eligibility_rules`, `discontinued_categories`.
  - `grammy_nominations_db`: `nomination_entries`, `nomination_credits`.
  - `grammy_winners_db`: `winner_records`, `big_four_sweeps`, `record_breakers`.
- **Audit Decision**: **APPROVED**

### Source 3: Kaggle - "The Grammy Awards" (Robyn Ritchie)
- **Source Name**: Kaggle Community Contributor (Robyn Ritchie)
- **Source URL**: `https://www.kaggle.com/datasets/unanimad/grammy-awards`
- **Dataset Name & Version**: Grammy Awards Dataset (1958–Present)
- **License Type**: **CC0: Public Domain**
- **Attribution Requirements**: Voluntary academic citation of contributor.
- **Academic Compatibility Assessment**: Compatible. Verified CC0 public domain license on dataset card.
- **Supported Collections**: Cross-validation benchmark for `nomination_entries` and `winner_records`.
- **Audit Decision**: **APPROVED**
