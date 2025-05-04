from execucao_texto import processar_dados_por_nome, processar_parecer_nome, exibir_processos
from loader import carregar_arquivo_json, ler_arquivo, criar_arquivo_cordenadas, criar_arquivo_erro, filtrar_nome, salvar_dados, criar_arquivo_novo_dados, criar_arquivo_processos
from coletar_dados import save_data, save_info_assistente, copy_vazio
from funcoes import filtrar_nome_processos, bottoes_processos, buscar_info_medico_assistente, salvar_alteracoes_processos, filtrar_dados, criar_linha_interface, interface_processos, salvar_alteracoes_processos_teste
import customtkinter as ctk
from tkinter import messagebox
import mouseinfo
import time
import pandas as pd

class App(ctk.CTk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(size)

        self.df = None
        self.caminho = None
        self.caminho_pasta = None
        self.check_list = None 
        self.nome = None
        
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="cols")
        self.grid_rowconfigure(0, weight=1)

        self.check_list = Check_list(self)
        self.check_list.withdraw()
        
        self.registrar_cordenada = Registrar_cordenada(self)
        self.formatar_texto = Formatar_texto(self, self.check_list, self) 
        self.menu = Menu(self, self.formatar_texto, self.registrar_cordenada) 
        self.carregar = Carregar(self, self.menu, self)
        #self.registrar_cordenada.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.carregar.grid(row=0, column=0, columnspan=3, sticky="nsew")
        #self.formatar_texto.grid(row=0, column=0, columnspan=3, sticky="nsew")
        #self.menu.grid(row=0, column=0, columnspan=3, sticky="nsew")""".
        #self.check_list.pack(pady=10, padx=20, fill="x")

    def alterar_tamanho(self, novo_tamanho):
        self.geometry(novo_tamanho)

class Check_list(ctk.CTkToplevel):
    def __init__(self, parent):#
        super().__init__(parent)
        
        self.parent = parent

        if self.parent.caminho:
            self.atualizar_interface()  
        else:
            print("caminho indefinido")

        self.alteracoes_checkboxes = {}

        self.botoes_frame = ctk.CTkFrame(self)#
        self.botoes_frame.pack(pady=5, padx=20, fill="x")

        self.busca_frame = ctk.CTkFrame(self)
        self.busca_frame.pack(pady=1, padx=20, fill="x")
 
        self.busca_entry = ctk.CTkEntry(self.busca_frame, width=250)
        self.busca_entry.pack(side="left", padx=5, pady=5)

        self.buscar_medico_btn = ctk.CTkButton(
            self.busca_frame, 
            text="Buscar Info Médico",
            command=self.buscar_info_medico
        )
        self.buscar_medico_btn.pack(side="left", padx=5, pady=5)
        
        self.buscar_assistente_btn = ctk.CTkButton(
            self.busca_frame, 
            text="Buscar Info Assistente",
            command=self.buscar_info_assistente
        )
        self.buscar_assistente_btn.pack(side="left", padx=5, pady=5)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=1000, height=600)#
        self.scrollable_frame.pack(pady=5, padx=20, fill="both", expand=True)        

        self.filtro_atual = "TODOS" 

        acoes_frame = ctk.CTkFrame(self)
        acoes_frame.pack(pady=10, padx=20, fill="x") 
     
        confirm_button = ctk.CTkButton(acoes_frame, text="Confirmar", command=self.confirmar_botao )
        confirm_button.pack(side="left", padx=10, pady=20)   

        atualizar_button = ctk.CTkButton(acoes_frame, text="Atualizar", command=self.atualizar_interface) #
        atualizar_button.pack(side="left", padx=10, pady=20)

        atualizar_button = ctk.CTkButton(acoes_frame, text="Excluir Resolvidos", ) #command=self.excluir_resolvidos
        atualizar_button.pack(side="right", padx=10, pady=20)
      
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        self.alteracoes_checkboxes.clear()
    
    def fechar_janela(self):
        self.withdraw()

    def carregar_dados_processos(self):  
        caminho_arquivo = f"{self.parent.caminho_pasta}/processos.json"
        df = ler_arquivo(caminho_arquivo)

        dados_usuarios = df.to_dict(orient="records")

        return dados_usuarios
    
    def confirmar_botao(self):
        caminho_arquivo = f'{self.parent.caminho_pasta}/processos.json'
        salvar_alteracoes_processos_teste(caminho_arquivo, self.alteracoes_checkboxes)

        self.atualizar_interface()


    def atualizar_interface(self):

        self.dados = self.carregar_dados_processos()

        try:
            bottoes_processos(self.botoes_frame, self.dados, self.scrollable_frame, self.alteracoes_checkboxes, self.filtro_atual, self.set_filtro)
        except Exception as e:
            print(f"Erro ao atualizar interface: {e}")

    def buscar_info_medico(self):
        self.caminho_arquivo = self.parent.caminho
        nome_digitado = self.busca_entry.get().upper()
        campo = "info_medico" 
        self.filtro_atual = campo
        self.termo_busca = nome_digitado
        codigos = buscar_info_medico_assistente(self.caminho_arquivo, campo, nome_digitado)
        print("Códigos filtrados:", codigos)

        self.set_filtro(campo, codigos_filtrados=codigos)

    def buscar_info_assistente(self):
        self.caminho_arquivo = self.parent.caminho
        nome_digitado = self.busca_entry.get().upper()
        campo = "info_assistente" 
        self.filtro_atual = campo
        self.termo_busca = nome_digitado

        codigos = buscar_info_medico_assistente(self.caminho_arquivo, campo, nome_digitado)   
        print("Códigos filtrados:", codigos)

        self.set_filtro(campo, codigos_filtrados=codigos)

    def set_filtro(self, novo_filtro, codigos_filtrados=None):
        self.filtro_atual = novo_filtro
        print("Novo filtro:", self.filtro_atual)
        interface_processos(self.dados, novo_filtro, self.scrollable_frame, self.alteracoes_checkboxes, codigos_filtrados=codigos_filtrados)
        print(self.filtro_atual)

class Carregar(ctk.CTkFrame):
    def __init__(self, parent, menu, app):
        super().__init__(parent)

        self.menu = menu 
        self.app = app 

        self.grid_columnconfigure(0, weight=1, minsize=330)
        self.grid_columnconfigure(1, weight=1, minsize=330)
        self.grid_columnconfigure(2, weight=1, minsize=330)

        self.label_info_inicial = ctk.CTkLabel(self, text="Carregue um arquivo para executar")
        self.label_info_inicial.grid(row=0, column=1, pady=15, padx=(0, 0))

        self.btn_carregar_arquivo = ctk.CTkButton(self, text="Carregar Arquivo", command=self.carregar_dados)
        self.btn_carregar_arquivo.grid(row=1, column=1, pady=(10, 0), padx=(10, 0))

        self.btn_novo_arquivo = ctk.CTkButton(self, text="Novo Arquivo", command=self.novo_arquivo_dados)
        self.btn_novo_arquivo.grid(row=2, column=1, pady=(10, 5), padx=(10, 0))

    def carregar_dados(self):
        resultado = carregar_arquivo_json()
        if resultado:
            df, caminho, caminho_pasta = resultado
            self.app.df = df
            self.app.caminho = caminho
            self.app.caminho_pasta = caminho_pasta
            criar_arquivo_cordenadas(caminho_pasta)
            criar_arquivo_erro(caminho_pasta)
            criar_arquivo_processos(caminho_pasta)
            self.grid_forget()
            self.app.alterar_tamanho("1000x700")

            self.menu.grid(row=0, column=0, columnspan=3, sticky="nsew")  
            return df,caminho, caminho_pasta
        else:
            messagebox.showwarning("Aviso", "Nenhum arquivo foi carregado corretamente.")
        return 

    def novo_arquivo_dados(self):
        criar_arquivo_novo_dados()

class Menu(ctk.CTkFrame):
    def __init__(self, parent, formatar_texto, registrar_cordenada):
        super().__init__(parent)

        self.formatar_texto = formatar_texto 
        self.parent = parent # <<< parece ser inutil
        self.registrar_cordenada = registrar_cordenada
        self.default_size = parent.geometry() # <<< parece ser inutil

        self.grid_columnconfigure(0, weight=1, minsize=330)
        self.grid_columnconfigure(1, weight=1, minsize=330)
        self.grid_columnconfigure(2, weight=1, minsize=330)

        self.label_menu = ctk.CTkLabel(self, text="MENU DE OPÇÕES")
        self.label_menu.grid(row=0, column=1, pady=15, padx=(1, 1))

        self.btn_formatar_texto = ctk.CTkButton(self, text="Formatar Texto", width=250, command=self.exibir_formatar_texto)
        self.btn_formatar_texto.grid(row=1, column=1, pady=(10,0), padx=(1, 1))

        self.btn_buscar_localização = ctk.CTkButton(self, text="Buscar Localização", width=250, command=self.mouse_info)
        self.btn_buscar_localização.grid(row=2, column=1, pady=(5,0), padx=(1, 1))

        self.btn_registrar_cordenada = ctk.CTkButton(self, text="Registrar Cordenada", width=250, command=self.criar_carregar)
        self.btn_registrar_cordenada.grid(row=3, column=1, pady=(5, 800), padx=(1, 1))

    def exibir_formatar_texto(self):
        self.grid_forget()
        self.parent.alterar_tamanho("1000x700")
        self.formatar_texto.grid(row=0, column=0, columnspan=3, sticky="nsew")

    def mouse_info(self):
        mouseinfo.MouseInfoWindow()

    def criar_carregar(self):
        self.grid_forget()
        self.registrar_cordenada.grid(row=0, column=0, columnspan=3, sticky="nsew")

class Registrar_cordenada(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent # <<< parece ser inutil primeiramente

        self.grid_columnconfigure(0, weight=1, minsize=330)
        self.grid_columnconfigure(1, weight=1, minsize=330)
        self.grid_columnconfigure(2, weight=1, minsize=330)

        label = ctk.CTkLabel(self, text="Preencha as coordenadas:", font=("Arial", 16))
        label.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")

        botao1 = ctk.CTkButton(self, text="Novo Posiocionamento")
        botao1.grid(row=1, column=1, pady=(15, 0), padx=5, sticky="nsew")

        botao2 = ctk.CTkButton(self, text="Carregar Posicionamento")
        botao2.grid(row=2, column=1, pady=(5, 600), padx=5, sticky="nsew")

class Formatar_texto(ctk.CTkFrame):
    def __init__(self, parent, check_list, app):
        super().__init__(parent)

        self.parent = parent
        self.check_list = check_list
        self.app = app

        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        # ==== Coluna 0 (com Frame para Botões) ====
        self.frame_coluna0 = ctk.CTkFrame(self)
        self.frame_coluna0.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.btn_coletar_dados = ctk.CTkButton(self.frame_coluna0, text="Coletar Dados", command=lambda: self.quantidade_coletar_dados("dados"), width=170)
        self.btn_coletar_dados.grid(row=0, column=0, pady=(5, 5), padx=(10, 10), sticky="w")

        self.btn_coletar_dados_info_assistente = ctk.CTkButton(self.frame_coluna0, text="Coletar Info Assistente", command=lambda: self.quantidade_coletar_dados("assistente"), width=170)
        self.btn_coletar_dados_info_assistente.grid(row=1, column=0, pady=(5, 5), padx=(10, 10), sticky="w")

        self.btn_enviar_erro = ctk.CTkButton(self.frame_coluna0, text="Enviar Erro", command=self.enviar_erro, width=170)
        self.btn_enviar_erro.grid(row=2, column=0, pady=(5, 5), padx=(10, 10), sticky="w")

        # ==== Coluna 1 (com Frame para Botões) ====
        self.frame_coluna1 = ctk.CTkFrame(self)
        self.frame_coluna1.grid(row=0, column=1, padx=(5, 5), pady=10, sticky="nsew")

        self.label_title = ctk.CTkLabel(self.frame_coluna1, text="Formatação de Texto", width=580)
        self.label_title.grid(row=0, column=0, pady=15, padx=(1, 1), sticky="ew")

        self.label_nome = ctk.CTkLabel(self.frame_coluna1, text="Nome: ", width=50)
        self.label_nome.grid(row=1, column=0, pady=15, padx=(1, 1), sticky="w")

        self.input_nome = ctk.CTkEntry(self.frame_coluna1, placeholder_text="Digite o Nome", width=520)
        self.input_nome.grid(row=1, column=0, padx=(0, 20), sticky="e")

        self.textarea_texto = ctk.CTkTextbox(self.frame_coluna1, height=300, width=550)
        self.textarea_texto.grid(row=2, column=0, padx=(10, 23), pady=(10, 10), sticky="nsew")

        self.btn_formatar_texto = ctk.CTkButton(self.frame_coluna1, text="Formatar Texto", width=400, height=35, command=self.organizar_texto)
        self.btn_formatar_texto.grid(row=3, column=0, pady=(15, 0), padx=(10, 23), sticky="ew")

        self.btn_formatar_parecer = ctk.CTkButton(self.frame_coluna1, text="Formatar Parecer", width=400, height=35, command=self.organizar_parecer)
        self.btn_formatar_parecer.grid(row=5, column=0, pady=(10, 10), padx=(10, 23), sticky="ew")

        # ==== Coluna 2 (com Frame para Botões) ====
        self.frame_coluna2 = ctk.CTkFrame(self)
        self.frame_coluna2.grid(row=0, column=2, padx=(5, 5), pady=10, sticky="nsew")

        self.btn_exibir_processos = ctk.CTkButton(self.frame_coluna2, text="Exibir Processos", command=self.organizar_exibir_processos, width=170)
        self.btn_exibir_processos.grid(row=1, column=0, pady=(5, 5), padx=(10, 10), sticky="w")   

        self.btn_check_list = ctk.CTkButton(self.frame_coluna2, width=170, text="Check List", command=self.tela_check_list)
        self.btn_check_list.grid(row=2, column=0, pady=(5, 5), padx=(10, 10), sticky="w")

    def tela_check_list(self):
        if not self.check_list:
            self.check_list = Check_list(self)
        self.check_list.deiconify()
        self.check_list.atualizar_interface()

    def validar_entrada(self, nome_digitado, df_caminho, textarea, mensagem_vazia="Nenhum nome foi digitado.", mensagem_df_vazio="Nenhum dado encontrado."):
        """Verifica se o nome foi digitado e se o DataFrame está carregado corretamente."""
        if not nome_digitado:
            mensagem = mensagem_vazia
        elif df_caminho is None or df_caminho.empty:
            mensagem = mensagem_df_vazio
        else:
            return True  # Indica que os dados são válidos

        textarea.delete('0.0', 'end')
        textarea.insert('0.0', mensagem)
        return False  
  
    def organizar_texto(self):
        nome_digitado = self.input_nome.get()
        df_caminho = ler_arquivo(self.parent.caminho)

        if not self.validar_entrada(nome_digitado, df_caminho, self.textarea_texto):
            return
    

        if df_caminho is not None:
            resultado = processar_dados_por_nome(df_caminho, nome_digitado)
            self.textarea_texto.delete('0.0', 'end')
            self.textarea_texto.insert('0.0', f'{resultado}')
        else:
            print("nenhum dado carregado")
    
    def organizar_exibir_processos(self):
        #df_sheet_processos = carregar_dados_sheet_processos()

        """if df_sheet_processos.empty:
            self.textarea_texto.delete('0.0', 'end')
            self.textarea_texto.insert('0.0', "nenhum dado encontrado")
        else:
            resultado = exibir_processos(df_sheet_processos)
            self.textarea_texto.delete('0.0', 'end')
            self.textarea_texto.insert('0.0', f'{resultado}')"""
            

    def quantidade_coletar_dados(self, tipo):
        dialog = ctk.CTkInputDialog(title="Número de Coletas", text="Digite o número de coletas")
        try:
            quantidade_str = dialog.get_input()
            if quantidade_str is None or quantidade_str.strip() == "":
                raise ValueError("Nenhum valor foi inserido")

            quantidade = int(quantidade_str)

            if quantidade <= 0:
                raise ValueError("O número deve ser maior que zero")
            
            if tipo == "dados": 
                self.coletar_dados(quantidade)
            elif tipo == "assistente":
                self.coletar_info_assistente(quantidade)

        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Por favor, insira um número inteiro válido.")

    def coletar_dados(self, quantidade):
        cordenada = f"{self.parent.caminho_pasta}/cordenadas.json"
        try:
            caminho = self.parent.caminho
            copy_vazio()
            for i in range(quantidade):
                dados = save_data(caminho, cordenada)

        except Exception as e:
            print(f"Erro em coletar_dados: {e}")

    def coletar_info_assistente(self, quantidade):
        caminho_coletar_dados = self.parent.caminho
        cordenada = f'{self.parent.caminho_pasta}/cordenadas.json'
        caminho_arquivo = f'{self.parent.caminho_pasta}/processos.json'
        try:
            time.sleep(2)
            for i in range(quantidade):
                dados = save_info_assistente(caminho_arquivo, cordenada, caminho_coletar_dados)
            
        except Exception as e:
            print(f"Erro em coletar_dados: {e}")

    def organizar_parecer(self):
        nome_digitado = self.input_nome.get()

        df_caminho = ler_arquivo(self.parent.caminho)
        if df_caminho is not None:
            resultado = processar_parecer_nome(df_caminho, nome_digitado)
            self.textarea_texto.delete('0.0', 'end')
            self.textarea_texto.insert('0.0', f'{resultado}')
        else:
            print("nenhum dado carregado")

    def enviar_erro(self):
        df_caminho = ler_arquivo(self.parent.caminho)
        pasta_caminho = f"{self.parent.caminho_pasta}/erro.json"
        nome_digitado = self.input_nome.get()
        try:
            if nome_digitado:
                df_nome = filtrar_nome(df_caminho, nome_digitado)
                df_dados = df_nome.to_dict(orient="records")
                salvar_dados(df_dados, pasta_caminho)
                
        except Exception as e:
            print(f"Erro em coletar dados {e}")


        
if __name__ == "__main__":
    app = App("DATAFORMAT", "1000x700")
    app.mainloop()



