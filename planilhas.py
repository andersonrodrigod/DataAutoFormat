import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


SERVICE_ACCOUNT_FILE = "credenciais.json"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES)
client = gspread.authorize(creds)

SHEET_ID = "1m9cDBnlICdon3E2FP1F-toCTroFGJy43JebFE5xLkps"

SHEET_ID_COLETAR_DADOS = "1dxncCavrAwjPDoH7UREOpttnLVZyJgYXLEr-Zn3Mq9g"

sheet_processos = client.open_by_key(SHEET_ID).sheet1

sheet_coletar_dados = client.open_by_key(SHEET_ID_COLETAR_DADOS).sheet1



def deletar_linhas_resolvidas():
    """
    Remove as linhas onde a coluna 'resolvido' for 'TRUE' na planilha do Google Sheets.
    """
    dados = sheet_processos.get_all_values()
    
    if not dados:
        return  # Se a planilha estiver vazia, não faz nada

    header = dados[0]  # Cabeçalho das colunas
    valores = dados[1:]  # Dados sem o cabeçalho

    # Índice da coluna 'resolvido' (baseado no cabeçalho)
    try:
        idx_resolvido = header.index("resolvido")
    except ValueError:
        print("Erro: Coluna 'resolvido' não encontrada.")
        return

    # Identifica as linhas a serem excluídas (linhas onde 'resolvido' é 'TRUE')
    linhas_para_excluir = [i + 2 for i, linha in enumerate(valores) if linha[idx_resolvido].strip().upper() == "TRUE"]

    # Deleta as linhas da planilha de baixo para cima para evitar mudanças nos índices
    for linha in reversed(linhas_para_excluir):
        sheet_processos.delete_rows(linha)


def carregar_dados_sheet_processos():
    deletar_linhas_resolvidas()
    return pd.DataFrame(sheet_processos.get_all_values()[1:], columns=["nome", "codigo", "tipo", "data", "hora", "visto", "verificar", "resolvido", "visto_data_hora", "resolvido_data_hora"])


