import sys
import os
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.routes.ai_clean import validate_plan, validate_result


def make_sample_df():
    return pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "Salary": [50000, 60000, 70000]
    })


# ---------- validate_plan ----------

def test_validate_plan_keeps_valid_step():
    df = make_sample_df()
    plan = {
        "steps": [
            {"operation": "sort_data", "params": {"column_raw": "age"}}
        ]
    }
    result = validate_plan(df, plan)
    assert len(result["steps"]) == 1
    assert result["skipped_steps"] == []

def test_validate_plan_skips_invalid_column():
    df = make_sample_df()
    plan = {
        "steps": [
            {"operation": "sort_data", "params": {"column_raw": "NotARealColumn"}}
        ]
    }
    result = validate_plan(df, plan)
    assert len(result["steps"]) == 0
    assert len(result["skipped_steps"]) == 1
    assert result["skipped_steps"][0]["operation"] == "sort_data"

def test_validate_plan_remove_duplicates_always_valid():
    df = make_sample_df()
    plan = {
        "steps": [
            {"operation": "remove_duplicates", "params": {}}
        ]
    }
    result = validate_plan(df, plan)
    assert len(result["steps"]) == 1
    assert result["skipped_steps"] == []

def test_validate_plan_rename_partial_valid():
    df = make_sample_df()
    plan = {
        "steps": [
            {"operation": "rename_columns", "params": {"renames": [
                {"old_name_raw": "age", "new_name_raw": "years"},
                {"old_name_raw": "FakeColumn", "new_name_raw": "ghost"}
            ]}}
        ]
    }
    result = validate_plan(df, plan)
    assert len(result["steps"]) == 1
    assert len(result["steps"][0]["params"]["renames"]) == 1
    assert result["steps"][0]["params"]["renames"][0]["old_name_raw"] == "age"

def test_validate_plan_group_summarize_invalid_column():
    df = make_sample_df()
    plan = {
        "steps": [
            {"operation": "group_summarize", "params": {
                "group_column_raw": "FakeGroup",
                "agg_column_raw": "Salary"
            }}
        ]
    }
    result = validate_plan(df, plan)
    assert len(result["steps"]) == 0
    assert len(result["skipped_steps"]) == 1


# ---------- validate_result ----------

def test_validate_result_passes_when_duplicates_removed():
    result = validate_result(
        operations=["remove_duplicates"],
        before_missing=0, after_missing=0,
        before_duplicates=2, after_duplicates=0,
        skipped_steps=[]
    )
    assert result["status"] == "passed"
    assert result["warnings"] == []

def test_validate_result_warns_when_duplicates_not_removed():
    result = validate_result(
        operations=["remove_duplicates"],
        before_missing=0, after_missing=0,
        before_duplicates=2, after_duplicates=2,
        skipped_steps=[]
    )
    assert result["status"] == "warning"
    assert len(result["warnings"]) == 1

def test_validate_result_warns_when_missing_not_changed():
    result = validate_result(
        operations=["fill_missing_mean"],
        before_missing=5, after_missing=5,
        before_duplicates=0, after_duplicates=0,
        skipped_steps=[]
    )
    assert result["status"] == "warning"

def test_validate_result_includes_skipped_steps_as_warnings():
    result = validate_result(
        operations=["sort_data"],
        before_missing=0, after_missing=0,
        before_duplicates=0, after_duplicates=0,
        skipped_steps=[{"operation": "rename_columns", "reason": "Column 'X' not found"}]
    )
    assert result["status"] == "warning"
    assert any("rename_columns" in w for w in result["warnings"])