from palavras import botoes_filtro
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from planilhas import sheet_processos
import pandas as pd
from firebase import atualizar_varios_campos


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
    """
    Função que é chamada quando um checkbox é alterado.
    Atualiza o dado local e marca a alteração no dicionário `alteracoes_checkboxes`.
    """
    pessoa = dados[index]
    pessoa[tipo] = checkbox_var.get()

    alteracoes_checkboxes[pessoa["codigo"]] = pessoa

    print(f"Alterações: {alteracoes_checkboxes}")
    print(f"Dados atualizados para {pessoa['nome']}: {pessoa}")


alteracoes_checkboxes = {} 


  


def filtrar_nome_processos(dados, tipo, scrollable_frame, alteracoes_checkboxes, nome_digitado=None):

    for widget in scrollable_frame.winfo_children():
        widget.destroy() 

    if tipo == "TODOS":
        dados_filtrados = [pessoa for pessoa in dados if not pessoa.get("removido", True)]
    elif tipo == "buscar_info_assistente":
        dados_filtrados = [pessoa for pessoa in dados if pessoa["info_assistente"] == nome_digitado]
    else:
        dados_filtrados = [pessoa for pessoa in dados if pessoa["tipo"] == tipo and not pessoa.get("removido", True)]
    
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
    

def remover_linhas_por_nome(nomes):
    # Aqui você deve usar a API do Google Sheets para excluir as linhas
    # Supondo que você tenha uma função para acessar a planilha com `sheet_processos`
    
    for nome in nomes:
        # A função `find` pode ser usada para procurar pelo nome da linha na planilha
        cell = sheet_processos.find(nome)
        
        if cell:
            # Deletando a linha onde o nome foi encontrado
            sheet_processos.delete_rows(cell.row)  # Deleta a linha inteira com base no número da linha

def salvar_alteracoes_processos(dados, top_level_window, alteracoes_checkboxes):
    """
    Função que salva as alterações no Google Sheets, enviando em batch update apenas os dados alterados.
    """
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
            else:
                campos["removido"] = False

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

def filtrar_processos_resolvidos(dados):
    df = pd.DataFrame(dados)  # Converte a lista de dicionários em DataFrame

    if "resolvido" in df.columns:  # Verifica se a coluna existe
        df["resolvido"] = df["resolvido"].astype(str).str.lower() == "true"
        # Filtrando as linhas onde "resolvido" é True
        df_filtrado = df[~df["resolvido"]]  # Exclui as linhas onde "resolvido" é True

        if "nome" in df.columns:
            nomes_para_remover = df[df["resolvido"]]["nome"].tolist()
            remover_linhas_por_nome(nomes_para_remover)

        processos_resolvidos_existem = not df[df["resolvido"]].empty
    else:
        df_filtrado = df  # Mantém o DataFrame original sem filtro
        processos_resolvidos_existem = False  # Nenhum processo foi resolvido

    return df_filtrado, processos_resolvidos_existem
