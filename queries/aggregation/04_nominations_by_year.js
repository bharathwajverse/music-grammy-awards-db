/**
 * ============================================================================
 * AGGREGATION PIPELINE 04: NOMINATIONS BY YEAR
 * ============================================================================
 * Database Scope: grammy_nominations_db
 * Primary Collection: nomination_entries
 * 
 * Demonstrated Operators:
 *   - $match
 *   - $group
 *   - $project
 *   - $sort
 * 
 * Calculated Metrics Label: DERIVED
 * Description:
 *   Examines temporal expansion of Grammy nominations year by year, computing
 *   total competitive slots, winner-to-nominee distribution, distinct categories
 *   contested, and average ballot slot depth.
 * ============================================================================
 */

const db = db.getSiblingDB("grammy_nominations_db");

const pipeline = [
  // Stage 1: $match - Filter for historical ceremonies starting with inaugural year (1958/1959)
  {
    $match: {
      nomination_year: { $exists: true, $gte: 1958 }
    }
  },

  // Stage 2: $group - Group nominations by ceremony year
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

  // Stage 3: $project - Structure chronological timeline metrics
  {
    $project: {
      _id: 0,
      ceremony_year: "$_id",
      DERIVED_total_nominations: 1,
      DERIVED_total_winners: 1,
      DERIVED_distinct_categories_count: { $size: "$DERIVED_distinct_categories" },
      DERIVED_distinct_nominees_count: { $size: "$DERIVED_distinct_nominees" },
      DERIVED_avg_slot_depth: {
        $round: ["$DERIVED_average_ballot_slot", 2]
      },
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },

  // Stage 4: $sort - Order chronologically by ceremony year ascending
  {
    $sort: {
      ceremony_year: 1
    }
  }
];

const results = db.nomination_entries.aggregate(pipeline).toArray();
printjson(results);
