import pandas as pd
import numpy as np


# Supplier scoring weights
WEIGHTS = {
    "cost": 0.25,
    "delivery_time": 0.20,
    "quality": 0.25,
    "on_time_delivery": 0.30,
}


def normalize_positive(series):
    """
    Normalize a metric where higher values are better.

    Result is between 0 and 1.
    """

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(1.0, index=series.index)

    return (series - minimum) / (maximum - minimum)


def normalize_negative(series):
    """
    Normalize a metric where lower values are better.

    Result is between 0 and 1.
    """

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(1.0, index=series.index)

    return (maximum - series) / (maximum - minimum)


def calculate_supplier_scores(supplier_df):
    """
    Calculate a weighted supplier performance score.

    Higher score = better supplier.
    """

    df = supplier_df.copy()

    # Cost: lower is better
    df["cost_score"] = normalize_negative(
        df["unit_cost"]
    )

    # Delivery time: lower is better
    df["delivery_time_score"] = normalize_negative(
        df["delivery_time_days"]
    )

    # Quality: higher is better
    df["quality_score"] = normalize_positive(
        df["quality_rating"]
    )

    # On-time delivery: higher is better
    df["on_time_delivery_score"] = normalize_positive(
        df["on_time_delivery_rate"]
    )

    # Weighted score
    df["supplier_score"] = (
        df["cost_score"] * WEIGHTS["cost"]
        + df["delivery_time_score"] * WEIGHTS["delivery_time"]
        + df["quality_score"] * WEIGHTS["quality"]
        + df["on_time_delivery_score"]
        * WEIGHTS["on_time_delivery"]
    )

    # Convert to 0–100
    df["supplier_score"] = (
        df["supplier_score"] * 100
    )

    return df


def classify_supplier(score):
    """
    Convert numerical supplier score into
    an easy-to-understand category.
    """

    if score >= 80:
        return "EXCELLENT"

    if score >= 60:
        return "GOOD"

    if score >= 40:
        return "AVERAGE"

    return "POOR"


def rank_suppliers(supplier_df):
    """
    Calculate scores, classifications and rankings.
    """

    df = calculate_supplier_scores(
        supplier_df
    )

    df["supplier_rating"] = (
        df["supplier_score"]
        .apply(classify_supplier)
    )

    df = df.sort_values(
        "supplier_score",
        ascending=False
    ).reset_index(drop=True)

    df["rank"] = (
        df.groupby("product_id")["supplier_score"]
        .rank(
            method="dense",
            ascending=False
        )
        .astype(int)
    )

    return df


def supplier_summary(supplier_df):
    """
    Generate a supplier-level summary.
    """

    scored = calculate_supplier_scores(
        supplier_df
    )

    summary = (
        scored
        .groupby(
            ["supplier_id", "supplier_name"],
            as_index=False
        )
        .agg(
            average_score=(
                "supplier_score",
                "mean"
            ),
            average_unit_cost=(
                "unit_cost",
                "mean"
            ),
            average_delivery_time=(
                "delivery_time_days",
                "mean"
            ),
            average_quality=(
                "quality_rating",
                "mean"
            ),
            average_on_time_delivery=(
                "on_time_delivery_rate",
                "mean"
            ),
        )
    )

    summary["supplier_rating"] = (
        summary["average_score"]
        .apply(classify_supplier)
    )

    return summary