import pandas as pd

from agents.graph import build_supply_chain_graph


SALES_PATH = "data/sample/sales_data.csv"
INVENTORY_PATH = "data/sample/inventory_data.csv"
SUPPLIER_PATH = "data/sample/supplier_data.csv"


def main():

    print("=" * 60)
    print("SUPPLY CHAIN MULTI-AGENT WORKFLOW")
    print("=" * 60)

    sales_df = pd.read_csv(SALES_PATH)
    inventory_df = pd.read_csv(INVENTORY_PATH)
    supplier_df = pd.read_csv(SUPPLIER_PATH)

    initial_state = {
        "sales_df": sales_df,
        "inventory_df": inventory_df,
        "supplier_df": supplier_df,
        "errors": [],
        "status": "Workflow started",
    }

    graph = build_supply_chain_graph()

    result = graph.invoke(initial_state)

    print("\nWORKFLOW STATUS")
    print("-" * 60)
    print(result.get("status"))

    print("\nFORECAST")
    print("-" * 60)

    forecast = result.get("forecast_result")

    if forecast:
        print("Product:", forecast["product_id"])
        print("Model:", forecast["model"])
        print("MAE:", round(forecast["mae"], 2))
        print("RMSE:", round(forecast["rmse"], 2))

    print("\nRECOMMENDATIONS")
    print("-" * 60)

    for recommendation in result.get("recommendations", []):
        print(
            f"[{recommendation['priority']}] "
            f"{recommendation['recommendation']}"
        )

        print(
            f"Reason: {recommendation['reason']}"
        )

    print("\nERRORS")
    print("-" * 60)

    if result.get("errors"):
        for error in result["errors"]:
            print(error)
    else:
        print("No errors")


if __name__ == "__main__":
    main()