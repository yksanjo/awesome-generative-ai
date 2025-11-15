"""
RepoBoard WhatsApp Bot
Uses WhatsApp Web API (unofficial) for personal use.
Note: This uses an unofficial API - use at your own risk.
"""

import os
import sys
import asyncio
from typing import Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from whatsapp import WhatsApp
except ImportError:
    print("Installing whatsapp library...")
    os.system("pip install whatsapp-web.py")
    from whatsapp import WhatsApp

import requests
from shared.config import settings

# Configuration
API_BASE_URL = os.getenv("REPOBOARD_API_URL", "http://localhost:8000")
WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE", "")  # Your phone number with country code


class RepoBoardWhatsAppBot:
    """WhatsApp bot for RepoBoard."""
    
    def __init__(self):
        self.api_url = API_BASE_URL
        self.whatsapp = WhatsApp(WHATSAPP_PHONE)
    
    def format_board_message(self, board_data: dict) -> str:
        """Format board data for WhatsApp message."""
        board = board_data['board']
        repos = board_data['repos']
        
        message = f"*{board['name']}*\n\n"
        message += f"{board['description']}\n\n"
        message += f"*{board['repo_count']} repositories:*\n\n"
        
        for i, item in enumerate(repos[:5], 1):  # Show first 5
            repo = item['repo']
            summary = item.get('summary')
            
            message += f"{i}. *{repo['full_name']}*\n"
            if summary:
                message += f"   {summary['summary'][:60]}...\n"
            message += f"   ⭐ {repo['stars']} stars\n"
            message += f"   {repo['url']}\n\n"
        
        if len(repos) > 5:
            message += f"... and {len(repos) - 5} more repositories"
        
        return message
    
    def format_search_results(self, repos: list, query: str) -> str:
        """Format search results for WhatsApp."""
        message = f"*🔍 Search Results for '{query}':*\n\n"
        
        for i, item in enumerate(repos[:5], 1):
            repo = item['repo']
            summary = item.get('summary')
            
            message += f"{i}. *{repo['full_name']}*\n"
            if summary:
                message += f"   {summary['summary'][:60]}...\n"
            message += f"   ⭐ {repo['stars']} stars\n"
            message += f"   {repo['url']}\n\n"
        
        return message
    
    def handle_message(self, message: str, sender: str) -> Optional[str]:
        """Handle incoming WhatsApp messages."""
        message = message.strip().lower()
        
        # Commands
        if message == "/start" or message == "start":
            return """🔍 *Welcome to RepoBoard Bot!*

Discover curated GitHub repositories.

*Commands:*
• *boards* - List all boards
• *search <query>* - Search repos
• *trending* - Get trending repos
• *help* - Show commands

Example: *search machine learning*"""
        
        elif message == "/help" or message == "help":
            return """*RepoBoard Commands:*

• *boards* - List all curated boards
• *board <name>* - View specific board
• *search <query>* - Search repositories
• *trending* - Get trending repos
• *help* - Show this help"""
        
        elif message == "/boards" or message == "boards":
            try:
                response = requests.get(f"{self.api_url}/boards?limit=10")
                boards = response.json()
                
                if not boards:
                    return "No boards found. Generate boards first!"
                
                message = "*📊 Curated Boards:*\n\n"
                for board in boards[:5]:
                    message += f"• *{board['name']}*\n"
                    message += f"  {board['description'][:50]}...\n"
                    message += f"  {board['repo_count']} repos\n\n"
                
                return message
            except Exception as e:
                return f"Error: {str(e)}"
        
        elif message.startswith("/search ") or message.startswith("search "):
            query = message.split(" ", 1)[1] if " " in message else ""
            if not query:
                return "Usage: *search <query>*\nExample: *search machine learning*"
            
            try:
                response = requests.get(f"{self.api_url}/search", params={"q": query, "limit": 5})
                repos = response.json()
                
                if not repos:
                    return f"No repositories found for '{query}'"
                
                return self.format_search_results(repos, query)
            except Exception as e:
                return f"Error: {str(e)}"
        
        elif message == "/trending" or message == "trending":
            try:
                response = requests.get(f"{self.api_url}/repos?min_stars=100&limit=5")
                repos = response.json()
                
                if not repos:
                    return "No trending repositories found"
                
                message = "*🔥 Trending Repositories:*\n\n"
                for i, item in enumerate(repos, 1):
                    repo = item['repo']
                    summary = item.get('summary')
                    
                    message += f"{i}. *{repo['full_name']}*\n"
                    if summary:
                        message += f"   {summary['category']}\n"
                    message += f"   ⭐ {repo['stars']} stars\n"
                    message += f"   {repo['url']}\n\n"
                
                return message
            except Exception as e:
                return f"Error: {str(e)}"
        
        else:
            return "Unknown command. Send *help* for commands."
    
    def send_message(self, to: str, message: str):
        """Send WhatsApp message."""
        try:
            self.whatsapp.send_message(to, message)
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def run(self):
        """Run the bot (polling mode)."""
        print("RepoBoard WhatsApp Bot started!")
        print("Send messages to your WhatsApp number to interact.")
        print("Note: This uses unofficial API - keep your phone connected.")
        
        # For polling, you'd need to implement message checking
        # This is a simplified version
        print("\nBot is running. Check messages manually or implement polling.")


def main():
    """Main function."""
    if not WHATSAPP_PHONE:
        print("Error: WHATSAPP_PHONE not set!")
        print("Set it in .env: WHATSAPP_PHONE=+1234567890")
        return
    
    bot = RepoBoardWhatsAppBot()
    bot.run()


if __name__ == "__main__":
    main()

