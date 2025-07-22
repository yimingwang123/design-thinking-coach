"""
Prompt Engine for Design Thinking Coach
Handles loading and management of system prompts and few-shot examples
"""

from pathlib import Path
from typing import Dict, Any, Optional
import logging

from .config_manager import ConfigManager

logger = logging.getLogger(__name__)

class PromptEngine:
    """
    Manages system prompts and few-shot examples for the Design Thinking Coach
    """
    
    def __init__(self):
        """
        Initialize prompt engine with configuration from ConfigManager
        """
        self.config_manager = ConfigManager()
        self.prompt_config = self.config_manager.get_prompt_config()
        
        # Cache for loaded prompts
        self._system_prompt_cache = None
        self._few_shot_cache = None
        
        logger.info("Prompt Engine initialized")
    
    def get_system_prompt(self) -> str:
        """
        Get the system prompt from configuration
        
        Returns:
            System prompt as string
        """
        if self._system_prompt_cache is None:
            # Reload from config manager to ensure fresh data
            self.prompt_config = self.config_manager.get_prompt_config()
            self._system_prompt_cache = self.prompt_config.get("system_prompt", "")
        
        return self._system_prompt_cache
    
    def get_few_shot_examples(self) -> str:
        """
        Get few-shot examples from configuration
        
        Returns:
            Few-shot examples as string
        """
        if self._few_shot_cache is None:
            # Reload from config manager to ensure fresh data
            self.prompt_config = self.config_manager.get_prompt_config()
            self._few_shot_cache = self.prompt_config.get("examples", "")
        
        return self._few_shot_cache
    
    def _load_prompt_file(self, file_path: str) -> str:
        """
        Load content from a prompt file
        
        Args:
            file_path: Path to the prompt file
            
        Returns:
            File content as string
        """
        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"Prompt file not found: {file_path}")
                return ""
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            logger.debug(f"Loaded prompt from {file_path}")
            return content
            
        except Exception as e:
            logger.error(f"Error loading prompt file {file_path}: {e}")
            return ""
    
    def reload_prompts(self):
        """
        Clear cache and force reload of all prompts from config manager
        """
        self._system_prompt_cache = None
        self._few_shot_cache = None
        
        # Force config manager to reload
        self.config_manager.reload_config()
        self.prompt_config = self.config_manager.get_prompt_config()
        
        logger.info("Prompt cache cleared - prompts will be reloaded on next access")
    
    def get_prompt_info(self) -> Dict[str, Any]:
        """
        Get information about loaded prompts
        
        Returns:
            Dictionary with prompt information and status
        """
        return {
            "system_prompt": {
                "loaded": self._system_prompt_cache is not None,
                "length": len(self._system_prompt_cache or ""),
                "preview": (self._system_prompt_cache or "")[:50] + "..." if self._system_prompt_cache else ""
            },
            "few_shot_examples": {
                "loaded": self._few_shot_cache is not None,
                "length": len(self._few_shot_cache or ""),
                "preview": (self._few_shot_cache or "")[:50] + "..." if self._few_shot_cache else ""
            }
        }