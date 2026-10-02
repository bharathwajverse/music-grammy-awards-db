/**
 * ============================================================================
 * AGGREGATION PIPELINE 02: WINS PER ARTIST
 * ============================================================================
 * Database Scope: grammy_winners_db
 * Primary Collection: winner_records
 * Foreign Collection: acceptance_speeches (Intra-database $lookup)
 * 
 * Demonstrated Operators:
 *   - $match
 *   - $lookup
 *   - $group
 *   - $project
 *   - $sort
 *   - $limit
 * 
 * Calculated Metrics Label: DERIVED
 * Description:
 *   Aggregates total Grammy Award victories per artist from official winner
 *   records, calculating cumulative trophy statuettes, live telecast presentations,
 *   speeches delivered, and distinct winning categories.
 * ============================================================================
 */

const db = db.getSiblingDB("grammy_winners_db");

const pipeline = [
  // Stage 1: $match - Filter for populated artist identifiers
  {
    $match: {
      primary_artist_id: { $exists: true, $ne: null }
    }
  },

  // Stage 2: $lookup - Join with acceptance speeches collection
  {
    $lookup: {
      from: "acceptance_speeches",
      localField: "winner_record_id",
      foreignField: "winner_record_id",
      as: "speech_records"
    }
  },

  // Stage 3: $group - Aggregate cumulative wins and trophy tallies per artist
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

  // Stage 4: $project - Structure derived metrics and calculate average statuettes per win
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

  // Stage 5: $sort - Sort by total wins descending, then cumulative statuettes descending
  {
    $sort: {
      DERIVED_total_wins: -1,
      DERIVED_total_statuettes_awarded: -1
    }
  },

  // Stage 6: $limit - Retrieve top 10 winning artists
  {
    $limit: 10
  }
];

const results = db.winner_records.aggregate(pipeline).toArray();
printjson(results);
