import os
import requests
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN environment variable is not set.")
    print("Run: export TELEGRAM_BOT_TOKEN='your-token'")
    exit(1)

bot = telebot.TeleBot(TOKEN)
API_URL = "http://localhost:8000/api/cards"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 *Know-Task-OS Telegram Interface*\n\n"
        "Commands:\n"
        "/tasks - List all active tasks and their statuses\n"
        "/add <title> | <description> - Create a new task for the AI Agents"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['tasks'])
def list_tasks(message):
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            cards = response.json()
            if not cards:
                bot.reply_to(message, "The board is currently empty. 📭")
                return
            
            text = "📋 *Active Tasks:*\n\n"
            for card in cards:
                status_icon = "⏳" if card['status'] == "In Progress" else "🔴" if card['status'] == "Blocked" else "✅" if card['status'] == "Done" else "📌"
                text += f"{status_icon} *{card['title']}*\nStatus: `{card['status']}`\nAgent: `{card.get('agentRole', 'Unassigned')}`\n\n"
            
            bot.reply_to(message, text, parse_mode="Markdown")
        else:
            bot.reply_to(message, f"❌ Failed to fetch tasks from the Dispatcher API. Status: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"❌ API Connection Error: {str(e)}")

@bot.message_handler(commands=['add'])
def add_task(message):
    text = message.text.replace("/add", "").strip()
    if not text:
        bot.reply_to(message, "⚠️ Usage: `/add <title> | <description>`", parse_mode="Markdown")
        return
        
    parts = text.split("|", 1)
    title = parts[0].strip()
    description = parts[1].strip() if len(parts) > 1 else "No description provided."
    
    try:
        response = requests.post(API_URL, json={"title": title, "description": description})
        if response.status_code in [200, 201]:
            bot.reply_to(message, f"✅ Task *{title}* dispatched successfully!\nAgents will start working on it soon.", parse_mode="Markdown")
        else:
            bot.reply_to(message, f"❌ Failed to create task. Status: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"❌ API Connection Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Telegram Bot is running... Polling for updates.")
    bot.polling(none_stop=True)
