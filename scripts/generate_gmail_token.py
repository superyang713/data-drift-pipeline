"""
Generate a token which can be used for cloud function to send gmails.

Note:
  credential.json can be downloaded from GCP.
  APIs & Services -> credentials
"""
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def generate_gmail_token():
    """
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


if __name__ == '__main__':
    generate_gmail_token()
