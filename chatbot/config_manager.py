"""
Configuration Manager for Design Thinking Coach
Central module for loading and managing application configuration
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from chatbot.utils import load_yaml

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Singleton class for managing configuration across the application
    """
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Load the master configuration file"""
        config_path = os.getenv("CONFIG_PATH", "config/master_config.yaml")
        try:
            self._config = load_yaml(config_path)
            logger.info(f"Master configuration loaded from {config_path}")
        except Exception as e:
            logger.error(f"Failed to load master config: {e}")
            self._config = self._get_fallback_config()
            logger.warning("Using fallback configuration")

    def _get_fallback_config(self) -> Dict[str, Any]:
        """Provide fallback configuration if master config file is missing"""
        return {
            "application": {
                "name": "Design Thinking Coach",
                "version": "1.0.0",
                "save_conversations": True,
                "log_level": "INFO"
            },
            "model": {
                "provider": "azure",
                "deployment_name": "gpt-4.1-mini",
                "api_version": "2025-01-01-preview",
                "temperature": 0.3,
                "max_tokens": 1000,
                "mock_responses": False
            },
            "prompts": {
                "system_prompt": "You are the Design Thinking Coach, an AI assistant specialized in guiding users through the design thinking process.",
                "examples": ""
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8000
            }
        }

    def get_config(self, section: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the configuration or a specific section
        
        Args:
            section: Optional section name to retrieve
            
        Returns:
            Full config dict or section dict
        """
        if section:
            if section in self._config:
                return self._config[section]
            else:
                logger.warning(f"Section '{section}' not found in config, returning empty dict")
                return {}
        return self._config

    def reload_config(self):
        """Force reload of configuration"""
        self._load_config()
        logger.info("Configuration reloaded")

    def get_model_config(self) -> Dict[str, Any]:
        """Get model-specific configuration with environment variable overrides"""
        model_config = self.get_config("model")
        
        # Override with environment variables if present
        if os.getenv("DEPLOYMENT_NAME"):
            model_config["deployment_name"] = os.getenv("DEPLOYMENT_NAME")
            
        if os.getenv("ENDPOINT_URL"):
            model_config["endpoint_url"] = os.getenv("ENDPOINT_URL")
            
        if os.getenv("MOCK_RESPONSES", "").lower() in ("true", "1", "yes"):
            model_config["mock_responses"] = True
            
        return model_config

    def get_prompt_config(self) -> Dict[str, Any]:
        """Get prompt-specific configuration"""
        return self.get_config("prompts")
        
    def get_framework_stages(self) -> list:
        """Get framework stages configuration"""
        return self.get_config("framework").get("stages", [])
        
    def get_server_config(self) -> Dict[str, Any]:
        """Get server configuration with environment variable overrides"""
        server_config = self.get_config("server")
        
        # Override with environment variables if present
        if os.getenv("PORT"):
            server_config["port"] = int(os.getenv("PORT"))
            
        if os.getenv("HOST"):
            server_config["host"] = os.getenv("HOST")
            
        return server_config
