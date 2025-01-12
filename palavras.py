substituicoes = {
    "TC": "TOMOGRAFIA DE",
    "RM": "RESSONÂNCIA DE",
    "RMN": "RESSONÂNCIA DE",
    "RNM": "RESSONÂNCIA DE",
    "RX": "RAIO-X DE",
    "USG": "ULTRASSOM DE",
    "US OBSTETRICA": "ULTRASSOM OBSTETRICA",
    "US": "ULTRASSOM DE",
    "+ ANEXAR": "",
    "ANEXAR": "",
    "ANEXAAR": "",
    "ITM": "",
    "OCT": "TOMOGRAFICA DE OCOERENCIA OPTICA",
    "LESALES": "",
    "LESALES.": "",
    "SOLICITAR": "",
    "APLICAR": "PREENCHER",
    "GM": "",
    "DE DE": "DE",
    "VERIFICAR SE PACIENTE POSSUI": "POSSUI",
    "VERIFICAR SE POSSUI NOVOS EXAMES": "POSSUI NOVOS EXAMES",
    "INFORMA OPME EM VERSO DA FOLHA": "OPME EM VERSO DA FOLHA",
    "OPME": "MATERIAL",
    "DE OU": "OU",
    "COM BF": "",
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
    "+ APOS SOLICITAR", "E APÓS SOLICITAR", "E APOS SOLICITAR", "APOS SOLICITAR", "APÓS SOLICITAR", "APOSSOLICITAR", "APOS, SOLICITAR PARECER", "APOS,SOLICITAR", "APOS. SOLICITAR", "APOS.SOLICITAR",  "E APOS, SOLICITAR", "E SOLICITAR O PARECER" "CASO NAO POSSUA, SOLICITAR", "CASO POSSUA, SOLICITAR", "+ APOS, SOLICITAR", "+APOS SOLICITAR", "+APOS, SOLICITAR", " + APOS, SOLICITAR", "PARECER DO", "PARECER DA", "PARECER PARA", "E CONTRATO DE ADESAO AO PLANO" "CONTRATO DE ADESAO AO PLANO"
]

questiona_texto = ["CHECAR", "VERIFICAR", "SE REALIZOU", "REALIZOU", "SE POSSUI", "POSSUI", "SE BF", "CHECAR SE", "VERIFICAR SE", "GM", "LESALES", "ITM"]

questionamento_assistente = ["CHECAR COM RELACIONAMENTO", "AGUARDO PARECER", "SE NÃO, CANCELAR PRÉ-SENHAS", "IMPRIMIR"]

frases_delete = ["CHECAR SE CONSULTA FOI PELO PLANO", "PARTE MEDICA OK", "CANCELAMENTO", "SEM MEDICAMENTOS OU OPME EM GUIA", "MEDICAMENTOS EM GUIA", "AGUARDO PARECER", "CHECAR SE CONSULTA"]

separacoes = "CONFIRMAR ENDEREÇO"

telegrama = ["ENVIAR TELEGRAMA", "ENVIAR TELEGRAMA,", "ENVIAR TELEGRAMA.", "TELEGRAMA"]

block_questionamento = ["ANEXAR", "TROCAR"]

palavras_parecer = ["SOLICITAR O PARECER", "SOLICITAR PARECER", "ENVIAR PARECER", "PARECER PARA", "PARECER DO"]

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
    (r"\+ ANEXAR", "E") 
]

cordenadas =  {
    "codigo_carteira_x": 61,
    "codigo_carteira_y": 592,
    "info_medico_x": 75,
    "info_medico_y": 703,
    "info_assistente_x": 38,
    "info_assistente_y": 774
}
