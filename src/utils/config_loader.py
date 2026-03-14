import yaml
import os
import re
import logging
from typing import Any, Dict
from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv

# Load .env file if it exists (for local testing or specific Databricks App secrets)
load_dotenv()

# Configure logging to stdout for Databricks App Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("config_loader")

def resolve_env_vars(obj: Any, key_name: str = "") -> Any:
    """Recursively expands environment variables and ensures URL schemes."""
    if isinstance(obj, dict):
        return {k: resolve_env_vars(v, k) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_env_vars(v, key_name) for v in obj]
    elif isinstance(obj, str):
        # Expand ${VAR} or $VAR
        expanded = os.path.expandvars(obj)
        
        # Log if expansion failed to find a variable (it stays as ${VAR})
        if "${" in expanded and expanded == obj:
            logger.warning(f"Variable expansion may have failed for: {obj}")

        # Specific check for Host URL scheme
        # Add https:// if missing for any host/url/endpoint strings
        if expanded and not expanded.startswith("http") and not expanded.startswith("${"):
            is_host_var = any(k in key_name.upper() for k in ["HOST", "URL", "ENDPOINT", "URI"])
            is_dab_secret = expanded.startswith("${bundle.secrets")
            if (is_host_var or is_dab_secret) and expanded != "databricks":
                expanded = f"https://{expanded}"
                
        if key_name == "hostname" or key_name == "DATABRICKS_HOST":
            if expanded and expanded.startswith("https://"):
                # Clean trailing slash which can break some SDK calls
                cleaned = expanded.rstrip('/')
                if cleaned != expanded:
                    logger.info(f"Cleaned trailing slash from hostname: {expanded} -> {cleaned}")
                    expanded = cleaned
                os.environ["DATABRICKS_HOST"] = expanded
        
        if key_name == "token" or key_name == "DATABRICKS_TOKEN":
            if expanded and not expanded.startswith("${"):
                os.environ["DATABRICKS_TOKEN"] = expanded
            
        return expanded
    return obj

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Loads configuration from a YAML file and resolves environment variables.
    """
    # Prioritize root config, then src
    root_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config_path)
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_path)
    
    if os.path.exists(root_path):
        abs_path = root_path
    elif os.path.exists(src_path):
        abs_path = src_path
    else:
        # Check parent directories for config.yaml as fallback
        current_dir = os.path.dirname(os.path.abspath(__file__))
        while current_dir and current_dir != os.path.dirname(current_dir):
            potential_path = os.path.join(current_dir, config_path)
            if os.path.exists(potential_path):
                abs_path = potential_path
                break
            current_dir = os.path.dirname(current_dir)
    
    if not abs_path:
        # Final fallback to current working directory
        abs_path = config_path
        
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Configuration file not found. Checked up to root and CWD.")
        
    with open(abs_path, 'r') as f:
        config = yaml.safe_load(f)
    
    logger.info(f"Loaded config from {abs_path}")
    return resolve_env_vars(config)

# Global config instance with error handling
try:
    CONFIG = load_config()
    logger.info("Configuration initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize configuration: {e}", exc_info=True)
    # Raise again so it's clear in the logs
    raise

_client = None

def get_ws_client():
    """Returns a memoized Databricks WorkspaceClient instance."""
    global _client
    if _client is None:
        _client = WorkspaceClient()
    return _client
