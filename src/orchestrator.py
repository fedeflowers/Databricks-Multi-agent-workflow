import mlflow
from typing import TypedDict, Annotated, List, Union
from langgraph.graph import StateGraph, END
from src.utils.config_loader import CONFIG
from src.agents.inventory_analyst import inventory_analyst_node
from src.agents.visual_merchandiser import visual_merchandiser_node
from src.agents.creative_analyst import creative_analyst_node

# Define Graph State
class AgentState(TypedDict):
    query: str
    messages: List[Dict]
    next_step: str

def supervisor_node(state: AgentState):
    """Router node that decides which agent to call."""
    query = state["query"].lower()
    print(f"Supervisor routing query: {query}")
    
    if "inventory" in query or "stock" in query:
        state["next_step"] = "inventory"
    elif "visual" in query or "display" in query or "guideline" in query:
        state["next_step"] = "merchandiser"
    elif "chart" in query or "viz" in query or "analysis" in query:
        state["next_step"] = "creative"
    else:
        state["next_step"] = END
        
    return state

def create_workflow():
    """Constructs the LangGraph workflow."""
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("inventory", inventory_analyst_node)
    workflow.add_node("merchandiser", visual_merchandiser_node)
    workflow.add_node("creative", creative_analyst_node)
    
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
            END: END
        }
    )
    
    # Add completion edges back to supervisor or end
    workflow.add_edge("inventory", END)
    workflow.add_edge("merchandiser", END)
    workflow.add_edge("creative", END)
    
    return workflow.compile()

def main():
    """Main execution of the Multi-agent system."""
    mlflow.set_tracking_uri(CONFIG["mlflow"]["tracking_uri"])
    
    app = create_workflow()
    
    initial_state = {
        "query": "Show me the inventory for Prada sunglasses",
        "messages": [],
        "next_step": ""
    }
    
    print("Running PLSA Workflow...")
    result = app.invoke(initial_state)
    print("\nWorkflow Result:")
    for msg in result["messages"]:
        print(f"[{msg['name']}]: {msg['content']}")

if __name__ == "__main__":
    main()
