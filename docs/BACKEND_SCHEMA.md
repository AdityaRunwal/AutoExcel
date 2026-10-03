# AutoExcel — Backend & Database Schema

## 1. Purpose

This document defines the current backend structure, API endpoints, data-processing flow, and PostgreSQL database schema used by AutoExcel.

The schema is based on the current implementation of the project.

---

# 2. Backend Architecture

The current backend architecture is:

```text
Frontend
   ↓
FastAPI
   ↓
Route Layer
   ↓
Dataset Processing
   ↓
Operation Detection
   ↓
Operation Execution
   ↓
Cleaning Summary
   ↓
PostgreSQL
   ↓
Cleaned File
```

The backend is implemented using:

- Python
- FastAPI
- pandas
- SQLAlchemy
- PostgreSQL
- openpyxl
- Uvicorn

---

# 3. PostgreSQL Database

Database name:

```text
autoexcel
```

PostgreSQL is used to store cleaning history and related application metadata.

The current database implementation does not require separate user, file, job, operation, and execution-log tables.

The main persistent table currently used by AutoExcel is:

```text
cleaning_history
```

---

# 4. Cleaning History Table

Table name:

```text
cleaning_history
```

Purpose:

Stores information about completed AutoExcel cleaning operations.

## Columns

| Column     | Type        | Purpose                               |
| ---------- | ----------- | ------------------------------------- |
| id         | Integer     | Unique record ID                      |
| filename   | String      | Name of the uploaded dataset          |
| prompt     | String/Text | Natural-language cleaning instruction |
| operations | String/Text | Operations detected and executed      |
| status     | String      | Cleaning status                       |
| created_at | DateTime    | Date and time of the cleaning request |

---

# 5. Cleaning History Model

The SQLAlchemy model is represented conceptually as:

```text
CleaningHistory
│
├── id
├── filename
├── prompt
├── operations
├── status
└── created_at
```

Example record:

```text
id:
1

filename:
AutoExcel_Test_Data.csv

prompt:
Remove duplicate rows

operations:
remove_duplicates

status:
completed

created_at:
2026-09-21 10:08:01
```

---

# 6. Cleaning History Flow

When a cleaning request is successfully completed:

```text
User uploads file
        ↓
User enters prompt
        ↓
Backend detects operations
        ↓
Backend applies operations
        ↓
Cleaning summary generated
        ↓
CleaningHistory record created
        ↓
Record saved in PostgreSQL
```

---

# 7. Backend Route Structure

The current backend contains route modules for different backend responsibilities.

Current route structure:

```text
backend/
│
└── app/
    │
    ├── routes/
    │   ├── upload.py
    │   ├── clean.py
    │   └── ai_clean.py
    │
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py
```

---

# 8. Upload API

## POST `/upload`

Purpose:

Uploads and analyzes an Excel or CSV dataset.

Supported files:

```text
.xlsx
.xls
.csv
```

### Request

The request uses:

```text
multipart/form-data
```

with:

```text
file
```

### Processing

The backend:

1. Receives the uploaded file.
2. Determines the file extension.
3. Reads the dataset using pandas.
4. Calculates dataset information.
5. Generates a dataset preview.
6. Returns the analysis as JSON.

---

# 9. Upload API Response

The `/upload` endpoint provides dataset information including:

```text
filename
rows
columns
column_names
data_types
missing_values
total_missing_values
duplicate_rows
empty_rows
empty_columns
preview
```

Example structure:

```json
{
    "filename": "AutoExcel_Test_Data.csv",
    "rows": 10,
    "columns": 7,
    "column_names": [
        "Name",
        "Age",
        "City"
    ],
    "data_types": {},
    "total_missing_values": 6,
    "duplicate_rows": 1,
    "empty_rows": 0,
    "empty_columns": 0,
    "preview": []
}
```

The exact response fields may evolve as the backend is improved.

---

# 10. AI Cleaning API

AutoExcel uses a two-step plan-then-execute flow (added in Phase 6/7), not a single direct-clean call.

## POST `/preview-plan`

Purpose:

Builds and validates a cleaning plan from the prompt, without executing anything. Used to show the user a "AI Cleaning Plan" review screen before any changes are made.

### Request

```text
file
prompt
```

Both submitted using `multipart/form-data`.

### Response

```json
{
    "steps": [
        { "operation": "remove_duplicates", "description": "Remove duplicate rows" }
    ],
    "skipped_steps": [],
    "has_plan": true,
    "clarification_needed": false,
    "message": ""
}
```

If no operation is detected, or every detected operation fails validation, `has_plan` is `false`, `clarification_needed` is `true`, and `message` explains why (see Section 15).

## POST `/ai-clean`

Purpose:

Re-builds and re-validates the same plan, then actually executes it and returns the cleaned file. Called only after the user clicks "Apply Plan" on the reviewed plan from `/preview-plan`.

### Request

```text
file
prompt
```

Both submitted using `multipart/form-data`.

# 11. AI Cleaning Processing Flow

The `/ai-clean` endpoint follows this flow:

```text
Receive File
      ↓
Identify File Type
      ↓
Read Dataset
      ↓
Analyze Before-Cleaning State
      ↓
Read User Prompt
      ↓
Detect Supported Operations
      ↓
Check Whether Operations Exist
      ↓
Apply Operations
      ↓
Analyze After-Cleaning State
      ↓
Generate Cleaning Summary
      ↓
Save Cleaning History
      ↓
Create Cleaned Output File
      ↓
Return Cleaned File
```

---

# 12. Supported File Processing

For Excel files:

```text
.xlsx
.xls
```

the backend uses pandas Excel reading and OpenPyXL for `.xlsx` output.

For CSV files:

```text
.csv
```

the backend uses:

```python
pd.read_csv()
```

and:

```python
df.to_csv()
```

for output.

---

# 13. Operation Detection

The backend contains a `detect_operations()` function.

Its purpose is to convert natural-language instructions into internal operation names.

Example:

```text
User prompt:

Remove duplicate rows and remove extra spaces.
```

Detected operations:

```text
remove_duplicates
remove_extra_spaces
```

The operation detector uses predefined supported phrases and keywords.

---

# 14. Current Operation Names

The current backend supports:

```text
remove_duplicates
fill_missing_mean
fill_missing_median
fill_missing_mode
remove_empty_rows
remove_empty_columns
standardize_columns
remove_negative_values
remove_extra_spaces
remove_missing
convert_numeric
remove_duplicate_columns
replace_negative_with_mean
remove_invalid_rows
standardize_text_lower
standardize_text_upper
standardize_text_title
standardize_dates
filter_rows
sort_data
rename_columns
create_calculated_column
group_summarize
create_summary_sheet
```

This list includes both the original Phase 1–5 operations and the 12 operations added in Phase 6 (plan-based detectors). Only operations implemented by the backend should be executed.

---

# 15. No-Operation / Clarification Responses

There are two places this can happen, with different response shapes.

## On `/preview-plan`

If no operation is detected, or every detected operation is skipped during validation:

```json
{
    "has_plan": false,
    "clarification_needed": true,
    "message": "I couldn't understand any specific cleaning operation in that prompt. Try being more specific, e.g. 'remove duplicates', 'fill missing values with mean', or 'sort by Salary descending'."
}
```

If operations were detected but all failed column validation, the message is instead built from the skip reasons, e.g.:

```json
{
    "has_plan": false,
    "clarification_needed": true,
    "message": "None of the requested operations could be applied: Column 'Salry' not found"
}
```

An empty or whitespace-only prompt is rejected the same way, before detection even runs.

## On `/ai-clean`

If no valid operations remain after validation at execution time, the backend returns:

```json
{
    "status": "no_operation",
    "message": "No supported cleaning operation was detected.",
    "prompt": "user prompt",
    "suggestions": [
        "Remove duplicate rows",
        "Fill missing values with mean",
        "Remove empty rows",
        "Remove extra spaces",
        "Standardize column names"
    ]
}
```

In normal usage this path is rarely reached, since `/preview-plan` already catches this case first and the user only clicks "Apply Plan" once a non-empty plan is shown.

The frontend uses these responses to display helpful messages/suggestions to the user instead of silently failing.

---

# 16. Cleaning Summary

After successful processing, the backend creates a cleaning summary.

The summary contains:

```text
before
after
changes
operations
```

## Before

Contains:

```text
rows
columns
missing_values
duplicate_rows
```

## After

Contains:

```text
rows
columns
missing_values
duplicate_rows
```

## Changes

Contains:

```text
rows_removed
columns_removed
missing_values_changed
duplicates_removed
```

## Operations

Contains the operations executed during cleaning.

## Validation (added in Phase 7)

Contains a result-validation verdict, generated by `validate_result()` after execution:

```json
{
    "status": "passed",
    "warnings": []
}
```

If an expected change didn't happen (e.g. "remove duplicates" was requested but no duplicates were actually removed), or if any steps were skipped during validation, `status` becomes `"warning"` and `warnings` lists the specific issues.

## Skipped Steps (added in Phase 6)

If any requested operations were skipped because a referenced column didn't exist, `cleaning_summary["skipped_steps"]` is included, listing each skipped operation and the reason.

---

# 17. Latest Summary Storage

The latest cleaning summary is temporarily stored in the backend using:

```text
latest_summary
```

The summary is updated after a successful cleaning operation.

It is used by the `/summary` endpoint.

This is temporary application state and is not currently stored as a separate database record.

---

# 18. Summary API

## GET `/summary`

Purpose:

Returns the latest cleaning summary.

Example structure:

```json
{
    "before": {
        "rows": 10,
        "columns": 7,
        "missing_values": 6,
        "duplicate_rows": 1
    },
    "after": {
        "rows": 9,
        "columns": 7,
        "missing_values": 6,
        "duplicate_rows": 0
    },
    "changes": {
        "rows_removed": 1,
        "columns_removed": 0,
        "missing_values_changed": 0,
        "duplicates_removed": 1
    },
    "operations": [
        "remove_duplicates"
    ]
}
```

---

# 19. History API

## GET `/history`

Purpose:

Returns the cleaning history stored in PostgreSQL.

Each history record contains:

```text
id
filename
prompt
operations
status
created_at
```

The frontend displays this information in the Cleaning History table.

---

# 20. Database Connection

The database connection is handled through:

```text
app/database.py
```

SQLAlchemy is used to create the database engine and session.

The application uses:

```text
SessionLocal
```

to interact with PostgreSQL.

---

# 21. Database Session Flow

The general database flow is:

```text
API Request
    ↓
Create Database Session
    ↓
Perform Database Operation
    ↓
Commit Changes
    ↓
Close Database Session
```

For example, after successful cleaning:

```text
Cleaning Completed
       ↓
Create CleaningHistory object
       ↓
db.add()
       ↓
db.commit()
       ↓
db.close()
```

---

# 22. Output File Storage

Cleaned files are currently stored in:

```text
data/
```

The backend creates the directory if it does not already exist.

Example:

```text
data/
│
├── cleaned_AutoExcel_Test_Data.csv
└── cleaned_test_data.xlsx
```

The original uploaded file is not overwritten by the cleaning operation.

---

# 23. Output File Generation

For CSV files:

```python
df.to_csv(
    output_file,
    index=False
)
```

For Excel files:

```python
df.to_excel(
    output_file,
    index=False,
    engine="openpyxl"
)
```

The backend returns the resulting file using FastAPI's `FileResponse`.

---

# 24. Frontend ↔ Backend Communication

The frontend communicates with the backend using JavaScript's Fetch API.

Backend base URL during local development:

```text
http://127.0.0.1:8000
```

Examples:

```text
POST /upload
POST /ai-clean
GET /summary
GET /history
```

The frontend development server runs separately.

Example:

```text
http://127.0.0.1:3000
```

CORS is configured so that the frontend can communicate with the FastAPI backend.

---

# 25. Error Handling

The backend should return appropriate errors for:

- Unsupported file extensions
- Unable to read datasets
- Invalid files
- Cleaning failures
- Database failures
- Output file failures

FastAPI `HTTPException` is used for backend request errors.

Example:

```text
400 Bad Request
```

may be returned when the uploaded file type is unsupported or cannot be read.

---

# 26. JSON Serialization

Dataset information returned by `/upload` must be JSON serializable.

Pandas datasets may contain values such as:

```text
NaN
```

which cannot always be returned directly in a JSON response.

Therefore, preview and other dataset information must be converted into JSON-safe values before being returned by FastAPI.

This is particularly important for datasets containing missing values.

---

# 27. Current API Summary

| Method | Endpoint        | Purpose                                         |
| ------ | --------------- | ------------------------------------------------ |
| GET    | `/`             | Health check — confirms API is running          |
| GET    | `/db-test`      | Confirms PostgreSQL connection is working        |
| POST   | `/upload`       | Upload and analyze dataset                      |
| POST   | `/preview-plan` | Build and validate a cleaning plan (no execution)|
| POST   | `/ai-clean`     | Execute the approved plan and clean the dataset  |
| GET    | `/summary`      | Get latest cleaning summary                      |
| GET    | `/history`      | Get cleaning history                             |

---

# 28. Current Database Summary

The current persistent database structure is:

```text
PostgreSQL
    │
    └── cleaning_history
            │
            ├── id
            ├── filename
            ├── prompt
            ├── operations
            ├── status
            └── created_at
```

---

# 29. Current Backend Limitations

The current version does not contain separate database tables for:

- Users
- Uploaded files
- Jobs
- Individual operations
- Execution logs

These were part of the earlier planned architecture but are not required by the current implementation.

They may be introduced in a future version if the application requires:

- User accounts
- Multiple users
- Job management
- Detailed execution tracking
- Advanced audit logs
- Cloud file management

---

# 30. Backend Design Principle

AutoExcel follows this backend principle:

> **"Keep the backend controlled, simple, explainable, and expandable."**

The backend should:

1. Accept the dataset.
2. Analyze the dataset.
3. Understand supported cleaning instructions.
4. Execute controlled operations.
5. Generate a clear summary.
6. Store cleaning history.
7. Return the cleaned dataset.