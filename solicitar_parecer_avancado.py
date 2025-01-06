import pandas as pd


def trocar_virgula():
    separador = " - "
    with open("solicitar_parecer.txt", "r", encoding="utf-8") as arquivo:
        content = arquivo.read()
        content = content.replace(",", separador)

    with open("solicitar_parecer.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(content)


df = pd.read_json("./dados/dados_coletados.json", encoding="utf-8")

parecer = "PARECER"
grupo = "GRUPO"


filtrar_parecer = df["info_assistente"].str.contains(parecer, na=False)
filtrar_grupo = ~df["info_assistente"].str.contains(grupo, na=False)

condicao_solicitar_parecer = df[filtrar_parecer & filtrar_grupo]

solicitar_parecer = condicao_solicitar_parecer[["codigo", "nome"]].drop_duplicates()


if not solicitar_parecer.empty:
    print(solicitar_parecer)

    solicitar_parecer.to_csv("solicitar_parecer.txt", sep=",", index=False, header=False, encoding="utf-8")
    trocar_virgula()
else:
    print("nenhum encontrado")