import os
from dotenv import load_dotenv
load_dotenv()

import mlflow
from utils.config_loader import CONFIG, get_ws_client
from databricks_langchain import DatabricksVectorSearch
from databricks_langchain import DatabricksEmbeddings

mlflow.set_tracking_uri("databricks")
mlflow.langchain.autolog() # Enables automatic tracing for LangChain components


@mlflow.trace(name="Visual_Merchandiser_VS")
def visual_merchandiser_node(state):
    """LangGraph node for visual merchandising guidelines using Vector Search."""
    query = state.get("query", "")
    endpoint = CONFIG["agents"]["visual_merchandiser"]["vector_search_endpoint"]
    index_name = CONFIG["agents"]["visual_merchandiser"]["vector_search_index"]
    
    print(f"Visual Merchandiser searching index: {index_name}")
    
    try:
        # Note: In a real Databricks environment, we'd use DatabricksEmbeddings 
        # or the managed index directly.
        vector_store = DatabricksVectorSearch(
            index_name=index_name,
            endpoint=endpoint,
            workspace_client=get_ws_client()
        )
        
        # Simple similarity search
        docs = vector_store.similarity_search(query, k=2)
        
        if docs:
            res = "Based on Prada Visual Guidelines:\n" + "\n".join([f"- {d.page_content}" for d in docs])
        else:
            res = "No specific visual guidelines found for this query."
            
    except Exception as e:
        res = f"Error searching visual guidelines: {str(e)}"
        
    state["messages"].append({
        "role": "assistant", 
        "content": res, 
        "name": "Visual_Merchandiser"
    })
    return state
