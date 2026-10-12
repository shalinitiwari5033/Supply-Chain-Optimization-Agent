from agents.llm_service import generate_ai_explanation
def decision_agent(state):
    """
    Generate explainable supply-chain recommendations.

    This is the rule-based version.
    An LLM will be added later to improve
    natural-language explanation.
    """

    recommendations = []

    inventory_df = state.get("inventory_result")
    risk_df = state.get("risk_result")

    if inventory_df is not None:

        reorder_items = inventory_df[
            inventory_df["inventory_status"].isin(
                ["STOCKOUT", "REORDER_REQUIRED"]
            )
        ]

        for _, row in reorder_items.iterrows():

            recommendations.append({
                "type": "Inventory",
                "product_id": row["product_id"],
                "priority": "HIGH",
                "recommendation": (
                    f"Reorder {row['product_name']} with approximately "
                    f"{row['recommended_order_quantity']:.0f} units."
                ),
                "reason": (
                    f"Current stock is {row['current_stock']:.0f}, "
                    f"while the calculated reorder point is "
                    f"{row['calculated_reorder_point']:.2f}."
                ),
            })

    if risk_df is not None:

        high_risk = risk_df[
            risk_df["risk_level"].isin(["HIGH", "CRITICAL"])
        ]

        for _, row in high_risk.iterrows():

            recommendations.append({
                "type": "Risk",
                "product_id": row["product_id"],
                "priority": row["risk_level"],
                "recommendation": (
                    f"Review supply-chain risk for {row['product_name']}."
                ),
                "reason": "; ".join(row["risk_factors"]),
            })

    if not recommendations:

        recommendations.append({
            "type": "General",
            "product_id": None,
            "priority": "LOW",
            "recommendation": "No immediate supply-chain action is required.",
            "reason": "Current inventory and risk indicators are within acceptable levels.",
        })

    
    forecast_result = state.get("forecast_result")
    risk_df = state.get("risk_result")

    ai_explanation = generate_ai_explanation(
         recommendations=recommendations,
         forecast_result=state.get("forecast_result"),
         risk_result=state.get("risk_result"),
)


    if ai_explanation:
        explanation_source = "LLM"
    else:
        explanation_source = "Rule-based fallback"

        ai_explanation = (
            "AI explanation is unavailable. "
            "Use the structured recommendations below. "
            "They were generated from the project's analytics rules."
        )

    return {
        "recommendations": recommendations,
        "ai_explanation": ai_explanation,
        "explanation_source": explanation_source,
        "status": "Decision analysis completed",
    }

