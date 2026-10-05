from analytics.forecasting import (
    prepare_daily_demand,
    create_forecasting_features,
    time_series_split,
    train_xgboost_model,
    predict_with_xgboost,
    evaluate_forecast,
)


def demand_forecasting_agent(state):
    """Run demand forecasting using the existing forecasting engine."""

    sales_df = state["cleaned_sales_df"]

    try:
        product_id = sales_df["product_id"].iloc[0]

        daily_demand = prepare_daily_demand(
            sales_df,
            product_id=product_id
        )

        feature_df = create_forecasting_features(daily_demand)

        train_df, test_df = time_series_split(
            feature_df,
            test_size=0.20
        )

        model, feature_columns = train_xgboost_model(train_df)

        predictions = predict_with_xgboost(
            model,
            test_df,
            feature_columns
        )

        metrics = evaluate_forecast(
            test_df["quantity_sold"],
            predictions
        )

        forecast_result = {
            "product_id": product_id,
            "model": "XGBoost",
            "mae": metrics["mae"],
            "rmse": metrics["rmse"],
            "test_predictions": predictions,
        }

        return {
            "forecast_result": forecast_result,
            "status": "Demand forecasting completed",
        }

    except Exception as exc:

        errors = state.get("errors", [])
        errors.append(str(exc))

        return {
            "status": "Demand forecasting failed",
            "errors": errors,
        }