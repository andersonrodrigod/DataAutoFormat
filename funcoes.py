from palavras import botoes_filtro
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from firebase_funcoes import atualizar_varios_campos
from datetime import datetime



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

    
    # Verifica se a chave 'visto_data_hora' existe, se não, inicializa como lista vazia
    if tipo == "visto" and novo_valor:
        pessoa["visto_data_hora"].append(datetime.now().strftime("%d/%m/%Y %H:%M"))

    if tipo == "resolvido" and novo_valor:
        pessoa["resolvido_data_hora"].append(datetime.now().strftime("%d/%m/%Y %H:%M"))

    alteracoes_checkboxes[pessoa["codigo"]] = pessoa

    print(f"Alterações: {alteracoes_checkboxes}")
    print(f"Dados atualizados para {pessoa['nome']}: {pessoa}")


alteracoes_checkboxes = {} 

def filtrar_nome_processos(dados, tipo, scrollable_frame, alteracoes_checkboxes, codigos_filtrados=None):

    for widget in scrollable_frame.winfo_children():
        widget.destroy() 

    if tipo == "TODOS":
        dados_filtrados = [pessoa for pessoa in dados if not pessoa.get("removido", True)]
    elif tipo == "info_assistente" and codigos_filtrados:
         dados_filtrados = [pessoa for pessoa in dados if pessoa["codigo"] in codigos_filtrados and not pessoa.get("removido", True)]
    elif tipo == "info_medico" and codigos_filtrados:
         dados_filtrados = [pessoa for pessoa in dados if pessoa["codigo"] in codigos_filtrados and not pessoa.get("removido", True)]
    else:
        dados_filtrados = [pessoa for pessoa in dados if pessoa["tipo"] == tipo and not pessoa.get("removido", True)]
    
    for i, pessoa in enumerate(dados_filtrados):
        pessoa.setdefault("visto_data_hora", [])
        pessoa.setdefault("resolvido_data_hora", [])
        nome_entry = ctk.CTkEntry(scrollable_frame, width=320, font=("Arial", 14))
        nome_entry.insert(0, pessoa["nome"])
        nome_entry.configure(state="readonly")  # Torna o campo somente leitura
        nome_entry.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        visto_var = tk.BooleanVar(value=pessoa["visto"])
        visto_checkbox = ctk.CTkCheckBox(
            scrollable_frame,
            text="Visto",
            variable=visto_var,
            command=lambda idx=i, var=visto_var: on_checkbox_click(idx, "visto", var, dados_filtrados, alteracoes_checkboxes))
        visto_checkbox.grid(row=i, column=1, padx=10, pady=5)

        aguardando_var = tk.BooleanVar(value=pessoa["verificar"])
        aguardando_checkbox = ctk.CTkCheckBox(
            scrollable_frame,
            text="Verificar",
            variable=aguardando_var,
            command=lambda idx=i, var=aguardando_var: on_checkbox_click(idx, "verificar", var, dados_filtrados, alteracoes_checkboxes))
        aguardando_checkbox.grid(row=i, column=2, padx=10, pady=5)

        resolvido_var = tk.BooleanVar(value=pessoa["resolvido"])
        resolvido_checkbox = ctk.CTkCheckBox(
            scrollable_frame,
            text="Resolvido",
            variable=resolvido_var,
            command=lambda idx=i, var=resolvido_var: on_checkbox_click(idx, "resolvido", var, dados_filtrados, alteracoes_checkboxes))
        resolvido_checkbox.grid(row=i, column=3, padx=10, pady=5)
    

def salvar_alteracoes_processos(dados, top_level_window, alteracoes_checkboxes):
    try:
        # Filtra os dados alterados (apenas as pessoas que foram modificadas)
        dados_alterados = [pessoa for pessoa in dados if pessoa["codigo"] in alteracoes_checkboxes]

        # Verifica se há dados para atualizar
        if not dados_alterados:
            messagebox.showinfo("Nenhuma alteração", "Não houve alterações para salvar.")
            return

        # Atualiza cada pessoa alterada no Firebase
        for pessoa in dados_alterados:
            codigo = pessoa.get("codigo")
            campos = {
                "visto": pessoa.get("visto", False),
                "verificar": pessoa.get("verificar", False),
                "resolvido": pessoa.get("resolvido", True)
            }

            if pessoa["resolvido"]:
                campos["removido"] = True
                campos["visto"] = False
                campos["verificar"] = False
                campos["resolvido"] = False
            else:
                campos["removido"] = False

            if pessoa["visto_data_hora"]:
                campos["visto_data_hora"] = pessoa["visto_data_hora"]
            if pessoa["resolvido_data_hora"]:
                campos["resolvido_data_hora"] = pessoa["resolvido_data_hora"]

            atualizar_varios_campos(codigo, campos)

        # Limpa o dicionário de alterações
        alteracoes_checkboxes.clear()

        # Feedback para o usuário
        top_level_window.lift()
        messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
        top_level_window.lift()

    except Exception as e:
        top_level_window.lift()
        messagebox.showerror("Erro", f"Ocorreu um erro ao salvar as alterações: {e}")
        top_level_window.lift()

