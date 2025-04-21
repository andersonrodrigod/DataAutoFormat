import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import json
# Caminho da chave
cred = credentials.Certificate("credenciais_firebase.json")

# Inicializar conexão com Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://medprocessai-a3a1c-default-rtdb.firebaseio.com'
})


def obter_novo_id(codigo):
    # Referência ao paciente
    ref_paciente = db.reference(f"dados_pacientes/{codigo}")

    # Verifica o contador do paciente, se existir
    contador_atual = ref_paciente.child("contador").get()

    if contador_atual is None:
        contador_atual = 1  # Se não houver contador, começa com 1

    # Atualiza o contador para o próximo número
    ref_paciente.child("contador").set(contador_atual + 1)

    return contador_atual


# ENVIA OS DADOS DA FUNÇÃO COLETAR_DADOS PARA O BANCO DE DADOS
def enviar_dados_pacientes(dados_paciente):
    codigo = dados_paciente["codigo"]
    nome = dados_paciente["nome"]
   

    ref_paciente = db.reference(f"dados_pacientes/{codigo}")

    ref_paciente.update({
        "nome": dados_paciente["nome"]
    })


    novo_id = obter_novo_id(codigo)

    novo_procedimento = {
        "codigo": dados_paciente["codigo"],
        "nome": dados_paciente["nome"],
        "codigo_procedimento": dados_paciente["codigo_procedimento"],
        "nome_procedimento": dados_paciente["nome_procedimento"],
        "info_assistente": dados_paciente["info_assistente"],
        "info_medico": dados_paciente["info_medico"],
        "medico_solicitante": dados_paciente["medico_solicitante"]
    }

    ref_paciente.child("procedimentos").child(str(novo_id)).set(novo_procedimento)
    ref_indices = db.reference("indices_nome")
    ref_indices.child(nome).set(codigo)

def enviar_dados_processo(processo):
    ref = db.reference(f"processos/{processo['codigo']}")
    ref.set(processo)

#ESSA FUNÇÃO DEVE SER APAGADA
"""def carregar_dados_pacientes():
    ref = db.reference("dados_pacientes")
    dados = ref.get()
    print(json.dumps(dados, indent=2, ensure_ascii=False))

    if not dados:
        return pd.DataFrame()
    
    lista_dados = []
    for codigo, info in dados.items():
        info["codigo"] = codigo
        lista_dados.append(info)

    df = pd.json_normalize(lista_dados)

    return df"""

# CARREGA OS DADOS EM UM DATA FRAME PARA SER UTILIZADO NO CHEKLIST COM NOME E CHECKBOXES COM EXCEÇÃO DO RESOLVIDOS
def carregar_dados_processo():
    ref = db.reference("processos")
    dados = ref.get()

    if not dados:
        return pd.DataFrame()
    
    lista_dados = [
        item for item in dados.values()
            if not item.get("resolvido", False)
    ]

    return pd.DataFrame(lista_dados)

# CARREGA DADOS_PACIENTE SEM SER UM DATAFRAME
def listar_pacientes():
    ref = db.reference("dados_pacientes")
    dados = ref.get()

    return dados

# PROCURA NOME DIGITADO NO DADOS_PACIENTE E RETORNA O CODIGO SE ACHAR OS NOMES
def buscar_info_medico_assistente(nome_digitado, campo):

    dados = listar_pacientes()

    pacientes_encontrados = [] 

    for codigo, paciente in dados.items():
        procedimentos = paciente.get('procedimentos', [])
        
        for procedimento in procedimentos:
            if procedimento:
                info_campo = procedimento.get(campo)
                if nome_digitado in info_campo:
                   pacientes_encontrados.append(codigo)
                   break       

    return pacientes_encontrados    


# CARREGA DADOS_PACIENTES EM UM DATAFRAME
def carregar_dados_paciente(codigo):
    caminho = f"dados_pacientes/{codigo}"
    ref = db.reference(caminho)
    dados = ref.get()

    if not dados:
        return pd.DataFrame()
    
    df = pd.DataFrame(dados.values())

    return df

# BUSCA PACIENTE POR NOME PELO INDICE E RETORNA O CODIGO DO DADO CHAVE ASSIM COMO NO INPUT FORMATAR TEXTO QUE SÓ PESQUISA PELO NOME
def buscar_paciente_por_nome(nome):
    ref_indices = db.reference("indices_nome")
    codigo = ref_indices.child(nome).get()

    if not codigo:
        return None  

    ref_paciente = db.reference(f"dados_pacientes/{codigo}")
    dados_paciente = ref_paciente.get()

    return dados_paciente

# CRIAR CONDICIONAIS ONDE BARRA O PROCESSO SE NAO VIER O DADO / PROCURA O CODIGO DO PACIENTE PELO INDICE(NOME/CODIGO) QUE RETORNOU NA FUNÇÃO buscar_paciente_por_nome TRANSFORMA A CHAVE PROCEDIEMNTOS EM UM DATA FRAME E RETORNA OS DADOS PARA FORMATAR TEXTO 
def buscar_info_paciente(dados_paciente):
    if not dados_paciente:
        return None, None, None, None, None, None

    nome_paciente = dados_paciente.get("nome", "Nome não encontrado")
    procedimentos_raw = dados_paciente.get("procedimentos", [])

    if isinstance(procedimentos_raw, dict):
        procedimentos = [proc for proc in procedimentos_raw.values() if proc]
    else:
        procedimentos = [proc for proc in procedimentos_raw if proc]

    if not procedimentos:
        return None, None, None, None, None, None
    
    procedimento = procedimentos[0]

    codigo = procedimento.get("codigo", "Código não encontrado")
    info_medico = procedimento.get("info_medico", "Informação médica não encontrada")
    codigo_procedimento = procedimento.get("codigo_procedimento", "Código de procedimento não encontrado")
    nome_procedimento = procedimento.get("nome_procedimento", "Nome de procedimento não encontrado")
    medico_solicitante = procedimento.get("medico_solicitante", "Médico solicitante não encontrado")

    return codigo, nome_paciente, codigo_procedimento, nome_procedimento, info_medico, medico_solicitante

# BUSCA PACIENTE POR NOME E FORMATAR TEXTO PARECER
def buscar_paciente_parecer(dados_paciente):
    nome_paciente = dados_paciente.get("nome", "Nome não encontrado")
    procedimentos_raw = dados_paciente.get("procedimentos", [])


    if isinstance(procedimentos_raw, dict):
        procedimentos = [proc for proc in dados_paciente.get("procedimentos").values() if proc]
    else:
        procedimentos = [proc for proc in procedimentos_raw if proc]

    if not procedimentos:
        return None, None, None, None

    df_procedimentos = pd.DataFrame(procedimentos)
    
    codigo = df_procedimentos["codigo"].iloc[0]
    info_medico = df_procedimentos["info_medico"].iloc[0]
    codigo_nome_procedimentos = df_procedimentos[["codigo_procedimento", "nome_procedimento"]].values.tolist()

    return codigo, nome_paciente, info_medico, codigo_nome_procedimentos
    

# ATUALIZA A INFORMAÇÃO DO CAMPO ESTÁ SENDO UTILIZADA NO CASO PARA ATUALIZAR O CAMPO DE REMOVIDO DE TRUE PARA FALSE CASO SE AUTOMAÇÃO ENCONTRAR UM DADO EM TRUE ELE RETORNA PARA FALSE
def atualizar_campo_processo(codigo, campo, valor):
    caminho = f"processos/{codigo}"
    ref = db.reference(caminho)
    print(caminho)
    ref.update({campo: valor})

# ATUALIZA A INFORMAÇÃO DOS CAMPOS ESTÁ SENDO UTILIZADA NO CASO PARA ATUALIZAR QUANDO SÃO DOIS CAMPOS POR EXEMPLO REMOVIDO E O DADO PROCESSO ELE ATUALIZA COM NOVAS INFORMAÇÕES
def atualizar_varios_campos(codigo, campos: dict):
    caminho = f"processos/{codigo}"
    ref = db.reference(caminho)
    ref.update(campos)
    print(f"[Firebase] Atualizado {codigo}: {campos}")

# ATUALIZA A NOVA INFORMAÇÃO DO ESDITAR DADO DO INFO_MEDICO
def atualizar_info_medico(nome, novo_valor):
    dados_paciente = buscar_paciente_por_nome(nome)

    if not dados_paciente:
        print("Paciente não encontrado.")
        return

    # Busca os dados necessários
    codigo, nome_paciente, codigo_proc, nome_proc, info_medico, medico_solicitante = buscar_info_paciente(dados_paciente)

    print("dados_paciente:", dados_paciente)
    print("info_medico:", info_medico)

 
    procedimentos = dados_paciente.get("procedimentos", {})
    id_proc = None

    if isinstance(procedimentos, dict):
        for id_, proc in procedimentos.items():
            if proc and proc.get("codigo_procedimento") == codigo_proc:
                id_proc = id_
                break
    elif isinstance(procedimentos, list):
        for id_, proc in enumerate(procedimentos):
            if proc and proc.get("codigo_procedimento") == codigo_proc:
                id_proc = id_
                break
    else:
        print("Formato de procedimentos não reconhecido.")
        return 

    if id_proc is None:
        print("Procedimento com esse código não encontrado.")
        return

    # Atualiza o campo info_medico no procedimento correto
    ref_proc = db.reference(f"dados_pacientes/{codigo}/procedimentos/{id_proc}")
    
    ref_proc.update({
        "info_medico": novo_valor
    })

