from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class Gmail:
    def __init__(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            self.service = build('gmail', 'v1', credentials=creds)

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')


    def read_mail_label(self, label):
        results = self.service.users().messages().list(userId='me', q='label:' + label).execute()
        if 'messages' in results:
            for message in results['messages']:
                self.get_mail_payload(message["id"])

    def get_mail_payload(self, message_id):
        message = self.service.users().messages().get(userId='me', id=message_id).execute()

        # Extract the content of the message from the payload field
        payload = message['payload']
        if 'parts' in payload:
            # If the message contains multiple parts, concatenate them into a single string
            parts = payload['parts']
            body = ''.join(part['body']['data'] for part in parts)
        else:
            # If the message contains a single part, extract the data directly
            body = payload['body']['data']

        message_content = base64.urlsafe_b64decode(body).decode('utf-8')
        pprint(message_content)

if __name__ == '__main__':
    gmail = Gmail()
    gmail.read_mail_label("Morning Brew")
