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

## 2. Actual Interface Structure (Single-Page App)

AutoExcel V1 is implemented as a single HTML page (frontend/index.html) with sections that show and hide dynamically, not a sequence of separate screens. There is no "Continue" button or screen-to-screen navigation.

The page sections, in order, are:

1. Header (logo + subtitle)
2. Cleaner Card - file upload dropzone + cleaning instructions textarea + "Clean Dataset" button
3. Status Message (shown/hidden as needed)
4. Download Area (hidden until a file is cleaned)
5. AI Cleaning Plan section (hidden until a plan is built)
6. Dataset Information section (hidden until a file is uploaded and analyzed)
7. Cleaning Summary section (hidden until a cleaning operation completes)
8. Cleaning History section (always visible, loads on page load)

### Actual User Flow

Upload Dataset (dropzone)
        -> Dataset automatically analyzed (POST /upload) - Dataset Information section appears
        -> Enter Prompt
        -> Click "Clean Dataset" - this calls POST /preview-plan (not /ai-clean directly)
        -> AI Cleaning Plan section appears with numbered steps + any skipped steps
        -> User clicks "Apply Plan" or "Cancel"
        -> If Apply Plan: POST /ai-clean executes the plan
        -> Cleaning Summary section appears + Download Area appears
        -> Cleaning History refreshes automatically

If no plan could be built (nothing detected, everything skipped, empty prompt, or empty file), the Status Message area shows a clarification message instead of the plan section.

## 3. Cleaner Card (Upload + Prompt)

Purpose:

Let the user upload a dataset and describe what they want cleaned, in one combined card.

Components:

- Dropzone (click to browse, or drag and drop)
- Supported file types hint: ".xlsx, .xls, .csv"
- Selected file name + size, with a "Remove" option
- Cleaning instructions textarea
- "Clean Dataset" submit button (disabled until both a file is selected and the prompt is non-empty)

Example:

Clean Your Dataset

Upload a dataset and enter prompt instructions to automatically
clean and structure your data.

[ Drag and drop your dataset here, or click to browse ]
Supports .xlsx, .xls, .csv

Cleaning instructions
[ Remove duplicate rows, remove extra spaces, and fill missing values with mean ]

[ Clean Dataset ]

Uploading a file immediately triggers dataset analysis (POST /upload) - there is no separate "analyze" step the user must trigger.

## 4. Dataset Information Section

Purpose:

Show the user that AutoExcel has successfully analyzed the uploaded dataset, before any cleaning happens.

Display:

- Rows
- Columns
- Missing Values
- Duplicate Rows
- Empty Rows
- Empty Columns
- Dataset Preview (first 10 rows)

This section appears automatically right after upload completes, and stays visible while the user writes their prompt.

Missing values in the preview must be safely displayed without causing frontend or backend serialization errors (values are converted to empty strings rather than null/NaN).

## 5. AI Cleaning Plan Section

Purpose:

Show what AutoExcel intends to do before any changes are made, and let the user approve or cancel.

Example:

AI Cleaning Plan

Review the steps AutoExcel will perform before applying them.

1. Remove duplicate rows
2. Fill missing values using median
3. Sort by Salary (descending)

Skipped Steps
- rename_columns: Column 'Custmer Name' not found

[ Apply Plan ]   [ Cancel ]

There is no "Sheet:" field shown anywhere - AutoExcel V1 operates on a single dataset per upload, not a multi-sheet workbook.

If the plan is empty (nothing detected or everything skipped), this section does not appear. Instead, the Status Message area shows the clarification text returned by the backend, e.g.:

I couldn't understand any specific cleaning operation in that prompt.
Try being more specific, e.g. 'remove duplicates', 'fill missing values
with mean', or 'sort by Salary descending'.

Clicking "Apply Plan" executes the plan (POST /ai-clean). Clicking "Cancel" simply hides this section with no backend call.

## 6. Processing / Loading State

There is no multi-step progress indicator (no "Analyzing / Planning / Processing / Validating" checklist UI). Instead, the single "Clean Dataset" / "Apply Plan" button shows a spinner and disables itself while its respective request is in flight.

Button text during the two stages:

- While building the plan: spinner shown, button disabled
- While applying the plan: spinner shown, button text "Cleaning..."

## 7. Cleaning Summary Section

Purpose:

Show the before/after results once a plan has been applied successfully.

Display:

Cleaning completed successfully

Before Cleaning          After Cleaning           Changes Made
Rows: 10,542             Rows: 10,500             Rows Removed: 42
Columns: 12              Columns: 12              Columns Removed: 0
Missing Values: 25       Missing Values: 0        Missing Values Changed: 25
Duplicate Rows: 42       Duplicate Rows: 0        Duplicates Removed: 42

Operations Applied
remove_duplicates, fill_missing_mean

If the result validation step flags a warning (an expected change didn't happen, or steps were skipped), this should be shown here as well - this is not yet wired into the current frontend markup and should be added as a follow-up UI task (see Section 14).

There is no separate "View Report" button in the current implementation - only "Download Cleaned File."

## 8. Download Area

Purpose:

Let the user download the cleaned file once cleaning succeeds.

The download section should use file-type-independent wording.

Example:

Your file has been cleaned successfully
cleaned_sales.csv
[ Download Cleaned File ]

For Excel:

Your file has been cleaned successfully
cleaned_sales.xlsx
[ Download Cleaned File ]

The UI must not permanently display "Download Cleaned Excel" or "Clean Excel" when the uploaded file is a CSV.

## 9. Cleaning History Section

Purpose:

Show previously completed cleaning operations, stored in PostgreSQL.

Display, in a table:

- Filename
- Prompt
- Operations (formatted into readable names, e.g. "Remove Duplicate Rows" instead of the raw remove_duplicates string)
- Status (shown as a colored status pill)
- Date

This section is always visible (not hidden), loads automatically on page load, and includes a "Refresh History" button for manually reloading it. History also refreshes automatically right after a successful cleaning operation.

Example:

Cleaning History                              [ Refresh History ]

Filename         Prompt                  Operations            Status      Date
sales.csv        Remove duplicates       Remove Duplicate Rows Completed   2026-09-25
customers.xlsx   Fill missing values     Fill Missing Values   Completed   2026-09-25
                                          with Mean

## 10. Error States

Errors are shown in the shared Status Message area (not a separate error screen).

Examples:

For unsupported files:
Please select a valid dataset file (.xlsx, .xls, .csv).

For a prompt that produced no plan:
I couldn't understand any specific cleaning operation in that prompt. ...

For a backend connection failure:
Error: Unable to connect to FastAPI backend at http://127.0.0.1:8000.

For a failed history load (fixed in Phase 7 - was a CORS misconfiguration, not a UI bug):
Unable to load cleaning history.

## 11. Responsive Design

The application must work on:

- Desktop
- Tablet
- Mobile

Desktop is the primary target for V1 because spreadsheet work is usually performed on larger screens.

## 12. UX Principles

1. Keep the user informed.
2. Never hide what AutoExcel plans to do - always show the plan before applying it.
3. Make destructive actions reviewable (Apply/Cancel on the plan).
4. Use clear language.
5. Avoid unnecessary screens - keep everything on one page with sections that appear as needed.
6. Show actual results.
7. Keep the interface focused on the spreadsheet task.
8. Use terminology that works for both Excel and CSV files.
9. Clearly distinguish dataset analysis, plan review, and results.
10. Never claim that cleaning succeeded if the backend operation failed or was skipped.

## 13. File-Type Independence

AutoExcel treats Excel and CSV as datasets rather than designing the interface around only Excel files.

Supported input files:

- .xlsx
- .xls
- .csv

The UI dynamically displays the actual uploaded filename. The same interface works for both formats.

## 14. Known Gaps / Follow-Up UI Work

- The result-validation warning (from validate_result(), Phase 7) is returned by the backend in the cleaning summary but is not yet displayed anywhere in the current frontend markup. A future pass should add a small warning banner to the Cleaning Summary section when validation.status === "warning".
- There is no dedicated "View Report" feature - if this is wanted in a future version, it would need new backend and frontend work, not just a UI label change.

## 15. Design Principle

AutoExcel should follow this principle:

"Simple interface. Clear instructions. Visible processing. Understandable results."

The user should always know:

- What file was uploaded.
- What AutoExcel detected.
- What operation is being requested.
- What was changed.
- Whether processing succeeded.
- Where to download the cleaned file.