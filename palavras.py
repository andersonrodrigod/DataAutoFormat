substituicoes = {
    "TC": "TOMOGRAFIA DE",
    "RM": "RESSONÂNCIA DE",
    "RMN": "RESSONÂNCIA DE",
    "RNM": "RESSONÂNCIA DE",
    "RX": "RAIO-X DE",
    "USG": "ULTRASSOM DE",
    "USGTV": "ULTRASSOM TRANSVAGINAL",
    "US OBSTETRICA": "ULTRASSOM OBSTETRICA",
    "US": "ULTRASSOM DE",
    "ANEXAR": "",
    "ITM": "",
    "OCT": "TOMOGRAFICA DE OCOERENCIA OPTICA",
    "LESALES": "",
    "LESALES.": "",
    "SOLICITAR": "",
    "APLICAR": "PREENCHER",
    "GM": "",
    "TAP": "",
    "DE DE": "DE",
    "DE DO": "DE",
    "SE POSSUI": "POSSUI",
    "VERIFICAR SE": "",
    "VERIFICAR": "",
    "OPME": "MATERIAL",
    "DE OU": "OU",
    "COM BF": "",
    "BNF": "",
    "COM BNF": "",
    "ROB": "",
    " ,": "",
    " , ": "",
    " .": "",
    ": ": "",
    " :": "",
    "+": ", ",
    " +": ",",
    " + ": ", ",
    "+ ": ", ",
    " - ": "",
    "- ": " ",
    " -": "",
}

delete_texto = [
    "+ APOS SOLICITAR", "E APÓS SOLICITAR", "E APOS SOLICITAR", "APOS SOLICITAR", "APÓS SOLICITAR", "APOSSOLICITAR", "APOS, SOLICITAR PARECER", "APOS,SOLICITAR", "APOS. SOLICITAR", "APOS.SOLICITAR",  "E APOS, SOLICITAR", "E SOLICITAR O PARECER" "CASO NAO POSSUA, SOLICITAR", "CASO POSSUA, SOLICITAR", "+ APOS, SOLICITAR", "+APOS SOLICITAR", "+APOS, SOLICITAR", " + APOS, SOLICITAR", "PARECER DO", "PARECER DA", "PARECER PARA", "E CONTRATO DE ADESAO AO PLANO" "CONTRATO DE ADESAO AO PLANO", "PEDIR PARECER", "PEDIR O PARECER," "+APÓS", "+APOS", "+ APÓS", "+ APOS"
]

questiona_texto = ["A2", "CHECAR", "VERIFICAR", "SE REALIZOU", "REALIZOU", "SOLICITAR PARECER", "SE POSSUI", "POSSUI", "SE BF", "CHECAR SE", "VERIFICAR SE", "GM", "LESALES", "ITM", "CONFIRMAR"]

questionamento_texto = ["Q1","CHECAR", "VERIFICAR", "SE REALIZOU", "REALIZOU", "SE POSSUI", "POSSUI", "SE BF", "CHECAR SE", "VERIFICAR SE", "GM", "LESALES", "ITM", "CONFIRMAR SE", "CONFIRMAR ONDE"]

questionamento_assistente = ["CHECAR COM RELACIONAMENTO", "AGUARDO PARECER", "SE NÃO, CANCELAR PRÉ-SENHAS", "IMPRIMIR"]

frases_delete = ["CHECAR SE CONSULTA FOI PELO PLANO", "PARTE MEDICA OK", "CANCELAMENTO", "SEM MEDICAMENTOS OU OPME EM GUIA", "MEDICAMENTOS EM GUIA", "AGUARDO PARECER", "CHECAR SE CONSULTA"]

separacoes = "CONFIRMAR ENDEREÇO"

telegrama = ["ENVIAR TELEGRAMA", "ENVIAR TELEGRAMA,", "ENVIAR TELEGRAMA.", "TELEGRAMA"]

block_questionamento = ["Q2","ANEXAR", "TROCAR", "SOLICITAR", "E APÓS", "E APOS", "APOS", "APÓS"]

palavras_parecer = ["SOLICITAR O PARECER", "SOLICITAR PARECER", "ENVIAR PARECER", "PARECER PARA", "PARECER DO", "PEDIR PARECER", "PEDIR O PARECER"]

parecer_block = ["-NÃO ANEXAR","NAO ANEXAR", "NÃO ANEXAR" "(NAO ANEXAR)", "(NÃO ANEXAR)","ITM", "LESALES", "GM"]

regras_substituicao = [
    (r"\s+", " "),        # Substitui múltiplos espaços por um único espaço
    (r" +", " "),         # Substitui múltiplos espaços por um único
    (r"^\s+|\s+$", ""),   # Remove espaços iniciais e finais
    (r"^\+|\+$", ""),     # Remove o sinal de mais (+) no início e no final
    (r"^[^\w\s,()]+|[^\w\s,()]+$", ""),  # Remove pontuação isolada no início e no final, exceto vírgulas
    (r"(?<!\w)-|-(?!\w)", ""),  # Remove traços que não estão entre palavras (isolados)
    (r"^\s*,", ""),        # Remove vírgula quando há espaços antes e depois dela
    (r",\s*$", ""),
    (r"^\s*$", ""),         # Remove linhas em branco
    (r"\+ ANEXAR", "E"),
    (r"(DE|APOS|APÓS|E)\s*$", "") 
]

cordenadas = {
    "codigo_carteira_x": 61,
    "codigo_carteira_y": 592,
    "info_medico_x": 75,
    "info_medico_y": 703,
    "info_assistente_x": 38,
    "info_assistente_y": 774,
    "codigo_procedimento_x": 534,
    "codigo_procedimento_y": 931,
    "codigo_carteira_t22a3x": 0,
    "codigo_carteira_t22a3y": 0,
    "info_telefone_1x": 0,
    "info_telefone_1y": 0, 
    "info_telefone_2x": 0,
    "info_telefone_2y": 0,
    "info_telefone_3x": 0,
    "info_telefone_3y": 0,
    "click_telefone_baixo_x": 0,
    "click_telefone_baixo_y": 0,
    "tela_amop": "viado 1",
    "tela_t22a3": "viado 2"
}


# ------------------------------------------------------------- // ----------------------------------------------------------------------------

# Bloco Padrão

block_padrao = ["CTT REALIZADO", "FEITOCTT", "CTT REALIZADO.", "FEITO CTT."]

todos_codigos = ["34010211", "41001230", "50070207", "30307147",  "30304083", "30304156", "30301181", "41844445", "30502322", "30501458", "30501369", "30501067", "30205034", "30501350", 
"30205042", "30205034", "30403154", "30502209", "30502225", "30501288" 
]

exame_angio = ["34010211", "41001230"]
exame_tratamento_ocular = ["50070207", "30307147"]
exame_implante_anel = ["30304083", "30304156"]
exame_ptose = ["30301181", "41844445"]
exame_naso = ["30502322", "30501458", "30501369", "30501067", "30205034", "30501350", "30205042", "30205034", "30403154", "30502209", "30502225", "30501288"]

categorias = {
    "Angio": exame_angio,
    "Tratamento Ocular": exame_tratamento_ocular,
    "Implante de Anel": exame_implante_anel,
    "Ptose": exame_ptose,
    "Naso": exame_naso,
}

# ------------------------------------------------------------- // ----------------------------------------------------------------------------
#Bloco Processos

botoes_filtro = ["TODOS", "TELEGRAMA", "PARECER", "RETORNO", "AGUARDANDO", "PENDENTE", "PRIMEIRO CONTATO", "SEM OBSERVACAO"]



# Bloco Info Assistente

tipos_observacao = ["TELEGRAMA", "PARECER", "RETORNO", "AGUARDANDO", "PENDENTE", "PRIMEIRO CONTATO", "SEM OBSERVACAO"]

palavras_info_assistente = ["TELEGRAMA", "PARECER", "AJ1", "AGD", "AGUARDO", "COBRO", "FEITO CTT", "CTT REALIZADO"]

mapeamento_palavras_info_assistente = {
    "TELEGRAMA": "TELEGRAMA",
    "PARECER": "PARECER",
    "AJ1": "RETORNO",
    "AGD": "AGUARDANDO",
    "AGUARDO": "AGUARDANDO",
    "COBRO": "PENDENTE",
    "FEITO CTT": "PRIMEIRO CONTATO",
    "CTT REALIZADO": "PRIMEIRO CONTATO",
    "SEM OBSERVACAO": "SEM OBSERVACAO"
}


# Bloco info Medico

palavras_info_medico = ["URGENTE", "PARECER", "TELEGRAMA"]













