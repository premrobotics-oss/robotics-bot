import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

SHEET_NAME = "Sheet1"  # Make sure this matches your Google Sheet tab name

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("chat-bot-468005-42231e3d5563.json", scope)
    client = gspread.authorize(creds)
    return client.open_by_url("https://docs.google.com/spreadsheets/d/10NblPl0Inj7JG86FSqYjISi7D5op8PQ52tQhGPdtlLA/edit").sheet1

def get_entries_for_trainer(trainer, date=None, week=False):
    sheet = get_sheet()
    data = sheet.get_all_records()
    result = []
    today = datetime.now().date()

    for row in data:
        try:
            row_date = datetime.strptime(row['Date'], "%Y-%m-%d").date()
        except ValueError:
            continue  # Skip rows with invalid date format

        if trainer.lower() in row['Trainer'].lower():
            if date and row_date == date:
                result.append(row)
            elif week and (today - row_date).days < 7:
                result.append(row)
    return result

def get_summary_today():
    sheet = get_sheet()
    data = sheet.get_all_records()
    today = datetime.now().date()
    result = []

    for row in data:
        try:
            row_date = datetime.strptime(row['Date'], "%Y-%m-%d").date()
        except ValueError:
            continue
        if row_date == today:
            result.append(row)
    return result
