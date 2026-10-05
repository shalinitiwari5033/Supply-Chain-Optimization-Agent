import streamlit as st

from frontend.components.metrics import display_kpi
from frontend.components.charts import (
    demand_chart,
    inventory_chart,
    risk_chart,
)


def show():

    st.header("📊 Supply Chain Overview")

    sales_df = st.session_state["sales_df"]
    inventory_df = st.session_state["inventory_df"]
    risk_df = st.session_state["risk_df"]

    total_products = inventory_df[
        "product_id"
    ].nunique()

    total_sales = sales_df[
        "quantity_sold"
    ].sum()

    products_requiring_reorder = (
        inventory_df["inventory_status"]
        .isin(
            [
                "STOCKOUT",
                "REORDER_REQUIRED",
            ]
        )
        .sum()
    )

    high_risk_products = (
        risk_df["risk_level"]
        .isin(
            [
                "HIGH",
                "CRITICAL",
            ]
        )
        .sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        display_kpi(
            "Products",
            total_products,
        )

    with col2:
        display_kpi(
            "Total Units Sold",
            f"{total_sales:,.0f}",
        )

    with col3:
        display_kpi(
            "Reorder Required",
            products_requiring_reorder,
        )

    with col4:
        display_kpi(
            "High/Critical Risk",
            high_risk_products,
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        demand_chart(sales_df)

    with col2:
        inventory_chart(inventory_df)

    st.divider()

    risk_chart(risk_df)