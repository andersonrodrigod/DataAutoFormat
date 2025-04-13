import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

# Caminho da chave
cred = credentials.Certificate("credenciais_firebase.json")

# Inicializar conexão com Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://medprocessai-a3a1c-default-rtdb.firebaseio.com'
})



def enviar_dados_pacientes(dados_paciente):
    ref = db.reference(f"dados_pacientes/{dados_paciente["nome"]}")
    ref.push(dados_paciente)

def carregar_dados_pacientes():
    ref = db.reference("dados_pacientes")
    dados = ref.get()

    if not dados:
        return pd.DataFrame()
    
    lista_dados = []
    for nome, info in dados.items():
        info["nome"] = nome
        lista_dados.append(info)

    df = pd.json_normalize(lista_dados)

    return df

def carregar_dados_paciente(nome):
    caminho = f"dados_pacientes/{nome}"
    ref = db.reference(caminho)
    dados = ref.get()

    if not dados:
        return pd.DataFrame()
    
    df = pd.DataFrame(dados.values())

    return df

    
def enviar_dados_processo(processo):
    ref = db.reference(f"processos/{processo['codigo']}")
    ref.set(processo)


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

def atualizar_campo_processo(codigo, campo, valor):
    caminho = f"processos/{codigo}"
    ref = db.reference(caminho)
    print(caminho)
    ref.update({campo: valor})

def atualizar_varios_campos(codigo, campos: dict):
    caminho = f"processos/{codigo}"
    ref = db.reference(caminho)
    ref.update(campos)