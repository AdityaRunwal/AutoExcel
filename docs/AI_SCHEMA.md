# AutoExcel — AI Schema & AI Contract

## 1. Purpose

This document defines how AutoExcel understands user prompts and converts them into structured cleaning operations.

**Note on implementation:** AutoExcel V1 uses a **rule-based detector system**, not a large language model. The "AI Planner" referenced throughout this document is implemented as a set of Python keyword/phrase detectors in `backend/app/routes/ai_clean.py`. This keeps behavior predictable and fully controlled, with no external AI API calls.

The Planner is responsible for detecting intent and building a plan.

The Python engine is responsible for execution.

The Planner never directly executes pandas/Python operations itself — it only produces a plan dictionary.

## 2. Actual Flow (as implemented)

User Prompt + Uploaded File
        -> Read file into a single pandas DataFrame
        -> build_cleaning_plan(prompt) detects operations via keyword/phrase matching
        -> Structured Plan (dict with "steps" list)
        -> validate_plan(df, plan) checks columns exist; invalid steps moved to skipped_steps
        -> POST /preview-plan returns readable plan + skipped steps, no execution
        -> User clicks "Apply Plan" (frontend)
        -> POST /ai-clean re-runs build_cleaning_plan + validate_plan, then executes
        -> apply_operations() / apply_calculated_column() / apply_summary_sheet()
        -> validate_result() compares before/after stats, flags warnings
        -> Cleaning Summary + Cleaned File Download

There is no multi-sheet workbook concept in V1 — each uploaded file (.xlsx, .xls, .csv) is read into one DataFrame and operations apply to that single dataset.

## 3. Planner Responsibilities

The Planner (detector functions) should:

- Parse the prompt using keyword and phrase matching.
- Identify which of the 12 supported operations apply.
- Extract operation parameters (column names, methods, values) directly from the prompt text.
- Return a structured plan dictionary.
- Flag when no operation was detected (clarification_needed: true).

The Planner does NOT:

- Call any external AI/LLM API.
- Generate or execute arbitrary Python code.
- Invent operations outside the supported list.
- Modify the original uploaded file (a new cleaned file is always written separately).
- Claim an operation succeeded before /ai-clean actually executes it.

## 4. Supported Operation Names (actual strings used in code)

1. remove_duplicates
2. fill_missing_mean, fill_missing_median, fill_missing_mode (missing-value handling is split into three distinct operations, not one with a method parameter)
3. remove_extra_spaces
4. standardize_text_lower, standardize_text_upper, standardize_text_title (standardize-text is similarly split by case)
5. convert_numeric / data-type change operations
6. standardize_dates
7. filter_rows
8. sort_data
9. rename_columns
10. create_calculated_column
11. group_summarize
12. create_summary_sheet

Additional operations have also been observed in testing (e.g. remove_missing, remove_duplicate_columns, remove_negative_values, replace_negative_with_mean, remove_invalid_rows, standardize_columns). These extend beyond the original V1 list of 12 and should be reconciled with this document in a future pass — see Section 10.

Any operation not detected by the current set of detector functions is treated as unsupported for that prompt.

## 5. Actual Plan Structure

The Planner returns a dictionary, not a list of operation objects with a sheet field (there is no sheet concept). Example, for the prompt "remove duplicates and sort by Salary descending":

{
  "steps": [
    { "operation": "remove_duplicates", "params": {} },
    { "operation": "sort_data", "params": { "column_raw": "Salary", "ascending": false } }
  ],
  "operations": ["remove_duplicates"],
  "filter_condition": null,
  "sort_condition": { "column_raw": "Salary", "ascending": false },
  "rename_conditions": [],
  "calc_column": null,
  "group_condition": null,
  "create_summary": false,
  "clarification_needed": false
}

After validate_plan(df, plan) runs, two more keys are added:

{
  "skipped_steps": [
    { "operation": "sort_data", "reason": "Column 'Salry' not found" }
  ]
}

(plan["steps"] is also filtered down to only the steps that passed validation.)

## 6. Step Structure

Each step in plan["steps"] contains exactly two keys:

- operation — one of the supported operation name strings (Section 4)
- params — a dictionary of operation-specific parameters, detected directly from prompt text (e.g. raw column names as typed by the user, which are matched case-insensitively against actual DataFrame columns during validation)

There is no sheet key — V1 operates on a single DataFrame per request.

## 7. Operation Parameter Notes (as implemented)

### remove_duplicates
params: {} — no parameters; always removes fully duplicated rows.

### fill_missing_mean / fill_missing_median / fill_missing_mode
Each is a distinct operation name. There is no single handle_missing_values operation with a method field — the method is encoded directly in the operation name.

### remove_extra_spaces
params: {} — strips leading/trailing/extra internal whitespace from text columns.

### standardize_text_lower / _upper / _title
Each case variant is a separate operation name rather than a method parameter.

### filter_rows
params: { column_raw, operator, value } — supports equals, contains, greater than / is greater than, less than / is less than phrasing.

### sort_data
params: { column_raw, ascending } — flexible phrasing for ascending/descending.

### rename_columns
params: { renames: [ { old_name_raw, new_name_raw }, ... ] } — supports multiple renames detected from a single prompt.

### create_calculated_column
params includes the new column name and a validated arithmetic expression (supports + - * /, parentheses, and natural phrases like "times"/"plus"). The expression is evaluated by a safe expression evaluator — never via Python's eval() on unsanitized input.

### group_summarize
params: { group_column_raw, agg_column_raw, aggregation } — supports sum, average, count, min, max.

### create_summary_sheet
params: {} — replaces the current dataset with column-level statistics (count, missing, unique, mean, min, max).

## 8. Planner Rules (as implemented)

### Rule 1 — Supported Operations Only
Only operations with a matching detector function can appear in a plan. Everything else is simply not detected — there is no separate "reject unsupported operation" path at the planning stage; an unrecognized request just produces zero steps (see Rule 3).

### Rule 2 — Real Column Names Only
validate_plan() checks every column name referenced in a step against the actual uploaded file's columns (case-insensitive). Steps referencing a non-existent column are moved to skipped_steps with a reason, rather than crashing the whole request.

### Rule 3 — No Operation Detected
If build_cleaning_plan() finds zero operations in the prompt, it returns:
{ "steps": [], "clarification_needed": true, "message": "I couldn't understand any specific cleaning operation in that prompt. Try being more specific, e.g. 'remove duplicates', 'fill missing values with mean', or 'sort by Salary descending'." }

### Rule 4 — All Steps Skipped at Validation
If operations were detected but every one of them failed validation (e.g. all referenced columns don't exist), /preview-plan builds a message from skipped_steps reasons:
{ "has_plan": false, "clarification_needed": true, "message": "None of the requested operations could be applied: Column 'X' not found" }

### Rule 5 — Empty Prompt
A blank or whitespace-only prompt is rejected before detection runs, with clarification_needed: true and a message asking the user to enter instructions.

### Rule 6 — Empty File
A file with zero data rows is rejected with an HTTP 400 error before any plan is built.

### Rule 7 — No Arbitrary Code Execution
create_calculated_column uses a restricted, safe expression evaluator. No operation anywhere in the system runs arbitrary user-supplied Python or pandas code.

## 9. Example (actual request/response)

User prompt: "Remove duplicate customers and fill missing ages with the median."

POST /preview-plan response:
{
  "steps": [
    { "operation": "remove_duplicates", "description": "Remove duplicate rows" },
    { "operation": "fill_missing_median", "description": "Fill missing values using median" }
  ],
  "skipped_steps": [],
  "has_plan": true,
  "clarification_needed": false,
  "message": ""
}

## 10. Known Gaps / Future Reconciliation

This section exists so the schema stays honest about where documentation and code have diverged:

- The original V1 operation list (12 single-named operations) does not match the actual detector set, which splits several operations by variant (missing-value method, text case) and includes additional operations not in the original list (e.g. remove_negative_values, remove_duplicate_columns).
- There is no "sheet" concept — this entire document previously assumed multi-sheet workbook support, which was never built and is out of scope per the project's stated boundaries.
- There is no LLM-based "AI Planner" — all detection is deterministic keyword/phrase matching. If a true AI/LLM planning layer is added in a future phase, this document must be revised again to reflect that change, and the current detector-based system should be described as the V1 baseline it replaces.
- Plan status values (ready/needs_clarification/etc., Section 14 in the previous version of this doc) do not exist in code. The actual signal is the combination of has_plan (bool) and clarification_needed (bool) plus a message string.

## 11. Separation of Responsibilities (still accurate)

Detector Functions (Planner)
   -> Parse prompt, identify operations and parameters
        -> validate_plan() (Validator) checks columns exist, filters invalid steps
        -> apply_operations() / apply_calculated_column() / apply_summary_sheet() (Executor) performs the actual pandas transformations
        -> validate_result() (Result Validator) compares before/after stats, flags warnings if an expected change didn't occur

The Planner never modifies the DataFrame directly — only the Executor functions do, and only after validation and (via the two-endpoint split) explicit user approval through the Plan Review UI.