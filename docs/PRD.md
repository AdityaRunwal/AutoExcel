# AutoExcel — Product Requirements Document (PRD)

## 1. Product Overview

### Product Name

AutoExcel

### Product Type

AI-powered spreadsheet data cleaning application.

### Product Goal

AutoExcel allows users to upload an Excel or CSV dataset and describe data-cleaning requirements using natural language.

The system detects supported cleaning operations from the user's prompt, applies those operations to the uploaded dataset, generates a before/after cleaning summary, stores the cleaning history, and provides the cleaned dataset for download.

AutoExcel is designed to make common spreadsheet cleaning tasks easier without requiring users to manually perform each operation in Excel or write Python code.

---

# 2. Problem Statement

Spreadsheet datasets often contain common data-quality problems such as:

- Duplicate rows
- Missing values
- Empty rows
- Empty columns
- Extra spaces
- Inconsistent column names
- Negative values
- Incorrect data types
- Duplicate columns
- Invalid rows

Cleaning these problems manually can be repetitive and time-consuming.

Users may know what they want to change but may not know the exact Excel or Python operation required.

AutoExcel solves this problem by allowing users to describe cleaning requirements using simple natural-language instructions.

Example:

> "Remove duplicate rows, remove extra spaces, and fill missing values with mean."

The system identifies the supported operations and applies them automatically.

---

# 3. Target Users

The initial target users are:

- Students
- Data analysts
- Researchers
- Business users
- Beginners working with spreadsheet datasets
- Users who regularly clean Excel or CSV files

The first version focuses primarily on dataset cleaning and basic data-quality improvement.

---

# 4. Product Vision

The long-term vision of AutoExcel is to become an intelligent spreadsheet automation assistant.

The current version focuses on controlled, reliable, and understandable dataset-cleaning operations.

The system should remain:

- Simple to use
- Reliable
- Explainable
- Maintainable
- Expandable

AutoExcel should execute only supported operations rather than executing arbitrary AI-generated code.

---

# 5. Current Version Workflow

The current AutoExcel workflow is:

```text
Upload Dataset
        ↓
Analyze Dataset
        ↓
Show Dataset Information & Preview
        ↓
Enter Natural-Language Cleaning Prompt
        ↓
Detect Supported Operations
        ↓
Execute Cleaning Operations
        ↓
Generate Before/After Cleaning Summary
        ↓
Save Cleaning History
        ↓
Download Cleaned Dataset
```

---

# 6. Supported File Types

AutoExcel currently supports:

- `.xlsx`
- `.xls`
- `.csv`

The output file keeps the appropriate format based on the uploaded dataset.

Future versions may support additional spreadsheet formats.

---

# 7. Supported Cleaning Operations

AutoExcel currently supports the following controlled cleaning operations:

1. Remove Duplicate Rows
2. Fill Missing Values with Mean
3. Fill Missing Values with Median
4. Fill Missing Values with Mode
5. Remove Empty Rows
6. Remove Empty Columns
7. Standardize Column Names
8. Remove Negative Values
9. Remove Extra Spaces
10. Remove Rows with Missing Values
11. Convert Columns to Numeric
12. Remove Duplicate Columns
13. Replace Negative Values with Mean
14. Remove Invalid Rows

The operation detector uses supported natural-language phrases to identify the requested operation.

Operations that are not supported should not be executed.

---

# 8. Example User Request

A user uploads:

```text
sales.csv
```

and enters:

```text
Remove duplicate rows and remove extra spaces.
```

AutoExcel should:

1. Read the uploaded dataset.
2. Analyze the dataset.
3. Detect the requested cleaning operations.
4. Execute the supported operations.
5. Generate a before/after cleaning summary.
6. Save the cleaning operation in cleaning history.
7. Provide the cleaned CSV file for download.

Another example:

```text
Fill missing values with mean and remove duplicate rows.
```

The system should detect:

```text
fill_missing_mean
remove_duplicates
```

and apply both operations.

---

# 9. Functional Requirements

## FR-01 File Upload

The system must allow users to upload supported dataset files.

Supported formats:

- `.xlsx`
- `.xls`
- `.csv`

The frontend must validate the selected file type before processing.

---

## FR-02 Dataset Analysis

The system must analyze the uploaded dataset before cleaning.

The analysis should include:

- Number of rows
- Number of columns
- Column names
- Data types
- Total missing values
- Duplicate rows
- Empty rows
- Empty columns
- Dataset preview

The dataset preview should display up to the first 10 rows.

---

## FR-03 Natural-Language Cleaning Input

The user must be able to enter cleaning instructions using natural language.

Example:

```text
Remove duplicate rows and fill missing values with mean.
```

---

## FR-04 Operation Detection

The backend must analyze the user's prompt and detect supported cleaning operations.

For example:

```text
User Prompt:
Remove duplicate rows and extra spaces.

Detected Operations:
- remove_duplicates
- remove_extra_spaces
```

Only supported operations should be detected and executed.

---

## FR-05 Operation Execution

The backend must execute the detected operations using controlled data-processing functions.

The system must not execute arbitrary Python code generated from user input.

---

## FR-06 Unsupported Request Handling

If no supported cleaning operation is detected, the system must not modify the dataset.

Instead, it should inform the user that no supported operation was detected and provide example supported operations.

Example:

```text
No supported cleaning operation was detected.

Try one of these:
- Remove duplicate rows
- Fill missing values with mean
- Remove empty rows
- Remove extra spaces
- Standardize column names
```

---

## FR-07 Cleaning Summary

After successful cleaning, the system must generate a before/after summary.

The summary should contain:

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

### Changes Made

- Rows removed
- Columns removed
- Missing values changed
- Duplicates removed

### Operations Applied

The summary must also display the operations detected and executed.

---

## FR-08 Cleaning History

The system must store cleaning history in PostgreSQL.

The history should contain information such as:

- Filename
- User prompt
- Operations performed
- Cleaning status
- Creation date/time

Users should be able to view the cleaning history from the frontend.

---

## FR-09 Download Cleaned Dataset

After successful cleaning, the system must provide the processed dataset for download.

The downloaded file should use an appropriate filename such as:

```text
cleaned_filename.xlsx
```

or

```text
cleaned_filename.csv
```

The download interface should use common wording such as:

```text
Download Cleaned File
```

so that the interface works consistently for both Excel and CSV files.

---

## FR-10 Error Handling

The system must provide understandable error messages for problems such as:

- Unsupported file type
- Invalid dataset
- Unable to read the file
- Backend connection failure
- Unsupported cleaning request
- Dataset processing failure

Backend errors should not expose unnecessary internal implementation details to the user.

---

# 10. Non-Functional Requirements

AutoExcel should be:

- Simple to use
- Reliable
- Maintainable
- Explainable
- Responsive
- Testable
- Secure

The application should use controlled backend operations instead of executing arbitrary code from user prompts.

The frontend and backend should communicate through defined FastAPI endpoints.

---

# 11. Current UI Structure

AutoExcel currently uses a single-page web interface.

The main UI contains:

### 1. Header

Displays:

```text
AutoExcel
AI-Powered Data Cleaning
```

### 2. Dataset Upload

Users can:

- Select a dataset
- Drag and drop a dataset
- Remove the selected dataset

Supported formats are:

```text
.xlsx
.xls
.csv
```

### 3. Dataset Information

After uploading a dataset, the interface displays:

- Rows
- Columns
- Missing values
- Duplicate rows
- Empty rows
- Empty columns

### 4. Dataset Preview

The interface displays the first 10 rows of the uploaded dataset.

### 5. Cleaning Instructions

Users enter their cleaning request in a natural-language text area.

### 6. Cleaning Result

After successful processing, the interface provides:

- Success message
- Cleaned filename
- Download Cleaned File button

### 7. Cleaning Summary

The interface displays:

- Before cleaning
- After cleaning
- Changes made
- Operations applied

### 8. Cleaning History

The interface displays previous cleaning operations including:

- Filename
- Prompt
- Operations
- Status
- Date

---

# 12. Backend Requirements

The backend is implemented using FastAPI.

The backend is responsible for:

- Receiving uploaded datasets
- Reading Excel and CSV files
- Analyzing datasets
- Detecting cleaning operations
- Applying cleaning operations
- Generating cleaning summaries
- Saving cleaning history
- Returning cleaned files

The main backend technologies include:

- Python
- FastAPI
- pandas
- SQLAlchemy
- PostgreSQL
- openpyxl
- Uvicorn

---

# 13. Current API Endpoints

The current AutoExcel backend provides the following main endpoints:

### POST `/upload`

Used to upload and analyze a dataset.

It provides information such as:

- Rows
- Columns
- Column names
- Data types
- Missing values
- Duplicate rows
- Empty rows
- Empty columns
- Dataset preview

---

### POST `/ai-clean`

Used to process the uploaded dataset according to the natural-language cleaning prompt.

The endpoint:

1. Reads the dataset.
2. Detects supported operations.
3. Applies the operations.
4. Generates the cleaning summary.
5. Saves cleaning history.
6. Returns the cleaned dataset.

---

### GET `/summary`

Returns the latest cleaning summary.

---

### GET `/history`

Returns previously stored cleaning history.

---

# 14. Database

AutoExcel uses PostgreSQL for storing cleaning history.

The current application contains a cleaning history model with information including:

- ID
- Filename
- Prompt
- Operations
- Status
- Created timestamp

The database is used to preserve the user's cleaning activity and display it in the frontend.

Additional database structures may be added in future versions if required.

---

# 15. Success Criteria

The current version of AutoExcel will be considered successful when:

- A user can upload an `.xlsx` file.
- A user can upload an `.xls` file.
- A user can upload a `.csv` file.
- The dataset can be analyzed successfully.
- Dataset information can be displayed.
- A dataset preview can be displayed.
- A user can enter a natural-language cleaning instruction.
- Supported cleaning operations can be detected.
- Supported operations can be executed.
- Unsupported operations are rejected safely.
- A before/after cleaning summary can be generated.
- Cleaning history can be stored in PostgreSQL.
- Cleaning history can be displayed.
- A cleaned dataset can be downloaded.
- Excel and CSV files can be processed using the same common workflow.

---

# 16. Current Limitations

The current version does not include:

- User authentication
- Multiple user accounts
- Cloud storage
- Collaborative editing
- Advanced dashboards
- Large-scale distributed processing
- Arbitrary Python code execution
- Autonomous AI agents
- Complex spreadsheet formula generation
- Advanced chart generation
- Multi-file batch processing

These features may be considered for future versions.

---

# 17. Future Expansion

Possible future improvements include:

- More cleaning operations
- Advanced natural-language understanding
- More file formats
- Multiple-file processing
- Data transformation operations
- Advanced spreadsheet formulas
- Charts and visualizations
- Conditional formatting
- User authentication
- Cloud storage
- Background processing
- Advanced data-quality reports
- More intelligent operation detection

---

# 18. Product Principle

AutoExcel follows the principle:

> **"Natural language describes the task. Controlled operations perform the work. Validation and summaries explain the result."**

The system should prioritize predictable and controlled data processing rather than unrestricted AI-generated code execution.