from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def create_calendar_event(action_items):
    creds = Credentials.from_authorized_user_file(
        "token.json", ["https://www.googleapis.com/auth/calendar"]
    )
    service = build("calendar", "v3", credentials=creds)

    start = action_items.get("start")
    end = action_items.get("end")

    if start and end:
        event_body = {
            "summary": action_items.get("title", "No Title"),
            "description": action_items.get("description", ""),
            "start": {"dateTime": start, "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end, "timeZone": "Asia/Kolkata"},
        }
    else:
        # fallback: use today for full-day event
        today = datetime.now().strftime("%Y-%m-%d")
        event_body = {
            "summary": action_items.get("title", "No Title"),
            "description": action_items.get("description", ""),
            "start": {"date": today},
            "end": {"date": today},
        }

    event = service.events().insert(calendarId="primary", body=event_body).execute()
    print(f"✅ Event created: {event.get('htmlLink')}")
    return event.get("id")
