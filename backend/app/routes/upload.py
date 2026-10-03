from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import os

router = APIRouter()


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):

    filename = file.filename or ""
    extension = os.path.splitext(filename)[1].lower()

    try:
        # Read dataset according to file type
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

    # Basic dataset information
    rows = len(df)
    columns = len(df.columns)

    # Missing values
    missing_values = df.isnull().sum().to_dict()
    total_missing_values = int(df.isnull().sum().sum())

    # Duplicate rows
    duplicate_rows = int(df.duplicated().sum())

    # Empty rows
    empty_rows = int(df.isnull().all(axis=1).sum())

    # Empty columns
    empty_columns = int(df.isnull().all(axis=0).sum())

    # Data types
    data_types = df.dtypes.astype(str).to_dict()

    # Numeric and text columns
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    text_columns = df.select_dtypes(include="object").columns.tolist()

    # Statistics
    try:
        statistics = df.describe().to_dict()
    except Exception:
        statistics = {}

        # Build a JSON-safe preview of the first 10 rows
    preview_df = df.head(10).copy()

    preview_df = preview_df.astype(object).where(
        pd.notnull(preview_df),
        None
    )

    preview = preview_df.to_dict(orient="records")

    return {
        "filename": filename,
        "file_type": extension,

        "rows": rows,
        "columns": columns,
        "column_names": df.columns.tolist(),

        "data_types": data_types,

        "numeric_columns": numeric_columns,
        "text_columns": text_columns,

        "missing_values": missing_values,
        "total_missing_values": total_missing_values,

        "duplicate_rows": duplicate_rows,
        "empty_rows": empty_rows,
        "empty_columns": empty_columns,

        "statistics": statistics,

        "preview": preview
    }