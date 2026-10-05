import pandas as pd
import numpy as np


# =========================================================
# Sales Analysis
# =========================================================

def sales_summary(sales_df):
    """
    Generate basic sales KPIs.
    """

    total_units = sales_df["quantity_sold"].sum()

    total_revenue = (
        sales_df["quantity_sold"]
        * sales_df["unit_price"]
    ).sum()

    average_daily_demand = (
        sales_df.groupby("date")["quantity_sold"]
        .sum()
        .mean()
    )

    unique_products = (
        sales_df["product_id"]
        .nunique()
    )

    date_min = sales_df["date"].min()
    date_max = sales_df["date"].max()

    return {
        "total_units_sold": int(total_units),
        "total_revenue": float(total_revenue),
        "average_daily_demand": float(
            average_daily_demand
        ),
        "unique_products": int(unique_products),
        "start_date": date_min,
        "end_date": date_max,
    }


# =========================================================
# Product Demand Analysis
# =========================================================

def product_demand_summary(sales_df):
    """
    Calculate demand statistics for every product.
    """

    summary = (
        sales_df
        .groupby(
            [
                "product_id",
                "product_name",
            ]
        )
        ["quantity_sold"]
        .agg(
            total_demand="sum",
            average_demand="mean",
            demand_std="std",
            minimum_demand="min",
            maximum_demand="max",
        )
        .reset_index()
    )

    summary["coefficient_of_variation"] = (
        summary["demand_std"]
        / summary["average_demand"]
    )

    return summary.sort_values(
        "total_demand",
        ascending=False,
    ).reset_index(drop=True)


# =========================================================
# Daily Demand
# =========================================================

def daily_demand(sales_df):
    """
    Aggregate total demand by date.
    """

    result = (
        sales_df
        .groupby("date")["quantity_sold"]
        .sum()
        .reset_index()
    )

    result = result.rename(
        columns={
            "quantity_sold": "total_demand"
        }
    )

    return result.sort_values("date")


# =========================================================
# Weekly Demand
# =========================================================

def weekly_demand(sales_df):
    """
    Aggregate demand by week.
    """

    df = sales_df.copy()

    df["week"] = (
        df["date"]
        .dt.to_period("W")
        .apply(lambda x: x.start_time)
    )

    result = (
        df
        .groupby("week")["quantity_sold"]
        .sum()
        .reset_index()
    )

    result = result.rename(
        columns={
            "quantity_sold": "total_demand"
        }
    )

    return result


# =========================================================
# Monthly Demand
# =========================================================

def monthly_demand(sales_df):
    """
    Aggregate demand by month.
    """

    df = sales_df.copy()

    df["month"] = (
        df["date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    result = (
        df
        .groupby("month")["quantity_sold"]
        .sum()
        .reset_index()
    )

    result = result.rename(
        columns={
            "quantity_sold": "total_demand"
        }
    )

    return result


# =========================================================
# Day-of-Week Analysis
# =========================================================

def weekday_demand(sales_df):
    """
    Calculate average demand by day of week.
    """

    df = sales_df.copy()

    df["weekday"] = (
        df["date"]
        .dt.day_name()
    )

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    result = (
        df
        .groupby("weekday")["quantity_sold"]
        .mean()
        .reindex(weekday_order)
        .reset_index()
    )

    result = result.rename(
        columns={
            "quantity_sold": "average_demand"
        }
    )

    return result


# =========================================================
# Inventory Analysis
# =========================================================

def inventory_summary(inventory_df):
    """
    Generate inventory KPIs.
    """

    total_stock = (
        inventory_df["current_stock"]
        .sum()
    )

    average_stock = (
        inventory_df["current_stock"]
        .mean()
    )

    products_below_reorder = (
        inventory_df["current_stock"]
        < inventory_df["reorder_level"]
    ).sum()

    return {
        "total_current_stock": int(
            total_stock
        ),
        "average_current_stock": float(
            average_stock
        ),
        "products_below_reorder": int(
            products_below_reorder
        ),
        "total_products": int(
            len(inventory_df)
        ),
    }


# =========================================================
# Inventory Risk
# =========================================================

def inventory_risk_table(inventory_df):
    """
    Identify products below their reorder level.
    """

    result = inventory_df.copy()

    result["stock_status"] = np.where(
        result["current_stock"]
        < result["reorder_level"],
        "Below Reorder Level",
        "Normal",
    )

    result["stock_gap"] = (
        result["current_stock"]
        - result["reorder_level"]
    )

    return result.sort_values(
        "stock_gap"
    ).reset_index(drop=True)


# =========================================================
# Supplier Analysis
# =========================================================

def supplier_summary(supplier_df):
    """
    Calculate supplier performance statistics.
    """

    result = (
        supplier_df
        .groupby(
            [
                "supplier_id",
                "supplier_name",
            ]
        )
        .agg(
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
            average_on_time_rate=(
                "on_time_delivery_rate",
                "mean"
            ),
        )
        .reset_index()
    )

    return result.sort_values(
        "average_on_time_rate",
        ascending=False,
    ).reset_index(drop=True)