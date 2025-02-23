from collections import OrderedDict
from loader import filtrar_nome, filtrar_nome_no_drop
from palavras import substituicoes, regras_substituicao, delete_texto, questiona_texto, frases_delete, block_questionamento, questionamento_texto
from processar_texto import substituir_texto, remover_caracteres, deletar_texto, deletar_info_medico, deletar_frases, processar_data, remover_datas, formatar_solicitacao, formatar_questionamento, consulta, endereco, formatar_texto, formatar_texto_parecer, texto_nome, texto_procedimento, definir_texto_procedimento, texto_obs
import pandas as pd
import numpy as np





def processar_dados_por_nome(df, nome):
    bf = filtrar_nome(df, nome)

    if bf.empty:
        return "NOME SELECINADO NÃO FOI COLETADO. COLETE OS DADOS DO PACIENTE PARA FORMATAR TEXTO DE SOLICITAÇÃO"
    
    info_medico = bf["info_medico"].iloc[0]
    nome_procedimento = bf["nome_procedimento"].iloc[0]
    medico_solicitante = bf["medico_solicitante"].iloc[0]

    consulta_plano = consulta(info_medico, medico_solicitante)
    confirmar_endereco = endereco(info_medico, nome_procedimento)

    texto_editado = remover_datas(info_medico)
    
    texto_editado = processar_data(texto_editado)
    

    deletar_consulta = deletar_frases(texto_editado, frases_delete)
    questionamento = formatar_questionamento(deletar_consulta, questionamento_texto, block_questionamento)
    questionamento = deletar_texto(questionamento, delete_texto)
    questionamento = substituir_texto(questionamento, substituicoes)
    questionamento = remover_caracteres(questionamento , regras_substituicao)
    questionamento = deletar_info_medico(questionamento)
    questionamento = deletar_frases(questionamento, frases_delete)

    solicitacao = formatar_solicitacao(texto_editado, questiona_texto)
    solicitacao = deletar_texto(solicitacao, delete_texto)
    solicitacao = remover_caracteres(solicitacao, regras_substituicao)
    solicitacao = substituir_texto(solicitacao, substituicoes)
    solicitacao = remover_caracteres(solicitacao , regras_substituicao)
    solicitacao = deletar_info_medico(solicitacao)
    solicitacao = deletar_frases(solicitacao, frases_delete)
    
    enviar_texto = formatar_texto(nome, nome_procedimento, solicitacao, questionamento, consulta_plano, confirmar_endereco)
        
    return enviar_texto
    

def processar_parecer_nome(df, nome):
    bf_drop = filtrar_nome(df, nome)

    if bf_drop.empty:
        return "NOME SELECIONADO NÃO FOI COLETADO, COLETE TODOS OS PROCEDIMENTOS PARA FORMATAR TEXTO DO PARECER"

    bf_no_drop = filtrar_nome_no_drop(df, nome)
    cod_carteira = bf_drop["codigo"].iloc[0]
    info_medico = bf_drop["info_medico"].iloc[0]
    procedimentos = bf_no_drop[["codigo_procedimento", "nome_procedimento"]].values.tolist()

    resultado = formatar_texto_parecer(nome, cod_carteira, procedimentos, info_medico)


    return resultado
    
def exibir_usuarios_padrao(df):
    usuario_nome = df[["nome", "codigo"]].drop_duplicates(subset="nome", keep="first")
    usuario_nome = usuario_nome.to_numpy()

    resultados = []

    for nome, codigo in usuario_nome:
        resultado = f"{codigo} - {nome}"
        resultados.append(resultado)
    
    return "\n".join(resultados)




def exibir_telegrama_parecer(df):
    if not df.empty:
        df_telegrama = df.explode("TELEGRAMA")[["TELEGRAMA"]].drop_duplicates().dropna()
        df_parecer = df.explode("PARECER")[["PARECER"]].drop_duplicates().dropna()

        df_telegrama = "\n".join(df_telegrama["TELEGRAMA"].astype(str).tolist()).strip()
        df_parecer = "\n".join(df_parecer["PARECER"].astype(str).tolist()).strip()

        return f"TEEGRAMA:\n{df_telegrama}\n\nPARECER:\n{df_parecer}"
    else:
        return "NÃO FOI COLETADO NENHUM PARECER OU TELEGRAMA"

    








    
def processar_dado_padrao_por_nome(df, nome):
    bf = filtrar_nome(df, nome) 
    nome_procedimento = bf["nome_procedimento"].iloc[0]
    codigo_procedimento = str(bf["codigo_procedimento"].iloc[0])

    print(type(codigo_procedimento))

    if not bf.empty:
        texto_nome_formatado = texto_nome(nome)
        texto_procedimento_formatado = texto_procedimento(nome_procedimento)
        texto_codigo_procedimento = definir_texto_procedimento(codigo_procedimento)
        return f"{texto_nome_formatado}{texto_procedimento_formatado}{texto_codigo_procedimento}{texto_obs()}"
    


        




