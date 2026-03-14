try:
    from unitycatalog.ai.core.client import UnityCatalogClient
    print("Found UnityCatalogClient")
except ImportError:
    try:
        from databricks_langchain.uc_ai import UCFunctionToolkit
        print("Found UCFunctionToolkit in databricks_langchain")
        # Check if we can get the expected client type
        from unitycatalog.ai.core.base import BaseFunctionClient
        print("Found BaseFunctionClient")
    except ImportError as e:
        print(f"Import error: {e}")
