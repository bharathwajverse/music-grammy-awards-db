/**
 * ============================================================================
 * AGGREGATION PIPELINE 10: CATEGORY RESTRUCTURE & LINEAGE ANALYTICS
 * ============================================================================
 * Database Scope: grammy_categories_db
 * Primary Collection: merged_split_history
 * 
 * Demonstrated Operators:
 *   - $match
 *   - $unwind (Array unwinding of source categories)
 *   - $group
 *   - $project
 *   - $sort
 *   - $count
 * 
 * Calculated Metrics Label: DERIVED
 * Description:
 *   Analyzes Academy restructuring events by unwinding source category
 *   arrays, computing reorganization frequencies per target category, and
 *   demonstrating the $count stage for total restructuring occurrences.
 * ============================================================================
 */

const db = db.getSiblingDB("grammy_categories_db");

// Pipeline A: Reorganization frequency per target category
const restructurePipeline = [
  // Stage 1: $match - Filter for populated primary categories
  {
    $match: {
      primary_category_id: { $exists: true, $ne: null }
    }
  },

  // Stage 2: $unwind - Flatten the source_category_ids array
  {
    $unwind: "$source_category_ids"
  },

  // Stage 3: $group - Group by primary category ID
  {
    $group: {
      _id: "$primary_category_id",
      DERIVED_merged_source_categories_count: { $sum: 1 },
      DERIVED_distinct_source_categories: { $addToSet: "$source_category_ids" },
      DERIVED_restructure_events: { $addToSet: "$event_id" }
    }
  },

  // Stage 4: $project - Structure metrics and label DERIVED
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

  // Stage 5: $sort - Rank by merged source count descending
  {
    $sort: {
      DERIVED_merged_source_categories_count: -1
    }
  }
];

// Pipeline B: $count stage demonstration counting total restructure source mappings
const countPipeline = [
  { $unwind: "$source_category_ids" },
  { $count: "DERIVED_total_source_category_mappings" }
];

print("--- CATEGORY RESTRUCTURE FREQUENCY PER TARGET ---");
const results = db.merged_split_history.aggregate(restructurePipeline).toArray();
printjson(results);

print("--- TOTAL SOURCE CATEGORY MAPPINGS COUNT ($count demonstration) ---");
const countResults = db.merged_split_history.aggregate(countPipeline).toArray();
printjson(countResults);
