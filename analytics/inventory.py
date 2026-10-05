import numpy as np
import pandas as pd


def calculate_average_daily_demand(sales_df):
    """
    Calculate average daily demand for each product.
    """

    sales = sales_df.copy()

    sales["date"] = pd.to_datetime(sales["date"])

    daily_demand = (
        sales.groupby(["product_id", "date"])["quantity_sold"]
        .sum()
        .reset_index()
    )

    average_demand = (
        daily_demand
        .groupby("product_id")["quantity_sold"]
        .mean()
        .reset_index()
        .rename(columns={"quantity_sold": "average_daily_demand"})
    )

    return average_demand


def calculate_demand_std(sales_df):
    """
    Calculate standard deviation of daily demand.
    """

    sales = sales_df.copy()

    sales["date"] = pd.to_datetime(sales["date"])

    daily_demand = (
        sales.groupby(["product_id", "date"])["quantity_sold"]
        .sum()
        .reset_index()
    )

    demand_std = (
        daily_demand
        .groupby("product_id")["quantity_sold"]
        .std()
        .fillna(0)
        .reset_index()
        .rename(columns={"quantity_sold": "demand_std"})
    )

    return demand_std


def calculate_safety_stock(
    average_daily_demand,
    demand_std,
    lead_time_days,
    service_level_z=1.65
):
    """
    Calculate safety stock.

    Formula:
        Safety Stock = Z × Demand Std × sqrt(Lead Time)
    """

    safety_stock = (
        service_level_z
        * demand_std
        * np.sqrt(lead_time_days)
    )

    return max(float(safety_stock), 0.0)


def calculate_reorder_point(
    average_daily_demand,
    lead_time_days,
    safety_stock
):
    """
    Calculate reorder point.

    Formula:
        Reorder Point = Average Daily Demand × Lead Time
                        + Safety Stock
    """

    reorder_point = (
        average_daily_demand * lead_time_days
        + safety_stock
    )

    return max(float(reorder_point), 0.0)


def calculate_eoq(
    annual_demand,
    ordering_cost,
    holding_cost
):
    """
    Calculate Economic Order Quantity.

    Formula:
        EOQ = sqrt((2 × Annual Demand × Ordering Cost)
                   / Holding Cost)
    """

    if holding_cost <= 0:
        return 0.0

    eoq = np.sqrt(
        (2 * annual_demand * ordering_cost)
        / holding_cost
    )

    return max(float(eoq), 0.0)


def detect_stockout_risk(
    current_stock,
    reorder_point
):
    """
    Determine whether current stock has reached
    the reorder threshold.
    """

    if current_stock <= 0:
        return "STOCKOUT"

    if current_stock <= reorder_point:
        return "REORDER_REQUIRED"

    return "HEALTHY"


def optimize_inventory(sales_df, inventory_df):
    """
    Generate inventory optimization metrics
    for all products.
    """

    average_demand = calculate_average_daily_demand(sales_df)
    demand_std = calculate_demand_std(sales_df)

    result = inventory_df.copy()

    result = result.merge(
        average_demand,
        on="product_id",
        how="left"
    )

    result = result.merge(
        demand_std,
        on="product_id",
        how="left"
    )

    result["average_daily_demand"] = (
        result["average_daily_demand"].fillna(0)
    )

    result["demand_std"] = (
        result["demand_std"].fillna(0)
    )

    result["safety_stock"] = result.apply(
        lambda row: calculate_safety_stock(
            row["average_daily_demand"],
            row["demand_std"],
            row["lead_time_days"]
        ),
        axis=1
    )

    result["calculated_reorder_point"] = result.apply(
        lambda row: calculate_reorder_point(
            row["average_daily_demand"],
            row["lead_time_days"],
            row["safety_stock"]
        ),
        axis=1
    )

    result["annual_demand"] = (
        result["average_daily_demand"] * 365
    )

    result["eoq"] = result.apply(
        lambda row: calculate_eoq(
            row["annual_demand"],
            row["ordering_cost"],
            row["holding_cost"]
        ),
        axis=1
    )

    result["inventory_status"] = result.apply(
        lambda row: detect_stockout_risk(
            row["current_stock"],
            row["calculated_reorder_point"]
        ),
        axis=1
    )

    result["recommended_order_quantity"] = np.where(
        result["inventory_status"].isin(
            ["STOCKOUT", "REORDER_REQUIRED"]
        ),
        np.ceil(result["eoq"]),
        0
    )

    return result