"""
FastAPI-based Design Thinking Coach Chatbot
Main application entry point with Azure OpenAI integration
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Optional, Dict, Any
import logging
from datetime import datetime

# Add parent directory to Python path to access root chatbot module
sys.path.append(str(Path(__file__).parent.parent))

from chatbot.core import DesignThinkingCoach
from chatbot.config_manager import ConfigManager
from chatbot.utils import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Design Thinking Coach API",
    description="AI-powered Design Thinking Coach using Azure OpenAI",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Config Manager
config_manager = ConfigManager()

# Initialize the Design Thinking Coach
coach = DesignThinkingCoach()

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    usage: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Design Thinking Coach API started successfully!")
    logger.info("📡 Azure OpenAI connection established")
    logger.info("🌐 Frontend will be served from /")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the main frontend HTML"""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    if frontend_path.exists():
        return FileResponse(frontend_path)
    else:
        return HTMLResponse("""
        <html>
            <head><title>Design Thinking Coach</title></head>
            <body>
                <h1>🤖 Design Thinking Coach API</h1>
                <p>Backend is running! Frontend not found at: {}</p>
                <p>API Documentation: <a href="/docs">/docs</a></p>
            </body>
        </html>
        """.format(frontend_path))

# Mount static files if they exist
frontend_static = Path(__file__).parent.parent / "frontend"
if frontend_static.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_static)), name="static")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """
    Main chat endpoint for Design Thinking coaching
    
    Args:
        chat_message: User message and optional session ID
        
    Returns:
        ChatResponse with bot reply, session info, and usage statistics
    """
    try:
        logger.info(f"💬 Received message: '{chat_message.message[:50]}...' from session: {chat_message.session_id}")
        
        # Use the correct method name and await the async call
        response = await coach.process_message(
            message=chat_message.message,
            session_id=chat_message.session_id or f"session-{datetime.now().timestamp()}"
        )
        
        logger.info(f"✅ Generated response for session: {response.get('session_id')}")
        
        return ChatResponse(
            reply=response["reply"],
            session_id=response["session_id"],
            usage=response.get("usage"),
            error=None
        )
        
    except Exception as e:
        logger.error(f"❌ Chat endpoint error: {str(e)}")
        return ChatResponse(
            reply="Entschuldigung, es gab einen technischen Fehler. Bitte versuchen Sie es erneut.",
            session_id=chat_message.session_id or "error",
            usage=None,
            error=str(e)
        )

@app.get("/api/sessions")
async def get_sessions():
    """Get all active chat sessions"""
    try:
        sessions = coach.list_sessions()
        return {"sessions": sessions}
    except Exception as e:
        logger.error(f"❌ Sessions endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get specific chat session history"""
    try:
        session = coach.sessions.get(session_id, [])
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"session_id": session_id, "messages": session}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Session detail error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/sessions/{session_id}")
async def reset_session(session_id: str):
    """Reset/clear a specific chat session"""
    try:
        coach.clear_session(session_id)
        return {"message": f"Session {session_id} reset successfully"}
    except Exception as e:
        logger.error(f"❌ Session reset error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "azure_openai": "connected" if coach.client else "disconnected"
    }

@app.get("/api/config")
async def get_config():
    """Get current configuration (without sensitive data)"""
    try:
        config = {
            "application": config_manager.get_config("application"),
            "framework": config_manager.get_config("framework"),
            "model": {
                "deployment_name": config_manager.get_model_config().get("deployment_name"),
                "temperature": config_manager.get_model_config().get("temperature"),
                "max_tokens": config_manager.get_model_config().get("max_tokens"),
                "mock_responses": config_manager.get_model_config().get("mock_responses")
            },
            "prompts": {
                "system_prompt_length": len(config_manager.get_prompt_config().get("system_prompt", "")),
                "examples_length": len(config_manager.get_prompt_config().get("examples", ""))
            }
        }
        return {"config": config}
    except Exception as e:
        logger.error(f"❌ Config endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/config/reload")
async def reload_config():
    """Reload configuration from master config file"""
    try:
        config_manager.reload_config()
        coach.reload_config()
        coach.prompt_engine.reload_prompts()
        logger.info("🔄 Configuration reloaded successfully")
        return {"status": "success", "message": "Configuration reloaded"}
    except Exception as e:
        logger.error(f"❌ Config reload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Get server config from config manager
    server_config = config_manager.get_server_config()
    
    # For development - run with: python main.py
    uvicorn.run(
        "main:app",
        host=server_config.get("host", "0.0.0.0"),
        port=server_config.get("port", 8000),
        reload=server_config.get("reload", True),
        log_level=server_config.get("log_level", "info")
    )
