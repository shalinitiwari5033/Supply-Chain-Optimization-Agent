import streamlit as st

from frontend.dashboard import (
    load_sample_data,
    calculate_analytics,
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

    st.session_state["sales_df"] = sales_df
    st.session_state["inventory_df"] = inventory_result
    st.session_state["supplier_df"] = supplier_result
    st.session_state["risk_df"] = risk_result

    st.sidebar.title(
        "Navigation"
    )

    page = st.sidebar.radio(
        "Go to",
        [
            "Overview",
            "Sales / Demand",
            "Inventory",
            "Supplier Analysis",
            "Risk Analysis",
            "AI Recommendations",
            "Data Management",
        ],
    )

    if page == "Overview":

        from frontend.pages.overview import show
        show()

    elif page == "Sales / Demand":

        from frontend.pages.demand_analysis import show
        show()

    elif page == "Inventory":

        from frontend.pages.inventory import show
        show()

    elif page == "Supplier Analysis":

        from frontend.pages.supplier_analysis import show
        show()

    elif page == "Risk Analysis":

        from frontend.pages.risk_analysis import show
        show()

    elif page == "AI Recommendations":

        from frontend.pages.recommendations import generate_ai_explanation
        generate_ai_explanation()

    elif page == "Data Management":

        from frontend.pages.data_management import show
        show()


if __name__ == "__main__":
    main()