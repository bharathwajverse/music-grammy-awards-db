/**
 * ============================================================================
 * AGGREGATION PIPELINE 01: NOMINATIONS PER ARTIST
 * ============================================================================
 * Database Scope: grammy_nominations_db
 * Primary Collection: nomination_entries
 * Foreign Collection: nominated_works (Intra-database $lookup)
 * 
 * Demonstrated Operators:
 *   - $match
 *   - $lookup
 *   - $unwind
 *   - $group
 *   - $project
 *   - $sort
 *   - $limit
 * 
 * Calculated Metrics Label: DERIVED
 * Description:
 *   Aggregates total career nominations for each musical artist, joining work
 *   metadata, tracking earliest and latest nomination years to compute career span,
 *   and enumerating distinct nominated categories and works.
 * ============================================================================
 */

const db = db.getSiblingDB("grammy_nominations_db");

const pipeline = [
  // Stage 1: $match - Filter for valid artist records with populated identifiers
  {
    $match: {
      primary_artist_id: { $exists: true, $ne: null }
    }
  },

  // Stage 2: $lookup - Intra-database join with nominated_works on work_id
  {
    $lookup: {
      from: "nominated_works",
      localField: "work_id",
      foreignField: "work_id",
      as: "work_details"
    }
  },

  // Stage 3: $unwind - Flatten joined work details while preserving entries without matching work docs
  {
    $unwind: {
      path: "$work_details",
      preserveNullAndEmptyArrays: true
    }
  },

  // Stage 4: $group - Group nominations by primary artist ID
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

  // Stage 5: $project - Shape output document with explicitly labeled DERIVED analytical metrics
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

  // Stage 6: $sort - Rank artists by derived total nominations descending
  {
    $sort: {
      DERIVED_total_nominations: -1,
      artist_billing_name: 1
    }
  },

  // Stage 7: $limit - Retrieve top 10 most nominated artists
  {
    $limit: 10
  }
];

const results = db.nomination_entries.aggregate(pipeline).toArray();
printjson(results);
