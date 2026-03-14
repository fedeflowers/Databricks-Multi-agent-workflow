import mlflow
from utils.config_loader import CONFIG, get_ws_client
from databricks_langchain.uc_ai import UCFunctionToolkit
from databricks_langchain import ChatDatabricks
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain import hub

@mlflow.trace(name="Creative_Analyst_UC")
def creative_analyst_node(state):
    """LangGraph node for creative analysis using Unity Catalog functions as tools."""
    query = state.get("query", "")
    functions = CONFIG["agents"]["creative_analyst"]["uc_functions"]
    model_name = CONFIG["agents"]["supervisor"]["model"]
    
    print(f"Creative Analyst using tools: {functions}")
    
    try:
        # 1. Load UC functions as tools
        from unitycatalog.ai.databricks import DatabricksFunctionClient
        uc_client = DatabricksFunctionClient(workspace_client=get_ws_client())
        toolkit = UCFunctionToolkit(
            function_names=functions,
            client=uc_client
        )
        tools = toolkit.get_tools()
        
        # 2. Initialize LLM
        llm = ChatDatabricks(endpoint=model_name)
        
        # 3. Create Agent
        prompt = hub.pull("hwchase17/openai-functions-agent")
        agent = create_tool_calling_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        # 4. Run Agent
        result = agent_executor.invoke({"input": query})
        res = result["output"]
        
    except Exception as e:
        res = f"Error in creative analysis: {str(e)}"
        
    state["messages"].append({
        "role": "assistant", 
        "content": res, 
        "name": "Creative_Analyst"
    })
    return state
