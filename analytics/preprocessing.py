import pandas as pd

from utils.validators import (
    validate_columns,
    clean_data,
    missing_value_report,
    duplicate_report,
    invalid_value_report,
)


def preprocess_dataset(
    df: pd.DataFrame,
    dataset_type: str,
):
    """
    Validate and clean a supply-chain dataset.

    Returns:
        cleaned_df
        quality_report
    """

    # -----------------------------------------------------
    # 1. Validate columns
    # -----------------------------------------------------

    column_validation = validate_columns(
        df,
        dataset_type,
    )

    if not column_validation["valid"]:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(
                column_validation["missing_columns"]
            )
        )

    # -----------------------------------------------------
    # 2. Collect original-data information
    # -----------------------------------------------------

    original_rows = len(df)
    original_columns = len(df.columns)

    missing_report = missing_value_report(df)

    duplicate_info = duplicate_report(df)

    # -----------------------------------------------------
    # 3. Clean dataset
    # -----------------------------------------------------

    cleaned_df = clean_data(
        df,
        dataset_type,
    )

    # -----------------------------------------------------
    # 4. Check invalid values after cleaning
    # -----------------------------------------------------

    invalid_report = invalid_value_report(
        cleaned_df,
        dataset_type,
    )

    # -----------------------------------------------------
    # 5. Build quality report
    # -----------------------------------------------------

    rows_removed = (
        original_rows - len(cleaned_df)
    )

    quality_report = {
        "dataset_type": dataset_type,

        "original_rows": original_rows,

        "cleaned_rows": len(cleaned_df),

        "rows_removed": rows_removed,

        "original_columns": original_columns,

        "missing_columns": column_validation[
            "missing_columns"
        ],

        "extra_columns": column_validation[
            "extra_columns"
        ],

        "duplicate_rows": duplicate_info[
            "duplicate_count"
        ],

        "invalid_values": invalid_report,

        "missing_values": missing_report,

        "has_missing_columns": not column_validation[
            "valid"
        ],
    }

    # -----------------------------------------------------
    # 6. Overall quality status
    # -----------------------------------------------------

    if rows_removed == 0 and duplicate_info[
        "duplicate_count"
    ] == 0:

        quality_report["status"] = "GOOD"

    else:

        quality_report["status"] = "CLEANED"

    return cleaned_df, quality_report