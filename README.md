# Databricks-Multi-agent-workflow

# Project: Prada Localized Shop Analytics (PLSA)
**Version:** 1.0.0 (2026)
**Owner:** Prada Group - Global AI Engineering

## 1. System Overview
An enterprise multi-agent system designed for Prada Shop Managers to access localized inventory, sales, and visual merchandising data.

## 2. Architecture Specifications
- **Orchestrator:** Supervisor Agent (Mosaic AI Agent SDK) acting as a router.
- **Sub-Agents:**
    - `Inventory_Analyst`: Accesses Genie Spaces via Managed MCP.
    - `Visual_Merchandiser`: Accesses Vector Search for guidelines.
    - `Creative_Analyst`: Accesses Custom MCP for specialized Plotly visualizations.
- **Infrastructure:**
    - **Deployment:** Databricks Asset Bundles (DABs).
    - **Hosting:** Model Serving (Agents) & Databricks Apps (Custom MCP).
    - **Governance:** Unity Catalog (UC) for data, permissions, and model aliases (@prod).

## 3. Tooling & MCP Configurations
- **Managed MCPs:**
    - Genie Space: `catalog.schema.prada_genie`
    - Vector Search: `catalog.schema.guidelines_index`
- **Custom MCP:**
    - Endpoint: `https://mcp-viz-prada.databricksapps.com/api/mcp`
    - Functions: `generate_plotly_chart`, `calculate_kpi_delta`.

## 4. CI/CD & MLOps Standards
- **Evaluation:** Gated by MLflow "LLM-as-a-judge" on Golden Datasets.
- **Observability:**
    - MLflow Traces (30-day UI retention).
    - Inference Tables (Indefinite Delta retention in `catalog.monitoring.logs`).
- **Drift Detection:** Managed via Lakehouse Monitoring on the Inference Tables.

## 5. Development Instructions for Genie
1. Always use **Python 3.11+** and **FastMCP** for server development.
2. Deployment configurations must be strictly defined in `databricks.yml`.
3. All agents must include `mlflow.trace` instrumentation.
4. UI components are built exclusively with **Streamlit**.

---

## 6. Project Structure & Deployment Guide

```
Databricks-Multi-agent-workflow/
├── README.md
├── databricks.yml              # DAB configuration (assets, targets, permissions)
├── bundle/                     # DAB bundle packaging
│   ├── mcp_server/             # Custom MCP FastMCP server code
│   ├── agents/                 # Multi-agent architecture (Supervisor & Sub-agents)
│   ├── streamlit_ui/           # Streamlit UI components
│   └── utils/                  # Shared utilities, MLflow instrumentation
├── src/                        # Application source code
│   ├── orchestrator.py         # Orchestrator main logic
│   ├── agents/                 # Sub-agents implementations (Inventory, Merchandiser, Creative)
│   │   ├── inventory_analyst.py
│   │   ├── visual_merchandiser.py
│   │   ├── creative_analyst.py
│   │   └── ...
│   ├── mcp/                    # Custom/Managed MCP client code
│   └── utils/                  # Domain/business utilities, metrics, helpers
├── setup/
│   ├── DDL.md                  # DDL scripts: create catalogs, schemas, example tables/data
│   └── deploy_instructions.md  # Step-by-step deployment instructions (catalog/schema/table setup)
└── .gitignore
```

- **src/** contains all core application code, including orchestrator logic, agent submodules, MCP clients, and supporting utilities.
- Assets in **bundle/** are used for DAB packaging and deployment.

### Deployment with Databricks Asset Bundles
- Define all assets (notebooks, clusters, jobs, tables) in `databricks.yml`.
- Package using DABs to ensure environment, permissions, and dependencies are reproducible for Databricks/AWS.

### Table Creation & Example Data
- See [setup/DDL.md](#file-DDL.md) for SQL DDLs to create catalogs, schemas, tables (prada_genie, guidelines_index, monitoring.logs).
- Includes example INSERTs for demo/test purposes.

### Setup Instructions
- Complete workflow to provision Unity Catalogs and Schemas in [setup/deploy_instructions.md](#file-deploy_instructions.md).
    - Step-by-step Databricks CLI commands (or UI prompts)
    - Guidance on asset deployment, table population, and permissions

---

For further details, refer to the respective files in the `setup/` directory. For asset bundle specifics, see the main `databricks.yml`.