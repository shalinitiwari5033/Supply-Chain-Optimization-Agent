import streamlit as st


def show():

    st.header("📦 Inventory Optimization")

    inventory_df = (
        st.session_state["inventory_df"]
        .copy()
    )

    display_columns = [
        "product_id",
        "product_name",
        "current_stock",
        "average_daily_demand",
        "safety_stock",
        "calculated_reorder_point",
        "eoq",
        "inventory_status",
        "recommended_order_quantity",
    ]

    st.dataframe(
        inventory_df[
            display_columns
        ].round(2),
        use_container_width=True,
    )

    st.subheader(
        "Products Requiring Reorder"
    )

    reorder = inventory_df[
        inventory_df["inventory_status"]
        .isin(
            [
                "STOCKOUT",
                "REORDER_REQUIRED",
            ]
        )
    ]

    if reorder.empty:

        st.success(
            "No products currently require reordering."
        )

    else:

        st.warning(
            f"{len(reorder)} product(s) "
            "require attention."
        )

        st.dataframe(
            reorder[
                [
                    "product_name",
                    "current_stock",
                    "calculated_reorder_point",
                    "recommended_order_quantity",
                ]
            ].round(2),
            use_container_width=True,
        )