import pandas as pd
from tkinter import filedialog, messagebox
from palavras import cordenadas
import os
import json
import pywinctl



def criar_arquivo_novo_dados():
    caminho_pasta = filedialog.askdirectory()

    if not caminho_pasta:
        print("operação cancelada")
        return

    if os.path.exists(caminho_pasta + "/dados_coletados.json"):
        messagebox.showinfo("ATENÇÃO", "Já existe um arquivo de dados_coletados na pasta, carregue o arquivo de dados_coletados para continuar")

    else:
        df = pd.DataFrame()
        df.to_json("dados_coletados.json", orient="records", indent=4)
        messagebox.showinfo("Sucesso", "Arquivo criado com sucesso, carregue o arquivo criado de dados_coletadoas para continuar")

def criar_arquivo_cordenadas(caminho_pasta):
    if caminho_pasta and not os.path.exists(caminho_pasta + "/cordenadas.json"):
        df = pd.DataFrame([cordenadas])
        df.to_json("cordenadas.json", orient="records", indent=4)
        print("arquivo criado com sucesso")

def criar_arquivo_erro(caminho_pasta):
    if caminho_pasta and not os.path.exists(caminho_pasta + "/erro.json"):
        df = pd.DataFrame()
        df.to_json("erro.json", orient="records", indent=4)
        print("arquivo criado com sucesso")

def ler_arquivo(arquivo):
    return pd.read_json(arquivo)

def salvar_dados(dados, caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.extend(dados)

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    messagebox.showinfo("Sucesso", "Erro enviado com sucesso")

def filtrar_nome(df, nome):
    return df[df["nome"] == nome].drop_duplicates(subset="nome", keep="first")

def filtrar_codigo(df,codigo):
    return df[df["codigo"] == codigo]

def filtrar_nome_no_drop(df, nome):
    return df[df["nome"] == nome]

def filtrar_por_nome_ou_codigo(df, valor):
    if valor.isdigit():  # Se o valor for numérico (código)
        return df[df["codigo"] == valor]
    else:  # Se não for numérico, assume-se que é o nome
        return df[df["nome"] == valor]

def carregar_arquivo_json(caminho_arquivo=None):
    messagebox.showinfo("ATENÇÃO", "Selecione o arquivo JSON dados_coletados")
    if not caminho_arquivo:
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo JSON dados_coletados",
            filetypes=[("Arquivos JSON", "*.json")]
        )

    if caminho_arquivo:

        caminho_pasta = os.path.dirname(caminho_arquivo)
        try:
            df = pd.read_json(caminho_arquivo)
            messagebox.showinfo("Sucesso", "Arquivo JSON carregado com sucesso")
            if df is not None:
                return df, caminho_arquivo, caminho_pasta
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao ler o arquivo JSON:\n{e}")
        except Exception as e:
            messagebox.showerror("Erro", "invesperado: \n{e}")
            
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo foi selecionado")

        return None
    

def atualizar_telas(caminho, janela_1, janela_2):
    try:
        with open(caminho, "r", encoding="utf-8") as file:
            dados = json.load(file)

        dados[0]["tela_amop"] = janela_1
        dados[0]["tela_t22a3"] = janela_2


        with open(caminho, "w", encoding="utf-8") as file:
            json.dump(dados, file, indent=4, ensure_ascii=False)
            
        print("dados salvos com sucesso")
    
    except Exception as e:
        print(f"Erro ao Salvar os dados json {e}")


def obter_telas():
    nome = "DATA"

    janelas = []

    for janela in pywinctl.getAllWindows():
        if nome.lower() in janela.title.lower():
            janelas.append(f'{janela.title}')

    return "\n\n".join(janelas) if janelas else "Nenhuma janela encontrada."


"""
def obter_telas():
    janelas = []

    # Itera sobre todas as janelas abertas
    for janela in pywinctl.getAllWindows():
        # Remove espaços extras do título da janela
        titulo = janela.title.strip()
        
        # Ignora janelas com títulos vazios ou irrelevantes
        if titulo and titulo != "": 
            janelas.append(titulo)

    # Retorna as janelas abertas ou uma mensagem caso nenhuma janela tenha sido encontrada
    return "\n".join(janelas) if janelas else "Nenhuma janela encontrada."
"""



def verificador_telas(caminho):
    df = pd.read_json(caminho)
    cordernadas = df[["tela_amop", "tela_t22a3"]]

    

    if (cordernadas == "").any().any():
        execut = False
        print("As telas não foram definidas")
    else:
        execut = True
        print("execução foi um sucesso")

    return execut











