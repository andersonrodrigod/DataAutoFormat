from execucao_texto import processar_dados_por_nome, processar_parecer_nome, exibir_usuarios_padrao, exibir_processos, exibir_info_medico
from loader import carregar_arquivo_json, ler_arquivo, criar_arquivo_cordenadas, criar_arquivo_erro, filtrar_nome, salvar_dados, criar_arquivo_novo_dados, atualizar_telas
from coletar_dados import save_data, save_info_assistente, save_data_dois, copy_vazio
from funcoes import bottoes_processos, salvar_alteracoes_sheet, filtrar_processos_resolvidos, obter_telas, verificador_telas
from planilhas import carregar_dados_sheet_processos
import customtkinter as ctk
from tkinter import messagebox
import mouseinfo
import time
import json

class App(ctk.CTk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(size)

        self.df = None
        self.caminho = None
        self.caminho_pasta = None
        self.nome = None
        
        
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="cols")
        self.grid_rowconfigure(0, weight=1)

        self.check_list = Check_list(self)
        self.check_list.withdraw()
        self.definir_telas = Definir_tela(self)
        self.definir_telas.withdraw()
        self.editar_dados = Editar_dados(self)
        self.editar_dados.withdraw()
    

        self.formatar_texto = Formatar_texto(self, self.check_list, self.definir_telas, self.editar_dados, self) 

        self.editar_dados = Editar_dados(self)
        self.editar_dados.withdraw()

        self.registrar_cordenada = Registrar_cordenada(self)
        self.menu = Menu(self, self.formatar_texto, self.registrar_cordenada) 
        self.carregar = Carregar(self, self.menu, self)
        #self.registrar_cordenada.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.carregar.grid(row=0, column=0, columnspan=3, sticky="nsew")
        #self.formatar_texto.grid(row=0, column=0, columnspan=3, sticky="nsew")
        #self.menu.grid(row=0, column=0, columnspan=3, sticky="nsew")""".
        #self.check_list.pack(pady=10, padx=20, fill="x")

    def alterar_tamanho(self, novo_tamanho):
        self.geometry(novo_tamanho)

class Editar_dados(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        nome = self.parent.nome if self.parent.nome else ""
 
        self.title("Editar Dados")
        self.geometry("450x350") 
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.label_nome = ctk.CTkLabel(self.main_frame, text="Nome:")
        self.label_nome.pack(pady=(0, 5), anchor="w")
        
        self.entry_nome = ctk.CTkEntry(self.main_frame, width=400)
        self.entry_nome.pack(pady=(0, 10))

        self.label_texto = ctk.CTkLabel(self.main_frame, text="Informações:")
        self.label_texto.pack(pady=(0, 5), anchor="w")
        
        self.textarea = ctk.CTkTextbox(self.main_frame, width=400, height=150)
        self.textarea.pack(pady=(0, 15))

        self.btn_editar = ctk.CTkButton(
            self.main_frame, 
            text="Editar",
            command=self.editar_dados
        )
        self.btn_editar.pack()
        
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def editar_dados(self):
        caminho_arquivo = self.parent.caminho  # Obtém o caminho do arquivo JSON
        df = ler_arquivo(caminho_arquivo)  # Lê o JSON e transforma em DataFrame

        nome = self.entry_nome.get()  # Obtém o nome
        novo_texto = self.textarea.get("1.0", "end-1c")  # Obtém o novo valor

        df.loc[df["nome"] == nome, "info_medico"] = novo_texto

        # Converte para lista de dicionários
        dados = df.to_dict(orient="records")

        # Salva de volta no JSON
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        print(f"Dados editados com sucesso - Nome: {nome}, Novo Texto: {novo_texto}")

    def fechar_janela(self):
        self.withdraw()


class Definir_tela(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.parent.alterar_tamanho("800x600") # # não funciona em top level

        self.label_janela1 = ctk.CTkLabel(self, text="Janela 1")
        self.label_janela1.pack(pady=10, padx=20)

        self.entry_janela1 = ctk.CTkEntry(self, width=400)
        self.entry_janela1.pack(pady=10, padx=20)

        # Campo de entrada para Janela 2
        self.label_janela2 = ctk.CTkLabel(self, text="Janela 2")
        self.label_janela2.pack(pady=10, padx=20)

        self.entry_janela2 = ctk.CTkEntry(self, width=400)
        self.entry_janela2.pack(pady=10, padx=20)

        # Botão Salvar
        self.botao_salvar = ctk.CTkButton(self, text="Salvar", command=self.definir_janelas)
        self.botao_salvar.pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
    
    def fechar_janela(self):
        self.withdraw()

    def definir_janelas(self):
        nome_digitado_janela_1 = self.entry_janela1.get()
        nome_digitado_janela_2 = self.entry_janela2.get()

        cordenadas = f'{self.parent.caminho_pasta}/cordenadas.json'

        atualizar_telas(cordenadas, nome_digitado_janela_1, nome_digitado_janela_2)

class Check_list(ctk.CTkToplevel):
    def __init__(self, parent):#
        super().__init__(parent)
        
        #self.app = app

        self.parent = parent

        self.parent.alterar_tamanho("1240x700") # não funciona em top level

        self.botoes_frame = ctk.CTkFrame(self)#
        self.botoes_frame.pack(pady=10, padx=20, fill="x")

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=1000, height=500)#
        self.scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.dados = carregar_dados_sheet_processos().to_dict(orient="records")
        

        # Armazena o filtro atual
        self.filtro_atual = "TODOS" 

        acoes_frame = ctk.CTkFrame(self)
        acoes_frame.pack(pady=10, padx=20, fill="x")

        self.atualizar_interface()
        
        confirm_button = ctk.CTkButton(acoes_frame, text="Confirmar", command=self.confirmar_botao)
        confirm_button.pack(side="left", padx=10, pady=20)

        atualizar_button = ctk.CTkButton(acoes_frame, text="Atualizar", command=self.atualizar_interface)
        atualizar_button.pack(side="left", padx=10, pady=20)

        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
    
    def fechar_janela(self):
        self.withdraw()

    def confirmar_botao(self):
        # Salvar alterações
        salvar_alteracoes_sheet(self.dados, self)

        # Filtrar os dados resolvidos
        df_filtrado, processos_resolvidos_existem = filtrar_processos_resolvidos(self.dados)

        if processos_resolvidos_existem:
            self.atualizar_interface()

        # Atualizar a interface após salvar alterações e remover processos resolvidos
        self.atualizar_interface()

    def atualizar_interface(self):
        # Limpar o conteúdo do scrollable_frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Atualizar os dados
        self.dados = carregar_dados_sheet_processos().to_dict(orient="records")

        # Recriar os widgets de exibição com os dados atualizados
        bottoes_processos(self.botoes_frame, self.dados, self.scrollable_frame)
    
class Carregar(ctk.CTkFrame):
    def __init__(self, parent, menu, app):
        super().__init__(parent)

        self.menu = menu 
        self.app = app 

        self.app.alterar_tamanho("1240x700")

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
    def __init__(self, parent, check_list, definir_telas, editar_dados, app):
        super().__init__(parent)

        self.parent = parent
        self.check_list = check_list
        self.definir_telas = definir_telas
        self.editar_dados = editar_dados
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

        self.btn_coletar_dados_teste = ctk.CTkButton(self.frame_coluna0, text="Coletar Dados 2", command=self.coletar_dois, width=170)
        self.btn_coletar_dados_teste.grid(row=3, column=0, pady=(5, 5), padx=(10, 10), sticky="w")        

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

        self.btn_editar_texto = ctk.CTkButton(self.frame_coluna1, text="Editar", width=400, height=35, command=self.tela_editar_dados)
        self.btn_editar_texto.grid(row=4, column=0, pady=(10, 0), padx=(10, 23), sticky="ew")

        self.btn_formatar_parecer = ctk.CTkButton(self.frame_coluna1, text="Formatar Parecer", width=400, height=35, command=self.organizar_parecer)
        self.btn_formatar_parecer.grid(row=5, column=0, pady=(10, 10), padx=(10, 23), sticky="ew")

        # ==== Coluna 2 (com Frame para Botões) ====
        self.frame_coluna2 = ctk.CTkFrame(self)
        self.frame_coluna2.grid(row=0, column=2, padx=(5, 5), pady=10, sticky="nsew")

        self.btn_exibir_processos = ctk.CTkButton(self.frame_coluna2, text="Exibir Processos", command=self.organizar_exibir_processos, width=170)
        self.btn_exibir_processos.grid(row=2, column=0, pady=(5, 5), padx=(10, 10), sticky="w")   

        self.btn_check_list = ctk.CTkButton(self.frame_coluna2, width=170, text="Check List", command=self.tela_check_list)
        self.btn_check_list.grid(row=3, column=0, pady=(5, 5), padx=(10, 10), sticky="w")

        self.btn_obter_janelas = ctk.CTkButton(self.frame_coluna2, width=170, text="Obter Janelas", command=self.mostrar_jenelas)
        self.btn_obter_janelas.grid(row=4, column=0, pady=(5, 5), padx=(10, 10), sticky="w")

        self.btn_definir_telas = ctk.CTkButton(self.frame_coluna2, width=170, text="Definir telas", command=self.tela_definir_telas)
        self.btn_definir_telas.grid(row=5, column=0, pady=(5, 5), padx=(10, 10), sticky="w")

    
    def tela_editar_dados(self):
        self.app.nome = self.input_nome.get()
        caminho_arquivo = ler_arquivo(self.parent.caminho)

        # Validação dos dados antes de continuar
        if not self.validar_entrada_editar(self.app.nome, caminho_arquivo):
            return  

        # Obtém as informações do médico
        info_medico = exibir_info_medico(caminho_arquivo, self.app.nome)

        # Criar ou atualizar a janela de edição
        if not self.editar_dados:
            self.editar_dados = Editar_dados(self.app)
        else:
            self.editar_dados.entry_nome.configure(state="normal")
            self.editar_dados.entry_nome.delete(0, "end")  
            self.editar_dados.entry_nome.insert(0, self.app.nome)  
            self.editar_dados.textarea.delete("1.0", "end")  
            self.editar_dados.textarea.insert("1.0", info_medico) 
            self.editar_dados.entry_nome.configure(state="readonly")  

        self.editar_dados.deiconify()

    def coletar_dois(self):
        cordenada = f"{self.parent.caminho_pasta}/cordenadas.json"
        execut = verificador_telas(cordenada)
        if execut == True:
            self.quantidade_coletar_dados("dados 2")
        else:
            messagebox.showerror("Erro", "Por favor, Defina as talas antes de executar a coleta.")

    def quantidade_coletar_dados(self, tipo):
        cordenada = f"{self.parent.caminho_pasta}/cordenadas.json"
        if tipo == "dados 2":
            verificador_telas(cordenada)
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
            elif tipo == "dados 2":
                self.coletar_dados_dois(quantidade)
            elif tipo == "assistente":
                self.coletar_info_assistente(quantidade)

        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Por favor, insira um número inteiro válido.")

    def coletar_dados(self, quantidade):
        cordenada = f"{self.parent.caminho_pasta}/cordenadas.json"
        resultado = verificador_telas(cordenada)
        print(resultado)
        try:
            caminho = self.parent.caminho
            copy_vazio()
            for i in range(quantidade):
                dados = save_data(caminho, cordenada)

        except Exception as e:
            print(f"Erro em coletar_dados: {e}")

    def coletar_dados_dois(self, quantidade):
        cordenada = f"{self.parent.caminho_pasta}/cordenadas.json"
        try:
            caminho = self.parent.caminho
            for i in range(quantidade):
                dados = save_data_dois(caminho, cordenada)

        except Exception as e:
            print(f"Erro em coletar_dados: {e}")

    def coletar_info_assistente(self, quantidade):
        cordenada = f'{self.parent.caminho_pasta}/cordenadas.json'

        try:
            time.sleep(2)
            copy_vazio()
            caminho_coletar = self.parent.caminho
            for i in range(quantidade):
                dados = save_info_assistente(cordenada, caminho_coletar)
            
        except Exception as e:
            print(f"Erro em coletar_dados: {e}")

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

    def tela_check_list(self):
        if not self.check_list:
            self.check_list = Check_list(self)
        self.check_list.deiconify()

    def tela_definir_telas(self):
        if not self.definir_telas:
            self.definir_telas = Definir_tela(self)
        self.definir_telas.deiconify() 

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

    def organizar_nome_usuario(self):
        caminho_arquivo = f"{self.parent.caminho_pasta}/dados_coletados_padrao.json"
        df_caminho = ler_arquivo(caminho_arquivo)

        if df_caminho is not None:
            resultado = exibir_usuarios_padrao(df_caminho)
            self.textarea_texto.delete('0.0', 'end')
            self.textarea_texto.insert('0.0', f'{resultado}')
        else:
            self.textarea_texto.insert('0.0', "Nenhum dado encontrado")
    
    def organizar_exibir_processos(self):
        df_sheet_processos = carregar_dados_sheet_processos()

        if df_sheet_processos.empty:
            self.textarea_texto.delete('0.0', 'end')
            self.textarea_texto.insert('0.0', "nenhum dado encontrado")
        else:
            resultado = exibir_processos(df_sheet_processos)
            self.textarea_texto.delete('0.0', 'end')
            self.textarea_texto.insert('0.0', f'{resultado}')

    def organizar_parecer(self):
        nome_digitado = self.input_nome.get()

        df_caminho = ler_arquivo(self.parent.caminho)
        if df_caminho is not None:
            resultado = processar_parecer_nome(df_caminho, nome_digitado)
            self.textarea_texto.delete('0.0', 'end')
            self.textarea_texto.insert('0.0', f'{resultado}')
        else:
            print("nenhum dado carregado")

    def mostrar_jenelas(self):
        janelas = obter_telas()

        self.textarea_texto.delete('0.0', "end")
        self.textarea_texto.insert('0.0', janelas)

    def validar_entrada_editar(self, nome, df):
    
        if not nome:
            messagebox.showwarning("Aviso", "Nenhum nome foi digitado.")
            return False

        if df is None or df.empty:
            messagebox.showwarning("Aviso", "Nenhum dado encontrado no arquivo.")
            return False

        if "nome" not in df.columns:
            messagebox.showwarning("Erro", "A coluna 'nome' não foi encontrada no arquivo.")
            return False

        if not (df["nome"] == nome).any():
            messagebox.showwarning("Aviso", "Nome não encontrado no arquivo.")
            return False

        return True 

    def validar_entrada(self, nome_digitado, df_caminho, textarea, mensagem_vazia="Nenhum nome foi digitado.", mensagem_df_vazio="Nenhum dado encontrado."):

        if not nome_digitado:
            mensagem = mensagem_vazia
        elif df_caminho is None or df_caminho.empty:
            mensagem = mensagem_df_vazio
        else:
            return True 

        textarea.delete('0.0', 'end')
        textarea.insert('0.0', mensagem)
        return False  


if __name__ == "__main__":
    app = App("DATAFORMAT", "1000x700")
    app.mainloop()



