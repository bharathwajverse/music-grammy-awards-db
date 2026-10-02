// ==============================================================================
// Database: grammy_history_db
// Domain: Ceremonies, Telecasts, Venues, Hosts, and Viewership Ratings
// Phase 19: Advanced MongoDB Queries & Complex Operators
// ==============================================================================

const db = db.getSiblingDB("grammy_history_db");

print("==================================================================");
print("ADVANCED QUERIES: grammy_history_db (Member 1: History)");
print("==================================================================");

// ------------------------------------------------------------------------------
// 1. COMPARISON: $eq (Equality)
// Find ceremonies broadcast on CBS.
// Relational Algebra equivalent: \sigma_{primary_network = 'CBS'}(ceremonies)
// ------------------------------------------------------------------------------
print("\n--- 1. Query: $eq (Broadcast Network = CBS) ---");
db.ceremonies.find(
  { primary_network: { $eq: "CBS" } },
  { _id: 0, ceremony_id: 1, edition_number: 1, broadcast_year: 1, primary_network: 1, host_city: 1 }
).sort({ broadcast_year: -1 }).limit(3);

// ------------------------------------------------------------------------------
// 2. COMPARISON: $ne (Not Equal)
// Find premier venues located outside the central Los Angeles metropolis.
// Relational Algebra equivalent: \sigma_{city \ne 'Los Angeles'}(venues)
// ------------------------------------------------------------------------------
print("\n--- 2. Query: $ne (Venue City != Los Angeles) ---");
db.venues.find(
  { city: { $ne: "Los Angeles" } },
  { _id: 0, venue_id: 1, venue_name: 1, city: 1, state: 1, max_seating_capacity: 1 }
).sort({ max_seating_capacity: -1 }).limit(3);

// ------------------------------------------------------------------------------
// 3. COMPARISON: $gt (Greater Than)
// Identify modern 21st-century ceremony telecasts broadcast after the year 2010.
// Relational Algebra equivalent: \sigma_{broadcast_year > 2010}(ceremonies)
// ------------------------------------------------------------------------------
print("\n--- 3. Query: $gt (Broadcast Year > 2010) ---");
db.ceremonies.find(
  { broadcast_year: { $gt: 2010 } },
  { _id: 0, ceremony_id: 1, broadcast_year: 1, host_city: 1, total_awards_presented: 1 }
).sort({ broadcast_year: 1 }).limit(3);

// ------------------------------------------------------------------------------
// 4. COMPARISON: $gte (Greater Than or Equal)
// Retrieve Nielsen ratings broadcasts with 20.0 million or more US viewers.
// Relational Algebra equivalent: \sigma_{us_viewers_millions \ge 20.0}(viewership_ratings)
// ------------------------------------------------------------------------------
print("\n--- 4. Query: $gte (US Viewers >= 20.0 Million) ---");
db.viewership_ratings.find(
  { us_viewers_millions: { $gte: 20.0 } },
  { _id: 0, rating_id: 1, ceremony_id: 1, us_viewers_millions: 1, household_rating_pct: 1 }
).sort({ us_viewers_millions: -1 }).limit(3);

// ------------------------------------------------------------------------------
// 5. COMPARISON: $lt (Less Than)
// Historical early golden era telecasts broadcast before the year 1970.
// Relational Algebra equivalent: \sigma_{broadcast_year < 1970}(ceremonies)
// ------------------------------------------------------------------------------
print("\n--- 5. Query: $lt (Broadcast Year < 1970) ---");
db.ceremonies.find(
  { broadcast_year: { $lt: 1970 } },
  { _id: 0, ceremony_id: 1, edition_number: 1, broadcast_year: 1, venue_id: 1 }
).sort({ edition_number: 1 }).limit(3);

// ------------------------------------------------------------------------------
// 6. COMPARISON: $lte (Less Than or Equal)
// Retrieve the inaugural decade of Grammy editions (Edition 1 through 10).
// Relational Algebra equivalent: \sigma_{edition_number \le 10}(ceremonies)
// ------------------------------------------------------------------------------
print("\n--- 6. Query: $lte (Edition Number <= 10) ---");
db.ceremonies.find(
  { edition_number: { $lte: 10 } },
  { _id: 0, ceremony_id: 1, edition_number: 1, ceremony_date: 1, primary_network: 1 }
).sort({ edition_number: 1 }).limit(3);

// ------------------------------------------------------------------------------
// 7. COMPARISON: $in (Contained in Set)
// Venues situated in designated entertainment capitals: Beverly Hills or Los Angeles.
// Relational Algebra equivalent: \sigma_{city \in \{'Beverly Hills', 'Los Angeles'\}}(venues)
// ------------------------------------------------------------------------------
print("\n--- 7. Query: $in (City in ['Beverly Hills', 'Los Angeles']) ---");
db.venues.find(
  { city: { $in: ["Beverly Hills", "Los Angeles"] } },
  { _id: 0, venue_id: 1, venue_name: 1, city: 1, max_seating_capacity: 1 }
).sort({ max_seating_capacity: -1 }).limit(3);

// ------------------------------------------------------------------------------
// 8. COMPARISON: $nin (Not Contained in Set)
// Ceremonies on networks other than commercial syndicates ABC or FOX.
// Relational Algebra equivalent: \sigma_{primary_network \notin \{'ABC', 'FOX'\}}(ceremonies)
// ------------------------------------------------------------------------------
print("\n--- 8. Query: $nin (Primary Network not in ['ABC', 'FOX']) ---");
db.ceremonies.find(
  { primary_network: { $nin: ["ABC", "FOX"] } },
  { _id: 0, ceremony_id: 1, broadcast_year: 1, primary_network: 1 }
).sort({ broadcast_year: 1 }).limit(3);

// ------------------------------------------------------------------------------
// 9. LOGICAL: $and (Logical Conjunction)
// Modern CBS broadcasts presenting over 80 awards.
// Relational Algebra equivalent: \sigma_{(broadcast_year \ge 2000) \land (primary_network = 'CBS') \land (total_awards_presented > 80)}(ceremonies)
// ------------------------------------------------------------------------------
print("\n--- 9. Query: $and (Year >= 2000 AND Network = CBS AND Awards > 80) ---");
db.ceremonies.find(
  {
    $and: [
      { broadcast_year: { $gte: 2000 } },
      { primary_network: { $eq: "CBS" } },
      { total_awards_presented: { $gt: 80 } }
    ]
  },
  { _id: 0, ceremony_id: 1, broadcast_year: 1, primary_network: 1, total_awards_presented: 1 }
).sort({ broadcast_year: -1 }).limit(3);

// ------------------------------------------------------------------------------
// 10. LOGICAL: $or (Logical Disjunction)
// Major venues accommodating >= 10,000 attendees OR located in Beverly Hills.
// Relational Algebra equivalent: \sigma_{(max_seating_capacity \ge 10000) \lor (city = 'Beverly Hills')}(venues)
// ------------------------------------------------------------------------------
print("\n--- 10. Query: $or (Capacity >= 10000 OR City = Beverly Hills) ---");
db.venues.find(
  {
    $or: [
      { max_seating_capacity: { $gte: 10000 } },
      { city: { $eq: "Beverly Hills" } }
    ]
  },
  { _id: 0, venue_id: 1, venue_name: 1, city: 1, max_seating_capacity: 1 }
).sort({ max_seating_capacity: -1 }).limit(4);

// ------------------------------------------------------------------------------
// 11. LOGICAL: $not (Logical Negation)
// Select ceremonies where total awards presented is NOT less than 50.
// Relational Algebra equivalent: \sigma_{\neg (total_awards_presented < 50)}(ceremonies)
// ------------------------------------------------------------------------------
print("\n--- 11. Query: $not (NOT total_awards_presented < 50) ---");
db.ceremonies.find(
  { total_awards_presented: { $not: { $lt: 50 } } },
  { _id: 0, ceremony_id: 1, edition_number: 1, total_awards_presented: 1 }
).sort({ total_awards_presented: 1 }).limit(3);

// ------------------------------------------------------------------------------
// 12. CURSOR CLAUSES: sort, limit, skip, and projection (Deterministic Pagination)
// Retrieves page 2 (items 6–10) of modern ceremonies sorted chronologically descending.
// Relational Algebra equivalent: \pi_{ceremony_id, broadcast_year, host_city}(\sigma_{broadcast_year \ge 1990}(ceremonies))
// ------------------------------------------------------------------------------
print("\n--- 12. Query: Cursor Methods (Sort, Skip, Limit, Projection) ---");
db.ceremonies.find(
  { broadcast_year: { $gte: 1990 } },
  { _id: 0, ceremony_id: 1, edition_number: 1, broadcast_year: 1, host_city: 1, primary_network: 1 }
)
.sort({ broadcast_year: -1 })
.skip(5)
.limit(5);

// ------------------------------------------------------------------------------
// 13. EMBEDDED DOCUMENTS: Dot Notation Navigation
// Querying nested provenance subdocuments (_source_provenance) for official archive tier.
// ------------------------------------------------------------------------------
print("\n--- 13. Query: Embedded Documents (Dot Notation on _source_provenance) ---");
db.ceremonies.find(
  {
    "_source_provenance.source_id": { $eq: "SRC-01" },
    "_source_provenance.provenance_tier": { $eq: "PRIMARY OFFICIAL SOURCE" }
  },
  { _id: 0, ceremony_id: 1, edition_number: 1, "_source_provenance.source_name": 1, "_source_provenance.provenance_tier": 1 }
).limit(3);
