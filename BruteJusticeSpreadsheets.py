from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')
	store = Storage(credential_path)
	credentials = store.get()
	if(not credentials or credentials.invalid):
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		credentials = tools.run_flow(flow, store, None)
		print('Storing credentials to ' + credential_path)
	return credentials

#spreadsheetId = '1-DjsyCbph0tw4Esg87pEApyp-NZn3B6yx5A6nk3uYUs'
#credentials = get_credentials()
#http = credentials.authorize(httplib2.Http())
#discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
#                    'version=v4')
#service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
#rangeName = 'B:B'
#result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
#values = result.get('values', [])

def ReadSpreadsheet(rangeNames, sheetid):
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
			'version=v4')
	service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
	spreadsheetId = sheetid
	result = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId, ranges=rangeNames).execute()
	values = []
	valueRanges = result.get('valueRanges', [])
	for item in valueRanges:
		if('values') in item.keys():#result.get('valueRanges', [])[0].keys():
			values.append(item['values'])
			#return values
			#return result
	#return []
	return values

def WriteSpreadsheet(spreadsheetID, sheet=1, cell='A1', value=0):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    spreadsheetId = spreadsheetID
    values = [[value]]
    body = {'values': values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId, range='Sheet{}!{}'.format(sheet, cell),
        valueInputOption='USER_ENTERED', body=body).execute()
    return result