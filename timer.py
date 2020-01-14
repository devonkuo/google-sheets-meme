from __future__ import print_function
import pickle
import os.path
import threading
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '18RlViaalQ-n0H_euMNSSHE5phQ6sH6CVtpKOJYK4KRA'

# The cell to modify in the spreadsheet.
CELL='back_end!A11'

def main():
    """Write elapsed time in seconds to a Google Sheet spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    def startTimer(count):
        body = {
            'values': [[count]]
        }
        print('tick: {}'.format(body))
        threading.Timer(1, startTimer, [count + 1]).start()

        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=CELL,
            valueInputOption='RAW', body=body).execute()

    startTimer(0)

if __name__ == '__main__':
    main()
