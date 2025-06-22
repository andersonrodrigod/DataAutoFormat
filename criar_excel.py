import pandas as pd


arquivo_json = pd.read_json("dados_analitics.json")

df = pd.DataFrame(arquivo_json)

df.to_excel("dados_analitics.xlsx", index=False)

print("Arquivo Excel criado com sucesso: dados_analitics.xlsx")
