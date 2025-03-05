from palavras import botoes_filtro
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from planilhas import sheet_processos

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
    
def bottoes_processos(frame, dados, scrollable_frame):
    botoes = botoes_filtro
    for i, texto in enumerate(botoes):
        botao = ctk.CTkButton(
            frame,
            text=texto,
            command=lambda t=texto: filtrar_nome_processos(dados, t, scrollable_frame)
        )
        botao.grid(row=0, column=i, padx=5, pady=5)

def on_checkbox_click(index, tipo, checkbox_var, dados):
    dados[index][tipo] = checkbox_var.get()  # Atualiza o dado local
    #print(f"Checkbox '{tipo}' da linha {index} clicado: {checkbox_var.get()}")

def salvar_alteracoes_sheet(dados, top_level_window):
    try:

        updates = []
        
        # Prepara as atualizações em um formato adequado para batch_update
        for i, pessoa in enumerate(dados, start=2):  # Começa em 2 para não sobrescrever o cabeçalho
            updates.append({
                'range': f'F{i}',  # Coluna 6 (F) para Visto
                'values': [[pessoa['visto']]]
            })
            updates.append({
                'range': f'G{i}',  # Coluna 7 (G) para Verificar
                'values': [[pessoa['verificar']]]
            })
            updates.append({
                'range': f'H{i}',  # Coluna 8 (H) para Resolvido
                'values': [[pessoa['resolvido']]]
            })
        
        # Atualiza as células em massa com uma única requisição
        sheet_processos.batch_update(updates)

        top_level_window.lift()
        messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
        top_level_window.lift()
    except Exception as e:
        top_level_window.lift()
        messagebox.showerror("Erro", f"Ocorreu um erro ao salvar as alterações: {e}")
        top_level_window.lift()

def filtrar_nome_processos(dados, tipo, scrollable_frame):

    for widget in scrollable_frame.winfo_children():
        widget.destroy() 

    if tipo == "TODOS":
        dados_filtrados = dados  # Exibe todos os nomes
    else:
        dados_filtrados = [pessoa for pessoa in dados if pessoa["tipo"] == tipo]

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
            command=lambda idx=i, var=visto_var: on_checkbox_click(idx, "visto", var, dados_filtrados))
        visto_checkbox.grid(row=i, column=1, padx=10, pady=5)

        aguardando_var = tk.BooleanVar(value=pessoa["verificar"])
        aguardando_checkbox = ctk.CTkCheckBox(
            scrollable_frame,
            text="Verificar",
            variable=aguardando_var,
            command=lambda idx=i, var=aguardando_var: on_checkbox_click(idx, "verificar", var, dados_filtrados))
        aguardando_checkbox.grid(row=i, column=2, padx=10, pady=5)

        resolvido_var = tk.BooleanVar(value=pessoa["resolvido"])
        resolvido_checkbox = ctk.CTkCheckBox(
            scrollable_frame,
            text="Resolvido",
            variable=resolvido_var,
            command=lambda idx=i, var=resolvido_var: on_checkbox_click(idx, "resolvido", var, dados_filtrados))
        resolvido_checkbox.grid(row=i, column=3, padx=10, pady=5)


   










