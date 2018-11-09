from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os

currentDirectory = os.path.dirname(os.path.abspath(__file__))

class GoogleSpreadSheet:
	scopes = 'https://www.googleapis.com/auth/spreadsheets'
	credentialsFile = currentDirectory + '/credentials.json'
	tokenFile = currentDirectory + '/token.json'

	def __init__(self):
		store = file.Storage(self.tokenFile)
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets(self.credentialsFile, self.scopes)
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

	def write(self, rangeName, values, spreadsheetId):
		body = {
		    'values': values
		}
		result = self.service.spreadsheets().values().update(
		    spreadsheetId=spreadsheetId, range=rangeName,
		    valueInputOption="RAW", body=body).execute()
		print('{0} cells updated.'.format(result.get('updatedCells')));

	def read(self, rangeName, spreadsheetId):
		result = self.service.spreadsheets().values().get(
		    spreadsheetId=spreadsheetId, range=rangeName).execute()
		numRows = result.get('values') if result.get('values')is not None else 0

		return numRows
