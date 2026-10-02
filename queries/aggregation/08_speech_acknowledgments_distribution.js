/**
 * ============================================================================
 * AGGREGATION PIPELINE 08: ACCEPTANCE SPEECH ACKNOWLEDGMENTS DISTRIBUTION
 * ============================================================================
 * Database Scope: grammy_winners_db
 * Primary Collection: acceptance_speeches
 * 
 * Demonstrated Operators:
 *   - $match
 *   - $unwind (Array unwinding of acknowledged entities)
 *   - $group
 *   - $project
 *   - $sort
 * 
 * Calculated Metrics Label: DERIVED
 * Description:
 *   Unwinds the individuals_acknowledged array in acceptance speeches to compute
 *   frequency distribution of acknowledged parties (e.g. Family, Fans, Label,
 *   Collaborators) alongside average speech delivery durations.
 * ============================================================================
 */

const db = db.getSiblingDB("grammy_winners_db");

const pipeline = [
  // Stage 1: $match - Filter for valid speeches with acknowledged entities
  {
    $match: {
      individuals_acknowledged: { $exists: true, $type: "array", $ne: [] }
    }
  },

  // Stage 2: $unwind - Flatten the array of acknowledged entity strings
  {
    $unwind: "$individuals_acknowledged"
  },

  // Stage 3: $group - Group by acknowledged entity type
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

  // Stage 4: $project - Structure metrics and label DERIVED
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

  // Stage 5: $sort - Rank by acknowledgment frequency descending
  {
    $sort: {
      DERIVED_acknowledgment_frequency: -1
    }
  }
];

const results = db.acceptance_speeches.aggregate(pipeline).toArray();
printjson(results);
