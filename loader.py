import pandas as pd
from tkinter import filedialog, messagebox
from palavras import cordenadas
import os
import json



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

def criar_arquivo_coletar_padrao(caminho_pasta):
    if caminho_pasta and not os.path.exists(caminho_pasta + "/dados_coletados_padrao.json"):
        df = pd.DataFrame()
        df.to_json("dados_coletados_padrao.json", orient="records", indent=4)
        print("arquivo criado com sucesso")

def criar_arquivo_processos(caminho_pasta):
    if caminho_pasta and not os.path.exists(caminho_pasta + "/processos.json"):
        dados = {
            "TELEGRAMA": [],
            "PARECER": [],
            "RETORNO": [], #AJ1 AJ2 AJ3
            "PENDENTE": [], #cobro
            "AGUARDANDO": [], #AGD
            "PRIMEIRO CONTATO": [],
            "SEM OBSERVACAO": []
        } 

        with open(caminho_pasta + "/processos.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        
        print("arquivo criado com sucesso")

def ler_arquivo(arquivo):
    return pd.read_json(arquivo)

def ler_arquivo_frame(arquivo):
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    
    df = pd.DataFrame({key: pd.Series(value) for key, value in dados.items()})

    return df

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

def filtrar_nome_no_drop(df, nome):
    return df[df["nome"] == nome]

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
    

    





