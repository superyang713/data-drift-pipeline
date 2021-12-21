#!/usr/bin/env python3

import json
import base64
from email.mime.text import MIMEText

from flask import jsonify
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def email_notification(request):
    data = request.get_json()
    text = data['text']
    to = data['to']
    subject = data["subject"]

    message = create_message(to, subject, text)
    send_message(message)

    return jsonify({"status": "ok"})


def create_message(to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    try:
        message = MIMEText(message_text)
    except AttributeError:
        message = MIMEText(json.dumps(message_text))
    message['to'] = to
    message['from'] = "me"
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    # Build the gmail service client
    service = build(
        'gmail', 'v1',
        credentials=Credentials.from_authorized_user_file('token.json', SCOPES))

    response = service \
        .users() \
        .messages() \
        .send(userId="me", body=message) \
        .execute()
    return response
