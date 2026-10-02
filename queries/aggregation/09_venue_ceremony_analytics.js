/**
 * ============================================================================
 * AGGREGATION PIPELINE 09: VENUE HOSTING & CAPACITY ANALYTICS
 * ============================================================================
 * Database Scope: grammy_history_db
 * Primary Collection: ceremonies
 * Foreign Collection: venues (Intra-database $lookup)
 * 
 * Demonstrated Operators:
 *   - $match
 *   - $lookup
 *   - $unwind
 *   - $group
 *   - $project
 *   - $sort
 * 
 * Calculated Metrics Label: DERIVED
 * Description:
 *   Performs a relational join between ceremonies and venues, computing
 *   hosting frequencies, average spectator capacities, and chronological
 *   hosting intervals per venue and host city.
 * ============================================================================
 */

const db = db.getSiblingDB("grammy_history_db");

const pipeline = [
  // Stage 1: $match - Filter for ceremonies with designated venues
  {
    $match: {
      venue_id: { $exists: true, $ne: null }
    }
  },

  // Stage 2: $lookup - Join with venues collection on venue_id
  {
    $lookup: {
      from: "venues",
      localField: "venue_id",
      foreignField: "venue_id",
      as: "venue_details"
    }
  },

  // Stage 3: $unwind - Flatten venue details
  {
    $unwind: "$venue_details"
  },

  // Stage 4: $group - Group by host venue
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

  // Stage 5: $project - Structure metrics and label DERIVED
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

  // Stage 6: $sort - Rank by total ceremonies hosted descending
  {
    $sort: {
      DERIVED_ceremonies_hosted_count: -1,
      DERIVED_venue_capacity: -1
    }
  }
];

const results = db.ceremonies.aggregate(pipeline).toArray();
printjson(results);
