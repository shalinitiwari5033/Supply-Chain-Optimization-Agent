from pathlib import Path

import pandas as pd

from analytics.forecasting import (
    prepare_daily_demand,
    time_series_split,
    naive_forecast,
    evaluate_forecast,
    create_forecasting_features,
    train_xgboost_model,
    predict_with_xgboost,
)


BASE_DIR = Path(__file__).resolve().parent.parent

SALES_PATH = (
    BASE_DIR
    / "data"
    / "sample"
    / "sales_data.csv"
)


def main():

    print("=" * 65)
    print("SUPPLY CHAIN DEMAND FORECASTING")
    print("=" * 65)

    # -----------------------------------------------------
    # 1. Load sales data
    # -----------------------------------------------------

    sales_df = pd.read_csv(
        SALES_PATH,
        parse_dates=["date"],
    )

    # -----------------------------------------------------
    # 2. Select product
    # -----------------------------------------------------

    product_id = "P001"

    print(
        f"\nProduct: {product_id}"
    )

    # -----------------------------------------------------
    # 3. Prepare daily demand
    # -----------------------------------------------------

    daily = prepare_daily_demand(
        sales_df,
        product_id,
    )

    print(
        f"Total observations: {len(daily)}"
    )

    # -----------------------------------------------------
    # 4. Create features
    # -----------------------------------------------------

    features = create_forecasting_features(
        daily
    )

    print(
        f"Observations after feature engineering: "
        f"{len(features)}"
    )

    # -----------------------------------------------------
    # 5. Time-series split
    # -----------------------------------------------------

    train, test = time_series_split(
        features,
        test_size=0.20,
    )

    print(
        f"Training observations: {len(train)}"
    )

    print(
        f"Testing observations: {len(test)}"
    )

    # -----------------------------------------------------
    # 6. Baseline
    # -----------------------------------------------------

    baseline_predictions = naive_forecast(
        train,
        test,
    )

    baseline_metrics = evaluate_forecast(
        test["quantity_sold"],
        baseline_predictions,
    )

    # -----------------------------------------------------
    # 7. XGBoost
    # -----------------------------------------------------

    model, feature_columns = (
        train_xgboost_model(train)
    )

    predictions = predict_with_xgboost(
        model,
        test,
        feature_columns,
    )

    ml_metrics = evaluate_forecast(
        test["quantity_sold"],
        predictions,
    )

    # -----------------------------------------------------
    # 8. Results
    # -----------------------------------------------------

    print("\n" + "=" * 65)
    print("MODEL RESULTS")
    print("=" * 65)

    print("\nNaive Baseline")
    print("-" * 65)

    print(
        f"MAE:  {baseline_metrics['MAE']:.2f}"
    )

    print(
        f"RMSE: {baseline_metrics['RMSE']:.2f}"
    )

    print("\nXGBoost")
    print("-" * 65)

    print(
        f"MAE:  {ml_metrics['MAE']:.2f}"
    )

    print(
        f"RMSE: {ml_metrics['RMSE']:.2f}"
    )

    # -----------------------------------------------------
    # 9. Comparison
    # -----------------------------------------------------

    mae_improvement = (
        (
            baseline_metrics["MAE"]
            - ml_metrics["MAE"]
        )
        / baseline_metrics["MAE"]
        * 100
    )

    print("\nComparison")
    print("-" * 65)

    print(
        f"MAE difference: "
        f"{mae_improvement:.2f}%"
    )


if __name__ == "__main__":
    main()