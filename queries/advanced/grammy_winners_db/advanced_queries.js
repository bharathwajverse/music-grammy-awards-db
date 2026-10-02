// ==============================================================================
// Database: grammy_winners_db
// Domain: Winner Records, Speeches, Winning Streaks, Press Releases, Hall of Fame
// Phase 19: Advanced MongoDB Queries & Complex Operators
// ==============================================================================

const db = db.getSiblingDB("grammy_winners_db");

print("==================================================================");
print("ADVANCED QUERIES: grammy_winners_db (Member 4: Winners)");
print("==================================================================");

// ------------------------------------------------------------------------------
// 1. COMPARISON: $eq (Equality)
// Identify award presentations delivered live on primetime telecast.
// Relational Algebra equivalent: \sigma_{presented_live_on_telecast = true}(winner_records)
// ------------------------------------------------------------------------------
print("\n--- 1. Query: $eq (Presented Live on Telecast = true) ---");
db.winner_records.find(
  { presented_live_on_telecast: { $eq: true } },
  { _id: 0, winner_record_id: 1, winning_work_id: 1, trophy_statuettes_awarded_count: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 2. COMPARISON: $ne (Inequality)
// Awards where statuette count differs from a single solitary trophy (!= 1).
// Relational Algebra equivalent: \sigma_{trophy_statuettes_awarded_count \ne 1}(winner_records)
// ------------------------------------------------------------------------------
print("\n--- 2. Query: $ne (Statuettes Awarded Count != 1) ---");
db.winner_records.find(
  { trophy_statuettes_awarded_count: { $ne: 1 } },
  { _id: 0, winner_record_id: 1, winning_work_id: 1, trophy_statuettes_awarded_count: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 3. COMPARISON: $gt (Greater Than)
// Speeches extending beyond 95 seconds in duration.
// Relational Algebra equivalent: \sigma_{speech_duration_seconds > 95}(acceptance_speeches)
// ------------------------------------------------------------------------------
print("\n--- 3. Query: $gt (Speech Duration Seconds > 95) ---");
db.acceptance_speeches.find(
  { speech_duration_seconds: { $gt: 95 } },
  { _id: 0, speech_id: 1, speech_duration_seconds: 1, playoff_music_interrupted: 1 }
).sort({ speech_duration_seconds: -1 }).limit(3);

// ------------------------------------------------------------------------------
// 4. COMPARISON: $gte (Greater Than or Equal)
// Consecutive winning streaks spanning 3 or more years.
// Relational Algebra equivalent: \sigma_{streak_span_years \ge 3}(consecutive_winners)
// ------------------------------------------------------------------------------
print("\n--- 4. Query: $gte (Streak Span Years >= 3) ---");
db.consecutive_winners.find(
  { streak_span_years: { $gte: 3 } },
  { _id: 0, streak_id: 1, creator_id: 1, category_id: 1, streak_span_years: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 5. COMPARISON: $lt (Less Than)
// Historic recordings released prior to 1945 inducted into Hall of Fame.
// Relational Algebra equivalent: \sigma_{original_release_year < 1945}(hall_of_fame_inductions)
// ------------------------------------------------------------------------------
print("\n--- 5. Query: $lt (Original Release Year < 1945) ---");
db.hall_of_fame_inductions.find(
  { original_release_year: { $lt: 1945 } },
  { _id: 0, induction_id: 1, inducted_work_title: 1, original_release_year: 1 }
).sort({ original_release_year: 1 }).limit(3);

// ------------------------------------------------------------------------------
// 6. COMPARISON: $lte (Less Than or Equal)
// Concise acceptance speeches delivered in 96 seconds or less.
// Relational Algebra equivalent: \sigma_{speech_duration_seconds \le 96}(acceptance_speeches)
// ------------------------------------------------------------------------------
print("\n--- 6. Query: $lte (Speech Duration Seconds <= 96) ---");
db.acceptance_speeches.find(
  { speech_duration_seconds: { $lte: 96 } },
  { _id: 0, speech_id: 1, speech_duration_seconds: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 7. COMPARISON: $in (Set Membership)
// Consecutive winning streaks in General Field categories.
// Relational Algebra equivalent: \sigma_{category_id \in \{Record, Album, Song\}}(consecutive_winners)
// ------------------------------------------------------------------------------
print("\n--- 7. Query: $in (General Field Category Streaks) ---");
db.consecutive_winners.find(
  {
    category_id: {
      $in: [
        "CAT_RECORD_OF_THE_YEAR_000",
        "CAT_ALBUM_OF_THE_YEAR_001",
        "CAT_SONG_OF_THE_YEAR_002"
      ]
    }
  },
  { _id: 0, streak_id: 1, creator_id: 1, category_id: 1, streak_span_years: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 8. COMPARISON: $nin (Set Non-Membership)
// Awards where statuette count is outside standard low values [1, 2].
// Relational Algebra equivalent: \sigma_{trophy_statuettes_awarded_count \notin \{1, 2\}}(winner_records)
// ------------------------------------------------------------------------------
print("\n--- 8. Query: $nin (Trophies NOT in [1, 2]) ---");
db.winner_records.find(
  { trophy_statuettes_awarded_count: { $nin: [1, 2] } },
  { _id: 0, winner_record_id: 1, trophy_statuettes_awarded_count: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 9. LOGICAL: $and (Conjunction)
// Telecast presentations where an acceptance speech was delivered live.
// Relational Algebra equivalent: \sigma_{(presented_live = true) \land (acceptance_delivered = true)}(winner_records)
// ------------------------------------------------------------------------------
print("\n--- 9. Query: $and (Live Telecast AND Acceptance Speech Delivered) ---");
db.winner_records.find(
  {
    $and: [
      { presented_live_on_telecast: { $eq: true } },
      { acceptance_speech_delivered: { $eq: true } }
    ]
  },
  { _id: 0, winner_record_id: 1, winning_work_id: 1, trophy_statuettes_awarded_count: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 10. LOGICAL: $or (Disjunction)
// Speeches interrupted by playoff music OR addressing social/political messages.
// Relational Algebra equivalent: \sigma_{(playoff_interrupted = true) \lor (social_message = true)}(acceptance_speeches)
// ------------------------------------------------------------------------------
print("\n--- 10. Query: $or (Music Interrupted OR Social Message) ---");
db.acceptance_speeches.find(
  {
    $or: [
      { playoff_music_interrupted: { $eq: true } },
      { social_political_message_flag: { $eq: true } }
    ]
  },
  { _id: 0, speech_id: 1, playoff_music_interrupted: 1, social_political_message_flag: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 11. LOGICAL: $not (Negation)
// Winning streaks where span is NOT less than 2 years.
// Relational Algebra equivalent: \sigma_{\neg (streak_span_years < 2)}(consecutive_winners)
// ------------------------------------------------------------------------------
print("\n--- 11. Query: $not (NOT streak_span_years < 2) ---");
db.consecutive_winners.find(
  { streak_span_years: { $not: { $lt: 2 } } },
  { _id: 0, streak_id: 1, streak_span_years: 1, creator_id: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 12. ARRAYS: acceptance_speeches & winner_press_releases
// ------------------------------------------------------------------------------
print("\n--- 12. Query: Arrays in acceptance_speeches and winner_press_releases ---");

// 12a. Array Containment on individuals_acknowledged
print("  [12a] Array Containment: individuals_acknowledged contains 'Family'");
db.acceptance_speeches.find(
  { individuals_acknowledged: "Family" },
  { _id: 0, speech_id: 1, individuals_acknowledged: 1 }
).limit(3);

// 12b. Array $all on individuals_acknowledged
print("  [12b] Array $all: individuals_acknowledged contains BOTH 'Record Label' and 'Fans'");
db.acceptance_speeches.find(
  { individuals_acknowledged: { $all: ["Record Label", "Fans"] } },
  { _id: 0, speech_id: 1, individuals_acknowledged: 1 }
).limit(3);

// 12c. Array $size on individuals_acknowledged
print("  [12c] Array $size: speeches acknowledging exactly 4 distinct entities");
db.acceptance_speeches.find(
  { individuals_acknowledged: { $size: 4 } },
  { _id: 0, speech_id: 1, individuals_acknowledged: 1 }
).limit(3);

// 12d. Array Containment on winner_press_releases.syndication_wire_distribution
print("  [12d] Array Containment: syndication_wire_distribution contains 'Associated Press'");
db.winner_press_releases.find(
  { syndication_wire_distribution: "Associated Press" },
  { _id: 0, release_id: 1, syndication_wire_distribution: 1 }
).limit(3);

// 12e. Array Positional Index (.0)
print("  [12e] Array Positional Index (.0): first acknowledged party equals 'Record Label'");
db.acceptance_speeches.find(
  { "individuals_acknowledged.0": "Record Label" },
  { _id: 0, speech_id: 1, "individuals_acknowledged.0": 1 }
).limit(2);

// ------------------------------------------------------------------------------
// 13. EMBEDDED DOCUMENTS: Dot Notation on _source_provenance
// ------------------------------------------------------------------------------
print("\n--- 13. Query: Embedded Documents in winner_records ---");
db.winner_records.find(
  { "_source_provenance.license_type": { $regex: "Public Domain" } },
  { _id: 0, winner_record_id: 1, "_source_provenance.source_name": 1, "_source_provenance.license_type": 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 14. CURSOR CLAUSES: Compound sort, skip, limit, projection
// ------------------------------------------------------------------------------
print("\n--- 14. Query: Cursor Clauses (Sort, Skip, Limit, Projection) ---");
db.winner_records.find(
  { presented_live_on_telecast: true },
  { _id: 0, winner_record_id: 1, winning_work_id: 1, trophy_statuettes_awarded_count: 1 }
)
.sort({ trophy_statuettes_awarded_count: -1, winner_record_id: 1 })
.skip(2)
.limit(4);
