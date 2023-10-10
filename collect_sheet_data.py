import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json

def gsheet_api_check(SCOPES):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def pull_sheet_data(SCOPES, SPREADSHEET_ID, DATA_TO_PULL):
    creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=DATA_TO_PULL).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print("COMPLETE: Data copied")
        return values


def convert_to_json(data):
    json_data = [dict(zip(data[0], row)) for row in data[1:]]
    with open('data.json', 'w') as outfile:
        json.dump(json_data, outfile)
    return json_data


def import_csv():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '1ZJk27bxI6H-dGHsxXl8hHBwDnkH5FHEdRq90nvB-CEo'
    DATA_TO_PULL = 'Form Responses 2'
    data = convert_to_json(pull_sheet_data(SCOPES, SPREADSHEET_ID, DATA_TO_PULL))
    return data

