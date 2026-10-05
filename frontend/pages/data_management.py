import streamlit as st
import pandas as pd


def show():

    st.header("📂 Data Management")

    st.write(
        "Upload supply-chain datasets for analysis."
    )

    sales_file = st.file_uploader(
        "Upload Sales CSV",
        type=["csv"],
        key="sales_upload",
    )

    inventory_file = st.file_uploader(
        "Upload Inventory CSV",
        type=["csv"],
        key="inventory_upload",
    )

    supplier_file = st.file_uploader(
        "Upload Supplier CSV",
        type=["csv"],
        key="supplier_upload",
    )

    if sales_file:

        sales_df = pd.read_csv(
            sales_file
        )

        st.subheader(
            "Sales Dataset Preview"
        )

        st.dataframe(
            sales_df.head(10),
            use_container_width=True,
        )

        st.success(
            f"Sales dataset loaded: "
            f"{len(sales_df):,} rows"
        )

    if inventory_file:

        inventory_df = pd.read_csv(
            inventory_file
        )

        st.subheader(
            "Inventory Dataset Preview"
        )

        st.dataframe(
            inventory_df.head(10),
            use_container_width=True,
        )

        st.success(
            f"Inventory dataset loaded: "
            f"{len(inventory_df):,} rows"
        )

    if supplier_file:

        supplier_df = pd.read_csv(
            supplier_file
        )

        st.subheader(
            "Supplier Dataset Preview"
        )

        st.dataframe(
            supplier_df.head(10),
            use_container_width=True,
        )

        st.success(
            f"Supplier dataset loaded: "
            f"{len(supplier_df):,} rows"
        )