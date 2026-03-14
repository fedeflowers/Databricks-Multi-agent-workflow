import sys
import os

# Add src to path
sys.path.append(os.path.abspath("src"))

try:
    from utils.config_loader import CONFIG, get_ws_client
    from agents.inventory_analyst import inventory_analyst_node
    from agents.creative_analyst import creative_analyst_node
    from agents.visual_merchandiser import visual_merchandiser_node
    
    print("Successfully imported all nodes and utilities.")
    
    # Mock state
    state = {
        "query": "test query",
        "messages": [],
        "next_step": "",
        "final_response": ""
    }
    
    # Test instantiation (will likely fail on actual API call if not on Databricks, but we want to check constructor)
    print("Testing Creative Analyst instantiation...")
    try:
        # We don't want to run the full executor, just check the toolkit init
        from langchain_databricks import UCFunctionToolkit
        functions = CONFIG["agents"]["creative_analyst"]["uc_functions"]
        toolkit = UCFunctionToolkit(function_names=functions, workspace_client=get_ws_client())
        print("UCFunctionToolkit initialized successfully.")
    except Exception as e:
        print(f"Creative Analyst (Toolkit) failed: {e}")

    print("Testing Inventory Analyst instantiation...")
    try:
        from databricks_langchain import GenieAgent
        space_id = CONFIG["agents"]["inventory_analyst"]["genie_space_id"]
        genie = GenieAgent(genie_space_id=space_id, workspace_client=get_ws_client())
        print("GenieAgent initialized successfully.")
    except Exception as e:
        print(f"Inventory Analyst (Genie) failed: {e}")

    print("Testing Visual Merchandiser instantiation...")
    try:
        from langchain_databricks.vectorstores import DatabricksVectorSearch
        endpoint = CONFIG["agents"]["visual_merchandiser"]["vector_search_endpoint"]
        index_name = CONFIG["agents"]["visual_merchandiser"]["vector_search_index"]
        vector_store = DatabricksVectorSearch(
            index_name=index_name,
            endpoint=endpoint,
            text_column="guideline_text",
            workspace_client=get_ws_client()
        )
        print("DatabricksVectorSearch initialized successfully.")
    except Exception as e:
        print(f"Visual Merchandiser (VectorSearch) failed: {e}")

except Exception as e:
    print(f"Setup failed: {e}")
