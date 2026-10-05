import pandas as pd

from analytics.inventory import (
    calculate_average_daily_demand,
    calculate_demand_std,
    calculate_safety_stock,
    calculate_reorder_point,
    calculate_eoq,
    detect_stockout_risk,
    optimize_inventory,
)


def test_average_daily_demand():

    sales = pd.DataFrame({
        "date": [
            "2025-01-01",
            "2025-01-01",
            "2025-01-02",
            "2025-01-02",
        ],
        "product_id": [
            "P001",
            "P001",
            "P001",
            "P001",
        ],
        "quantity_sold": [
            10,
            20,
            20,
            10,
        ],
    })

    result = calculate_average_daily_demand(sales)

    assert len(result) == 1
    assert result.iloc[0]["average_daily_demand"] == 30


def test_safety_stock():

    result = calculate_safety_stock(
        average_daily_demand=10,
        demand_std=2,
        lead_time_days=5,
    )

    assert result > 0


def test_reorder_point():

    result = calculate_reorder_point(
        average_daily_demand=10,
        lead_time_days=5,
        safety_stock=15,
    )

    assert result == 65


def test_eoq():

    result = calculate_eoq(
        annual_demand=3650,
        ordering_cost=100,
        holding_cost=10,
    )

    assert result > 0


def test_stockout_status():

    assert detect_stockout_risk(0, 50) == "STOCKOUT"

    assert detect_stockout_risk(40, 50) == "REORDER_REQUIRED"

    assert detect_stockout_risk(100, 50) == "HEALTHY"


def test_inventory_optimization():

    sales = pd.DataFrame({
        "date": [
            "2025-01-01",
            "2025-01-02",
            "2025-01-03",
            "2025-01-04",
        ],
        "product_id": [
            "P001",
            "P001",
            "P001",
            "P001",
        ],
        "quantity_sold": [
            10,
            12,
            11,
            13,
        ],
    })

    inventory = pd.DataFrame({
        "product_id": ["P001"],
        "product_name": ["Laptop"],
        "current_stock": [20],
        "lead_time_days": [5],
        "reorder_level": [50],
        "holding_cost": [10],
        "ordering_cost": [100],
        "warehouse_id": ["WH001"],
    })

    result = optimize_inventory(
        sales,
        inventory
    )

    assert len(result) == 1
    assert "safety_stock" in result.columns
    assert "calculated_reorder_point" in result.columns
    assert "eoq" in result.columns
    assert "inventory_status" in result.columns