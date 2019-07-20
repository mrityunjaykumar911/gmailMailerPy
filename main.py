#!/usr/local/bin/python
"""
    Filename:           main.py
    Author:             mrityunjaykumar
    Date:               02/02/19
    author_email:       mrkumar@cs.stonybrook.edu
"""
from __future__ import absolute_import
# from email_all import main_1
from fetch_sheet import main_1
from mailer import main_2

if __name__ == '__main__':
    # Fetch data from Google Sheet, Sheet ID defined in config.py
    main_1()
    # send the mail to recipients
    main_2()