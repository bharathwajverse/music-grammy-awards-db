/**
 * ============================================================================
 * MASTER AGGREGATION PIPELINE SUITE
 * ============================================================================
 * Project: Advanced Database Management Systems (ADBMS)
 * Module: Module 10 — Advanced Query & Aggregation Framework
 * Academic Phase: Phase 20 — Aggregation Framework
 * 
 * MANDATORY OPERATORS DEMONSTRATED:
 *   1. $match   (Filtering input streams, pre-aggregation & post-aggregation)
 *   2. $group   (Accumulator aggregation, distinct sets, mathematical sums)
 *   3. $sort    (Multi-key ordering, ascending/descending)
 *   4. $project (Document reshaping, derived field expressions, formatting)
 *   5. $count   (Counting pipeline stream results)
 *   6. $lookup  (Relational left outer joins across collections)
 *   7. $unwind  (Deconstruction of array fields)
 * 
 * MANDATORY ANALYTICAL EXAMPLES:
 *   1. Nominations per artist
 *   2. Wins per artist
 *   3. Wins by category
 *   4. Nominations by year
 *   5. Category trends
 *   6. Artists appearing in multiple categories
 *   7. Multi-time winners
 * 
 * SUPPLEMENTARY ANALYTICAL PIPELINES:
 *   8. Speech acknowledgments distribution ($unwind arrays)
 *   9. Venue hosting & capacity analytics ($lookup relational join)
 *  10. Category restructure & lineage analytics ($count & $unwind)
 * 
 * COMPLIANCE MANDATE:
 *   All calculated fields are explicitly prefixed or annotated as DERIVED.
 *   Real project data only. No synthetic or invented facts.
 * ============================================================================
 */

print("==================================================================");
print("STARTING PHASE 20 MASTER AGGREGATION PIPELINE SUITE EXECUTION");
print("==================================================================");

// ----------------------------------------------------------------------------
// 1. NOMINATIONS PER ARTIST (grammy_nominations_db)
// Demonstrates: $match, $lookup, $unwind, $group, $project, $sort, $limit
// ----------------------------------------------------------------------------
print("\n[PIPELINE 01] Nominations per Artist (grammy_nominations_db.nomination_entries)");
const dbNom = db.getSiblingDB("grammy_nominations_db");

const pipe01 = [
  { $match: { primary_artist_id: { $exists: true, $ne: null } } },
  {
    $lookup: {
      from: "nominated_works",
      localField: "work_id",
      foreignField: "work_id",
      as: "work_details"
    }
  },
  { $unwind: { path: "$work_details", preserveNullAndEmptyArrays: true } },
  {
    $group: {
      _id: "$primary_artist_id",
      artist_billing_name: { $first: "$entry_billing_title" },
      DERIVED_total_nominations: { $sum: 1 },
      DERIVED_earliest_nomination_year: { $min: "$nomination_year" },
      DERIVED_latest_nomination_year: { $max: "$nomination_year" },
      DERIVED_distinct_works: { $addToSet: "$work_details.work_title" },
      DERIVED_categories_nominated: { $addToSet: "$category_id" }
    }
  },
  {
    $project: {
      _id: 0,
      artist_id: "$_id",
      artist_billing_name: 1,
      DERIVED_total_nominations: 1,
      DERIVED_earliest_nomination_year: 1,
      DERIVED_latest_nomination_year: 1,
      DERIVED_career_span_years: {
        $subtract: ["$DERIVED_latest_nomination_year", "$DERIVED_earliest_nomination_year"]
      },
      DERIVED_distinct_works_count: { $size: "$DERIVED_distinct_works" },
      DERIVED_distinct_categories_count: { $size: "$DERIVED_categories_nominated" },
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },
  { $sort: { DERIVED_total_nominations: -1, artist_billing_name: 1 } },
  { $limit: 5 }
];

printjson(dbNom.nomination_entries.aggregate(pipe01).toArray());

// ----------------------------------------------------------------------------
// 2. WINS PER ARTIST (grammy_winners_db)
// Demonstrates: $match, $lookup, $group, $project, $sort, $limit
// ----------------------------------------------------------------------------
print("\n[PIPELINE 02] Wins per Artist (grammy_winners_db.winner_records)");
const dbWin = db.getSiblingDB("grammy_winners_db");

const pipe02 = [
  { $match: { primary_artist_id: { $exists: true, $ne: null } } },
  {
    $lookup: {
      from: "acceptance_speeches",
      localField: "winner_record_id",
      foreignField: "winner_record_id",
      as: "speech_records"
    }
  },
  {
    $group: {
      _id: "$primary_artist_id",
      DERIVED_total_wins: { $sum: 1 },
      DERIVED_total_statuettes_awarded: { $sum: "$trophy_statuettes_awarded_count" },
      DERIVED_live_telecast_wins: {
        $sum: { $cond: ["$presented_live_on_telecast", 1, 0] }
      },
      DERIVED_speeches_delivered: {
        $sum: { $cond: ["$acceptance_speech_delivered", 1, 0] }
      },
      DERIVED_winning_categories: { $addToSet: "$category_id" },
      DERIVED_winning_ceremonies: { $addToSet: "$ceremony_id" }
    }
  },
  {
    $project: {
      _id: 0,
      artist_id: "$_id",
      DERIVED_total_wins: 1,
      DERIVED_total_statuettes_awarded: 1,
      DERIVED_avg_statuettes_per_win: {
        $round: [
          { $divide: ["$DERIVED_total_statuettes_awarded", "$DERIVED_total_wins"] },
          2
        ]
      },
      DERIVED_live_telecast_wins: 1,
      DERIVED_speeches_delivered: 1,
      DERIVED_distinct_winning_categories_count: { $size: "$DERIVED_winning_categories" },
      DERIVED_distinct_ceremonies_count: { $size: "$DERIVED_winning_ceremonies" },
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },
  { $sort: { DERIVED_total_wins: -1, DERIVED_total_statuettes_awarded: -1 } },
  { $limit: 5 }
];

printjson(dbWin.winner_records.aggregate(pipe02).toArray());

// ----------------------------------------------------------------------------
// 3. WINS BY CATEGORY (grammy_winners_db)
// Demonstrates: $match, $group, $project, $sort, $limit
// ----------------------------------------------------------------------------
print("\n[PIPELINE 03] Wins by Category (grammy_winners_db.winner_records)");
const pipe03 = [
  { $match: { category_id: { $exists: true, $ne: null } } },
  {
    $group: {
      _id: "$category_id",
      DERIVED_total_historical_wins: { $sum: 1 },
      DERIVED_cumulative_statuettes: { $sum: "$trophy_statuettes_awarded_count" },
      DERIVED_telecast_presentations: {
        $sum: { $cond: ["$presented_live_on_telecast", 1, 0] }
      },
      DERIVED_distinct_winners: { $addToSet: "$primary_artist_id" },
      DERIVED_earliest_ceremony: { $min: "$ceremony_id" },
      DERIVED_latest_ceremony: { $max: "$ceremony_id" }
    }
  },
  {
    $project: {
      _id: 0,
      category_id: "$_id",
      DERIVED_total_historical_wins: 1,
      DERIVED_cumulative_statuettes: 1,
      DERIVED_telecast_presentations: 1,
      DERIVED_telecast_percentage: {
        $round: [
          {
            $multiply: [
              { $divide: ["$DERIVED_telecast_presentations", "$DERIVED_total_historical_wins"] },
              100
            ]
          },
          2
        ]
      },
      DERIVED_distinct_winners_count: { $size: "$DERIVED_distinct_winners" },
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },
  { $sort: { DERIVED_total_historical_wins: -1, DERIVED_cumulative_statuettes: -1 } },
  { $limit: 5 }
];

printjson(dbWin.winner_records.aggregate(pipe03).toArray());

// ----------------------------------------------------------------------------
// 4. NOMINATIONS BY YEAR (grammy_nominations_db)
// Demonstrates: $match, $group, $project, $sort
// ----------------------------------------------------------------------------
print("\n[PIPELINE 04] Nominations by Year (grammy_nominations_db.nomination_entries)");
const pipe04 = [
  { $match: { nomination_year: { $exists: true, $gte: 1958 } } },
  {
    $group: {
      _id: "$nomination_year",
      DERIVED_total_nominations: { $sum: 1 },
      DERIVED_total_winners: {
        $sum: { $cond: ["$is_winner_flag", 1, 0] }
      },
      DERIVED_distinct_categories: { $addToSet: "$category_id" },
      DERIVED_distinct_nominees: { $addToSet: "$primary_artist_id" },
      DERIVED_average_ballot_slot: { $avg: "$ballot_slot_order" }
    }
  },
  {
    $project: {
      _id: 0,
      ceremony_year: "$_id",
      DERIVED_total_nominations: 1,
      DERIVED_total_winners: 1,
      DERIVED_distinct_categories_count: { $size: "$DERIVED_distinct_categories" },
      DERIVED_distinct_nominees_count: { $size: "$DERIVED_distinct_nominees" },
      DERIVED_avg_slot_depth: { $round: ["$DERIVED_average_ballot_slot", 2] },
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },
  { $sort: { ceremony_year: 1 } },
  { $limit: 5 }
];

printjson(dbNom.nomination_entries.aggregate(pipe04).toArray());

// ----------------------------------------------------------------------------
// 5. CATEGORY TRENDS (grammy_nominations_db)
// Demonstrates: $match, $group, $project, $sort
// ----------------------------------------------------------------------------
print("\n[PIPELINE 05] Category Trends Across Decades (grammy_nominations_db.nomination_entries)");
const pipe05 = [
  {
    $match: {
      category_id: {
        $in: [
          "CAT_RECORD_OF_THE_YEAR_000",
          "CAT_ALBUM_OF_THE_YEAR_001",
          "CAT_SONG_OF_THE_YEAR_002",
          "CAT_BEST_NEW_ARTIST_003"
        ]
      }
    }
  },
  {
    $group: {
      _id: {
        category_id: "$category_id",
        decade: {
          $multiply: [
            { $floor: { $divide: ["$nomination_year", 10] } },
            10
          ]
        }
      },
      DERIVED_nominations_in_decade: { $sum: 1 },
      DERIVED_winners_in_decade: {
        $sum: { $cond: ["$is_winner_flag", 1, 0] }
      },
      DERIVED_distinct_artists: { $addToSet: "$primary_artist_id" },
      min_year: { $min: "$nomination_year" },
      max_year: { $max: "$nomination_year" }
    }
  },
  {
    $project: {
      _id: 0,
      category_id: "$_id.category_id",
      decade_label: { $concat: [{ $toString: "$_id.decade" }, "s"] },
      DERIVED_nominations_count: "$DERIVED_nominations_in_decade",
      DERIVED_winners_count: "$DERIVED_winners_in_decade",
      DERIVED_distinct_artists_count: { $size: "$DERIVED_distinct_artists" },
      DERIVED_decade_span: {
        $concat: [{ $toString: "$min_year" }, " - ", { $toString: "$max_year" }]
      },
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },
  { $sort: { category_id: 1, decade_label: 1 } },
  { $limit: 6 }
];

printjson(dbNom.nomination_entries.aggregate(pipe05).toArray());

// ----------------------------------------------------------------------------
// 6. ARTISTS APPEARING IN MULTIPLE CATEGORIES (grammy_nominations_db)
// Demonstrates: $match, $group, $project, post-$match, $sort, $limit
// ----------------------------------------------------------------------------
print("\n[PIPELINE 06] Artists Appearing in Multiple Categories (grammy_nominations_db.nomination_entries)");
const pipe06 = [
  { $match: { primary_artist_id: { $exists: true, $ne: null } } },
  {
    $group: {
      _id: "$primary_artist_id",
      artist_billing_title: { $first: "$entry_billing_title" },
      categories_set: { $addToSet: "$category_id" },
      years_set: { $addToSet: "$nomination_year" },
      DERIVED_total_nominations: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      artist_id: "$_id",
      artist_billing_title: 1,
      DERIVED_distinct_categories_count: { $size: "$categories_set" },
      DERIVED_distinct_categories_list: "$categories_set",
      DERIVED_distinct_years_count: { $size: "$years_set" },
      DERIVED_total_nominations: 1,
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },
  { $match: { DERIVED_distinct_categories_count: { $gt: 1 } } },
  { $sort: { DERIVED_distinct_categories_count: -1, DERIVED_total_nominations: -1 } },
  { $limit: 5 }
];

printjson(dbNom.nomination_entries.aggregate(pipe06).toArray());

// ----------------------------------------------------------------------------
// 7. MULTI-TIME WINNERS & REPEAT RECIPIENTS (grammy_winners_db)
// Demonstrates: $match, $group, post-$match, $lookup, $project, $sort, $count
// ----------------------------------------------------------------------------
print("\n[PIPELINE 07] Multi-Time Winners & Repeat Recipients (grammy_winners_db.winner_records)");
const pipe07 = [
  { $match: { primary_artist_id: { $exists: true, $ne: null } } },
  {
    $group: {
      _id: "$primary_artist_id",
      DERIVED_career_wins_count: { $sum: 1 },
      DERIVED_total_statuettes: { $sum: "$trophy_statuettes_awarded_count" },
      DERIVED_winning_ceremonies: { $addToSet: "$ceremony_id" },
      DERIVED_winning_categories: { $addToSet: "$category_id" }
    }
  },
  { $match: { DERIVED_career_wins_count: { $gt: 1 } } },
  {
    $lookup: {
      from: "consecutive_winners",
      localField: "_id",
      foreignField: "artist_id",
      as: "streak_records"
    }
  },
  {
    $project: {
      _id: 0,
      artist_id: "$_id",
      DERIVED_career_wins_count: 1,
      DERIVED_total_statuettes: 1,
      DERIVED_distinct_ceremonies_count: { $size: "$DERIVED_winning_ceremonies" },
      DERIVED_distinct_categories_count: { $size: "$DERIVED_winning_categories" },
      DERIVED_has_consecutive_streaks: { $gt: [{ $size: "$streak_records" }, 0] },
      DERIVED_consecutive_streaks_count: { $size: "$streak_records" },
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },
  { $sort: { DERIVED_career_wins_count: -1, DERIVED_total_statuettes: -1 } },
  { $limit: 5 }
];

printjson(dbWin.winner_records.aggregate(pipe07).toArray());

// $count Operator Demonstration on Multi-Time Winners Stream
print("\n[OPERATOR DEMO: $count] Total Multi-Time Winners Count");
const pipeCount = [
  { $match: { primary_artist_id: { $exists: true, $ne: null } } },
  { $group: { _id: "$primary_artist_id", wins: { $sum: 1 } } },
  { $match: { wins: { $gt: 1 } } },
  { $count: "DERIVED_total_multi_time_winners_count" }
];

printjson(dbWin.winner_records.aggregate(pipeCount).toArray());

// ----------------------------------------------------------------------------
// 8. SPEECH ACKNOWLEDGMENTS DISTRIBUTION (grammy_winners_db)
// Demonstrates: $match, $unwind, $group, $project, $sort
// ----------------------------------------------------------------------------
print("\n[PIPELINE 08] Speech Acknowledgments Distribution (grammy_winners_db.acceptance_speeches)");
const pipe08 = [
  { $match: { individuals_acknowledged: { $exists: true, $type: "array", $ne: [] } } },
  { $unwind: "$individuals_acknowledged" },
  {
    $group: {
      _id: "$individuals_acknowledged",
      DERIVED_acknowledgment_frequency: { $sum: 1 },
      DERIVED_avg_speech_duration_seconds: { $avg: "$speech_duration_seconds" },
      DERIVED_distinct_speakers: { $addToSet: "$primary_speaker_creator_id" },
      DERIVED_speeches_with_social_message: {
        $sum: { $cond: ["$social_political_message_flag", 1, 0] }
      }
    }
  },
  {
    $project: {
      _id: 0,
      acknowledged_entity: "$_id",
      DERIVED_acknowledgment_frequency: 1,
      DERIVED_avg_duration_sec: {
        $round: ["$DERIVED_avg_speech_duration_seconds", 2]
      },
      DERIVED_distinct_speakers_count: { $size: "$DERIVED_distinct_speakers" },
      DERIVED_speeches_with_social_message: 1,
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },
  { $sort: { DERIVED_acknowledgment_frequency: -1 } }
];

printjson(dbWin.acceptance_speeches.aggregate(pipe08).toArray());

// ----------------------------------------------------------------------------
// 9. VENUE HOSTING & CAPACITY ANALYTICS (grammy_history_db)
// Demonstrates: $match, $lookup, $unwind, $group, $project, $sort
// ----------------------------------------------------------------------------
print("\n[PIPELINE 09] Venue Hosting & Capacity Analytics (grammy_history_db.ceremonies)");
const dbHis = db.getSiblingDB("grammy_history_db");
const pipe09 = [
  { $match: { venue_id: { $exists: true, $ne: null } } },
  {
    $lookup: {
      from: "venues",
      localField: "venue_id",
      foreignField: "venue_id",
      as: "venue_details"
    }
  },
  { $unwind: "$venue_details" },
  {
    $group: {
      _id: {
        venue_id: "$venue_details.venue_id",
        venue_name: "$venue_details.venue_name",
        city: "$venue_details.city",
        state: "$venue_details.state"
      },
      DERIVED_ceremonies_hosted_count: { $sum: 1 },
      DERIVED_earliest_edition: { $min: "$edition_number" },
      DERIVED_latest_edition: { $max: "$edition_number" },
      DERIVED_venue_capacity: { $first: "$venue_details.capacity" }
    }
  },
  {
    $project: {
      _id: 0,
      venue_id: "$_id.venue_id",
      venue_name: "$_id.venue_name",
      city: "$_id.city",
      state: "$_id.state",
      DERIVED_ceremonies_hosted_count: 1,
      DERIVED_earliest_edition: 1,
      DERIVED_latest_edition: 1,
      DERIVED_venue_capacity: 1,
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },
  { $sort: { DERIVED_ceremonies_hosted_count: -1, DERIVED_venue_capacity: -1 } }
];

printjson(dbHis.ceremonies.aggregate(pipe09).toArray());

// ----------------------------------------------------------------------------
// 10. CATEGORY RESTRUCTURE & LINEAGE ANALYTICS (grammy_categories_db)
// Demonstrates: $match, $unwind, $group, $project, $sort, $count
// ----------------------------------------------------------------------------
print("\n[PIPELINE 10] Category Restructure & Lineage Analytics (grammy_categories_db.merged_split_history)");
const dbCat = db.getSiblingDB("grammy_categories_db");
const pipe10 = [
  { $match: { primary_category_id: { $exists: true, $ne: null } } },
  { $unwind: "$source_category_ids" },
  {
    $group: {
      _id: "$primary_category_id",
      DERIVED_merged_source_categories_count: { $sum: 1 },
      DERIVED_distinct_source_categories: { $addToSet: "$source_category_ids" },
      DERIVED_restructure_events: { $addToSet: "$event_id" }
    }
  },
  {
    $project: {
      _id: 0,
      primary_category_id: "$_id",
      DERIVED_merged_source_categories_count: 1,
      DERIVED_distinct_sources_count: { $size: "$DERIVED_distinct_source_categories" },
      DERIVED_events_count: { $size: "$DERIVED_restructure_events" },
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },
  { $sort: { DERIVED_merged_source_categories_count: -1 } },
  { $limit: 5 }
];

printjson(dbCat.merged_split_history.aggregate(pipe10).toArray());

print("\n==================================================================");
print("ALL AGGREGATION PIPELINES EXECUTED SUCCESSFULLY");
print("==================================================================");
