import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials
import countries_generator
import states_generator

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open("Best Ranked Countries in SMO Any%")

countries_generator.generate()

spreadsheet.values_clear("countries")
spreadsheet.values_update(
    "countries",
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open("countries.tsv"), delimiter="\t"))}
)

states_generator.generate()

spreadsheet.values_clear("US States")
spreadsheet.values_update(
    "US States",
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open("states.tsv"), delimiter="\t"))}
)
