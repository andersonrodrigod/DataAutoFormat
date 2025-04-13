from collections import OrderedDict
from loader import filtrar_nome, filtrar_nome_no_drop
from palavras import substituicoes, regras_substituicao, delete_texto, questiona_texto, frases_delete, block_questionamento, questionamento_texto, tipos_observacao
from processar_texto import substituir_texto, remover_caracteres, deletar_texto, deletar_info_medico, deletar_frases, processar_data, remover_datas, formatar_solicitacao, formatar_questionamento, consulta, endereco, formatar_texto, formatar_texto_parecer, texto_nome, texto_procedimento, definir_texto_procedimento, texto_obs
from funcoes import ajustar_nome_codigo
from firebase import carregar_dados_paciente



def processar_dados_por_nome(df):
    #bf = filtrar_nome(df, nome)


    if df.empty:
        return "NOME SELECINADO NÃO FOI COLETADO. COLETE OS DADOS DO PACIENTE PARA FORMATAR TEXTO DE SOLICITAÇÃO"
    
    info_medico = df["info_medico"].iloc[0]
    nome_procedimento = df["nome_procedimento"].iloc[0]
    medico_solicitante = df["medico_solicitante"].iloc[0]
    nome = df["nome"].iloc[0]

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
    
def processar_parecer_nome(df):


    if df.empty:
        return "NOME SELECIONADO NÃO FOI COLETADO, COLETE TODOS OS PROCEDIMENTOS PARA FORMATAR TEXTO DO PARECER"

    cod_carteira = df["codigo"].iloc[0]
    nome = df["nome"].iloc[0]
    info_medico = df["info_medico"].iloc[0]
    procedimentos = df[["codigo_procedimento", "nome_procedimento"]].values.tolist()

    resultado = formatar_texto_parecer(nome, cod_carteira, procedimentos, info_medico)

    return resultado
    
def exibir_usuarios_padrao(df):

    if not df.empty:
        usuario_nome = df[["nome", "codigo"]].drop_duplicates(subset="nome", keep="first")
        usuario_nome = usuario_nome.to_numpy()

        resultados = []

        for nome, codigo in usuario_nome:
            resultado = f"{codigo} - {nome}"
            resultados.append(resultado)
        
        
        return "\n".join(resultados)
    else:
        return "num valor padrão foi varrido"        


def exibir_processos(df):

    resultado = ""

    # Loop para filtrar e gerar o texto de cada tipo
    for tipo in tipos_observacao:
        # Filtra o DataFrame para as linhas onde o tipo corresponde ao valor na lista
        df_filtrado = df[df['tipo'] == tipo]
        
        # Adiciona o título do tipo
        resultado += f"{tipo}:\n"
        
        # Adiciona as linhas filtradas
        for index, row in df_filtrado.iterrows():
            resultado += f"{row['codigo']}\t{row['nome']}\n"
        
        resultado += "\n" + "="*50 + "\n"  # Para separar visualmente os tipos

    # Retorna o resultado final
    return resultado

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
    
def exibir_info_medico(df, nome):
    bf = filtrar_nome(df, nome)

    texto_info_medico = str(bf["info_medico"].iloc[0])

    if not bf.empty:
        return texto_info_medico

        




