import pandas as pd
import numpy as np


def calculate_stock_risk(current_stock, reorder_point):
    """
    Calculate inventory/stock risk.

    Returns a score from 0 to 100.
    Higher score = higher risk.
    """

    if reorder_point <= 0:
        return 0.0

    stock_ratio = current_stock / reorder_point

    if current_stock <= 0:
        return 100.0

    if stock_ratio <= 0.50:
        return 90.0

    if stock_ratio <= 0.75:
        return 70.0

    if stock_ratio <= 1.00:
        return 50.0

    return 10.0


def calculate_demand_risk(demand_std, average_daily_demand):
    """
    Estimate demand volatility risk.

    Higher coefficient of variation = higher risk.
    """

    if average_daily_demand <= 0:
        return 0.0

    coefficient_of_variation = (
        demand_std / average_daily_demand
    )

    if coefficient_of_variation >= 0.50:
        return 90.0

    if coefficient_of_variation >= 0.30:
        return 70.0

    if coefficient_of_variation >= 0.15:
        return 50.0

    return 10.0


def calculate_supplier_risk(supplier_score):
    """
    Convert supplier performance score into
    supplier risk.
    """

    if supplier_score < 40:
        return 90.0

    if supplier_score < 60:
        return 70.0

    if supplier_score < 80:
        return 40.0

    return 10.0


def calculate_lead_time_risk(lead_time_days):
    """
    Estimate risk associated with supplier lead time.
    """

    if lead_time_days >= 14:
        return 90.0

    if lead_time_days >= 10:
        return 70.0

    if lead_time_days >= 5:
        return 40.0

    return 10.0


def classify_risk(risk_score):
    """
    Convert risk score into a category.
    """

    if risk_score >= 75:
        return "CRITICAL"

    if risk_score >= 50:
        return "HIGH"

    if risk_score >= 25:
        return "MEDIUM"

    return "LOW"


def generate_risk_factors(row):
    """
    Generate human-readable explanations
    for the calculated risk.
    """

    factors = []

    if row["stock_risk"] >= 70:
        factors.append(
            "Inventory level is significantly below the reorder threshold."
        )

    if row["demand_risk"] >= 70:
        factors.append(
            "Demand shows high variability."
        )

    if row["supplier_risk"] >= 70:
        factors.append(
            "Supplier performance is weak."
        )

    if row["lead_time_risk"] >= 70:
        factors.append(
            "Supplier lead time is high."
        )

    if not factors:
        factors.append(
            "No major supply-chain risk detected."
        )

    return factors


def calculate_overall_risk(row):
    """
    Calculate weighted overall supply-chain risk.

    Inventory receives the highest weight because
    stock availability directly affects fulfillment.
    """

    risk_score = (
        row["stock_risk"] * 0.35
        + row["demand_risk"] * 0.25
        + row["supplier_risk"] * 0.25
        + row["lead_time_risk"] * 0.15
    )

    return float(risk_score)


def analyze_risk(
    inventory_df,
    supplier_df,
    demand_df
):
    inventory = inventory_df.copy()
    suppliers = supplier_df.copy()
    demand = demand_df.copy()

    # The inventory dataframe may already contain
    # demand metrics calculated by the inventory module.
    # Remove them before merging fresh demand metrics
    # to avoid duplicate Pandas columns such as _x and _y.
    inventory = inventory.drop(
        columns=[
            "average_daily_demand",
            "demand_std",
        ],
        errors="ignore",
    )

    # ------------------------------------------------
    # Demand metrics
    # ------------------------------------------------

    demand_summary = (
        demand
        .groupby("product_id")
        .agg(
            average_daily_demand=(
                "quantity_sold",
                "mean"
            ),
            demand_std=(
                "quantity_sold",
                "std"
            )
        )
        .reset_index()
    )

    demand_summary["demand_std"] = (
        demand_summary["demand_std"]
        .fillna(0)
    )

    # ------------------------------------------------
    # Supplier metrics
    # ------------------------------------------------

    supplier_summary = (
        suppliers
        .groupby("product_id")
        .agg(
            average_supplier_score=(
                "supplier_score",
                "mean"
            )
        )
        .reset_index()
    )

    # ------------------------------------------------
    # Combine datasets
    # ------------------------------------------------

    result = inventory.merge(
        demand_summary,
        on="product_id",
        how="left"
    )

    result = result.merge(
        supplier_summary,
        on="product_id",
        how="left"
    )

    result["average_daily_demand"] = (
        result["average_daily_demand"]
        .fillna(0)
    )

    result["demand_std"] = (
        result["demand_std"]
        .fillna(0)
    )

    result["average_supplier_score"] = (
        result["average_supplier_score"]
        .fillna(0)
    )

    # ------------------------------------------------
    # Calculate individual risks
    # ------------------------------------------------

    reorder_column = (
        "calculated_reorder_point"
        if "calculated_reorder_point" in result.columns
        else "reorder_level"
    )

    result["stock_risk"] = result.apply(
        lambda row: calculate_stock_risk(
            row["current_stock"],
            row[reorder_column]
        ),
        axis=1
    )

    result["demand_risk"] = result.apply(
        lambda row: calculate_demand_risk(
            row["demand_std"],
            row["average_daily_demand"]
        ),
        axis=1
    )

    result["supplier_risk"] = (
        result["average_supplier_score"]
        .apply(calculate_supplier_risk)
    )

    result["lead_time_risk"] = (
        result["lead_time_days"]
        .apply(calculate_lead_time_risk)
    )

    # ------------------------------------------------
    # Overall risk
    # ------------------------------------------------

    result["overall_risk_score"] = (
        result.apply(
            calculate_overall_risk,
            axis=1
        )
    )

    result["risk_level"] = (
        result["overall_risk_score"]
        .apply(classify_risk)
    )

    # ------------------------------------------------
    # Risk explanation
    # ------------------------------------------------

    result["risk_factors"] = (
        result.apply(
            generate_risk_factors,
            axis=1
        )
    )

    return result