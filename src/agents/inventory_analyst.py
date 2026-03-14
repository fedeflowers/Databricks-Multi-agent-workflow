import os
from dotenv import load_dotenv
load_dotenv()

import mlflow
from utils.config_loader import CONFIG
from databricks_langchain import GenieAgent

mlflow.set_tracking_uri("databricks")
mlflow.langchain.autolog() # Enables automatic tracing for LangChain components

@mlflow.trace(name="Inventory_Analyst_Genie")
def inventory_analyst_node(state):
    """LangGraph node for inventory analysis using Databricks Genie."""
    query = state.get("query", "")
    space_id = CONFIG["agents"]["inventory_analyst"]["genie_space_id"]
    
    print(f"Inventory Analyst calling Genie Space: {space_id}")
    
    # Initialize Genie Agent
    genie = GenieAgent(genie_space_id=space_id)
    
    # Execute query
    try:
        response = genie.invoke({"messages": [{"role": "user", "content": query}]})
        res = response["messages"][-1].content
    except Exception as e:
        res = f"Error querying Genie Space: {str(e)}"
        
    state["messages"].append({
        "role": "assistant", 
        "content": res, 
        "name": "Inventory_Analyst"
    })
    return state
