/**
 * ============================================================================
 * AGGREGATION PIPELINE 05: CATEGORY TRENDS
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
 *   Tracks longitudinal trends and evolutions across the General Field
 *   categories (Record of the Year, Album of the Year, Song of the Year,
 *   Best New Artist) bucketed by decade, measuring candidate volume,
 *   winner counts, and unique artist representation over time.
 * ============================================================================
 */

const db = db.getSiblingDB("grammy_nominations_db");

const pipeline = [
  // Stage 1: $match - Filter for the Big Four General Field categories
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

  // Stage 2: $group - Compound group by category ID and mathematical decade bucket
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

  // Stage 3: $project - Format decade label, compute distinct counts, and label DERIVED
  {
    $project: {
      _id: 0,
      category_id: "$_id.category_id",
      decade_label: {
        $concat: [{ $toString: "$_id.decade" }, "s"]
      },
      DERIVED_nominations_count: "$DERIVED_nominations_in_decade",
      DERIVED_winners_count: "$DERIVED_winners_in_decade",
      DERIVED_distinct_artists_count: { $size: "$DERIVED_distinct_artists" },
      DERIVED_decade_span: {
        $concat: [{ $toString: "$min_year" }, " - ", { $toString: "$max_year" }]
      },
      DERIVED_calculation_status: { $literal: "DERIVED" }
    }
  },

  // Stage 4: $sort - Sort by category and chronological decade
  {
    $sort: {
      category_id: 1,
      decade_label: 1
    }
  }
];

const results = db.nomination_entries.aggregate(pipeline).toArray();
printjson(results);
