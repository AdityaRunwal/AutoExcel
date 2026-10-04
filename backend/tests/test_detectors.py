import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.routes.ai_clean import detect_operations, detect_filter_condition, detect_sort_condition


# ---------- detect_operations ----------

def test_detect_remove_duplicates():
    assert "remove_duplicates" in detect_operations("remove duplicate rows")

def test_detect_remove_duplicates_synonym():
    assert "remove_duplicates" in detect_operations("delete repeated records")

def test_detect_fill_missing_mean():
    ops = detect_operations("fill missing values with mean")
    assert "fill_missing_mean" in ops

def test_detect_fill_missing_median():
    ops = detect_operations("fill missing values with median")
    assert "fill_missing_median" in ops

def test_detect_fill_missing_mode():
    ops = detect_operations("replace missing values with the most common value")
    assert "fill_missing_mode" in ops

def test_detect_remove_extra_spaces():
    ops = detect_operations("remove extra spaces")
    assert "remove_extra_spaces" in ops

def test_detect_standardize_text_upper():
    ops = detect_operations("standardize text to uppercase")
    assert "standardize_text_upper" in ops

def test_detect_standardize_text_title():
    ops = detect_operations("standardize text to title case")
    assert "standardize_text_title" in ops

def test_detect_standardize_text_lower_default():
    ops = detect_operations("standardize text")
    assert "standardize_text_lower" in ops

def test_detect_multiple_operations():
    ops = detect_operations("remove duplicate rows and remove extra spaces")
    assert "remove_duplicates" in ops
    assert "remove_extra_spaces" in ops

def test_detect_no_operations():
    ops = detect_operations("make me a pivot chart")
    assert ops == []

def test_detect_no_duplicate_operations_in_result():
    ops = detect_operations("remove duplicate rows, remove duplicates, remove duplicate")
    assert ops.count("remove_duplicates") == 1

def test_detect_remove_negative_values():
    ops = detect_operations("remove negative values")
    assert "remove_negative_values" in ops

def test_detect_replace_negative_with_mean():
    ops = detect_operations("replace negative values with mean")
    assert "replace_negative_with_mean" in ops
    # Must NOT also trigger plain remove_negative_values
    assert "remove_negative_values" not in ops


# ---------- detect_filter_condition ----------

def test_filter_remove_greater_than():
    result = detect_filter_condition("remove rows where Age is greater than 60")
    assert result is not None
    assert result["action"] == "remove"
    assert result["column_raw"] == "age"
    assert result["operator"] == "greater_than"
    assert result["value_raw"] == "60"

def test_filter_keep_less_than():
    result = detect_filter_condition("keep rows where Salary is less than 50000")
    assert result is not None
    assert result["action"] == "keep"
    assert result["operator"] == "less_than"

def test_filter_contains():
    result = detect_filter_condition("remove rows where City contains Pune")
    assert result is not None
    assert result["operator"] == "contains"

def test_filter_no_match_returns_none():
    result = detect_filter_condition("remove duplicates")
    assert result is None


# ---------- detect_sort_condition ----------

def test_sort_descending():
    result = detect_sort_condition("sort by Salary descending")
    assert result is not None
    assert result["column_raw"] == "salary"
    assert result["direction"] == "descending"

def test_sort_ascending_default():
    result = detect_sort_condition("sort by Age")
    assert result is not None
    assert result["direction"] == "ascending"

def test_sort_no_sort_keyword_returns_none():
    result = detect_sort_condition("remove duplicates")
    assert result is None

from app.routes.ai_clean import (
    detect_rename_conditions,
    detect_calculated_column,
    detect_group_condition,
    detect_summary_sheet,
)


# ---------- detect_rename_conditions ----------

def test_rename_single():
    result = detect_rename_conditions("rename Age to Years")
    assert len(result) == 1
    assert result[0]["old_name_raw"] == "age"
    assert result[0]["new_name"] == "years"

def test_rename_multiple():
    result = detect_rename_conditions("rename Age to Years and rename City to Location")
    assert len(result) == 2
    assert result[0]["old_name_raw"] == "age"
    assert result[0]["new_name"] == "years"
    assert result[1]["old_name_raw"] == "city"
    assert result[1]["new_name"] == "location"

def test_rename_no_rename_keyword():
    result = detect_rename_conditions("remove duplicates")
    assert result == []


# ---------- detect_calculated_column ----------

def test_calculated_column_basic():
    result = detect_calculated_column("create a column Total as Price times Quantity")
    assert result is not None
    assert result["new_name"] == "total"
    assert "price" in result["expr_raw"]
    assert "quantity" in result["expr_raw"]

def test_calculated_column_add_variant():
    result = detect_calculated_column("add column Total as Price plus Tax")
    assert result is not None
    assert result["new_name"] == "total"

def test_calculated_column_no_match():
    result = detect_calculated_column("remove duplicates")
    assert result is None

def test_calculated_column_missing_column_keyword():
    result = detect_calculated_column("create Total as Price times Quantity")
    assert result is None


# ---------- detect_group_condition ----------

def test_group_sum():
    result = detect_group_condition("group by City and sum Score")
    assert result is not None
    assert result["group_column_raw"] == "city"
    assert result["agg_function"] == "sum"
    assert result["agg_column_raw"] == "score"

def test_group_average_synonym():
    result = detect_group_condition("group by Region and average Sales")
    assert result is not None
    assert result["agg_function"] == "mean"

def test_group_no_groupby_keyword():
    result = detect_group_condition("remove duplicates")
    assert result is None

def test_group_missing_aggregation():
    result = detect_group_condition("group by City")
    assert result is None


# ---------- detect_summary_sheet ----------

def test_summary_sheet_true():
    assert detect_summary_sheet("create summary sheet") is True

def test_summary_sheet_synonym():
    assert detect_summary_sheet("summarize the dataset") is True

def test_summary_sheet_false():
    assert detect_summary_sheet("remove duplicates") is False

# ---------- Phase 10: expanded synonym coverage ----------

def test_detect_remove_empty_rows_synonym():
    ops = detect_operations("drop empty rows")
    assert "remove_empty_rows" in ops

def test_detect_remove_empty_columns_synonym():
    ops = detect_operations("get rid of empty columns")
    assert "remove_empty_columns" in ops

def test_detect_standardize_columns_synonym():
    ops = detect_operations("fix the column names")
    assert "standardize_columns" in ops

def test_detect_convert_numeric_synonym():
    ops = detect_operations("turn columns into numbers")
    assert "convert_numeric" in ops

def test_detect_remove_duplicate_columns_synonym():
    ops = detect_operations("drop duplicate columns")
    assert "remove_duplicate_columns" in ops

def test_detect_standardize_dates_synonym():
    ops = detect_operations("fix the dates")
    assert "standardize_dates" in ops