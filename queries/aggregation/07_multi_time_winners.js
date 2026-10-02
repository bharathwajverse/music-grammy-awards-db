/**
 * ============================================================================
 * AGGREGATION PIPELINE 07: MULTI-TIME WINNERS & REPEAT RECIPIENTS
 * ============================================================================
 * Database Scope: grammy_winners_db
 * Primary Collection: winner_records
 * Foreign Collection: consecutive_winners (Intra-database $lookup)
 * 
 * Demonstrated Operators:
 *   - $match (initial and post-group filtering)
 *   - $group
 *   - $lookup
 *   - $project
 *   - $sort
 *   - $limit
 *   - $count (in companion pipeline)
 * 
 * Calculated Metrics Label: DERIVED
 * Description:
 *   Identifies elite recording artists who have won multiple Grammy Awards (> 1 win),
 *   joining consecutive winning streaks, computing career statuette accumulations,
 *   and enumerating distinct ceremony editions where trophies were won.
 * ============================================================================
 */

const db = db.getSiblingDB("grammy_winners_db");

// Pipeline A: Multi-time winners ranked with streak enrichment
const multiTimeWinnersPipeline = [
  // Stage 1: $match - Filter for valid artist records
  {
    $match: {
      primary_artist_id: { $exists: true, $ne: null }
    }
  },

  // Stage 2: $group - Calculate total wins, statuettes, and unique ceremonies/categories
  {
    $group: {
      _id: "$primary_artist_id",
      DERIVED_career_wins_count: { $sum: 1 },
      DERIVED_total_statuettes: { $sum: "$trophy_statuettes_awarded_count" },
      DERIVED_winning_ceremonies: { $addToSet: "$ceremony_id" },
      DERIVED_winning_categories: { $addToSet: "$category_id" }
    }
  },

  // Stage 3: $match - Filter strictly for multi-time winners (> 1 win)
  {
    $match: {
      DERIVED_career_wins_count: { $gt: 1 }
    }
  },

  // Stage 4: $lookup - Join with consecutive_winners collection on artist ID
  {
    $lookup: {
      from: "consecutive_winners",
      localField: "_id",
      foreignField: "artist_id",
      as: "streak_records"
    }
  },

  // Stage 5: $project - Structure derived metrics and annotate calculation status
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

  // Stage 6: $sort - Rank by career wins descending, then total statuettes descending
  {
    $sort: {
      DERIVED_career_wins_count: -1,
      DERIVED_total_statuettes: -1
    }
  },

  // Stage 7: $limit - Retrieve top 10 multi-time winners
  {
    $limit: 10
  }
];

// Pipeline B: $count stage demonstration counting total multi-time winners
const countPipeline = [
  { $match: { primary_artist_id: { $exists: true, $ne: null } } },
  { $group: { _id: "$primary_artist_id", wins: { $sum: 1 } } },
  { $match: { wins: { $gt: 1 } } },
  { $count: "DERIVED_total_multi_time_winners_count" }
];

print("--- MULTI-TIME WINNERS LEADERBOARD ---");
const leaders = db.winner_records.aggregate(multiTimeWinnersPipeline).toArray();
printjson(leaders);

print("--- TOTAL MULTI-TIME WINNERS COUNT ($count demonstration) ---");
const countResult = db.winner_records.aggregate(countPipeline).toArray();
printjson(countResult);
