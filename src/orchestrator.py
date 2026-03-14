import mlflow
import json
from typing import TypedDict, List, Dict, Union
from langgraph.graph import StateGraph, END
from databricks_langchain import ChatDatabricks
from utils.config_loader import CONFIG
from agents.inventory_analyst import inventory_analyst_node
from agents.visual_merchandiser import visual_merchandiser_node
from agents.creative_analyst import creative_analyst_node

# Define Graph State
class AgentState(TypedDict):
    query: str
    messages: List[Dict]
    next_step: str
    final_response: str

@mlflow.trace(name="Supervisor_Routing")
def supervisor_node(state: AgentState):
    """LLM-based supervisor that routes the query to the correct specialist."""
    query = state["query"]
    model_name = CONFIG["agents"]["supervisor"]["model"]
    
    llm = ChatDatabricks(endpoint=model_name)
    
    system_prompt = (
        "You are a Prada Store Manager Assistant Supervisor. "
        "Your job is to route the user query to the correct specialist agent.\n"
        "Specialists:\n"
        "- inventory: For product stock levels, warehouse availability, and inventory counts.\n"
        "- merchandiser: For visual display guidelines, shop floor aesthetics, and Prada brand placement rules.\n"
        "- creative: For sales analysis, product performance details, and complex data interrogation across tables.\n"
        "- general: For general greetings or questions that don't need a specialist.\n\n"
        "Return ONLY a JSON object with a single key 'selection' valued as one of [inventory, merchandiser, creative, general]."
    )
    
    try:
        response = llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ])
        content = response.content.strip()
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        
        decision = json.loads(content)
        selection = decision.get("selection", "general")
    except Exception as e:
        print(f"Error in supervisor routing: {e}")
        selection = "general"
        
    state["next_step"] = selection
    print(f"Supervisor routed to: {selection}")
    return state

@mlflow.trace(name="General_Assistant")
def general_node(state: AgentState):
    """Direct LLM response for general queries."""
    query = state["query"]
    model_name = CONFIG["agents"]["supervisor"]["model"]
    
    llm = ChatDatabricks(endpoint=model_name)
    response = llm.invoke([
        {"role": "system", "content": "You are a helpful Prada Assistant. Answer the user query directly."},
        {"role": "user", "content": query}
    ])
    state["final_response"] = response.content
    state["messages"].append({"role": "assistant", "content": response.content, "name": "General_Assistant"})
    return state

def create_workflow():
    """Constructs the LangGraph workflow."""
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("inventory", inventory_analyst_node)
    workflow.add_node("merchandiser", visual_merchandiser_node)
    workflow.add_node("creative", creative_analyst_node)
    workflow.add_node("general", general_node)
    
    # Set Entry Point
    workflow.set_entry_point("supervisor")
    
    # Add Conditional Edges
    workflow.add_conditional_edges(
        "supervisor",
        lambda x: x["next_step"],
        {
            "inventory": "inventory",
            "merchandiser": "merchandiser",
            "creative": "creative",
            "general": "general"
        }
    )
    
    # Add completion edges
    workflow.add_edge("inventory", END)
    workflow.add_edge("merchandiser", END)
    workflow.add_edge("creative", END)
    workflow.add_edge("general", END)
    
    return workflow.compile()

# Initialize the app once
PLSA_APP = create_workflow()

def run_agent(query: str):
    """Runs the multi-agent system for a given query."""
    mlflow.set_tracking_uri(CONFIG["mlflow"]["tracking_uri"])
    
    initial_state = {
        "query": query,
        "messages": [],
        "next_step": "",
        "final_response": ""
    }
    
    result = PLSA_APP.invoke(initial_state)
    
    # Extract final response
    if not result.get("final_response") and result["messages"]:
        result["final_response"] = result["messages"][-1]["content"]
        
    return result

if __name__ == "__main__":
    # Test run
    test_query = "What is the stock level for Prada Galleria bags?"
    print(f"Testing with query: {test_query}")
    res = run_agent(test_query)
    print(f"Final Response: {res['final_response']}")
