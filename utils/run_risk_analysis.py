import pandas as pd

from analytics.supplier_scoring import (
    rank_suppliers,
)

from analytics.risk_analysis import (
    analyze_risk,
)


def main():

    sales_path = "data/sample/sales_data.csv"
    inventory_path = "data/sample/inventory_data.csv"
    supplier_path = "data/sample/supplier_data.csv"

    sales_df = pd.read_csv(
        sales_path
    )

    inventory_df = pd.read_csv(
        inventory_path
    )

    supplier_df = pd.read_csv(
        supplier_path
    )

    # First calculate supplier scores.
    supplier_scored = rank_suppliers(
        supplier_df
    )

    # Then calculate supply-chain risk.
    risk_result = analyze_risk(
        inventory_df=inventory_df,
        supplier_df=supplier_scored,
        demand_df=sales_df,
    )

    columns = [
        "product_id",
        "product_name",
        "current_stock",
        "average_daily_demand",
        "stock_risk",
        "demand_risk",
        "supplier_risk",
        "lead_time_risk",
        "overall_risk_score",
        "risk_level",
        "risk_factors",
    ]

    print("\nSUPPLY CHAIN RISK ANALYSIS")
    print("=" * 100)

    print(
        risk_result[columns]
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()