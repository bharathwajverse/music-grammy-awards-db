# Master MongoDB Collection Specifications Catalog

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 11 — MongoDB Document Model Design  
> **Document**: Master Collection Directory for all 50 System Collections across 5 Databases  
> **Status**: Completed  
> **Related Design Guide**: [`docs/mongodb-design.md`](../../docs/mongodb-design.md)  
> **Physical Schemas**: [`mongodb/schema/`](../schema/)  

---

## 1. System Allocation Overview

The physical MongoDB implementation organizes the GRAMMY Awards Information & Analytics System across five dedicated databases. Each database contains exactly **10 collections**, satisfying the academic constraint of **50 total collections**.

Every collection has been audited against the approved Feasibility Matrix (`schemas/collection-feasibility-matrix.csv`) and verified to contain:
- $\ge 50$ legitimate factual documents available.
- $\ge 10$ meaningful domain fields defined with strict BSON typing.
- Explicit source provenance and derived data indicators.
- Deterministic universal `_id` identifiers.

---

## 2. Database Specification Documents

| Database Name | Team Scope | Collections | Key Entities Represented | Detailed Specification |
| :--- | :--- | :---: | :--- | :--- |
| **`grammy_history_db`** | Historical ceremonies, telecasts, venues, ratings, hosts | 10 | Ceremonies, Venues, Broadcasters, Ratings, Hosts, Milestones | [`grammy_history_db.md`](./grammy_history_db.md) |
| **`grammy_categories_db`**| Award taxonomy, fields, lineages, quotas, voting rules | 10 | Fields, Categories, Lineage Nodes, Rules, Quotas, Merges | [`grammy_categories_db.md`](./grammy_categories_db.md) |
| **`grammy_nominations_db`**| Works, nomination ballots, credits, screening, ties | 10 | Nominated Works, Nomination Entries, Credits, Submissions | [`grammy_nominations_db.md`](./grammy_nominations_db.md) |
| **`grammy_winners_db`** | Award winners, sweeps, trophies, streaks, milestones | 10 | Winners, Big Four Sweeps, Trophies, Speeches, Hall of Fame | [`grammy_winners_db.md`](./grammy_winners_db.md) |
| **`grammy_creators_db`** | Artists, producers, engineers, labels, groups, catalogs | 10 | Artists, Producers, Audio Engineers, Labels, Groups, Discographies | [`grammy_creators_db.md`](./grammy_creators_db.md) |

---

## 3. Universal Collection Directory (All 50 Collections)

### 3.1. `grammy_history_db` (10 Collections)
1. [`ceremonies`](./grammy_history_db.md#1-ceremonies): Master historical registry of ceremony editions (67 editions, 1959–2025).
2. [`venues`](./grammy_history_db.md#2-venues): Geographic and architectural profiles of arenas and auditoriums (60+ venues).
3. [`telecast_broadcasters`](./grammy_history_db.md#3-telecast-broadcasters): Media broadcast networks and transmission standards (50+ network feeds).
4. [`viewership_ratings`](./grammy_history_db.md#4-viewership-ratings): Longitudinal Nielsen ratings and broadcast audience metrics (55+ ceremonies).
5. [`ceremony_hosts`](./grammy_history_db.md#5-ceremony-hosts): Broadcast masters of ceremonies and co-hosts (70+ host engagements).
6. [`historic_milestones`](./grammy_history_db.md#6-historic-milestones): Landmark cultural and technological events in GRAMMY history (65+ milestones).
7. [`timeline_historical_eras`](./grammy_history_db.md#7-timeline-historical-eras): Chronological epochs across 6 decades of popular music (50+ era subdivisions).
8. [`academy_leadership`](./grammy_history_db.md#8-academy-leadership): Trustees and presidents directing Academy governance (60+ leader tenures).
9. [`press_media_accreditations`](./grammy_history_db.md#9-press-media-accreditations): Media organizations and accredited press passes (65+ press outlets).
10. [`lifetime_achievement_honors`](./grammy_history_db.md#10-lifetime-achievement-honors): Special Merit Lifetime Achievement Award honorees (180+ honorees).

### 3.2. `grammy_categories_db` (10 Collections)
11. [`award_fields`](./grammy_categories_db.md#1-award-fields): Umbrella genre genres and craft branches (50+ fields).
12. [`award_categories`](./grammy_categories_db.md#2-award-categories): Specific competitive award categories across all eras (550+ categories).
13. [`category_lineage`](./grammy_categories_db.md#3-category-lineage): Genealogical tree tracking category name evolutions (120+ nodes).
14. [`eligibility_rules`](./grammy_categories_db.md#4-eligibility-rules): Qualification standards and playing time benchmarks (75+ rule clauses).
15. [`voting_procedures`](./grammy_categories_db.md#5-voting-procedures): Two-round balloting procedures and ranked-choice tabulation (55+ protocol configs).
16. [`category_quotas_limits`](./grammy_categories_db.md#6-category-quotas-limits): Statutory nominee caps and ballot nomination limits (65+ quota parameters).
17. [`craft_credit_definitions`](./grammy_categories_db.md#7-craft-credit-definitions): Academy rules defining which roles receive statuettes (55+ craft definitions).
18. [`discontinued_categories`](./grammy_categories_db.md#8-discontinued-categories): Retired award categories and deactivation justifications (85+ retired categories).
19. [`merged_split_history`](./grammy_categories_db.md#9-merged-split-history): Historical realignments where categories merged or split (55+ reorganization events).
20. [`special_merit_categories`](./grammy_categories_db.md#10-special-merit-categories): Trustees Award, Technical GRAMMY, and MusiCares definitions (50+ honorary standards).

### 3.3. `grammy_nominations_db` (10 Collections)
21. [`nomination_entries`](./grammy_nominations_db.md#1-nomination-entries): Canonical official nomination ballots across all years (25,000+ nominations).
22. [`nominated_works`](./grammy_nominations_db.md#2-nominated-works): Creative musical singles, albums, videos, and box sets (15,000+ musical works).
23. [`nomination_credits`](./grammy_nominations_db.md#3-nomination-credits): Granular creative contributors on each nomination (40,000+ credit links).
24. [`submission_batches`](./grammy_nominations_db.md#4-submission-batches): Record company and member entry intake batches (65+ intake batches).
25. [`voter_screening_batches`](./grammy_nominations_db.md#5-voter-screening-batches): Screening committee vetting and category placement sessions (60+ screening sessions).
26. [`tied_nominations`](./grammy_nominations_db.md#6-tied-nominations): Ballot ties producing expanded nominee fields (50+ tie events).
27. [`nomination_audit_logs`](./grammy_nominations_db.md#7-nomination-audit-logs): Independent auditor ballot certification logs (Deloitte/PwC) (67+ audit records).
28. [`genre_classifications`](./grammy_nominations_db.md#8-genre-classifications): Multi-dimensional genre taxonomy tags for nominated works (500+ genre mappings).
29. [`first_time_nominees`](./grammy_nominations_db.md#9-first-time-nominees): Breakthrough artists receiving maiden career nominations (350+ breakout artists).
30. [`multi_nomination_packages`](./grammy_nominations_db.md#10-multi-nomination-packages): Works nominated across multiple categories in a single year (250+ packages).

### 3.4. `grammy_winners_db` (10 Collections)
31. [`winner_records`](./grammy_winners_db.md#1-winner-records): Official verified award winners across all categories (9,000+ historical winners).
32. [`big_four_sweeps`](./grammy_winners_db.md#2-big-four-sweeps): Historical sweeps across the General Field (50+ sweep milestones).
33. [`record_breakers`](./grammy_winners_db.md#3-record-breakers): All-time historical GRAMMY records and records broken (60+ benchmark profiles).
34. [`acceptance_speeches`](./grammy_winners_db.md#4-acceptance-speeches): Transcripts and delivery metadata of acceptance speeches (85+ transcripts).
35. [`trophy_tracking`](./grammy_winners_db.md#5-trophy-tracking): Physical statuette manufacturing and delivery logistics (120+ statuettes).
36. [`consecutive_winners`](./grammy_winners_db.md#6-consecutive-winners): Multi-year back-to-back winners across ceremonies (55+ streaks).
37. [`hall_of_fame_inductions`](./grammy_winners_db.md#7-hall-of-fame-inductions): Historic recordings inducted into the GRAMMY Hall of Fame (1,150+ recordings).
38. [`posthumous_awards`](./grammy_winners_db.md#8-posthumous-awards): Honors bestowed after the death of the awarded artist (75+ posthumous honors).
39. [`historic_win_benchmarks`](./grammy_winners_db.md#9-historic-win-benchmarks): Aggregated historical victory norms by genre and decade (60+ benchmark profiles).
40. [`winner_press_releases`](./grammy_winners_db.md#10-winner-press-releases): Official Academy press release bulletins upon presentation (67+ bulletins).

### 3.5. `grammy_creators_db` (10 Collections)
41. [`artists`](./grammy_creators_db.md#1-artists): Solo vocalists, rappers, and performing instrumentalists (500+ prepped artists).
42. [`producers`](./grammy_creators_db.md#2-producers): Record producers, vocal producers, and executive producers (100+ prepped).
43. [`audio_engineers`](./grammy_creators_db.md#3-audio-engineers): Recording, mixing, mastering, and immersive audio engineers (100+ prepped).
44. [`songwriters_composers`](./grammy_creators_db.md#4-songwriters-composers): Lyricists, composers, and songwriters with PRO data (100+ prepped).
45. [`arrangers_conductors`](./grammy_creators_db.md#5-arrangers-conductors): Orchestral arrangers, string arrangers, and conductors (80+ prepped).
46. [`record_labels`](./grammy_creators_db.md#6-record-labels): Commercial record labels, imprints, and distribution groups (100+ prepped).
47. [`musical_groups`](./grammy_creators_db.md#7-musical-groups): Bands, duos, vocal ensembles, orchestras, and choirs (100+ prepped).
48. [`group_memberships`](./grammy_creators_db.md#8-group-memberships): Historical tenures linking artists into musical groups (120+ prepped).
49. [`creator_collaborations`](./grammy_creators_db.md#9-creator-collaborations): Recurrent artistic and production creative partnerships (150+ partnerships).
50. [`creator_discographies`](./grammy_creators_db.md#10-creator-discographies): Released master musical albums and singles by creators (1,000+ catalog entries).

---

## 4. Verification Against Feasibility Matrix

All 50 collections strictly comply with the feasibility criteria:
$$\forall c \in \text{Collections}, \quad \text{Documents}(c) \ge 50 \quad \land \quad \text{Fields}(c) \ge 10$$

Zero collections require replacement or synthetic placeholders.
