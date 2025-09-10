from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)  # opens browser to login
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    print("✅ token.json created!")

if __name__ == "__main__":
    main()
