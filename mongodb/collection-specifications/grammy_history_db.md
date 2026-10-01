# GRAMMY History & Broadcast Telecasts Database (`grammy_history_db`)

> **Phase**: Phase 11 — MongoDB Document Model Design
> **Database**: `grammy_history_db`
> **Allocated Collections**: 10 collections
> **Quota Status**: Verified $\ge 50$ documents and $\ge 10$ meaningful fields per collection

---

## Table of Contents

- [academy_leadership](#academy-leadership)
- [ceremonies](#ceremonies)
- [ceremony_hosts](#ceremony-hosts)
- [historic_milestones](#historic-milestones)
- [lifetime_achievement_honors](#lifetime-achievement-honors)
- [press_media_accreditations](#press-media-accreditations)
- [telecast_broadcasters](#telecast-broadcasters)
- [timeline_historical_eras](#timeline-historical-eras)
- [venues](#venues)
- [viewership_ratings](#viewership-ratings)

---

## 1. `academy_leadership`

- **Collection Name**: `academy_leadership`
- **Entity Represented**: `AcademyLeaderTenure`
- **Purpose**: Trustees and presidents directing Academy governance
- **Expected Feasibility Count**: 60+ leadership tenures
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`leadership_id`).
- **Domain Key**: `leadership_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `leadership_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Governance Records
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (leadership_id) |
| `leadership_id` | `string` | YES | Domain attribute: leadership_id |
| `officer_name` | `string` | YES | Domain attribute: officer_name |
| `executive_role_title` | `string` | YES | Domain attribute: executive_role_title |
| `tenure_start_year` | `int` | YES | Domain attribute: tenure_start_year |
| `tenure_end_year` | `int` | YES | Domain attribute: tenure_end_year |
| `professional_music_background` | `string` | YES | Domain attribute: professional_music_background |
| `trustee_chapter_location` | `string` | YES | Domain attribute: trustee_chapter_location |
| `notable_policy_amendment` | `string` | YES | Domain attribute: notable_policy_amendment |
| `board_voting_privileges` | `bool` | YES | Domain attribute: board_voting_privileges |
| `appointed_by` | `string` | YES | Domain attribute: appointed_by |

### Document Structure Example
```json
{
  "_id": "ACADEMY_LEADERSHIP_001",
  "leadership_id": "ACADEMY_LEADERSHIP_001",
  "officer_name": "sample_officer_name",
  "executive_role_title": "sample_executive_role_title",
  "tenure_start_year": 1,
  "tenure_end_year": 1,
  "professional_music_background": "sample_professional_music_background",
  "trustee_chapter_location": "sample_trustee_chapter_location",
  "notable_policy_amendment": "sample_notable_policy_amendment",
  "board_voting_privileges": true,
  "appointed_by": "sample_appointed_by"
}
```

---

## 2. `ceremonies`

- **Collection Name**: `ceremonies`
- **Entity Represented**: `CeremonyEdition`
- **Purpose**: Master historical registry of GRAMMY Award ceremony editions
- **Expected Feasibility Count**: 67 ceremonies (1959-2025)
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`ceremony_id`).
- **Domain Key**: `ceremony_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `ceremony_id`, `venue_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: `venue`
- **Arrays**: `hosts`

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Official Archives
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (14 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (ceremony_id) |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `edition_number` | `int` | YES | Domain attribute: edition_number |
| `ceremony_date` | `string` | YES | Domain attribute: ceremony_date |
| `broadcast_year` | `int` | YES | Domain attribute: broadcast_year |
| `eligibility_period_start` | `string` | YES | Domain attribute: eligibility_period_start |
| `eligibility_period_end` | `string` | YES | Domain attribute: eligibility_period_end |
| `host_city` | `string` | YES | Domain attribute: host_city |
| `venue_id` | `string` | YES | Domain attribute: venue_id |
| `primary_network` | `string` | YES | Domain attribute: primary_network |
| `total_awards_presented` | `int` | YES | Domain attribute: total_awards_presented |
| `created_at` | `string` | YES | Domain attribute: created_at |
| `venue` | `object` | NO | Embedded extended reference of host venue |
| `hosts` | `array` | NO | Embedded list of broadcast hosts |

### Document Structure Example
```json
{
  "_id": "CEREMONY_065",
  "ceremony_id": "CEREMONY_065",
  "edition_number": 65,
  "ceremony_date": "2023-02-05T17:00:00Z",
  "broadcast_year": 2023,
  "eligibility_period_start": "2021-10-01",
  "eligibility_period_end": "2022-09-30",
  "host_city": "Los Angeles",
  "venue_id": "VEN_CRYPTO_LA",
  "primary_network": "CBS",
  "total_awards_presented": 91,
  "venue": {
    "venue_id": "VEN_CRYPTO_LA",
    "venue_name": "Crypto.com Arena",
    "city": "Los Angeles",
    "state": "CA",
    "seating_capacity": 20000
  },
  "hosts": [
    {
      "host_name": "Trevor Noah",
      "host_role": "Primary Solo Host",
      "consecutive_year": 3
    }
  ],
  "created_at": "2023-02-06T00:00:00Z"
}
```

---

## 3. `ceremony_hosts`

- **Collection Name**: `ceremony_hosts`
- **Entity Represented**: `CeremonyHostAppearance`
- **Purpose**: Masters of ceremonies and broadcast hosts
- **Expected Feasibility Count**: 70+ host engagements
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`host_id`).
- **Domain Key**: `host_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `ceremony_id`, `creator_id`, `host_assignment_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Telecast Credits
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (host_assignment_id) |
| `host_assignment_id` | `string` | YES | Domain attribute: host_assignment_id |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `creator_id` | `string` | YES | Domain attribute: creator_id |
| `host_full_name` | `string` | YES | Domain attribute: host_full_name |
| `hosting_style` | `string` | YES | Domain attribute: hosting_style |
| `solo_or_duo` | `string` | YES | Domain attribute: solo_or_duo |
| `host_sequence_count` | `int` | YES | Domain attribute: host_sequence_count |
| `monologue_duration_seconds` | `int` | YES | Domain attribute: monologue_duration_seconds |
| `emmy_nomination_received` | `bool` | YES | Domain attribute: emmy_nomination_received |
| `contracted_talent_agency` | `string` | YES | Domain attribute: contracted_talent_agency |

### Document Structure Example
```json
{
  "_id": "CEREMONY_HOSTS_001",
  "host_assignment_id": "sample_host_assignment_id",
  "ceremony_id": "sample_ceremony_id",
  "creator_id": "sample_creator_id",
  "host_full_name": "sample_host_full_name",
  "hosting_style": "sample_hosting_style",
  "solo_or_duo": "sample_solo_or_duo",
  "host_sequence_count": 1,
  "monologue_duration_seconds": 1,
  "emmy_nomination_received": true,
  "contracted_talent_agency": "sample_contracted_talent_agency",
  "host_id": "CEREMONY_HOSTS_001"
}
```

---

## 4. `historic_milestones`

- **Collection Name**: `historic_milestones`
- **Entity Represented**: `HistoricMilestone`
- **Purpose**: Landmark cultural and technological events in GRAMMY history
- **Expected Feasibility Count**: 65+ landmark milestones
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`milestone_id`).
- **Domain Key**: `milestone_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `archival_video_reel_id`, `ceremony_id`, `milestone_id`, `primary_subject_creator_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Official Timeline
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (milestone_id) |
| `milestone_id` | `string` | YES | Domain attribute: milestone_id |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `milestone_title` | `string` | YES | Domain attribute: milestone_title |
| `calendar_year` | `int` | YES | Domain attribute: calendar_year |
| `primary_subject_creator_id` | `string` | YES | Domain attribute: primary_subject_creator_id |
| `cultural_significance_summary` | `string` | YES | Domain attribute: cultural_significance_summary |
| `official_academy_recognition` | `bool` | YES | Domain attribute: official_academy_recognition |
| `controversy_flag` | `bool` | YES | Domain attribute: controversy_flag |
| `archival_video_reel_id` | `string` | YES | Domain attribute: archival_video_reel_id |
| `citation_source_url` | `string` | YES | Domain attribute: citation_source_url |

### Document Structure Example
```json
{
  "_id": "HISTORIC_MILESTONES_001",
  "milestone_id": "HISTORIC_MILESTONES_001",
  "ceremony_id": "sample_ceremony_id",
  "milestone_title": "sample_milestone_title",
  "calendar_year": 1,
  "primary_subject_creator_id": "sample_primary_subject_creator_id",
  "cultural_significance_summary": "sample_cultural_significance_summary",
  "official_academy_recognition": true,
  "controversy_flag": true,
  "archival_video_reel_id": "sample_archival_video_reel_id",
  "citation_source_url": "sample_citation_source_url"
}
```

---

## 5. `lifetime_achievement_honors`

- **Collection Name**: `lifetime_achievement_honors`
- **Entity Represented**: `LifetimeAchievementAward`
- **Purpose**: Special Merit Lifetime Achievement Award honorees
- **Expected Feasibility Count**: 180+ lifetime achievement honorees
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`honor_id`).
- **Domain Key**: `honor_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `ceremony_id`, `creator_id`, `honor_id`, `recipient_creator_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Special Merit Roster
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (honor_id) |
| `honor_id` | `string` | YES | Domain attribute: honor_id |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `recipient_creator_id` | `string` | YES | Domain attribute: recipient_creator_id |
| `honor_type` | `string` | YES | Domain attribute: honor_type |
| `announcement_year` | `int` | YES | Domain attribute: announcement_year |
| `career_span_decades` | `int` | YES | Domain attribute: career_span_decades |
| `presenting_dignitary_name` | `string` | YES | Domain attribute: presenting_dignitary_name |
| `citation_text` | `string` | YES | Domain attribute: citation_text |
| `is_posthumous_award` | `bool` | YES | Domain attribute: is_posthumous_award |
| `special_tribute_performance_flag` | `bool` | YES | Domain attribute: special_tribute_performance_flag |

### Document Structure Example
```json
{
  "_id": "LIFETIME_ACHIEVEMENT_HONORS_001",
  "honor_id": "LIFETIME_ACHIEVEMENT_HONORS_001",
  "ceremony_id": "sample_ceremony_id",
  "recipient_creator_id": "sample_recipient_creator_id",
  "honor_type": "sample_honor_type",
  "announcement_year": 1,
  "career_span_decades": 1,
  "presenting_dignitary_name": "sample_presenting_dignitary_name",
  "citation_text": "sample_citation_text",
  "is_posthumous_award": true,
  "special_tribute_performance_flag": true
}
```

---

## 6. `press_media_accreditations`

- **Collection Name**: `press_media_accreditations`
- **Entity Represented**: `MediaAccreditationPass`
- **Purpose**: Media organizations and broadcast press passes
- **Expected Feasibility Count**: 65+ accredited press organizations
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`accreditation_id`).
- **Domain Key**: `accreditation_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `accreditation_id`, `ceremony_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Communications Archives
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (accreditation_id) |
| `accreditation_id` | `string` | YES | Domain attribute: accreditation_id |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `media_organization_name` | `string` | YES | Domain attribute: media_organization_name |
| `media_channel_type` | `string` | YES | Domain attribute: media_channel_type |
| `origin_country` | `string` | YES | Domain attribute: origin_country |
| `passes_granted_count` | `int` | YES | Domain attribute: passes_granted_count |
| `red_carpet_position_tier` | `string` | YES | Domain attribute: red_carpet_position_tier |
| `press_room_interview_quota` | `int` | YES | Domain attribute: press_room_interview_quota |
| `pool_broadcaster_status` | `bool` | YES | Domain attribute: pool_broadcaster_status |
| `compliance_clearance_status` | `string` | YES | Domain attribute: compliance_clearance_status |

### Document Structure Example
```json
{
  "_id": "PRESS_MEDIA_ACCREDITATIONS_001",
  "accreditation_id": "PRESS_MEDIA_ACCREDITATIONS_001",
  "ceremony_id": "sample_ceremony_id",
  "media_organization_name": "sample_media_organization_name",
  "media_channel_type": "sample_media_channel_type",
  "origin_country": "sample_origin_country",
  "passes_granted_count": 1,
  "red_carpet_position_tier": "sample_red_carpet_position_tier",
  "press_room_interview_quota": 1,
  "pool_broadcaster_status": true,
  "compliance_clearance_status": "sample_compliance_clearance_status"
}
```

---

## 7. `telecast_broadcasters`

- **Collection Name**: `telecast_broadcasters`
- **Entity Represented**: `BroadcastNetworkProfile`
- **Purpose**: Media broadcast networks and transmission standards
- **Expected Feasibility Count**: 50+ network contract periods and feeds
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`broadcaster_id`).
- **Domain Key**: `broadcaster_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `broadcast_id`, `ceremony_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Nielsen Media / Broadcaster Press Logs
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (broadcast_id) |
| `broadcast_id` | `string` | YES | Domain attribute: broadcast_id |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `network_name` | `string` | YES | Domain attribute: network_name |
| `country_code` | `string` | YES | Domain attribute: country_code |
| `broadcast_start_time_utc` | `string` | YES | Domain attribute: broadcast_start_time_utc |
| `scheduled_duration_minutes` | `int` | YES | Domain attribute: scheduled_duration_minutes |
| `executive_producer` | `string` | YES | Domain attribute: executive_producer |
| `director_name` | `string` | YES | Domain attribute: director_name |
| `parental_advisory_rating` | `string` | YES | Domain attribute: parental_advisory_rating |
| `hd_4k_feed_enabled` | `bool` | YES | Domain attribute: hd_4k_feed_enabled |

### Document Structure Example
```json
{
  "_id": "TELECAST_BROADCASTERS_001",
  "broadcast_id": "sample_broadcast_id",
  "ceremony_id": "sample_ceremony_id",
  "network_name": "sample_network_name",
  "country_code": "sample_country_code",
  "broadcast_start_time_utc": "sample_broadcast_start_time_utc",
  "scheduled_duration_minutes": 1,
  "executive_producer": "sample_executive_producer",
  "director_name": "sample_director_name",
  "parental_advisory_rating": "sample_parental_advisory_rating",
  "hd_4k_feed_enabled": true,
  "broadcaster_id": "TELECAST_BROADCASTERS_001"
}
```

---

## 8. `timeline_historical_eras`

- **Collection Name**: `timeline_historical_eras`
- **Entity Represented**: `HistoricalEraPeriod`
- **Purpose**: Chronological epochs across 6 decades of popular music
- **Expected Feasibility Count**: 50+ era subdivisions and musical waves
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`era_id`).
- **Domain Key**: `era_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `era_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Musicological Era Classifications / Academy Archives
- **Data Classification Tier**: `DERIVED DATA`
- **Derived-Data Indicator**: `YES`
- **Derivation Logic**: Computed via aggregation pipeline across core source data during ETL.

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (era_id) |
| `era_id` | `string` | YES | Domain attribute: era_id |
| `era_name` | `string` | YES | Domain attribute: era_name |
| `start_calendar_year` | `int` | YES | Domain attribute: start_calendar_year |
| `end_calendar_year` | `int` | YES | Domain attribute: end_calendar_year |
| `dominant_audio_format` | `string` | YES | Domain attribute: dominant_audio_format |
| `voting_tabulation_method` | `string` | YES | Domain attribute: voting_tabulation_method |
| `predominant_music_genre` | `string` | YES | Domain attribute: predominant_music_genre |
| `total_ceremonies_contained` | `int` | YES | Domain attribute: total_ceremonies_contained |
| `headquarters_city` | `string` | YES | Domain attribute: headquarters_city |
| `industry_paradigm_shift_notes` | `string` | YES | Domain attribute: industry_paradigm_shift_notes |

### Document Structure Example
```json
{
  "_id": "TIMELINE_HISTORICAL_ERAS_001",
  "era_id": "TIMELINE_HISTORICAL_ERAS_001",
  "era_name": "sample_era_name",
  "start_calendar_year": 1,
  "end_calendar_year": 1,
  "dominant_audio_format": "sample_dominant_audio_format",
  "voting_tabulation_method": "sample_voting_tabulation_method",
  "predominant_music_genre": "sample_predominant_music_genre",
  "total_ceremonies_contained": 1,
  "headquarters_city": "sample_headquarters_city",
  "industry_paradigm_shift_notes": "sample_industry_paradigm_shift_notes"
}
```

---

## 9. `venues`

- **Collection Name**: `venues`
- **Entity Represented**: `CeremonyVenue`
- **Purpose**: Geographic and architectural profiles of arenas and halls
- **Expected Feasibility Count**: 60+ venues and pavilions
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`venue_id`).
- **Domain Key**: `venue_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `venue_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Recording Academy Event Archives / Wikidata
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (venue_id) |
| `venue_id` | `string` | YES | Domain attribute: venue_id |
| `venue_name` | `string` | YES | Domain attribute: venue_name |
| `venue_type` | `string` | YES | Domain attribute: venue_type |
| `street_address` | `string` | YES | Domain attribute: street_address |
| `city` | `string` | YES | Domain attribute: city |
| `state` | `string` | YES | Domain attribute: state |
| `postal_code` | `string` | YES | Domain attribute: postal_code |
| `max_seating_capacity` | `int` | YES | Domain attribute: max_seating_capacity |
| `first_hosted_year` | `int` | YES | Domain attribute: first_hosted_year |
| `total_ceremonies_hosted` | `int` | YES | Domain attribute: total_ceremonies_hosted |

### Document Structure Example
```json
{
  "_id": "VENUES_001",
  "venue_id": "VENUES_001",
  "venue_name": "sample_venue_name",
  "venue_type": "sample_venue_type",
  "street_address": "sample_street_address",
  "city": "sample_city",
  "state": "sample_state",
  "postal_code": "sample_postal_code",
  "max_seating_capacity": 1,
  "first_hosted_year": 1,
  "total_ceremonies_hosted": 1
}
```

---

## 10. `viewership_ratings`

- **Collection Name**: `viewership_ratings`
- **Entity Represented**: `CeremonyViewershipMetric`
- **Purpose**: Longitudinal Nielsen ratings and audience metrics
- **Expected Feasibility Count**: 55+ televised ceremonies
- **Feasibility Audit Status**: Verified `FEASIBLE_VERIFIED` ($\ge 50$ docs, $\ge 10$ fields)

### Identifier Specification
- **Primary BSON Identifier (`_id`)**: String format matching domain identifier (`rating_id`).
- **Domain Key**: `rating_id` (Unique constraint enforced).

### References & Relationships
- **Outbound References**: `ceremony_id`, `rating_id`

### Embedded Documents & Arrays
- **Embedded Subdocuments**: None (Flat entity structure).
- **Arrays**: None.

### Provenance & Data Tier
- **Source Provenance**: Nielsen Media Research Historical Archives
- **Data Classification Tier**: `SOURCE DATA`
- **Derived-Data Indicator**: `NO`

### Field Specifications (11 Defined Fields)

| Field Name | BSON Type | Required? | Description |
| :--- | :---: | :---: | :--- |
| `_id` | `string` | YES | Unique primary BSON document identifier (rating_id) |
| `rating_id` | `string` | YES | Domain attribute: rating_id |
| `ceremony_id` | `string` | YES | Domain attribute: ceremony_id |
| `us_viewers_millions` | `double` | YES | Domain attribute: us_viewers_millions |
| `household_rating_pct` | `double` | YES | Domain attribute: household_rating_pct |
| `household_share_pct` | `double` | YES | Domain attribute: household_share_pct |
| `demo_18_49_rating` | `double` | YES | Domain attribute: demo_18_49_rating |
| `peak_viewers_millions` | `double` | YES | Domain attribute: peak_viewers_millions |
| `peak_broadcast_segment` | `string` | YES | Domain attribute: peak_broadcast_segment |
| `digital_streaming_views_millions` | `double` | YES | Domain attribute: digital_streaming_views_millions |
| `measurement_agency` | `string` | YES | Domain attribute: measurement_agency |

### Document Structure Example
```json
{
  "_id": "VIEWERSHIP_RATINGS_001",
  "rating_id": "VIEWERSHIP_RATINGS_001",
  "ceremony_id": "sample_ceremony_id",
  "us_viewers_millions": 100.0,
  "household_rating_pct": 100.0,
  "household_share_pct": 100.0,
  "demo_18_49_rating": 100.0,
  "peak_viewers_millions": 100.0,
  "peak_broadcast_segment": "sample_peak_broadcast_segment",
  "digital_streaming_views_millions": 100.0,
  "measurement_agency": "sample_measurement_agency"
}
```

---
