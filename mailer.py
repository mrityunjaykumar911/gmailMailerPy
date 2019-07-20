#!/usr/local/bin/python
"""
    Filename:           mailer.py
    Author:             mrityunjaykumar
    Date:               01/02/19
    author_email:       mrkumar@cs.stonybrook.edu
"""
from __future__ import print_function

import base64
import pickle
import os.path
from email.mime.text import MIMEText

from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
from config import SENDER_MAIL_ID, MAIL_TOKEN_PICKLE_LOCATION, INDIVIDUAL_MAIL_ID, HTML_FILE_NAME, \
    MAIL_CREDENTIAL_JSON_LOCATION, MAIL_SUBJECT_NAME

SCOPES = ['https://mail.google.com/']

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text, _subtype="html")
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': (base64.urlsafe_b64encode(message.as_bytes())).decode("utf-8")}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except Exception as error:
      print('An error occurred: %s' % error)


def main_2():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(MAIL_TOKEN_PICKLE_LOCATION):
        with open(MAIL_TOKEN_PICKLE_LOCATION, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                MAIL_CREDENTIAL_JSON_LOCATION, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(MAIL_TOKEN_PICKLE_LOCATION, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # text is hello
    text = ""
    msg_gmail = "EMPTY MESSAGE HERE"
    with open(HTML_FILE_NAME) as fs:
        text = "\n".join(fs.readlines())

    try:
        msg_gmail = create_message(sender=SENDER_MAIL_ID,
                                   to=INDIVIDUAL_MAIL_ID,
                                   subject=MAIL_SUBJECT_NAME,message_text=text)
    except Exception as ex:
        print("Error while creating the email messgae", ex)
        exit(1)

    try:
        send_message(service=service,
                     user_id=SENDER_MAIL_ID,
                     message=msg_gmail)
    except Exception as ex:
        print("Error while sending the email messgae", ex)
        exit(1)

    print("--- Mailing done ---")

if __name__ == '__main__':
    main_2()