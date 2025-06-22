from palavras import botoes_filtro
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import pandas as pd
from datetime import datetime
from loader import ler_arquivo, editar_dados, editar_dados_teste
import json

def encontrar_palavra(palavras, info):
    for palavra in palavras:
        if palavra in info:
            return palavra
    return "SEM OBSERVACAO"

def obter_palavra(palavra, mapeamento_palavras):
    for chave, valor in mapeamento_palavras.items():
        if chave in palavra:
            return valor
        
    return None

def ajustar_nome_codigo(usuarios):
    resultados = []
    
    for codigo, nome in usuarios:
        resultado = f"{nome} - {codigo}"
        resultados.append(resultado)

    return "\n".join(resultados)
    
def bottoes_processos(frame, dados, scrollable_frame, alteracoes_checkboxes, filtro, callback_set_filtro):
    botoes = botoes_filtro
    for i, texto in enumerate(botoes):
        botao = ctk.CTkButton(
            frame,
            text=texto,
            command=lambda t=texto:  callback_set_filtro(t)
        )
        botao.grid(row=0, column=i, padx=5, pady=5)

    interface_processos(dados, filtro, scrollable_frame, alteracoes_checkboxes, callback_set_filtro)   


def atualizar_data_hora(tipo, valor, pessoa):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    if tipo == "visto":
        if valor:
            if isinstance(pessoa.get("visto_data_hora"), list):
                pessoa["visto_data_hora"].append(agora)
            else:
                pessoa["visto_data_hora"] = [agora]
            print(f"[INFO] visto_data_hora adicionada: {agora}")
        else:
            pessoa["visto_data_hora"] = []  # Ou use .pop(...) se quiser remover a chave
            print("[INFO] visto_data_hora esvaziada")

    elif tipo == "resolvido":
        if valor:
            if isinstance(pessoa.get("resolvido_data_hora"), list):
                pessoa["resolvido_data_hora"].append(agora)
            else:
                pessoa["resolvido_data_hora"] = [agora]
            print(f"[INFO] resolvido_data_hora adicionada: {agora}")
        else:
            pessoa["resolvido_data_hora"] = []
            print("[INFO] resolvido_data_hora esvaziada")


def on_checkbox_click(codigo, tipo, checkbox_var, dados, alteracoes_checkboxes):
    pessoa = next((p for p in dados if p["codigo"] == codigo), None)
    
    if pessoa:
        novo_valor = checkbox_var.get()
        pessoa[tipo] = novo_valor

    atualizar_data_hora(tipo, novo_valor, pessoa)
    alteracoes_checkboxes[pessoa["codigo"]] = pessoa # type: ignore
    print(f"[{tipo.upper()}] Alterado para {novo_valor} | Código: {pessoa['codigo']}") # type: ignore
    print(f"→ Dados atuais: {pessoa}")


def salvar_alteracoes_processos(arquivo, alteracoes_checkboxes):
    print("\n[ETAPA 1] Verificando alterações...")

    try:
        dados_allterados = [alteracoes_checkboxes[codigo] for codigo in alteracoes_checkboxes]
        print(f"alterações >>> {dados_allterados}")

        if not alteracoes_checkboxes:
            print("Nenhuma alteração detectada.")
            return
        
        alteracoes_salvas = []

        print("→ Alterações detectadas nos códigos:")
        for pessoa in dados_allterados:
            codigo = pessoa.get("codigo")
            campos = {
                "visto": pessoa.get("visto"),
                "verificar": pessoa.get("verificar"),
                "resolvido": pessoa.get("resolvido"),
                "visto_data_hora": pessoa.get("visto_data_hora"),
                "resolvido_data_hora": pessoa.get("resolvido_data_hora"),
                "removido": pessoa.get("removido")
            }

            if pessoa.get("resolvido") == True:
                campos["visto"] = False
                campos["verificar"] = False
                campos["resolvido"] = False
                campos["removido"] = True

            alteracoes_salvas.append({
                "codigo": codigo,
                "alteracoes": campos
            })


            
        editar_dados_teste(alteracoes_salvas, arquivo)
        
         
    except AttributeError as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao salvar as alterações: {e}")


def filtrar_dados(dados, tipo, codigos_filtrados=None):
    df = pd.DataFrame(dados)
  
    if tipo == "TODOS":
        return df[df["removido"] == False].to_dict(orient="records")
        
    elif tipo in ["info_assistente", "info_medico"] and codigos_filtrados:
        return df[(df["codigo"].isin(codigos_filtrados)) & (df["removido"] == False)].to_dict(orient="records")
    else:
        return df[(df["tipo"] == tipo) & (df["removido"] == False)].to_dict(orient="records")

def criar_linha_interface(pessoa, scrollable_frame, linha, dados, alteracoes_checkboxes):
    nome_entry = ctk.CTkEntry(scrollable_frame, width=320, font=("Arial", 14))
    nome_entry.insert(0, pessoa["nome"])
    nome_entry.configure(state="readonly")
    nome_entry.grid(row=linha, column=0, padx=10, pady=5, sticky="w")

    for idx, (campo, texto) in enumerate([("visto", "Visto"), ("verificar", "Verificar"), ("resolvido", "Resolvido")], start=1):
        var = tk.BooleanVar(value=pessoa[campo])
        checkbox = ctk.CTkCheckBox(
            scrollable_frame,
            text=texto,
            variable=var,
            command=lambda codigo=pessoa["codigo"], v=var, c=campo: on_checkbox_click(codigo, c, v, dados, alteracoes_checkboxes))
        checkbox.grid(row=linha, column=idx, padx=10, pady=5)


def interface_processos(dados, tipo, scrollable_frame, alteracoes_checkboxes, codigos_filtrados=None):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    dados_filtrados = filtrar_dados(dados, tipo, codigos_filtrados)
    #print(f">>>{dados_filtrados}")

    for i, pessoa in enumerate(dados_filtrados):
        criar_linha_interface(pessoa, scrollable_frame, i, dados, alteracoes_checkboxes)

    return tipo



def filtrar_nome_processos(dados, tipo, scrollable_frame, alteracoes_checkboxes, codigos_filtrados=None):
    for widget in scrollable_frame.winfo_children():
        widget.destroy() 

    df = pd.DataFrame(dados)

    if tipo == "TODOS":
        dados_filtrados = df[df["removido"] == False]
    elif tipo in ["info_assistente", "info_medico"] and codigos_filtrados:
        dados_filtrados = df[(df["codigo"].isin(codigos_filtrados)) & (df["removido"] == False)]
    else:
        dados_filtrados = df[(df["tipo"] == tipo) & (df["removido"] == False)]

    dados_filtrados = dados_filtrados.to_dict(orient="records")

    print(f"Filtro aplicado: {tipo}")
    print(f"Dados filtrados: {dados_filtrados}")
    
    for i, pessoa in enumerate(dados_filtrados):
        nome_entry = ctk.CTkEntry(scrollable_frame, width=320, font=("Arial", 14))
        nome_entry.insert(0, pessoa["nome"])
        nome_entry.configure(state="readonly")  # Torna o campo somente leitura
        nome_entry.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        visto_var = tk.BooleanVar(value=pessoa["visto"])
        visto_checkbox = ctk.CTkCheckBox(
            scrollable_frame,
            text="Visto",
            variable=visto_var,
            command=lambda idx=i, var=visto_var: on_checkbox_click(idx, "visto", var, dados, alteracoes_checkboxes))
        visto_checkbox.grid(row=i, column=1, padx=10, pady=5)

        aguardando_var = tk.BooleanVar(value=pessoa["verificar"])
        aguardando_checkbox = ctk.CTkCheckBox(
            scrollable_frame,
            text="Verificar",
            variable=aguardando_var,
            command=lambda idx=i, var=aguardando_var: on_checkbox_click(idx, "verificar", var, dados, alteracoes_checkboxes))
        aguardando_checkbox.grid(row=i, column=2, padx=10, pady=5)

        resolvido_var = tk.BooleanVar(value=pessoa["resolvido"])
        resolvido_checkbox = ctk.CTkCheckBox(
            scrollable_frame,
            text="Resolvido",
            variable=resolvido_var,
            command=lambda idx=i, var=resolvido_var: on_checkbox_click(idx, "resolvido", var, dados, alteracoes_checkboxes))
        resolvido_checkbox.grid(row=i, column=3, padx=10, pady=5)
    
    return tipo

def buscar_info_medico_assistente(caminho_arquivo, campo, nome_digitado):
    df = ler_arquivo(caminho_arquivo)

    resultado = df[df[campo].str.contains(nome_digitado, case=False, na=False)] 

    if not resultado.empty:
        return resultado["codigo"].drop_duplicates().tolist()
    else:
        return []


