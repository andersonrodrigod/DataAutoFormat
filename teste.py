import json

def salvar_parecer(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f'Dado adicionado em "PARECER" com sucesso!')

def salvar_telegrama(caminho, dados):
    # Salvar os dados no arquivo JSON
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f'Dado adicionado em "TELEGRAMA" com sucesso!')


name = "ANDERSON RODRIGO RODRIGUES DOS SANTOS"
codigo = "3010I258574003"

user = f"{name} - {codigo}"

palavras = ["TELEGRAMA", "PARECER"]

arquivo_telegram_parecer = "parecer_telegrama.json"

info_assistente = "ENVIO TELEGRAMA"

palavra_encontrada = [item for item in palavras if item in info_assistente]

print(palavra_encontrada)

if "TELEGRAMA" in palavra_encontrada or "PARECER" in palavra_encontrada:
    with open(arquivo_telegram_parecer, "r", encoding="utf-8") as f:
        dados = json.load(f)
        print("Dados carregados do arquivo:", dados) 

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
