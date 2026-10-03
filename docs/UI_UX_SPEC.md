# AutoExcel — UI/UX Specification

## 1. Design Goal

AutoExcel should look like a modern professional AI/data product.

The design should be:

- Clean
- Minimal
- Professional
- Easy to understand
- Fast
- Responsive

Avoid unnecessary animations and visual complexity.

The interface should use common terminology for both Excel and CSV files.

For example:

- "Dataset" instead of "Excel file"
- "Cleaned File" instead of "Cleaned Excel"
- "Download Cleaned File" instead of "Download Cleaned Excel"

---

# 2. Main User Flow

Home

↓

Upload Dataset

↓

Analyze Dataset

↓

Enter Prompt

↓

Generate Plan

↓

Review Plan

↓

Apply Plan

↓

Processing

↓

Results

↓

Download Cleaned File

---

# 3. Screen 1 — Home / Upload

Purpose:

Allow the user to upload a spreadsheet dataset and start a cleaning task.

Components:

- AutoExcel logo
- Short product description
- Upload area
- Browse button
- Supported file types

Example:

AutoExcel

AI-powered spreadsheet data cleaning

"Upload your dataset and tell AutoExcel what you want."

[ Drop your dataset here ]

[ Browse ]

Supported:

.xlsx, .xls, .csv

---

# 4. Screen 2 — Dataset Analysis

Purpose:

Show the user that AutoExcel has successfully analyzed the uploaded dataset.

Display:

- File name
- Number of rows
- Number of columns
- Missing values
- Duplicate rows
- Empty rows
- Empty columns
- Data preview

Example:

sales.csv

Rows: 10,542

Columns: 12

Duplicates: 42

Missing Values: 25

Empty Rows: 0

Empty Columns: 0

### Dataset Preview

Display the first 10 rows of the uploaded dataset.

[ Continue ]

---

# 5. Screen 3 — Prompt / Workspace

Purpose:

Allow the user to tell AutoExcel what to do.

Components:

- Dataset information
- Data preview
- Large prompt input
- Cleaning instructions
- Clean Dataset button

Example:

"What would you like AutoExcel to do?"

[ Remove duplicate rows and fill missing values with mean... ]

[ Clean Dataset ]

The interface should use the same terminology for Excel and CSV files.

---

# 6. Screen 4 — AI Plan

Purpose:

Show what AutoExcel intends to do before execution.

Example:

AI Plan

1. Remove duplicates

   Sheet: Customers

   Column: customer_id

2. Handle missing values

   Column: age

   Method: median

3. Create summary

   Group by: region

   Calculation: total sales

[ Apply Plan ]

[ Cancel ]

The AI plan must only contain supported operations.

---

# 7. Screen 5 — Processing

Display simple progress:

Analyzing

✓

Planning

✓

Processing

●

Validating

○

The interface should clearly communicate that processing is in progress.

Example loading messages:

"Analyzing dataset..."

"Creating cleaning plan..."

"Processing dataset..."

"Validating result..."

---

# 8. Screen 6 — Results

Display:

Cleaning Complete

Rows:

10,542 → 10,500

Duplicates:

42 → 0

Missing Values:

25 → 0

Operations completed:

- Remove duplicates
- Handle missing values
- Create summary

Validation:

✓ Passed

Buttons:

[ Download Cleaned File ]

[ View Report ]

The download button must use a common name that works for both Excel and CSV files.

---

# 9. Dataset Information

After a file is uploaded successfully, display a dataset information section.

The section should show:

- Rows
- Columns
- Missing Values
- Duplicate Rows
- Empty Rows
- Empty Columns

A dataset preview should display up to 10 rows.

The preview should work for:

- .xlsx
- .xls
- .csv

Missing values in the preview must be safely displayed without causing frontend or backend serialization errors.

---

# 10. Download Area

The download section should use file-type-independent wording.

Use:

"Your file has been cleaned successfully."

Example:

cleaned_sales.csv

[ Download Cleaned File ]

For Excel:

cleaned_sales.xlsx

[ Download Cleaned File ]

The UI must not permanently display:

- Download Cleaned Excel
- Clean Excel

when the uploaded file is a CSV.

---

# 11. Cleaning History

The application should display a cleaning history section.

The history should include:

- Filename
- Prompt
- Operations
- Status
- Date

Example:

| Filename | Prompt | Operations | Status | Date |
|----------|--------|------------|--------|------|
| sales.csv | Remove duplicates | remove_duplicates | completed | 2026-09-25 |
| customers.xlsx | Fill missing values | handle_missing_values | completed | 2026-09-25 |

The history should support both Excel and CSV files.

---

# 12. Loading States

Every operation that takes time should show a loading state.

Examples:

"Analyzing dataset..."

"Creating cleaning plan..."

"Processing dataset..."

"Validating result..."

The Clean Dataset button should indicate when processing is active.

---

# 13. Error States

Errors should be simple and understandable.

Example:

"AutoExcel could not analyze this dataset."

Reason:

"The uploaded dataset contains invalid or unsupported data."

[ Upload Another Dataset ]

For unsupported files:

"Please select a valid dataset file (.xlsx, .xls, .csv)."

For unsupported cleaning instructions:

"No supported cleaning operation was detected."

The interface should provide examples of supported operations.

---

# 14. Responsive Design

The application must work on:

- Desktop
- Tablet
- Mobile

Desktop is the primary target for V1 because spreadsheet work is usually performed on larger screens.

---

# 15. UX Principles

1. Keep the user informed.

2. Never hide what the AI plans to do.

3. Make destructive actions reviewable.

4. Use clear language.

5. Avoid unnecessary screens.

6. Show actual results.

7. Keep the interface focused on the spreadsheet task.

8. Use terminology that works for both Excel and CSV files.

9. Clearly distinguish analysis, processing, and results.

10. Never claim that cleaning succeeded if the backend operation failed.

---

# 16. File-Type Independence

AutoExcel should treat Excel and CSV as datasets rather than designing the interface around only Excel files.

Supported input files:

- .xlsx
- .xls
- .csv

The UI should dynamically display the actual uploaded filename.

Examples:

sales.xlsx

sales.csv

The same interface should work for both formats.

---

# 17. V1 Interface Structure

The current V1 interface should contain:

1. Header
2. Dataset Upload
3. Cleaning Instructions
4. Clean Dataset Button
5. Status Messages
6. Download Cleaned File
7. Dataset Information
8. Dataset Preview
9. Cleaning Summary
10. Cleaning History

The interface should remain simple and should not introduce unnecessary screens if the functionality can be handled within the existing page.

---

# 18. Design Principle

AutoExcel should follow this principle:

"Simple interface. Clear instructions. Visible processing. Understandable results."

The user should always know:

- What file was uploaded.
- What AutoExcel detected.
- What operation is being requested.
- What was changed.
- Whether processing succeeded.
- Where to download the cleaned file.