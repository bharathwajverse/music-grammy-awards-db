# GRAMMY Creators, Artists & Industry Entities Database (`grammy_creators_db`)

> **Phase**: Phase 11 — MongoDB Document Model Design
> **Database**: `grammy_creators_db`
> **Allocated Collections**: 10 collections
> **Quota Status**: Verified $\ge 50$ documents and $\ge 10$ meaningful fields per collection

---

## Table of Contents

- [arrangers_conductors](#arrangers-conductors)
- [artists](#artists)
- [audio_engineers](#audio-engineers)
- [creator_collaborations](#creator-collaborations)
- [creator_discographies](#creator-discographies)
- [group_memberships](#group-memberships)
- [musical_groups](#musical-groups)
- [producers](#producers)
- [record_labels](#record-labels)
- [songwriters_composers](#songwriters-composers)

---

## 1. `arrangers_conductors`

- **Collection Name**: `arrangers_conductors`
- **Entity Represented**: `ArrangerConductor`
- **Purpose**: Orchestral arrangers and symphony conductors
- **Expected Feasibility Count**: 20000+ arrangers (80+ prepped)
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`arranger_id`).
- **Domain Key**: `arranger_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `arranger_id`, `creator_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz
- **Data Classification Tier**: `SECONDARY OPEN DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (arranger_id) |
| `arranger_id` | `string` | YES | Domain attribute: arranger_id |
| `creator_id` | `string` | YES | Domain attribute: creator_id |
| `arrangement_discipline` | `string` | YES | Domain attribute: arrangement_discipline |
| `resident_orchestra_ensemble` | `string` | YES | Domain attribute: resident_orchestra_ensemble |
| `formal_conservatory_education` | `string` | YES | Domain attribute: formal_conservatory_education |
| `sheet_music_publisher` | `string` | YES | Domain attribute: sheet_music_publisher |
| `conducts_own_compositions` | `bool` | YES | Domain attribute: conducts_own_compositions |
| `classical_crossover_experience` | `bool` | YES | Domain attribute: classical_crossover_experience |
| `union_musicians_local` | `string` | YES | Domain attribute: union_musicians_local |
| `career_commission_count` | `int` | YES | Domain attribute: career_commission_count |

### Document Structure Example
```json
{
  "_id": "ARRANGERS_CONDUCTORS_001",
  "arranger_id": "ARRANGERS_CONDUCTORS_001",
  "creator_id": "sample_creator_id",
  "arrangement_discipline": "sample_arrangement_discipline",
  "resident_orchestra_ensemble": "sample_resident_orchestra_ensemble",
  "formal_conservatory_education": "sample_formal_conservatory_education",
  "sheet_music_publisher": "sample_sheet_music_publisher",
  "conducts_own_compositions": true,
  "classical_crossover_experience": true,
  "union_musicians_local": "sample_union_musicians_local",
  "career_commission_count": 1
}
```

---

## 2. `artists`

- **Collection Name**: `artists`
- **Entity Represented**: `MusicalArtist`
- **Purpose**: Solo performing vocalists and instrumentalists
- **Expected Feasibility Count**: 2.3M+ artists (500+ prepped)
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`artist_id`).
- **Domain Key**: `artist_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `artist_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: `groups`, `instruments`, `pro_affiliations`

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz / Wikidata
- **Data Classification Tier**: `SECONDARY OPEN DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (15 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (artist_id) |
| `artist_id` | `string` | YES | Domain attribute: artist_id |
| `full_legal_name` | `string` | YES | Domain attribute: full_legal_name |
| `stage_name` | `string` | YES | Domain attribute: stage_name |
| `primary_musical_genre` | `string` | YES | Domain attribute: primary_musical_genre |
| `birth_or_formation_date` | `string` | YES | Domain attribute: birth_or_formation_date |
| `country_of_citizenship` | `string` | YES | Domain attribute: country_of_citizenship |
| `active_career_start_year` | `int` | YES | Domain attribute: active_career_start_year |
| `is_group_ensemble_flag` | `bool` | YES | Domain attribute: is_group_ensemble_flag |
| `musicbrainz_artist_gid` | `string` | YES | Domain attribute: musicbrainz_artist_gid |
| `official_website_url` | `string` | YES | Domain attribute: official_website_url |
| `biography_overview` | `string` | YES | Domain attribute: biography_overview |
| `instruments` | `array` | NO | Orthogonal 4NF musical instrument competencies |
| `pro_affiliations` | `array` | NO | Orthogonal 4NF performing rights organizations |
| `groups` | `array` | NO | Embedded summaries of musical group memberships |

### Document Structure Example
```json
{
  "_id": "CRT_BEYONCE_001",
  "creator_id": "CRT_BEYONCE_001",
  "legal_name": "Beyonc\u00e9 Giselle Knowles-Carter",
  "stage_name": "Beyonc\u00e9",
  "birth_date": "1981-09-04",
  "birth_country": "United States",
  "primary_role": "Vocalist / Songwriter / Producer",
  "active_years_start": 1997,
  "instruments": [
    "Vocals",
    "Piano"
  ],
  "pro_affiliations": [
    "ASCAP",
    "PRS"
  ],
  "groups": [
    {
      "group_id": "GRP_DESTINYS_CHILD",
      "group_name": "Destiny's Child"
    }
  ],
  "is_deceased": false,
  "created_at": "2021-01-01T00:00:00Z"
}
```

---

## 3. `audio_engineers`

- **Collection Name**: `audio_engineers`
- **Entity Represented**: `AudioEngineer`
- **Purpose**: Recording mixing mastering and spatial audio engineers
- **Expected Feasibility Count**: 40000+ engineers (100+ prepped)
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`engineer_id`).
- **Domain Key**: `engineer_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `creator_id`, `discogs_engineer_id`, `engineer_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz / Audio Engineering Society
- **Data Classification Tier**: `SECONDARY OPEN DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (engineer_id) |
| `engineer_id` | `string` | YES | Domain attribute: engineer_id |
| `creator_id` | `string` | YES | Domain attribute: creator_id |
| `engineering_specialization` | `string` | YES | Domain attribute: engineering_specialization |
| `primary_mastering_facility` | `string` | YES | Domain attribute: primary_mastering_facility |
| `hardware_console_credits` | `string` | YES | Domain attribute: hardware_console_credits |
| `dolby_atmos_certified_status` | `bool` | YES | Domain attribute: dolby_atmos_certified_status |
| `aes_professional_membership` | `bool` | YES | Domain attribute: aes_professional_membership |
| `first_album_engineering_year` | `int` | YES | Domain attribute: first_album_engineering_year |
| `technical_patents_held` | `int` | YES | Domain attribute: technical_patents_held |
| `discogs_engineer_id` | `string` | YES | Domain attribute: discogs_engineer_id |

### Document Structure Example
```json
{
  "_id": "AUDIO_ENGINEERS_001",
  "engineer_id": "AUDIO_ENGINEERS_001",
  "creator_id": "sample_creator_id",
  "engineering_specialization": "sample_engineering_specialization",
  "primary_mastering_facility": "sample_primary_mastering_facility",
  "hardware_console_credits": "sample_hardware_console_credits",
  "dolby_atmos_certified_status": true,
  "aes_professional_membership": true,
  "first_album_engineering_year": 1,
  "technical_patents_held": 1,
  "discogs_engineer_id": "sample_discogs_engineer_id"
}
```

---

## 4. `creator_collaborations`

- **Collection Name**: `creator_collaborations`
- **Entity Represented**: `CollaborativePartnership`
- **Purpose**: Recurrent artistic and production creative partnerships
- **Expected Feasibility Count**: 150+ documented partnerships
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`collab_id`).
- **Domain Key**: `collab_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `collab_id`, `creator_a_id`, `creator_b_id`, `creator_id_1`, `creator_id_2`, `work_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz / Nomination Co-Credits Join
- **Data Classification Tier**: `DERIVED DATA`
- **Derived-Data Indicator**: `YES`
- **Derivation Logic**: Computed via aggregation pipeline across core source data during ETL.

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (collab_id) |
| `collab_id` | `string` | YES | Domain attribute: collab_id |
| `work_id` | `string` | YES | Domain attribute: work_id |
| `creator_a_id` | `string` | YES | Domain attribute: creator_a_id |
| `creator_b_id` | `string` | YES | Domain attribute: creator_b_id |
| `collaboration_nature` | `string` | YES | Domain attribute: collaboration_nature |
| `billing_credit_format` | `string` | YES | Domain attribute: billing_credit_format |
| `publishing_split_percentage` | `double` | YES | Domain attribute: publishing_split_percentage |
| `joint_grammy_nominations_count` | `int` | YES | Domain attribute: joint_grammy_nominations_count |
| `clearance_agreement_date` | `string` | YES | Domain attribute: clearance_agreement_date |
| `inter_label_licensing_waiver` | `string` | YES | Domain attribute: inter_label_licensing_waiver |

### Document Structure Example
```json
{
  "_id": "CREATOR_COLLABORATIONS_001",
  "collab_id": "CREATOR_COLLABORATIONS_001",
  "work_id": "sample_work_id",
  "creator_a_id": "sample_creator_a_id",
  "creator_b_id": "sample_creator_b_id",
  "collaboration_nature": "sample_collaboration_nature",
  "billing_credit_format": "sample_billing_credit_format",
  "publishing_split_percentage": 100.0,
  "joint_grammy_nominations_count": 1,
  "clearance_agreement_date": "sample_clearance_agreement_date",
  "inter_label_licensing_waiver": "sample_inter_label_licensing_waiver"
}
```

---

## 5. `creator_discographies`

- **Collection Name**: `creator_discographies`
- **Entity Represented**: `CreatorReleaseCatalogEntry`
- **Purpose**: Released master musical albums and singles by creators
- **Expected Feasibility Count**: 1000+ release catalog entries
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`discography_id`).
- **Domain Key**: `discography_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `creator_id`, `discography_id`, `master_rights_holder_label_id`, `record_label_id`, `work_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz / RIAA Certification Database
- **Data Classification Tier**: `SECONDARY OPEN DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (discography_id) |
| `discography_id` | `string` | YES | Domain attribute: discography_id |
| `creator_id` | `string` | YES | Domain attribute: creator_id |
| `work_id` | `string` | YES | Domain attribute: work_id |
| `release_calendar_year` | `int` | YES | Domain attribute: release_calendar_year |
| `primary_credit_type` | `string` | YES | Domain attribute: primary_credit_type |
| `catalog_matrix_code` | `string` | YES | Domain attribute: catalog_matrix_code |
| `billboard_200_peak_position` | `int` | YES | Domain attribute: billboard_200_peak_position |
| `riaa_certification_status` | `string` | YES | Domain attribute: riaa_certification_status |
| `recording_studio_facility` | `string` | YES | Domain attribute: recording_studio_facility |
| `master_rights_holder_label_id` | `string` | YES | Domain attribute: master_rights_holder_label_id |

### Document Structure Example
```json
{
  "_id": "CREATOR_DISCOGRAPHIES_001",
  "discography_id": "CREATOR_DISCOGRAPHIES_001",
  "creator_id": "sample_creator_id",
  "work_id": "sample_work_id",
  "release_calendar_year": 1,
  "primary_credit_type": "sample_primary_credit_type",
  "catalog_matrix_code": "sample_catalog_matrix_code",
  "billboard_200_peak_position": 1,
  "riaa_certification_status": "sample_riaa_certification_status",
  "recording_studio_facility": "sample_recording_studio_facility",
  "master_rights_holder_label_id": "sample_master_rights_holder_label_id"
}
```

---

## 6. `group_memberships`

- **Collection Name**: `group_memberships`
- **Entity Represented**: `GroupMembershipTenure`
- **Purpose**: Tenures linking individual artists into musical groups
- **Expected Feasibility Count**: 500000+ memberships (120+ prepped)
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`membership_id`).
- **Domain Key**: `membership_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `artist_id`, `group_id`, `membership_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz Relationship Graph
- **Data Classification Tier**: `SECONDARY OPEN DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (membership_id) |
| `membership_id` | `string` | YES | Domain attribute: membership_id |
| `group_id` | `string` | YES | Domain attribute: group_id |
| `artist_id` | `string` | YES | Domain attribute: artist_id |
| `role_within_group` | `string` | YES | Domain attribute: role_within_group |
| `tenure_start_year` | `int` | YES | Domain attribute: tenure_start_year |
| `tenure_end_year` | `int` | YES | Domain attribute: tenure_end_year |
| `is_founding_member` | `bool` | YES | Domain attribute: is_founding_member |
| `is_primary_frontperson` | `bool` | YES | Domain attribute: is_primary_frontperson |
| `royalty_split_contract_percentage` | `double` | YES | Domain attribute: royalty_split_contract_percentage |
| `member_departure_reason` | `string` | YES | Domain attribute: member_departure_reason |

### Document Structure Example
```json
{
  "_id": "GROUP_MEMBERSHIPS_001",
  "membership_id": "GROUP_MEMBERSHIPS_001",
  "group_id": "sample_group_id",
  "artist_id": "sample_artist_id",
  "role_within_group": "sample_role_within_group",
  "tenure_start_year": 1,
  "tenure_end_year": 1,
  "is_founding_member": true,
  "is_primary_frontperson": true,
  "royalty_split_contract_percentage": 100.0,
  "member_departure_reason": "sample_member_departure_reason"
}
```

---

## 7. `musical_groups`

- **Collection Name**: `musical_groups`
- **Entity Represented**: `MusicalPerformingGroup`
- **Purpose**: Bands duos vocal ensembles orchestras and choirs
- **Expected Feasibility Count**: 150000+ groups (100+ prepped)
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`group_id`).
- **Domain Key**: `group_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `group_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: `members`

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz / Wikidata
- **Data Classification Tier**: `SECONDARY OPEN DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (12 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (group_id) |
| `group_id` | `string` | YES | Domain attribute: group_id |
| `group_name` | `string` | YES | Domain attribute: group_name |
| `formation_calendar_year` | `int` | YES | Domain attribute: formation_calendar_year |
| `disbandment_year` | `int` | YES | Domain attribute: disbandment_year |
| `ensemble_structure_type` | `string` | YES | Domain attribute: ensemble_structure_type |
| `origin_city` | `string` | YES | Domain attribute: origin_city |
| `origin_country` | `string` | YES | Domain attribute: origin_country |
| `current_activity_status` | `bool` | YES | Domain attribute: current_activity_status |
| `signature_musical_style` | `string` | YES | Domain attribute: signature_musical_style |
| `musicbrainz_group_gid` | `string` | YES | Domain attribute: musicbrainz_group_gid |
| `members` | `array` | NO | Embedded roster of musical group members |

### Document Structure Example
```json
{
  "_id": "MUSICAL_GROUPS_001",
  "group_id": "MUSICAL_GROUPS_001",
  "group_name": "sample_group_name",
  "formation_calendar_year": 1,
  "disbandment_year": 1,
  "ensemble_structure_type": "sample_ensemble_structure_type",
  "origin_city": "sample_origin_city",
  "origin_country": "sample_origin_country",
  "current_activity_status": true,
  "signature_musical_style": "sample_signature_musical_style",
  "musicbrainz_group_gid": "sample_musicbrainz_group_gid",
  "members": [
    "SAMPLE_ITEM"
  ]
}
```

---

## 8. `producers`

- **Collection Name**: `producers`
- **Entity Represented**: `RecordProducer`
- **Purpose**: Record producers and vocal producers
- **Expected Feasibility Count**: 50000+ producers (100+ prepped)
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`producer_id`).
- **Domain Key**: `producer_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `associated_record_label_id`, `creator_id`, `discogs_producer_id`, `producer_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: `certified_workflows`, `eligible_categories`

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz Core Data
- **Data Classification Tier**: `SECONDARY OPEN DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (13 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (producer_id) |
| `producer_id` | `string` | YES | Domain attribute: producer_id |
| `creator_id` | `string` | YES | Domain attribute: creator_id |
| `primary_production_genre` | `string` | YES | Domain attribute: primary_production_genre |
| `headquarters_studio_location` | `string` | YES | Domain attribute: headquarters_studio_location |
| `production_company_affiliation` | `string` | YES | Domain attribute: production_company_affiliation |
| `analog_digital_workflow_preference` | `string` | YES | Domain attribute: analog_digital_workflow_preference |
| `total_career_credits_count` | `int` | YES | Domain attribute: total_career_credits_count |
| `discogs_producer_id` | `string` | YES | Domain attribute: discogs_producer_id |
| `first_notable_production_year` | `int` | YES | Domain attribute: first_notable_production_year |
| `signature_sound_profile` | `string` | YES | Domain attribute: signature_sound_profile |
| `certified_workflows` | `array` | NO | 5NF multi-key certified acoustic and spatial mixing workflows |
| `eligible_categories` | `array` | NO | Categories admissible for producer submissions |

### Document Structure Example
```json
{
  "_id": "PRODUCERS_001",
  "producer_id": "PRODUCERS_001",
  "creator_id": "sample_creator_id",
  "primary_production_genre": "sample_primary_production_genre",
  "headquarters_studio_location": "sample_headquarters_studio_location",
  "production_company_affiliation": "sample_production_company_affiliation",
  "analog_digital_workflow_preference": "sample_analog_digital_workflow_preference",
  "total_career_credits_count": 1,
  "discogs_producer_id": "sample_discogs_producer_id",
  "first_notable_production_year": 1,
  "signature_sound_profile": "sample_signature_sound_profile",
  "certified_workflows": [
    "SAMPLE_ITEM"
  ],
  "eligible_categories": [
    "SAMPLE_ITEM"
  ]
}
```

---

## 9. `record_labels`

- **Collection Name**: `record_labels`
- **Entity Represented**: `CommercialRecordLabel`
- **Purpose**: Commercial record companies imprints and distributors
- **Expected Feasibility Count**: 100000+ labels (100+ prepped)
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`label_id`).
- **Domain Key**: `label_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `label_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz Core Data (Labels)
- **Data Classification Tier**: `SECONDARY OPEN DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (label_id) |
| `label_id` | `string` | YES | Domain attribute: label_id |
| `label_corporate_name` | `string` | YES | Domain attribute: label_corporate_name |
| `parent_music_group` | `string` | YES | Domain attribute: parent_music_group |
| `foundation_year` | `int` | YES | Domain attribute: foundation_year |
| `corporate_headquarters_city` | `string` | YES | Domain attribute: corporate_headquarters_city |
| `origin_country` | `string` | YES | Domain attribute: origin_country |
| `commercial_distribution_channel` | `string` | YES | Domain attribute: commercial_distribution_channel |
| `riaa_member_standing` | `bool` | YES | Domain attribute: riaa_member_standing |
| `historical_catalog_size` | `int` | YES | Domain attribute: historical_catalog_size |
| `current_operational_status` | `string` | YES | Domain attribute: current_operational_status |

### Document Structure Example
```json
{
  "_id": "RECORD_LABELS_001",
  "label_id": "RECORD_LABELS_001",
  "label_corporate_name": "sample_label_corporate_name",
  "parent_music_group": "sample_parent_music_group",
  "foundation_year": 1,
  "corporate_headquarters_city": "sample_corporate_headquarters_city",
  "origin_country": "sample_origin_country",
  "commercial_distribution_channel": "sample_commercial_distribution_channel",
  "riaa_member_standing": true,
  "historical_catalog_size": 1,
  "current_operational_status": "sample_current_operational_status"
}
```

---

## 10. `songwriters_composers`

- **Collection Name**: `songwriters_composers`
- **Entity Represented**: `SongwriterComposer`
- **Purpose**: Lyricists composers and songwriters with PRO data
- **Expected Feasibility Count**: 100000+ songwriters (100+ prepped)
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`songwriter_id`).
- **Domain Key**: `songwriter_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `creator_id`, `songwriter_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: MusicBrainz / ASCAP / BMI
- **Data Classification Tier**: `SECONDARY OPEN DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (songwriter_id) |
| `songwriter_id` | `string` | YES | Domain attribute: songwriter_id |
| `creator_id` | `string` | YES | Domain attribute: creator_id |
| `pro_affiliation` | `string` | YES | Domain attribute: pro_affiliation |
| `ipi_cae_identifier` | `string` | YES | Domain attribute: ipi_cae_identifier |
| `music_publisher_company` | `string` | YES | Domain attribute: music_publisher_company |
| `lyric_vs_composition_focus` | `string` | YES | Domain attribute: lyric_vs_composition_focus |
| `registered_works_count` | `int` | YES | Domain attribute: registered_works_count |
| `inducted_songwriters_hof` | `bool` | YES | Domain attribute: inducted_songwriters_hof |
| `primary_songwriting_instrument` | `string` | YES | Domain attribute: primary_songwriting_instrument |
| `signature_melodic_style` | `string` | YES | Domain attribute: signature_melodic_style |

### Document Structure Example
```json
{
  "_id": "SONGWRITERS_COMPOSERS_001",
  "songwriter_id": "SONGWRITERS_COMPOSERS_001",
  "creator_id": "sample_creator_id",
  "pro_affiliation": "sample_pro_affiliation",
  "ipi_cae_identifier": "sample_ipi_cae_identifier",
  "music_publisher_company": "sample_music_publisher_company",
  "lyric_vs_composition_focus": "sample_lyric_vs_composition_focus",
  "registered_works_count": 1,
  "inducted_songwriters_hof": true,
  "primary_songwriting_instrument": "sample_primary_songwriting_instrument",
  "signature_melodic_style": "sample_signature_melodic_style"
}
```

---
