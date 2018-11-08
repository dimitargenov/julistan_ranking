from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class GoogleSpreadSheet:
	scopes = 'https://www.googleapis.com/auth/spreadsheets'

	def __init__(self):
		store = file.Storage('token.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('credentials.json', self.scopes)
			creds = tools.run_flow(flow, store)
		self.service = build('sheets', 'v4', http=creds.authorize(Http()))

	## Create spreadsheet
	def create(self, title):
		spreadsheet = {
		    'properties': {
		        'title': title
		    }
		}
		spreadsheet = self.service.spreadsheets().create(body=spreadsheet,
		                                fields='spreadsheetId').execute()
		print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
		exit()

	## Change the spreadsheet's title.
	def updateTitle(self, title, spreadsheetId):
		requests = []
		requests.append({
		    'updateSpreadsheetProperties': {
		        'properties': {
		            'title': title
		        },
		        'fields': 'title'
		    }
		})
		body = {
		    'requests': requests
		}
		response = self.service.spreadsheets().batchUpdate(
		    spreadsheetId=spreadsheetId,
		    body=body).execute()
		find_replace_response = response.get('replies')[1].get('findReplace')
		print('{0} replacements made.'.format(find_replace_response.get('occurrencesChanged')))

	def write(self, range_name, values, spreadsheet_id):
		body = {
		    'values': values
		}
		result = self.service.spreadsheets().values().update(
		    spreadsheetId=spreadsheet_id, range=range_name,
		    valueInputOption="RAW", body=body).execute()
		print('{0} cells updated.'.format(result.get('updatedCells')));        
