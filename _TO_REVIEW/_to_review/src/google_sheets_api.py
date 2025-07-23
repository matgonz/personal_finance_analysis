
# class GoogleSheetsAPI:

#     def __init__(self, json_credentials: str):
        
#         # Define the scope
#         self.scope = ["https://spreadsheets.google.com/feeds", 
#                       "https://www.googleapis.com/auth/drive"]
        
#         # Add credentials to the account
#         self.creds = Credentials.from_service_account_file(json_credentials, scopes=self.scope)

#         # Authorize the clientsheet 
#         self.client = gspread.authorize(self.creds)


#     def update_google_sheets(self, 
#                              new_transactions: pd.DataFrame, 
#                              sheet_name: str):

#         # Get the instance of the Spreadsheet
#         sheet = self.client.open(sheet_name).sheet1

#         # Get the existing data
#         existing_data = sheet.get_all_values()

#         print(existing_data)

#         # Convert the DataFrame to a list of lists
#         #new_data = transactions.values.tolist()

#         # Append new rows
#         # for row in new_data:
#         #     sheet.append_row(row)

import gspread
from oauth2client.service_account import ServiceAccountCredentials



file_creds = "personalprojects-447411-c86a8a15ab35.json"

scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(filename=file_creds, 
                                                         scopes=scopes)
client = gspread.authorize(creds)
print(client)

planilha_completa = client.open(title="mge_personal_finance_database", 
                                folder_id="11D66zBHjnqhnNlXDZxWB-bFOHbJ6LMq1")

planilha = planilha_completa.get_worksheet(0)
dados = planilha.get_all_records()
print(dados)