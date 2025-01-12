from collections import OrderedDict
from loader import filtrar_nome, filtrar_nome_no_drop
from palavras import substituicoes, regras_substituicao, delete_texto, questiona_texto, frases_delete, block_questionamento
from processar_texto import substituir_texto, remover_caracteres, deletar_texto, deletar_info_medico, deletar_frases, processar_data, remover_datas, formatar_solicitacao, formatar_questionamento, consulta, endereco, formatar_texto, formatar_texto_parecer
import pandas as pd



nome = "LUCIANO MARCOS FERREIRA"

df = pd.read_json("./dados/dados_coletados.json")

def processar_dados_por_nome(df, nome):
    bf = filtrar_nome(df, nome)

    if bf.empty:
        return {
            "nome": None,
            "mensagem": f"O nome '{nome}' não foi encontrado no banco de dados.",
            "procedimento": None,
            "solicitacoes": None,
            "questionamento": None,
            "observacao": None,
            "consulta_plano": None,
            "endereco": None
        }    
    
    info_medico = bf["info_medico"].iloc[0]
    nome_procedimento = bf["nome_procedimento"].iloc[0]
    medico_solicitante = bf["medico_solicitante"].iloc[0]
    texto_editado = remover_datas(info_medico)
    texto_editado = processar_data(texto_editado)

    consulta_plano = consulta(info_medico, medico_solicitante)
    confirmar_endereco = endereco(info_medico, nome_procedimento)

    deletar_consulta = deletar_frases(texto_editado, frases_delete)
    questionamento = formatar_questionamento(deletar_consulta, questiona_texto, block_questionamento)
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
    bf_no_drop = filtrar_nome_no_drop(df, nome)
    cod_carteira = bf_drop["codigo"].iloc[0]
    info_medico = bf_drop["info_medico"].iloc[0]
    procedimentos = bf_no_drop[["codigo_procedimento", "nome_procedimento"]].values.tolist()

    resultado = formatar_texto_parecer(nome, cod_carteira, procedimentos, info_medico)

    return resultado



