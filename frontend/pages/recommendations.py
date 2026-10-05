import streamlit as st


def show():

    st.header("🤖 AI Recommendations")

    st.info(
        "The AI Decision Agent will be connected "
        "in Phase 2."
    )

    st.write(
        "Currently, the system provides "
        "deterministic analytics from:"
    )

    st.write("• Demand forecasting")
    st.write("• Inventory optimization")
    st.write("• Supplier scoring")
    st.write("• Risk analysis")

    st.divider()

    st.subheader(
        "Example Future Recommendation"
    )

    st.write(
        "The AI Decision Agent will interpret "
        "these analytics and generate an "
        "explainable supply-chain recommendation."
    )