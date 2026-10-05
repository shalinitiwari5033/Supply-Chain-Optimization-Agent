import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


# =========================================================
# Prepare Daily Demand
# =========================================================

def prepare_daily_demand(
    sales_df,
    product_id=None,
):
    """
    Convert transaction-level sales data into
    daily demand data.

    If product_id is provided, only that product
    is analyzed.
    """

    df = sales_df.copy()

    # Make sure date is datetime
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(
        subset=["date"]
    )

    # Filter product if requested
    if product_id is not None:

        df = df[
            df["product_id"] == product_id
        ]

    # Aggregate sales by date
    daily = (
        df.groupby("date")["quantity_sold"]
        .sum()
        .reset_index()
    )

    daily = daily.sort_values(
        "date"
    ).reset_index(drop=True)

    return daily


# =========================================================
# Train/Test Split
# =========================================================

def time_series_split(
    daily_df,
    test_size=0.20,
):
    """
    Split time-series data chronologically.

    IMPORTANT:
    We do not randomly shuffle time-series data.
    """

    df = daily_df.sort_values(
        "date"
    ).reset_index(drop=True)

    split_index = int(
        len(df) * (1 - test_size)
    )

    train = df.iloc[
        :split_index
    ].copy()

    test = df.iloc[
        split_index:
    ].copy()

    return train, test


# =========================================================
# Naive Forecast
# =========================================================

def naive_forecast(
    train_df,
    test_df,
):
    """
    Baseline forecast.

    Uses the last observed training demand
    as the prediction for every test day.
    """

    last_value = train_df[
        "quantity_sold"
    ].iloc[-1]

    predictions = np.full(
        len(test_df),
        last_value,
    )

    return predictions


# =========================================================
# Forecast Evaluation
# =========================================================

def evaluate_forecast(
    actual,
    predicted,
):
    """
    Calculate MAE and RMSE.
    """

    mae = mean_absolute_error(
        actual,
        predicted,
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted,
        )
    )

    return {
        "MAE": float(mae),
        "RMSE": float(rmse),
    }


# =========================================================
# Feature Engineering
# =========================================================

def create_forecasting_features(daily_df):
    """
    Create time-series features for ML forecasting.
    """

    df = daily_df.copy()

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df = df.sort_values(
        "date"
    ).reset_index(drop=True)

    # Calendar features
    df["day_of_week"] = (
        df["date"].dt.dayofweek
    )

    df["day_of_month"] = (
        df["date"].dt.day
    )

    df["month"] = (
        df["date"].dt.month
    )

    df["week_of_year"] = (
        df["date"].dt.isocalendar().week
        .astype(int)
    )

    # Trend
    df["trend"] = np.arange(
        len(df)
    )

    # Lag features
    df["lag_1"] = (
        df["quantity_sold"]
        .shift(1)
    )

    df["lag_7"] = (
        df["quantity_sold"]
        .shift(7)
    )

    df["lag_14"] = (
        df["quantity_sold"]
        .shift(14)
    )

    # Rolling features
    df["rolling_mean_7"] = (
        df["quantity_sold"]
        .shift(1)
        .rolling(7)
        .mean()
    )

    df["rolling_mean_14"] = (
        df["quantity_sold"]
        .shift(1)
        .rolling(14)
        .mean()
    )

    # Remove rows created by lag/rolling operations
    df = df.dropna().reset_index(
        drop=True
    )

    return df


# =========================================================
# XGBoost Model
# =========================================================

def train_xgboost_model(train_df):
    """
    Train an XGBoost demand forecasting model.
    """

    from xgboost import XGBRegressor

    feature_columns = [
        "day_of_week",
        "day_of_month",
        "month",
        "week_of_year",
        "trend",
        "lag_1",
        "lag_7",
        "lag_14",
        "rolling_mean_7",
        "rolling_mean_14",
    ]

    X_train = train_df[
        feature_columns
    ]

    y_train = train_df[
        "quantity_sold"
    ]

    model = XGBRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42,
    )

    model.fit(
        X_train,
        y_train,
    )

    return model, feature_columns


# =========================================================
# Model Prediction
# =========================================================

def predict_with_xgboost(
    model,
    test_df,
    feature_columns,
):
    """
    Generate predictions using trained XGBoost model.
    """

    X_test = test_df[
        feature_columns
    ]

    predictions = model.predict(
        X_test
    )

    # Demand cannot be negative
    predictions = np.maximum(
        predictions,
        0,
    )

    return predictions