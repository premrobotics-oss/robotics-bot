from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your bot.")

# Add more command handlers if needed
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Help text goes here")

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    # app.add_handler(CommandHandler("help", help_command))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
