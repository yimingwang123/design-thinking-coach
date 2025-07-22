"""
Design Thinking Coach Core Module
Hauptklasse für die Chat-Logik und Integration mit Azure OpenAI
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

from openai import AzureOpenAI
from dotenv import load_dotenv

from .prompt_engine import PromptEngine
from .utils import save_json, load_json
from .config_manager import ConfigManager

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class DesignThinkingCoach:
    """
    Main class for the Design Thinking Coach chatbot
    Handles chat sessions, prompt management, and Azure OpenAI integration
    """
    
    def __init__(self):
        """
        Initialize the Design Thinking Coach
        """
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_config()
        self.model_config = self.config_manager.get_model_config()
        self.prompt_engine = PromptEngine()
        self.client = self._init_azure_client()
        self.sessions: Dict[str, List[Dict]] = {}
        
        # Create conversations directory if it doesn't exist
        self.conversations_dir = Path("backend/conversations")
        self.conversations_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Design Thinking Coach initialized successfully")
    
    def reload_config(self):
        """Reload configuration from the central config manager"""
        self.config_manager.reload_config()
        self.config = self.config_manager.get_config()
        self.model_config = self.config_manager.get_model_config()
    
    def _init_azure_client(self) -> Optional[AzureOpenAI]:
        """
        Initialize Azure OpenAI client using configuration from the config manager
        """
        # Check if we're in mock mode
        if self.model_config.get("mock_responses", False):
            logger.info("Mock responses enabled - skipping Azure OpenAI client initialization")
            return None
            
        try:
            # Get configuration from model_config (with env var overrides already applied)
            endpoint = self.model_config.get("endpoint_url")
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            
            if not api_key:
                logger.warning("AZURE_OPENAI_API_KEY environment variable is not set")
                return None
            
            client = AzureOpenAI(
                azure_endpoint=endpoint,
                api_key=api_key,
                api_version=self.model_config.get("api_version", "2025-01-01-preview")
            )
            
            logger.info(f"Azure OpenAI client initialized with endpoint: {endpoint}")
            return client
            
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {e}")
            return None
    
    async def process_message(self, message: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Process a user message and return the coach's response
        
        Args:
            message: User's input message
            session_id: Session identifier for conversation tracking
            
        Returns:
            Dict containing reply, usage info, and metadata
        """
        try:
            # Get or create session
            if session_id not in self.sessions:
                self.sessions[session_id] = []
            
            # Add user message to session
            user_message = {
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            }
            self.sessions[session_id].append(user_message)
            
            # Build conversation context
            messages = self._build_conversation_context(session_id)
            
            # Get model configuration
            model_name = self.model_config.get("deployment_name", "gpt-4.1-mini")
            
            # Check if we're in mock mode or client is not initialized
            if self.model_config.get("mock_responses", False) or self.client is None:
                logger.info("Using mock response mode")
                # Generate a simple mock response
                if "problem" in message.lower():
                    reply = "Das klingt nach einem spannenden Problem! Lassen Sie uns das systematisch angehen. Zuerst sollten wir ein klares **Problem Statement** formulieren."
                elif "idee" in message.lower():
                    reply = "Interessante Idee! Lassen Sie uns diese mit dem **How-Might-We** Ansatz weiterentwickeln."
                else:
                    reply = "Danke für Ihre Nachricht. Als Design Thinking Coach helfe ich Ihnen gerne weiter. Was beschäftigt Sie heute?"
                
                # Simulate usage
                usage = {
                    "prompt_tokens": 150,
                    "completion_tokens": 100,
                    "total_tokens": 250
                }
            else:
                # Call Azure OpenAI
                logger.info(f"Sending request to Azure OpenAI model: {model_name}")
                completion = self.client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    max_tokens=self.model_config.get("max_tokens", 1000),
                    temperature=self.model_config.get("temperature", 0.3),
                    top_p=self.model_config.get("top_p", 0.95),
                    frequency_penalty=self.model_config.get("frequency_penalty", 0),
                    presence_penalty=self.model_config.get("presence_penalty", 0),
                    stream=False
                )
                # Extract response from completion
                reply = completion.choices[0].message.content
                usage = {
                    "prompt_tokens": completion.usage.prompt_tokens,
                    "completion_tokens": completion.usage.completion_tokens,
                    "total_tokens": completion.usage.total_tokens
                } if completion.usage else None
            
            # Variable 'reply' and 'usage' are already set in the previous block
            
            # Add assistant response to session
            assistant_message = {
                "role": "assistant",
                "content": reply,
                "timestamp": datetime.now().isoformat()
            }
            self.sessions[session_id].append(assistant_message)
            
            # Save conversation if enabled
            app_config = self.config_manager.get_config("application")
            if app_config.get("save_conversations", True):
                self._save_conversation(session_id)
            
            logger.info(f"Successfully processed message for session {session_id}")
            
            return {
                "reply": reply,
                "usage": usage,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            raise
    
    def _build_conversation_context(self, session_id: str) -> List[Dict[str, str]]:
        """
        Build the full conversation context including system prompt and history
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of message dictionaries for OpenAI API
        """
        messages = []
        
        # Add system prompt
        system_prompt = self.prompt_engine.get_system_prompt()
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add few-shot examples
        examples = self.prompt_engine.get_few_shot_examples()
        if examples:
            messages.append({
                "role": "system",
                "content": f"Hier sind Beispiele für gute Gespräche:\n\n{examples}"
            })
        
        # Add conversation history (limit to last 10 exchanges to manage token count)
        session_messages = self.sessions.get(session_id, [])
        recent_messages = session_messages[-20:]  # Last 20 messages (10 exchanges)
        
        for msg in recent_messages:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return messages
    
    def _save_conversation(self, session_id: str):
        """Save conversation to file"""
        try:
            file_path = self.conversations_dir / f"{session_id}_{datetime.now().strftime('%Y%m%d')}.json"
            conversation_data = {
                "session_id": session_id,
                "messages": self.sessions[session_id],
                "last_updated": datetime.now().isoformat()
            }
            save_json(str(file_path), conversation_data)
            logger.debug(f"Conversation saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")
    
    def get_public_config(self) -> Dict[str, Any]:
        """Get configuration without sensitive information"""
        return {
            "model": self.config.get("model"),
            "temperature": self.config.get("temperature"),
            "max_tokens": self.config.get("max_tokens"),
            "save_history": self.config.get("save_history", True)
        }
    
    def list_sessions(self) -> List[str]:
        """List all active session IDs"""
        return list(self.sessions.keys())
    
    def clear_session(self, session_id: str):
        """Clear a specific session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Session {session_id} cleared")
    
    def clear_all_sessions(self):
        """Clear all sessions"""
        self.sessions.clear()
        logger.info("All sessions cleared")