"""
Conversational AI handler for RepoBoard Telegram Bot.
Uses LLM to understand natural language and respond conversationally.
"""

import os
import sys
from typing import Optional, Dict, Any
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Import LLM client
import importlib.util
llm_client_path = parent_dir / "llm-service" / "llm_client.py"
spec = importlib.util.spec_from_file_location("llm_client", llm_client_path)
llm_client_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(llm_client_module)
LLMClient = llm_client_module.LLMClient

import requests

API_BASE_URL = os.getenv("REPOBOARD_API_URL", "http://localhost:8000")


class ConversationHandler:
    """Handles natural language conversations with users."""
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.conversation_history: Dict[int, list] = {}  # user_id -> messages
    
    def get_user_history(self, user_id: int) -> list:
        """Get conversation history for a user."""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        return self.conversation_history[user_id]
    
    def add_to_history(self, user_id: int, role: str, content: str):
        """Add message to conversation history."""
        history = self.get_user_history(user_id)
        history.append({"role": role, "content": content})
        # Keep only last 10 messages to avoid token limits
        if len(history) > 10:
            history.pop(0)
    
    def understand_intent(self, user_message: str, user_id: int) -> Dict[str, Any]:
        """Use LLM to understand user intent and extract information."""
        prompt = f"""You are a helpful assistant for RepoBoard, a GitHub repository curation tool.

User message: "{user_message}"

Analyze the user's intent and extract information. Respond in JSON format:
{{
    "intent": "search|trending|boards|help|chat",
    "query": "extracted search query if intent is search",
    "category": "category filter if mentioned",
    "language": "programming language if mentioned",
    "response_type": "action|conversation"
}}

Intents:
- "search": User wants to search for repositories
- "trending": User wants trending repositories
- "boards": User wants to see curated boards
- "help": User needs help
- "chat": General conversation

Examples:
- "find python libraries" -> {{"intent": "search", "query": "python libraries"}}
- "show me trending repos" -> {{"intent": "trending"}}
- "what boards do you have?" -> {{"intent": "boards"}}
- "hello" -> {{"intent": "chat", "response_type": "conversation"}}
"""
        
        try:
            response = self.llm_client._call_llm(prompt, "You are a helpful assistant that analyzes user intent.")
            # Parse JSON from response
            import json
            import re
            json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: simple keyword matching
                return self._fallback_intent(user_message)
        except Exception as e:
            print(f"Error understanding intent: {e}")
            return self._fallback_intent(user_message)
    
    def _fallback_intent(self, message: str) -> Dict[str, Any]:
        """Fallback intent detection using keywords."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["search", "find", "look for", "show me"]):
            return {"intent": "search", "query": message, "response_type": "action"}
        elif any(word in message_lower for word in ["trending", "popular", "hot"]):
            return {"intent": "trending", "response_type": "action"}
        elif any(word in message_lower for word in ["board", "curated", "collection"]):
            return {"intent": "boards", "response_type": "action"}
        elif any(word in message_lower for word in ["help", "how", "what can"]):
            return {"intent": "help", "response_type": "action"}
        else:
            return {"intent": "chat", "response_type": "conversation"}
    
    def generate_conversational_response(self, user_message: str, user_id: int, context: Optional[Dict] = None) -> str:
        """Generate a conversational response using LLM."""
        history = self.get_user_history(user_id)
        
        # Build conversation context
        system_prompt = """You are RepoBoard Bot, a friendly assistant that helps users discover GitHub repositories.

You can:
- Search for repositories
- Show trending repositories
- Display curated boards
- Have friendly conversations

Be helpful, concise, and friendly. When users ask about repos, offer to search or show trending ones."""
        
        # Build messages for LLM
        messages = [{"role": "system", "content": system_prompt}]
        for msg in history[-5:]:  # Last 5 messages for context
            messages.append(msg)
        messages.append({"role": "user", "content": user_message})
        
        # Add context if available
        if context:
            context_str = f"\n\nContext: {context}"
            messages[-1]["content"] += context_str
        
        try:
            response = self.llm_client._call_llm(
                "\n".join([f"{m['role']}: {m['content']}" for m in messages]),
                system_prompt
            )
            
            # Add to history
            self.add_to_history(user_id, "user", user_message)
            self.add_to_history(user_id, "assistant", response)
            
            return response
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm having trouble understanding. Try using commands like /search or /trending!"
    
    def handle_conversation(self, user_message: str, user_id: int) -> tuple[str, Optional[Dict]]:
        """
        Handle conversational message.
        Returns: (response_text, action_data)
        action_data is None for pure conversation, or dict with action info
        """
        # Understand intent
        intent = self.understand_intent(user_message, user_id)
        
        if intent.get("response_type") == "action":
            # Return action data for command handler
            return None, intent
        else:
            # Generate conversational response
            response = self.generate_conversational_response(user_message, user_id)
            return response, None

