import pandas as pd

from analytics.inventory import optimize_inventory


def main():

    sales_path = "data/sample/sales_data.csv"
    inventory_path = "data/sample/inventory_data.csv"

    sales_df = pd.read_csv(sales_path)
    inventory_df = pd.read_csv(inventory_path)

    result = optimize_inventory(
        sales_df,
        inventory_df
    )

    columns = [
        "product_id",
        "product_name",
        "current_stock",
        "average_daily_demand",
        "lead_time_days",
        "safety_stock",
        "calculated_reorder_point",
        "eoq",
        "inventory_status",
        "recommended_order_quantity",
    ]

    print("\nINVENTORY OPTIMIZATION")
    print("=" * 80)

    print(
        result[columns].round(2).to_string(index=False)
    )


if __name__ == "__main__":
    main()