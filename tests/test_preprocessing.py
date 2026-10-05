import pandas as pd

from utils.validators import (
    validate_columns,
    clean_data,
)


def test_sales_columns():

    df = pd.DataFrame(
        columns=[
            "date",
            "product_id",
            "product_name",
            "quantity_sold",
            "unit_price",
            "customer_location",
        ]
    )

    result = validate_columns(
        df,
        "sales"
    )

    assert result["valid"] is True


def test_negative_sales_removed():

    df = pd.DataFrame(
        {
            "date": [
                "2026-01-01",
                "2026-01-02",
            ],
            "product_id": [
                "P001",
                "P002",
            ],
            "product_name": [
                "Laptop",
                "Mouse",
            ],
            "quantity_sold": [
                10,
                -5,
            ],
            "unit_price": [
                50000,
                800,
            ],
            "customer_location": [
                "Bhopal",
                "Delhi",
            ],
        }
    )

    cleaned = clean_data(
        df,
        "sales"
    )

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["quantity_sold"] == 10


def test_duplicate_rows_removed():

    df = pd.DataFrame(
        {
            "date": [
                "2026-01-01",
                "2026-01-01",
            ],
            "product_id": [
                "P001",
                "P001",
            ],
            "product_name": [
                "Laptop",
                "Laptop",
            ],
            "quantity_sold": [
                10,
                10,
            ],
            "unit_price": [
                50000,
                50000,
            ],
            "customer_location": [
                "Bhopal",
                "Bhopal",
            ],
        }
    )

    cleaned = clean_data(
        df,
        "sales"
    )

    assert len(cleaned) == 1

from analytics.preprocessing import preprocess_dataset
from analytics.data_quality import (
    create_quality_summary,
    missing_values_table,
)


def test_preprocess_sales_dataset():

    df = pd.DataFrame(
        {
            "date": [
                "2026-01-01",
                "2026-01-02",
                "2026-01-02",
            ],
            "product_id": [
                "P001",
                "P002",
                "P002",
            ],
            "product_name": [
                "Laptop",
                "Mouse",
                "Mouse",
            ],
            "quantity_sold": [
                10,
                20,
                20,
            ],
            "unit_price": [
                50000,
                800,
                800,
            ],
            "customer_location": [
                "Bhopal",
                "Delhi",
                "Delhi",
            ],
        }
    )

    cleaned_df, report = preprocess_dataset(
        df,
        "sales",
    )

    assert len(cleaned_df) == 2

    assert report["original_rows"] == 3

    assert report["cleaned_rows"] == 2

    assert report["rows_removed"] == 1


def test_quality_summary():

    df = pd.DataFrame(
        {
            "date": ["2026-01-01"],
            "product_id": ["P001"],
            "product_name": ["Laptop"],
            "quantity_sold": [10],
            "unit_price": [50000],
            "customer_location": ["Bhopal"],
        }
    )

    cleaned_df, report = preprocess_dataset(
        df,
        "sales",
    )

    summary = create_quality_summary(
        report
    )

    assert summary["Dataset"] == "Sales"

    assert summary["Original Rows"] == 1

    assert summary["Cleaned Rows"] == 1