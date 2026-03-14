import mlflow
from src.utils.config_loader import CONFIG

def visual_merchandiser_node(state):
    """LangGraph node for visual merchandising guidelines."""
    query = state.get("query", "")
    with mlflow.trace(name="Visual_Merchandiser_Search") as trace:
        print(f"Visual Merchandiser processing: {query}")
        # Logic to call Vector Search via Managed MCP
        # placeholder logic
        res = f"Visual guidelines for {query}: Use glass shelving."
        state["messages"].append({"role": "assistant", "content": res, "name": "Visual_Merchandiser"})
    return state
