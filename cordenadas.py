import pandas as pd

caminho = "cordenadas.json"

def carregar_cordenada(caminho):
    df = pd.read_json(caminho)

    codigo_carteira = df[["codigo_carteira_x", "codigo_carteira_y"]].iloc[0]
    info_medico = df[["info_medico_x", "info_medico_y"]].iloc[0]
    info_assistente = df[["info_assistente_x", "info_assistente_y"]].iloc[0]
    codigo_procedimento = df[["codigo_procedimento_x", "codigo_procedimento_y"]].iloc[0]



    codigo_carteira_x, codigo_carteira_y = map(int, codigo_carteira)
    info_medico_x, info_medico_y = map(int, info_medico)
    info_assistente_x, info_assistente_y = map(int, info_assistente)
    codigo_procedimento_x, codigo_procedimento_y = map(int, codigo_procedimento)

    

    codigo_carteira = codigo_carteira_x, codigo_carteira_y
    info_medico = info_medico_x, info_medico_y
    info_assistente = info_assistente_x, info_assistente_y
    codigo_procedimento = codigo_procedimento_x, codigo_procedimento_y


    return codigo_carteira, info_medico, info_assistente, codigo_procedimento 




resultado = carregar_cordenada(caminho)

print(resultado)


   
