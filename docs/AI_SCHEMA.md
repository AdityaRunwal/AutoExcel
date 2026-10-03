# AutoExcel — AI Schema & AI Contract

## 1. Purpose

This document defines how the AI understands user requests and converts them into structured operations.

The AI is responsible for planning.

The Python engine is responsible for execution.

The AI must never directly execute Python code.

---

# 2. AI Flow

User Prompt

↓

Workbook Profile

↓

AI Planner

↓

Structured JSON Plan

↓

Schema Validation

↓

Operation Validation

↓

Execution Engine

↓

Result Validation

---

# 3. AI Responsibilities

The AI should:

- Understand the user's request.
- Identify required operations.
- Select only supported operations.
- Identify relevant sheets.
- Identify relevant columns.
- Generate valid operation parameters.
- Return structured JSON.
- Ask for clarification when required information is missing.

The AI should NOT:

- Generate arbitrary Python.
- Execute code.
- Invent unsupported operations.
- Modify the original file.
- Claim an operation was completed before execution.
- Use sheet or column names that do not exist in the workbook profile.

---

# 4. Supported Operation Names

The AI can only use these 12 operation names:

1. `remove_duplicates`
2. `handle_missing_values`
3. `remove_whitespace`
4. `standardize_text`
5. `change_data_type`
6. `standardize_dates`
7. `filter_rows`
8. `sort_data`
9. `rename_columns`
10. `create_calculated_column`
11. `group_and_summarize`
12. `create_summary_sheet`

Any operation outside this list must be rejected as unsupported in V1.

---

# 5. Structured Plan

The AI must return a structured JSON plan.

Example:

{
  "operations": [
    {
      "operation": "remove_duplicates",
      "sheet": "Customers",
      "parameters": {
        "columns": ["customer_id"]
      }
    }
  ]
}

---

# 6. Operation Structure

Each operation must contain:

- `operation`
- `sheet`
- `parameters`

Example:

{
  "operation": "sort_data",
  "sheet": "Sales",
  "parameters": {
    "column": "sales",
    "order": "descending"
  }
}

---

# 7. Operation Parameter Rules

Each supported operation must use controlled parameters.

## remove_duplicates

Example:

{
  "operation": "remove_duplicates",
  "sheet": "Customers",
  "parameters": {
    "columns": ["customer_id"]
  }
}

The `columns` parameter is optional when the user wants to remove completely duplicated rows.

---

## handle_missing_values

Example:

{
  "operation": "handle_missing_values",
  "sheet": "Customers",
  "parameters": {
    "column": "age",
    "method": "median"
  }
}

Supported methods may include:

- `mean`
- `median`
- `mode`
- `remove_rows`

---

## remove_whitespace

Example:

{
  "operation": "remove_whitespace",
  "sheet": "Customers",
  "parameters": {
    "columns": ["name", "city"]
  }
}

---

## standardize_text

Example:

{
  "operation": "standardize_text",
  "sheet": "Customers",
  "parameters": {
    "column": "city",
    "method": "lowercase"
  }
}

The exact supported text-standardization methods must be validated by the operation engine.

---

## change_data_type

Example:

{
  "operation": "change_data_type",
  "sheet": "Sales",
  "parameters": {
    "column": "quantity",
    "data_type": "integer"
  }
}

---

## standardize_dates

Example:

{
  "operation": "standardize_dates",
  "sheet": "Sales",
  "parameters": {
    "column": "order_date",
    "format": "YYYY-MM-DD"
  }
}

---

## filter_rows

Example:

{
  "operation": "filter_rows",
  "sheet": "Sales",
  "parameters": {
    "column": "sales",
    "condition": ">",
    "value": 1000
  }
}

---

## sort_data

Example:

{
  "operation": "sort_data",
  "sheet": "Sales",
  "parameters": {
    "column": "sales",
    "order": "descending"
  }
}

Supported order values:

- `ascending`
- `descending`

---

## rename_columns

Example:

{
  "operation": "rename_columns",
  "sheet": "Customers",
  "parameters": {
    "mapping": {
      "Customer Name": "customer_name",
      "Phone Number": "phone_number"
    }
  }
}

---

## create_calculated_column

Example:

{
  "operation": "create_calculated_column",
  "sheet": "Sales",
  "parameters": {
    "column": "total_sales",
    "formula": "quantity * price"
  }
}

The formula must be validated before execution.

The AI must not generate arbitrary Python code.

---

## group_and_summarize

Example:

{
  "operation": "group_and_summarize",
  "sheet": "Sales",
  "parameters": {
    "group_by": ["region"],
    "column": "sales",
    "aggregation": "sum"
  }
}

---

## create_summary_sheet

Example:

{
  "operation": "create_summary_sheet",
  "sheet": "Sales",
  "parameters": {
    "group_by": ["region"],
    "column": "sales",
    "aggregation": "sum",
    "output_sheet": "Sales Summary"
  }
}

---

# 8. AI Rules

## Rule 1 — Supported Operations Only

Only the 12 supported operations can be returned.

---

## Rule 2 — Actual Workbook Information

The AI must use the actual sheet names and column names provided by the workbook profile.

The AI must not invent sheet names or columns.

---

## Rule 3 — No Guessing

If the request is ambiguous and the required information cannot be determined safely, the AI should request clarification instead of guessing.

---

## Rule 4 — Unsupported Operations

If the user requests an operation that is not supported in V1, the AI must return a clear message explaining that the operation is currently unavailable.

---

## Rule 5 — Structured Output

The AI must return structured JSON that follows the AutoExcel AI schema.

---

## Rule 6 — No Executable Code

The AI must never return executable Python code.

The AI only creates a plan.

---

## Rule 7 — Parameter Validation

Parameters must be appropriate for the selected operation.

Invalid parameters must be rejected before execution.

---

# 9. Example

User:

"Remove duplicate customers and fill missing ages with the median."

AI output:

{
  "operations": [
    {
      "operation": "remove_duplicates",
      "sheet": "Customers",
      "parameters": {
        "columns": ["customer_id"]
      }
    },
    {
      "operation": "handle_missing_values",
      "sheet": "Customers",
      "parameters": {
        "column": "age",
        "method": "median"
      }
    }
  ]
}

---

# 10. Invalid Example

The AI must NOT return:

{
  "python_code": "df.drop_duplicates()"
}

The AI must only select supported operations and provide structured parameters.

---

# 11. Plan Validation

Before execution, the backend must:

1. Check that the operation name is supported.
2. Check that the sheet exists.
3. Check that required columns exist.
4. Check that parameters are valid.
5. Check that parameter values are supported.
6. Reject unsupported operations.
7. Reject malformed plans.

Only validated plans can reach the execution engine.

---

# 12. AI Failure Handling

If the AI cannot safely understand the request, it should return a structured response indicating that clarification is required.

Example:

{
  "status": "needs_clarification",
  "message": "Which column should be used to identify duplicate customers?"
}

---

# 13. Unsupported Operation Response

If the user requests an unsupported operation:

Example:

{
  "status": "unsupported_operation",
  "message": "This operation is not supported in AutoExcel V1."
}

The system must not execute the requested operation.

---

# 14. Plan Status

The AI plan may have one of the following statuses:

- `ready`
- `needs_clarification`
- `unsupported_operation`
- `invalid_plan`

Only a plan with status `ready` can proceed to execution.

---

# 15. AI and Execution Separation

The responsibilities are strictly separated:

AI Planner

→ Understands the request

→ Creates the structured plan

↓

Validator

→ Checks the plan

↓

Python Operation Engine

→ Executes the approved operations

↓

Result Validator

→ Checks the result

The AI does not directly modify the spreadsheet.

---

# 16. Important Principle

AI = Planner

Python Engine = Executor

Validator = Safety Layer

Result Validator = Quality Check

The core AutoExcel principle is:

"AI understands the request. Controlled tools perform the work. Validation checks the result."