import re
from palavras import regras_substituicao, substituicoes


def processar_data(texto):
    datas_validas = re.findall(r"\b\d{2}[-/:]\d{2}\b", texto)

    if not datas_validas:
        return "Nenhuma data válida encontrada"
    
    ultima_data = datas_validas[-1]

    parte_texto = texto.split(ultima_data, 1)
    texto_pos_ultima_data = parte_texto[1] if len(parte_texto) > 1 else ""

    return texto_pos_ultima_data

def remover_datas(texto):
    
    texto_sem_datas = re.sub(r"\b\d{2}[-/:]\d{2}[-/:](20|21|22|23|24|25)\b[^\w\s]*", "", texto)

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


def separar_questionamento(texto, questiona_texto):
    if texto:
        padrao = rf"([^.?]*\b(?:{'|'.join(map(re.escape, questiona_texto))})\b.*?(?:[.!?]|$))"
        
        # Encontrar todas as ocorrências no texto
        resultados = re.finditer(padrao, texto)
        
        questionamentos_encontrados = []

        # Para cada ocorrência, adicione ao lista
        for resultado in resultados:
            questionamentos_encontrados.append(resultado.group(0).strip())

        # Se houver mais de uma ocorrência, junte-as com um espaço
        if questionamentos_encontrados:
            return " ".join(questionamentos_encontrados)

    return None

def seperar_textos(questionamento, texto, endereco):
    if questionamento and questionamento in texto:
        texto = texto.replace(questionamento, "").strip()
    
    if endereco and endereco in texto:
        texto = texto.replace(endereco, "").strip()

    return texto

def confirma_endereco(texto, endereco):
    if texto:
        if endereco in texto:
            return endereco
        else:
            return None

def enviar_telegrama(texto, telegrama):
    if texto:
        for item in telegrama:
            if item in texto:
                texto = texto.split(item)[0].strip() 

    return texto

    
def verificar_textos(texto, questionamento, endereco):
    texto = remover_caracteres(texto, regras_substituicao)
    resultado = []

    if texto and questionamento and endereco:
        resultado.append(f"A auditoria está solicitando: {texto}. para dar continuidade á análise do procedimento.")
        resultado.append(f"A auditoria está questionando se {questionamento}")
        resultado.append(f"o seu endereço permanece o mesmo?")
    elif texto and questionamento:
        resultado.append(f"A auditoria está solicitando: {texto}. para dar continuidade á análise do procedimento.")
        resultado.append(f"A auditoria está questionando se {questionamento}")
    elif texto and endereco:
        resultado.append(f"A auditoria está solicitando: {texto}. para dar continuidade á análise do procedimento.")
        resultado.append(f"o seu endereço permanece o mesmo?")
    elif texto:
        resultado.append(f"A auditoria está solicitando: {texto}. para dar continuidade á análise do procedimento.")
    elif questionamento and endereco:
        resultado.append(f"A auditoria está questionando se {questionamento}")
        resultado.append(f"o seu endereço permanece o mesmo?")
    elif questionamento:
        resultado.append(f"A auditoria está questionando se {questionamento}")
    elif endereco:
        resultado.append(f"o seu endereço permanece o mesmo?")
    else:
        resultado.append("sem informações")

    return " ".join(resultado)


def texto_procedimento(texto):
    return f'É sobre o procedimento que foi dado entrada *{texto}*'

def texto_nome(nome):
    return f'Olá tudo bem? aqui e do *hapvida* nesse contato falo com {nome}'

def texto_plano(texto):
     if "PELO PLANO" in texto and "CONSULTA CONFIRMADA" not in texto:
        return "A auditoria questiona *SE A CONSULTA FOI PELO PLANO OU PARTICULAR* "

def texto_observação(texto):
    if ("ANEXAR" in texto or "ANEXAAR" in texto) and "NÃO ANEXAR" not in texto and "NAO ANEXAR" not in texto:
        return "*Obs:* Gentileza enviar a foto legível (através deste whatsapp) A foto precisa ser da folha inteira e sem cortar nenhuma informação."
    else:
        return None
    
def texto_solicitacao(texto):
    resultado = ""
    for chave, valor in texto.items():
        if valor is not None:
            resultado += f"{valor}\n\n"
    
    return resultado
    
