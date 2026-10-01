# MongoDB Physical Schema Validators (`$jsonSchema`)

> **Course**: Advanced Database Management Systems (ADBMS)  
> **System**: GRAMMY Awards Information & Analytics System  
> **Phase**: Phase 11 — MongoDB Document Model Design  
> **Directory**: `mongodb/schema/`  
> **Target Databases**: 5 databases, 10 collections each (50 total collections)  

---

## 1. Directory Structure

This directory contains native MongoDB collection validator definitions in `$jsonSchema` format for all 50 collections across the five project databases.

```text
mongodb/schema/
├── grammy_history_db/        # 10 collection validator JSON files
├── grammy_categories_db/     # 10 collection validator JSON files
├── grammy_nominations_db/    # 10 collection validator JSON files
├── grammy_winners_db/        # 10 collection validator JSON files
└── grammy_creators_db/       # 10 collection validator JSON files
```

---

## 2. Validator Format Specification

Every JSON file in this directory follows the official MongoDB `$jsonSchema` specification used during `db.createCollection()` or `collMod`:

```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "title": "<database_name>.<collection_name>",
    "description": "MongoDB collection validator for <collection_name>",
    "required": ["_id", "domain_primary_key", ...],
    "properties": {
      "_id": {
        "bsonType": "string",
        "description": "Universal primary document identifier"
      },
      ...
    },
    "additionalProperties": true
  }
}
```

---

## 3. Database Collection Coverage

| Database Name | Collections | Minimum Fields | Validator Location |
| :--- | :---: | :---: | :--- |
| **`grammy_history_db`** | 10 | 11–14 | [`grammy_history_db/`](./grammy_history_db/) |
| **`grammy_categories_db`** | 10 | 11–14 | [`grammy_categories_db/`](./grammy_categories_db/) |
| **`grammy_nominations_db`** | 10 | 11–14 | [`grammy_nominations_db/`](./grammy_nominations_db/) |
| **`grammy_winners_db`** | 10 | 11–15 | [`grammy_winners_db/`](./grammy_winners_db/) |
| **`grammy_creators_db`** | 10 | 11–15 | [`grammy_creators_db/`](./grammy_creators_db/) |

---

## 4. Applying Validators to MongoDB Atlas / Compass

To apply a schema validator during collection creation via the MongoDB Node/Python shell:

```python
import json
from pymongo import MongoClient

client = MongoClient("mongodb+srv://...")
db = client["grammy_history_db"]

with open("mongodb/schema/grammy_history_db/ceremonies.json") as f:
    validator = json.load(f)

db.create_collection("ceremonies", validator=validator)
```
