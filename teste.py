import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

# Dados fictícios com status
dados = [
    {"nome_completo": "João Silva Alencar", "status": "TELEGRAMA"},
    {"nome_completo": "Maria Oliveira", "status": "PARECER"},
    {"nome_completo": "Carlos Souza Araujo dos santos", "status": "RETORNO"},
    {"nome_completo": "Anderson Rodrigo Rodrigues dos santos", "status": "AGUARDANDO"},
    {"nome_completo": "Jeferson rodrigues dos Santos", "status": "PENDENTE"},
    {"nome_completo": "Ana Costa", "status": "PRIMEIRO CONTATO"},
    {"nome_completo": "Pedro Santos", "status": "SEM OBSERVACAO"},
    {"nome_completo": "Lucas Oliveira", "status": "TELEGRAMA"},
    {"nome_completo": "Fernanda Silva", "status": "PARECER"},
    {"nome_completo": "Rafael Souza", "status": "RETORNO"},
    {"nome_completo": "Camila Rodrigues", "status": "AGUARDANDO"},
    {"nome_completo": "Gustavo Almeida", "status": "PENDENTE"},
    {"nome_completo": "Fernanda Silva", "status": "PARECER"},
    {"nome_completo": "Rafael Souza", "status": "RETORNO"},
    {"nome_completo": "Camila Rodrigues", "status": "AGUARDANDO"},
    {"nome_completo": "Gustavo Almeida", "status": "PENDENTE"},
    # Adicione mais dados conforme necessário
]

# Função para filtrar os nomes com base no status
def filtrar_nomes(status):
    # Limpa o frame atual
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Filtra os dados com base no status
    if status == "TODOS":
        dados_filtrados = dados  # Exibe todos os nomes
    else:
        dados_filtrados = [pessoa for pessoa in dados if pessoa["status"] == status]

    # Adiciona os nomes filtrados ao frame
    for i, pessoa in enumerate(dados_filtrados):
        # CTkEntry para o nome completo (permitindo copiar o texto)
        nome_entry = ctk.CTkEntry(scrollable_frame, width=320, font=("Arial", 14))
        nome_entry.insert(0, pessoa["nome_completo"])
        nome_entry.configure(state="readonly")  # Torna o campo somente leitura
        nome_entry.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        # Checkboxes
        for j in range(3):
            checkbox_var = tk.BooleanVar()
            checkbox = ctk.CTkCheckBox(scrollable_frame, text=f"Opção {j+1}", variable=checkbox_var,
                                       command=lambda idx=i, var=checkbox_var: on_checkbox_click(idx, var))
            checkbox.grid(row=i, column=j+1, padx=10, pady=5)

# Função para lidar com o clique nos checkboxes
def on_checkbox_click(index, checkbox_var):
    print(f"Checkbox {index} clicado: {checkbox_var.get()}")

# Configuração da janela principal
app = ctk.CTk()
app.geometry("1250x700")
app.title("Lista de Pessoas com Filtros")

# Frame para os botões de filtro
filtro_frame = ctk.CTkFrame(app)
filtro_frame.pack(pady=10, padx=20, fill="x")

# Botões de filtro
botoes_filtro = ["TODOS", "TELEGRAMA", "PARECER", "RETORNO", "AGUARDANDO", "PENDENTE", "PRIMEIRO CONTATO", "SEM OBSERVACAO"]
for i, texto in enumerate(botoes_filtro):
    botao = ctk.CTkButton(filtro_frame, text=texto, command=lambda s=texto: filtrar_nomes(s))
    botao.grid(row=0, column=i, padx=5, pady=5)

# Frame com barra de rolagem para conter os nomes e checkboxes
scrollable_frame = ctk.CTkScrollableFrame(app, width=1000, height=500)
scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Exibe todos os nomes inicialmente
filtrar_nomes("TODOS")  # Exibe todos os nomes ao iniciar

# Botão para confirmar as seleções
confirm_button = ctk.CTkButton(app, text="Confirmar", command=lambda: messagebox.showinfo("Info", "Seleções confirmadas!"))
confirm_button.pack(pady=20)

# Iniciar a aplicação
app.mainloop()