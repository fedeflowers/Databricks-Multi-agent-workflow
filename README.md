# Databricks-Multi-agent-workflow: Prada Localized Shop Analytics (PLSA)

Example of multi agent workflow in databricks

## 1. System Overview
An enterprise multi-agent system designed for Prada Shop Managers to access localized inventory, sales, and visual merchandising data using native Databricks tools. The system utilizes a hub-and-spoke orchestration model where a Supervisor routes queries to specialized agents.

## 2. Project Structure

```text
Databricks-Multi-agent-workflow/
├── README.md               # Project documentation
├── databricks.yml          # Databricks Asset Bundle (DAB) configuration
├── config.yaml             # Centralized configuration for agents (Genie IDs, VS indexes, UC functions)
├── Makefile                # Automation scripts for deployment and cleanup
├── requirements.txt        # Python dependencies
├── .env                    # Local environment variables (not committed)
├── src/                    # Application source code
│   ├── app.py              # Streamlit Chatbot UI with thinking trace visualization
│   ├── orchestrator.py     # LangGraph workflow and Supervisor routing logic
│   ├── agents/             # Specialist agent implementations
│   │   ├── inventory_analyst.py    # Databricks Genie integration
│   │   ├── visual_merchandiser.py  # Mosaic AI Vector Search integration
│   │   └── creative_analyst.py     # Unity Catalog Functions as tools
│   └── utils/              # Shared utilities
│       └── config_loader.py        # Environment-aware configuration helper
├── setup/                  # Infrastructure and setup scripts
│   ├── DDL.sql             # SQL for creating demo tables and functions
│   └── deploy_instructions.md
└── .gitignore
```

## 3. Agent Orchestration (The Orchestrator)
The system is powered by **LangGraph**, implementing a Supervisor/Specialist pattern found in `src/orchestrator.py`.

### Supervisor Node
The `supervisor_node` acts as the intelligent router. It uses `ChatDatabricks` to analyze the user's intent and select the most appropriate specialist:
- **Inventory**: Routed to the Genie Space analyst.
- **Merchandiser**: Routed to the Vector Search specialist.
- **Creative**: Routed to the UC Functions analyst.
- **General**: Handled directly for greetings or simple queries.

### Workflow State
The system maintains an `AgentState` containing the query, message history, routing decision (`next_step`), and the `final_response`.

---

## 4. Sub-Agent Details

### 🛍️ Inventory Analyst (`src/agents/inventory_analyst.py`)
- **Core Technology**: [Databricks Genie](https://docs.databricks.com/en/genie/index.html).
- **Function**: Provides a conversational interface over structured SQL data.
- **Implementation**: Uses `GenieAgent` to invoke a specific `genie_space_id` defined in `config.yaml`.

### 🖼️ Visual Merchandiser (`src/agents/visual_merchandiser.py`)
- **Core Technology**: [Mosaic AI Vector Search](https://docs.databricks.com/en/generative-ai/vector-search.html).
- **Function**: Retrieves visual display guidelines and brand placement rules.
- **Implementation**: Performs similarity searches on a Databricks Vector Search index using `DatabricksVectorSearch`.

### 💡 Creative Analyst (`src/agents/creative_analyst.py`)
- **Core Technology**: [Unity Catalog Functions](https://docs.databricks.com/en/udf/unity-catalog-functions.html) & Tool Calling.
- **Function**: Complex sales analysis and multi-table interrogation.
- **Implementation**: Uses `UCFunctionToolkit` to wrap SQL/Python functions as LangChain tools. It operates as a ReAct agent to autonomously find product details before running analysis.

---

## 5. Deployment & Execution
The project is built to run as a **Databricks App** managed via DABs.

### Prerequisites
- Databricks CLI configured for your workspace.
- Unity Catalog access with permissions for Vector Search and UC Functions.

### Deployment Commands
```bash
make deploy
```

## 6. Observability
- **MLflow Tracing**: Integrated throughout the workflow. Each node in the LangGraph and every tool call is traced automatically.
- **Trace Visualization**: Traces can be viewed in the Databricks MLflow UI or captured directly within the Streamlit "Thinking" steps.
