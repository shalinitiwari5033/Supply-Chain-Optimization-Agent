from pathlib import Path

import pandas as pd

from analytics.forecasting import (
    prepare_daily_demand,
    time_series_split,
    naive_forecast,
    evaluate_forecast,
)


BASE_DIR = Path(__file__).resolve().parent.parent

SALES_PATH = (
    BASE_DIR
    / "data"
    / "sample"
    / "sales_data.csv"
)


def main():

    print("=" * 60)
    print("DEMAND FORECASTING - BASELINE")
    print("=" * 60)

    # Load sales
    sales_df = pd.read_csv(
        SALES_PATH,
        parse_dates=["date"],
    )

    # Use one product first
    product_id = "P001"

    print(
        f"\nProduct: {product_id}"
    )

    # Prepare daily demand
    daily = prepare_daily_demand(
        sales_df,
        product_id,
    )

    print(
        f"Total days: {len(daily)}"
    )

    # Train/test split
    train, test = time_series_split(
        daily,
        test_size=0.20,
    )

    print(
        f"Training days: {len(train)}"
    )

    print(
        f"Testing days: {len(test)}"
    )

    # Baseline
    predictions = naive_forecast(
        train,
        test,
    )

    # Evaluate
    metrics = evaluate_forecast(
        test["quantity_sold"],
        predictions,
    )

    print("\nBASELINE RESULTS")
    print("-" * 60)

    print(
        f"MAE:  {metrics['MAE']:.2f}"
    )

    print(
        f"RMSE: {metrics['RMSE']:.2f}"
    )


if __name__ == "__main__":
    main()