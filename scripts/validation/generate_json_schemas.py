"""
Schema Generator: Automatically synthesizes formal MongoDB JSON Schemas
for all 50 collections across the 5 member databases of the
GRAMMY Awards Information & Analytics System.
"""

import json
from pathlib import Path

BASE_SCHEMA_DIR = Path("schemas/json_schemas")

# Master definition of all 50 collections and their >=10 meaningful fields
COLLECTION_SPECS = {
    "grammy_history_db": {
        "ceremonies": {
            "ceremony_id": "string",
            "edition_number": "int",
            "ceremony_date": "string",
            "broadcast_year": "int",
            "eligibility_period_start": "string",
            "eligibility_period_end": "string",
            "host_city": "string",
            "venue_id": "string",
            "primary_network": "string",
            "total_awards_presented": "int",
            "created_at": "string"
        },
        "venues": {
            "venue_id": "string",
            "venue_name": "string",
            "venue_type": "string",
            "street_address": "string",
            "city": "string",
            "state": "string",
            "postal_code": "string",
            "max_seating_capacity": "int",
            "first_hosted_year": "int",
            "total_ceremonies_hosted": "int"
        },
        "telecast_broadcasters": {
            "broadcast_id": "string",
            "ceremony_id": "string",
            "network_name": "string",
            "country_code": "string",
            "broadcast_start_time_utc": "string",
            "scheduled_duration_minutes": "int",
            "executive_producer": "string",
            "director_name": "string",
            "parental_advisory_rating": "string",
            "hd_4k_feed_enabled": "bool"
        },
        "viewership_ratings": {
            "rating_id": "string",
            "ceremony_id": "string",
            "us_viewers_millions": "number",
            "household_rating_pct": "number",
            "household_share_pct": "number",
            "demo_18_49_rating": "number",
            "peak_viewers_millions": "number",
            "peak_broadcast_segment": "string",
            "digital_streaming_views_millions": "number",
            "measurement_agency": "string"
        },
        "ceremony_hosts": {
            "host_assignment_id": "string",
            "ceremony_id": "string",
            "creator_id": "string",
            "host_full_name": "string",
            "hosting_style": "string",
            "solo_or_duo": "string",
            "host_sequence_count": "int",
            "monologue_duration_seconds": "int",
            "emmy_nomination_received": "bool",
            "contracted_talent_agency": "string"
        },
        "historic_milestones": {
            "milestone_id": "string",
            "ceremony_id": "string",
            "milestone_title": "string",
            "calendar_year": "int",
            "primary_subject_creator_id": "string",
            "cultural_significance_summary": "string",
            "official_academy_recognition": "bool",
            "controversy_flag": "bool",
            "archival_video_reel_id": "string",
            "citation_source_url": "string"
        },
        "academy_leadership": {
            "leadership_id": "string",
            "officer_name": "string",
            "executive_role_title": "string",
            "tenure_start_year": "int",
            "tenure_end_year": "int",
            "professional_music_background": "string",
            "trustee_chapter_location": "string",
            "notable_policy_amendment": "string",
            "board_voting_privileges": "bool",
            "appointed_by": "string"
        },
        "lifetime_achievement_honors": {
            "honor_id": "string",
            "ceremony_id": "string",
            "recipient_creator_id": "string",
            "honor_type": "string",
            "announcement_year": "int",
            "career_span_decades": "int",
            "presenting_dignitary_name": "string",
            "citation_text": "string",
            "is_posthumous_award": "bool",
            "special_tribute_performance_flag": "bool"
        },
        "timeline_historical_eras": {
            "era_id": "string",
            "era_name": "string",
            "start_calendar_year": "int",
            "end_calendar_year": "int",
            "dominant_audio_format": "string",
            "voting_tabulation_method": "string",
            "predominant_music_genre": "string",
            "total_ceremonies_contained": "int",
            "headquarters_city": "string",
            "industry_paradigm_shift_notes": "string"
        },
        "press_media_accreditations": {
            "accreditation_id": "string",
            "ceremony_id": "string",
            "media_organization_name": "string",
            "media_channel_type": "string",
            "origin_country": "string",
            "passes_granted_count": "int",
            "red_carpet_position_tier": "string",
            "press_room_interview_quota": "int",
            "pool_broadcaster_status": "bool",
            "compliance_clearance_status": "string"
        }
    },
    "grammy_categories_db": {
        "award_fields": {
            "field_id": "string",
            "field_name": "string",
            "field_abbreviation": "string",
            "field_description": "string",
            "inaugural_ceremony_edition": "int",
            "current_active_status": "bool",
            "active_categories_count": "int",
            "specialist_committee_jurisdiction": "string",
            "field_curator_role": "string",
            "last_bylaw_revision_year": "int"
        },
        "award_categories": {
            "category_id": "string",
            "field_id": "string",
            "official_category_name": "string",
            "standard_short_code": "string",
            "inaugural_edition": "int",
            "is_general_field": "bool",
            "current_status": "string",
            "maximum_nominees_allowed": "int",
            "voting_tier_access": "string",
            "trophy_statuette_eligibility_rule": "string",
            "entry_fee_tier": "string"
        },
        "category_lineage": {
            "lineage_id": "string",
            "category_id": "string",
            "predecessor_category_name": "string",
            "successor_category_name": "string",
            "effective_ceremony_edition": "int",
            "transition_classification": "string",
            "structural_rationale": "string",
            "nominee_slate_impact_count": "int",
            "trustee_resolution_reference": "string",
            "ballot_clarification_bulletin": "string"
        },
        "eligibility_rules": {
            "rule_id": "string",
            "category_id": "string",
            "effective_edition": "int",
            "minimum_playing_time_minutes": "number",
            "minimum_track_count": "int",
            "featured_performance_threshold_pct": "number",
            "us_release_commercial_requirement": "bool",
            "language_composition_restrictions": "string",
            "sample_replay_clearance_rule": "string",
            "entry_window_months": "int"
        },
        "voting_procedures": {
            "procedure_id": "string",
            "category_id": "string",
            "voting_round_number": "int",
            "electorate_body_type": "string",
            "is_ranked_choice_ballot": "bool",
            "craft_committee_review_required": "bool",
            "committee_member_roster_count": "int",
            "nomination_slot_capacity": "int",
            "tie_breaking_protocol": "string",
            "auditing_firm_signoff_flag": "bool"
        },
        "discontinued_categories": {
            "discontinued_id": "string",
            "category_name": "string",
            "final_active_ceremony_edition": "int",
            "cumulative_years_active": "int",
            "retirement_rationale": "string",
            "merged_into_category_id": "string",
            "total_winners_awarded": "int",
            "total_nominations_recorded": "int",
            "historic_significance_tag": "string",
            "archive_vault_reference": "string"
        },
        "category_quotas_limits": {
            "quota_id": "string",
            "category_id": "string",
            "ceremony_edition": "int",
            "standard_nominee_limit": "int",
            "emergency_tie_allowance": "int",
            "max_credited_producers_eligible": "int",
            "max_credited_engineers_eligible": "int",
            "playing_time_contribution_threshold_pct": "number",
            "lyricist_track_threshold_pct": "number",
            "pro_rata_trophy_rule": "string"
        },
        "special_merit_categories": {
            "special_merit_id": "string",
            "award_title": "string",
            "conferral_frequency": "string",
            "governing_board_supermajority_pct": "number",
            "candidate_selection_protocol": "string",
            "trophy_or_plaque_type": "string",
            "first_conferred_year": "int",
            "target_industry_discipline": "string",
            "peer_nomination_permitted": "bool",
            "ceremony_segment_placement": "string"
        },
        "craft_credit_definitions": {
            "craft_def_id": "string",
            "category_id": "string",
            "craft_role_name": "string",
            "mandatory_statuette_recipient": "bool",
            "certificate_of_merit_alternative": "bool",
            "audio_stem_mastering_threshold": "number",
            "assistant_engineer_eligibility": "bool",
            "sample_creator_eligibility": "bool",
            "documentation_proof_standard": "string",
            "union_credit_registry_crosscheck": "string"
        },
        "merged_split_history": {
            "event_id": "string",
            "restructuring_type": "string",
            "effective_year": "int",
            "primary_category_id": "string",
            "source_category_ids": "array",
            "consolidation_justification": "string",
            "gender_neutral_reform_flag": "bool",
            "member_feedback_period_days": "int",
            "trustee_vote_tally": "string",
            "published_press_bulletin_id": "string"
        }
    },
    "grammy_nominations_db": {
        "nomination_entries": {
            "nomination_id": "string",
            "ceremony_id": "string",
            "category_id": "string",
            "work_id": "string",
            "nomination_year": "int",
            "entry_billing_title": "string",
            "primary_artist_id": "string",
            "is_winner_flag": "bool",
            "ballot_slot_order": "int",
            "auditor_validation_code": "string",
            "created_timestamp": "string"
        },
        "nominated_works": {
            "work_id": "string",
            "work_type": "string",
            "work_title": "string",
            "commercial_release_date": "string",
            "primary_label_id": "string",
            "isrc_code": "string",
            "upc_barcode": "string",
            "duration_total_seconds": "int",
            "track_count": "int",
            "parental_advisory_flag": "bool",
            "language_iso_code": "string"
        },
        "nomination_credits": {
            "credit_id": "string",
            "nomination_id": "string",
            "creator_id": "string",
            "credit_role": "string",
            "credit_billing_rank": "int",
            "work_contribution_summary": "string",
            "contribution_percentage": "number",
            "is_lead_performer": "bool",
            "is_producer_credit": "bool",
            "academy_verified_status": "bool"
        },
        "submission_batches": {
            "batch_id": "string",
            "ceremony_id": "string",
            "submitting_label_id": "string",
            "submission_timestamp": "string",
            "total_entries_count": "int",
            "entry_fee_total_usd": "number",
            "compliance_officer_name": "string",
            "first_round_accepted_count": "int",
            "disqualified_entries_count": "int",
            "payment_reconciliation_hash": "string"
        },
        "genre_classifications": {
            "classification_id": "string",
            "work_id": "string",
            "submitted_field_id": "string",
            "assigned_field_id": "string",
            "primary_genre_tag": "string",
            "secondary_genre_tags": "array",
            "screening_committee_consensus": "string",
            "contested_by_label_flag": "bool",
            "reclassification_justification": "string",
            "determination_date": "string"
        },
        "first_time_nominees": {
            "first_nom_id": "string",
            "nomination_id": "string",
            "creator_id": "string",
            "debut_ceremony_edition": "int",
            "breakout_work_id": "string",
            "best_new_artist_nominated": "bool",
            "age_at_debut_nomination": "int",
            "prior_uncredited_appearances": "int",
            "commercial_breakout_tier": "string",
            "career_inception_year": "int"
        },
        "tied_nominations": {
            "tie_id": "string",
            "ceremony_id": "string",
            "category_id": "string",
            "tied_nomination_ids": "array",
            "tied_vote_count_audited": "int",
            "ballot_auditor_token": "string",
            "board_tie_waiver_approved": "bool",
            "expanded_slate_size": "int",
            "adjudication_timestamp": "string",
            "bylaw_clause_reference": "string"
        },
        "multi_nomination_packages": {
            "package_id": "string",
            "ceremony_id": "string",
            "creator_id": "string",
            "total_nominations_count": "int",
            "general_field_nominations_count": "int",
            "genre_field_nominations_count": "int",
            "leading_nominee_rank": "int",
            "nominated_work_ids": "array",
            "public_announcement_tier": "string",
            "ceremony_year": "int"
        },
        "voter_screening_batches": {
            "screening_batch_id": "string",
            "ceremony_id": "string",
            "field_id": "string",
            "panel_chair_creator_id": "string",
            "session_start_timestamp": "string",
            "session_end_timestamp": "string",
            "works_screened_count": "int",
            "disqualifications_ordered": "int",
            "quorum_certified": "bool",
            "panel_confidentiality_hash": "string"
        },
        "nomination_audit_logs": {
            "audit_id": "string",
            "nomination_id": "string",
            "auditing_firm_id": "string",
            "lead_auditor_name": "string",
            "audit_timestamp": "string",
            "digital_signature_hash": "string",
            "tabulation_vault_partition": "string",
            "discrepancy_check_passed": "bool",
            "recount_required_flag": "bool",
            "compliance_certificate_code": "string"
        }
    },
    "grammy_winners_db": {
        "winner_records": {
            "winner_record_id": "string",
            "nomination_id": "string",
            "ceremony_id": "string",
            "category_id": "string",
            "winning_work_id": "string",
            "primary_artist_id": "string",
            "broadcast_presentation_order": "int",
            "presented_live_on_telecast": "bool",
            "acceptance_speech_delivered": "bool",
            "trophy_statuettes_awarded_count": "int",
            "verified_timestamp": "string"
        },
        "big_four_sweeps": {
            "sweep_id": "string",
            "ceremony_id": "string",
            "creator_id": "string",
            "sweep_achievement_type": "string",
            "aoty_nomination_id": "string",
            "roty_nomination_id": "string",
            "soty_nomination_id": "string",
            "bna_nomination_id": "string",
            "sweep_calendar_year": "int",
            "career_significance_rating": "string"
        },
        "record_breakers": {
            "record_id": "string",
            "winner_record_id": "string",
            "creator_id": "string",
            "record_metric_name": "string",
            "previous_record_holder_name": "string",
            "previous_record_value": "number",
            "new_record_value": "number",
            "record_establishment_year": "int",
            "creator_age_at_record": "number",
            "academy_verified_announcement_url": "string"
        },
        "acceptance_speeches": {
            "speech_id": "string",
            "winner_record_id": "string",
            "primary_speaker_creator_id": "string",
            "speech_duration_seconds": "int",
            "playoff_music_interrupted": "bool",
            "primary_quote_transcript": "string",
            "individuals_acknowledged": "array",
            "social_political_message_flag": "bool",
            "press_room_followup_id": "string",
            "broadcast_clip_timecode": "string"
        },
        "trophy_tracking": {
            "trophy_id": "string",
            "winner_record_id": "string",
            "recipient_creator_id": "string",
            "statuette_serial_number": "string",
            "engraved_billing_text": "string",
            "manufacturing_foundry_name": "string",
            "grammium_alloy_specification": "string",
            "gold_plating_thickness_microns": "number",
            "dispatch_shipment_date": "string",
            "custody_receipt_hash": "string"
        },
        "consecutive_winners": {
            "streak_id": "string",
            "creator_id": "string",
            "category_id": "string",
            "streak_span_years": "int",
            "initial_ceremony_edition": "int",
            "terminal_ceremony_edition": "int",
            "winning_work_ids_list": "array",
            "is_streak_currently_active": "bool",
            "historical_streak_rank": "int",
            "category_monopoly_notes": "string"
        },
        "posthumous_awards": {
            "posthumous_id": "string",
            "winner_record_id": "string",
            "deceased_creator_id": "string",
            "date_of_passing": "string",
            "award_ceremony_date": "string",
            "accepted_by_representative": "string",
            "representative_legal_relationship": "string",
            "in_memoriam_segment_aired": "bool",
            "estate_concurrence_status": "string",
            "tribute_performance_id": "string"
        },
        "historic_win_benchmarks": {
            "benchmark_id": "string",
            "benchmark_title": "string",
            "qualifying_win_threshold": "int",
            "total_qualifying_creators": "int",
            "pioneering_creator_id": "string",
            "year_threshold_first_achieved": "int",
            "most_recent_qualifier_id": "string",
            "egot_component_flag": "bool",
            "rarity_index_score": "number",
            "hall_of_records_citation": "string"
        },
        "hall_of_fame_inductions": {
            "induction_id": "string",
            "inducted_work_title": "string",
            "recording_artist_name": "string",
            "original_release_year": "int",
            "induction_ceremony_year": "int",
            "recording_medium_format": "string",
            "qualifying_minimum_age_years": "int",
            "historical_impact_essay": "string",
            "museum_exhibition_status": "string",
            "catalog_archival_code": "string"
        },
        "winner_press_releases": {
            "release_id": "string",
            "ceremony_id": "string",
            "release_headline": "string",
            "publication_timestamp_utc": "string",
            "headlining_creator_ids": "array",
            "telecast_highlights_summary": "string",
            "pr_communications_director": "string",
            "syndication_wire_distribution": "array",
            "press_asset_bundle_url": "string",
            "archival_digest_id": "string"
        }
    },
    "grammy_creators_db": {
        "artists": {
            "artist_id": "string",
            "full_legal_name": "string",
            "stage_name": "string",
            "primary_musical_genre": "string",
            "birth_or_formation_date": "string",
            "country_of_citizenship": "string",
            "active_career_start_year": "int",
            "is_group_ensemble_flag": "bool",
            "musicbrainz_artist_gid": "string",
            "official_website_url": "string",
            "biography_overview": "string"
        },
        "producers": {
            "producer_id": "string",
            "creator_id": "string",
            "primary_production_genre": "string",
            "headquarters_studio_location": "string",
            "production_company_affiliation": "string",
            "analog_digital_workflow_preference": "string",
            "total_career_credits_count": "int",
            "discogs_producer_id": "string",
            "first_notable_production_year": "int",
            "signature_sound_profile": "string"
        },
        "audio_engineers": {
            "engineer_id": "string",
            "creator_id": "string",
            "engineering_specialization": "string",
            "primary_mastering_facility": "string",
            "hardware_console_credits": "string",
            "dolby_atmos_certified_status": "bool",
            "aes_professional_membership": "bool",
            "first_album_engineering_year": "int",
            "technical_patents_held": "int",
            "discogs_engineer_id": "string"
        },
        "songwriters_composers": {
            "songwriter_id": "string",
            "creator_id": "string",
            "pro_affiliation": "string",
            "ipi_cae_identifier": "string",
            "music_publisher_company": "string",
            "lyric_vs_composition_focus": "string",
            "registered_works_count": "int",
            "inducted_songwriters_hof": "bool",
            "primary_songwriting_instrument": "string",
            "signature_melodic_style": "string"
        },
        "arrangers_conductors": {
            "arranger_id": "string",
            "creator_id": "string",
            "arrangement_discipline": "string",
            "resident_orchestra_ensemble": "string",
            "formal_conservatory_education": "string",
            "sheet_music_publisher": "string",
            "conducts_own_compositions": "bool",
            "classical_crossover_experience": "bool",
            "union_musicians_local": "string",
            "career_commission_count": "int"
        },
        "record_labels": {
            "label_id": "string",
            "label_corporate_name": "string",
            "parent_music_group": "string",
            "foundation_year": "int",
            "corporate_headquarters_city": "string",
            "origin_country": "string",
            "commercial_distribution_channel": "string",
            "riaa_member_standing": "bool",
            "historical_catalog_size": "int",
            "current_operational_status": "string"
        },
        "musical_groups": {
            "group_id": "string",
            "group_name": "string",
            "formation_calendar_year": "int",
            "disbandment_year": "int",
            "ensemble_structure_type": "string",
            "origin_city": "string",
            "origin_country": "string",
            "current_activity_status": "bool",
            "signature_musical_style": "string",
            "musicbrainz_group_gid": "string"
        },
        "group_memberships": {
            "membership_id": "string",
            "group_id": "string",
            "artist_id": "string",
            "role_within_group": "string",
            "tenure_start_year": "int",
            "tenure_end_year": "int",
            "is_founding_member": "bool",
            "is_primary_frontperson": "bool",
            "royalty_split_contract_percentage": "number",
            "member_departure_reason": "string"
        },
        "creator_discographies": {
            "discography_id": "string",
            "creator_id": "string",
            "work_id": "string",
            "release_calendar_year": "int",
            "primary_credit_type": "string",
            "catalog_matrix_code": "string",
            "billboard_200_peak_position": "int",
            "riaa_certification_status": "string",
            "recording_studio_facility": "string",
            "master_rights_holder_label_id": "string"
        },
        "creator_collaborations": {
            "collab_id": "string",
            "work_id": "string",
            "creator_a_id": "string",
            "creator_b_id": "string",
            "collaboration_nature": "string",
            "billing_credit_format": "string",
            "publishing_split_percentage": "number",
            "joint_grammy_nominations_count": "int",
            "clearance_agreement_date": "string",
            "inter_label_licensing_waiver": "string"
        }
    }
}

TYPE_MAP = {
    "string": {"type": "string"},
    "int": {"type": "integer"},
    "number": {"type": "number"},
    "bool": {"type": "boolean"},
    "array": {"type": "array", "items": {"type": "string"}}
}

def generate_schemas():
    total_generated = 0
    for db_name, collections in COLLECTION_SPECS.items():
        db_dir = BASE_SCHEMA_DIR / db_name
        db_dir.mkdir(parents=True, exist_ok=True)
        
        for coll_name, fields in collections.items():
            properties = {}
            required = []
            
            for field_name, field_type in fields.items():
                properties[field_name] = TYPE_MAP[field_type].copy()
                properties[field_name]["description"] = f"Domain attribute: {field_name}"
                required.append(field_name)
            
            schema = {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": f"{db_name}.{coll_name}",
                "description": f"Formal MongoDB schema for {coll_name} collection in {db_name}",
                "type": "object",
                "required": required,
                "properties": properties,
                "additionalProperties": True
            }
            
            out_file = db_dir / f"{coll_name}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(schema, f, indent=2)
            total_generated += 1
            
    print(f"Successfully generated {total_generated} JSON Schemas across 5 databases.")

if __name__ == "__main__":
    generate_schemas()
