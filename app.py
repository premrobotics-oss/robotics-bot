from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from google_sheets import get_gspread_client
import os

app = Flask(__name__)

# Telegram Bot Token (set this as an environment variable in Render)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = Bot(token=TOKEN)

# Dispatcher setup
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# Google Sheet Setup
SHEET_NAME = 'Robotics Class Log'  # Change if your sheet name differs

def start(update, context):
    update.message.reply_text("Hello! Use /status to check today's class logs.")

def status(update, context):
    try:
        client = get_gspread_client()
        sheet = client.open(SHEET_NAME).sheet1
        data = sheet.get_all_records()
        if not data:
            update.message.reply_text("No records found.")
            return
        latest = data[-1]
        msg = f"📅 Date: {latest['Date']}\n👨‍🏫 Trainer: {latest['Trainer']}\n📚 Theory: {latest['Theory Duration']} min\n🔧 Lab: {latest['Lab Duration']} min"
        update.message.reply_text(msg)
    except Exception as e:
        update.message.reply_text("Error accessing data.")
        print(f"Error: {e}")

# Add command handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("status", status))

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route('/')
def index():
    return "Bot is running."

if __name__ == '__main__':
    app.run(debug=True)
