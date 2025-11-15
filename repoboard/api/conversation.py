"""
Conversation handler for API chat endpoint.
"""

import os
import sys
from typing import Dict, Any
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


class ConversationHandler:
    """Handles natural language conversations."""
    
    def __init__(self):
        self.llm_client = LLMClient()
    
    def understand_intent(self, user_message: str) -> Dict[str, Any]:
        """Use LLM to understand user intent."""
        prompt = f"""You are a helpful assistant for RepoBoard, a GitHub repository curation tool.

User message: "{user_message}"

Analyze the user's intent and extract information. Respond in JSON format:
{{
    "intent": "search|trending|boards|help|chat",
    "query": "extracted search query if intent is search",
    "category": "category filter if mentioned",
    "language": "programming language if mentioned"
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
"""
        
        try:
            response = self.llm_client._call_llm(prompt, "You are a helpful assistant that analyzes user intent.")
            import json
            import re
            json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._fallback_intent(user_message)
        except Exception as e:
            print(f"Error understanding intent: {e}")
            return self._fallback_intent(user_message)
    
    def _fallback_intent(self, message: str) -> Dict[str, Any]:
        """Fallback intent detection using keywords."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["search", "find", "look for", "show me"]):
            return {"intent": "search", "query": message}
        elif any(word in message_lower for word in ["trending", "popular", "hot"]):
            return {"intent": "trending"}
        elif any(word in message_lower for word in ["board", "curated", "collection"]):
            return {"intent": "boards"}
        else:
            return {"intent": "chat"}
    
    def generate_conversational_response(self, user_message: str) -> str:
        """Generate a conversational response."""
        system_prompt = """You are RepoBoard AI, a friendly assistant that helps users discover GitHub repositories.

You can:
- Search for repositories
- Show trending repositories
- Display curated boards
- Have friendly conversations

Be helpful, concise, and friendly. When users ask about repos, offer to search or show trending ones."""
        
        try:
            response = self.llm_client._call_llm(user_message, system_prompt)
            return response
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I can help you search for repositories, show trending repos, or browse curated boards! Try asking me to find something specific."

