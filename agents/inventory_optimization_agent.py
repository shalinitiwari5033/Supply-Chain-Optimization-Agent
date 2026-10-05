from analytics.inventory import optimize_inventory


def inventory_optimization_agent(state):
    """Optimize inventory using deterministic inventory calculations."""

    try:
        result = optimize_inventory(
            state["cleaned_sales_df"],
            state["cleaned_inventory_df"]
        )

        return {
            "inventory_result": result,
            "status": "Inventory optimization completed",
        }

    except Exception as exc:

        errors = state.get("errors", [])
        errors.append(str(exc))

        return {
            "status": "Inventory optimization failed",
            "errors": errors,
        }