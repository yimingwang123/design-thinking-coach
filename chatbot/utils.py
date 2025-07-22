"""
Utility functions for the Design Thinking Coach
Handles file operations, configuration loading, and logging setup
"""

import json
import yaml
import logging
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Load environment variables
load_dotenv()

# Check for mock mode
MOCK_MODE = os.getenv('MOCK_RESPONSES', 'false').lower() in ('true', '1', 'yes')

def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a YAML configuration file
    
    Args:
        file_path: Path to YAML file
        
    Returns:
        Dictionary with configuration data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        yaml.YAMLError: If file is invalid YAML
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in {file_path}: {e}")

def save_yaml(file_path: str, data: Dict[str, Any]):
    """
    Save data to a YAML file
    
    Args:
        file_path: Path to save YAML file
        data: Dictionary to save
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True)

def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a JSON file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary with data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in {file_path}: {e}")
        return {}

def save_json(file_path: str, data: Any, indent: int = 2):
    """
    Save data to a JSON file
    
    Args:
        file_path: Path to save JSON file
        data: Data to save
        indent: JSON indentation
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False, default=str)

def setup_logging(level: str = "INFO", log_file: str = None):
    """
    Setup logging configuration
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
    """
    # Create logs directory if logging to file
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Setup handlers
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=handlers,
        force=True
    )
    
    # Reduce openai library logging
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

def validate_environment() -> Dict[str, Any]:
    """
    Validate required environment variables and configuration
    
    Returns:
        Dictionary with validation results
    """
    import os
    
    validation = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Check required environment variables
    required_env_vars = [
        "AZURE_OPENAI_API_KEY",
        "ENDPOINT_URL",
        "DEPLOYMENT_NAME"
    ]
    
    for var in required_env_vars:
        if not os.getenv(var):
            validation["errors"].append(f"Missing environment variable: {var}")
            validation["valid"] = False
    
    # Check configuration files
    config_files = [
        "backend/config/config.yaml",
        "backend/config/prompts/system.md",
        "backend/config/prompts/examples.md"
    ]
    
    for file_path in config_files:
        if not Path(file_path).exists():
            validation["warnings"].append(f"Configuration file not found: {file_path}")
    
    return validation

def format_conversation_for_export(messages: List[Dict]) -> str:
    """
    Format conversation messages for export (e.g., to markdown)
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        Formatted conversation as string
    """
    formatted = []
    formatted.append(f"# Design Thinking Coach Conversation")
    formatted.append(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    formatted.append("")
    
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        timestamp = msg.get("timestamp", "")
        
        if role == "user":
            formatted.append(f"## 👤 User ({timestamp})")
        elif role == "assistant":
            formatted.append(f"## 🤖 Coach ({timestamp})")
        else:
            formatted.append(f"## 🔧 System ({timestamp})")
        
        formatted.append("")
        formatted.append(content)
        formatted.append("")
        formatted.append("---")
        formatted.append("")
    
    return "\n".join(formatted)

def clean_old_conversations(conversations_dir: str = "conversations", days_to_keep: int = 30):
    """
    Clean up old conversation files
    
    Args:
        conversations_dir: Directory containing conversation files
        days_to_keep: Number of days to keep conversations
    """
    import time
    
    conversations_path = Path(conversations_dir)
    if not conversations_path.exists():
        return
    
    cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
    
    deleted_count = 0
    for file_path in conversations_path.glob("*.json"):
        if file_path.stat().st_mtime < cutoff_time:
            file_path.unlink()
            deleted_count += 1
    
    if deleted_count > 0:
        logging.info(f"Cleaned up {deleted_count} old conversation files")