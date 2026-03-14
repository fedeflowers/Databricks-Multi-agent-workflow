# Databricks-Multi-agent-workflow: Prada Localized Shop Analytics (PLSA)

**Version:** 2.0.0 (2026)
**Owner:** Prada Group - Global AI Engineering

## 1. System Overview
An enterprise multi-agent system designed for Prada Shop Managers to access localized inventory, sales, and visual merchandising data using native Databricks tools.

## 2. Architecture Specifications
- **UI:** Streamlit Chatbot with expandable "thinking" steps for agent trace visibility.
- **Orchestrator:** LLM-powered Supervisor (LangGraph) acting as an intelligent router.
- **Sub-Agents:**
    - `Inventory_Analyst`: Accesses **Databricks Genie Spaces** for conversational data queries.
    - `Visual_Merchandiser`: Accesses **Mosaic AI Vector Search** for display guidelines.
    - `Creative_Analyst`: Accesses **Unity Catalog Functions** as tools for specialized SQL analysis.
- **Infrastructure:**
    - **Deployment:** Databricks Asset Bundles (DABs) as a **Databricks App**.
    - **Governance:** Unity Catalog (UC) for data, functions, and model serving.

## 3. Project Structure

```
Databricks-Multi-agent-workflow/
├── README.md
├── databricks.yml              # DAB configuration (Databricks App)
├── config.yaml                 # Agent & Tool configurations (Genie ID, VS Index, etc.)
├── requirements.txt
├── src/                        # Application source code
│   ├── app.py                  # Streamlit Chatbot UI
│   ├── orchestrator.py         # Multi-agent supervisor & LangGraph workflow
│   ├── agents/                 # Sub-agents implementations
│   │   ├── inventory_analyst.py
│   │   ├── visual_merchandiser.py
│   │   ├── creative_analyst.py
│   └── utils/                  # Shared utilities (config_loader, etc.)
├── setup/
│   ├── DDL.sql                 # SQL DDLs for mocking tables and guidelines
│   └── deploy_instructions.md
└── .gitignore
```

## 4. Deployment with Databricks Asset Bundles
The project is deployed as a Databricks App. 

1. **Prerequisites:**
   - Databricks CLI configured.
   - Access to a Genie Space, Vector Search endpoint, and UC functions.

2. **Deploy:**
   ```bash
   databricks bundle deploy -t dev
   ```

3. **Run:**
   The Streamlit app will be hosted as a Databricks App in your workspace.

## 5. Observability
- **MLflow Traces:** Every agent execution and tool call is automatically instrumented with `mlflow.trace`.
- **Thinking UI:** The Streamlit app provides a real-time visualization of the agent orchestration steps.


databricks sync . /Workspace/Users/fioriofederico99@gmail.com/plsa-app
databricks apps deploy plsa-app --source-code-path /Workspace/Users/fioriofederico99@gmail.com/plsa-app/src
