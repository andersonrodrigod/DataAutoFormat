import pyperclip
import os
import pyautogui as py
import time
import json
import pandas as pd
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

def garantir_copia():
    """Verifica se há algo na área de transferência, se não houver, tenta copiar novamente."""
    while not pyperclip.paste():
        print("Área de transferência vazia. Tentando copiar novamente...")
        copy()  # Chama novamente a função de cópia
        time.sleep(0.3)

def copy_vazio():
    pyperclip.copy("")

def copy():
    py.hotkey("ctrl", "c")

def copy_tab():
    py.hotkey("ctrl", "c")
    time.sleep(0.5)
    py.press("tab")
    time.sleep(0.5)

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

    cordenada_codigo_carteira, cordenada_info_medico, cordenada_info_assistente, cordenada_codigo_procedimento = processando_cordenadas

    cordenada_codigo_carteira_x, cordenada_codigo_carteira_y = cordenada_codigo_carteira
    
    cordenada_info_medico_x, cordenada_info_medico_y = cordenada_info_medico

    cordenada_info_assistente_x, cordenada_info_assistente_y = cordenada_info_assistente 

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

def save_dados_padrao(caminho_coletar_padrao, cordernadas):
    
    processando_cordenadas = carregar_cordenada(cordernadas)

    cordenada_codigo_carteira, cordenada_info_medico, cordenada_info_assistente, cordenada_codigo_procedimento = processando_cordenadas

    cordenada_info_assistente_x, cordenada_info_assistente_y = cordenada_info_assistente 

    cordenada_codigo_carteira_x, cordenada_codigo_carteira_y = cordenada_codigo_carteira

    cordenada_codigo_procedimento_x, cordenada_codigo_procedimento_y = cordenada_codigo_procedimento

    copy_tab_proc()
    codigo_procedimento = cod_proc()
    if codigo_procedimento in todos_codigos:
        copy_click(cordenada_info_assistente_x, cordenada_info_assistente_y)
        info_assistente = info_assistent()
        if not any(item in info_assistente for item in block_padrao):
            py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
            time.sleep(0.5)
            save_data(caminho_coletar_padrao, cordernadas)
            py.click(cordenada_codigo_procedimento_x, cordenada_codigo_procedimento_y)
            time.sleep(0.5)
        else:
            py.click(cordenada_codigo_procedimento_x, cordenada_codigo_procedimento_y)
            py.press("down")
    else:
        py.press("down")

def carregar_dados(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
        return dados 

def salvar_processo(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f'Dado adicionado com sucesso!')

def save_info_assistente(cordenadas, caminho_coletar):

    processando_cordenadas = carregar_cordenada(cordenadas)

    cordenada_codigo_carteira, cordenada_info_medico, cordenada_info_assistente, cordenada_codigo_procedimento = processando_cordenadas

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

    
