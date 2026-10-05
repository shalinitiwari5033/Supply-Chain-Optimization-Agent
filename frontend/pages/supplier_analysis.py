import streamlit as st

from frontend.components.charts import (
    supplier_score_chart,
)


def show():

    st.header("🚚 Supplier Analysis")

    supplier_df = (
        st.session_state["supplier_df"]
        .copy()
    )

    supplier_score_chart(
        supplier_df
    )

    st.subheader(
        "Supplier Performance"
    )

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

    st.dataframe(
        supplier_df[
            columns
        ].round(2),
        use_container_width=True,
    )