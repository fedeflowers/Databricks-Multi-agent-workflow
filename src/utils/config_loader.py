import yaml
import os
import re
import logging
from typing import Any, Dict
from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv

# Load .env file at the very beginning to populate os.environ
load_dotenv()

# Configure logging to stdout for Databricks App Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("config_loader")

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Loads configuration from a YAML file.
    """
    # Prioritize root config, then src
    root_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config_path)
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_path)
    
    abs_path = None
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
        logger.warning(f"Configuration file {config_path} not found. Relying on environment variables.")
        return {}
        
    with open(abs_path, 'r') as f:
        config = yaml.safe_load(f)
    
    logger.info(f"Loaded config from {abs_path}")
    return config

# Global config instance
CONFIG = load_config()

_client = None

def get_ws_client():
    """Returns a memoized Databricks WorkspaceClient instance using environment credentials."""
    global _client
    if _client is None:
        # The SDK automatically uses DATABRICKS_HOST and DATABRICKS_TOKEN from os.environ
        _client = WorkspaceClient()
    return _client
