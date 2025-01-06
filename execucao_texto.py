from collections import OrderedDict
from loader import filtrar_nome
from palavras import substituicoes, regras_substituicao, delete_texto, questiona_texto, separacoes, telegrama, frases_delete
from processar_texto import substituir_texto, remover_caracteres, deletar_texto, separar_questionamento, seperar_textos, confirma_endereco, verificar_textos, enviar_telegrama, deletar_info_medico, deletar_frases, texto_procedimento, texto_observação, texto_plano, texto_nome, processar_data, remover_datas

def processar_dados_por_nome(df, nome):
    bf = filtrar_nome(df, nome)

    if bf.empty:
        return {
            "nome": None,
            "mensagem": f"O nome '{nome}' não foi encontrado no banco de dados.",
            "procedimento": None,
            "solicitacoes": None,
            "observacao": None,
            "consulta_plano": None
        }    
    
    nome = texto_nome(nome)
    info_medico = bf["info_medico"].iloc[0]
    observacao = texto_observação(info_medico)
    consulta_plano = texto_plano(info_medico)
    nome_procedimento = bf["nome_procedimento"].iloc[0]
    texto_editado = remover_datas(info_medico)
    texto_editado = processar_data(texto_editado)  
    texto_editado = deletar_texto(texto_editado, delete_texto)
    texto_editado = remover_caracteres(texto_editado, regras_substituicao)
    texto_editado = substituir_texto(texto_editado, substituicoes)
    texto_editado = remover_caracteres(texto_editado, regras_substituicao)
    texto_editado = deletar_info_medico(texto_editado)
    texto_editado = deletar_frases(texto_editado, frases_delete)
    endereco = confirma_endereco(texto_editado, separacoes)
    questionamento = separar_questionamento(texto_editado, questiona_texto)
    texto_editado = seperar_textos(questionamento, texto_editado, endereco)
    texto_editado = enviar_telegrama(texto_editado, telegrama)
    solicitacoes = verificar_textos(texto_editado, questionamento, endereco)
    procedimento = texto_procedimento(nome_procedimento)
        
    return {
        "nome": nome,
        "procedimento": procedimento,
        "solicitacoes": solicitacoes,
        "observacao": observacao,
        "consulta_plano": consulta_plano
    }
    

