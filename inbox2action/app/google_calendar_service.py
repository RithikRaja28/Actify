from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def create_calendar_event(action_items):
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/calendar"])
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": action_items.get("title", "No Title"),
        "description": action_items.get("description", ""),
        "start": {
            "dateTime": action_items.get("start"),
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": action_items.get("end"),
            "timeZone": "Asia/Kolkata"
        },
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    return event.get("id")
