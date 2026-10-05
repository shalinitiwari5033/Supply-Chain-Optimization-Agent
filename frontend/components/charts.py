import plotly.express as px
import streamlit as st


def demand_chart(sales_df):

    daily = (
        sales_df
        .groupby("date")["quantity_sold"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        daily,
        x="date",
        y="quantity_sold",
        title="Daily Demand",
        labels={
            "date": "Date",
            "quantity_sold": "Units Sold",
        },
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


def inventory_chart(inventory_df):

    fig = px.bar(
        inventory_df,
        x="product_name",
        y="current_stock",
        title="Current Inventory",
        labels={
            "product_name": "Product",
            "current_stock": "Units",
        },
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


def supplier_score_chart(supplier_df):

    summary = (
        supplier_df
        .groupby(
            ["supplier_id", "supplier_name"],
            as_index=False,
        )["supplier_score"]
        .mean()
        .sort_values(
            "supplier_score",
            ascending=False,
        )
    )

    fig = px.bar(
        summary,
        x="supplier_name",
        y="supplier_score",
        title="Supplier Performance",
        labels={
            "supplier_name": "Supplier",
            "supplier_score": "Score",
        },
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


def risk_chart(risk_df):

    summary = (
        risk_df["risk_level"]
        .value_counts()
        .reset_index()
    )

    summary.columns = [
        "risk_level",
        "count",
    ]

    fig = px.bar(
        summary,
        x="risk_level",
        y="count",
        title="Supply Chain Risk Distribution",
        labels={
            "risk_level": "Risk Level",
            "count": "Products",
        },
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )