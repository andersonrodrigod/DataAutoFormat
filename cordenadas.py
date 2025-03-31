import pandas as pd

def carregar_cordenada(caminho):
    df = pd.read_json(caminho)

    codigo_carteira = df[["codigo_carteira_x", "codigo_carteira_y"]].iloc[0]
    info_medico = df[["info_medico_x", "info_medico_y"]].iloc[0]
    info_assistente = df[["info_assistente_x", "info_assistente_y"]].iloc[0]
    codigo_procedimento = df[["codigo_procedimento_x", "codigo_procedimento_y"]].iloc[0]
    codigo_carteira_t22a3 = df[["codigo_carteira_t22a3x", "codigo_carteira_t22a3y"]].iloc[0]
    info_telefone_1 = df[["info_telefone_1x", "info_telefone_1y"]].iloc[0]
    info_telefone_2 = df[["info_telefone_2x", "info_telefone_2y"]].iloc[0]
    info_telefone_3 = df[["info_telefone_3x", "info_telefone_3y"]].iloc[0]
    click_telefone_baixo = df[["click_telefone_baixo_x", "click_telefone_baixo_y"]]
    amop = df["tela_amop"].astype(str).iloc[0]
    t22a3 = df["tela_t22a3"].astype(str).iloc[0]

    #amop

    codigo_carteira_x, codigo_carteira_y = map(int, codigo_carteira)
    info_medico_x, info_medico_y = map(int, info_medico)
    info_assistente_x, info_assistente_y = map(int, info_assistente)
    codigo_procedimento_x, codigo_procedimento_y = map(int, codigo_procedimento)

    codigo_carteira = codigo_carteira_x, codigo_carteira_y
    info_medico = info_medico_x, info_medico_y
    info_assistente = info_assistente_x, info_assistente_y
    codigo_procedimento = codigo_procedimento_x, codigo_procedimento_y

    #t22a3

    codigo_carteira_tx, codigo_carteira_ty = map(int, codigo_carteira_t22a3)
    info_telefone_1x, info_telefone_1y = map(int, info_telefone_1)
    info_telefone_2x, info_telefone_2y = map(int, info_telefone_2)
    info_telefone_3x, info_telefone_3y = map(int, info_telefone_3)
    click_telefone_baixo_x, click_telefone_baixo_y = map(int, info_telefone_3)

    codigo_carteira_t = codigo_carteira_tx, codigo_carteira_ty
    telefone_1 = info_telefone_1x,  info_telefone_1y
    telefone_2 = info_telefone_2x,  info_telefone_2y
    telefone_3 = info_telefone_3x,  info_telefone_3y
    telefone_baixo = click_telefone_baixo_x, click_telefone_baixo_y


    return codigo_carteira, info_medico, info_assistente, codigo_procedimento, codigo_carteira_t, telefone_1, telefone_2, telefone_3, telefone_baixo, amop, t22a3 

