# AutoExcel — Technical Requirements Document (TRD)

## 1. Technical Overview

AutoExcel is a full-stack web application for natural-language-based spreadsheet data cleaning.

The system allows users to:

- Upload Excel or CSV datasets
- Analyze uploaded datasets
- View dataset information and preview
- Enter natural-language cleaning instructions
- Detect supported cleaning operations
- Execute controlled data-cleaning operations
- Generate before/after cleaning summaries
- Store cleaning history in PostgreSQL
- Download the cleaned dataset

The system uses a frontend application, a FastAPI backend, pandas for data processing, and PostgreSQL for persistent cleaning history.

---

# 2. Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript

The frontend is served locally using a simple HTTP server.

Example:

```text
http://127.0.0.1:3000
```

## Backend

- Python
- FastAPI
- Uvicorn

The backend runs locally using:

```text
http://127.0.0.1:8000
```

## Data Processing

- pandas

Pandas is responsible for:

- Reading datasets
- Analyzing datasets
- Detecting missing values
- Detecting duplicate rows
- Applying cleaning operations
- Generating cleaned datasets

## Excel Processing

- openpyxl

OpenPyXL is used for Excel `.xlsx` file processing and output generation.

## CSV Processing

- pandas CSV reader/writer

CSV files are processed using pandas.

## Database

- PostgreSQL
- SQLAlchemy

PostgreSQL stores cleaning history and related application information.

## API Testing

FastAPI's Swagger documentation can be used to test backend endpoints.

The main API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Version Control

Git will be used for version control.

GitHub publication will be performed after the project is completed and tested.

---

# 3. High-Level Architecture

The current AutoExcel architecture is:

```text
User
  ↓
HTML/CSS/JavaScript Frontend
  ↓
FastAPI Backend
  ↓
File Processing
  ↓
Dataset Analysis
  ↓
Natural-Language Prompt
  ↓
Operation Detection
  ↓
Controlled Cleaning Operations
  ↓
Cleaning Summary
  ↓
PostgreSQL Cleaning History
  ↓
Cleaned Dataset
  ↓
Download
```

The frontend communicates with the FastAPI backend through HTTP requests.

---

# 4. Architecture Principles

## Principle 1 — Controlled Operations

User prompts are used to identify supported cleaning operations.

The system does not execute arbitrary Python code generated from user input.

Each cleaning operation is implemented as controlled backend logic.

---

## Principle 2 — Supported Operations Only

The backend must execute only operations that are explicitly supported by AutoExcel.

If a prompt does not contain a supported operation, the system must not perform an unsupported action.

---

## Principle 3 — Original File Protection

The uploaded file must not be modified directly.

Cleaning operations should create a separate cleaned output file.

Example:

```text
Original:
sales.csv

Output:
cleaned_sales.csv
```

---

## Principle 4 — Clear User Feedback

The system should provide understandable feedback for:

- Successful uploads
- Invalid files
- Unsupported operations
- Processing errors
- Successful cleaning
- Download availability

---

## Principle 5 — Expandability

The cleaning-operation architecture should allow additional operations to be added later without redesigning the entire backend.

---

# 5. Backend Components

## API Layer

The FastAPI API layer is responsible for:

- Receiving uploaded files
- Reading datasets
- Returning dataset information
- Processing cleaning requests
- Returning cleaning summaries
- Returning cleaning history
- Returning cleaned files

---

## Dataset Analyzer

The dataset analysis functionality is responsible for determining:

- Number of rows
- Number of columns
- Column names
- Data types
- Missing values
- Duplicate rows
- Empty rows
- Empty columns
- Dataset preview

The preview should contain up to the first 10 rows.

---

## Operation Detector

The operation detector analyzes the user's natural-language prompt.

Example:

```text
Prompt:

Remove duplicate rows and remove extra spaces.
```

Detected operations:

```text
remove_duplicates
remove_extra_spaces
```

The detector uses supported keywords and phrases to map natural-language instructions to internal operation names.

---

## Operation Engine

The operation engine executes the detected operations on the pandas DataFrame.

Each operation is implemented as controlled Python logic.

---

## Cleaning Summary

The backend generates a summary containing:

### Before Cleaning

- Rows
- Columns
- Missing values
- Duplicate rows

### After Cleaning

- Rows
- Columns
- Missing values
- Duplicate rows

### Changes

- Rows removed
- Columns removed
- Missing values changed
- Duplicates removed

### Operations

The operations that were detected and executed.

---

## History Manager

The history functionality stores completed cleaning operations in PostgreSQL.

Stored information includes:

- Filename
- Prompt
- Operations
- Status
- Creation timestamp

---

# 6. Supported Cleaning Operations

The current operation engine supports:

1. `remove_duplicates`
2. `fill_missing_mean`
3. `fill_missing_median`
4. `fill_missing_mode`
5. `remove_empty_rows`
6. `remove_empty_columns`
7. `standardize_columns`
8. `remove_negative_values`
9. `remove_extra_spaces`
10. `remove_missing`
11. `convert_numeric`
12. `remove_duplicate_columns`
13. `replace_negative_with_mean`
14. `remove_invalid_rows`

These operations are controlled backend operations.

Unsupported operations must not be executed.

---

# 7. File Processing

## Supported Input Files

The system supports:

```text
.xlsx
.xls
.csv
```

---

## File Processing Flow

```text
Upload File
    ↓
Validate Extension
    ↓
Read Dataset
    ↓
Analyze Dataset
    ↓
Display Dataset Information
    ↓
Display Dataset Preview
```

For cleaning:

```text
Cleaning Prompt
    ↓
Detect Operations
    ↓
If No Operation:
    Return No-Operation Response
    ↓
If Supported Operations:
    Apply Operations
    ↓
Generate Cleaning Summary
    ↓
Save Cleaning History
    ↓
Create Output File
    ↓
Return Cleaned File
```

---

# 8. API Requirements

The current backend provides the following main endpoints.

## POST `/upload`

Used to upload and analyze a dataset.

The endpoint accepts:

```text
multipart/form-data
```

with a file.

It returns dataset information such as:

- Filename
- Number of rows
- Number of columns
- Column names
- Data types
- Missing values
- Duplicate rows
- Empty rows
- Empty columns
- Dataset preview

---

## POST `/ai-clean`

Used to clean a dataset according to a natural-language prompt.

The endpoint accepts:

```text
file
prompt
```

The endpoint:

1. Reads the uploaded file.
2. Detects supported operations.
3. Handles unsupported requests.
4. Applies detected operations.
5. Generates the cleaning summary.
6. Saves cleaning history.
7. Creates the cleaned output file.
8. Returns the cleaned file.

---

## GET `/summary`

Returns the latest cleaning summary.

The summary contains:

```text
before
after
changes
operations
```

---

## GET `/history`

Returns previously stored cleaning history from PostgreSQL.

The response contains information such as:

```text
id
filename
prompt
operations
status
created_at
```

---

# 9. Frontend Requirements

The frontend must provide the following functionality.

## File Upload

The user must be able to:

- Select a file
- Drag and drop a file
- View the selected filename
- View file size
- Remove the selected file

---

## Dataset Information

After upload, the frontend should display:

- Rows
- Columns
- Missing values
- Duplicate rows
- Empty rows
- Empty columns

---

## Dataset Preview

The frontend should display up to 10 rows of the uploaded dataset.

The preview should update based on the selected dataset.

---

## Cleaning Prompt

The user should be able to enter natural-language cleaning instructions.

Example:

```text
Remove duplicate rows, remove extra spaces, and fill missing values with mean.
```

---

## Cleaning Button

The cleaning button should:

- Remain disabled when required input is missing.
- Show a processing state while cleaning.
- Send the selected file and prompt to `/ai-clean`.

---

## Cleaning Result

After successful cleaning, the frontend should display:

```text
Your file has been cleaned successfully.
```

and provide:

```text
Download Cleaned File
```

The wording should work for both Excel and CSV files.

---

## Cleaning Summary

The frontend should display:

- Before Cleaning
- After Cleaning
- Changes Made
- Operations Applied

---

## Cleaning History

The frontend should display:

- Filename
- Prompt
- Operations
- Status
- Date

A refresh button should allow the user to reload the latest history.

---

# 10. Error Handling

The backend must handle errors such as:

- Unsupported file type
- Invalid file
- Corrupted dataset
- Unable to read file
- Empty or invalid dataset
- No supported cleaning operation
- Cleaning operation failure
- Database failure
- Output file creation failure

The frontend should convert backend failures into understandable user-facing messages.

Examples:

```text
Unable to analyze dataset.
```

```text
No supported cleaning operation was detected.
```

```text
Unable to process the dataset.
```

---

# 11. Data Validation

The system must validate uploaded datasets before processing.

Validation should include:

- File extension
- Successful file reading
- Valid tabular structure
- DataFrame creation
- Required dataset information

The backend should also handle values such as:

- Missing values
- `NaN`
- Empty cells

Special care must be taken when returning dataset information and preview data through JSON because pandas may contain values that are not directly JSON serializable.

---

# 12. Database Requirements

PostgreSQL is used for persistent cleaning history.

The application uses SQLAlchemy for database interaction.

The current cleaning history model contains:

```text
id
filename
prompt
operations
status
created_at
```

Example history record:

```text
Filename:
sales.csv

Prompt:
Remove duplicate rows

Operations:
remove_duplicates

Status:
completed
```

The database should preserve cleaning history even after the frontend is refreshed.

---

# 13. Current Project Structure

The project follows a structure similar to:

```text
AutoExcel/
│
├── backend/
│   │
│   ├── app/
│   │   ├── routes/
│   │   │   ├── upload.py
│   │   │   ├── clean.py
│   │   │   └── ai_clean.py
│   │   │
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   └── venv/
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── data/
│
├── docs/
│   ├── PRD.md
│   ├── TRD.md
│   ├── UI_UX_SPEC.md
│   ├── BACKEND_SCHEMA.md
│   └── AI_SCHEMA.md
│
├── tests/
│
├── .gitignore
└── README.md
```

The exact project structure may evolve as development continues.

---

# 14. API Communication

The frontend communicates with the backend using the Fetch API.

The backend base URL during local development is:

```text
http://127.0.0.1:8000
```

Examples:

```text
POST http://127.0.0.1:8000/upload
```

```text
POST http://127.0.0.1:8000/ai-clean
```

```text
GET http://127.0.0.1:8000/summary
```

```text
GET http://127.0.0.1:8000/history
```

CORS configuration allows the frontend development server to communicate with the backend.

---

# 15. Output File Requirements

The backend must create a separate cleaned output file.

For CSV:

```text
cleaned_<original_filename>.csv
```

For Excel:

```text
cleaned_<original_filename>.xlsx
```

The original uploaded file must remain unchanged.

The cleaned file must contain the results of the requested supported operations.

---

# 16. Security Requirements

The system must:

- Restrict supported file extensions.
- Never execute arbitrary Python code from user prompts.
- Use controlled cleaning functions.
- Keep database credentials outside source code where possible.
- Keep API keys and secrets outside source code.
- Avoid exposing unnecessary backend stack traces to end users.
- Keep the original uploaded file unchanged.
- Validate input before processing.

---

# 17. Testing Requirements

Testing should cover the important application functionality.

Testing areas include:

## File Upload Testing

Test:

- `.xlsx`
- `.xls`
- `.csv`
- Unsupported file types
- Invalid files

## Dataset Analysis Testing

Test:

- Row count
- Column count
- Missing values
- Duplicate rows
- Empty rows
- Empty columns
- Dataset preview

## Operation Testing

Each supported operation should be tested independently.

Examples:

```text
remove_duplicates
fill_missing_mean
remove_extra_spaces
standardize_columns
```

## API Testing

Test:

```text
POST /upload
POST /ai-clean
GET /summary
GET /history
```

## Integration Testing

Test the complete workflow:

```text
Upload
→ Analyze
→ Enter Prompt
→ Detect Operation
→ Clean
→ Generate Summary
→ Save History
→ Download
```

---

# 18. Current Technical Limitations

The current version does not require:

- Next.js
- TypeScript
- Tailwind CSS
- Redis
- Celery
- Microservices
- Kubernetes
- Cloud infrastructure
- Distributed processing
- Complex AI agent frameworks

The project is intentionally kept at a moderate complexity level suitable for a student AI/ML project.

These technologies may be considered in future versions if the application's requirements increase.

---

# 19. Development Approach

Development follows an incremental approach.

The current project development flow is:

```text
Project Foundation
        ↓
Backend Setup
        ↓
Database Setup
        ↓
File Upload
        ↓
Dataset Analysis
        ↓
Cleaning Operations
        ↓
Natural-Language Operation Detection
        ↓
Cleaning Execution
        ↓
Cleaning Summary
        ↓
Cleaning History
        ↓
CSV Support
        ↓
Common Excel/CSV UI
        ↓
Testing
        ↓
Documentation
        ↓
Final Project Testing
        ↓
GitHub Publication
```

Each major feature should be tested before moving to the next feature.

---

# 20. Development Principle

AutoExcel should follow this technical principle:

> **"Natural language identifies the task. Controlled Python operations perform the cleaning. Validation and summaries explain the result."**

The architecture should remain simple, reliable, maintainable, and expandable.