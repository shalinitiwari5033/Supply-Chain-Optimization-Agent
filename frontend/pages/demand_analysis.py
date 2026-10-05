import streamlit as st
import plotly.express as px


def show():

    st.header("📈 Sales & Demand Analysis")

    sales_df = st.session_state["sales_df"].copy()

    products = sorted(
        sales_df["product_name"].unique()
    )

    selected_product = st.selectbox(
        "Select Product",
        ["All Products"] + products,
    )

    if selected_product != "All Products":

        filtered = sales_df[
            sales_df["product_name"]
            == selected_product
        ]

    else:
        filtered = sales_df

    daily = (
        filtered
        .groupby("date")["quantity_sold"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        daily,
        x="date",
        y="quantity_sold",
        title="Demand Trend",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Daily Demand",
            f"{daily['quantity_sold'].mean():.2f}",
        )

    with col2:
        st.metric(
            "Maximum Daily Demand",
            f"{daily['quantity_sold'].max():.0f}",
        )

    with col3:
        st.metric(
            "Minimum Daily Demand",
            f"{daily['quantity_sold'].min():.0f}",
        )

    st.subheader("Demand Data")

    st.dataframe(
        daily,
        use_container_width=True,
    )