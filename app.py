from flask import Flask, request
import telegram
import os
from google_sheets import get_entries_for_trainer, get_summary_today
from datetime import datetime

TOKEN = os.getenv("TOKEN")
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text.strip()

    if text.startswith("/today"):
        name = text[7:].strip()
        entries = get_entries_for_trainer(name, date=datetime.now().date())
        if entries:
            msg = f"📅 Today's sessions by {name}:\n"
            total = 0
            for row in entries:
                msg += f"- {row['Session Type']}: {row['Topic']} ({row['Duration (min)']} min)\n"
                total += int(row['Duration (min)'])
            msg += f"\n🕒 Total: {total} minutes"
        else:
            msg = f"No sessions found today for {name}."
        bot.send_message(chat_id=chat_id, text=msg)

    elif text.startswith("/week"):
        name = text[6:].strip()
        entries = get_entries_for_trainer(name, week=True)
        if entries:
            msg = f"📆 This week's sessions by {name}:\n"
            total = 0
            for row in entries:
                msg += f"{row['Date']} - {row['Session Type']}: {row['Topic']} ({row['Duration (min)']} min)\n"
                total += int(row['Duration (min)'])
            msg += f"\n🕒 Total: {total} minutes"
        else:
            msg = f"No sessions found this week for {name}."
        bot.send_message(chat_id=chat_id, text=msg)

    elif text.startswith("/summary"):
        entries = get_summary_today()
        if entries:
            msg = "📋 Today's Robotics Sessions:\n"
            for row in entries:
                msg += f"{row['Trainer']} – {row['Session Type']} – {row['Topic']} ({row['Duration (min)']} min)\n"
        else:
            msg = "No sessions found for today."
        bot.send_message(chat_id=chat_id, text=msg)

    else:
        bot.send_message(chat_id=chat_id, text="Commands:\n/today John\n/week Alice\n/summary")

    return "ok", 200
