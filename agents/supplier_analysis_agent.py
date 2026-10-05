from analytics.supplier_scoring import rank_suppliers
from analytics.risk_analysis import analyze_risk


def supplier_analysis_agent(state):
    """Analyze supplier performance and supply-chain risk."""

    try:
        supplier_result = rank_suppliers(
            state["cleaned_supplier_df"]
        )

        risk_result = analyze_risk(
            inventory_df=state["inventory_result"],
            supplier_df=supplier_result,
            demand_df=state["cleaned_sales_df"],
        )

        return {
            "supplier_result": supplier_result,
            "risk_result": risk_result,
            "status": "Supplier and risk analysis completed",
        }

    except Exception as exc:

        errors = state.get("errors", [])
        errors.append(str(exc))

        return {
            "status": "Supplier analysis failed",
            "errors": errors,
        }