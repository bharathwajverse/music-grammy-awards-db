/**
 * ============================================================================
 * AGGREGATION PIPELINE 06: ARTISTS APPEARING IN MULTIPLE CATEGORIES
 * ============================================================================
 * Database Scope: grammy_nominations_db
 * Primary Collection: nomination_entries
 * 
 * Demonstrated Operators:
 *   - $match (initial and post-group filtering)
 *   - $group
 *   - $project
 *   - $sort
 *   - $limit
 * 
 * Calculated Metrics Label: DERIVED
 * Description:
 *   Identifies versatile recording artists who have secured nominations across
 *   two or more distinct Grammy Award categories, calculating unique category
 *   diversity sets, active ceremony year ranges, and total career nominations.
 * ============================================================================
 */

const db = db.getSiblingDB("grammy_nominations_db");

const pipeline = [
  // Stage 1: $match - Filter for populated artist identifiers
  {
    $match: {
      primary_artist_id: { $exists: true, $ne: null }
    }
  },

  // Stage 2: $group - Collect distinct categories and years per artist
  {
    $group: {
      _id: "$primary_artist_id",
      artist_billing_title: { $first: "$entry_billing_title" },
      categories_set: { $addToSet: "$category_id" },
      years_set: { $addToSet: "$nomination_year" },
      DERIVED_total_nominations: { $sum: 1 }
    }
  },

  // Stage 3: $project - Compute set sizes and prepare for diversity filtering
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

  // Stage 4: $match - Filter exclusively for artists with nominations in multiple categories (> 1)
  {
    $match: {
      DERIVED_distinct_categories_count: { $gt: 1 }
    }
  },

  // Stage 5: $sort - Rank by category diversity descending, then total nominations descending
  {
    $sort: {
      DERIVED_distinct_categories_count: -1,
      DERIVED_total_nominations: -1
    }
  },

  // Stage 6: $limit - Retrieve top 15 most versatile cross-category artists
  {
    $limit: 15
  }
];

const results = db.nomination_entries.aggregate(pipeline).toArray();
printjson(results);
