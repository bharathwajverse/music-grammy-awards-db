# Complete Data Dictionary: 50 Collections (10 per Database)

This document specifies the exact schema requirements for all 50 collections across the five member databases. Every collection contains a minimum of 10 meaningful, typed domain attributes and will hold at least 50 authentic documents.

---

# 1. Database: `grammy_history_db` (Member 1)

### 1.1 `ceremonies`
| Field | Type | Description |
| :--- | :--- | :--- |
| `ceremony_id` | String | Unique primary identifier (e.g., `CEREMONY_065`) |
| `edition_number` | Integer | Annual edition number (1 to 67) |
| `ceremony_date` | String | ISO-8601 calendar date of the telecast (YYYY-MM-DD) |
| `broadcast_year` | Integer | Calendar year of broadcast |
| `eligibility_period_start` | String | Start date of eligible recording release window |
| `eligibility_period_end` | String | End date of eligible recording release window |
| `host_city` | String | Metropolitan city hosting the ceremony |
| `venue_id` | String | Foreign reference to `venues.venue_id` |
| `primary_network` | String | Telecast network (CBS, NBC, ABC) |
| `total_awards_presented` | Integer | Total number of awards handed out across all fields |
| `created_at` | String | Record creation timestamp |

### 1.2 `venues`
| Field | Type | Description |
| :--- | :--- | :--- |
| `venue_id` | String | Unique venue code (e.g., `VEN_CRYPTO_LA`) |
| `venue_name` | String | Official commercial or historic name of the venue |
| `venue_type` | String | Type of venue (Arena, Theater, Auditorium, Hotel) |
| `street_address` | String | Physical postal address |
| `city` | String | City location |
| `state` | String | State / territory |
| `postal_code` | String | ZIP / postal code |
| `max_seating_capacity` | Integer | Maximum attendance capacity |
| `first_hosted_year` | Integer | Earliest year hosting a GRAMMY ceremony |
| `total_ceremonies_hosted` | Integer | Total count of ceremonies held at this location |

### 1.3 `telecast_broadcasters`
| Field | Type | Description |
| :--- | :--- | :--- |
| `broadcast_id` | String | Unique telecast contract identifier |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `network_name` | String | Primary domestic broadcast network |
| `country_code` | String | ISO country code of principal broadcast (e.g., US) |
| `broadcast_start_time_utc` | String | UTC broadcast commencement time |
| `scheduled_duration_minutes` | Integer | Programmed runtime in minutes |
| `executive_producer` | String | Lead executive producer (e.g., Ken Ehrlich, Ben Winston) |
| `director_name` | String | Television director of live broadcast |
| `parental_advisory_rating` | String | TV Parental Guidelines rating (e.g., TV-14-DL) |
| `hd_4k_feed_enabled` | Boolean | True if high-definition/UHD 4K broadcast feed available |

### 1.4 `viewership_ratings`
| Field | Type | Description |
| :--- | :--- | :--- |
| `rating_id` | String | Unique rating ledger ID |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `us_viewers_millions` | Double | Total average US television audience in millions |
| `household_rating_pct` | Double | Nielsen household rating percentage |
| `household_share_pct` | Double | Nielsen percentage of television sets in use |
| `demo_18_49_rating` | Double | Demographic rating for age group 18–49 |
| `peak_viewers_millions` | Double | Peak instantaneous viewer audience in millions |
| `peak_broadcast_segment` | String | Performance or award segment delivering peak viewers |
| `digital_streaming_views_millions`| Double | Paramount+/CBS digital streaming audience |
| `measurement_agency` | String | Source auditing company (Nielsen Media Research) |

### 1.5 `ceremony_hosts`
| Field | Type | Description |
| :--- | :--- | :--- |
| `host_assignment_id` | String | Unique host record ID |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `creator_id` | String | Foreign reference to `artists.artist_id` |
| `host_full_name` | String | Full professional billing name of host |
| `hosting_style` | String | Primary performance medium (Comedian, Recording Artist, Actor) |
| `solo_or_duo` | String | Hosting format (Solo, Duo, Ensemble) |
| `host_sequence_count` | Integer | Cumulative times this host has anchored the telecast |
| `monologue_duration_seconds`| Integer | Duration of opening monologue in seconds |
| `emmy_nomination_received` | Boolean | Indicates if telecast received an Emmy nomination for hosting |
| `contracted_talent_agency` | String | Representing talent agency (CAA, WME, UTA) |

### 1.6 `historic_milestones`
| Field | Type | Description |
| :--- | :--- | :--- |
| `milestone_id` | String | Unique milestone identifier |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `milestone_title` | String | Descriptive title of historic occurrence |
| `calendar_year` | Integer | Calendar year of event |
| `primary_subject_creator_id` | String | Primary artist or leader involved |
| `cultural_significance_summary` | String | Academic commentary on industry impact |
| `official_academy_recognition` | Boolean | Officially highlighted in Academy archives |
| `controversy_flag` | Boolean | Flag indicating historical controversy or protest |
| `archival_video_reel_id` | String | Academy audio-visual archive catalog code |
| `citation_source_url` | String | Verifiable reference link |

### 1.7 `academy_leadership`
| Field | Type | Description |
| :--- | :--- | :--- |
| `leadership_id` | String | Unique officer tenure identifier |
| `officer_name` | String | Name of executive officer |
| `executive_role_title` | String | Title (President, CEO, Chairman of Board of Trustees) |
| `tenure_start_year` | Integer | Commencement year of administration |
| `tenure_end_year` | Integer | Conclusion year of administration (null if active) |
| `professional_music_background` | String | Previous industry career role |
| `trustee_chapter_location` | String | Regional Academy Chapter (Los Angeles, New York, Nashville) |
| `notable_policy_amendment` | String | Major voting or structural reform enacted |
| `board_voting_privileges` | Boolean | Whether officer holds a vote on the Board of Trustees |
| `appointed_by` | String | Governing body appointing executive |

### 1.8 `lifetime_achievement_honors`
| Field | Type | Description |
| :--- | :--- | :--- |
| `honor_id` | String | Unique Special Merit honor ID |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `recipient_creator_id` | String | Foreign reference to `artists.artist_id` |
| `honor_type` | String | Merit category (Lifetime Achievement, Trustees Award) |
| `announcement_year` | Integer | Year award was conferred |
| `career_span_decades` | Integer | Length of active career in decades |
| `presenting_dignitary_name` | String | Individual presenting the award medallion |
| `citation_text` | String | Official Academy citation read at ceremony |
| `is_posthumous_award` | Boolean | Whether award was conferred posthumously |
| `special_tribute_performance_flag` | Boolean | Whether honored with an all-star musical tribute |

### 1.9 `timeline_historical_eras`
| Field | Type | Description |
| :--- | :--- | :--- |
| `era_id` | String | Unique era code (e.g., `ERA_VINYL_ERA`) |
| `era_name` | String | Formal era name (Golden Age, Vinyl Era, Digital Streaming) |
| `start_calendar_year` | Integer | Starting year of historical era |
| `end_calendar_year` | Integer | Concluding year of historical era |
| `dominant_audio_format` | String | Industry standard recording medium (Vinyl LP, CD, MP3, Streams) |
| `voting_tabulation_method` | String | Paper Ballot, Scantron, Online Member Portal |
| `predominant_music_genre` | String | Leading commercial genre of the era |
| `total_ceremonies_contained` | Integer | Number of annual presentations in era |
| `headquarters_city` | String | Location of national Academy headquarters |
| `industry_paradigm_shift_notes`| String | Historical context on market transition |

### 1.10 `press_media_accreditations`
| Field | Type | Description |
| :--- | :--- | :--- |
| `accreditation_id` | String | Unique media credential code |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `media_organization_name` | String | News outlet or network (Rolling Stone, Billboard, AP) |
| `media_channel_type` | String | Outlet format (Print, Broadcast TV, Digital, Radio) |
| `origin_country` | String | Country of publication |
| `passes_granted_count` | Integer | Total credential badges issued |
| `red_carpet_position_tier` | String | Red carpet placement ranking (Tier 1, Tier 2, Pool) |
| `press_room_interview_quota` | Integer | Allotted backstage media room interviews |
| `pool_broadcaster_status` | Boolean | Authorized pool camera operator |
| `compliance_clearance_status` | String | Status of background security clearance |

---

# 2. Database: `grammy_categories_db` (Member 2)

### 2.1 `award_fields`
| Field | Type | Description |
| :--- | :--- | :--- |
| `field_id` | String | Unique field code (e.g., `FLD_POP`) |
| `field_name` | String | Full formal name (General Field, Pop, Rock, Classical) |
| `field_abbreviation` | String | Short code |
| `field_description` | String | Academy definition of genre boundaries |
| `inaugural_ceremony_edition` | Integer | First edition incorporating this genre field |
| `current_active_status` | Boolean | True if categories are actively awarded |
| `active_categories_count` | Integer | Total categories belonging to field currently |
| `specialist_committee_jurisdiction` | String | Name of screening committee governing field |
| `field_curator_role` | String | Academy oversight trustee position |
| `last_bylaw_revision_year` | Integer | Year of most recent definition update |

### 2.2 `award_categories`
| Field | Type | Description |
| :--- | :--- | :--- |
| `category_id` | String | Unique primary category key (e.g., `CAT_AOTY`) |
| `field_id` | String | Foreign reference to `award_fields.field_id` |
| `official_category_name` | String | Full name (Album of the Year) |
| `standard_short_code` | String | Abbreviation (AOTY) |
| `inaugural_edition` | Integer | First ceremony edition awarded |
| `is_general_field` | Boolean | True if open to all voting members regardless of craft |
| `current_status` | String | Status (Active, Retired, Merged, Renamed) |
| `maximum_nominees_allowed` | Integer | Nominee slate cap (e.g., 5, 8, or 10) |
| `voting_tier_access` | String | All Voting Members vs Craft Specialists Only |
| `trophy_statuette_eligibility_rule` | String | Rule dictating statuette eligibility for collaborators |
| `entry_fee_tier` | String | Standard OEP submission fee tier |

### 2.3 `category_lineage`
| Field | Type | Description |
| :--- | :--- | :--- |
| `lineage_id` | String | Unique lineage entry identifier |
| `category_id` | String | Foreign reference to `award_categories.category_id` |
| `predecessor_category_name` | String | Previous name or parent category |
| `successor_category_name` | String | Updated name or split category |
| `effective_ceremony_edition` | Integer | Edition in which transformation took effect |
| `transition_classification` | String | Renamed, Split, Merged, Restructured |
| `structural_rationale` | String | Justification given in Board of Trustees minutes |
| `nominee_slate_impact_count` | Integer | Change in available nominee slots |
| `trustee_resolution_reference` | String | Reference number of official resolution |
| `ballot_clarification_bulletin` | String | Guidance note sent to voting members |

### 2.4 `eligibility_rules`
| Field | Type | Description |
| :--- | :--- | :--- |
| `rule_id` | String | Unique rule specification ID |
| `category_id` | String | Foreign reference to `award_categories.category_id` |
| `effective_edition` | Integer | Ceremony edition this rule version applies to |
| `minimum_playing_time_minutes` | Double | Minimum album playing time (e.g., 15.0 or 30.0 mins) |
| `minimum_track_count` | Integer | Minimum distinct tracks required (e.g., 5 tracks) |
| `featured_performance_threshold_pct` | Double | Percentage of album featuring primary artist |
| `us_release_commercial_requirement` | Boolean | Commercial availability required in the US market |
| `language_composition_restrictions` | String | Specific language percentage rules (e.g., Latin) |
| `sample_replay_clearance_rule` | String | Guidelines on interpolation and copyrighted samples |
| `entry_window_months` | Integer | Length of commercial release window in months |

### 2.5 `voting_procedures`
| Field | Type | Description |
| :--- | :--- | :--- |
| `procedure_id` | String | Unique procedure code |
| `category_id` | String | Foreign reference to `award_categories.category_id` |
| `voting_round_number` | Integer | First Round (Nominations) vs Final Round (Winners) |
| `electorate_body_type` | String | General Membership vs Nomination Review Committee |
| `is_ranked_choice_ballot` | Boolean | Whether preferential/ranked-choice voting is used |
| `craft_committee_review_required`| Boolean | True if subject to craft screening panel |
| `committee_member_roster_count` | Integer | Number of screening committee members |
| `nomination_slot_capacity` | Integer | Number of voting selections permitted per member |
| `tie_breaking_protocol` | String | Bylaw rule invoked in event of identical votes |
| `auditing_firm_signoff_flag` | Boolean | Verification status from independent accounting firm |

### 2.6 `discontinued_categories`
| Field | Type | Description |
| :--- | :--- | :--- |
| `discontinued_id` | String | Unique retired category ID |
| `category_name` | String | Historic name of discontinued award |
| `final_active_ceremony_edition` | Integer | Last ceremony year award was presented |
| `cumulative_years_active` | Integer | Total years category was on the ballot |
| `retirement_rationale` | String | Rationale (Genre obsolescence, category consolidation) |
| `merged_into_category_id` | String | Category receiving legacy submissions (if any) |
| `total_winners_awarded` | Integer | All-time winner count |
| `total_nominations_recorded` | Integer | All-time nomination count |
| `historic_significance_tag` | String | Cultural importance descriptor |
| `archive_vault_reference` | String | Archival file identifier |

### 2.7 `category_quotas_limits`
| Field | Type | Description |
| :--- | :--- | :--- |
| `quota_id` | String | Unique quota specification code |
| `category_id` | String | Foreign reference to `award_categories.category_id` |
| `ceremony_edition` | Integer | Applicable ceremony edition |
| `standard_nominee_limit` | Integer | Default nominee slate capacity |
| `emergency_tie_allowance` | Integer | Maximum extra nominees admitted due to ties |
| `max_credited_producers_eligible` | Integer | Cap on statuettes for producers on an entry |
| `max_credited_engineers_eligible` | Integer | Cap on statuettes for sound engineers |
| `playing_time_contribution_threshold_pct` | Double | Minimum playing time % for producer eligibility (33% rule) |
| `lyricist_track_threshold_pct` | Double | Minimum contribution % for songwriter eligibility |
| `pro_rata_trophy_rule` | String | Policy regarding replacement and purchase of extra trophies |

### 2.8 `special_merit_categories`
| Field | Type | Description |
| :--- | :--- | :--- |
| `special_merit_id` | String | Unique special merit category code |
| `award_title` | String | Name of honor (Trustees Award, Technical GRAMMY) |
| `conferral_frequency` | String | Frequency (Annual, Discretionary, Triennial) |
| `governing_board_supermajority_pct` | Double | Required vote percentage of Board of Trustees (e.g., 66.7%) |
| `candidate_selection_protocol` | String | Vetting process description |
| `trophy_or_plaque_type` | String | Physical artifact type (Gramophone Statuette, Plaque, Medallion) |
| `first_conferred_year` | Integer | Inception year |
| `target_industry_discipline` | String | Eligible discipline (Engineering, Philanthropy, Performance) |
| `peer_nomination_permitted` | Boolean | True if general voting members may submit candidates |
| `ceremony_segment_placement` | String | Presentation placement (Special Merit Ceremony, Prime-time Broadcast) |

### 2.9 `craft_credit_definitions`
| Field | Type | Description |
| :--- | :--- | :--- |
| `craft_def_id` | String | Unique craft definition key |
| `category_id` | String | Foreign reference to `award_categories.category_id` |
| `craft_role_name` | String | Role name (Mastering Engineer, Mixer, Vocal Arranger) |
| `mandatory_statuette_recipient` | Boolean | Entitled to official golden gramophone statuette |
| `certificate_of_merit_alternative`| Boolean | Awarded official Certificate of Participation |
| `audio_stem_mastering_threshold` | Double | Contribution threshold required for stem engineers |
| `assistant_engineer_eligibility` | Boolean | Eligibility policy for assistant/tape engineers |
| `sample_creator_eligibility` | Boolean | Eligibility policy for writers of sampled compositions |
| `documentation_proof_standard` | String | Evidence required (Union contract, liner notes, DAW session log) |
| `union_credit_registry_crosscheck` | String | Registry checked (AFM, SAG-AFTRA) |

### 2.10 `merged_split_history`
| Field | Type | Description |
| :--- | :--- | :--- |
| `event_id` | String | Unique restructuring event ID |
| `restructuring_type` | String | Event type (Merger, Split, Elimination, Rebrand) |
| `effective_year` | Integer | Calendar year of execution |
| `primary_category_id` | String | Foreign reference to `award_categories.category_id` |
| `source_category_ids` | Array of String | Pre-existing category IDs folded into new structure |
| `consolidation_justification` | String | Official explanation published by Recording Academy |
| `gender_neutral_reform_flag` | Boolean | True if part of 2012 gender-neutral category overhaul |
| `member_feedback_period_days` | Integer | Duration of public/member consultation period |
| `trustee_vote_tally` | String | Board voting outcome record |
| `published_press_bulletin_id` | String | Press bulletin reference code |

---

# 3. Database: `grammy_nominations_db` (Member 3)

### 3.1 `nomination_entries`
| Field | Type | Description |
| :--- | :--- | :--- |
| `nomination_id` | String | Deterministic primary key (e.g., `NOM_065_AOTY_01`) |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `category_id` | String | Foreign reference to `award_categories.category_id` |
| `work_id` | String | Foreign reference to `nominated_works.work_id` |
| `nomination_year` | Integer | Year of ceremony presentation |
| `entry_billing_title` | String | Nominated work title as printed on official ballot |
| `primary_artist_id` | String | Foreign reference to `artists.artist_id` |
| `is_winner_flag` | Boolean | True if this entry won the GRAMMY |
| `ballot_slot_order` | Integer | Alphabetical or randomized position on voting ballot |
| `auditor_validation_code` | String | Cryptographic signoff token from tabulation auditor |
| `created_timestamp` | String | Record creation timestamp |

### 3.2 `nominated_works`
| Field | Type | Description |
| :--- | :--- | :--- |
| `work_id` | String | Unique musical work code (e.g., `WRK_RENAISSANCE_2022`) |
| `work_type` | String | Type of work (Album, Track, Song, Box Set, Video) |
| `work_title` | String | Official commercial title of release |
| `commercial_release_date` | String | Date commercially made available to the public |
| `primary_label_id` | String | Foreign reference to `record_labels.label_id` |
| `isrc_code` | String | International Standard Recording Code |
| `upc_barcode` | String | Universal Product Code barcode |
| `duration_total_seconds` | Integer | Total audio playing time in seconds |
| `track_count` | Integer | Total tracks on release |
| `parental_advisory_flag` | Boolean | RIAA Parental Advisory Explicit Content indicator |
| `language_iso_code` | String | Primary language code (ISO 639-1) |

### 3.3 `nomination_credits`
| Field | Type | Description |
| :--- | :--- | :--- |
| `credit_id` | String | Unique credit attribution ID |
| `nomination_id` | String | Foreign reference to `nomination_entries.nomination_id` |
| `creator_id` | String | Foreign reference to `artists.artist_id` / `creators` |
| `credit_role` | String | Credited role (Artist, Producer, Engineer, Songwriter) |
| `credit_billing_rank` | Integer | Billing order on liner notes |
| `work_contribution_summary` | String | Specific contribution (Lead Vocals, Synthesizer, Mixing) |
| `contribution_percentage` | Double | Pro-rata percentage of album or track |
| `is_lead_performer` | Boolean | True if billed as lead recording artist |
| `is_producer_credit` | Boolean | True if credited as producer |
| `academy_verified_status` | Boolean | Formally verified by Academy Credit Research Department |

### 3.4 `submission_batches`
| Field | Type | Description |
| :--- | :--- | :--- |
| `batch_id` | String | Unique Online Entry Process (OEP) batch code |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `submitting_label_id` | String | Foreign reference to `record_labels.label_id` |
| `submission_timestamp` | String | Timestamp submission was finalized in OEP |
| `total_entries_count` | Integer | Total entries submitted in batch |
| `entry_fee_total_usd` | Double | Total submission fees invoiced |
| `compliance_officer_name` | String | Label authorized representative submitting entries |
| `first_round_accepted_count` | Integer | Entries passing initial eligibility review |
| `disqualified_entries_count` | Integer | Entries rejected for release date or rule violations |
| `payment_reconciliation_hash` | String | Financial payment transaction hash |

### 3.5 `genre_classifications`
| Field | Type | Description |
| :--- | :--- | :--- |
| `classification_id` | String | Unique classification review ID |
| `work_id` | String | Foreign reference to `nominated_works.work_id` |
| `submitted_field_id` | String | Genre field requested by submitting label |
| `assigned_field_id` | String | Genre field determined by screening committee |
| `primary_genre_tag` | String | Primary musical style descriptor |
| `secondary_genre_tags` | Array of String | Sub-genres and stylistic elements |
| `screening_committee_consensus`| String | Committee determination status (Unanimous, Majority, Split) |
| `contested_by_label_flag` | Boolean | True if record company filed formal appeal |
| `reclassification_justification`| String | Explanation for shifting genre placement |
| `determination_date` | String | Date decision was ratified |

### 3.6 `first_time_nominees`
| Field | Type | Description |
| :--- | :--- | :--- |
| `first_nom_id` | String | Unique debut nominee record code |
| `nomination_id` | String | Foreign reference to `nomination_entries.nomination_id` |
| `creator_id` | String | Foreign reference to `artists.artist_id` |
| `debut_ceremony_edition` | Integer | Ceremony edition of debut nomination |
| `breakout_work_id` | String | Work garnering the first nomination |
| `best_new_artist_nominated` | Boolean | True if also nominated for Best New Artist that year |
| `age_at_debut_nomination` | Integer | Age of creator when first nominated |
| `prior_uncredited_appearances` | Integer | Prior career appearances without official billing |
| `commercial_breakout_tier` | String | Streaming/Sales commercial profile level |
| `career_inception_year` | Integer | Year of earliest commercial release |

### 3.7 `tied_nominations`
| Field | Type | Description |
| :--- | :--- | :--- |
| `tie_id` | String | Unique tie incident ID |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `category_id` | String | Foreign reference to `award_categories.category_id` |
| `tied_nomination_ids` | Array of String | Nomination IDs receiving equal vote tallies |
| `tied_vote_count_audited` | Integer | Audited vote total producing tie |
| `ballot_auditor_token` | String | Auditor verification code |
| `board_tie_waiver_approved` | Boolean | Board of Trustees ratification of slate expansion |
| `expanded_slate_size` | Integer | Resulting total nominees on final ballot (e.g., 6 or 9) |
| `adjudication_timestamp` | String | Timestamp tie was resolved |
| `bylaw_clause_reference` | String | Relevant rulebook section cited |

### 3.8 `multi_nomination_packages`
| Field | Type | Description |
| :--- | :--- | :--- |
| `package_id` | String | Unique multi-nominee aggregation ID |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `creator_id` | String | Foreign reference to `artists.artist_id` |
| `total_nominations_count` | Integer | Total nominations accumulated in that ceremony |
| `general_field_nominations_count` | Integer | Nominations in Big Four categories |
| `genre_field_nominations_count` | Integer | Nominations in craft and genre categories |
| `leading_nominee_rank` | Integer | Rank among all nominees for that year (e.g., #1 most nominated) |
| `nominated_work_ids` | Array of String | List of works contributing to nomination tally |
| `public_announcement_tier` | String | Announcement order in live telecast nomination reveal |
| `ceremony_year` | Integer | Calendar year of ceremony |

### 3.9 `voter_screening_batches`
| Field | Type | Description |
| :--- | :--- | :--- |
| `screening_batch_id` | String | Unique screening session code |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `field_id` | String | Foreign reference to `award_fields.field_id` |
| `panel_chair_creator_id` | String | Chair of screening committee |
| `session_start_timestamp` | String | Meeting commencement timestamp |
| `session_end_timestamp` | String | Meeting adjournment timestamp |
| `works_screened_count` | Integer | Number of entries reviewed for craft adherence |
| `disqualifications_ordered` | Integer | Number of recordings disqualified |
| `quorum_certified` | Boolean | True if legal attendance quorum was met |
| `panel_confidentiality_hash` | String | Cryptographic verification of member NDAs |

### 3.10 `nomination_audit_logs`
| Field | Type | Description |
| :--- | :--- | :--- |
| `audit_id` | String | Unique vote verification audit entry |
| `nomination_id` | String | Foreign reference to `nomination_entries.nomination_id` |
| `auditing_firm_id` | String | Accounting agency (Deloitte, PwC) |
| `lead_auditor_name` | String | Partner responsible for vote tabulation |
| `audit_timestamp` | String | Timestamp tabulation was sealed |
| `digital_signature_hash` | String | SHA-256 digital signature of ballot tally |
| `tabulation_vault_partition` | String | Secure server partition reference |
| `discrepancy_check_passed` | Boolean | Reconciled against raw electronic voting records |
| `recount_required_flag` | Boolean | Indicates if statistical recount was executed |
| `compliance_certificate_code` | String | Official certificate number |

---

# 4. Database: `grammy_winners_db` (Member 4)

### 4.1 `winner_records`
| Field | Type | Description |
| :--- | :--- | :--- |
| `winner_record_id` | String | Unique primary winner identifier (e.g., `WIN_NOM_065_AOTY_01`) |
| `nomination_id` | String | Foreign reference to `nomination_entries.nomination_id` |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `category_id` | String | Foreign reference to `award_categories.category_id` |
| `winning_work_id` | String | Foreign reference to `nominated_works.work_id` |
| `primary_artist_id` | String | Foreign reference to `artists.artist_id` |
| `broadcast_presentation_order` | Integer | Sequential order presented during telecast or premiere ceremony |
| `presented_live_on_telecast` | Boolean | True if presented on prime-time CBS broadcast |
| `acceptance_speech_delivered` | Boolean | True if recipient was present to give remarks |
| `trophy_statuettes_awarded_count`| Integer | Total statuettes physically awarded for this entry |
| `verified_timestamp` | String | Time entry was certified as winner |

### 4.2 `big_four_sweeps`
| Field | Type | Description |
| :--- | :--- | :--- |
| `sweep_id` | String | Unique sweep record key |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `creator_id` | String | Foreign reference to `artists.artist_id` |
| `sweep_achievement_type` | String | Full Sweep (All 4), Clean Sweep, Triple Crown |
| `aoty_nomination_id` | String | Album of the Year nomination reference |
| `roty_nomination_id` | String | Record of the Year nomination reference |
| `soty_nomination_id` | String | Song of the Year nomination reference |
| `bna_nomination_id` | String | Best New Artist nomination reference |
| `sweep_calendar_year` | Integer | Year of achievement |
| `career_significance_rating` | String | Historical analysis classification |

### 4.3 `record_breakers`
| Field | Type | Description |
| :--- | :--- | :--- |
| `record_id` | String | Unique historical record entry |
| `winner_record_id` | String | Foreign reference to `winner_records.winner_record_id` |
| `creator_id` | String | Foreign reference to `artists.artist_id` |
| `record_metric_name` | String | Description of record (Most Lifetime Wins, Youngest AOTY Winner) |
| `previous_record_holder_name` | String | Prior historical benchmark holder |
| `previous_record_value` | Double | Numeric quantity of previous record |
| `new_record_value` | Double | Numeric quantity of newly established record |
| `record_establishment_year` | Integer | Year record was broken |
| `creator_age_at_record` | Double | Exact age of artist when achieving record |
| `academy_verified_announcement_url`| String | Official press release link |

### 4.4 `acceptance_speeches`
| Field | Type | Description |
| :--- | :--- | :--- |
| `speech_id` | String | Unique speech transcript record |
| `winner_record_id` | String | Foreign reference to `winner_records.winner_record_id` |
| `primary_speaker_creator_id` | String | Foreign reference to `artists.artist_id` |
| `speech_duration_seconds` | Integer | Time taken for speech in seconds |
| `playoff_music_interrupted` | Boolean | True if exit music began playing during remarks |
| `primary_quote_transcript` | String | Key excerpt of remarks |
| `individuals_acknowledged` | Array of String | Collaborators, family, or executives thanked |
| `social_political_message_flag` | Boolean | Highlights advocacy or social causes addressed |
| `press_room_followup_id` | String | Backstage interview transcript reference |
| `broadcast_clip_timecode` | String | Video archive timestamp |

### 4.5 `trophy_tracking`
| Field | Type | Description |
| :--- | :--- | :--- |
| `trophy_id` | String | Unique physical statuette serial code |
| `winner_record_id` | String | Foreign reference to `winner_records.winner_record_id` |
| `recipient_creator_id` | String | Creator receiving this individual statuette |
| `statuette_serial_number` | String | Laser-engraved inventory number |
| `engraved_billing_text` | String | Full multi-line text engraved on brass nameplate |
| `manufacturing_foundry_name` | String | Foundry crafting trophy (Billings Artworks, Ridgeway CO) |
| `grammium_alloy_specification` | String | Proprietary zinc-aluminum alloy formula code |
| `gold_plating_thickness_microns`| Double | Thickness of 24k gold plating |
| `dispatch_shipment_date` | String | Date statuette was shipped following post-show engraving |
| `custody_receipt_hash` | String | Signed delivery confirmation hash |

### 4.6 `consecutive_winners`
| Field | Type | Description |
| :--- | :--- | :--- |
| `streak_id` | String | Unique winning streak ID |
| `creator_id` | String | Foreign reference to `artists.artist_id` |
| `category_id` | String | Foreign reference to `award_categories.category_id` |
| `streak_span_years` | Integer | Number of consecutive ceremonies won |
| `initial_ceremony_edition` | Integer | First ceremony edition of streak |
| `terminal_ceremony_edition` | Integer | Concluding ceremony edition of streak |
| `winning_work_ids_list` | Array of String | List of works winning during streak |
| `is_streak_currently_active` | Boolean | Indicates if streak is unbroken |
| `historical_streak_rank` | Integer | All-time rank for streak length |
| `category_monopoly_notes` | String | Historical analysis of streak |

### 4.7 `posthumous_awards`
| Field | Type | Description |
| :--- | :--- | :--- |
| `posthumous_id` | String | Unique posthumous award record |
| `winner_record_id` | String | Foreign reference to `winner_records.winner_record_id` |
| `deceased_creator_id` | String | Foreign reference to `artists.artist_id` |
| `date_of_passing` | String | Date of artist death |
| `award_ceremony_date` | String | Date award was presented |
| `accepted_by_representative` | String | Family member, bandmate, or estate executor accepting |
| `representative_legal_relationship`| String | Relationship (Spouse, Child, Estate Trustee) |
| `in_memoriam_segment_aired` | Boolean | Featured in broadcast In Memoriam montage |
| `estate_concurrence_status` | String | Formal estate acceptance confirmation |
| `tribute_performance_id` | String | Telecast musical tribute ID |

### 4.8 `historic_win_benchmarks`
| Field | Type | Description |
| :--- | :--- | :--- |
| `benchmark_id` | String | Unique institutional benchmark ID |
| `benchmark_title` | String | Milestone title (e.g., 20+ Grammy Wins, 3-time AOTY Winner) |
| `qualifying_win_threshold` | Integer | Number of wins required to qualify |
| `total_qualifying_creators` | Integer | Total artists attaining threshold in history |
| `pioneering_creator_id` | String | First person to reach milestone |
| `year_threshold_first_achieved` | Integer | Year benchmark was inaugurated |
| `most_recent_qualifier_id` | String | Most recent artist to cross milestone |
| `egot_component_flag` | Boolean | Component of prestigious EGOT grand slam |
| `rarity_index_score` | Double | Statistical rarity metric (0.0 to 100.0) |
| `hall_of_records_citation` | String | Academy citation text |

### 4.9 `hall_of_fame_inductions`
| Field | Type | Description |
| :--- | :--- | :--- |
| `induction_id` | String | Unique Hall of Fame induction key |
| `inducted_work_title` | String | Historic single or album inducted |
| `recording_artist_name` | String | Performing artist or orchestra |
| `original_release_year` | Integer | Year first commercially issued |
| `induction_ceremony_year` | Integer | Year inducted into GRAMMY Hall of Fame |
| `recording_medium_format` | String | Original format (78 RPM Shellac, 45 RPM Vinyl, 33 1/3 LP) |
| `qualifying_minimum_age_years` | Integer | Age qualification (minimum 25 years old) |
| `historical_impact_essay` | String | Curatorial essay on enduring qualitative merit |
| `museum_exhibition_status` | String | On display at GRAMMY Museum Los Angeles |
| `catalog_archival_code` | String | Library of Congress or Academy archive index |

### 4.10 `winner_press_releases`
| Field | Type | Description |
| :--- | :--- | :--- |
| `release_id` | String | Unique press release bulletin code |
| `ceremony_id` | String | Foreign reference to `ceremonies.ceremony_id` |
| `release_headline` | String | Official press announcement title |
| `publication_timestamp_utc` | String | Timestamp dispatched to global media |
| `headlining_creator_ids` | Array of String | Key winning artists highlighted |
| `telecast_highlights_summary` | String | Summary of major wins and show ratings |
| `pr_communications_director` | String | Executive signing off on publication |
| `syndication_wire_distribution`| Array of String | Press wire services (PR Newswire, BusinessWire, AP) |
| `press_asset_bundle_url` | String | High-resolution press kit photo download link |
| `archival_digest_id` | String | Archival press record ID |

---

# 5. Database: `grammy_creators_db` (Member 5)

### 5.1 `artists`
| Field | Type | Description |
| :--- | :--- | :--- |
| `artist_id` | String | Primary creator identifier (e.g., `CRT_BEYONCE_001`) |
| `full_legal_name` | String | Legal birth name |
| `stage_name` | String | Public performing name |
| `primary_musical_genre` | String | Core musical style |
| `birth_or_formation_date` | String | Date of birth or founding |
| `country_of_citizenship` | String | Country of origin |
| `active_career_start_year` | Integer | Debut commercial career year |
| `is_group_ensemble_flag` | Boolean | True if band or group entity |
| `musicbrainz_artist_gid` | String | Canonical UUID from MusicBrainz Open Database |
| `official_website_url` | String | Verified web URL |
| `biography_overview` | String | Biographical career profile |

### 5.2 `producers`
| Field | Type | Description |
| :--- | :--- | :--- |
| `producer_id` | String | Unique producer specialty profile ID |
| `creator_id` | String | Foreign reference to `artists.artist_id` |
| `primary_production_genre` | String | Genre specialization |
| `headquarters_studio_location` | String | Primary recording studio base (City, State) |
| `production_company_affiliation`| String | Production banner / enterprise |
| `analog_digital_workflow_preference` | String | Analog Tape, Hybrid, In-The-Box DAW |
| `total_career_credits_count` | Integer | Total verified production discography credits |
| `discogs_producer_id` | String | Discogs music database identifier |
| `first_notable_production_year` | Integer | Year of first commercially successful production |
| `signature_sound_profile` | String | Distinctive acoustic/sonic trademark |

### 5.3 `audio_engineers`
| Field | Type | Description |
| :--- | :--- | :--- |
| `engineer_id` | String | Unique audio engineering profile ID |
| `creator_id` | String | Foreign reference to `artists.artist_id` |
| `engineering_specialization` | String | Tracking, Mixing, Mastering, Immersive Audio |
| `primary_mastering_facility` | String | Commercial studio facility |
| `hardware_console_credits` | String | Primary mixing desks (SSL 4000, Neve 88RS) |
| `dolby_atmos_certified_status` | Boolean | Certified for immersive spatial audio mixing |
| `aes_professional_membership` | Boolean | Member of Audio Engineering Society |
| `first_album_engineering_year` | Integer | Year of earliest credited engineering release |
| `technical_patents_held` | Integer | Count of audio hardware/software patents held |
| `discogs_engineer_id` | String | Discogs catalog profile ID |

### 5.4 `songwriters_composers`
| Field | Type | Description |
| :--- | :--- | :--- |
| `songwriter_id` | String | Unique songwriting entity identifier |
| `creator_id` | String | Foreign reference to `artists.artist_id` |
| `pro_affiliation` | String | Performing Rights Organization (ASCAP, BMI, SESAC, PRS) |
| `ipi_cae_identifier` | String | International Interested Parties Information code |
| `music_publisher_company` | String | Primary publishing company (Sony Music Publishing, Universal) |
| `lyric_vs_composition_focus` | String | Lyricist, Melodic Composer, Both |
| `registered_works_count` | Integer | Total copyrighted compositions registered |
| `inducted_songwriters_hof` | Boolean | Inducted into Songwriters Hall of Fame |
| `primary_songwriting_instrument`| String | Piano, Acoustic Guitar, Bass, Synth |
| `signature_melodic_style` | String | Stylistic songwriting signature |

### 5.5 `arrangers_conductors`
| Field | Type | Description |
| :--- | :--- | :--- |
| `arranger_id` | String | Unique arranging profile key |
| `creator_id` | String | Foreign reference to `artists.artist_id` |
| `arrangement_discipline` | String | Orchestral, Big Band, Choral, String Quartet |
| `resident_orchestra_ensemble` | String | Affiliated symphony orchestra or ensemble |
| `formal_conservatory_education` | String | Music conservatory (Juilliard, Berklee, Royal Academy) |
| `sheet_music_publisher` | String | Commercial score publishing house |
| `conducts_own_compositions` | Boolean | Personally conducts live and studio recordings |
| `classical_crossover_experience`| Boolean | Arranges for mainstream popular recording artists |
| `union_musicians_local` | String | American Federation of Musicians (AFM) Local branch |
| `career_commission_count` | Integer | Number of symphonic/academic commissions |

### 5.6 `record_labels`
| Field | Type | Description |
| :--- | :--- | :--- |
| `label_id` | String | Unique record label code (e.g., `LBL_COLUMBIA`) |
| `label_corporate_name` | String | Full registered corporate entity name |
| `parent_music_group` | String | Major conglomerate (Universal Music Group, Sony Music, Warner) |
| `foundation_year` | Integer | Year company was established |
| `corporate_headquarters_city` | String | Headquarters city |
| `origin_country` | String | Country of origin |
| `commercial_distribution_channel`| String | Global physical and digital distributor |
| `riaa_member_standing` | Boolean | Active member of Recording Industry Association of America |
| `historical_catalog_size` | Integer | Number of distinct commercial album releases |
| `current_operational_status` | String | Active, Imprint, Defunct, Dormant |

### 5.7 `musical_groups`
| Field | Type | Description |
| :--- | :--- | :--- |
| `group_id` | String | Unique band / group identifier |
| `group_name` | String | Commercial band name |
| `formation_calendar_year` | Integer | Year band was formed |
| `disbandment_year` | Integer | Year band broke up (null if active) |
| `ensemble_structure_type` | String | Duo, Trio, Quartet, Quintet, Big Band, Collective |
| `origin_city` | String | City where group originated |
| `origin_country` | String | Country of origin |
| `current_activity_status` | Boolean | True if actively touring/recording |
| `signature_musical_style` | String | Defining musical genre |
| `musicbrainz_group_gid` | String | MusicBrainz band UUID |

### 5.8 `group_memberships`
| Field | Type | Description |
| :--- | :--- | :--- |
| `membership_id` | String | Unique member-group tenure code |
| `group_id` | String | Foreign reference to `musical_groups.group_id` |
| `artist_id` | String | Foreign reference to `artists.artist_id` |
| `role_within_group` | String | Instrument/Role (Lead Vocals, Bass, Drums, Guitar) |
| `tenure_start_year` | Integer | Year joined group |
| `tenure_end_year` | Integer | Year departed group (null if still active) |
| `is_founding_member` | Boolean | Part of original band lineup |
| `is_primary_frontperson` | Boolean | Primary media spokesperson / lead vocalist |
| `royalty_split_contract_percentage` | Double | Legal contract share of band royalties |
| `member_departure_reason` | String | Solo career, artistic differences, retirement |

### 5.9 `creator_discographies`
| Field | Type | Description |
| :--- | :--- | :--- |
| `discography_id` | String | Unique discography entry key |
| `creator_id` | String | Foreign reference to `artists.artist_id` |
| `work_id` | String | Foreign reference to `nominated_works.work_id` |
| `release_calendar_year` | Integer | Year of commercial release |
| `primary_credit_type` | String | Primary Artist, Featured Performer, Producer, Engineer |
| `catalog_matrix_code` | String | Vinyl/CD matrix catalog number |
| `billboard_200_peak_position` | Integer | Peak chart position on US Billboard 200 |
| `riaa_certification_status` | String | Gold, Platinum, Multi-Platinum, Diamond, Uncertified |
| `recording_studio_facility` | String | Commercial studio where album was tracked |
| `master_rights_holder_label_id`| String | Foreign reference to `record_labels.label_id` |

### 5.10 `creator_collaborations`
| Field | Type | Description |
| :--- | :--- | :--- |
| `collab_id` | String | Unique collaborative partnership ID |
| `work_id` | String | Foreign reference to `nominated_works.work_id` |
| `creator_a_id` | String | Foreign reference to first creator |
| `creator_b_id` | String | Foreign reference to second creator |
| `collaboration_nature` | String | Duet, Guest Feature, Producer-Artist Tandem, Co-writers |
| `billing_credit_format` | String | Billing style ("Artist A feat. Artist B", "Artist A & Artist B") |
| `publishing_split_percentage` | Double | Agreed publishing royalty division (e.g., 50.0%) |
| `joint_grammy_nominations_count`| Integer | Cumulative nominations shared by this pairing |
| `clearance_agreement_date` | String | Date legal cross-label clearance was executed |
| `inter_label_licensing_waiver` | String | Legal waiver reference number |
