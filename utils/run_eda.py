from pathlib import Path

import pandas as pd

from analytics.eda import (
    sales_summary,
    product_demand_summary,
    daily_demand,
    weekly_demand,
    monthly_demand,
    weekday_demand,
    inventory_summary,
    inventory_risk_table,
    supplier_summary,
)


BASE_DIR = Path(__file__).resolve().parent.parent

SALES_PATH = (
    BASE_DIR
    / "data"
    / "sample"
    / "sales_data.csv"
)

INVENTORY_PATH = (
    BASE_DIR
    / "data"
    / "sample"
    / "inventory_data.csv"
)

SUPPLIER_PATH = (
    BASE_DIR
    / "data"
    / "sample"
    / "supplier_data.csv"
)


def main():

    print("=" * 60)
    print("SUPPLY CHAIN EDA")
    print("=" * 60)

    # -----------------------------------------------------
    # Load data
    # -----------------------------------------------------

    sales_df = pd.read_csv(
        SALES_PATH,
        parse_dates=["date"],
    )

    inventory_df = pd.read_csv(
        INVENTORY_PATH
    )

    supplier_df = pd.read_csv(
        SUPPLIER_PATH
    )

    # -----------------------------------------------------
    # Sales
    # -----------------------------------------------------

    print("\nSALES SUMMARY")
    print("-" * 60)

    summary = sales_summary(
        sales_df
    )

    for key, value in summary.items():

        print(
            f"{key}: {value}"
        )

    # -----------------------------------------------------
    # Product demand
    # -----------------------------------------------------

    print("\nPRODUCT DEMAND")
    print("-" * 60)

    print(
        product_demand_summary(
            sales_df
        ).to_string(index=False)
    )

    # -----------------------------------------------------
    # Monthly demand
    # -----------------------------------------------------

    print("\nMONTHLY DEMAND")
    print("-" * 60)

    print(
        monthly_demand(
            sales_df
        ).tail(12).to_string(index=False)
    )

    # -----------------------------------------------------
    # Weekday demand
    # -----------------------------------------------------

    print("\nWEEKDAY DEMAND")
    print("-" * 60)

    print(
        weekday_demand(
            sales_df
        ).to_string(index=False)
    )

    # -----------------------------------------------------
    # Inventory
    # -----------------------------------------------------

    print("\nINVENTORY SUMMARY")
    print("-" * 60)

    inventory_info = inventory_summary(
        inventory_df
    )

    for key, value in inventory_info.items():

        print(
            f"{key}: {value}"
        )

    print("\nINVENTORY RISK")
    print("-" * 60)

    print(
        inventory_risk_table(
            inventory_df
        )[
            [
                "product_id",
                "product_name",
                "current_stock",
                "reorder_level",
                "stock_status",
            ]
        ].to_string(index=False)
    )

    # -----------------------------------------------------
    # Suppliers
    # -----------------------------------------------------

    print("\nSUPPLIER SUMMARY")
    print("-" * 60)

    print(
        supplier_summary(
            supplier_df
        ).to_string(index=False)
    )

    print("\nEDA completed successfully.")


if __name__ == "__main__":
    main()