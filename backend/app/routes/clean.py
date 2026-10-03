from fastapi import APIRouter, UploadFile, File, Form
import pandas as pd

router = APIRouter()


@router.post("/clean")
async def clean_excel(
    file: UploadFile = File(...),
    operation: str = Form(...)
):
    df = pd.read_excel(file.file)

    if operation == "remove_duplicates":
        original_rows = len(df)

        df = df.drop_duplicates()

        removed_rows = original_rows - len(df)

        return {
            "filename": file.filename,
            "operation": operation,
            "original_rows": original_rows,
            "remaining_rows": len(df),
            "removed_rows": removed_rows
        }

    if operation == "remove_missing":
        original_rows = len(df)

        df = df.dropna()

        removed_rows = original_rows - len(df)

        return {
            "filename": file.filename,
            "operation": operation,
            "original_rows": original_rows,
            "remaining_rows": len(df),
            "removed_rows": removed_rows
        }

    if operation == "fill_missing_mean":
        numeric_columns = df.select_dtypes(include="number").columns

        for column in numeric_columns:
            df[column] = df[column].fillna(df[column].mean())

        return {
            "filename": file.filename,
            "operation": operation,
            "numeric_columns": numeric_columns.tolist(),
            "message": "Missing numerical values filled with mean"
        }

    if operation == "fill_missing_median":
        numeric_columns = df.select_dtypes(include="number").columns

        for column in numeric_columns:
            df[column] = df[column].fillna(df[column].median())

        return {
            "filename": file.filename,
            "operation": operation,
            "numeric_columns": numeric_columns.tolist(),
            "message": "Missing numerical values filled with median"
        }

    if operation == "fill_missing_mode":
        for column in df.columns:
            if df[column].isnull().any():
                mode_value = df[column].mode()

                if not mode_value.empty:
                    df[column] = df[column].fillna(mode_value[0])

        return {
            "filename": file.filename,
            "operation": operation,
            "message": "Missing values filled with mode"
        }

    if operation == "remove_empty_columns":
        original_columns = len(df.columns)

        df = df.dropna(axis=1, how="all")

        removed_columns = original_columns - len(df.columns)

        return {
            "filename": file.filename,
            "operation": operation,
            "original_columns": original_columns,
            "remaining_columns": len(df.columns),
            "removed_columns": removed_columns
        }

    if operation == "remove_empty_rows":
        original_rows = len(df)

        df = df.dropna(how="all")

        removed_rows = original_rows - len(df)

        return {
            "filename": file.filename,
            "operation": operation,
            "original_rows": original_rows,
            "remaining_rows": len(df),
            "removed_rows": removed_rows
        }

    if operation == "standardize_columns":
        original_columns = df.columns.tolist()

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        return {
            "filename": file.filename,
            "operation": operation,
            "original_columns": original_columns,
            "new_columns": df.columns.tolist()
        }

    if operation == "convert_numeric":
        converted_columns = []

        for column in df.columns:
            converted = pd.to_numeric(df[column], errors="coerce")

            if converted.notna().sum() > 0:
                df[column] = converted
                converted_columns.append(column)

        return {
            "filename": file.filename,
            "operation": operation,
            "converted_columns": converted_columns,
            "message": "Columns converted to numeric where possible"
        }

    if operation == "remove_extra_spaces":
        text_columns = []

        for column in df.select_dtypes(include="object").columns:
            df[column] = df[column].str.strip()
            text_columns.append(column)

        return {
            "filename": file.filename,
            "operation": operation,
            "text_columns": text_columns,
            "message": "Extra spaces removed from text columns"
        }

    if operation == "remove_duplicate_columns":
        original_columns = len(df.columns)

        df = df.loc[:, ~df.columns.duplicated()]

        removed_columns = original_columns - len(df.columns)

        return {
            "filename": file.filename,
            "operation": operation,
            "original_columns": original_columns,
            "remaining_columns": len(df.columns),
            "removed_columns": removed_columns
        }

    if operation == "remove_negative_values":
        numeric_columns = df.select_dtypes(include="number").columns

        for column in numeric_columns:
            df[column] = df[column].clip(lower=0)

        return {
            "filename": file.filename,
            "operation": operation,
            "numeric_columns": numeric_columns.tolist(),
            "message": "Negative numerical values replaced with 0"
        }

    if operation == "replace_negative_with_mean":
        numeric_columns = df.select_dtypes(include="number").columns

        for column in numeric_columns:
            mean_value = df[column][df[column] >= 0].mean()
            df.loc[df[column] < 0, column] = mean_value

        return {
            "filename": file.filename,
            "operation": operation,
            "numeric_columns": numeric_columns.tolist(),
            "message": "Negative values replaced with column mean"
        }

    if operation == "remove_invalid_rows":
        original_rows = len(df)

        df = df.replace([float("inf"), float("-inf")], pd.NA)
        df = df.dropna()

        removed_rows = original_rows - len(df)

        return {
            "filename": file.filename,
            "operation": operation,
            "original_rows": original_rows,
            "remaining_rows": len(df),
            "removed_rows": removed_rows
        }

    return {
        "error": "Operation not supported"
    }