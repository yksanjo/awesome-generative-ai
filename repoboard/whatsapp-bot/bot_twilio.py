"""
RepoBoard WhatsApp Bot using Twilio
Official, reliable WhatsApp integration.
"""

import os
import sys
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

# Configuration
API_BASE_URL = os.getenv("REPOBOARD_API_URL", "http://localhost:8000")
app = Flask(__name__)


def format_board_message(board_data: dict) -> str:
    """Format board data for WhatsApp."""
    board = board_data['board']
    repos = board_data['repos']
    
    message = f"*{board['name']}*\n\n"
    message += f"{board['description']}\n\n"
    message += f"*{board['repo_count']} repositories:*\n\n"
    
    for i, item in enumerate(repos[:5], 1):
        repo = item['repo']
        summary = item.get('summary')
        
        message += f"{i}. *{repo['full_name']}*\n"
        if summary:
            message += f"   {summary['summary'][:60]}...\n"
        message += f"   ⭐ {repo['stars']} stars\n"
        message += f"   {repo['url']}\n\n"
    
    return message


def handle_message(message: str) -> str:
    """Handle incoming WhatsApp messages."""
    message = message.strip().lower()
    
    if message == "/start" or message == "start":
        return """🔍 *Welcome to RepoBoard Bot!*

Discover curated GitHub repositories.

*Commands:*
• *boards* - List all boards
• *search <query>* - Search repos
• *trending* - Get trending repos
• *help* - Show commands"""
    
    elif message == "/help" or message == "help":
        return """*RepoBoard Commands:*

• *boards* - List all curated boards
• *search <query>* - Search repositories
• *trending* - Get trending repos
• *help* - Show this help"""
    
    elif message == "/boards" or message == "boards":
        try:
            response = requests.get(f"{API_BASE_URL}/boards?limit=5")
            boards = response.json()
            
            if not boards:
                return "No boards found."
            
            msg = "*📊 Curated Boards:*\n\n"
            for board in boards:
                msg += f"• *{board['name']}*\n"
                msg += f"  {board['description'][:50]}...\n"
                msg += f"  {board['repo_count']} repos\n\n"
            
            return msg
        except Exception as e:
            return f"Error: {str(e)}"
    
    elif message.startswith("/search ") or message.startswith("search "):
        query = message.split(" ", 1)[1] if " " in message else ""
        if not query:
            return "Usage: *search <query>*"
        
        try:
            response = requests.get(f"{API_BASE_URL}/search", params={"q": query, "limit": 5})
            repos = response.json()
            
            if not repos:
                return f"No repositories found for '{query}'"
            
            msg = f"*🔍 Results for '{query}':*\n\n"
            for i, item in enumerate(repos, 1):
                repo = item['repo']
                msg += f"{i}. *{repo['full_name']}*\n"
                msg += f"   ⭐ {repo['stars']} stars\n"
                msg += f"   {repo['url']}\n\n"
            
            return msg
        except Exception as e:
            return f"Error: {str(e)}"
    
    elif message == "/trending" or message == "trending":
        try:
            response = requests.get(f"{API_BASE_URL}/repos?min_stars=100&limit=5")
            repos = response.json()
            
            if not repos:
                return "No trending repositories found"
            
            msg = "*🔥 Trending:*\n\n"
            for i, item in enumerate(repos, 1):
                repo = item['repo']
                msg += f"{i}. *{repo['full_name']}*\n"
                msg += f"   ⭐ {repo['stars']} stars\n\n"
            
            return msg
        except Exception as e:
            return f"Error: {str(e)}"
    
    else:
        return "Unknown command. Send *help* for commands."


@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """Twilio webhook for WhatsApp messages."""
    incoming_message = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "")
    
    # Handle the message
    response_text = handle_message(incoming_message)
    
    # Create Twilio response
    resp = MessagingResponse()
    resp.message(response_text)
    
    return str(resp)


@app.route("/", methods=["GET"])
def health():
    """Health check endpoint."""
    return "RepoBoard WhatsApp Bot is running!"


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

