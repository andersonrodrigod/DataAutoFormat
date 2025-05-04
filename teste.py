import json

# Caminho do arquivo
caminho_arquivo = "processos.json"

# Carregar os dados existentes
with open(caminho_arquivo, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Atualizar os dados
for pessoa in dados:
    pessoa["visto_data_hora"] = []
    pessoa["resolvido_data_hora"] = []
    pessoa["data_hora_bot"] = []
    pessoa["visto"] = False
    pessoa["verificar"] = False
# Salvar os dados de volta no arquivo
with open(caminho_arquivo, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)

print("Atualização concluída com sucesso!")