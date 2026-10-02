/**
 * ============================================================================
 * AGGREGATION PIPELINE 03: WINS BY CATEGORY
 * ============================================================================
 * Database Scope: grammy_winners_db
 * Primary Collection: winner_records
 * 
 * Demonstrated Operators:
 *   - $match
 *   - $group
 *   - $project
 *   - $sort
 *   - $limit
 * 
 * Calculated Metrics Label: DERIVED
 * Description:
 *   Analyzes historical trophy allocation across award categories, computing
 *   total victories, cumulative statuettes awarded, live telecast broadcast
 *   percentages, and distinct winning artists.
 * ============================================================================
 */

const db = db.getSiblingDB("grammy_winners_db");

const pipeline = [
  // Stage 1: $match - Ensure category ID is defined
  {
    $match: {
      category_id: { $exists: true, $ne: null }
    }
  },

  // Stage 2: $group - Aggregate awards by category
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

  // Stage 3: $project - Calculate telecast presentation percentage and format metrics
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
      DERIVED_earliest_ceremony: 1,
      DERIVED_latest_ceremony: 1,
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },

  // Stage 4: $sort - Rank categories by total historical wins descending
  {
    $sort: {
      DERIVED_total_historical_wins: -1,
      DERIVED_cumulative_statuettes: -1
    }
  },

  // Stage 5: $limit - Retrieve top 10 categories
  {
    $limit: 10
  }
];

const results = db.winner_records.aggregate(pipeline).toArray();
printjson(results);
