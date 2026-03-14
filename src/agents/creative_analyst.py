import os
from dotenv import load_dotenv
load_dotenv()

import mlflow
from utils.config_loader import CONFIG, get_ws_client
from databricks_langchain.uc_ai import UCFunctionToolkit
from databricks_langchain import ChatDatabricks
from langgraph.prebuilt import create_react_agent

mlflow.set_tracking_uri("databricks")
mlflow.langchain.autolog() # Enables automatic tracing for LangChain components

@mlflow.trace(name="Creative_Analyst_UC")
def creative_analyst_node(state):
    """LangGraph node for creative analysis using Unity Catalog functions as tools."""
    query = state.get("query", "")
    functions = CONFIG["agents"]["creative_analyst"]["uc_functions"]
    model_name = CONFIG["agents"]["supervisor"]["model"]
    
    print(f"Creative Analyst using tools: {functions}")
    
    try:
        # 1. Load UC functions as tools
        toolkit = UCFunctionToolkit(
            function_names=functions,
            workspace_client=get_ws_client()
        )
        tools = toolkit.tools
        
        # 2. Initialize LLM
        llm = ChatDatabricks(endpoint=model_name)
        
        # 3. Define System Prompt for the agent
        system_prompt = (
            "You are a Prada Creative Analyst. Your goal is to analyze product performance and sales.\n"
            "If you need a 'product_id' or 'product_name' but don't have it, use 'query_products' first to find it.\n"
            "NEVER pass 'null', 'None', or empty strings to required tool parameters. "
            "If you cannot find a parameter value, ask the user for clarification instead of guessing."
        )
        
        # 4. Create Agent
        # Use prompt or messages_modifier based on your langgraph version
        agent = create_react_agent(llm, tools, prompt=system_prompt)
        
        # 5. Run Agent
        result = agent.invoke({"messages": [{"role": "user", "content": query}]})
        res = result["messages"][-1].content
        
    except Exception as e:
        res = f"Error in creative analysis: {str(e)}"
        
    state["messages"].append({
        "role": "assistant", 
        "content": res, 
        "name": "Creative_Analyst"
    })
    return state
