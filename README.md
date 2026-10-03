# AutoExcel

**AI-Powered Excel Data Cleaning Application**

AutoExcel is a prompt-based Excel data cleaning application that allows users to upload an Excel file and describe the cleaning operation they want in natural language.

For example:

> Remove duplicate rows, remove extra spaces, and fill missing values with mean

AutoExcel detects the requested operations, cleans the Excel file, generates a cleaned file for download, displays a cleaning summary, and stores the cleaning history in PostgreSQL.

---

## Features

* Upload Excel files
* Natural-language cleaning instructions
* Automatic cleaning-operation detection
* Multiple cleaning operations in a single prompt
* Cleaned Excel file generation
* Download cleaned Excel files
* Before/after cleaning summary
* Operations Applied section
* Cleaning history
* PostgreSQL-based history storage
* Unsupported-prompt handling
* Invalid Excel file handling
* Backend/frontend error handling

---

## Supported Cleaning Operations

AutoExcel currently supports:

1. Remove duplicate rows
2. Fill missing values with mean
3. Fill missing values with median
4. Fill missing values with mode
5. Remove empty rows
6. Remove empty columns
7. Standardize column names
8. Remove negative values
9. Remove extra spaces
10. Remove rows with missing values
11. Convert columns to numeric
12. Remove duplicate columns
13. Replace negative values with mean
14. Remove invalid rows

---

## Example Prompts

### Multiple operations

```text
Remove duplicate rows, remove extra spaces, and fill missing values with mean
```

### Duplicate rows

```text
Remove repeated records
```

### Missing values

```text
Fill blank cells with the average
```

### Median

```text
Replace empty cells using the median
```

### Mode

```text
Fill missing data with the most common value
```

### Negative values

```text
Remove negative valu
```
