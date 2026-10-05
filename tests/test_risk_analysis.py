import pandas as pd

from analytics.risk_analysis import (
    calculate_stock_risk,
    calculate_demand_risk,
    calculate_supplier_risk,
    calculate_lead_time_risk,
    classify_risk,
    calculate_overall_risk,
    analyze_risk,
)


def test_stock_risk():

    assert calculate_stock_risk(0, 100) == 100

    assert calculate_stock_risk(40, 100) == 90

    assert calculate_stock_risk(60, 100) == 70

    assert calculate_stock_risk(90, 100) == 50

    assert calculate_stock_risk(150, 100) == 10


def test_demand_risk():

    assert calculate_demand_risk(
        demand_std=60,
        average_daily_demand=100
    ) == 90

    assert calculate_demand_risk(
        demand_std=40,
        average_daily_demand=100
    ) == 70

    assert calculate_demand_risk(
        demand_std=20,
        average_daily_demand=100
    ) == 50

    assert calculate_demand_risk(
        demand_std=5,
        average_daily_demand=100
    ) == 10


def test_supplier_risk():

    assert calculate_supplier_risk(30) == 90

    assert calculate_supplier_risk(50) == 70

    assert calculate_supplier_risk(70) == 40

    assert calculate_supplier_risk(90) == 10


def test_lead_time_risk():

    assert calculate_lead_time_risk(15) == 90

    assert calculate_lead_time_risk(12) == 70

    assert calculate_lead_time_risk(7) == 40

    assert calculate_lead_time_risk(3) == 10


def test_risk_classification():

    assert classify_risk(90) == "CRITICAL"

    assert classify_risk(60) == "HIGH"

    assert classify_risk(30) == "MEDIUM"

    assert classify_risk(10) == "LOW"


def test_overall_risk():

    row = pd.Series({
        "stock_risk": 80,
        "demand_risk": 60,
        "supplier_risk": 40,
        "lead_time_risk": 20,
    })

    result = calculate_overall_risk(row)

    assert result > 0
    assert result <= 100


def test_analyze_risk():

    inventory_df = pd.DataFrame({
        "product_id": ["P001"],
        "product_name": ["Laptop"],
        "current_stock": [20],
        "lead_time_days": [10],
        "reorder_level": [50],
        "holding_cost": [10],
        "ordering_cost": [100],
        "warehouse_id": ["WH001"],
    })

    supplier_df = pd.DataFrame({
        "supplier_id": ["S001"],
        "supplier_name": ["Supplier A"],
        "product_id": ["P001"],
        "unit_cost": [100],
        "delivery_time_days": [5],
        "quality_rating": [4.5],
        "on_time_delivery_rate": [95],
        "supplier_score": [85],
    })

    demand_df = pd.DataFrame({
        "product_id": [
            "P001",
            "P001",
            "P001",
            "P001",
        ],
        "quantity_sold": [
            10,
            20,
            15,
            25,
        ],
    })

    result = analyze_risk(
        inventory_df,
        supplier_df,
        demand_df
    )

    assert len(result) == 1

    assert "stock_risk" in result.columns
    assert "demand_risk" in result.columns
    assert "supplier_risk" in result.columns
    assert "lead_time_risk" in result.columns
    assert "overall_risk_score" in result.columns
    assert "risk_level" in result.columns
    assert "risk_factors" in result.columns

    assert 0 <= result.iloc[0]["overall_risk_score"] <= 100