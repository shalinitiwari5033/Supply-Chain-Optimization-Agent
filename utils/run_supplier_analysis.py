import pandas as pd

from analytics.supplier_scoring import (
    rank_suppliers,
    supplier_summary,
)


def main():

    supplier_path = (
        "data/sample/supplier_data.csv"
    )

    supplier_df = pd.read_csv(
        supplier_path
    )

    ranked = rank_suppliers(
        supplier_df
    )

    print("\nSUPPLIER ANALYSIS")
    print("=" * 80)

    columns = [
        "supplier_id",
        "supplier_name",
        "product_id",
        "unit_cost",
        "delivery_time_days",
        "quality_rating",
        "on_time_delivery_rate",
        "supplier_score",
        "supplier_rating",
        "rank",
    ]

    print(
        ranked[columns]
        .round(2)
        .to_string(index=False)
    )

    print("\nSUPPLIER SUMMARY")
    print("=" * 80)

    summary = supplier_summary(
        supplier_df
    )

    print(
        summary.round(2)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()