import yaml
import os
from typing import Any, Dict

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Loads configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file.
        
    Returns:
        A dictionary containing the configuration.
    """
    # Try to find the config file relative to the project root
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    abs_path = os.path.join(root_dir, config_path)
    
    if not os.path.exists(abs_path):
        # Fallback to local path
        abs_path = config_path
        
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Configuration file not found at {abs_path}")
        
    with open(abs_path, 'r') as f:
        return yaml.safe_load(f)

# Global config instance
CONFIG = load_config()
