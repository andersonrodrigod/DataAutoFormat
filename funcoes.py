from palavras import botoes_filtro
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import pandas as pd
from datetime import datetime
from loader import ler_arquivo, editar_dados

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

    filtrar_nome_processos(dados, filtro, scrollable_frame, alteracoes_checkboxes)   


def on_checkbox_click(index, tipo, checkbox_var, dados, alteracoes_checkboxes):
    pessoa = dados[index]
    
    novo_valor = checkbox_var.get()
    
    pessoa[tipo] = novo_valor

    if tipo == "visto":
        if novo_valor:
            pessoa["visto_data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        else:
            pessoa.pop("visto_data_hora", None)

    elif tipo == "resolvido":
        if novo_valor:
            pessoa["resolvido_data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        else:
            pessoa.pop("resolvido_data_hora", None)

    alteracoes_checkboxes[pessoa["codigo"]] = pessoa
    #print(f"Alterações: {alteracoes_checkboxes}")
    #print(f"Dados atualizados para {pessoa['nome']}: {pessoa}")


def salvar_alteracoes_processos(arquivo, top_level_window, alteracoes_checkboxes):
    try:
        dados_alterados = [alteracoes_checkboxes[codigo] for codigo in alteracoes_checkboxes]

        if not dados_alterados:
            messagebox.showinfo("Nenhuma alteração", "Não houve alterações para salvar.")
            return

        for pessoa in dados_alterados:
            codigo = pessoa.get("codigo")
            campos = {
                "visto": pessoa.get("visto", False),
                "verificar": pessoa.get("verificar", False),
                "resolvido": pessoa.get("resolvido", False)
            }

            if pessoa["resolvido"] == True:
                campos["removido"] = True
                campos["visto"] = False
                campos["verificar"] = False
                campos["resolvido"] = False
            else:
                campos["removido"] = False


            if campos.get("visto") == True and pessoa.get("visto_data_hora"):
                campos["visto_data_hora"] = pessoa["visto_data_hora"]

            if pessoa.get("resolvido") == True and pessoa.get("resolvido_data_hora"):
                campos["resolvido_data_hora"] = pessoa["resolvido_data_hora"]

            #print(campos)
         
            editar_dados(codigo, campos, arquivo)

        top_level_window.lift()
        messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
        top_level_window.lift()

    except Exception as e:
        top_level_window.lift()
        messagebox.showerror("Erro", f"Ocorreu um erro ao salvar as alterações: {e}")
        top_level_window.lift()

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

    resultado = df[df[campo].str.contains(nome_digitado, case=False, na=False)]  # Adicionando case=False para ignorar maiúsculas/minúsculas

    if not resultado.empty:
        return resultado["codigo"].tolist()
    else:
        return []


