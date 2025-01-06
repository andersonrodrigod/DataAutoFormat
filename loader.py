import pandas as pd
from tkinter import filedialog, messagebox
from palavras import cordenadas
import os
import json

def criar_arquivo_cordenadas(caminho_pasta):
    if caminho_pasta and not os.path.exists(caminho_pasta + "/cordenadas.json"):
        df = pd.DataFrame([cordenadas])
        df.to_json("cordenadas.json", orient="records", indent=4)
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

def carregar_arquivo_json(caminho_arquivo=None):
    if not caminho_arquivo:
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo JSON",
            filetypes=[("Arquivos JSON", "*.json")]
        )

    if caminho_arquivo:

        caminho_pasta = os.path.dirname(caminho_arquivo)
        try:
            df = pd.read_json(caminho_arquivo)
            messagebox.showinfo("Sucesso", "Arquivo JSON carregado com sucesso")
            if df is not None:
                return df, caminho_arquivo, caminho_pasta
            else:
                print("Nenhum dado foi carregado")
                return None, caminho_arquivo, caminho_pasta
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao ler o arquivo JSON:\n{e}")
        except Exception as e:
            messagebox.showerror("Erro", "invesperado: \n{e}")
            
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo foi selecionado")

        return None, None
    
def carregar_arquivo_erro(caminho_pasta):
    if caminho_pasta and not os.path.exists(caminho_pasta + "/erro.json"):
        df = pd.DataFrame()
        df.to_json("erro.json", orient="records", indent=4)
        print("arquivo criado com sucesso")

def criar_arquivo():
    caminho_do_arquivo = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", ".json"), ("All files", ".")],
        title="Salvar arquivo"
    )

    posicao = {
        "codigo_carteira": [
            {"x": 0, "y": 0}
        ],
        "info_meidico" : [
            {"x": 0, "y": 0}
        ],
        "info_assistente": [
            {"x": 0, "y": 0}
        ]
    }

    if caminho_do_arquivo:
        with open(caminho_do_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(posicao, arquivo, indent=4)
            print(f"arquivo {caminho_do_arquivo} criado com sucesso")       
   
        

