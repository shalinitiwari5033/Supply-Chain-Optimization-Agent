from pathlib import Path

import pandas as pd


# =========================================================
# Required Columns
# =========================================================

REQUIRED_COLUMNS = {
    "sales": [
        "date",
        "product_id",
        "product_name",
        "quantity_sold",
        "unit_price",
        "customer_location",
    ],
    "inventory": [
        "product_id",
        "product_name",
        "current_stock",
        "lead_time_days",
        "reorder_level",
        "holding_cost",
        "ordering_cost",
        "warehouse_id",
    ],
    "supplier": [
        "supplier_id",
        "supplier_name",
        "product_id",
        "unit_cost",
        "delivery_time_days",
        "quality_rating",
        "on_time_delivery_rate",
    ],
}


# =========================================================
# Load Dataset
# =========================================================

def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if file_path.suffix.lower() != ".csv":
        raise ValueError(
            "Only CSV files are currently supported."
        )

    df = pd.read_csv(file_path)

    return df


# =========================================================
# Column Validation
# =========================================================

def validate_columns(df, dataset_type):
    """
    Check whether all required columns are present.
    """

    if dataset_type not in REQUIRED_COLUMNS:
        raise ValueError(
            f"Unknown dataset type: {dataset_type}"
        )

    required = set(REQUIRED_COLUMNS[dataset_type])
    actual = set(df.columns)

    missing_columns = sorted(required - actual)
    extra_columns = sorted(actual - required)

    return {
        "valid": len(missing_columns) == 0,
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
    }


# =========================================================
# Data Type Conversion
# =========================================================

def convert_data_types(df, dataset_type):
    """
    Convert important columns to appropriate data types.
    """

    df = df.copy()

    if dataset_type == "sales":

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        numeric_columns = [
            "quantity_sold",
            "unit_price",
        ]

    elif dataset_type == "inventory":

        numeric_columns = [
            "current_stock",
            "lead_time_days",
            "reorder_level",
            "holding_cost",
            "ordering_cost",
        ]

    elif dataset_type == "supplier":

        numeric_columns = [
            "unit_cost",
            "delivery_time_days",
            "quality_rating",
            "on_time_delivery_rate",
        ]

    else:
        raise ValueError(
            f"Unknown dataset type: {dataset_type}"
        )

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


# =========================================================
# Missing Value Report
# =========================================================

def missing_value_report(df):
    """
    Return missing-value counts and percentages.
    """

    missing_count = df.isnull().sum()

    missing_percentage = (
        df.isnull().mean() * 100
    ).round(2)

    report = pd.DataFrame(
        {
            "missing_count": missing_count,
            "missing_percentage": missing_percentage,
        }
    )

    return report


# =========================================================
# Duplicate Report
# =========================================================

def duplicate_report(df):
    """
    Identify duplicate rows.
    """

    duplicate_count = int(
        df.duplicated().sum()
    )

    return {
        "duplicate_count": duplicate_count
    }


# =========================================================
# Invalid Value Detection
# =========================================================

def invalid_value_report(df, dataset_type):
    """
    Detect values that should not be negative
    or outside logical ranges.
    """

    issues = {}

    if dataset_type == "sales":

        issues["negative_quantity"] = int(
            (df["quantity_sold"] < 0).sum()
        )

        issues["negative_price"] = int(
            (df["unit_price"] < 0).sum()
        )

        issues["invalid_dates"] = int(
            df["date"].isna().sum()
        )

    elif dataset_type == "inventory":

        for column in [
            "current_stock",
            "lead_time_days",
            "reorder_level",
            "holding_cost",
            "ordering_cost",
        ]:
            issues[f"negative_{column}"] = int(
                (df[column] < 0).sum()
            )

    elif dataset_type == "supplier":

        for column in [
            "unit_cost",
            "delivery_time_days",
        ]:
            issues[f"negative_{column}"] = int(
                (df[column] < 0).sum()
            )

        issues["invalid_quality_rating"] = int(
            (
                (df["quality_rating"] < 0)
                | (df["quality_rating"] > 5)
            ).sum()
        )

        issues["invalid_on_time_rate"] = int(
            (
                (df["on_time_delivery_rate"] < 0)
                | (df["on_time_delivery_rate"] > 100)
            ).sum()
        )

    return issues


# =========================================================
# Cleaning
# =========================================================

def clean_data(df, dataset_type):
    """
    Clean the dataset using safe, transparent rules.
    """

    df = df.copy()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Convert data types
    df = convert_data_types(
        df,
        dataset_type
    )

    # Remove rows where required core values are missing
    if dataset_type == "sales":

        df = df.dropna(
            subset=[
                "date",
                "product_id",
                "quantity_sold",
            ]
        )

        # Sales cannot have negative quantities
        df = df[
            df["quantity_sold"] >= 0
        ]

        # Prices cannot be negative
        df = df[
            df["unit_price"] >= 0
        ]

    elif dataset_type == "inventory":

        df = df.dropna(
            subset=[
                "product_id",
                "current_stock",
                "lead_time_days",
            ]
        )

        for column in [
            "current_stock",
            "lead_time_days",
            "reorder_level",
            "holding_cost",
            "ordering_cost",
        ]:
            df = df[df[column] >= 0]

    elif dataset_type == "supplier":

        df = df.dropna(
            subset=[
                "supplier_id",
                "product_id",
                "unit_cost",
            ]
        )

        df = df[df["unit_cost"] >= 0]
        df = df[df["delivery_time_days"] >= 0]

        df = df[
            (df["quality_rating"] >= 0)
            & (df["quality_rating"] <= 5)
        ]

        df = df[
            (df["on_time_delivery_rate"] >= 0)
            & (df["on_time_delivery_rate"] <= 100)
        ]

    return df.reset_index(drop=True)


# =========================================================
# Complete Quality Report
# =========================================================

def generate_quality_report(
    original_df,
    cleaned_df,
    dataset_type,
):
    """
    Generate a complete data-quality summary.
    """

    column_report = validate_columns(
        original_df,
        dataset_type
    )

    missing_report = missing_value_report(
        original_df
    )

    duplicate_info = duplicate_report(
        original_df
    )

    invalid_report = invalid_value_report(
        cleaned_df,
        dataset_type
    )

    report = {
        "dataset_type": dataset_type,
        "original_rows": len(original_df),
        "cleaned_rows": len(cleaned_df),
        "rows_removed": (
            len(original_df) - len(cleaned_df)
        ),
        "original_columns": len(original_df.columns),
        "missing_columns": column_report[
            "missing_columns"
        ],
        "extra_columns": column_report[
            "extra_columns"
        ],
        "has_required_columns": column_report[
            "valid"
        ],
        "duplicate_rows": duplicate_info[
            "duplicate_count"
        ],
        "invalid_values": invalid_report,
        "missing_values": missing_report,
    }

    return report


# =========================================================
# Main Validation Pipeline
# =========================================================

def validate_and_clean(
    file_path,
    dataset_type,
):
    """
    Complete validation and cleaning pipeline.

    Returns:
        cleaned_df
        quality_report
    """

    df = load_csv(file_path)

    column_validation = validate_columns(
        df,
        dataset_type
    )

    if not column_validation["valid"]:

        raise ValueError(
            "Missing required columns: "
            + ", ".join(
                column_validation["missing_columns"]
            )
        )

    cleaned_df = clean_data(
        df,
        dataset_type
    )

    report = generate_quality_report(
        df,
        cleaned_df,
        dataset_type
    )

    return cleaned_df, report