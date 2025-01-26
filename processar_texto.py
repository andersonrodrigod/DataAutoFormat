import re
from palavras import regras_substituicao, substituicoes, palavras_parecer, parecer_block, exame_angio, categorias
from loader import filtrar_nome_no_drop, filtrar_nome


def processar_data(texto):
    datas_validas = re.findall(r"\b\d{2}[-/:]\d{2}\b", texto)

    if not datas_validas:
        return "Nenhuma data válida encontrada"
    
    ultima_data = datas_validas[-1]

    parte_texto = texto.split(ultima_data, 1)
    texto_pos_ultima_data = parte_texto[1] if len(parte_texto) > 1 else ""

    return texto_pos_ultima_data

def remover_datas(texto):
    
    texto_sem_datas = re.sub(r"\b\d{2}[-/:]\d{2}[-/:](20|21|22|23|24|25|2020|2021|2022|2023|2024|2025)\b[^\w\s]*", "", texto)

    texto = texto_sem_datas.strip()

    return texto

def substituir_texto(texto, substituicoes):
    if texto:
        for chave, valor in substituicoes.items():
            texto = re.sub(rf"\b{re.escape(chave)}\b", valor, texto)
    return texto

def remover_caracteres(texto, regras_substituicoes):
    if texto:
        for padrao, substituicoes in regras_substituicoes:
            texto = re.sub(padrao, substituicoes, texto)
    return texto
    
def deletar_texto(texto, delete_texto):
    if texto:
        for item in delete_texto:
            if item in texto:  
                texto = texto.split(item, 1)[0] 
    return texto

def deletar_info_medico(texto):
    if texto:
        indice = texto.rfind('>')

        if indice != -1:
            texto = texto[indice + 1:].strip()
            return texto
        else:
            return texto
    
def deletar_frases(texto, frases):
    if texto:   
        for item in frases:
            if item in texto:
                texto = texto.replace(item, "").strip()
                texto = remover_caracteres(texto, regras_substituicao)
                texto = substituir_texto(texto, substituicoes)

        if texto == "":
            print("Texto ficou vazio, retornando None.")
            return None
        
    return texto

def consulta(texto, medico):
    if "MEDICO TRANSCRICAO" in medico or "PELO PLANO" in texto:
        return "CONSULTA FOI PARTICULAR OU PELO PLANO?"
    
def endereco(texto, procedimento):
    if "ANGIOGRAFIA" in procedimento or "ENDEREÇO" in texto or "ENDERECO" in texto:
        return "Seu endereço permanece o mesmo do sistema?"

def formatar_solicitacao(texto, condicoes):
    if texto:
       
        palavras = '|'.join(condicoes) 
        padrao = rf'ANEXAR|SOLICITAR|\s*(.*?)(\s*(?:{palavras})\s*|\s*\.)|$'

        resultado = re.search(padrao, texto)

        if resultado:
            # Condição 1: Encontrar o padrão e verificar se encontrou a palavra-chave
            if resultado.group(2):
                return resultado.group(1).strip()  # Retorna tudo depois de ANEXAR até a palavra-chave
            else:
                return None  # Caso não tenha a palavra-chave, retorna até o ponto
        else:
            # Condição 2: Caso não encontre o padrão ANEXAR
            return None
   
def formatar_questionamento(texto, questiona_texto, condicoes):
    if texto:
        palavras_iniciais_regex = '|'.join(questiona_texto)
        palavras = '|'.join(condicoes)
        padrao = rf'({palavras_iniciais_regex})\s*(.*?)(?:\s*(?:{palavras})\s*|\.|$)'

        resultado = re.search(padrao, texto)

        if resultado:
            if resultado.group(2):  # Verifica se o grupo 2 não é None ou vazio
                return resultado.group(2).strip()  # Retorna o texto após as palavras iniciais até encontrar "palavras" ou ponto
            else:
                return None  # Caso o grupo 2 seja vazio ou None
        else:
            return None  # Caso não encontre nenhum padrão

    return None

def formatar_texto(nome, procedimento, solicitacao, questionamento, consulta_plano, endereco):
    resultado = []
    if nome:
        resultado.append(f'Olá tudo bom? aqui é do *HAPVIDA NOTREDAME* falo com *{nome}*?\n\n') 

    if procedimento:
        resultado.append(f'É sobre o procedimento que foi dado entrada *{procedimento}*\n\n')

    if solicitacao:
        resultado.append(f'A auditoria está solicitando: *{solicitacao}* para dar continuidade a análise do procedimento.\n\n')

    if questionamento:
        resultado.append(f'A auditoria questiona se: *{questionamento}*\n\n')
    
    if consulta_plano:
        resultado.append(f'A auditoria questiona se: *{consulta_plano}*\n\n')

    if solicitacao:
        resultado.append("*Obs:* Gentileza enviar a foto legível (através deste whatsapp) A foto precisa ser da folha inteira e sem cortar nenhuma informação.\n\n")

    if endereco:
        resultado.append(endereco)

    if resultado:
        return "".join(resultado)
    else:
        return None
    
def buscar_parecer(texto, palavras_parecer, parecer_block):
    if texto:
        palavras_parecer = '|'.join(palavras_parecer)
        parecer_block = '|'.join(parecer_block)

        padrao = rf'({palavras_parecer})\s*(.*?)(?:\s*(?:{parecer_block})\s*|\(|\.|$)'

        resultado = re.search(padrao, texto)

        if resultado:
            grupo1 = resultado.group(1).strip()

            if resultado.group(2): 
                grupo2 = resultado.group(2).strip()
            else:
                grupo2 = ''  

            return f"{grupo1} {grupo2}".strip()
    
    return None
  
 
def formatar_texto_parecer(nome, codigo, procedimentos, info_medico):
    codigo_nome_procedimento = []

    nome = nome
    codigo = codigo

    info = buscar_parecer(info_medico, palavras_parecer, parecer_block)
    
    for cod_proc, nome_proc in procedimentos:
        if cod_proc not in codigo_nome_procedimento:
            codigo_nome_procedimento.append(f"{cod_proc} - {nome_proc}\n")
    
    header = f"{nome} - {codigo}\n"

    if codigo_nome_procedimento:
        codigo_nome_procedimento = "".join(codigo_nome_procedimento)
    
    resultado = f"PARECER / NDI MINAS / {header}\nBom dia,\n\n{info}\n\n{header}{codigo_nome_procedimento}"


    return resultado


def texto_nome(nome):
    return f'Olá tudo bom? aqui é do *HAPVIDA NOTREDAME* falo com *{nome}*?\n\n'

def texto_procedimento(procedimento):
    return f'É sobre o procedimento que foi dado entrada *{procedimento}*\n\n'

def texto_obs():
    return f'\n\n*Obs:* Gentileza enviar a foto legível (através deste whatsapp) A foto precisa ser da folha inteira e sem cortar nenhuma informação.\n\n'

def texto_angio_tc():
    return f'A auditoria médica está solicitando o resultado dos seguintes exames:\n\n- *RESSONÂNCIA CARDIACA*\n- *CINTILO MIOCARDIO*\n- *TESTE ERGOMETRICO*\n- *ECOCARDIOGRAMA COM ESTRESSE FARMACOLOGICO*\n- *CATETERISMO*\n\nPoderia nos enviar por aqui os exames realizados?\n\nSeu endereço permanece o mesmo do sistema?'

def texto_otorrino():
    return f'A auditoria médica está solicitando o resultado dos seguintes exames:\n\n- *NASOFIBROLARINGOSCOPIA (LAUDO E IMAGENS)*\n- *TOMOGRAFIA DA FACE (LAUDO E IMAGENS)*\n- *RAIO X CAVUM*\n\nPoderia nos enviar por aqui os exames realizados?'

def texto_tratamento_ocular():
    return f'A auditoria médica está solicitando o resultado dos seguintes exames:\n\n- *ACUIDADE VISUAL*\n- *TOMOGRAFIA DE COERENCIA OPTICA*\n\nPoderia nos enviar por aqui os exames realizados?'

def implante_anel():
    return f'A auditoria médica está solicitando o resultado dos seguintes exames:\n\n- *PENTACAM*\n- *CERATOSCOPIA*\n\nPoderia nos enviar por aqui os exames realizados?'

def ptose():
    return f'A auditoria médica está solicitando o resultado dos seguintes exames:\n\n- *CAPIMETRIA*\n- *FOTO DOS OLHOS*\n\nPoderia nos enviar por aqui os exames realizados?'


def definir_texto_procedimento(procedimento):
    exame = None
    for categoria, exames in categorias.items():
        if procedimento in exames:
            exame = categoria
            break

    if exame == "Angio":
        return  texto_angio_tc()
    
    if exame == "Tratamento Ocular":
        return  texto_tratamento_ocular()
    
    if exame == "Implante de Anel":  
        return  implante_anel()

    if exame == "Ptose":
        return  ptose()

    if exame == "Naso":
        return  texto_otorrino()

        
    return 'TEXTO DE PROCEDIMENTO NÃO ENCONTRADO'



    
    
        

    

    
        













