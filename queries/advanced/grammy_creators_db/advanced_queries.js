// ==============================================================================
// Database: grammy_creators_db
// Domain: Artists, Songwriters, Musical Groups, Collaborations, Producers
// Phase 19: Advanced MongoDB Queries & Complex Operators
// ==============================================================================

const db = db.getSiblingDB("grammy_creators_db");

print("==================================================================");
print("ADVANCED QUERIES: grammy_creators_db (Member 5: Creators/Music)");
print("==================================================================");

// ------------------------------------------------------------------------------
// 1. COMPARISON: $eq (Equality)
// Identify domestic recording artists with citizenship in the United States.
// Relational Algebra equivalent: \sigma_{country_of_citizenship = 'United States'}(artists)
// ------------------------------------------------------------------------------
print("\n--- 1. Query: $eq (Citizenship = United States) ---");
db.artists.find(
  { country_of_citizenship: { $eq: "United States" } },
  { _id: 0, artist_id: 1, full_legal_name: 1, country_of_citizenship: 1, primary_musical_genre: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 2. COMPARISON: $ne (Inequality)
// Identify international recording artists (citizenship outside United States).
// Relational Algebra equivalent: \sigma_{country_of_citizenship \ne 'United States'}(artists)
// ------------------------------------------------------------------------------
print("\n--- 2. Query: $ne (Citizenship != United States) ---");
db.artists.find(
  { country_of_citizenship: { $ne: "United States" } },
  { _id: 0, artist_id: 1, full_legal_name: 1, country_of_citizenship: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 3. COMPARISON: $gt (Greater Than)
// Prolific songwriters with more than 120 registered musical compositions.
// Relational Algebra equivalent: \sigma_{registered_works_count > 120}(songwriters_composers)
// ------------------------------------------------------------------------------
print("\n--- 3. Query: $gt (Registered Works Count > 120) ---");
db.songwriters_composers.find(
  { registered_works_count: { $gt: 120 } },
  { _id: 0, songwriter_id: 1, creator_id: 1, registered_works_count: 1, pro_affiliation: 1 }
).sort({ registered_works_count: -1 }).limit(3);

// ------------------------------------------------------------------------------
// 4. COMPARISON: $gte (Greater Than or Equal)
// Recording artists who commenced active professional careers in 1950 or later.
// Relational Algebra equivalent: \sigma_{active_career_start_year \ge 1950}(artists)
// ------------------------------------------------------------------------------
print("\n--- 4. Query: $gte (Career Start Year >= 1950) ---");
db.artists.find(
  { active_career_start_year: { $gte: 1950 } },
  { _id: 0, artist_id: 1, stage_name: 1, active_career_start_year: 1 }
).sort({ active_career_start_year: 1 }).limit(3);

// ------------------------------------------------------------------------------
// 5. COMPARISON: $lt (Less Than)
// Founding pioneer recording artists active prior to 1955.
// Relational Algebra equivalent: \sigma_{active_career_start_year < 1955}(artists)
// ------------------------------------------------------------------------------
print("\n--- 5. Query: $lt (Career Start Year < 1955) ---");
db.artists.find(
  { active_career_start_year: { $lt: 1955 } },
  { _id: 0, artist_id: 1, stage_name: 1, active_career_start_year: 1 }
).sort({ active_career_start_year: 1 }).limit(3);

// ------------------------------------------------------------------------------
// 6. COMPARISON: $lte (Less Than or Equal)
// Musical groups and ensembles formed on or before 1965.
// Relational Algebra equivalent: \sigma_{formation_calendar_year \le 1965}(musical_groups)
// ------------------------------------------------------------------------------
print("\n--- 6. Query: $lte (Formation Year <= 1965) ---");
db.musical_groups.find(
  { formation_calendar_year: { $lte: 1965 } },
  { _id: 0, group_id: 1, group_name: 1, formation_calendar_year: 1, ensemble_structure_type: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 7. COMPARISON: $in (Set Membership)
// Songwriters affiliated with prime performance rights organizations (ASCAP, BMI).
// Relational Algebra equivalent: \sigma_{pro_affiliation \in \{'ASCAP', 'BMI'\}}(songwriters_composers)
// ------------------------------------------------------------------------------
print("\n--- 7. Query: $in (PRO Affiliation in ASCAP or BMI) ---");
db.songwriters_composers.find(
  { pro_affiliation: { $in: ["ASCAP", "BMI"] } },
  { _id: 0, songwriter_id: 1, pro_affiliation: 1, registered_works_count: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 8. COMPARISON: $nin (Set Non-Membership)
// Recording artists specializing in genres outside mainstream Pop and Rock.
// Relational Algebra equivalent: \sigma_{primary_musical_genre \notin \{'Pop / Vocal', 'Rock'\}}(artists)
// ------------------------------------------------------------------------------
print("\n--- 8. Query: $nin (Genre NOT in Pop or Rock) ---");
db.artists.find(
  { primary_musical_genre: { $nin: ["Pop / Vocal", "Rock"] } },
  { _id: 0, artist_id: 1, stage_name: 1, primary_musical_genre: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 9. LOGICAL: $and (Conjunction)
// Solo recording artists who launched careers in 1950 or later.
// Relational Algebra equivalent: \sigma_{(active_career_start_year \ge 1950) \land (is_group_ensemble_flag = false)}(artists)
// ------------------------------------------------------------------------------
print("\n--- 9. Query: $and (Career Start >= 1950 AND Solo Artist) ---");
db.artists.find(
  {
    $and: [
      { active_career_start_year: { $gte: 1950 } },
      { is_group_ensemble_flag: { $eq: false } }
    ]
  },
  { _id: 0, artist_id: 1, stage_name: 1, active_career_start_year: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 10. LOGICAL: $or (Disjunction)
// Musical groups that are currently active OR structured as Quartets.
// Relational Algebra equivalent: \sigma_{(current_activity_status = true) \lor (structure = 'Quartet')}(musical_groups)
// ------------------------------------------------------------------------------
print("\n--- 10. Query: $or (Active Status OR Quartet Structure) ---");
db.musical_groups.find(
  {
    $or: [
      { current_activity_status: { $eq: true } },
      { ensemble_structure_type: { $eq: "Quartet" } }
    ]
  },
  { _id: 0, group_id: 1, group_name: 1, current_activity_status: 1, ensemble_structure_type: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 11. LOGICAL: $not (Negation)
// Songwriters whose cataloged works count is NOT less than 100.
// Relational Algebra equivalent: \sigma_{\neg (registered_works_count < 100)}(songwriters_composers)
// ------------------------------------------------------------------------------
print("\n--- 11. Query: $not (NOT registered_works < 100) ---");
db.songwriters_composers.find(
  { registered_works_count: { $not: { $lt: 100 } } },
  { _id: 0, songwriter_id: 1, registered_works_count: 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 12. EMBEDDED DOCUMENTS: Dot Notation on _source_provenance
// ------------------------------------------------------------------------------
print("\n--- 12. Query: Embedded Documents in artists ---");
db.artists.find(
  { "_source_provenance.source_id": { $eq: "SRC-03" } },
  { _id: 0, artist_id: 1, stage_name: 1, "_source_provenance.source_name": 1, "_source_provenance.provenance_tier": 1 }
).limit(3);

// ------------------------------------------------------------------------------
// 13. CURSOR CLAUSES: Sort, skip, limit, projection
// ------------------------------------------------------------------------------
print("\n--- 13. Query: Cursor Clauses (Sort, Skip, Limit, Projection) ---");
db.artists.find(
  { is_group_ensemble_flag: false },
  { _id: 0, artist_id: 1, stage_name: 1, primary_musical_genre: 1, active_career_start_year: 1 }
)
.sort({ active_career_start_year: 1, stage_name: 1 })
.skip(2)
.limit(4);
