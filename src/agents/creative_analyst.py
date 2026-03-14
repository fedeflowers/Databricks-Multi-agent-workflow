import mlflow
from src.utils.config_loader import CONFIG

def creative_analyst_node(state):
    """LangGraph node for creative visualizations."""
    query = state.get("query", "")
    with mlflow.trace(name="Creative_Analyst_Viz") as trace:
        print(f"Creative Analyst processing: {query}")
        # Logic to call Custom MCP for Plotly
        # placeholder logic
        res = f"Creative analysis for {query}: Generated Plotly line chart."
        state["messages"].append({"role": "assistant", "content": res, "name": "Creative_Analyst"})
    return state
