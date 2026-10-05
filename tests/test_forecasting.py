import pandas as pd
import numpy as np

from analytics.forecasting import (
    prepare_daily_demand,
    time_series_split,
    naive_forecast,
    evaluate_forecast,
)


def test_prepare_daily_demand():

    df = pd.DataFrame(
        {
            "date": [
                "2026-01-01",
                "2026-01-01",
                "2026-01-02",
            ],
            "product_id": [
                "P001",
                "P001",
                "P001",
            ],
            "quantity_sold": [
                10,
                20,
                15,
            ],
        }
    )

    result = prepare_daily_demand(
        df,
        "P001",
    )

    assert len(result) == 2

    assert result.iloc[0]["quantity_sold"] == 30

    assert result.iloc[1]["quantity_sold"] == 15


def test_time_series_split():

    df = pd.DataFrame(
        {
            "date": pd.date_range(
                "2026-01-01",
                periods=10,
                freq="D",
            ),
            "quantity_sold": range(10),
        }
    )

    train, test = time_series_split(
        df,
        test_size=0.20,
    )

    assert len(train) == 8

    assert len(test) == 2

    assert train["date"].max() < test["date"].min()


def test_naive_forecast():

    train = pd.DataFrame(
        {
            "date": pd.date_range(
                "2026-01-01",
                periods=3,
                freq="D",
            ),
            "quantity_sold": [
                10,
                20,
                30,
            ],
        }
    )

    test = pd.DataFrame(
        {
            "date": pd.date_range(
                "2026-01-04",
                periods=2,
                freq="D",
            ),
            "quantity_sold": [
                25,
                35,
            ],
        }
    )

    predictions = naive_forecast(
        train,
        test,
    )

    assert len(predictions) == 2

    assert predictions[0] == 30

    assert predictions[1] == 30


def test_evaluate_forecast():

    actual = [10, 20, 30]

    predicted = [12, 18, 29]

    result = evaluate_forecast(
        actual,
        predicted,
    )

    assert "MAE" in result

    assert "RMSE" in result

    assert result["MAE"] >= 0

    assert result["RMSE"] >= 0

from analytics.forecasting import (
    create_forecasting_features,
    train_xgboost_model,
    predict_with_xgboost,
)

def test_create_forecasting_features():

    dates = pd.date_range(
        "2026-01-01",
        periods=30,
        freq="D",
    )

    df = pd.DataFrame(
        {
            "date": dates,
            "quantity_sold": range(
                10,
                40,
            ),
        }
    )

    result = create_forecasting_features(
        df
    )

    assert "day_of_week" in result.columns

    assert "month" in result.columns

    assert "lag_1" in result.columns

    assert "lag_7" in result.columns

    assert "rolling_mean_7" in result.columns

    assert len(result) > 0


def test_xgboost_forecast():

    dates = pd.date_range(
        "2026-01-01",
        periods=60,
        freq="D",
    )

    df = pd.DataFrame(
        {
            "date": dates,
            "quantity_sold": (
                20
                + np.arange(60) * 0.2
            ),
        }
    )

    features = create_forecasting_features(
        df
    )

    train = features.iloc[
        :-10
    ]

    test = features.iloc[
        -10:
    ]

    model, feature_columns = (
        train_xgboost_model(train)
    )

    predictions = predict_with_xgboost(
        model,
        test,
        feature_columns,
    )

    assert len(predictions) == 10

    assert np.all(
        predictions >= 0
    )


