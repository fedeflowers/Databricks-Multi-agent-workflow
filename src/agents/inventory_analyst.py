import mlflow
from src.utils.config_loader import CONFIG

def inventory_analyst_node(state):
    """LangGraph node for inventory analysis."""
    query = state.get("query", "")
    with mlflow.trace(name="Inventory_Analyst_Query") as trace:
        print(f"Inventory Analyst processing: {query}")
        # Logic to call Genie Space via Managed MCP
        # placeholder logic
        res = f"Inventory check for {query}: 100 units available."
        state["messages"].append({"role": "assistant", "content": res, "name": "Inventory_Analyst"})
    return state
