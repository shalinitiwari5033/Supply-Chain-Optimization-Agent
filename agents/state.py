from typing import Any, Dict, Optional
from typing_extensions import TypedDict


class SupplyChainState(TypedDict, total=False):
    # Input datasets
    sales_df: Any
    inventory_df: Any
    supplier_df: Any

    # Processed datasets
    cleaned_sales_df: Any
    cleaned_inventory_df: Any
    cleaned_supplier_df: Any

    # Analytics results
    forecast_result: Optional[Dict[str, Any]]
    inventory_result: Any
    supplier_result: Any
    risk_result: Any

    # Final output
    recommendations: Any

    # Workflow information
    status: str
    errors: list