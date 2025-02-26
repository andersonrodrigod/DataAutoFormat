import json
import pandas as pd

def salvar_parecer(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f'Dado adicionado em "PARECER" com sucesso!')

def salvar_telegrama(caminho, dados):
    # Salvar os dados no arquivo JSON
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f'Dado adicionado em "TELEGRAMA" com sucesso!')

def carregar_dados_telegrama_parecer(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
        return dados 

name = "ANDERSON RODRIGO RODRIGUES DOS SANTOS"
codigo = "3010I258574003"

user = f"{name} - {codigo}"

palavras = ["TELEGRAMA", "PARECER"]

arquivo_telegram_parecer = "processos.json"

info_assistente = "ENVIO PARECER NO GRUPO DE APOIO TELEGRAMA?"

palavra_encontrada = [item for item in palavras if item in info_assistente]

print(palavra_encontrada)

if palavra_encontrada:
    dados = carregar_dados_telegrama_parecer(arquivo_telegram_parecer)

    if "TELEGRAMA" in palavra_encontrada:
        palavra_parecer_telegrama = "TELEGRAMA"
        dados[palavra_parecer_telegrama].append(user)
        salvar_telegrama(arquivo_telegram_parecer, dados)
    elif "PARECER" in palavra_encontrada:
        palavra_parecer_telegrama = "PARECER"
        dados[palavra_parecer_telegrama].append(user)
        salvar_parecer(arquivo_telegram_parecer, dados)
    else:
        palavra_parecer_telegrama = None

    print(palavra_parecer_telegrama)
else:
    print("não foi encotnrada essas palavras")

def ler_arquivo(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Transformando em DataFrame de forma segura
    df = pd.DataFrame({key: pd.Series(value) for key, value in dados.items()})

    return df

def exibir_telegrama_parecer(df):
    df = ler_arquivo(df)
    if not df.empty:
        df_telegrama = df["TELEGRAMA"].drop_duplicates()
        df_parecer = df["PARECER"].drop_duplicates()

        df_telegrama = "\n".join(df_telegrama.astype(str)).strip()
        df_parecer = "\n".join(df_parecer.astype(str)).strip()

        return f"TEEGRAMA:\n{df_telegrama}\n\nPARECER:\n{df_parecer}"
    else:
        return "NÃO FOI COLETADO NENHUM PARECER OU TELEGRAMA"
    

resultado = exibir_telegrama_parecer(arquivo_telegram_parecer)

print(resultado)