-- ==============================================================================
-- GRAMMY Awards Information & Analytics System
-- Module 1 & 6: Relational Reference DDL Schema (Pre-Denormalization Normal Form)
-- Course: Advanced Database Management Systems (ADBMS)
-- ==============================================================================
-- This schema models the complete enterprise entity domain across all 5 databases
-- in strict Third Normal Form (3NF) / BCNF before MongoDB document embedding.
-- ==============================================================================

-- -----------------------------------------------------------------------------
-- 1. HISTORY & OPERATIONS DOMAIN (grammy_history_db)
-- -----------------------------------------------------------------------------

CREATE TABLE venues (
    venue_id VARCHAR(32) PRIMARY KEY,
    venue_name VARCHAR(128) NOT NULL,
    venue_type VARCHAR(64) NOT NULL,
    street_address VARCHAR(255),
    city VARCHAR(64) NOT NULL,
    state VARCHAR(32) NOT NULL,
    postal_code VARCHAR(16),
    max_seating_capacity INT CHECK (max_seating_capacity > 0),
    first_hosted_year INT CHECK (first_hosted_year >= 1958),
    total_ceremonies_hosted INT DEFAULT 0 CHECK (total_ceremonies_hosted >= 0)
);

CREATE TABLE ceremonies (
    ceremony_id VARCHAR(32) PRIMARY KEY,
    edition_number INT UNIQUE NOT NULL CHECK (edition_number > 0),
    ceremony_date DATE NOT NULL,
    broadcast_year INT NOT NULL CHECK (broadcast_year >= 1959),
    eligibility_period_start DATE NOT NULL,
    eligibility_period_end DATE NOT NULL,
    host_city VARCHAR(64) NOT NULL,
    venue_id VARCHAR(32) NOT NULL REFERENCES venues(venue_id),
    primary_network VARCHAR(32) NOT NULL,
    total_awards_presented INT NOT NULL CHECK (total_awards_presented > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE telecast_broadcasters (
    broadcast_id VARCHAR(32) PRIMARY KEY,
    ceremony_id VARCHAR(32) NOT NULL REFERENCES ceremonies(ceremony_id),
    network_name VARCHAR(64) NOT NULL,
    country_code CHAR(2) NOT NULL DEFAULT 'US',
    broadcast_start_time_utc TIMESTAMP NOT NULL,
    scheduled_duration_minutes INT NOT NULL CHECK (scheduled_duration_minutes > 0),
    executive_producer VARCHAR(128) NOT NULL,
    director_name VARCHAR(128) NOT NULL,
    parental_advisory_rating VARCHAR(16) NOT NULL,
    hd_4k_feed_enabled BOOLEAN DEFAULT TRUE
);

CREATE TABLE viewership_ratings (
    rating_id VARCHAR(32) PRIMARY KEY,
    ceremony_id VARCHAR(32) UNIQUE NOT NULL REFERENCES ceremonies(ceremony_id),
    us_viewers_millions NUMERIC(5,2) NOT NULL CHECK (us_viewers_millions >= 0),
    household_rating_pct NUMERIC(4,2) NOT NULL CHECK (household_rating_pct >= 0),
    household_share_pct NUMERIC(4,2) NOT NULL CHECK (household_share_pct >= 0),
    demo_18_49_rating NUMERIC(4,2) NOT NULL CHECK (demo_18_49_rating >= 0),
    peak_viewers_millions NUMERIC(5,2) CHECK (peak_viewers_millions >= us_viewers_millions),
    peak_broadcast_segment VARCHAR(128),
    digital_streaming_views_millions NUMERIC(5,2) DEFAULT 0,
    measurement_agency VARCHAR(64) NOT NULL DEFAULT 'Nielsen Media Research'
);

CREATE TABLE historic_milestones (
    milestone_id VARCHAR(32) PRIMARY KEY,
    ceremony_id VARCHAR(32) NOT NULL REFERENCES ceremonies(ceremony_id),
    milestone_title VARCHAR(255) NOT NULL,
    calendar_year INT NOT NULL CHECK (calendar_year >= 1959),
    primary_subject_creator_id VARCHAR(32),
    cultural_significance_summary TEXT NOT NULL,
    official_academy_recognition BOOLEAN DEFAULT TRUE,
    controversy_flag BOOLEAN DEFAULT FALSE,
    archival_video_reel_id VARCHAR(64),
    citation_source_url VARCHAR(255) NOT NULL
);

CREATE TABLE academy_leadership (
    leadership_id VARCHAR(32) PRIMARY KEY,
    officer_name VARCHAR(128) NOT NULL,
    executive_role_title VARCHAR(64) NOT NULL,
    tenure_start_year INT NOT NULL CHECK (tenure_start_year >= 1957),
    tenure_end_year INT CHECK (tenure_end_year >= tenure_start_year),
    professional_music_background VARCHAR(128),
    trustee_chapter_location VARCHAR(64) NOT NULL,
    notable_policy_amendment TEXT,
    board_voting_privileges BOOLEAN DEFAULT TRUE,
    appointed_by VARCHAR(64) NOT NULL
);

CREATE TABLE timeline_historical_eras (
    era_id VARCHAR(32) PRIMARY KEY,
    era_name VARCHAR(64) UNIQUE NOT NULL,
    start_calendar_year INT NOT NULL,
    end_calendar_year INT NOT NULL CHECK (end_calendar_year >= start_calendar_year),
    dominant_audio_format VARCHAR(64) NOT NULL,
    voting_tabulation_method VARCHAR(64) NOT NULL,
    predominant_music_genre VARCHAR(64) NOT NULL,
    total_ceremonies_contained INT NOT NULL CHECK (total_ceremonies_contained > 0),
    headquarters_city VARCHAR(64) NOT NULL,
    industry_paradigm_shift_notes TEXT
);

CREATE TABLE press_media_accreditations (
    accreditation_id VARCHAR(32) PRIMARY KEY,
    ceremony_id VARCHAR(32) NOT NULL REFERENCES ceremonies(ceremony_id),
    media_organization_name VARCHAR(128) NOT NULL,
    media_channel_type VARCHAR(32) NOT NULL,
    origin_country CHAR(2) NOT NULL DEFAULT 'US',
    passes_granted_count INT NOT NULL CHECK (passes_granted_count > 0),
    red_carpet_position_tier VARCHAR(16) NOT NULL,
    press_room_interview_quota INT DEFAULT 0,
    pool_broadcaster_status BOOLEAN DEFAULT FALSE,
    compliance_clearance_status VARCHAR(32) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 2. CATEGORIES & TAXONOMY DOMAIN (grammy_categories_db)
-- -----------------------------------------------------------------------------

CREATE TABLE award_fields (
    field_id VARCHAR(32) PRIMARY KEY,
    field_name VARCHAR(64) UNIQUE NOT NULL,
    field_abbreviation VARCHAR(16) NOT NULL,
    field_description TEXT NOT NULL,
    inaugural_ceremony_edition INT NOT NULL CHECK (inaugural_ceremony_edition > 0),
    current_active_status BOOLEAN DEFAULT TRUE,
    active_categories_count INT DEFAULT 0 CHECK (active_categories_count >= 0),
    specialist_committee_jurisdiction VARCHAR(128) NOT NULL,
    field_curator_role VARCHAR(64) NOT NULL,
    last_bylaw_revision_year INT CHECK (last_bylaw_revision_year >= 1958)
);

CREATE TABLE award_categories (
    category_id VARCHAR(32) PRIMARY KEY,
    field_id VARCHAR(32) NOT NULL REFERENCES award_fields(field_id),
    official_category_name VARCHAR(128) UNIQUE NOT NULL,
    standard_short_code VARCHAR(32) NOT NULL,
    inaugural_edition INT NOT NULL CHECK (inaugural_edition > 0),
    is_general_field BOOLEAN DEFAULT FALSE,
    current_status VARCHAR(32) NOT NULL DEFAULT 'Active',
    maximum_nominees_allowed INT NOT NULL DEFAULT 5 CHECK (maximum_nominees_allowed >= 3),
    voting_tier_access VARCHAR(64) NOT NULL,
    trophy_statuette_eligibility_rule VARCHAR(128) NOT NULL,
    entry_fee_tier VARCHAR(32) NOT NULL
);

CREATE TABLE category_lineage (
    lineage_id VARCHAR(32) PRIMARY KEY,
    category_id VARCHAR(32) NOT NULL REFERENCES award_categories(category_id),
    predecessor_category_name VARCHAR(128) NOT NULL,
    successor_category_name VARCHAR(128) NOT NULL,
    effective_ceremony_edition INT NOT NULL CHECK (effective_ceremony_edition > 0),
    transition_classification VARCHAR(32) NOT NULL,
    structural_rationale TEXT NOT NULL,
    nominee_slate_impact_count INT DEFAULT 0,
    trustee_resolution_reference VARCHAR(64) NOT NULL,
    ballot_clarification_bulletin TEXT
);

CREATE TABLE eligibility_rules (
    rule_id VARCHAR(32) PRIMARY KEY,
    category_id VARCHAR(32) NOT NULL REFERENCES award_categories(category_id),
    effective_edition INT NOT NULL CHECK (effective_edition > 0),
    minimum_playing_time_minutes NUMERIC(5,2) DEFAULT 0.0,
    minimum_track_count INT DEFAULT 1 CHECK (minimum_track_count >= 1),
    featured_performance_threshold_pct NUMERIC(5,2) DEFAULT 0.0,
    us_release_commercial_requirement BOOLEAN DEFAULT TRUE,
    language_composition_restrictions VARCHAR(64),
    sample_replay_clearance_rule TEXT,
    entry_window_months INT NOT NULL DEFAULT 12
);

CREATE TABLE voting_procedures (
    procedure_id VARCHAR(32) PRIMARY KEY,
    category_id VARCHAR(32) NOT NULL REFERENCES award_categories(category_id),
    voting_round_number INT NOT NULL CHECK (voting_round_number IN (1, 2)),
    electorate_body_type VARCHAR(64) NOT NULL,
    is_ranked_choice_ballot BOOLEAN DEFAULT FALSE,
    craft_committee_review_required BOOLEAN DEFAULT FALSE,
    committee_member_roster_count INT DEFAULT 0,
    nomination_slot_capacity INT NOT NULL CHECK (nomination_slot_capacity > 0),
    tie_breaking_protocol VARCHAR(128) NOT NULL,
    auditing_firm_signoff_flag BOOLEAN DEFAULT TRUE
);

CREATE TABLE discontinued_categories (
    discontinued_id VARCHAR(32) PRIMARY KEY,
    category_name VARCHAR(128) NOT NULL,
    final_active_ceremony_edition INT NOT NULL CHECK (final_active_ceremony_edition > 0),
    cumulative_years_active INT NOT NULL CHECK (cumulative_years_active > 0),
    retirement_rationale TEXT NOT NULL,
    merged_into_category_id VARCHAR(32) REFERENCES award_categories(category_id),
    total_winners_awarded INT NOT NULL CHECK (total_winners_awarded >= 0),
    total_nominations_recorded INT NOT NULL CHECK (total_nominations_recorded >= total_winners_awarded),
    historic_significance_tag VARCHAR(64) NOT NULL,
    archive_vault_reference VARCHAR(64) NOT NULL
);

CREATE TABLE category_quotas_limits (
    quota_id VARCHAR(32) PRIMARY KEY,
    category_id VARCHAR(32) NOT NULL REFERENCES award_categories(category_id),
    ceremony_edition INT NOT NULL CHECK (ceremony_edition > 0),
    standard_nominee_limit INT NOT NULL DEFAULT 5,
    emergency_tie_allowance INT NOT NULL DEFAULT 2,
    max_credited_producers_eligible INT DEFAULT 10,
    max_credited_engineers_eligible INT DEFAULT 10,
    playing_time_contribution_threshold_pct NUMERIC(5,2) NOT NULL DEFAULT 33.0,
    lyricist_track_threshold_pct NUMERIC(5,2) DEFAULT 0.0,
    pro_rata_trophy_rule VARCHAR(128) NOT NULL
);

CREATE TABLE special_merit_categories (
    special_merit_id VARCHAR(32) PRIMARY KEY,
    award_title VARCHAR(128) UNIQUE NOT NULL,
    conferral_frequency VARCHAR(32) NOT NULL,
    governing_board_supermajority_pct NUMERIC(5,2) NOT NULL CHECK (governing_board_supermajority_pct > 50.0),
    candidate_selection_protocol TEXT NOT NULL,
    trophy_or_plaque_type VARCHAR(64) NOT NULL,
    first_conferred_year INT NOT NULL CHECK (first_conferred_year >= 1958),
    target_industry_discipline VARCHAR(64) NOT NULL,
    peer_nomination_permitted BOOLEAN DEFAULT FALSE,
    ceremony_segment_placement VARCHAR(64) NOT NULL
);

CREATE TABLE craft_credit_definitions (
    craft_def_id VARCHAR(32) PRIMARY KEY,
    category_id VARCHAR(32) NOT NULL REFERENCES award_categories(category_id),
    craft_role_name VARCHAR(64) NOT NULL,
    mandatory_statuette_recipient BOOLEAN DEFAULT TRUE,
    certificate_of_merit_alternative BOOLEAN DEFAULT FALSE,
    audio_stem_mastering_threshold NUMERIC(5,2) DEFAULT 0.0,
    assistant_engineer_eligibility BOOLEAN DEFAULT FALSE,
    sample_creator_eligibility BOOLEAN DEFAULT FALSE,
    documentation_proof_standard VARCHAR(128) NOT NULL,
    union_credit_registry_crosscheck VARCHAR(64) NOT NULL
);

CREATE TABLE merged_split_history (
    event_id VARCHAR(32) PRIMARY KEY,
    restructuring_type VARCHAR(32) NOT NULL,
    effective_year INT NOT NULL CHECK (effective_year >= 1959),
    primary_category_id VARCHAR(32) NOT NULL REFERENCES award_categories(category_id),
    consolidation_justification TEXT NOT NULL,
    gender_neutral_reform_flag BOOLEAN DEFAULT FALSE,
    member_feedback_period_days INT DEFAULT 0,
    trustee_vote_tally VARCHAR(32) NOT NULL,
    published_press_bulletin_id VARCHAR(64) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 3. CREATORS & LABELS DOMAIN (grammy_creators_db)
-- -----------------------------------------------------------------------------

CREATE TABLE creators (
    creator_id VARCHAR(32) PRIMARY KEY,
    full_legal_name VARCHAR(128) NOT NULL,
    stage_name VARCHAR(128),
    primary_musical_genre VARCHAR(64),
    birth_or_formation_date DATE,
    country_of_citizenship VARCHAR(64) NOT NULL,
    active_career_start_year INT CHECK (active_career_start_year >= 1920),
    is_group_ensemble_flag BOOLEAN DEFAULT FALSE,
    musicbrainz_gid CHAR(36) UNIQUE,
    official_website_url VARCHAR(255),
    biography_overview TEXT
);

CREATE TABLE record_labels (
    label_id VARCHAR(32) PRIMARY KEY,
    label_corporate_name VARCHAR(128) UNIQUE NOT NULL,
    parent_music_group VARCHAR(128) NOT NULL,
    foundation_year INT CHECK (foundation_year >= 1880),
    corporate_headquarters_city VARCHAR(64) NOT NULL,
    origin_country CHAR(2) NOT NULL DEFAULT 'US',
    commercial_distribution_channel VARCHAR(64) NOT NULL,
    riaa_member_standing BOOLEAN DEFAULT TRUE,
    historical_catalog_size INT DEFAULT 0 CHECK (historical_catalog_size >= 0),
    current_operational_status VARCHAR(32) NOT NULL DEFAULT 'Active'
);

CREATE TABLE musical_groups (
    group_id VARCHAR(32) PRIMARY KEY,
    group_name VARCHAR(128) UNIQUE NOT NULL,
    formation_calendar_year INT NOT NULL CHECK (formation_calendar_year >= 1920),
    disbandment_year INT CHECK (disbandment_year >= formation_calendar_year),
    ensemble_structure_type VARCHAR(32) NOT NULL,
    origin_city VARCHAR(64) NOT NULL,
    origin_country CHAR(2) NOT NULL DEFAULT 'US',
    current_activity_status BOOLEAN DEFAULT TRUE,
    signature_musical_style VARCHAR(64) NOT NULL,
    musicbrainz_group_gid CHAR(36) UNIQUE
);

CREATE TABLE group_memberships (
    membership_id VARCHAR(32) PRIMARY KEY,
    group_id VARCHAR(32) NOT NULL REFERENCES musical_groups(group_id),
    creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    role_within_group VARCHAR(64) NOT NULL,
    tenure_start_year INT NOT NULL CHECK (tenure_start_year >= 1920),
    tenure_end_year INT CHECK (tenure_end_year >= tenure_start_year),
    is_founding_member BOOLEAN DEFAULT TRUE,
    is_primary_frontperson BOOLEAN DEFAULT FALSE,
    royalty_split_contract_percentage NUMERIC(5,2) DEFAULT 0.0,
    member_departure_reason VARCHAR(128)
);

CREATE TABLE producers (
    producer_id VARCHAR(32) PRIMARY KEY,
    creator_id VARCHAR(32) UNIQUE NOT NULL REFERENCES creators(creator_id),
    primary_production_genre VARCHAR(64) NOT NULL,
    headquarters_studio_location VARCHAR(128) NOT NULL,
    production_company_affiliation VARCHAR(128),
    analog_digital_workflow_preference VARCHAR(32) NOT NULL,
    total_career_credits_count INT DEFAULT 0,
    discogs_producer_id VARCHAR(64),
    first_notable_production_year INT,
    signature_sound_profile TEXT
);

CREATE TABLE audio_engineers (
    engineer_id VARCHAR(32) PRIMARY KEY,
    creator_id VARCHAR(32) UNIQUE NOT NULL REFERENCES creators(creator_id),
    engineering_specialization VARCHAR(64) NOT NULL,
    primary_mastering_facility VARCHAR(128) NOT NULL,
    hardware_console_credits VARCHAR(128),
    dolby_atmos_certified_status BOOLEAN DEFAULT FALSE,
    aes_professional_membership BOOLEAN DEFAULT TRUE,
    first_album_engineering_year INT,
    technical_patents_held INT DEFAULT 0,
    discogs_engineer_id VARCHAR(64)
);

CREATE TABLE songwriters_composers (
    songwriter_id VARCHAR(32) PRIMARY KEY,
    creator_id VARCHAR(32) UNIQUE NOT NULL REFERENCES creators(creator_id),
    pro_affiliation VARCHAR(32) NOT NULL,
    ipi_cae_identifier VARCHAR(32),
    music_publisher_company VARCHAR(128) NOT NULL,
    lyric_vs_composition_focus VARCHAR(32) NOT NULL,
    registered_works_count INT DEFAULT 0,
    inducted_songwriters_hof BOOLEAN DEFAULT FALSE,
    primary_songwriting_instrument VARCHAR(64) NOT NULL,
    signature_melodic_style TEXT
);

CREATE TABLE arrangers_conductors (
    arranger_id VARCHAR(32) PRIMARY KEY,
    creator_id VARCHAR(32) UNIQUE NOT NULL REFERENCES creators(creator_id),
    arrangement_discipline VARCHAR(64) NOT NULL,
    resident_orchestra_ensemble VARCHAR(128),
    formal_conservatory_education VARCHAR(128),
    sheet_music_publisher VARCHAR(128),
    conducts_own_compositions BOOLEAN DEFAULT FALSE,
    classical_crossover_experience BOOLEAN DEFAULT FALSE,
    union_musicians_local VARCHAR(32) NOT NULL,
    career_commission_count INT DEFAULT 0
);

-- -----------------------------------------------------------------------------
-- 4. NOMINATIONS & BALLOTS DOMAIN (grammy_nominations_db)
-- -----------------------------------------------------------------------------

CREATE TABLE nominated_works (
    work_id VARCHAR(32) PRIMARY KEY,
    work_type VARCHAR(32) NOT NULL,
    work_title VARCHAR(255) NOT NULL,
    commercial_release_date DATE NOT NULL,
    primary_label_id VARCHAR(32) NOT NULL REFERENCES record_labels(label_id),
    isrc_code VARCHAR(32),
    upc_barcode VARCHAR(32),
    duration_total_seconds INT NOT NULL CHECK (duration_total_seconds > 0),
    track_count INT NOT NULL DEFAULT 1 CHECK (track_count >= 1),
    parental_advisory_flag BOOLEAN DEFAULT FALSE,
    language_iso_code CHAR(2) NOT NULL DEFAULT 'en'
);

CREATE TABLE nomination_entries (
    nomination_id VARCHAR(32) PRIMARY KEY,
    ceremony_id VARCHAR(32) NOT NULL REFERENCES ceremonies(ceremony_id),
    category_id VARCHAR(32) NOT NULL REFERENCES award_categories(category_id),
    work_id VARCHAR(32) NOT NULL REFERENCES nominated_works(work_id),
    nomination_year INT NOT NULL CHECK (nomination_year >= 1959),
    entry_billing_title VARCHAR(255) NOT NULL,
    primary_artist_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    is_winner_flag BOOLEAN DEFAULT FALSE,
    ballot_slot_order INT NOT NULL CHECK (ballot_slot_order > 0),
    auditor_validation_code VARCHAR(64) NOT NULL,
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_nomination_slot UNIQUE (ceremony_id, category_id, work_id)
);

CREATE TABLE nomination_credits (
    credit_id VARCHAR(32) PRIMARY KEY,
    nomination_id VARCHAR(32) NOT NULL REFERENCES nomination_entries(nomination_id),
    creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    credit_role VARCHAR(64) NOT NULL,
    credit_billing_rank INT NOT NULL DEFAULT 1,
    work_contribution_summary VARCHAR(128) NOT NULL,
    contribution_percentage NUMERIC(5,2) DEFAULT 0.0,
    is_lead_performer BOOLEAN DEFAULT FALSE,
    is_producer_credit BOOLEAN DEFAULT FALSE,
    academy_verified_status BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_nomination_creator_role UNIQUE (nomination_id, creator_id, credit_role)
);

CREATE TABLE submission_batches (
    batch_id VARCHAR(32) PRIMARY KEY,
    ceremony_id VARCHAR(32) NOT NULL REFERENCES ceremonies(ceremony_id),
    submitting_label_id VARCHAR(32) NOT NULL REFERENCES record_labels(label_id),
    submission_timestamp TIMESTAMP NOT NULL,
    total_entries_count INT NOT NULL CHECK (total_entries_count > 0),
    entry_fee_total_usd NUMERIC(10,2) NOT NULL CHECK (entry_fee_total_usd >= 0),
    compliance_officer_name VARCHAR(128) NOT NULL,
    first_round_accepted_count INT NOT NULL CHECK (first_round_accepted_count >= 0),
    disqualified_entries_count INT NOT NULL DEFAULT 0,
    payment_reconciliation_hash VARCHAR(64) NOT NULL
);

CREATE TABLE genre_classifications (
    classification_id VARCHAR(32) PRIMARY KEY,
    work_id VARCHAR(32) NOT NULL REFERENCES nominated_works(work_id),
    submitted_field_id VARCHAR(32) NOT NULL REFERENCES award_fields(field_id),
    assigned_field_id VARCHAR(32) NOT NULL REFERENCES award_fields(field_id),
    primary_genre_tag VARCHAR(64) NOT NULL,
    screening_committee_consensus VARCHAR(32) NOT NULL,
    contested_by_label_flag BOOLEAN DEFAULT FALSE,
    reclassification_justification TEXT,
    determination_date DATE NOT NULL
);

CREATE TABLE first_time_nominees (
    first_nom_id VARCHAR(32) PRIMARY KEY,
    nomination_id VARCHAR(32) UNIQUE NOT NULL REFERENCES nomination_entries(nomination_id),
    creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    debut_ceremony_edition INT NOT NULL CHECK (debut_ceremony_edition > 0),
    breakout_work_id VARCHAR(32) NOT NULL REFERENCES nominated_works(work_id),
    best_new_artist_nominated BOOLEAN DEFAULT FALSE,
    age_at_debut_nomination INT CHECK (age_at_debut_nomination > 0),
    prior_uncredited_appearances INT DEFAULT 0,
    commercial_breakout_tier VARCHAR(32) NOT NULL,
    career_inception_year INT CHECK (career_inception_year >= 1920)
);

CREATE TABLE tied_nominations (
    tie_id VARCHAR(32) PRIMARY KEY,
    ceremony_id VARCHAR(32) NOT NULL REFERENCES ceremonies(ceremony_id),
    category_id VARCHAR(32) NOT NULL REFERENCES award_categories(category_id),
    tied_vote_count_audited INT NOT NULL CHECK (tied_vote_count_audited > 0),
    ballot_auditor_token VARCHAR(64) NOT NULL,
    board_tie_waiver_approved BOOLEAN DEFAULT TRUE,
    expanded_slate_size INT NOT NULL CHECK (expanded_slate_size > 5),
    adjudication_timestamp TIMESTAMP NOT NULL,
    bylaw_clause_reference VARCHAR(64) NOT NULL
);

CREATE TABLE multi_nomination_packages (
    package_id VARCHAR(32) PRIMARY KEY,
    ceremony_id VARCHAR(32) NOT NULL REFERENCES ceremonies(ceremony_id),
    creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    total_nominations_count INT NOT NULL CHECK (total_nominations_count >= 2),
    general_field_nominations_count INT NOT NULL DEFAULT 0,
    genre_field_nominations_count INT NOT NULL DEFAULT 0,
    leading_nominee_rank INT NOT NULL DEFAULT 1,
    public_announcement_tier VARCHAR(32) NOT NULL,
    ceremony_year INT NOT NULL CHECK (ceremony_year >= 1959),
    CONSTRAINT uq_multi_nom_creator UNIQUE (ceremony_id, creator_id)
);

CREATE TABLE voter_screening_batches (
    screening_batch_id VARCHAR(32) PRIMARY KEY,
    ceremony_id VARCHAR(32) NOT NULL REFERENCES ceremonies(ceremony_id),
    field_id VARCHAR(32) NOT NULL REFERENCES award_fields(field_id),
    panel_chair_creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    session_start_timestamp TIMESTAMP NOT NULL,
    session_end_timestamp TIMESTAMP NOT NULL,
    works_screened_count INT NOT NULL CHECK (works_screened_count > 0),
    disqualifications_ordered INT NOT NULL DEFAULT 0,
    quorum_certified BOOLEAN DEFAULT TRUE,
    panel_confidentiality_hash VARCHAR(64) NOT NULL
);

CREATE TABLE nomination_audit_logs (
    audit_id VARCHAR(32) PRIMARY KEY,
    nomination_id VARCHAR(32) NOT NULL REFERENCES nomination_entries(nomination_id),
    auditing_firm_id VARCHAR(64) NOT NULL,
    lead_auditor_name VARCHAR(128) NOT NULL,
    audit_timestamp TIMESTAMP NOT NULL,
    digital_signature_hash VARCHAR(64) NOT NULL,
    tabulation_vault_partition VARCHAR(64) NOT NULL,
    discrepancy_check_passed BOOLEAN DEFAULT TRUE,
    recount_required_flag BOOLEAN DEFAULT FALSE,
    compliance_certificate_code VARCHAR(64) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 5. WINNERS & TROPHIES DOMAIN (grammy_winners_db)
-- -----------------------------------------------------------------------------

CREATE TABLE winner_records (
    winner_record_id VARCHAR(32) PRIMARY KEY,
    nomination_id VARCHAR(32) UNIQUE NOT NULL REFERENCES nomination_entries(nomination_id),
    ceremony_id VARCHAR(32) NOT NULL REFERENCES ceremonies(ceremony_id),
    category_id VARCHAR(32) NOT NULL REFERENCES award_categories(category_id),
    winning_work_id VARCHAR(32) NOT NULL REFERENCES nominated_works(work_id),
    primary_artist_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    broadcast_presentation_order INT NOT NULL CHECK (broadcast_presentation_order > 0),
    presented_live_on_telecast BOOLEAN DEFAULT TRUE,
    acceptance_speech_delivered BOOLEAN DEFAULT TRUE,
    trophy_statuettes_awarded_count INT NOT NULL CHECK (trophy_statuettes_awarded_count >= 1),
    verified_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE big_four_sweeps (
    sweep_id VARCHAR(32) PRIMARY KEY,
    ceremony_id VARCHAR(32) NOT NULL REFERENCES ceremonies(ceremony_id),
    creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    sweep_achievement_type VARCHAR(32) NOT NULL,
    aoty_nomination_id VARCHAR(32) NOT NULL REFERENCES nomination_entries(nomination_id),
    roty_nomination_id VARCHAR(32) NOT NULL REFERENCES nomination_entries(nomination_id),
    soty_nomination_id VARCHAR(32) NOT NULL REFERENCES nomination_entries(nomination_id),
    bna_nomination_id VARCHAR(32) NOT NULL REFERENCES nomination_entries(nomination_id),
    sweep_calendar_year INT NOT NULL CHECK (sweep_calendar_year >= 1959),
    career_significance_rating VARCHAR(32) NOT NULL
);

CREATE TABLE record_breakers (
    record_id VARCHAR(32) PRIMARY KEY,
    winner_record_id VARCHAR(32) REFERENCES winner_records(winner_record_id),
    creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    record_metric_name VARCHAR(128) NOT NULL,
    previous_record_holder_name VARCHAR(128) NOT NULL,
    previous_record_value NUMERIC(8,2) NOT NULL,
    new_record_value NUMERIC(8,2) NOT NULL CHECK (new_record_value > previous_record_value),
    record_establishment_year INT NOT NULL CHECK (record_establishment_year >= 1959),
    creator_age_at_record NUMERIC(5,2),
    academy_verified_announcement_url VARCHAR(255) NOT NULL
);

CREATE TABLE acceptance_speeches (
    speech_id VARCHAR(32) PRIMARY KEY,
    winner_record_id VARCHAR(32) UNIQUE NOT NULL REFERENCES winner_records(winner_record_id),
    primary_speaker_creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    speech_duration_seconds INT NOT NULL CHECK (speech_duration_seconds > 0),
    playoff_music_interrupted BOOLEAN DEFAULT FALSE,
    primary_quote_transcript TEXT NOT NULL,
    social_political_message_flag BOOLEAN DEFAULT FALSE,
    press_room_followup_id VARCHAR(64),
    broadcast_clip_timecode VARCHAR(32) NOT NULL
);

CREATE TABLE trophy_tracking (
    trophy_id VARCHAR(32) PRIMARY KEY,
    winner_record_id VARCHAR(32) NOT NULL REFERENCES winner_records(winner_record_id),
    recipient_creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    statuette_serial_number VARCHAR(64) UNIQUE NOT NULL,
    engraved_billing_text TEXT NOT NULL,
    manufacturing_foundry_name VARCHAR(128) NOT NULL DEFAULT 'Billings Artworks',
    grammium_alloy_specification VARCHAR(64) NOT NULL,
    gold_plating_thickness_microns NUMERIC(4,2) NOT NULL DEFAULT 5.0,
    dispatch_shipment_date DATE,
    custody_receipt_hash VARCHAR(64)
);

CREATE TABLE consecutive_winners (
    streak_id VARCHAR(32) PRIMARY KEY,
    creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    category_id VARCHAR(32) NOT NULL REFERENCES award_categories(category_id),
    streak_span_years INT NOT NULL CHECK (streak_span_years >= 2),
    initial_ceremony_edition INT NOT NULL,
    terminal_ceremony_edition INT NOT NULL CHECK (terminal_ceremony_edition > initial_ceremony_edition),
    is_streak_currently_active BOOLEAN DEFAULT FALSE,
    historical_streak_rank INT NOT NULL DEFAULT 1,
    category_monopoly_notes TEXT
);

CREATE TABLE posthumous_awards (
    posthumous_id VARCHAR(32) PRIMARY KEY,
    winner_record_id VARCHAR(32) UNIQUE NOT NULL REFERENCES winner_records(winner_record_id),
    deceased_creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    date_of_passing DATE NOT NULL,
    award_ceremony_date DATE NOT NULL,
    accepted_by_representative VARCHAR(128) NOT NULL,
    representative_legal_relationship VARCHAR(64) NOT NULL,
    in_memoriam_segment_aired BOOLEAN DEFAULT TRUE,
    estate_concurrence_status VARCHAR(32) NOT NULL,
    tribute_performance_id VARCHAR(64)
);

CREATE TABLE historic_win_benchmarks (
    benchmark_id VARCHAR(32) PRIMARY KEY,
    benchmark_title VARCHAR(128) UNIQUE NOT NULL,
    qualifying_win_threshold INT NOT NULL CHECK (qualifying_win_threshold > 0),
    total_qualifying_creators INT NOT NULL CHECK (total_qualifying_creators >= 1),
    pioneering_creator_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    year_threshold_first_achieved INT NOT NULL CHECK (year_threshold_first_achieved >= 1959),
    most_recent_qualifier_id VARCHAR(32) NOT NULL REFERENCES creators(creator_id),
    egot_component_flag BOOLEAN DEFAULT FALSE,
    rarity_index_score NUMERIC(5,2) NOT NULL CHECK (rarity_index_score >= 0.0),
    hall_of_records_citation TEXT NOT NULL
);

CREATE TABLE hall_of_fame_inductions (
    induction_id VARCHAR(32) PRIMARY KEY,
    inducted_work_title VARCHAR(255) NOT NULL,
    recording_artist_name VARCHAR(128) NOT NULL,
    original_release_year INT NOT NULL CHECK (original_release_year >= 1900),
    induction_ceremony_year INT NOT NULL CHECK (induction_ceremony_year >= 1973),
    recording_medium_format VARCHAR(64) NOT NULL,
    qualifying_minimum_age_years INT NOT NULL DEFAULT 25 CHECK (qualifying_minimum_age_years >= 25),
    historical_impact_essay TEXT NOT NULL,
    museum_exhibition_status VARCHAR(64) NOT NULL,
    catalog_archival_code VARCHAR(64) NOT NULL
);

CREATE TABLE winner_press_releases (
    release_id VARCHAR(32) PRIMARY KEY,
    ceremony_id VARCHAR(32) NOT NULL REFERENCES ceremonies(ceremony_id),
    release_headline VARCHAR(255) NOT NULL,
    publication_timestamp_utc TIMESTAMP NOT NULL,
    telecast_highlights_summary TEXT NOT NULL,
    pr_communications_director VARCHAR(128) NOT NULL,
    press_asset_bundle_url VARCHAR(255) NOT NULL,
    archival_digest_id VARCHAR(64) NOT NULL
);

-- End of Relational Reference Schema
