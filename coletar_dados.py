import pyperclip
import os
import pyautogui as py
import time
import json
import pandas as pd
import pygetwindow as gw
from cordenadas import carregar_cordenada
from palavras import todos_codigos, block_padrao, palavras_info_assistente, mapeamento_palavras_info_assistente
from funcoes import encontrar_palavra, obter_palavra
from datetime import datetime
from planilhas import sheet_processos, sheet_coletar_dados, carregar_dados_sheet_processos
from pytz import timezone


def cod():
    return pyperclip.paste()

def name():
    return pyperclip.paste()

def cod_proc():
    return pyperclip.paste()

def name_proc():
    return pyperclip.paste()

def medico_requesting():
    return pyperclip.paste()

def info_assistent():
    return pyperclip.paste()

def info_medico():
    return pyperclip.paste()

def telefone():
    return pyperclip.paste()



def garantir_copia():
    """Verifica se há algo na área de transferência. Se não houver, tenta copiar novamente até 5 vezes.
    Se falhar, pressiona Enter duas vezes e encerra a função.
    """
    tentativas = 0
    while tentativas < 7:
        if pyperclip.paste():
            print("Texto copiado com sucesso!")
            return  # Sai da função se a cópia for bem-sucedida
        print(f"Tentativa {tentativas + 1}: Área de transferência vazia. Tentando copiar novamente...")
        copy()  # Chama novamente a função de cópia
        time.sleep(0.3)
        tentativas += 1

    print("Falha ao copiar. Pressionando Enter duas vezes...")
    py.press('enter')
    py.press('enter')

def focar_janela(nome_janela):
    janela = gw.getWindowsWithTitle(nome_janela)

    if janela:
        janela[0].activate()
    else:
        print(f"Janela com título '{nome_janela}' não encontrada.")


def copy_vazio():
    pyperclip.copy("")

def copy():
    py.hotkey("ctrl", "c")

def copy_tab():
    py.hotkey("ctrl", "c")
    garantir_copia()
    py.press("tab")

def tab_copy():
    py.press("tab")
    time.sleep(0.5)
    py.hotkey("ctrl", "c")
    garantir_copia()

def shift_tab():
    py.hotkey("shift", "tab")

def copy_click(x, y):
    py.click(x, y)
    py.hotkey("ctrl", "c")
    garantir_copia()

def copy_tab_proc():
    time.sleep(0.5)
    py.hotkey("ctrl", "c")
    time.sleep(0.5)


def carregar_dados_existentes(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados_existentes = json.load(f)
            max_id = 0
            if dados_existentes:
                for item in dados_existentes:
                    if item["id"] > max_id:
                        max_id = item["id"]
    else:
        dados_existentes = []
        max_id = 0
    return dados_existentes, max_id

def salvar_dados(dados_existentes, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados_existentes, f, indent=4, ensure_ascii=False)

def save_data(caminho_arquivo, cordenadas_caminho):

    processando_cordenadas = carregar_cordenada(cordenadas_caminho)

    cordenada_codigo_carteira, cordenada_info_medico, cordenada_info_assistente, cordenada_codigo_procedimento, c_codigo_carteira_t, c_telefone_1, c_telefone_2, c_telefone_3, c_telefone_baixo, amop, t22a3 = processando_cordenadas

    cordenada_codigo_carteira_x, cordenada_codigo_carteira_y = cordenada_codigo_carteira
    
    cordenada_info_medico_x, cordenada_info_medico_y = cordenada_info_medico

    cordenada_info_assistente_x, cordenada_info_assistente_y = cordenada_info_assistente 

    cordenada_codigo_procedimento_x, cordenada_codigo_procedimento_y = cordenada_codigo_procedimento

    try:
        dados_existentes, max_id = carregar_dados_existentes(caminho_arquivo)
        id_count = max_id + 1

        copy_tab()
        codigo = cod()

        copy_tab()
        nome = name()

        copy_click(cordenada_codigo_procedimento_x, cordenada_codigo_procedimento_y)
        codigo_procedimento = cod_proc()

        copy_tab()
        nome_procedimento = name_proc()

        py.press("tab")
        copy_tab()
        medico_solicitante = medico_requesting()

        copy_tab()
        copy_click(cordenada_info_assistente_x, cordenada_info_assistente_y)
        info_assistente = info_assistent()

        copy_click(cordenada_info_medico_x, cordenada_info_medico_y)
        info_medic = info_medico()

        py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
        py.press("down")

        dados = {
            "id": id_count,
            "codigo": codigo,
            "nome": nome,
            "codigo_procedimento": codigo_procedimento,
            "nome_procedimento": nome_procedimento,
            "info_assistente": f"{info_assistente}.",
            "info_medico": f"{info_medic}.",
            "medico_solicitante": medico_solicitante
        }

        dados_sheet = [
            [codigo, nome, codigo_procedimento, nome_procedimento, info_assistente, info_medic, medico_solicitante]
        ]

        dados_existentes.append(dados)
        sheet_coletar_dados.append_rows(dados_sheet)
        salvar_dados(dados_existentes, caminho_arquivo)

        return dados

    except Exception as e:
        print(f"Erro em save_data: {e}")
        import traceback
        traceback.print_exc()
        raise

def save_telefones(telefone_1x, telefone_1y, telefone_2x, telefone_2y, telefone_3x, telefone_3y, telefone_baixo_x, telefone_baixo_y):


    telefones = set() 

    tentativas = 0


    for x, y in [(telefone_1x, telefone_1y), (telefone_2x, telefone_2y), (telefone_3x, telefone_3y)]:
        copy_click(x, y) 
        
        tel = telefone()  

        if not tel:  
            print("Clipboard vazio. Parando a coleta.")
            return telefones  

        telefones.add(tel)

        if len(telefones) >= 3: 
            print("Coleta concluída com 3 telefones diferentes.")
            return telefones  
            
    while len(telefones) < 3:
        if tentativas >= 5:  
            print("Máximo de 5 tentativas atingido. Encerrando a coleta.")
            return telefones 
        
        py.click(telefone_baixo_x, telefone_baixo_y)
        time.sleep(0.5)
        copy_click(telefone_3x, telefone_3y)
        tel = telefone()

        if not tel:
            print("Clipboard vazio. Parando a coleta.")
            return telefones  

        telefones.add(tel)

        if len(telefones) >= 3: 
            print("Coleta concluída com 3 telefones diferentes.")
            return telefones 

        tentativas += 1  

    return telefones


def coletar_dados_telefones_t22a3(caminho_arquivo, cordenadas_caminho, codigo):
        
    processando_cordenadas = carregar_cordenada(cordenadas_caminho)

    c_codigo_carteira, c_info_medico, c_info_assistente, codigo_procedimento, c_codigo_carteira_t, c_telefone_1, c_telefone_2, c_telefone_3, c_telefone_baixo, amop, t22a3 = processando_cordenadas

    cordenada_codigo_carteira_x, cordenada_codigo_carteira_y = c_codigo_carteira
    cordenada_info_medico_x, cordenada_info_medico_y = c_info_medico
    cordenada_info_assistente_x, cordenada_info_assistente_y = c_info_assistente
    codigo_carteira_tx, codigo_carteira_ty = c_codigo_carteira_t
    telefone_1x, telefone_1y = c_telefone_1
    telefone_2x, telefone_2y = c_telefone_2
    telefone_3x, telefone_3y = c_telefone_3
    telefone_baixo_x, telefone_baixo_y = c_telefone_baixo


    pyperclip.copy(codigo)
    time.sleep(1)
    py.press(codigo_carteira_tx, codigo_carteira_ty)
    time.sleep(0.5)
    py.hotkey("ctrl", "v")
    time.sleep(0.5)
    py.press("f8")
    time.sleep(0.5)

    telefones = save_telefones(telefone_1x, telefone_1y, telefone_2x, telefone_2y, telefone_3x, telefone_3y, telefone_baixo_x, telefone_baixo_y)


def save_data_dois(caminho_arquivo, cordenadas_caminho):

    processando_cordenadas = carregar_cordenada(cordenadas_caminho)

    c_codigo_carteira, c_info_medico, c_info_assistente, codigo_procedimento, c_codigo_carteira_t, c_telefone_1, c_telefone_2, c_telefone_3, c_telefone_baixo, amop, t22a3 = processando_cordenadas

    cordenada_codigo_carteira_x, cordenada_codigo_carteira_y = c_codigo_carteira
    cordenada_info_medico_x, cordenada_info_medico_y = c_info_medico
    cordenada_info_assistente_x, cordenada_info_assistente_y = c_info_assistente
    codigo_carteira_tx, codigo_carteira_ty = c_codigo_carteira_t
    telefone_1x, telefone_1y = c_telefone_1
    telefone_2x, telefone_2y = c_telefone_2
    telefone_3x, telefone_3y = c_telefone_3
    telefone_baixo_x, telefone_baixo_y = c_telefone_baixo




    try:
        dados_existentes, max_id = carregar_dados_existentes(caminho_arquivo)
        id_count = max_id + 1

        copy_tab()
        codigo = cod()

        copy_tab()
        nome = name()

        for _ in range(3):
            time.sleep(0.2)
            py.press("tab")

        copy_tab()
        codigo_procedimento = cod_proc()

        copy_tab()
        nome_procedimento = name_proc()

        py.press("tab")
        copy_tab()
        medico_solicitante = medico_requesting()

        copy_tab()
        copy_click(cordenada_info_assistente_x, cordenada_info_assistente_y)
        info_assistente = info_assistent()

        copy_click(cordenada_info_medico_x, cordenada_info_medico_y)
        info_medic = info_medico()

        focar_janela(t22a3)

        py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
        py.press("down")

        dados = {
            "id": id_count,
            "codigo": codigo,
            "nome": nome,
            "codigo_procedimento": codigo_procedimento,
            "nome_procedimento": nome_procedimento,
            "info_assistente": f"{info_assistente}.",
            "info_medico": f"{info_medic}.",
            "medico_solicitante": medico_solicitante,
        }

        dados_sheet = [
            [codigo, nome, codigo_procedimento, nome_procedimento, info_assistente, info_medic, medico_solicitante]
        ]

        dados_existentes.append(dados)
        sheet_coletar_dados.append_rows(dados_sheet)
        salvar_dados(dados_existentes, caminho_arquivo)

        return dados

    except Exception as e:
        print(f"Erro em save_data: {e}")
        import traceback
        traceback.print_exc()
        raise


def carregar_dados(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
        return dados 

def save_info_assistente(cordenadas, caminho_coletar):

    processando_cordenadas = carregar_cordenada(cordenadas)

    cordenada_codigo_carteira, cordenada_info_medico, cordenada_info_assistente, cordenada_codigo_procedimento, c_codigo_carteira_t, c_telefone_1, c_telefone_2, c_telefone_3, c_telefone_baixo, amop, t22a3 = processando_cordenadas

    cordenada_codigo_carteira_x, cordenada_codigo_carteira_y = cordenada_codigo_carteira

    cordenada_info_assistente_x, cordenada_info_assistente_y = cordenada_info_assistente

    copy()
    garantir_copia()

    codigo = cod()
    copy_vazio()

    dados = carregar_dados_sheet_processos()

    df = pd.DataFrame(dados)

    if not df.empty and codigo in df["codigo"].values:
         # Encontrar a linha do código na planilha
        index = dados[dados["codigo"] == codigo].index[0]
        tipo_atual = dados.at[index, "tipo"]

        print(tipo_atual)
        # Verifica se a palavra_processo é igual ao tipo existente
        copy_click(cordenada_info_assistente_x, cordenada_info_assistente_y)
        garantir_copia()
        info_assistente = info_assistent()
        copy_vazio()
        palavra_encontrada = encontrar_palavra(palavras_info_assistente, info_assistente)
        palavra_processo = obter_palavra(palavra_encontrada, mapeamento_palavras_info_assistente)

        if palavra_processo == tipo_atual:
            py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)       
            time.sleep(0.5)
            py.press("down")
            print("Código já está no banco de dados e tipo é o mesmo, apenas clicando.")
        else:
            sheet_processos.update_cell(index + 2, 3, palavra_processo)  # Atualiza a célula correspondente
            py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
            time.sleep(0.5)
            py.press("down")
            print("Código já está no banco de dados, tipo atualizado.")
    else:
        copy_click(cordenada_info_assistente_x, cordenada_info_assistente_y)
        garantir_copia()
        info_assistente = info_assistent()
        copy_vazio()

        palavra_encontrada = encontrar_palavra(palavras_info_assistente, info_assistente)
        palavra_encontrada = obter_palavra(palavra_encontrada, mapeamento_palavras_info_assistente)

        palavra_processo = palavra_encontrada

        py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
        time.sleep(0.5)

        tab_copy()
        garantir_copia()
        nome = name()
        copy_vazio()

        shift_tab()

        fuso_horario = timezone("America/Sao_Paulo")
        agora = datetime.now(fuso_horario)

        data = agora.strftime("%Y-%m-%d")
        hora = agora.strftime("%H:%M")

        usuario_sheet = [
            [nome, codigo, palavra_processo, data, hora, False, False, False]
        ]

        #dados.append(usuario)
        sheet_processos.append_rows(usuario_sheet)
        #salvar_processo(caminho, dados)

        if palavra_processo == "SEM OBSERVACAO":
            save_data(caminho_coletar, cordenadas)

def save_info_contato(cordenadas):
    processando_cordenadas = carregar_cordenada(cordenadas)