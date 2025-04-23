import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from datetime import datetime
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
    if not isinstance(dados_paciente, dict):
        return None, None, None, None

    nome_paciente = dados_paciente.get("nome", "Nome não encontrado")
    procedimentos_raw = dados_paciente.get("procedimentos", [])

    # Garante que vamos trabalhar com uma lista de procedimentos válidos
    if isinstance(procedimentos_raw, dict):
        procedimentos = [proc for proc in procedimentos_raw.values() if proc]
    elif isinstance(procedimentos_raw, list):
        procedimentos = [proc for proc in procedimentos_raw if proc]
    else:
        procedimentos = []

    if not procedimentos:
        return None, None, None, None

    # Pegamos o primeiro procedimento para extrair os dados
    primeiro_proc = procedimentos[0]
    codigo = primeiro_proc.get("codigo", "")
    info_medico = primeiro_proc.get("info_medico", "")

    # Criamos a lista com código e nome dos procedimentos
    codigo_nome_procedimentos = []

    for proc in procedimentos:
        codigo = proc.get("codigo_procedimento", "")
        nome = proc.get("nome_procedimento", "")
        codigo_nome_procedimentos.append([codigo, nome])

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


def excluir_processos_removidos():
    ref_processos = db.reference("processos")
    processos = ref_processos.get()

    if not processos:
        return

    for codigo, dados in processos.items():
        if dados.get("removido") == True:
            # Enviar diretamente para a lixeira (sem histórico)
            db.reference(f"lixeira_dados_processos/{codigo}").set(dados)

            # Remover do banco principal
            ref_processos.child(codigo).delete()

def mover_pacientes_para_lixeira():
    ref_lixeira_processos = db.reference("lixeira_dados_processos")
    lixeira_processos = ref_lixeira_processos.get()

    if not lixeira_processos:
        print("Nenhum processo na lixeira.")
        return

    ref_pacientes = db.reference("dados_pacientes")
    pacientes = ref_pacientes.get()

    if not pacientes:
        return

    total_movidos = 0

    for codigo in lixeira_processos.keys():
        if codigo in pacientes:
            paciente_info = pacientes[codigo]
            db.reference(f"lixeira_dados_pacientes/{codigo}").set(paciente_info)
            ref_pacientes.child(codigo).delete()
            total_movidos += 1
            print(f"Paciente {codigo} movido para a lixeira.")

    if total_movidos == 0:
        print("Nenhum paciente encontrado para mover.")
    else:
        print(f"{total_movidos} pacientes movidos para a lixeira.")

def buscar_processo_lixeira(codigo):
    caminho = f"lixeira_dados_processos/{codigo}"
    ref = db.reference(caminho)
    dados = ref.get()

    return dados if dados else None

def deletar_processo_lixeira(codigo):
    caminho = f"lixeira_dados_processos/{codigo}"
    ref = db.reference(caminho)
    ref.delete()
    print(f"Paciente {codigo} removido da lixeira.")

def buscar_paciente_lixeira(codigo):
    caminho = f"lixeira_dados_pacientes/{codigo}"
    ref = db.reference(caminho)
    dados = ref.get()

    return dados if dados else None

def deletar_paciente_lixeira(codigo):
    caminho = f"lixeira_dados_pacientes/{codigo}"
    ref = db.reference(caminho)
    ref.delete()
    print(f"Paciente {codigo} removido da lixeira.")

def enviar_paciente_da_lixeira(codigo):
    ref_lixeira = db.reference(f"lixeira_dados_pacientes/{codigo}")
    paciente = ref_lixeira.get()

    if paciente:
        # Envia de volta para o banco principal
        db.reference(f"dados_pacientes/{codigo}").set(paciente)
        
    
        print(f"Paciente {codigo} restaurado com sucesso.")
        return True
    else:
        print(f"Nenhum paciente com o código {codigo} encontrado na lixeira.")
        return False
    
def buscar_paciente_dados(codigo):
    caminho = f"dados_pacientes/{codigo}"
    ref = db.reference(caminho)
    dados = ref.get()

    return dados if dados else None

def verificar_procedimento_existe(dados_paciente, codigo_procedimento):
    
    procedimentos = dados_paciente.get("procedimentos", {})
    id_proc = None

    if isinstance(procedimentos, dict):
        for id, proc in procedimentos.items():
            if proc and proc.get("codigo_procedimento") == codigo_procedimento:
                id_proc = id
                break

    elif isinstance(procedimentos, list):
        for id, proc in enumerate(procedimentos):
            if proc and proc.get("codigo_procedimento") == codigo_procedimento:
                id_proc = id
                break
    
    else:
        print("Formato de procedimentos não reconhecido.")
        return 
    
    return id_proc
        


