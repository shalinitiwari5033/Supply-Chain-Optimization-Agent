import streamlit as st

from frontend.components.charts import (
    risk_chart,
)


def show():

    st.header("⚠️ Supply Chain Risk")

    risk_df = (
        st.session_state["risk_df"]
        .copy()
    )

    risk_chart(risk_df)

    st.subheader(
        "Product Risk Assessment"
    )

    columns = [
        "product_id",
        "product_name",
        "stock_risk",
        "demand_risk",
        "supplier_risk",
        "lead_time_risk",
        "overall_risk_score",
        "risk_level",
    ]

    st.dataframe(
        risk_df[
            columns
        ].round(2),
        use_container_width=True,
    )

    st.subheader(
        "Risk Factors"
    )

    for _, row in risk_df.iterrows():

        with st.expander(
            f"{row['product_name']} — "
            f"{row['risk_level']}"
        ):

            st.write(
                f"Overall Risk Score: "
                f"{row['overall_risk_score']:.2f}"
            )

            for factor in row["risk_factors"]:
                st.write(
                    f"• {factor}"
                )