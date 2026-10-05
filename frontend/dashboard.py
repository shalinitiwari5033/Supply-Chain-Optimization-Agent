import streamlit as st
import pandas as pd

from analytics.inventory import optimize_inventory
from analytics.supplier_scoring import rank_suppliers
from analytics.risk_analysis import analyze_risk


SALES_PATH = "data/sample/sales_data.csv"
INVENTORY_PATH = "data/sample/inventory_data.csv"
SUPPLIER_PATH = "data/sample/supplier_data.csv"


@st.cache_data
def load_sample_data():

    sales_df = pd.read_csv(SALES_PATH)
    inventory_df = pd.read_csv(INVENTORY_PATH)
    supplier_df = pd.read_csv(SUPPLIER_PATH)

    sales_df["date"] = pd.to_datetime(
        sales_df["date"]
    )

    return (
        sales_df,
        inventory_df,
        supplier_df,
    )


@st.cache_data
def calculate_analytics(
    sales_df,
    inventory_df,
    supplier_df,
):

    inventory_result = optimize_inventory(
        sales_df,
        inventory_df,
    )

    supplier_result = rank_suppliers(
        supplier_df,
    )

    risk_result = analyze_risk(
        inventory_df=inventory_result,
        supplier_df=supplier_result,
        demand_df=sales_df,
    )

    return (
        inventory_result,
        supplier_result,
        risk_result,
    )


def main():

    st.set_page_config(
        page_title="Supply Chain Optimization Agent",
        page_icon="📦",
        layout="wide",
    )

    st.title(
        "📦 Supply Chain Optimization Agent"
    )

    st.caption(
        "AI-powered supply-chain decision support system"
    )

    (
        sales_df,
        inventory_df,
        supplier_df,
    ) = load_sample_data()

    (
        inventory_result,
        supplier_result,
        risk_result,
    ) = calculate_analytics(
        sales_df,
        inventory_df,
        supplier_df,
    )

    # Store data for pages
    st.session_state["sales_df"] = sales_df
    st.session_state["inventory_df"] = inventory_result
    st.session_state["supplier_df"] = supplier_result
    st.session_state["risk_df"] = risk_result

    st.success(
        "Analytics engine loaded successfully."
    )

    st.info(
        "Use the pages in the sidebar to explore "
        "demand, inventory, suppliers and risk."
    )


if __name__ == "__main__":
    main()