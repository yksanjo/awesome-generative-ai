"""
RepoBoard Telegram Bot
Integrates RepoBoard with Telegram for easy access to curated boards.
"""

import os
import sys
from typing import Optional
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
import requests
from shared.config import settings
from conversation import ConversationHandler

# Bot configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_BASE_URL = os.getenv("REPOBOARD_API_URL", "http://localhost:8000")

# Initialize conversation handler
conversation_handler = ConversationHandler()


def escape_markdown(text: str) -> str:
    """Escape special Markdown characters to prevent parsing errors."""
    if not text:
        return ""
    # Escape special Markdown characters (must escape backslash first!)
    text = text.replace('\\', '\\\\')  # Escape backslashes first
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


def safe_markdown(text: str, max_length: int = None) -> str:
    """Safely format text for Markdown, escaping special characters."""
    if not text:
        return ""
    if max_length and len(text) > max_length:
        text = text[:max_length] + "..."
    return escape_markdown(text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    welcome_message = """
🔍 *Welcome to RepoBoard Bot!*

Discover curated GitHub repositories organized into boards.

*Commands:*
/boards - List all curated boards
/search <query> - Search repositories
/trending - Get trending repositories
/subscribe <board> - Subscribe to board updates
/myboards - Your subscribed boards
/help - Show all commands

*Quick Search:*
Type `@repoboard_bot <query>` in any chat for instant results!
    """
    try:
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    except Exception:
        # Fallback to plain text if Markdown fails
        await update.message.reply_text(welcome_message.replace('*', '').replace('_', '').replace('`', ''))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = """
*RepoBoard Bot Commands:*

/start - Welcome message
/boards - List all curated boards
/board <name> - View specific board
/search <query> - Search repositories
/trending - Get trending repos
/subscribe <board> - Subscribe to board updates
/unsubscribe <board> - Unsubscribe
/myboards - Your subscribed boards
/help - Show this help message

*Inline Search:*
Type `@repoboard_bot <query>` in any chat for instant results!
    """
    try:
        await update.message.reply_text(help_text, parse_mode='Markdown')
    except Exception:
        # Fallback to plain text if Markdown fails
        await update.message.reply_text(help_text.replace('*', '').replace('_', '').replace('`', ''))


async def list_boards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /boards command - list all boards."""
    try:
        response = requests.get(f"{API_BASE_URL}/boards?limit=20", timeout=10)
        response.raise_for_status()
        boards = response.json()
        
        if not boards:
            await update.message.reply_text("📭 No boards found. Generate boards first!")
            return
        
        message = "*📊 Curated Boards:*\n\n"
        keyboard = []
        
        for board in boards[:10]:  # Show first 10
            board_name = safe_markdown(board.get('name', 'Unknown'))
            board_desc = safe_markdown(board.get('description', 'No description'), 50)
            message += f"• *{board_name}*\n"
            message += f"  {board_desc}...\n"
            message += f"  {board.get('repo_count', 0)} repositories\n\n"
            
            keyboard.append([
                InlineKeyboardButton(
                    f"📋 {board.get('name', 'Unknown')}",
                    callback_data=f"board_{board.get('id', 0)}"
                )
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await update.message.reply_text(
                message,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        except Exception as e:
            if "Can't parse entities" in str(e) or "can't find end" in str(e):
                # Fallback to plain text if Markdown fails
                message_plain = message.replace('*', '').replace('_', '').replace('`', '')
                await update.message.reply_text(
                    message_plain,
                    reply_markup=reply_markup
                )
            else:
                raise
    except requests.exceptions.ConnectionError:
            try:
                await update.message.reply_text(
                    f"❌ *Connection Error*\n\n"
                    f"Could not connect to the API at `{API_BASE_URL}`\n\n"
                    f"Make sure the API is running:\n"
                    f"```bash\n./START_API.sh\n```",
                    parse_mode='Markdown'
                )
            except Exception:
                await update.message.reply_text(
                    f"❌ Connection Error\n\n"
                    f"Could not connect to the API at {API_BASE_URL}\n\n"
                    f"Make sure the API is running: ./START_API.sh"
                )
    except requests.exceptions.Timeout:
        await update.message.reply_text("⏱️ Request timed out. Please try again.")
    except Exception as e:
            try:
                await update.message.reply_text(
                    f"❌ Error fetching boards: {str(e)}\n\n"
                    f"API URL: `{API_BASE_URL}`",
                    parse_mode='Markdown'
                )
            except Exception:
                await update.message.reply_text(
                    f"❌ Error fetching boards: {str(e)}\n\n"
                    f"API URL: {API_BASE_URL}"
                )


async def show_board(update: Update, context: ContextTypes.DEFAULT_TYPE, board_id: int):
    """Show a specific board with its repositories."""
    try:
        response = requests.get(f"{API_BASE_URL}/boards/{board_id}", timeout=10)
        response.raise_for_status()
        board_data = response.json()
        
        board = board_data.get('board', {})
        repos = board_data.get('repos', [])
        
        if not board:
            raise ValueError("Board not found")
        
        board_name = safe_markdown(board.get('name', 'Unknown'))
        board_desc = safe_markdown(board.get('description', 'No description'))
        message = f"*{board_name}*\n\n"
        message += f"{board_desc}\n\n"
        message += f"*{board.get('repo_count', 0)} repositories:*\n\n"
        
        if repos:
            for i, item in enumerate(repos[:10], 1):  # Show first 10
                repo = item.get('repo', {})
                summary = item.get('summary')
                
                repo_name = safe_markdown(repo.get('full_name', 'Unknown'))
                message += f"{i}. *{repo_name}*\n"
                if summary and summary.get('summary'):
                    summary_text = safe_markdown(summary['summary'], 80)
                    message += f"   {summary_text}...\n"
                message += f"   ⭐ {repo.get('stars', 0)} stars\n"
                repo_url = repo.get('url', '')
                message += f"   🔗 {repo_url}\n\n"
            
            if len(repos) > 10:
                message += f"... and {len(repos) - 10} more repositories"
        else:
            message += "No repositories in this board yet."
        
        keyboard = [[
            InlineKeyboardButton("🌐 View on Web", url=f"{API_BASE_URL.replace('/api', '')}/boards/{board_id}")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Use callback query if it's a button click, otherwise send new message
        if update.callback_query:
            try:
                await update.callback_query.edit_message_text(
                    message,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            except Exception as e:
                if "Can't parse entities" in str(e) or "can't find end" in str(e):
                    # Fallback to plain text if Markdown fails
                    message_plain = message.replace('*', '').replace('_', '').replace('`', '')
                    await update.callback_query.edit_message_text(
                        message_plain,
                        reply_markup=reply_markup
                    )
                else:
                    raise
        else:
            await update.message.reply_text(
                message,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
    except requests.exceptions.ConnectionError:
        error_msg = f"❌ Could not connect to API at `{API_BASE_URL}`"
        if update.callback_query:
            await update.callback_query.answer(error_msg, show_alert=True)
        else:
            try:
                await update.message.reply_text(error_msg, parse_mode='Markdown')
            except Exception:
                await update.message.reply_text(error_msg.replace('*', '').replace('_', '').replace('`', ''))
    except requests.exceptions.HTTPError as e:
        error_msg = f"❌ Board not found (Error {e.response.status_code})"
        if update.callback_query:
            await update.callback_query.answer(error_msg, show_alert=True)
        else:
            await update.message.reply_text(error_msg)
    except Exception as e:
        error_msg = f"❌ Error fetching board: {str(e)}"
        if update.callback_query:
            await update.callback_query.answer(error_msg, show_alert=True)
        else:
            await update.message.reply_text(error_msg)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith("board_"):
        board_id = int(data.split("_")[1])
        await show_board(update, context, board_id)


async def search_repos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /search command."""
    query_text = ' '.join(context.args) if context.args else None
    
    if not query_text:
        await update.message.reply_text(
            "Usage: /search <query>\n\n"
            "Examples:\n"
            "• /search python\n"
            "• /search machine learning\n"
            "• /search web framework\n"
            "• /search react"
        )
        return
    
    try:
        # Show "Searching..." message
        searching_msg = await update.message.reply_text(f"🔍 Searching for '{query_text}'...")
        
        response = requests.get(f"{API_BASE_URL}/search", params={"q": query_text, "limit": 10}, timeout=15)
        response.raise_for_status()
        repos = response.json()
        
        # Delete searching message
        try:
            await searching_msg.delete()
        except:
            pass  # Ignore if message already deleted
        
        if not repos:
            await update.message.reply_text(
                f"❌ No repositories found for '{query_text}'\n\n"
                "Try a different search term or check spelling."
            )
            return
        
        query_escaped = safe_markdown(query_text)
        message = f"*🔍 Search Results for '{query_escaped}':*\n\n"
        
        for i, item in enumerate(repos[:5], 1):  # Show first 5
            repo = item.get('repo', {})
            summary = item.get('summary')
            
            repo_name = safe_markdown(repo.get('full_name', 'Unknown'))
            message += f"{i}. *{repo_name}*\n"
            if summary and summary.get('summary'):
                summary_text = safe_markdown(summary['summary'], 60)
                message += f"   {summary_text}...\n"
            message += f"   ⭐ {repo.get('stars', 0)} stars"
            if summary and summary.get('category'):
                category = safe_markdown(summary['category'])
                message += f" | {category}"
            message += f"\n   🔗 {repo.get('url', '')}\n\n"
        
        if len(repos) > 5:
            message += f"*... and {len(repos) - 5} more results*"
        
        try:
            await update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)
        except Exception as e:
            if "Can't parse entities" in str(e) or "can't find end" in str(e):
                # Fallback to plain text if Markdown fails
                message_plain = message.replace('*', '').replace('_', '').replace('`', '')
                await update.message.reply_text(message_plain, disable_web_page_preview=True)
            else:
                raise
    except requests.exceptions.ConnectionError:
            try:
                await update.message.reply_text(
                    f"❌ *Connection Error*\n\n"
                    f"Could not connect to the API at `{API_BASE_URL}`\n\n"
                    f"Make sure the API is running:\n"
                    f"```bash\n./START_API.sh\n```",
                    parse_mode='Markdown'
                )
            except Exception:
                await update.message.reply_text(
                    f"❌ Connection Error\n\n"
                    f"Could not connect to the API at {API_BASE_URL}\n\n"
                    f"Make sure the API is running: ./START_API.sh"
                )
    except requests.exceptions.Timeout:
        await update.message.reply_text("⏱️ Search timed out. Please try again with a shorter query.")
    except Exception as e:
            try:
                await update.message.reply_text(
                    f"❌ Error searching: {str(e)}\n\n"
                    f"API URL: `{API_BASE_URL}`",
                    parse_mode='Markdown'
                )
            except Exception:
                await update.message.reply_text(
                    f"❌ Error searching: {str(e)}\n\n"
                    f"API URL: {API_BASE_URL}"
                )


async def trending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /trending command."""
    try:
        # Show "Loading..." message
        loading_msg = await update.message.reply_text("🔥 Loading trending repositories...")
        
        response = requests.get(f"{API_BASE_URL}/repos?min_stars=100&limit=10", timeout=15)
        response.raise_for_status()
        repos = response.json()
        
        # Delete loading message
        try:
            await loading_msg.delete()
        except:
            pass  # Ignore if message already deleted
        
        if not repos:
            await update.message.reply_text("📭 No trending repositories found\n\nTry ingesting repos first!")
            return
        
        message = "*🔥 Trending Repositories:*\n\n"
        
        for i, item in enumerate(repos[:10], 1):
            repo = item.get('repo', {})
            summary = item.get('summary')
            
            repo_name = safe_markdown(repo.get('full_name', 'Unknown'))
            message += f"{i}. *{repo_name}*\n"
            if summary and summary.get('summary'):
                category = summary.get('category', '')
                summary_text = safe_markdown(summary['summary'], 50)
                if category:
                    category_escaped = safe_markdown(category)
                    message += f"   {category_escaped} - {summary_text}...\n"
                else:
                    message += f"   {summary_text}...\n"
            message += f"   ⭐ {repo.get('stars', 0)} stars\n"
            message += f"   🔗 {repo.get('url', '')}\n\n"
        
        try:
            await update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)
        except Exception as e:
            if "Can't parse entities" in str(e) or "can't find end" in str(e):
                # Fallback to plain text if Markdown fails
                message_plain = message.replace('*', '').replace('_', '').replace('`', '')
                await update.message.reply_text(message_plain, disable_web_page_preview=True)
            else:
                raise
    except requests.exceptions.ConnectionError:
            try:
                await update.message.reply_text(
                    f"❌ *Connection Error*\n\n"
                    f"Could not connect to the API at `{API_BASE_URL}`\n\n"
                    f"Make sure the API is running:\n"
                    f"```bash\n./START_API.sh\n```",
                    parse_mode='Markdown'
                )
            except Exception:
                await update.message.reply_text(
                    f"❌ Connection Error\n\n"
                    f"Could not connect to the API at {API_BASE_URL}\n\n"
                    f"Make sure the API is running: ./START_API.sh"
                )
    except requests.exceptions.Timeout:
        await update.message.reply_text("⏱️ Request timed out. Please try again.")
    except Exception as e:
            try:
                await update.message.reply_text(
                    f"❌ Error fetching trending: {str(e)}\n\n"
                    f"API URL: `{API_BASE_URL}`",
                    parse_mode='Markdown'
                )
            except Exception:
                await update.message.reply_text(
                    f"❌ Error fetching trending: {str(e)}\n\n"
                    f"API URL: {API_BASE_URL}"
                )


async def handle_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle natural language conversations."""
    user_message = update.message.text
    user_id = update.message.from_user.id
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Handle conversation
    response_text, action_data = conversation_handler.handle_conversation(user_message, user_id)
    
    if action_data:
        # Execute action based on intent
        intent = action_data.get("intent")
        
        if intent == "search":
            query = action_data.get("query", user_message)
            # Update context args with the query
            context.args = query.split()
            await search_repos(update, context)
        elif intent == "trending":
            await trending(update, context)
        elif intent == "boards":
            await list_boards(update, context)
        elif intent == "help":
            await help_command(update, context)
        else:
            # Fallback to conversational response
            if response_text:
                await update.message.reply_text(response_text)
    else:
        # Pure conversation
        if response_text:
            # Don't use Markdown for LLM responses as they may contain special characters
            await update.message.reply_text(response_text)
        else:
            await update.message.reply_text(
                "I can help you search for repositories, show trending repos, or browse curated boards!\n\n"
                "Try saying:\n"
                "• \"Find Python libraries\"\n"
                "• \"Show me trending repos\"\n"
                "• \"What boards do you have?\"\n\n"
                "Or use commands: /search, /trending, /boards"
            )


def main():
    """Start the bot."""
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set!")
        print("Get a token from @BotFather on Telegram")
        return
    
    # Create application with error handling
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("boards", list_boards))
        application.add_handler(CommandHandler("search", search_repos))
        application.add_handler(CommandHandler("trending", trending))
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Add conversation handler (handles all text messages)
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_conversation))
        
        # Add error handler
        async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
            """Handle errors."""
            import logging
            logger = logging.getLogger(__name__)
            error_str = str(context.error)
            logger.error(f"Exception while handling an update: {error_str}")
            
            # Check if it's a conflict error
            if "Conflict" in error_str:
                print("\n❌ CONFLICT ERROR: Another bot instance is running!")
                print("   Run: ./KILL_ALL_BOTS.sh to stop all instances")
                print("   Or: pkill -9 -f 'bot.py'")
            
            # Check if it's a Markdown parsing error
            elif "Can't parse entities" in error_str or "can't find end of the entity" in error_str:
                print(f"\n⚠️  Markdown parsing error: {error_str}")
                # Try to send a plain text message instead
                if update and hasattr(update, 'effective_chat'):
                    try:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="⚠️ Sorry, there was an error formatting the message. Please try again or use a different search term."
                        )
                    except:
                        pass  # Ignore if we can't send error message
        
        application.add_error_handler(error_handler)
        
        # Start bot with drop_pending_updates to avoid conflicts
        print("RepoBoard Telegram Bot started!")
        print("   (Dropping pending updates to avoid conflicts...)")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True  # This helps avoid conflicts
        )
    except Exception as e:
        if "Conflict" in str(e):
            print("\n❌ CONFLICT ERROR: Another bot instance is running!")
            print("   Run: ./KILL_ALL_BOTS.sh to stop all instances")
            print("   Or: pkill -9 -f 'bot.py'")
        else:
            print(f"\n❌ Error starting bot: {e}")
        raise


if __name__ == "__main__":
    main()

