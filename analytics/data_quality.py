import pandas as pd


def create_quality_summary(report):
    """
    Convert the technical quality report into
    a simple summary dictionary.
    """

    missing_total = int(
        report["missing_values"]["missing_count"].sum()
    )

    invalid_total = sum(
        report["invalid_values"].values()
    )

    summary = {
        "Dataset": report["dataset_type"].title(),

        "Status": report["status"],

        "Original Rows": report["original_rows"],

        "Cleaned Rows": report["cleaned_rows"],

        "Rows Removed": report["rows_removed"],

        "Columns": report["original_columns"],

        "Missing Values": missing_total,

        "Duplicate Rows": report["duplicate_rows"],

        "Invalid Values": invalid_total,
    }

    return summary


def missing_values_table(report):
    """
    Return missing-value information
    in a clean DataFrame format.
    """

    missing_df = report["missing_values"].copy()

    missing_df = missing_df[
        missing_df["missing_count"] > 0
    ]

    return missing_df.reset_index().rename(
        columns={
            "index": "column"
        }
    )