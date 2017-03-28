# -*- coding: utf-8 -*-
# @Author: Jeremiah
# @Date:   2017-03-24 22:56:46
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2017-03-27 21:37:39


from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
APPLICATION_NAME = 'vixxoUploader'
CLIENT_SECRET_FILE = os.path.join(os.path.join(os.path.expanduser('~'), 'surveyMagic'), 'clientid.json')



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'vixxoUploader.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getSheetService():
    """Gets and returns the basic service for use in other methods
    or via the interactive command prompt
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    return service

def get_drive_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    return service

def addSpreadsheet(api_service, title=None):
    requestBody = {}
    if title:
        requestBody['properties'] = {'title': title}
    request = api_service.spreadsheets().create(body= requestBody)
    response = request.execute()
    return response

def add_lines_to_spreadsheet(api_service, spreadsheetId, values):
    range_ = 'A1'
    value_input_option = 'RAW' 
    insert_data_option = 'OVERWRITE'
    value_range_body = {
        'values' : values
    
    }
    result = api_service.spreadsheets().values().append(
        spreadsheetId = spreadsheetId, range=range_,
        valueInputOption = value_input_option, body=value_range_body).execute()
    return result

def shareDocument(spreadsheetId):
    service = get_drive_service()
    bodyData = {'role': 'writer', 'type': 'anyone'}
    result = service.permissions().create(fileId=spreadsheetId, body=bodyData)
    return result




def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)


    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()
