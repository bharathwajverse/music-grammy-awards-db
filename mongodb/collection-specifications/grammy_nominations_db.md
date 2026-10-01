# GRAMMY Nominations & Works Registry Database (`grammy_nominations_db`)

> **Phase**: Phase 11 — MongoDB Document Model Design
> **Database**: `grammy_nominations_db`
> **Allocated Collections**: 10 collections
> **Quota Status**: Verified $\ge 50$ documents and $\ge 10$ meaningful fields per collection

---

## Table of Contents

- [first_time_nominees](#first-time-nominees)
- [genre_classifications](#genre-classifications)
- [multi_nomination_packages](#multi-nomination-packages)
- [nominated_works](#nominated-works)
- [nomination_audit_logs](#nomination-audit-logs)
- [nomination_credits](#nomination-credits)
- [nomination_entries](#nomination-entries)
- [submission_batches](#submission-batches)
- [tied_nominations](#tied-nominations)
- [voter_screening_batches](#voter-screening-batches)

---

## 1. `first_time_nominees`

- **Collection Name**: `first_time_nominees`
- **Entity Represented**: `MaidenNominationEvent`
- **Purpose**: Breakthrough artists receiving maiden career nominations
- **Expected Feasibility Count**: 350+ breakout artist nominations
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`first_nom_id`).
- **Domain Key**: `first_nom_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `breakout_work_id`, `category_id`, `ceremony_id`, `creator_id`, `first_nom_id`, `nomination_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Longitudinal Analysis of Official Nomination Rolls
- **Data Classification Tier**: `DERIVED DATA`
- **Derived-Data Indicator**: `YES`
- **Derivation Logic**: Computed via aggregation pipeline across core source data during ETL.

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (first_nom_id) |
| `first_nom_id` | `string` | YES | Domain attribute: first_nom_id |
| `nomination_id` | `string` | YES | Domain attribute: nomination_id |
| `creator_id` | `string` | YES | Domain attribute: creator_id |
| `debut_ceremony_edition` | `int` | YES | Domain attribute: debut_ceremony_edition |
| `breakout_work_id` | `string` | YES | Domain attribute: breakout_work_id |
| `best_new_artist_nominated` | `bool` | YES | Domain attribute: best_new_artist_nominated |
| `age_at_debut_nomination` | `int` | YES | Domain attribute: age_at_debut_nomination |
| `prior_uncredited_appearances` | `int` | YES | Domain attribute: prior_uncredited_appearances |
| `commercial_breakout_tier` | `string` | YES | Domain attribute: commercial_breakout_tier |
| `career_inception_year` | `int` | YES | Domain attribute: career_inception_year |

### Document Structure Example
```json
{
  "_id": "FIRST_TIME_NOMINEES_001",
  "first_nom_id": "FIRST_TIME_NOMINEES_001",
  "nomination_id": "sample_nomination_id",
  "creator_id": "sample_creator_id",
  "debut_ceremony_edition": 1,
  "breakout_work_id": "sample_breakout_work_id",
  "best_new_artist_nominated": true,
  "age_at_debut_nomination": 1,
  "prior_uncredited_appearances": 1,
  "commercial_breakout_tier": "sample_commercial_breakout_tier",
  "career_inception_year": 1
}
```

---

## 2. `genre_classifications`

- **Collection Name**: `genre_classifications`
- **Entity Represented**: `WorkGenreClassification`
- **Purpose**: Multi-dimensional genre taxonomy tagging of works
- **Expected Feasibility Count**: 500+ genre mappings for works
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`classification_id`).
- **Domain Key**: `classification_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `assigned_field_id`, `classification_id`, `submitted_field_id`, `work_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: `secondary_genre_tags`

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz / Craft Committee Taxonomies
- **Data Classification Tier**: `SECONDARY OPEN DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (classification_id) |
| `classification_id` | `string` | YES | Domain attribute: classification_id |
| `work_id` | `string` | YES | Domain attribute: work_id |
| `submitted_field_id` | `string` | YES | Domain attribute: submitted_field_id |
| `assigned_field_id` | `string` | YES | Domain attribute: assigned_field_id |
| `primary_genre_tag` | `string` | YES | Domain attribute: primary_genre_tag |
| `secondary_genre_tags` | `array` | YES | Domain attribute: secondary_genre_tags |
| `screening_committee_consensus` | `string` | YES | Domain attribute: screening_committee_consensus |
| `contested_by_label_flag` | `bool` | YES | Domain attribute: contested_by_label_flag |
| `reclassification_justification` | `string` | YES | Domain attribute: reclassification_justification |
| `determination_date` | `string` | YES | Domain attribute: determination_date |

### Document Structure Example
```json
{
  "_id": "GENRE_CLASSIFICATIONS_001",
  "classification_id": "GENRE_CLASSIFICATIONS_001",
  "work_id": "sample_work_id",
  "submitted_field_id": "sample_submitted_field_id",
  "assigned_field_id": "sample_assigned_field_id",
  "primary_genre_tag": "sample_primary_genre_tag",
  "secondary_genre_tags": [
    "SAMPLE_ITEM"
  ],
  "screening_committee_consensus": "sample_screening_committee_consensus",
  "contested_by_label_flag": true,
  "reclassification_justification": "sample_reclassification_justification",
  "determination_date": "sample_determination_date"
}
```

---

## 3. `multi_nomination_packages`

- **Collection Name**: `multi_nomination_packages`
- **Entity Represented**: `MultiNominationPackage`
- **Purpose**: Works nominated across multiple categories in single year
- **Expected Feasibility Count**: 250+ multi-nominated works
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`package_id`).
- **Domain Key**: `package_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `ceremony_id`, `creator_id`, `package_id`, `primary_artist_id`, `work_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: `nominated_work_ids`

### Provenance & Data Tier
- **Source Provenance**: Derived Cross-Category Aggregations
- **Data Classification Tier**: `DERIVED DATA`
- **Derived-Data Indicator**: `YES`
- **Derivation Logic**: Computed via aggregation pipeline across core source data during ETL.

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (package_id) |
| `package_id` | `string` | YES | Domain attribute: package_id |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `creator_id` | `string` | YES | Domain attribute: creator_id |
| `total_nominations_count` | `int` | YES | Domain attribute: total_nominations_count |
| `general_field_nominations_count` | `int` | YES | Domain attribute: general_field_nominations_count |
| `genre_field_nominations_count` | `int` | YES | Domain attribute: genre_field_nominations_count |
| `leading_nominee_rank` | `int` | YES | Domain attribute: leading_nominee_rank |
| `nominated_work_ids` | `array` | YES | Domain attribute: nominated_work_ids |
| `public_announcement_tier` | `string` | YES | Domain attribute: public_announcement_tier |
| `ceremony_year` | `int` | YES | Domain attribute: ceremony_year |

### Document Structure Example
```json
{
  "_id": "MULTI_NOMINATION_PACKAGES_001",
  "package_id": "MULTI_NOMINATION_PACKAGES_001",
  "ceremony_id": "sample_ceremony_id",
  "creator_id": "sample_creator_id",
  "total_nominations_count": 1,
  "general_field_nominations_count": 1,
  "genre_field_nominations_count": 1,
  "leading_nominee_rank": 1,
  "nominated_work_ids": [
    "SAMPLE_ITEM"
  ],
  "public_announcement_tier": "sample_public_announcement_tier",
  "ceremony_year": 1
}
```

---

## 4. `nominated_works`

- **Collection Name**: `nominated_works`
- **Entity Represented**: `NominatedMusicalWork`
- **Purpose**: Creative musical works nominated for awards
- **Expected Feasibility Count**: 15000+ musical works
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`work_id`).
- **Domain Key**: `work_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `primary_label_id`, `primary_record_label_id`, `work_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: `record_label`
- **Arrays**: `genres`

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz / Recording Academy
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (14 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (work_id) |
| `work_id` | `string` | YES | Domain attribute: work_id |
| `work_type` | `string` | YES | Domain attribute: work_type |
| `work_title` | `string` | YES | Domain attribute: work_title |
| `commercial_release_date` | `string` | YES | Domain attribute: commercial_release_date |
| `primary_label_id` | `string` | YES | Domain attribute: primary_label_id |
| `isrc_code` | `string` | YES | Domain attribute: isrc_code |
| `upc_barcode` | `string` | YES | Domain attribute: upc_barcode |
| `duration_total_seconds` | `int` | YES | Domain attribute: duration_total_seconds |
| `track_count` | `int` | YES | Domain attribute: track_count |
| `parental_advisory_flag` | `bool` | YES | Domain attribute: parental_advisory_flag |
| `language_iso_code` | `string` | YES | Domain attribute: language_iso_code |
| `record_label` | `object` | NO | Embedded record label imprint |
| `genres` | `array` | NO | Embedded scalar genre tags |

### Document Structure Example
```json
{
  "_id": "NOMINATED_WORKS_001",
  "work_id": "NOMINATED_WORKS_001",
  "work_type": "sample_work_type",
  "work_title": "sample_work_title",
  "commercial_release_date": "sample_commercial_release_date",
  "primary_label_id": "sample_primary_label_id",
  "isrc_code": "sample_isrc_code",
  "upc_barcode": "sample_upc_barcode",
  "duration_total_seconds": 1,
  "track_count": 1,
  "parental_advisory_flag": true,
  "language_iso_code": "sample_language_iso_code",
  "record_label": {
    "sample_sub_prop": "value"
  },
  "genres": [
    "SAMPLE_ITEM"
  ]
}
```

---

## 5. `nomination_audit_logs`

- **Collection Name**: `nomination_audit_logs`
- **Entity Represented**: `BallotAuditLogRecord`
- **Purpose**: Independent accounting firm ballot tabulations
- **Expected Feasibility Count**: 67+ ceremony audit log records
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`audit_id`).
- **Domain Key**: `audit_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `audit_id`, `auditing_firm_id`, `ceremony_id`, `nomination_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Deloitte / PwC Audit Certification Reports
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (audit_id) |
| `audit_id` | `string` | YES | Domain attribute: audit_id |
| `nomination_id` | `string` | YES | Domain attribute: nomination_id |
| `auditing_firm_id` | `string` | YES | Domain attribute: auditing_firm_id |
| `lead_auditor_name` | `string` | YES | Domain attribute: lead_auditor_name |
| `audit_timestamp` | `string` | YES | Domain attribute: audit_timestamp |
| `digital_signature_hash` | `string` | YES | Domain attribute: digital_signature_hash |
| `tabulation_vault_partition` | `string` | YES | Domain attribute: tabulation_vault_partition |
| `discrepancy_check_passed` | `bool` | YES | Domain attribute: discrepancy_check_passed |
| `recount_required_flag` | `bool` | YES | Domain attribute: recount_required_flag |
| `compliance_certificate_code` | `string` | YES | Domain attribute: compliance_certificate_code |

### Document Structure Example
```json
{
  "_id": "NOMINATION_AUDIT_LOGS_001",
  "audit_id": "NOMINATION_AUDIT_LOGS_001",
  "nomination_id": "sample_nomination_id",
  "auditing_firm_id": "sample_auditing_firm_id",
  "lead_auditor_name": "sample_lead_auditor_name",
  "audit_timestamp": "sample_audit_timestamp",
  "digital_signature_hash": "sample_digital_signature_hash",
  "tabulation_vault_partition": "sample_tabulation_vault_partition",
  "discrepancy_check_passed": true,
  "recount_required_flag": true,
  "compliance_certificate_code": "sample_compliance_certificate_code"
}
```

---

## 6. `nomination_credits`

- **Collection Name**: `nomination_credits`
- **Entity Represented**: `NominationCreditRoster`
- **Purpose**: Disaggregated creative contributors for each nomination
- **Expected Feasibility Count**: 40000+ credit links
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`credit_id`).
- **Domain Key**: `credit_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `creator_id`, `credit_id`, `nomination_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Nominee Credit Booklets
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (credit_id) |
| `credit_id` | `string` | YES | Domain attribute: credit_id |
| `nomination_id` | `string` | YES | Domain attribute: nomination_id |
| `creator_id` | `string` | YES | Domain attribute: creator_id |
| `credit_role` | `string` | YES | Domain attribute: credit_role |
| `credit_billing_rank` | `int` | YES | Domain attribute: credit_billing_rank |
| `work_contribution_summary` | `string` | YES | Domain attribute: work_contribution_summary |
| `contribution_percentage` | `double` | YES | Domain attribute: contribution_percentage |
| `is_lead_performer` | `bool` | YES | Domain attribute: is_lead_performer |
| `is_producer_credit` | `bool` | YES | Domain attribute: is_producer_credit |
| `academy_verified_status` | `bool` | YES | Domain attribute: academy_verified_status |

### Document Structure Example
```json
{
  "_id": "NOMINATION_CREDITS_001",
  "credit_id": "NOMINATION_CREDITS_001",
  "nomination_id": "sample_nomination_id",
  "creator_id": "sample_creator_id",
  "credit_role": "sample_credit_role",
  "credit_billing_rank": 1,
  "work_contribution_summary": "sample_work_contribution_summary",
  "contribution_percentage": 100.0,
  "is_lead_performer": true,
  "is_producer_credit": true,
  "academy_verified_status": true
}
```

---

## 7. `nomination_entries`

- **Collection Name**: `nomination_entries`
- **Entity Represented**: `NominationEntry`
- **Purpose**: Canonical official nomination ballots across all years
- **Expected Feasibility Count**: 25000+ historical nominations
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`nomination_id`).
- **Domain Key**: `nomination_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `category_id`, `ceremony_id`, `nomination_id`, `primary_artist_id`, `work_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: `credited_talent`

### Provenance & Data Tier
- **Source Provenance**: Official Recording Academy Nomination Rolls
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (13 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (nomination_id) |
| `nomination_id` | `string` | YES | Domain attribute: nomination_id |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `category_id` | `string` | YES | Domain attribute: category_id |
| `work_id` | `string` | YES | Domain attribute: work_id |
| `nomination_year` | `int` | YES | Domain attribute: nomination_year |
| `entry_billing_title` | `string` | YES | Domain attribute: entry_billing_title |
| `primary_artist_id` | `string` | YES | Domain attribute: primary_artist_id |
| `is_winner_flag` | `bool` | YES | Domain attribute: is_winner_flag |
| `ballot_slot_order` | `int` | YES | Domain attribute: ballot_slot_order |
| `auditor_validation_code` | `string` | YES | Domain attribute: auditor_validation_code |
| `created_timestamp` | `string` | YES | Domain attribute: created_timestamp |
| `credited_talent` | `array` | NO | Embedded array of credited personnel on nomination |

### Document Structure Example
```json
{
  "_id": "NOM_065_AOTY_01",
  "nomination_id": "NOM_065_AOTY_01",
  "ceremony_id": "CEREMONY_065",
  "category_id": "CAT_AOTY",
  "work_id": "WRK_RENAISSANCE_2022",
  "ballot_slot_order": 1,
  "is_winner": false,
  "submission_id": "SUB_065_1042",
  "is_tied_nomination": false,
  "screening_passed": true,
  "credited_talent": [
    {
      "credit_id": "CRD_065_AOTY_01_01",
      "creator_id": "CRT_BEYONCE_001",
      "creator_name": "Beyonc\u00e9",
      "credit_role": "Lead Artist / Producer",
      "contribution_percentage": 85.0
    }
  ],
  "created_at": "2022-11-15T15:00:00Z"
}
```

---

## 8. `submission_batches`

- **Collection Name**: `submission_batches`
- **Entity Represented**: `IntakeSubmissionBatch`
- **Purpose**: Record label and member submission intake batches
- **Expected Feasibility Count**: 65+ intake batches
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`batch_id`).
- **Domain Key**: `batch_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `batch_id`, `ceremony_id`, `submitting_label_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Academy Awards Intake Logs
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (batch_id) |
| `batch_id` | `string` | YES | Domain attribute: batch_id |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `submitting_label_id` | `string` | YES | Domain attribute: submitting_label_id |
| `submission_timestamp` | `string` | YES | Domain attribute: submission_timestamp |
| `total_entries_count` | `int` | YES | Domain attribute: total_entries_count |
| `entry_fee_total_usd` | `double` | YES | Domain attribute: entry_fee_total_usd |
| `compliance_officer_name` | `string` | YES | Domain attribute: compliance_officer_name |
| `first_round_accepted_count` | `int` | YES | Domain attribute: first_round_accepted_count |
| `disqualified_entries_count` | `int` | YES | Domain attribute: disqualified_entries_count |
| `payment_reconciliation_hash` | `string` | YES | Domain attribute: payment_reconciliation_hash |

### Document Structure Example
```json
{
  "_id": "SUBMISSION_BATCHES_001",
  "batch_id": "SUBMISSION_BATCHES_001",
  "ceremony_id": "sample_ceremony_id",
  "submitting_label_id": "sample_submitting_label_id",
  "submission_timestamp": "sample_submission_timestamp",
  "total_entries_count": 1,
  "entry_fee_total_usd": 100.0,
  "compliance_officer_name": "sample_compliance_officer_name",
  "first_round_accepted_count": 1,
  "disqualified_entries_count": 1,
  "payment_reconciliation_hash": "sample_payment_reconciliation_hash"
}
```

---

## 9. `tied_nominations`

- **Collection Name**: `tied_nominations`
- **Entity Represented**: `TiedNominationEvent`
- **Purpose**: Ballot ties producing expanded nominee fields
- **Expected Feasibility Count**: 50+ historical tie events
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`tie_id`).
- **Domain Key**: `tie_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `category_id`, `ceremony_id`, `tie_id`, `tied_nominee_ids`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: `tied_nomination_ids`

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Official Ballot Announcements
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (tie_id) |
| `tie_id` | `string` | YES | Domain attribute: tie_id |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `category_id` | `string` | YES | Domain attribute: category_id |
| `tied_nomination_ids` | `array` | YES | Domain attribute: tied_nomination_ids |
| `tied_vote_count_audited` | `int` | YES | Domain attribute: tied_vote_count_audited |
| `ballot_auditor_token` | `string` | YES | Domain attribute: ballot_auditor_token |
| `board_tie_waiver_approved` | `bool` | YES | Domain attribute: board_tie_waiver_approved |
| `expanded_slate_size` | `int` | YES | Domain attribute: expanded_slate_size |
| `adjudication_timestamp` | `string` | YES | Domain attribute: adjudication_timestamp |
| `bylaw_clause_reference` | `string` | YES | Domain attribute: bylaw_clause_reference |

### Document Structure Example
```json
{
  "_id": "TIED_NOMINATIONS_001",
  "tie_id": "TIED_NOMINATIONS_001",
  "ceremony_id": "sample_ceremony_id",
  "category_id": "sample_category_id",
  "tied_nomination_ids": [
    "SAMPLE_ITEM"
  ],
  "tied_vote_count_audited": 1,
  "ballot_auditor_token": "sample_ballot_auditor_token",
  "board_tie_waiver_approved": true,
  "expanded_slate_size": 1,
  "adjudication_timestamp": "sample_adjudication_timestamp",
  "bylaw_clause_reference": "sample_bylaw_clause_reference"
}
```

---

## 10. `voter_screening_batches`

- **Collection Name**: `voter_screening_batches`
- **Entity Represented**: `ScreeningCommitteeSession`
- **Purpose**: Screening committee review sessions vetting entries
- **Expected Feasibility Count**: 60+ screening sessions
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`session_id`).
- **Domain Key**: `session_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `ceremony_id`, `field_id`, `panel_chair_creator_id`, `screening_batch_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Academy Screening Committee Logs
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (screening_batch_id) |
| `screening_batch_id` | `string` | YES | Domain attribute: screening_batch_id |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `field_id` | `string` | YES | Domain attribute: field_id |
| `panel_chair_creator_id` | `string` | YES | Domain attribute: panel_chair_creator_id |
| `session_start_timestamp` | `string` | YES | Domain attribute: session_start_timestamp |
| `session_end_timestamp` | `string` | YES | Domain attribute: session_end_timestamp |
| `works_screened_count` | `int` | YES | Domain attribute: works_screened_count |
| `disqualifications_ordered` | `int` | YES | Domain attribute: disqualifications_ordered |
| `quorum_certified` | `bool` | YES | Domain attribute: quorum_certified |
| `panel_confidentiality_hash` | `string` | YES | Domain attribute: panel_confidentiality_hash |

### Document Structure Example
```json
{
  "_id": "VOTER_SCREENING_BATCHES_001",
  "screening_batch_id": "sample_screening_batch_id",
  "ceremony_id": "sample_ceremony_id",
  "field_id": "sample_field_id",
  "panel_chair_creator_id": "sample_panel_chair_creator_id",
  "session_start_timestamp": "sample_session_start_timestamp",
  "session_end_timestamp": "sample_session_end_timestamp",
  "works_screened_count": 1,
  "disqualifications_ordered": 1,
  "quorum_certified": true,
  "panel_confidentiality_hash": "sample_panel_confidentiality_hash",
  "session_id": "VOTER_SCREENING_BATCHES_001"
}
```

---
