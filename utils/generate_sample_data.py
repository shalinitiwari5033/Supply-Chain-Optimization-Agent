from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

RANDOM_SEED = 42

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = BASE_DIR / "data" / "sample"
TEMPLATE_DIR = BASE_DIR / "data" / "templates"

SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(RANDOM_SEED)


# ---------------------------------------------------------
# Product master data
# ---------------------------------------------------------

PRODUCTS = [
    ("P001", "Laptop"),
    ("P002", "Mouse"),
    ("P003", "Keyboard"),
    ("P004", "Monitor"),
    ("P005", "Headphones"),
    ("P006", "Webcam"),
    ("P007", "Printer"),
    ("P008", "Router"),
]


# ---------------------------------------------------------
# 1. Generate Sales Data
# ---------------------------------------------------------

def generate_sales_data():
    dates = pd.date_range(
        start="2025-01-01",
        end="2026-06-30",
        freq="D"
    )

    rows = []

    base_demand = {
        "P001": 12,
        "P002": 35,
        "P003": 24,
        "P004": 10,
        "P005": 28,
        "P006": 15,
        "P007": 8,
        "P008": 18,
    }

    prices = {
        "P001": 55000,
        "P002": 800,
        "P003": 1500,
        "P004": 14000,
        "P005": 2500,
        "P006": 3500,
        "P007": 12000,
        "P008": 4500,
    }

    locations = [
        "Bhopal",
        "Indore",
        "Delhi",
        "Mumbai",
        "Pune",
        "Bengaluru",
    ]

    for date in dates:

        # Mild weekly seasonality
        weekday_factor = 1.10 if date.dayofweek < 5 else 0.85

        # Slight yearly trend
        day_number = (date - dates[0]).days
        trend_factor = 1 + (day_number / len(dates)) * 0.20

        for product_id, product_name in PRODUCTS:

            base = base_demand[product_id]

            random_factor = rng.normal(1.0, 0.15)

            quantity = (
                base
                * weekday_factor
                * trend_factor
                * random_factor
            )

            quantity = max(1, int(round(quantity)))

            rows.append(
                {
                    "date": date,
                    "product_id": product_id,
                    "product_name": product_name,
                    "quantity_sold": quantity,
                    "unit_price": prices[product_id],
                    "customer_location": rng.choice(locations),
                }
            )

    df = pd.DataFrame(rows)

    return df


# ---------------------------------------------------------
# 2. Generate Inventory Data
# ---------------------------------------------------------

def generate_inventory_data():
    inventory_rows = []

    lead_times = {
        "P001": 7,
        "P002": 5,
        "P003": 6,
        "P004": 10,
        "P005": 5,
        "P006": 8,
        "P007": 12,
        "P008": 7,
    }

    warehouses = ["WH01", "WH02", "WH03"]

    for product_id, product_name in PRODUCTS:

        lead_time = lead_times[product_id]

        current_stock = int(
            rng.integers(20, 250)
        )

        reorder_level = int(
            rng.integers(20, 100)
        )

        holding_cost = round(
            float(rng.uniform(10, 150)),
            2
        )

        ordering_cost = round(
            float(rng.uniform(100, 1000)),
            2
        )

        inventory_rows.append(
            {
                "product_id": product_id,
                "product_name": product_name,
                "current_stock": current_stock,
                "lead_time_days": lead_time,
                "reorder_level": reorder_level,
                "holding_cost": holding_cost,
                "ordering_cost": ordering_cost,
                "warehouse_id": rng.choice(warehouses),
            }
        )

    return pd.DataFrame(inventory_rows)


# ---------------------------------------------------------
# 3. Generate Supplier Data
# ---------------------------------------------------------

def generate_supplier_data():
    suppliers = [
        ("S001", "Supplier A"),
        ("S002", "Supplier B"),
        ("S003", "Supplier C"),
        ("S004", "Supplier D"),
    ]

    supplier_rows = []

    base_costs = {
        "P001": 50000,
        "P002": 600,
        "P003": 1100,
        "P004": 11500,
        "P005": 1900,
        "P006": 2700,
        "P007": 9500,
        "P008": 3500,
    }

    for supplier_id, supplier_name in suppliers:

        for product_id, _ in PRODUCTS:

            base_cost = base_costs[product_id]

            unit_cost = base_cost * rng.uniform(
                0.90,
                1.12
            )

            delivery_time = int(
                rng.integers(3, 13)
            )

            quality_rating = round(
                float(rng.uniform(3.5, 5.0)),
                2
            )

            on_time_delivery_rate = round(
                float(rng.uniform(80, 99)),
                2
            )

            supplier_rows.append(
                {
                    "supplier_id": supplier_id,
                    "supplier_name": supplier_name,
                    "product_id": product_id,
                    "unit_cost": round(unit_cost, 2),
                    "delivery_time_days": delivery_time,
                    "quality_rating": quality_rating,
                    "on_time_delivery_rate": on_time_delivery_rate,
                }
            )

    return pd.DataFrame(supplier_rows)


# ---------------------------------------------------------
# 4. Create CSV Templates
# ---------------------------------------------------------

def create_templates():

    sales_template = pd.DataFrame(
        columns=[
            "date",
            "product_id",
            "product_name",
            "quantity_sold",
            "unit_price",
            "customer_location",
        ]
    )

    inventory_template = pd.DataFrame(
        columns=[
            "product_id",
            "product_name",
            "current_stock",
            "lead_time_days",
            "reorder_level",
            "holding_cost",
            "ordering_cost",
            "warehouse_id",
        ]
    )

    supplier_template = pd.DataFrame(
        columns=[
            "supplier_id",
            "supplier_name",
            "product_id",
            "unit_cost",
            "delivery_time_days",
            "quality_rating",
            "on_time_delivery_rate",
        ]
    )

    sales_template.to_csv(
        TEMPLATE_DIR / "sales_template.csv",
        index=False
    )

    inventory_template.to_csv(
        TEMPLATE_DIR / "inventory_template.csv",
        index=False
    )

    supplier_template.to_csv(
        TEMPLATE_DIR / "supplier_template.csv",
        index=False
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("Generating sample datasets...")

    sales_df = generate_sales_data()
    inventory_df = generate_inventory_data()
    supplier_df = generate_supplier_data()

    sales_path = SAMPLE_DIR / "sales_data.csv"
    inventory_path = SAMPLE_DIR / "inventory_data.csv"
    supplier_path = SAMPLE_DIR / "supplier_data.csv"

    sales_df.to_csv(
        sales_path,
        index=False
    )

    inventory_df.to_csv(
        inventory_path,
        index=False
    )

    supplier_df.to_csv(
        supplier_path,
        index=False
    )

    create_templates()

    print("\nSample datasets created successfully.")

    print(f"\nSales rows: {len(sales_df)}")
    print(f"Inventory rows: {len(inventory_df)}")
    print(f"Supplier rows: {len(supplier_df)}")

    print("\nFiles created:")

    print(f"  {sales_path}")
    print(f"  {inventory_path}")
    print(f"  {supplier_path}")

    print("\nTemplates created:")
    print(f"  {TEMPLATE_DIR / 'sales_template.csv'}")
    print(f"  {TEMPLATE_DIR / 'inventory_template.csv'}")
    print(f"  {TEMPLATE_DIR / 'supplier_template.csv'}")


if __name__ == "__main__":
    main()