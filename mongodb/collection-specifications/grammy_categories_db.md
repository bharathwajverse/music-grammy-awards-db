# GRAMMY Award Categories & Governance Database (`grammy_categories_db`)

> **Phase**: Phase 11 — MongoDB Document Model Design
> **Database**: `grammy_categories_db`
> **Allocated Collections**: 10 collections
> **Quota Status**: Verified $\ge 50$ documents and $\ge 10$ meaningful fields per collection

---

## Table of Contents

- [award_categories](#award-categories)
- [award_fields](#award-fields)
- [category_lineage](#category-lineage)
- [category_quotas_limits](#category-quotas-limits)
- [craft_credit_definitions](#craft-credit-definitions)
- [discontinued_categories](#discontinued-categories)
- [eligibility_rules](#eligibility-rules)
- [merged_split_history](#merged-split-history)
- [special_merit_categories](#special-merit-categories)
- [voting_procedures](#voting-procedures)

---

## 1. `award_categories`

- **Collection Name**: `award_categories`
- **Entity Represented**: `AwardCategory`
- **Purpose**: Specific competitive award categories across all eras
- **Expected Feasibility Count**: 550+ distinct historical categories
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`category_id`).
- **Domain Key**: `category_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `category_id`, `field_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: `award_field`, `eligibility_rules`
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Official Recording Academy Category Registry
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (14 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (category_id) |
| `category_id` | `string` | YES | Domain attribute: category_id |
| `field_id` | `string` | YES | Domain attribute: field_id |
| `official_category_name` | `string` | YES | Domain attribute: official_category_name |
| `standard_short_code` | `string` | YES | Domain attribute: standard_short_code |
| `inaugural_edition` | `int` | YES | Domain attribute: inaugural_edition |
| `is_general_field` | `bool` | YES | Domain attribute: is_general_field |
| `current_status` | `string` | YES | Domain attribute: current_status |
| `maximum_nominees_allowed` | `int` | YES | Domain attribute: maximum_nominees_allowed |
| `voting_tier_access` | `string` | YES | Domain attribute: voting_tier_access |
| `trophy_statuette_eligibility_rule` | `string` | YES | Domain attribute: trophy_statuette_eligibility_rule |
| `entry_fee_tier` | `string` | YES | Domain attribute: entry_fee_tier |
| `award_field` | `object` | NO | Embedded umbrella field taxonomy metadata |
| `eligibility_rules` | `object` | NO | Embedded category eligibility guidelines |

### Document Structure Example
```json
{
  "_id": "CAT_AOTY",
  "category_id": "CAT_AOTY",
  "category_name": "Album of the Year",
  "standard_short_code": "AOTY",
  "award_field": {
    "field_id": "FLD_GENERAL",
    "field_name": "General Field",
    "field_abbreviation": "GEN"
  },
  "eligibility_rules": {
    "min_total_playing_time_minutes": 15.0,
    "min_distinct_tracks": 5,
    "playing_time_percentage_new_recordings": 75.0
  },
  "is_active": true,
  "first_awarded_year": 1959,
  "last_awarded_year": 2025,
  "statutory_recipient_types": [
    "Artist",
    "Producer",
    "Engineer",
    "Songwriter"
  ],
  "max_nominees_standard": 8,
  "created_at": "1959-05-04T00:00:00Z"
}
```

---

## 2. `award_fields`

- **Collection Name**: `award_fields`
- **Entity Represented**: `AwardFieldDomain`
- **Purpose**: Broad genre umbrella categories and committees
- **Expected Feasibility Count**: 50+ historical and modern fields
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`field_id`).
- **Domain Key**: `field_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `field_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Awards Guidelines
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (field_id) |
| `field_id` | `string` | YES | Domain attribute: field_id |
| `field_name` | `string` | YES | Domain attribute: field_name |
| `field_abbreviation` | `string` | YES | Domain attribute: field_abbreviation |
| `field_description` | `string` | YES | Domain attribute: field_description |
| `inaugural_ceremony_edition` | `int` | YES | Domain attribute: inaugural_ceremony_edition |
| `current_active_status` | `bool` | YES | Domain attribute: current_active_status |
| `active_categories_count` | `int` | YES | Domain attribute: active_categories_count |
| `specialist_committee_jurisdiction` | `string` | YES | Domain attribute: specialist_committee_jurisdiction |
| `field_curator_role` | `string` | YES | Domain attribute: field_curator_role |
| `last_bylaw_revision_year` | `int` | YES | Domain attribute: last_bylaw_revision_year |

### Document Structure Example
```json
{
  "_id": "AWARD_FIELDS_001",
  "field_id": "AWARD_FIELDS_001",
  "field_name": "sample_field_name",
  "field_abbreviation": "sample_field_abbreviation",
  "field_description": "sample_field_description",
  "inaugural_ceremony_edition": 1,
  "current_active_status": true,
  "active_categories_count": 1,
  "specialist_committee_jurisdiction": "sample_specialist_committee_jurisdiction",
  "field_curator_role": "sample_field_curator_role",
  "last_bylaw_revision_year": 1
}
```

---

## 3. `category_lineage`

- **Collection Name**: `category_lineage`
- **Entity Represented**: `CategoryLineageNode`
- **Purpose**: Genealogical tree tracking how categories evolved
- **Expected Feasibility Count**: 120+ historical lineage nodes
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`lineage_id`).
- **Domain Key**: `lineage_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `ancestor_category_id`, `category_id`, `current_category_id`, `lineage_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Academy Category Rulebooks
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (lineage_id) |
| `lineage_id` | `string` | YES | Domain attribute: lineage_id |
| `category_id` | `string` | YES | Domain attribute: category_id |
| `predecessor_category_name` | `string` | YES | Domain attribute: predecessor_category_name |
| `successor_category_name` | `string` | YES | Domain attribute: successor_category_name |
| `effective_ceremony_edition` | `int` | YES | Domain attribute: effective_ceremony_edition |
| `transition_classification` | `string` | YES | Domain attribute: transition_classification |
| `structural_rationale` | `string` | YES | Domain attribute: structural_rationale |
| `nominee_slate_impact_count` | `int` | YES | Domain attribute: nominee_slate_impact_count |
| `trustee_resolution_reference` | `string` | YES | Domain attribute: trustee_resolution_reference |
| `ballot_clarification_bulletin` | `string` | YES | Domain attribute: ballot_clarification_bulletin |

### Document Structure Example
```json
{
  "_id": "CATEGORY_LINEAGE_001",
  "lineage_id": "CATEGORY_LINEAGE_001",
  "category_id": "sample_category_id",
  "predecessor_category_name": "sample_predecessor_category_name",
  "successor_category_name": "sample_successor_category_name",
  "effective_ceremony_edition": 1,
  "transition_classification": "sample_transition_classification",
  "structural_rationale": "sample_structural_rationale",
  "nominee_slate_impact_count": 1,
  "trustee_resolution_reference": "sample_trustee_resolution_reference",
  "ballot_clarification_bulletin": "sample_ballot_clarification_bulletin"
}
```

---

## 4. `category_quotas_limits`

- **Collection Name**: `category_quotas_limits`
- **Entity Represented**: `CategoryQuotaParameter`
- **Purpose**: Statutory caps on nominee counts and member ballots
- **Expected Feasibility Count**: 65+ quota parameter definitions
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`quota_id`).
- **Domain Key**: `quota_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `category_id`, `quota_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Academy Regulatory Rules
- **Data Classification Tier**: `DERIVED DATA`
- **Derived-Data Indicator**: `YES`
- **Derivation Logic**: Computed via aggregation pipeline across core source data during ETL.

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (quota_id) |
| `quota_id` | `string` | YES | Domain attribute: quota_id |
| `category_id` | `string` | YES | Domain attribute: category_id |
| `ceremony_edition` | `int` | YES | Domain attribute: ceremony_edition |
| `standard_nominee_limit` | `int` | YES | Domain attribute: standard_nominee_limit |
| `emergency_tie_allowance` | `int` | YES | Domain attribute: emergency_tie_allowance |
| `max_credited_producers_eligible` | `int` | YES | Domain attribute: max_credited_producers_eligible |
| `max_credited_engineers_eligible` | `int` | YES | Domain attribute: max_credited_engineers_eligible |
| `playing_time_contribution_threshold_pct` | `double` | YES | Domain attribute: playing_time_contribution_threshold_pct |
| `lyricist_track_threshold_pct` | `double` | YES | Domain attribute: lyricist_track_threshold_pct |
| `pro_rata_trophy_rule` | `string` | YES | Domain attribute: pro_rata_trophy_rule |

### Document Structure Example
```json
{
  "_id": "CATEGORY_QUOTAS_LIMITS_001",
  "quota_id": "CATEGORY_QUOTAS_LIMITS_001",
  "category_id": "sample_category_id",
  "ceremony_edition": 1,
  "standard_nominee_limit": 1,
  "emergency_tie_allowance": 1,
  "max_credited_producers_eligible": 1,
  "max_credited_engineers_eligible": 1,
  "playing_time_contribution_threshold_pct": 100.0,
  "lyricist_track_threshold_pct": 100.0,
  "pro_rata_trophy_rule": "sample_pro_rata_trophy_rule"
}
```

---

## 5. `craft_credit_definitions`

- **Collection Name**: `craft_credit_definitions`
- **Entity Represented**: `CraftCreditRuleDefinition`
- **Purpose**: Academy standards determining statuette-eligible roles
- **Expected Feasibility Count**: 55+ craft credit benchmarks
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`credit_def_id`).
- **Domain Key**: `credit_def_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `category_id`, `craft_def_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Craft Committee Guidelines
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (craft_def_id) |
| `craft_def_id` | `string` | YES | Domain attribute: craft_def_id |
| `category_id` | `string` | YES | Domain attribute: category_id |
| `craft_role_name` | `string` | YES | Domain attribute: craft_role_name |
| `mandatory_statuette_recipient` | `bool` | YES | Domain attribute: mandatory_statuette_recipient |
| `certificate_of_merit_alternative` | `bool` | YES | Domain attribute: certificate_of_merit_alternative |
| `audio_stem_mastering_threshold` | `double` | YES | Domain attribute: audio_stem_mastering_threshold |
| `assistant_engineer_eligibility` | `bool` | YES | Domain attribute: assistant_engineer_eligibility |
| `sample_creator_eligibility` | `bool` | YES | Domain attribute: sample_creator_eligibility |
| `documentation_proof_standard` | `string` | YES | Domain attribute: documentation_proof_standard |
| `union_credit_registry_crosscheck` | `string` | YES | Domain attribute: union_credit_registry_crosscheck |

### Document Structure Example
```json
{
  "_id": "CRAFT_CREDIT_DEFINITIONS_001",
  "craft_def_id": "sample_craft_def_id",
  "category_id": "sample_category_id",
  "craft_role_name": "sample_craft_role_name",
  "mandatory_statuette_recipient": true,
  "certificate_of_merit_alternative": true,
  "audio_stem_mastering_threshold": 100.0,
  "assistant_engineer_eligibility": true,
  "sample_creator_eligibility": true,
  "documentation_proof_standard": "sample_documentation_proof_standard",
  "union_credit_registry_crosscheck": "sample_union_credit_registry_crosscheck",
  "credit_def_id": "CRAFT_CREDIT_DEFINITIONS_001"
}
```

---

## 6. `discontinued_categories`

- **Collection Name**: `discontinued_categories`
- **Entity Represented**: `DiscontinuedCategoryAudit`
- **Purpose**: Retired award categories with deactivation rationale
- **Expected Feasibility Count**: 85+ retired award categories
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`discontinued_id`).
- **Domain Key**: `discontinued_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `category_id`, `discontinued_id`, `merged_into_category_id`, `successor_category_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Academy Category Retirement Records
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (discontinued_id) |
| `discontinued_id` | `string` | YES | Domain attribute: discontinued_id |
| `category_name` | `string` | YES | Domain attribute: category_name |
| `final_active_ceremony_edition` | `int` | YES | Domain attribute: final_active_ceremony_edition |
| `cumulative_years_active` | `int` | YES | Domain attribute: cumulative_years_active |
| `retirement_rationale` | `string` | YES | Domain attribute: retirement_rationale |
| `merged_into_category_id` | `string` | YES | Domain attribute: merged_into_category_id |
| `total_winners_awarded` | `int` | YES | Domain attribute: total_winners_awarded |
| `total_nominations_recorded` | `int` | YES | Domain attribute: total_nominations_recorded |
| `historic_significance_tag` | `string` | YES | Domain attribute: historic_significance_tag |
| `archive_vault_reference` | `string` | YES | Domain attribute: archive_vault_reference |

### Document Structure Example
```json
{
  "_id": "DISCONTINUED_CATEGORIES_001",
  "discontinued_id": "DISCONTINUED_CATEGORIES_001",
  "category_name": "sample_category_name",
  "final_active_ceremony_edition": 1,
  "cumulative_years_active": 1,
  "retirement_rationale": "sample_retirement_rationale",
  "merged_into_category_id": "sample_merged_into_category_id",
  "total_winners_awarded": 1,
  "total_nominations_recorded": 1,
  "historic_significance_tag": "sample_historic_significance_tag",
  "archive_vault_reference": "sample_archive_vault_reference"
}
```

---

## 7. `eligibility_rules`

- **Collection Name**: `eligibility_rules`
- **Entity Represented**: `CategoryEligibilityRule`
- **Purpose**: Formal qualification standards for submitted recordings
- **Expected Feasibility Count**: 75+ eligibility rule clauses
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`rule_id`).
- **Domain Key**: `rule_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `category_id`, `field_id`, `rule_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Awards Guidelines
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (rule_id) |
| `rule_id` | `string` | YES | Domain attribute: rule_id |
| `category_id` | `string` | YES | Domain attribute: category_id |
| `effective_edition` | `int` | YES | Domain attribute: effective_edition |
| `minimum_playing_time_minutes` | `double` | YES | Domain attribute: minimum_playing_time_minutes |
| `minimum_track_count` | `int` | YES | Domain attribute: minimum_track_count |
| `featured_performance_threshold_pct` | `double` | YES | Domain attribute: featured_performance_threshold_pct |
| `us_release_commercial_requirement` | `bool` | YES | Domain attribute: us_release_commercial_requirement |
| `language_composition_restrictions` | `string` | YES | Domain attribute: language_composition_restrictions |
| `sample_replay_clearance_rule` | `string` | YES | Domain attribute: sample_replay_clearance_rule |
| `entry_window_months` | `int` | YES | Domain attribute: entry_window_months |

### Document Structure Example
```json
{
  "_id": "ELIGIBILITY_RULES_001",
  "rule_id": "ELIGIBILITY_RULES_001",
  "category_id": "sample_category_id",
  "effective_edition": 1,
  "minimum_playing_time_minutes": 100.0,
  "minimum_track_count": 1,
  "featured_performance_threshold_pct": 100.0,
  "us_release_commercial_requirement": true,
  "language_composition_restrictions": "sample_language_composition_restrictions",
  "sample_replay_clearance_rule": "sample_sample_replay_clearance_rule",
  "entry_window_months": 1
}
```

---

## 8. `merged_split_history`

- **Collection Name**: `merged_split_history`
- **Entity Represented**: `CategoryReorganizationEvent`
- **Purpose**: Historical re-alignments where categories merged or split
- **Expected Feasibility Count**: 55+ reorganization events
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`reorg_id`).
- **Domain Key**: `reorg_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `event_id`, `primary_category_id`, `published_press_bulletin_id`, `source_category_ids`, `target_category_ids`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: `source_category_ids`

### Provenance & Data Tier
- **Source Provenance**: Academy Reorganization Announcements
- **Data Classification Tier**: `DERIVED DATA`
- **Derived-Data Indicator**: `YES`
- **Derivation Logic**: Computed via aggregation pipeline across core source data during ETL.

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (event_id) |
| `event_id` | `string` | YES | Domain attribute: event_id |
| `restructuring_type` | `string` | YES | Domain attribute: restructuring_type |
| `effective_year` | `int` | YES | Domain attribute: effective_year |
| `primary_category_id` | `string` | YES | Domain attribute: primary_category_id |
| `source_category_ids` | `array` | YES | Domain attribute: source_category_ids |
| `consolidation_justification` | `string` | YES | Domain attribute: consolidation_justification |
| `gender_neutral_reform_flag` | `bool` | YES | Domain attribute: gender_neutral_reform_flag |
| `member_feedback_period_days` | `int` | YES | Domain attribute: member_feedback_period_days |
| `trustee_vote_tally` | `string` | YES | Domain attribute: trustee_vote_tally |
| `published_press_bulletin_id` | `string` | YES | Domain attribute: published_press_bulletin_id |

### Document Structure Example
```json
{
  "_id": "MERGED_SPLIT_HISTORY_001",
  "event_id": "sample_event_id",
  "restructuring_type": "sample_restructuring_type",
  "effective_year": 1,
  "primary_category_id": "sample_primary_category_id",
  "source_category_ids": [
    "SAMPLE_ITEM"
  ],
  "consolidation_justification": "sample_consolidation_justification",
  "gender_neutral_reform_flag": true,
  "member_feedback_period_days": 1,
  "trustee_vote_tally": "sample_trustee_vote_tally",
  "published_press_bulletin_id": "sample_published_press_bulletin_id",
  "reorg_id": "MERGED_SPLIT_HISTORY_001"
}
```

---

## 9. `special_merit_categories`

- **Collection Name**: `special_merit_categories`
- **Entity Represented**: `SpecialMeritCategoryDefinition`
- **Purpose**: Governance standards for honorary and non-competitive awards
- **Expected Feasibility Count**: 50+ special merit standards
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`special_category_id`).
- **Domain Key**: `special_category_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `special_merit_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Special Merit Committee Charters
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (special_merit_id) |
| `special_merit_id` | `string` | YES | Domain attribute: special_merit_id |
| `award_title` | `string` | YES | Domain attribute: award_title |
| `conferral_frequency` | `string` | YES | Domain attribute: conferral_frequency |
| `governing_board_supermajority_pct` | `double` | YES | Domain attribute: governing_board_supermajority_pct |
| `candidate_selection_protocol` | `string` | YES | Domain attribute: candidate_selection_protocol |
| `trophy_or_plaque_type` | `string` | YES | Domain attribute: trophy_or_plaque_type |
| `first_conferred_year` | `int` | YES | Domain attribute: first_conferred_year |
| `target_industry_discipline` | `string` | YES | Domain attribute: target_industry_discipline |
| `peer_nomination_permitted` | `bool` | YES | Domain attribute: peer_nomination_permitted |
| `ceremony_segment_placement` | `string` | YES | Domain attribute: ceremony_segment_placement |

### Document Structure Example
```json
{
  "_id": "SPECIAL_MERIT_CATEGORIES_001",
  "special_merit_id": "sample_special_merit_id",
  "award_title": "sample_award_title",
  "conferral_frequency": "sample_conferral_frequency",
  "governing_board_supermajority_pct": 100.0,
  "candidate_selection_protocol": "sample_candidate_selection_protocol",
  "trophy_or_plaque_type": "sample_trophy_or_plaque_type",
  "first_conferred_year": 1,
  "target_industry_discipline": "sample_target_industry_discipline",
  "peer_nomination_permitted": true,
  "ceremony_segment_placement": "sample_ceremony_segment_placement",
  "special_category_id": "SPECIAL_MERIT_CATEGORIES_001"
}
```

---

## 10. `voting_procedures`

- **Collection Name**: `voting_procedures`
- **Entity Represented**: `VotingProcedureProtocol`
- **Purpose**: Voting stages and balloting algorithms across eras
- **Expected Feasibility Count**: 55+ voting procedural configs
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`procedure_id`).
- **Domain Key**: `procedure_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `category_id`, `field_id`, `procedure_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Voting Procedures Manual
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (procedure_id) |
| `procedure_id` | `string` | YES | Domain attribute: procedure_id |
| `category_id` | `string` | YES | Domain attribute: category_id |
| `voting_round_number` | `int` | YES | Domain attribute: voting_round_number |
| `electorate_body_type` | `string` | YES | Domain attribute: electorate_body_type |
| `is_ranked_choice_ballot` | `bool` | YES | Domain attribute: is_ranked_choice_ballot |
| `craft_committee_review_required` | `bool` | YES | Domain attribute: craft_committee_review_required |
| `committee_member_roster_count` | `int` | YES | Domain attribute: committee_member_roster_count |
| `nomination_slot_capacity` | `int` | YES | Domain attribute: nomination_slot_capacity |
| `tie_breaking_protocol` | `string` | YES | Domain attribute: tie_breaking_protocol |
| `auditing_firm_signoff_flag` | `bool` | YES | Domain attribute: auditing_firm_signoff_flag |

### Document Structure Example
```json
{
  "_id": "VOTING_PROCEDURES_001",
  "procedure_id": "VOTING_PROCEDURES_001",
  "category_id": "sample_category_id",
  "voting_round_number": 1,
  "electorate_body_type": "sample_electorate_body_type",
  "is_ranked_choice_ballot": true,
  "craft_committee_review_required": true,
  "committee_member_roster_count": 1,
  "nomination_slot_capacity": 1,
  "tie_breaking_protocol": "sample_tie_breaking_protocol",
  "auditing_firm_signoff_flag": true
}
```

---
