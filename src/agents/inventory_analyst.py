import mlflow
from utils.config_loader import CONFIG
from databricks_langchain import GenieAgent

@mlflow.trace(name="Inventory_Analyst_Genie")
def inventory_analyst_node(state):
    """LangGraph node for inventory analysis using Databricks Genie."""
    query = state.get("query", "")
    space_id = CONFIG["agents"]["inventory_analyst"]["genie_space_id"]
    
    print(f"Inventory Analyst calling Genie Space: {space_id}")
    
    # Initialize Genie Agent
    from utils.config_loader import get_ws_client
    genie = GenieAgent(genie_space_id=space_id, workspace_client=get_ws_client())
    
    # Execute query
    try:
        response = genie.invoke(query)
        res = response.content
    except Exception as e:
        res = f"Error querying Genie Space: {str(e)}"
        
    state["messages"].append({
        "role": "assistant", 
        "content": res, 
        "name": "Inventory_Analyst"
    })
    return state
