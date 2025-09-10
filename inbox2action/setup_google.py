from google_auth_oauthlib.flow import InstalledAppFlow

# Scope = permissions; this one allows read/write to Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    # Load credentials.json and start OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)  # Opens browser for login
    
    # Save token.json for later use
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    print("✅ Google Calendar token.json created successfully!")

if __name__ == "__main__":
    main()
