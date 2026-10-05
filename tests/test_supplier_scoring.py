import pandas as pd

from analytics.supplier_scoring import (
    normalize_positive,
    normalize_negative,
    calculate_supplier_scores,
    classify_supplier,
    rank_suppliers,
    supplier_summary,
)


def test_normalize_positive():

    series = pd.Series([10, 20, 30])

    result = normalize_positive(series)

    assert result.iloc[0] == 0
    assert result.iloc[-1] == 1


def test_normalize_negative():

    series = pd.Series([10, 20, 30])

    result = normalize_negative(series)

    assert result.iloc[0] == 1
    assert result.iloc[-1] == 0


def test_supplier_score():

    supplier_df = pd.DataFrame({
        "supplier_id": [
            "S001",
            "S002",
            "S003",
        ],
        "supplier_name": [
            "Supplier A",
            "Supplier B",
            "Supplier C",
        ],
        "product_id": [
            "P001",
            "P001",
            "P001",
        ],
        "unit_cost": [
            100,
            120,
            150,
        ],
        "delivery_time_days": [
            3,
            5,
            8,
        ],
        "quality_rating": [
            4.8,
            4.0,
            3.0,
        ],
        "on_time_delivery_rate": [
            98,
            90,
            75,
        ],
    })

    result = calculate_supplier_scores(
        supplier_df
    )

    assert "supplier_score" in result.columns

    assert result["supplier_score"].between(
        0, 100
    ).all()


def test_supplier_classification():

    assert classify_supplier(90) == "EXCELLENT"
    assert classify_supplier(70) == "GOOD"
    assert classify_supplier(50) == "AVERAGE"
    assert classify_supplier(20) == "POOR"


def test_rank_suppliers():

    supplier_df = pd.DataFrame({
        "supplier_id": [
            "S001",
            "S002",
        ],
        "supplier_name": [
            "Supplier A",
            "Supplier B",
        ],
        "product_id": [
            "P001",
            "P001",
        ],
        "unit_cost": [
            100,
            150,
        ],
        "delivery_time_days": [
            3,
            8,
        ],
        "quality_rating": [
            4.8,
            3.0,
        ],
        "on_time_delivery_rate": [
            98,
            75,
        ],
    })

    result = rank_suppliers(
        supplier_df
    )

    assert "rank" in result.columns
    assert result.iloc[0]["rank"] == 1
    assert result.iloc[0]["supplier_id"] == "S001"


def test_supplier_summary():

    supplier_df = pd.DataFrame({
        "supplier_id": [
            "S001",
            "S001",
        ],
        "supplier_name": [
            "Supplier A",
            "Supplier A",
        ],
        "product_id": [
            "P001",
            "P002",
        ],
        "unit_cost": [
            100,
            120,
        ],
        "delivery_time_days": [
            3,
            4,
        ],
        "quality_rating": [
            4.8,
            4.5,
        ],
        "on_time_delivery_rate": [
            98,
            95,
        ],
    })

    result = supplier_summary(
        supplier_df
    )

    assert len(result) == 1
    assert "average_score" in result.columns
    assert "supplier_rating" in result.columns