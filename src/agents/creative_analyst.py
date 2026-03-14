import mlflow
from src.utils.config_loader import CONFIG
from databricks import sql

# Actual table interrogation and creative analysis code

def creative_analyst_node(state):
    """LangGraph node for creative visualizations and table interrogation."""
    query = state.get("query", "")
    catalog = CONFIG['creative_analyst'].get('catalog', 'prada_catalog')
    schema = CONFIG['creative_analyst'].get('schema', 'plsa')
    mcp_endpoint = CONFIG['creative_analyst'].get('mcp_endpoint', '')
    
    with mlflow.trace(name="Creative_Analyst_Viz") as trace:
        print(f"Creative Analyst processing: {query}")
        result_messages = []
        try:
            # Connect to Databricks SQL endpoint (serverless)
            with sql.connect(server_hostname=CONFIG['sql']['hostname'], http_path=CONFIG['sql']['http_path'],
                            access_token=CONFIG['sql']['token']) as conn:
                cursor = conn.cursor()
                # Example: Interrogate products table
                cursor.execute(f"SELECT * FROM {catalog}.{schema}.products LIMIT 5")
                products = cursor.fetchall()
                result_messages.append(f"Sample products: {products}")
                # Example: Interrogate sales table
                cursor.execute(f"SELECT * FROM {catalog}.{schema}.sales LIMIT 5")
                sales = cursor.fetchall()
                result_messages.append(f"Sample sales: {sales}")
                # Example: Query inventory
                cursor.execute(f"SELECT * FROM {catalog}.{schema}.inventory LIMIT 5")
                inventory = cursor.fetchall()
                result_messages.append(f"Sample inventory: {inventory}")
                # Example: Query employees
                cursor.execute(f"SELECT * FROM {catalog}.{schema}.employees LIMIT 5")
                employees = cursor.fetchall()
                result_messages.append(f"Sample employees: {employees}")
                # Optional: guidelines index
                cursor.execute(f"SELECT * FROM {catalog}.{schema}.guidelines_index LIMIT 2")
                guidelines = cursor.fetchall()
                result_messages.append(f"Sample guidelines: {guidelines}")
        except Exception as e:
            result_messages.append(f"Error interrogating tables: {str(e)}")
        # Compose assistant response
        res = f"Creative analysis for {query}:\n" + "\n".join(result_messages)
        state["messages"].append({"role": "assistant", "content": res, "name": "Creative_Analyst"})
    return state
