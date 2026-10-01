# First Normal Form (1NF) Specification & Transformation

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 9 — Schema Normalization Proofs  
> **Document**: First Normal Form (1NF) Formal Definition, Unnormalized Raw Data Analysis, Atomicity Violations, and Decomposition  
> **Status**: Completed  
> **Theoretical Framework**: E.F. Codd (1970) / Elmasri & Navathe (*Fundamentals of Database Systems*, 7th Edition, Chapter 14)  
> **Related Artifacts**:  
> - 2NF Transformation: [`normalization/2nf.md`](./2nf.md)  
> - Normalization Summary: [`normalization/normalization-summary.md`](./normalization-summary.md)  
> - Functional Dependencies: [`normalization/functional-dependencies.md`](./functional-dependencies.md)  

---

## 1. Formal Theoretical Definition of First Normal Form (1NF)

According to E.F. Codd (1970):
> A relation schema $R$ is in **First Normal Form (1NF)** if and only if all underlying attribute domains contain only **atomic (indivisible) values**, and the value of any attribute in a tuple is a **single value** from the domain of that attribute.

### 1.1. Core Mathematical Properties of 1NF:
1. **Domain Atomicity**: For every attribute $A \in R$, every value $v \in dom(A)$ is considered indivisible by the relational database management system.
2. **No Repeating Groups**: Tuples cannot contain variable-length lists, sets, or nested repeating groups.
3. **No Multivalued Arrays**: Attributes cannot store comma-delimited strings, nested collections, or JSON arrays inside a single column cell.
4. **Tuple Uniqueness**: Every relation must have a unique identifier (candidate key) that distinguishes each tuple from all other tuples.

---

## 2. The Unnormalized Starting Structure ($\mathcal{U}_{\text{UNF}}$)

Prior to database normalization, legacy music catalogs and raw telecast logs frequently capture GRAMMY event and nomination data as denormalized flat files or CSV spreadsheets with composite and multivalued fields.

### 2.1. Starting Schema Formulation:
$$\mathcal{U}_{\text{UNF}}(\text{ceremony\_edition}, \text{ceremony\_date}, \text{venue\_full\_address}, \text{co\_hosts}, \text{category\_name}, \text{field\_info},$$
$$\text{work\_title}, \text{genres}, \text{release\_label\_info}, \text{credited\_talent\_roster}, \text{is\_winner}, \text{trophy\_details})$$

### 2.2. Sample Raw Unnormalized Tuple:

```text
[Tuple 1]:
ceremony_edition:        65 (2023)
ceremony_date:           "February 5, 2023"
venue_full_address:      "Crypto.com Arena, 1111 S Figueroa St, Los Angeles, CA 90015, Capacity: 20000"
co_hosts:                {"Trevor Noah", "James Corden", "Alicia Keys"}  [MULTIVALUED ARRAY]
category_name:           "Album of the Year"
field_info:              "General Field (Code: GEN, Curator: Recording Academy Trustees)"
work_title:              "Renaissance"
genres:                  {"Dance", "Electronic", "House", "R&B"}  [MULTIVALUED SET]
release_label_info:      "Parkwood Entertainment / Columbia Records (Sony Music)"
credited_talent_roster:  [REPEATING GROUP]:
                         {
                           ("Beyoncé Knowles-Carter", "Lead Artist / Producer", 85.0%),
                           ("The-Dream", "Songwriter / Co-Producer", 40.0%),
                           ("Mike Dean", "Mastering Engineer", 100.0%),
                           ("Honey Dijon", "Featured Producer", 15.0%)
                         }
is_winner:               TRUE
trophy_details:          "Serial: TRP_2023_AOTY_001, Material: Grammium Zinc Alloy, Plating: 24k Gold 5.0µm"
```

---

## 3. Identification of 1NF Violations

The unnormalized structure $\mathcal{U}_{\text{UNF}}$ exhibits four distinct violations of First Normal Form:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   1NF VIOLATION AUDIT IN RAW DATA                                      │
├─────┬──────────────────────────┬────────────────────────────┬──────────────────────────────────────────┤
│ No. │ Attribute                │ Anomaly Type               │ Violation Description                    │
├─────┼──────────────────────────┼────────────────────────────┼──────────────────────────────────────────┤
│ 1   │ credited_talent_roster   │ Repeating Group            │ Nested relation containing variable-     │
│     │                          │ (Non-Flat Relation)        │ length arrays of craft personnel credits.│
├─────┼──────────────────────────┼────────────────────────────┼──────────────────────────────────────────┤
│ 2   │ co_hosts, genres         │ Multivalued Attribute Set  │ Comma-separated or array values within   │
│     │                          │ ({v_1, v_2, ..., v_k})     │ a single scalar table column cell.       │
├─────┼──────────────────────────┼────────────────────────────┼──────────────────────────────────────────┤
│ 3   │ venue_full_address       │ Composite Attribute        │ String concatenating name, street, city, │
│     │                          │ (Name + City + State + Cap)│ state, zip, and max capacity.            │
├─────┼──────────────────────────┼────────────────────────────┼──────────────────────────────────────────┤
│ 4   │ field_info, label_info,  │ Composite Semi-Structured  │ Multiple distinct domain attributes      │
│     │ trophy_details           │ Concatenation              │ merged into unstructured text blocks.    │
└─────┴──────────────────────────┴────────────────────────────┴──────────────────────────────────────────┘
```

### 3.1. Detailed Operational Hazards of Non-1NF Schemas:
1. **Query Inefficiency**: To search for nominations where "Mike Dean" acted as Mastering Engineer, the query engine must perform slow full-table string pattern scans (`LIKE '%Mike Dean%'`) across the `credited_talent_roster` text column.
2. **Aggregations Blocked**: Calculating the total number of distinct genres represented across Album of the Year nominees is impossible using standard relational algebra projection without non-standard string splitting.
3. **Loss of Integrity Constraints**: Individual capacity integers (`20000`) cannot have SQL `CHECK (max_seating_capacity > 0)` constraints applied when embedded inside street address text strings.

---

## 4. 1NF Decomposition & Normalization Transformation

To achieve First Normal Form, all composite attributes are decomposed into atomic attributes, and all repeating groups/multivalued sets are converted into separate rows or independent relations.

### 4.1. Step 1: Flattening Composite Attributes into Atomic Scalar Domains
- `venue_full_address` decomposes into atomic fields:
  - `venue_id: VARCHAR(32)`
  - `venue_name: VARCHAR(128)`
  - `street_address: VARCHAR(255)`
  - `city: VARCHAR(64)`
  - `state: VARCHAR(32)`
  - `postal_code: VARCHAR(16)`
  - `max_seating_capacity: INT`
- `field_info` decomposes into:
  - `field_id: VARCHAR(32)`
  - `field_name: VARCHAR(64)`
  - `field_abbreviation: VARCHAR(16)`
  - `field_curator_role: VARCHAR(64)`
- `trophy_details` decomposes into:
  - `trophy_id: VARCHAR(32)`
  - `statuette_serial_number: VARCHAR(64)`
  - `grammium_alloy_specification: VARCHAR(64)`
  - `gold_plating_thickness_microns: NUMERIC(4,2)`

### 4.2. Step 2: Eliminating Repeating Groups and Multivalued Sets
Each repeating group and multivalued array is extracted into its own first-class relation with a composite key linking back to the parent entity:
- Multivalued `co_hosts` $\implies$ `ceremony_hosts(\underline{\text{host\_record\_id}}, \text{ceremony\_id}, \text{host\_name}, \dots)$
- Multivalued `genres` $\implies$ `genre_classifications(\underline{\text{classification\_id}}, \text{work\_id}, \text{primary\_genre\_tag}, \dots)$
- Repeating `credited_talent_roster` $\implies$ `nomination_credits(\underline{\text{credit\_id}}, \text{nomination\_id}, \text{creator\_id}, \text{credit\_role}, \text{contribution\_percentage})$

---

## 5. Resulting 1NF Relational Representation

Following 1NF normalization, the database consists exclusively of flat relations with atomic attributes:

$$\mathcal{R}_{\text{1NF\_FLAT}}(\underline{\text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{creator\_id}, \text{credit\_role}},$$
$$\text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{venue\_name}, \text{city}, \text{state}, \text{max\_seating\_capacity}, \text{primary\_network},$$
$$\text{category\_name}, \text{standard\_short\_code}, \text{field\_id}, \text{field\_name},$$
$$\text{work\_title}, \text{work\_type}, \text{commercial\_release\_date}, \text{label\_id}, \text{label\_name},$$
$$\text{creator\_legal\_name}, \text{stage\_name}, \text{country\_of\_citizenship}, \text{contribution\_percentage},$$
$$\text{nomination\_id}, \text{ballot\_slot\_order}, \text{is\_winner\_flag})$$

---

## 6. Identification of Keys and Functional Dependencies in 1NF

### 6.1. Candidate Keys and Primary Key for $\mathcal{R}_{\text{1NF\_FLAT}}$:
Because a single creative work competing in a category has multiple credited contributors (artists, producers, mixers), no subset of attributes without the contributor and craft role can uniquely identify a tuple.
- **Candidate Key 1 (Designated Primary Key)**:
  $$PK = CK_1 = \{ \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{creator\_id}, \text{credit\_role} \}$$
- **Candidate Key 2**:
  $$CK_2 = \{ \text{nomination\_id}, \text{creator\_id}, \text{credit\_role} \}$$

### 6.2. Functional Dependencies Holding in 1NF:
1. $FD_1: \text{ceremony\_id} \to \text{edition\_number}, \text{ceremony\_date}, \text{broadcast\_year}, \text{venue\_id}, \text{primary\_network}$
2. $FD_2: \text{venue\_id} \to \text{venue\_name}, \text{city}, \text{state}, \text{max\_seating\_capacity}$
3. $FD_3: \text{category\_id} \to \text{category\_name}, \text{standard\_short\_code}, \text{field\_id}$
4. $FD_4: \text{field\_id} \to \text{field\_name}$
5. $FD_5: \text{work\_id} \to \text{work\_title}, \text{work\_type}, \text{commercial\_release\_date}, \text{label\_id}$
6. $FD_6: \text{label\_id} \to \text{label\_name}$
7. $FD_7: \text{creator\_id} \to \text{creator\_legal\_name}, \text{stage\_name}, \text{country\_of\_citizenship}$
8. $FD_8: \text{nomination\_id} \to \text{ceremony\_id}, \text{category\_id}, \text{work\_id}, \text{ballot\_slot\_order}, \text{is\_winner\_flag}$
9. $FD_9: \text{ceremony\_id}, \text{category\_id}, \text{work\_id} \to \text{nomination\_id}, \text{ballot\_slot\_order}, \text{is\_winner\_flag}$
10. $FD_{10}: \text{nomination\_id}, \text{creator\_id}, \text{credit\_role} \to \text{contribution\_percentage}$

---

## 7. Validity of 1NF Transformation

### 7.1. Information Equivalence and Lossless Property:
The transformation from $\mathcal{U}_{\text{UNF}}$ to $\mathcal{R}_{\text{1NF\_FLAT}}$ is strictly **information-preserving and lossless**:
- Every piece of data present in the unnormalized structure is retained in a structured atomic column.
- The decomposition is guaranteed to be a lossless transformation that eliminates repeating groups while maintaining tuple integrity.
- No semantic connections are severed; foreign keys (`venue_id`, `field_id`, `label_id`, `nomination_id`) preserve all contextual relationships.

### 7.2. Why 1NF Alone Is Insufficient:
While $\mathcal{R}_{\text{1NF\_FLAT}}$ guarantees atomic attributes, it suffers from severe redundancy:
- In $CK_2 = \{\text{nomination\_id}, \text{creator\_id}, \text{credit\_role}\}$, non-prime attributes like $\text{work\_title}$ depend solely on $\text{work\_id}$ (which depends on $\text{nomination\_id}$), rather than the whole composite key.
- This represents a **Partial Functional Dependency**, violating **Second Normal Form (2NF)**.
