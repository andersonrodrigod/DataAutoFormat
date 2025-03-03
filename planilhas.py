import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


SERVICE_ACCOUNT_FILE = "credenciais.json"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES)
client = gspread.authorize(creds)

SHEET_ID = "1m9cDBnlICdon3E2FP1F-toCTroFGJy43JebFE5xLkps"

sheet_processos = client.open_by_key(SHEET_ID).sheet1


df_shet_processos = pd.DataFrame(sheet_processos.get_all_values()[1:], columns=["nome", "codigo", "tipo", "data", "hora", "visto", "resolvido"])