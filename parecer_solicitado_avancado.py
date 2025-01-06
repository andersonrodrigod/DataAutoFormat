import pandas as pd


def trocar_virgula():
    with open("parecer_solicitado.txt", "r", encoding="utf-8") as arquivo:
        separador = " - "
        content = arquivo.read()
        content = content.replace(",", separador)

    with open("parecer_solicitado.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(content)


df = pd.read_json("./dados/dados_coletados.json", encoding="utf-8")

parecer = "PARECER"

filtrar_parecer_medico = df["info_medico"].str.contains(parecer, na=False)

filtrar_parecer_assistente = ~df["info_assistente"].str.contains(parecer, na=False)

condicao_parecer_solicitado = df[filtrar_parecer_medico & filtrar_parecer_assistente]

parecer_solicitado = condicao_parecer_solicitado[["codigo", "nome"]].drop_duplicates()

if not parecer_solicitado.empty:
    
    parecer_solicitado.to_csv("parecer_solicitado.txt", index=False, header=False)
    trocar_virgula()
else:
    print("nenhum encontrado")

