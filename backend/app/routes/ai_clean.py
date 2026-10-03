from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import os
import re

from app.database import SessionLocal
from app.models import CleaningHistory

router = APIRouter()

latest_summary = {}

def detect_operations(prompt: str):
    prompt = prompt.lower()

    operations = []

    # Remove duplicate rows
    if any(phrase in prompt for phrase in [
        "duplicate rows",
        "repeated rows",
        "repeated records",
        "repeated data",
        "duplicate data",
        "duplicate records",
        "repeated entries",
        "duplicate entries",
        "duplicate removal",
        "remove duplicate",
        "remove duplicates",
        "delete duplicate",
        "delete duplicates",
        "remove repeated",
        "remove repeated rows",
        "delete repeated rows",
        "remove repeated records",
        "delete repeated records",
        "get rid of duplicates",
        "get rid of duplicate rows"
    ]):
        operations.append("remove_duplicates")

    # Fill missing values with mean / average
    if any(phrase in prompt for phrase in [
        "missing",
        "empty",
        "blank",
        "missing values",
        "empty values",
        "blank values",
        "missing cells",
        "empty cells",
        "blank cells"
    ]):

        if any(word in prompt for word in [
            "mean",
            "average",
            "avg",
            "mean value",
            "average value",
            "using mean",
            "using average",
            "with the mean",
            "with the average",
            "using the mean",
            "using the average",
            "fill with mean",
            "fill with average",
            "replace with mean",
            "replace with average"
        ]):
                operations.append("fill_missing_mean")

    # Fill missing values with median
    if any(phrase in prompt for phrase in [
        "missing",
        "empty",
        "blank",
        "missing values",
        "empty values",
        "blank values",
        "missing cells",
        "empty cells",
        "blank cells"
    ]):
        if any(word in prompt for word in [
            "median",
            "median value",
            "using median",
            "with the median",
            "using the median",
            "fill with median",
            "replace with median"
        ]):
            operations.append("fill_missing_median")

    # Fill missing values with mode
    if any(phrase in prompt for phrase in [
        "missing",
        "empty",
        "blank",
        "missing values",
        "empty values",
        "blank values",
        "missing cells",
        "empty cells",
        "blank cells"
    ]):
        if any(word in prompt for word in [
            "mode",
            "most common",
            "most frequent",
            "using mode",
            "using the mode",
            "with the mode",
            "fill with mode",
            "replace with mode"
        ]):
            operations.append("fill_missing_mode")

    # Remove completely empty rows
    if any(phrase in prompt for phrase in [
        "empty rows",
        "blank rows",
        "remove empty rows",
        "delete empty rows",
        "remove blank rows",
        "delete blank rows"
    ]):
        operations.append("remove_empty_rows")

    # Remove completely empty columns
    if any(phrase in prompt for phrase in [
        "empty columns",
        "blank columns",
        "remove empty columns",
        "delete empty columns",
        "remove blank columns",
        "delete blank columns"
    ]):
        operations.append("remove_empty_columns")

    # Standardize column names
    if any(phrase in prompt for phrase in [
        "standardize columns",
        "standardize column names",
        "clean column names",
        "normalize column names",
        "format column names"
    ]):
        operations.append("standardize_columns")

    # Remove negative values
    if (
        any(phrase in prompt for phrase in [
            "remove negative",
            "remove negative values",
            "delete negative values",
            "negative values to zero",
            "replace negative values with 0"
        ])
        and not any(phrase in prompt for phrase in [
            "replace negative values with mean",
            "replace negative values by mean",
            "negative values with mean"
        ])
    ):
        operations.append("remove_negative_values")

    # Remove extra spaces
    if any(phrase in prompt for phrase in [
        "extra spaces",
        "unnecessary spaces",
        "unwanted spaces",
        "leading spaces",
        "trailing spaces",
        "multiple spaces",
        "double spaces",
        "remove spaces",
        "remove extra spaces",
        "remove unwanted spaces",
        "remove unnecessary spaces",
        "clean spaces",
        "clean extra spaces",
        "clean unnecessary spaces",
        "trim spaces",
        "trim whitespace",
        "strip spaces",
        "strip whitespace",
        "remove whitespace",
        "clean whitespace"
    ]):
        operations.append("remove_extra_spaces")

    # Remove rows containing missing values
    if any(phrase in prompt for phrase in [
        "remove missing",
        "remove rows with missing",
        "delete rows with missing",
        "drop rows with missing",
        "remove incomplete rows",
        "delete incomplete rows"
    ]):
        operations.append("remove_missing")

    # Convert columns to numeric
    if any(phrase in prompt for phrase in [
        "convert numeric",
        "convert to numeric",
        "convert columns to numeric",
        "convert to numbers",
        "convert columns to numbers",
        "make columns numeric",
        "make the columns numeric",
        "change columns to numeric",
        "change the columns to numeric"
    ]):
        operations.append("convert_numeric")

    # Convert columns to text
    if any(phrase in prompt for phrase in [
        "convert to text",
        "convert columns to text",
        "convert to string",
        "convert columns to string",
        "make columns text",
        "change columns to text",
        "change the columns to text"
    ]):
        operations.append("convert_to_text")

    # Convert columns to date
    if any(phrase in prompt for phrase in [
        "convert to date",
        "convert columns to date",
        "convert to dates",
        "convert columns to dates",
        "make columns date",
        "change columns to date",
        "change the columns to date",
        "parse dates",
        "convert date columns"
    ]):
        operations.append("convert_to_date")

    # Standardize dates to YYYY-MM-DD
    if any(phrase in prompt for phrase in [
        "standardize date",
        "standardize dates",
        "standardize the date",
        "standardize the dates",
        "format dates",
        "format date columns",
        "normalize dates",
        "consistent date format"
    ]):
        operations.append("standardize_dates")

    # Remove duplicate columns
    if any(phrase in prompt for phrase in [
        "duplicate columns",
        "duplicated columns",
        "repeated columns",
        "remove duplicate columns",
        "delete duplicate columns"
    ]):
        operations.append("remove_duplicate_columns")

    # Replace negative values with mean
    if any(phrase in prompt for phrase in [
        "replace negative values with mean",
        "replace negative values by mean",
        "negative values with mean"
    ]):
        operations.append("replace_negative_with_mean")

    # Remove invalid rows
    if any(phrase in prompt for phrase in [
        "remove invalid rows",
        "delete invalid rows",
        "remove invalid data",
        "delete invalid data"
    ]):
        operations.append("remove_invalid_rows")

    # Standardize text (lowercase / uppercase / title case)
    if any(phrase in prompt for phrase in [
        "standardize text",
        "normalize text",
        "clean text",
        "standardize the text",
        "text formatting",
        "format text"
    ]):
        if any(word in prompt for word in ["uppercase", "upper case", "capital letters", "all caps"]):
            operations.append("standardize_text_upper")
        elif any(word in prompt for word in ["title case", "capitalize", "capitalize each word"]):
            operations.append("standardize_text_title")
        else:
            operations.append("standardize_text_lower")

    if any(phrase in prompt for phrase in ["lowercase text", "convert text to lowercase", "make text lowercase"]):
        operations.append("standardize_text_lower")

    if any(phrase in prompt for phrase in ["uppercase text", "convert text to uppercase", "make text uppercase"]):
        operations.append("standardize_text_upper")

    if any(phrase in prompt for phrase in ["title case text", "convert text to title case", "capitalize text"]):
        operations.append("standardize_text_title")

    # Remove duplicate operations if detected more than once
    operations = list(dict.fromkeys(operations))

    return operations


def detect_filter_condition(prompt):
    prompt_lower = prompt.lower()

    if "keep rows" in prompt_lower:
        action = "keep"
    elif "remove rows" in prompt_lower or "delete rows" in prompt_lower:
        action = "remove"
    else:
        return None

    match = re.search(
        r"where\s+([a-zA-Z0-9_ ]+?)\s+(is greater than|is more than|is less than|is equal to|is not equal to|greater than|more than|less than|equal to|contains|equals|is)\s+([a-zA-Z0-9_. ]+)",
        prompt_lower
    )

    if not match:
        return None

    column_raw = match.group(1).strip()
    operator_raw = match.group(2).strip()
    value_raw = match.group(3).strip()

    operator_map = {
        "is": "equals",
        "equals": "equals",
        "equal to": "equals",
        "is equal to": "equals",
        "greater than": "greater_than",
        "more than": "greater_than",
        "is greater than": "greater_than",
        "is more than": "greater_than",
        "less than": "less_than",
        "is less than": "less_than",
        "contains": "contains"
    }

    return {
        "action": action,
        "column_raw": column_raw,
        "operator": operator_map.get(operator_raw),
        "value_raw": value_raw
    }


def detect_sort_condition(prompt):
    prompt_lower = prompt.lower()

    if "sort" not in prompt_lower:
        return None

    match = re.search(
        r"sort(?:\s+rows)?\s+by\s+([a-zA-Z0-9_ ]+?)(?:\s+in)?(?:\s+(ascending|descending|asc|desc)(?:\s+order)?)?$",
        prompt_lower
    )

    if not match:
        return None

    column_raw = match.group(1).strip()
    direction_raw = match.group(2)

    if direction_raw in ("descending", "desc"):
        direction = "descending"
    else:
        direction = "ascending"

    return {
        "column_raw": column_raw,
        "direction": direction
    }


def detect_rename_conditions(prompt):
    prompt_lower = prompt.lower()

    if "rename" not in prompt_lower:
        return []

    matches = re.findall(
        r"rename\s+([a-zA-Z0-9_ ]+?)\s+to\s+([a-zA-Z0-9_ ]+?)(?=\s+and\s+rename|\s*$|,)",
        prompt_lower
    )

    rename_conditions = []

    for old_name, new_name in matches:
        rename_conditions.append({
            "old_name_raw": old_name.strip(),
            "new_name": new_name.strip()
        })

    return rename_conditions


def detect_calculated_column(prompt):
    prompt_lower = prompt.lower()

    if "column" not in prompt_lower or " as " not in prompt_lower:
        return None

    match = re.search(
        r"(?:create|add)\s+(?:a\s+)?column\s+([a-zA-Z0-9_ ]+?)\s+as\s+(.+)",
        prompt_lower
    )

    if not match:
        return None

    new_name = match.group(1).strip()
    expr_raw = match.group(2).strip()

    return {
        "new_name": new_name,
        "expr_raw": expr_raw
    }


def apply_calculated_column(df, calc_column):
    if not calc_column:
        return df

    new_name = calc_column["new_name"]
    expr = calc_column["expr_raw"]

    expr = expr.replace(" multiplied by ", " * ")
    expr = expr.replace(" times ", " * ")
    expr = expr.replace(" divided by ", " / ")
    expr = expr.replace(" plus ", " + ")
    expr = expr.replace(" minus ", " - ")

    sorted_columns = sorted(df.columns, key=len, reverse=True)

    column_map = {}
    for index, col in enumerate(sorted_columns):
        placeholder = f"col{index}ref"
        pattern = re.compile(re.escape(col.lower()))
        if pattern.search(expr.lower()):
            expr = pattern.sub(placeholder, expr, count=0)
            column_map[placeholder] = col

    if not re.match(r'^[a-zA-Z0-9_\.\+\-\*\/\(\)\s]+$', expr):
        return df

    eval_locals = {}
    for placeholder, col in column_map.items():
        eval_locals[placeholder] = pd.to_numeric(df[col], errors="coerce")

    try:
        result = eval(expr, {"__builtins__": {}}, eval_locals)
        df[new_name] = result
    except Exception:
        pass

    return df


def detect_group_condition(prompt):
    prompt_lower = prompt.lower()

    if "group by" not in prompt_lower:
        return None

    match = re.search(
        r"group by\s+([a-zA-Z0-9_ ]+?)\s+and\s+(sum|average|avg|mean|count|min|minimum|max|maximum)\s+([a-zA-Z0-9_ ]+)",
        prompt_lower
    )

    if not match:
        return None

    group_column_raw = match.group(1).strip()
    agg_raw = match.group(2).strip()
    agg_column_raw = match.group(3).strip()

    agg_map = {
        "sum": "sum",
        "average": "mean",
        "avg": "mean",
        "mean": "mean",
        "count": "count",
        "min": "min",
        "minimum": "min",
        "max": "max",
        "maximum": "max"
    }

    return {
        "group_column_raw": group_column_raw,
        "agg_function": agg_map.get(agg_raw),
        "agg_column_raw": agg_column_raw
    }

def detect_summary_sheet(prompt):
    prompt_lower = prompt.lower()

    if any(phrase in prompt_lower for phrase in [
        "create summary sheet",
        "create a summary sheet",
        "generate summary sheet",
        "generate a summary sheet",
        "create summary",
        "create a summary",
        "summarize dataset",
        "summarize the dataset",
        "summarize data",
        "dataset summary",
        "column summary",
        "column statistics",
        "column stats"
    ]):
        return True

    return False


def apply_summary_sheet(df):
    summary_rows = []

    for column in df.columns:
        col_data = df[column]
        numeric_col = pd.to_numeric(col_data, errors="coerce")
        is_numeric = numeric_col.notna().sum() > 0

        row = {
            "column": column,
            "count": int(col_data.notna().sum()),
            "missing": int(col_data.isna().sum()),
            "unique": int(col_data.nunique(dropna=True)),
            "mean": round(float(numeric_col.mean()), 2) if is_numeric else "",
            "min": round(float(numeric_col.min()), 2) if is_numeric else "",
            "max": round(float(numeric_col.max()), 2) if is_numeric else ""
        }

        summary_rows.append(row)

    return pd.DataFrame(summary_rows)

def build_cleaning_plan(prompt):
    if not prompt or not prompt.strip():
        return {
            "steps": [],
            "operations": [],
            "filter_condition": None,
            "sort_condition": None,
            "rename_conditions": [],
            "calc_column": None,
            "group_condition": None,
            "create_summary": False,
            "clarification_needed": True,
            "message": "Please enter cleaning instructions before generating a plan."
        }

    operations = detect_operations(prompt)
    filter_condition = detect_filter_condition(prompt)
    sort_condition = detect_sort_condition(prompt)
    rename_conditions = detect_rename_conditions(prompt)
    calc_column = detect_calculated_column(prompt)
    group_condition = detect_group_condition(prompt)
    create_summary = detect_summary_sheet(prompt)

    plan_steps = []

    for op in operations:
        plan_steps.append({"operation": op, "params": {}})

    if filter_condition:
        plan_steps.append({"operation": "filter_rows", "params": filter_condition})

    if sort_condition:
        plan_steps.append({"operation": "sort_data", "params": sort_condition})

    if rename_conditions:
        plan_steps.append({"operation": "rename_columns", "params": {"renames": rename_conditions}})

    if calc_column:
        plan_steps.append({"operation": "create_calculated_column", "params": calc_column})

    if group_condition:
        plan_steps.append({"operation": "group_summarize", "params": group_condition})

    if create_summary:
        plan_steps.append({"operation": "create_summary_sheet", "params": {}})

    if not plan_steps:
        return {
            "steps": plan_steps,
            "operations": operations,
            "filter_condition": filter_condition,
            "sort_condition": sort_condition,
            "rename_conditions": rename_conditions,
            "calc_column": calc_column,
            "group_condition": group_condition,
            "create_summary": create_summary,
            "clarification_needed": True,
            "message": "I couldn't understand any specific cleaning operation in that prompt. Try being more specific, e.g. 'remove duplicates', 'fill missing values with mean', or 'sort by Salary descending'."
        }

    return {
        "steps": plan_steps,
        "operations": operations,
        "filter_condition": filter_condition,
        "sort_condition": sort_condition,
        "rename_conditions": rename_conditions,
        "calc_column": calc_column,
        "group_condition": group_condition,
        "create_summary": create_summary,
        "clarification_needed": False
    }

def validate_plan(df, plan):
    available_columns = [col.strip().lower() for col in df.columns]
    valid_steps = []
    skipped_steps = []

    def column_exists(col_name):
        return col_name.strip().lower() in available_columns

    for step in plan["steps"]:
        operation = step["operation"]
        params = step["params"]
        is_valid = True
        reason = ""

        if operation == "filter_rows":
            if not column_exists(params.get("column_raw", "")):
                is_valid = False
                reason = f"Column '{params.get('column_raw')}' not found"

        elif operation == "sort_data":
            if not column_exists(params.get("column_raw", "")):
                is_valid = False
                reason = f"Column '{params.get('column_raw')}' not found"

        elif operation == "rename_columns":
            valid_renames = [
                r for r in params.get("renames", [])
                if column_exists(r.get("old_name_raw", ""))
            ]
            if not valid_renames:
                is_valid = False
                reason = "None of the specified columns to rename were found"
            else:
                params["renames"] = valid_renames

        elif operation == "group_summarize":
            group_col = params.get("group_column_raw", "")
            agg_col = params.get("agg_column_raw", "")
            if not column_exists(group_col) or not column_exists(agg_col):
                is_valid = False
                reason = f"Column '{group_col}' or '{agg_col}' not found"

        if is_valid:
            valid_steps.append(step)
        else:
            skipped_steps.append({"operation": operation, "reason": reason})

    plan["steps"] = valid_steps
    plan["skipped_steps"] = skipped_steps

    return plan

def validate_result(operations, before_missing, after_missing, before_duplicates, after_duplicates, skipped_steps):
    warnings = []

    if "remove_duplicates" in operations:
        if before_duplicates > 0 and after_duplicates == before_duplicates:
            warnings.append("Remove duplicates was requested, but no duplicate rows were removed.")

    if any(op in operations for op in ["fill_missing_mean", "fill_missing_median", "fill_missing_mode"]):
        if before_missing > 0 and after_missing == before_missing:
            warnings.append("Fill missing values was requested, but no missing values were changed.")

    if skipped_steps:
        for s in skipped_steps:
            warnings.append(f"Skipped: {s['operation']} ({s['reason']})")

    return {
        "status": "warning" if warnings else "passed",
        "warnings": warnings
    }

def apply_operations(df, operations, filter_condition=None, sort_condition=None, rename_conditions=None, group_condition=None):

    for operation in operations:

        if operation == "remove_duplicates":
            df = df.drop_duplicates()

        elif operation == "fill_missing_mean":
            numeric_columns = df.select_dtypes(include="number").columns

            for column in numeric_columns:
                df[column] = df[column].fillna(df[column].mean())

        elif operation == "fill_missing_median":
            numeric_columns = df.select_dtypes(include="number").columns

            for column in numeric_columns:
                df[column] = df[column].fillna(df[column].median())

        elif operation == "fill_missing_mode":
            for column in df.columns:
                if df[column].isnull().any():
                    mode_value = df[column].mode()

                    if not mode_value.empty:
                        df[column] = df[column].fillna(mode_value[0])

        elif operation == "remove_empty_rows":
            df = df.dropna(how="all")

        elif operation == "remove_empty_columns":
            df = df.dropna(axis=1, how="all")

        elif operation == "standardize_columns":
            df.columns = (
                df.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_")
            )

        elif operation == "remove_negative_values":
            numeric_columns = df.select_dtypes(include="number").columns

            for column in numeric_columns:
                df[column] = df[column].clip(lower=0)

        elif operation == "remove_extra_spaces":
            for column in df.select_dtypes(include="object").columns:
                df[column] = df[column].str.strip()

        elif operation == "standardize_text_lower":
            for column in df.select_dtypes(include="object").columns:
                df[column] = df[column].str.lower()

        elif operation == "standardize_text_upper":
            for column in df.select_dtypes(include="object").columns:
                df[column] = df[column].str.upper()

        elif operation == "standardize_text_title":
            for column in df.select_dtypes(include="object").columns:
                df[column] = df[column].str.title()

        elif operation == "remove_missing":
            df = df.dropna()

        elif operation == "convert_numeric":
            for column in df.columns:
                converted = pd.to_numeric(df[column], errors="coerce")

                if converted.notna().sum() > 0:
                    df[column] = converted

        elif operation == "convert_to_text":
            for column in df.columns:
                df[column] = df[column].astype(str)

        elif operation == "convert_to_date":
            for column in df.columns:
                converted = pd.to_datetime(df[column], errors="coerce")

                if converted.notna().sum() > 0:
                    df[column] = converted

        elif operation == "standardize_dates":
            for column in df.columns:
                converted = pd.to_datetime(df[column], errors="coerce")

                if converted.notna().sum() > 0:
                    df[column] = converted.dt.strftime("%Y-%m-%d")

        elif operation == "remove_duplicate_columns":
            df = df.loc[:, ~df.columns.duplicated()]

        elif operation == "replace_negative_with_mean":
            numeric_columns = df.select_dtypes(include="number").columns

            for column in numeric_columns:
                mean_value = df.loc[df[column] >= 0, column].mean()

                if pd.notna(mean_value):
                    df[column] = df[column].astype(float)
                    df.loc[df[column] < 0, column] = mean_value

        elif operation == "filter_rows" and filter_condition:
            column_raw = filter_condition["column_raw"]
            operator = filter_condition["operator"]
            value_raw = filter_condition["value_raw"]
            action = filter_condition["action"]

            matched_column = None
            for col in df.columns:
                if col.strip().lower() == column_raw.strip().lower():
                    matched_column = col
                    break

            condition = None

            if matched_column is not None and operator:
                if operator == "equals":
                    condition = df[matched_column].astype(str).str.lower() == value_raw.lower()

                elif operator == "contains":
                    condition = df[matched_column].astype(str).str.lower().str.contains(value_raw.lower(), na=False)

                elif operator in ("greater_than", "less_than"):
                    try:
                        value_num = float(value_raw)
                        numeric_column = pd.to_numeric(df[matched_column], errors="coerce")

                        if operator == "greater_than":
                            condition = numeric_column > value_num
                        else:
                            condition = numeric_column < value_num
                    except ValueError:
                        condition = None

            if condition is not None:
                if action == "keep":
                    df = df[condition]
                else:
                    df = df[~condition]

        elif operation == "sort_data" and sort_condition:
            column_raw = sort_condition["column_raw"]
            direction = sort_condition["direction"]

            matched_column = None
            for col in df.columns:
                if col.strip().lower() == column_raw.strip().lower():
                    matched_column = col
                    break

            if matched_column is not None:
                df = df.sort_values(
                    by=matched_column,
                    ascending=(direction == "ascending")
                )

        elif operation == "rename_columns" and rename_conditions:
            rename_map = {}

            for condition in rename_conditions:
                old_name_raw = condition["old_name_raw"]
                new_name = condition["new_name"]

                matched_column = None
                for col in df.columns:
                    if col.strip().lower() == old_name_raw.strip().lower():
                        matched_column = col
                        break

                if matched_column is not None:
                    rename_map[matched_column] = new_name

            if rename_map:
                df = df.rename(columns=rename_map)

        elif operation == "group_summarize" and group_condition:
            group_column_raw = group_condition["group_column_raw"]
            agg_function = group_condition["agg_function"]
            agg_column_raw = group_condition["agg_column_raw"]

            matched_group_column = None
            matched_agg_column = None

            for col in df.columns:
                if col.strip().lower() == group_column_raw.strip().lower():
                    matched_group_column = col
                if col.strip().lower() == agg_column_raw.strip().lower():
                    matched_agg_column = col

            if matched_group_column is not None and matched_agg_column is not None and agg_function:
                if agg_function != "count":
                    df[matched_agg_column] = pd.to_numeric(df[matched_agg_column], errors="coerce")

                df = df.groupby(matched_group_column, as_index=False)[matched_agg_column].agg(agg_function)

    return df

def describe_step(step):
    operation = step["operation"]
    params = step.get("params", {})

    descriptions = {
        "remove_duplicates": "Remove duplicate rows",
        "fill_missing_mean": "Fill missing values using the mean",
        "fill_missing_median": "Fill missing values using the median",
        "fill_missing_mode": "Fill missing values using the mode",
        "remove_empty_rows": "Remove completely empty rows",
        "remove_empty_columns": "Remove completely empty columns",
        "standardize_columns": "Standardize column names",
        "remove_negative_values": "Remove negative values (set to 0)",
        "remove_extra_spaces": "Remove extra spaces from text",
        "remove_missing": "Remove rows with any missing values",
        "convert_numeric": "Convert columns to numeric where possible",
        "convert_to_text": "Convert columns to text",
        "convert_to_date": "Convert columns to date",
        "standardize_dates": "Standardize dates to YYYY-MM-DD",
        "remove_duplicate_columns": "Remove duplicate columns",
        "replace_negative_with_mean": "Replace negative values with the column mean",
        "standardize_text_lower": "Convert text to lowercase",
        "standardize_text_upper": "Convert text to UPPERCASE",
        "standardize_text_title": "Convert text to Title Case",
        "create_summary_sheet": "Create a summary sheet of column statistics"
    }

    if operation in descriptions:
        return descriptions[operation]

    if operation == "filter_rows":
        action = "Keep" if params.get("action") == "keep" else "Remove"
        return f"{action} rows where {params.get('column_raw')} {params.get('operator')} {params.get('value_raw')}"

    if operation == "sort_data":
        return f"Sort by {params.get('column_raw')} ({params.get('direction')})"

    if operation == "rename_columns":
        renames = params.get("renames", [])
        parts = [f"{r['old_name_raw']} \u2192 {r['new_name']}" for r in renames]
        return "Rename columns: " + ", ".join(parts)

    if operation == "create_calculated_column":
        return f"Create column '{params.get('new_name')}' as {params.get('expr_raw')}"

    if operation == "group_summarize":
        return f"Group by {params.get('group_column_raw')} and {params.get('agg_function')} {params.get('agg_column_raw')}"

    return operation


@router.post("/preview-plan")
async def preview_plan(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    filename = file.filename or ""
    extension = os.path.splitext(filename)[1].lower()

    try:
        if extension in [".xlsx", ".xls"]:
            df = pd.read_excel(file.file)
        elif extension == ".csv":
            df = pd.read_csv(file.file)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload .xlsx, .xls, or .csv"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to read the file: {str(e)}"
        )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file has no data rows to clean."
        )

    plan = build_cleaning_plan(prompt)
    plan = validate_plan(df, plan)

    readable_steps = [
        {"operation": step["operation"], "description": describe_step(step)}
        for step in plan["steps"]
    ]

    has_plan = len(readable_steps) > 0
    clarification_needed = plan.get("clarification_needed", False) or not has_plan
    message = plan.get("message", "")

    if not has_plan and not message:
        skipped = plan.get("skipped_steps", [])
        if skipped:
            reasons = "; ".join(s["reason"] for s in skipped)
            message = f"None of the requested operations could be applied: {reasons}"
        else:
            message = "I couldn't understand any specific cleaning operation in that prompt. Try being more specific, e.g. 'remove duplicates', 'fill missing values with mean', or 'sort by Salary descending'."

    return {
        "steps": readable_steps,
        "skipped_steps": plan.get("skipped_steps", []),
        "has_plan": has_plan,
        "clarification_needed": clarification_needed,
        "message": message
    }

@router.post("/ai-clean")
async def ai_clean_excel(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):

    filename = file.filename or ""
    extension = os.path.splitext(filename)[1].lower()

    try:
        if extension in [".xlsx", ".xls"]:
            df = pd.read_excel(file.file)

        elif extension == ".csv":
            df = pd.read_csv(file.file)

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload .xlsx, .xls, or .csv"
            )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to read the file: {str(e)}"
        )



    # BEFORE cleaning information
    before_rows = len(df)
    before_columns = len(df.columns)
    before_missing = int(df.isnull().sum().sum())
    before_duplicates = int(df.duplicated().sum())

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file has no data rows to clean."
        )

    plan = build_cleaning_plan(prompt)
    plan = validate_plan(df, plan)

    operations = [step["operation"] for step in plan["steps"] if step["operation"] in plan["operations"]]
    valid_op_names = [step["operation"] for step in plan["steps"]]

    filter_condition = plan["filter_condition"] if "filter_rows" in valid_op_names else None
    sort_condition = plan["sort_condition"] if "sort_data" in valid_op_names else None
    rename_conditions = plan["rename_conditions"] if "rename_columns" in valid_op_names else []
    calc_column = plan["calc_column"] if "create_calculated_column" in valid_op_names else None
    group_condition = plan["group_condition"] if "group_summarize" in valid_op_names else None
    create_summary = plan["create_summary"] if "create_summary_sheet" in valid_op_names else False

    operations = valid_op_names

    if not operations:
        return {
            "status": "no_operation",
            "message": "No supported cleaning operation was detected.",
            "prompt": prompt,
            "suggestions": [
            "Remove duplicate rows",
            "Fill missing values with mean",
            "Remove empty rows",
            "Remove extra spaces",
            "Standardize column names"
        ]
    }

    df = apply_operations(df, operations, filter_condition, sort_condition, rename_conditions, group_condition)

    if calc_column:
        df = apply_calculated_column(df, calc_column)

    if create_summary:
        df = apply_summary_sheet(df)

    # AFTER cleaning information
    after_rows = len(df)
    after_columns = len(df.columns)
    after_missing = int(df.isnull().sum().sum())
    after_duplicates = int(df.duplicated().sum())

    # Cleaning summary
    cleaning_summary = {
        "before": {
            "rows": before_rows,
            "columns": before_columns,
            "missing_values": before_missing,
            "duplicate_rows": before_duplicates
        },
        "after": {
            "rows": after_rows,
            "columns": after_columns,
            "missing_values": after_missing,
            "duplicate_rows": after_duplicates
        },
        "changes": {
            "rows_removed": before_rows - after_rows,
            "columns_removed": before_columns - after_columns,
            "missing_values_changed": before_missing - after_missing,
            "duplicates_removed": before_duplicates - after_duplicates
        },
        "operations": operations
    }

    if plan.get("skipped_steps"):
        cleaning_summary["skipped_steps"] = plan["skipped_steps"]

    cleaning_summary["validation"] = validate_result(
        operations, before_missing, after_missing, before_duplicates, after_duplicates, plan.get("skipped_steps", [])
    )

    latest_summary.clear()
    latest_summary.update(cleaning_summary)

    print("Cleaning Summary:")
    print(cleaning_summary)

    # Save cleaning history
    db = SessionLocal()

    history = CleaningHistory(
        filename=file.filename,
        prompt=prompt,
        operations=", ".join(operations),
        status="completed"
    )

    db.add(history)
    db.commit()
    db.close()

    # Create data folder
    output_folder = "data"
    os.makedirs(output_folder, exist_ok=True)

    # Create output file
    output_file = os.path.abspath(
        os.path.join(
            output_folder,
            "cleaned_" + file.filename
        )
    )

    if extension == ".csv":
        df.to_csv(output_file, index=False)

        return FileResponse(
            path=output_file,
            media_type="text/csv",
            filename="cleaned_" + file.filename
        )
    else:
        df.to_excel(
            output_file,
            index=False,
            engine="openpyxl"
        )

        return FileResponse(
            path=output_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="cleaned_" + file.filename
        )


@router.get("/history")
def get_history():

    db = SessionLocal()

    history = db.query(CleaningHistory).all()

    result = []

    for item in history:
        result.append({
            "id": item.id,
            "filename": item.filename,
            "prompt": item.prompt,
            "operations": item.operations,
            "status": item.status,
            "created_at": item.created_at
        })

    db.close()

    return result

@router.get("/summary")
def get_summary():
    return latest_summary