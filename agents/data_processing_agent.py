from analytics.preprocessing import preprocess_dataset


def data_processing_agent(state):
    """Validate and clean all incoming datasets."""

    errors = state.get("errors", [])

    try:
        sales_df, sales_report = preprocess_dataset(
            state["sales_df"],
            "sales"
        )

        inventory_df, inventory_report = preprocess_dataset(
            state["inventory_df"],
            "inventory"
        )

        supplier_df, supplier_report = preprocess_dataset(
            state["supplier_df"],
            "supplier"
        )

        return {
            "cleaned_sales_df": sales_df,
            "cleaned_inventory_df": inventory_df,
            "cleaned_supplier_df": supplier_df,
            "status": "Data processing completed",
            "errors": errors,
        }

    except Exception as exc:
        errors.append(str(exc))

        return {
            "status": "Data processing failed",
            "errors": errors,
        }