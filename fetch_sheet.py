#!/usr/local/bin/python
"""
    Filename:           fetch_sheet.py
    Author:             mrityunjaykumar
    Date:               31/01/19
    author_email:       mrkumar@cs.stonybrook.edu
"""
from __future__ import print_function

"""
Function to retrieve
"""
from config import FILTER_DATE, SHEET_TOKEN_PICKLE_LOCATION, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME, \
    SHEET_CREDENTIAL_JSON_LOCATION, HTML_FILE_NAME

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pandas as pd
pd.set_option('display.max_colwidth', -1)


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def main_1():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(SHEET_TOKEN_PICKLE_LOCATION):
        with open(SHEET_TOKEN_PICKLE_LOCATION, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SHEET_CREDENTIAL_JSON_LOCATION, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(SHEET_TOKEN_PICKLE_LOCATION, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    # print(values)

    columns = ["Timestamp",
               "Your Name",
               "Talk title",
               "Presenter's name and affiliation",
               "URL of the talk",
               "Summary and key ideas",
               "URL of the paper",
               "URL of the slides"]

    # fix values
    fixed_values = []
    for each in values:
        if len(each)!= len(columns):
            diff_len = abs(len(each)- len(columns))
            excess_cols = [" "] * diff_len
            each.extend(excess_cols)
        fixed_values.append(each)

    datecolumn_name = "Timestamp"
    df = pd.DataFrame(fixed_values, columns=columns)
    # date filter --> timestamp filter
    # Column name to change to datetime
    df[datecolumn_name] = pd.to_datetime(df[datecolumn_name])
    import datetime

    df = df[(df[datecolumn_name] > pd.Timestamp(FILTER_DATE))]
    # df.drop(columns=[datecolumn_name], inplace=True)
    # df.drop(columns=["Your Name"], inplace=True)

    formatter_string = """ Talk: <a href="{url_talk}" > {talk_name} </a>, <br> \n
                           Presented by: {presenter_name},<br> \n
                           Suggested by: {suggested_by},<br> \n
                           URL of the talk : {paper_url},<br> \n
                           URL of the slide : {paper_slides_url},<br> \n
                           Summary: {paper_summary}
                       """

    naye_values = []
    for index, row in df.iterrows():
        talk_name = row["Talk title"]
        url_talk = row["URL of the talk"]
        suggested_by = row["Your Name"]
        presenter_name = row["Presenter's name and affiliation"]
        paper_url = row["URL of the paper"]
        paper_slides_url = row["URL of the slides"]
        paper_summary = row["Summary and key ideas"]

        copy_formatter = formatter_string
        copy_formatter = copy_formatter.format(talk_name=talk_name,
                              suggested_by=suggested_by,
                              presenter_name=presenter_name,
                              paper_url=paper_url,
                              paper_slides_url=paper_slides_url,
                              paper_summary=paper_summary,
                              url_talk=url_talk)
        naye_values.append(copy_formatter)

    df.to_html(HTML_FILE_NAME, index=False, header=True)

    pre_table_html_code = """
                          <html>
                            <title>HTML Reference</title>
                          <head>
                          <style>
                          .dataframe {
                               font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                               border-collapse: collapse;
                               width: 100%;
                          }
                          .dataframe td, .dataframe th {
                            border: 1px solid #ddd;
                            padding: 8px;
                          }

                          .dataframe tr:nth-child(even){background-color: #f2f2f2;}

                          .dataframe tr:hover {background-color: #ddd;}

                          .dataframe th {
                            padding-top: 12px;
                            padding-bottom: 12px;
                            text-align: left;
                            background-color: #4CAF50;
                            color: white;
                          }
                          </style>
                          </head>
                          <body>
                          <h2>
                          CSE 656    Computer Vision Seminar
                          </h2>
                          <h3>
                          Spring 2019
                          </h3>
                          """
    post_table_html_code = """
                              </body>
                              </html>
                              """
    all_lines = []

    for each in naye_values:
        each = "<p>" + each + "</p>"
        all_lines.append(each)

    with open(HTML_FILE_NAME, "w") as fs:
        fs.write(pre_table_html_code)
        fs.writelines(all_lines)
        fs.write(post_table_html_code)
    print("--- Fetching done ---")

if __name__ == '__main__':
    main_1()