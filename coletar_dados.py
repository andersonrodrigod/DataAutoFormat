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

def garantir_copia_info():
    tentativas = 0
    while tentativas < 7:
        py.hotkey("ctrl", "c")  
        time.sleep(0.3)

        texto_copiado = pyperclip.paste()
        if texto_copiado:
            return texto_copiado

        tentativas += 1
        #print(f"Tentativa {tentativas}: Área de transferência vazia. Tentando copiar novamente...")

    #print("Falha ao copiar. Pressionando Enter duas vezes...")
    return None

    

def garantir_copia():
    tentativas = 0
    while tentativas < 7:
        if pyperclip.paste():
            return
        copy()
        time.sleep(0.3)
        tentativas += 1

    if not pyperclip.paste():
        raise RuntimeError("Falha ao copiar o texto após 7 tentativas.")

def copy_vazio():
    pyperclip.copy("")

def copy_info():
    py.hotkey("ctrl", "c")
    garantir_copia_info()

def copy():
    py.hotkey("ctrl", "c")
    garantir_copia()

def tab():
    py.press("tab")

def shift_tab():
    py.hotkey("shift", "tab")

def copy_click(x, y):
    py.click(x, y)
    time.sleep(0.3)
    py.hotkey("ctrl", "c")
    garantir_copia()

def copy_click_info(x, y):
    py.click(x, y)
    time.sleep(0.3)
    py.hotkey("ctrl", "c")
    garantir_copia_info()


def carregar_dados_existentes(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados_existentes = json.load(f)

    return dados_existentes

def salvar_dados(dados_existentes, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados_existentes, f, indent=4, ensure_ascii=False)

def editar_dados(codigo, atualizacoes, caminho_arquivo):
    dados = carregar_dados_existentes(caminho_arquivo)

    for usuario in dados:
        if usuario.get("codigo") == codigo:
            for chave, novo_valor in atualizacoes.items():
                if isinstance(usuario.get(chave), list):
                    usuario[chave].append(novo_valor)
                else:
                    usuario[chave] = novo_valor
            
            break

    
    salvar_dados(dados, caminho_arquivo)



def save_data(caminho_arquivo, cordenadas_caminho):

    processando_cordenadas = carregar_cordenada(cordenadas_caminho)

    cordenada_codigo_carteira, cordenada_info_medico, cordenada_info_assistente, cordenada_codigo_procedimento, codigo_carteira_t, telefone_1, telefone_2, telefone_3, telefone_baixo, amop, t22a3 = processando_cordenadas

    cordenada_codigo_carteira_x, cordenada_codigo_carteira_y = cordenada_codigo_carteira
    
    cordenada_info_medico_x, cordenada_info_medico_y = cordenada_info_medico

    cordenada_info_assistente_x, cordenada_info_assistente_y = cordenada_info_assistente 

    cordenada_codigo_procedimento_x, cordenada_codigo_procedimento_y = cordenada_codigo_procedimento

    try:
        dados_existentes = carregar_dados_existentes(caminho_arquivo)

        df = pd.DataFrame(dados_existentes)

        
        copy()
        codigo = cod()

        copy_vazio()
        tab()

        copy()
        nome = name()

        copy_vazio()

        copy_click(cordenada_codigo_procedimento_x, cordenada_codigo_procedimento_y)
        codigo_procedimento = cod_proc()

        if not df.empty and "codigo" in df.columns and codigo in df["codigo"].values:
            codigo_in_dados = df[df["codigo"] == codigo]
            procedimento_in_dados = codigo_in_dados["codigo_procedimento"].values
            if codigo_procedimento in procedimento_in_dados:
                #print("código em banco de dados")
                py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
                py.press("down")
                return

        copy_vazio()
        tab()

        copy()
        nome_procedimento = name_proc()

        copy_vazio()
        tab()
        tab()

        copy()
        medico_solicitante = medico_requesting()

        copy_vazio()

        copy_click_info(cordenada_info_assistente_x, cordenada_info_assistente_y)
        info_assistente = info_assistent()

        copy_vazio()

        copy_click_info(cordenada_info_medico_x, cordenada_info_medico_y)
        info_medic = info_medico()

        copy_vazio()

        py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
        py.press("down")

        dados = {
            "codigo": codigo,
            "nome": nome,
            "codigo_procedimento": f"{codigo_procedimento}",
            "nome_procedimento": nome_procedimento,
            "info_assistente": f"{info_assistente}.",
            "info_medico": f"{info_medic}.",
            "medico_solicitante": medico_solicitante,
        }

        dados_existentes.append(dados)

        salvar_dados(dados_existentes, caminho_arquivo)

        return dados

    except Exception as e:
        print(f"Erro em save_data: {e}")
        import traceback
        traceback.print_exc()
        raise

def save_data_analitics(caminho_arquivo, cordenadas_caminho):

    processando_cordenadas = carregar_cordenada(cordenadas_caminho)

    cordenada_codigo_carteira, cordenada_info_medico, cordenada_info_assistente, cordenada_codigo_procedimento, codigo_carteira_t, telefone_1, telefone_2, telefone_3, telefone_baixo, amop, t22a3 = processando_cordenadas

    cordenada_codigo_carteira_x, cordenada_codigo_carteira_y = cordenada_codigo_carteira
    
    cordenada_info_medico_x, cordenada_info_medico_y = cordenada_info_medico

    cordenada_info_assistente_x, cordenada_info_assistente_y = cordenada_info_assistente 

    cordenada_codigo_procedimento_x, cordenada_codigo_procedimento_y = cordenada_codigo_procedimento

    fuso_horario = timezone("America/Sao_Paulo")
    agora = datetime.now(fuso_horario)
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M")

    try:
        dados_existentes = carregar_dados_existentes(caminho_arquivo)

        df = pd.DataFrame(dados_existentes)

        
        copy()
        codigo = cod()

        copy_vazio()
        tab()

        copy()
        nome = name()

        copy_vazio()

        copy_click(cordenada_codigo_procedimento_x, cordenada_codigo_procedimento_y)
        codigo_procedimento = cod_proc()

        if not df.empty and "codigo" in df.columns and codigo in df["codigo"].values:
            codigo_in_dados = df[df["codigo"] == codigo]
            procedimento_in_dados = codigo_in_dados["codigo_procedimento"].values
            if codigo_procedimento in procedimento_in_dados:
                #print("código em banco de dados")
                copy_click_info(cordenada_info_assistente_x, cordenada_info_assistente_y)
                info_assistente = info_assistent()
                copy_vazio()
                
                copy_click_info(cordenada_info_medico_x, cordenada_info_medico_y)
                info_medic = info_medico()
                copy_vazio()

                atualizacoes = {
                    "info_assistente": f"{info_assistente}.",
                    "info_medico": f"{info_medic}.",
                    "data_hora_bot": f"{data} {hora}"
                }

                editar_dados(codigo, atualizacoes, caminho_arquivo)

                py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
                py.press("down")
                return

        copy_vazio()
        tab()

        copy()
        nome_procedimento = name_proc()

        copy_vazio()
        tab()
        tab()

        copy()
        medico_solicitante = medico_requesting()

        copy_vazio()

        copy_click_info(cordenada_info_assistente_x, cordenada_info_assistente_y)
        info_assistente = info_assistent()

        copy_vazio()

        copy_click_info(cordenada_info_medico_x, cordenada_info_medico_y)
        info_medic = info_medico()

        copy_vazio()

        py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
        py.press("down")

        dados = {
            "codigo": codigo,
            "nome": nome,
            "codigo_procedimento": f"{codigo_procedimento}",
            "nome_procedimento": nome_procedimento,
            "info_assistente": f"{info_assistente}.",
            "info_medico": f"{info_medic}.",
            "medico_solicitante": medico_solicitante,
            "data_hora_bot": [f"{data} {hora}"]
        }

        dados_existentes.append(dados)

        salvar_dados(dados_existentes, caminho_arquivo)

        return dados

    except Exception as e:
        print(f"Erro em save_data: {e}")
        import traceback
        traceback.print_exc()
        raise






def save_info_assistente(caminho_arquivo, cordenadas, caminho_coletar_dados):

    processando_cordenadas = carregar_cordenada(cordenadas)

    cordenada_codigo_carteira, cordenada_info_medico, cordenada_info_assistente, cordenada_codigo_procedimento, codigo_carteira_t, telefone_1, telefone_2, telefone_3, telefone_baixo, amop, t22a3 = processando_cordenadas

    cordenada_codigo_carteira_x, cordenada_codigo_carteira_y = cordenada_codigo_carteira

    cordenada_info_assistente_x, cordenada_info_assistente_y = cordenada_info_assistente

    dados_existentes = carregar_dados_existentes(caminho_arquivo)

    fuso_horario = timezone("America/Sao_Paulo")
    agora = datetime.now(fuso_horario)
    data = agora.strftime("%Y-%m-%d")
    hora = agora.strftime("%H:%M")

    copy()

    codigo = cod()

    copy_vazio()

    dados = dados_existentes

    df = pd.DataFrame(dados)

    #print(df)

    if not df.empty and "codigo" in df.columns and codigo in df["codigo"].values:
        codigo_in_processo = df[df["codigo"] == codigo]
        tipo_in_processo = codigo_in_processo["tipo"].values[0]
        removido_atual = codigo_in_processo["removido"].values[0]


        copy_click_info(cordenada_info_assistente_x, cordenada_info_assistente_y)
        info_assistente = info_assistent()
        palavra_encontrada = encontrar_palavra(palavras_info_assistente, info_assistente)
        palavra_processo = obter_palavra(palavra_encontrada, mapeamento_palavras_info_assistente)


        if palavra_processo == tipo_in_processo:
            atualizacoes = {
                "data_hora_bot": f"{data} {hora}"
            }

            if removido_atual:
                atualizacoes["removido"] = False

            editar_dados(codigo, atualizacoes, caminho_arquivo)
            py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
            time.sleep(0.5)
            py.press("down")
            #print("Código já está no banco de dados e tipo é o mesmo, apenas clicando.")
        else:
            atualizacoes = {
                "tipo": palavra_processo,
                "data_hora_bot": f"{data} {hora}"
            }

            if removido_atual:
                atualizacoes["removido"] = False
            
            editar_dados(codigo, atualizacoes, caminho_arquivo)

            py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
            time.sleep(0.5)
            py.press("down")
            #print("Código já está no banco de dados, tipo atualizado.")
    else:
        copy_click_info(cordenada_info_assistente_x, cordenada_info_assistente_y)
        info_assistente = info_assistent()
        copy_vazio()

        palavra_encontrada = encontrar_palavra(palavras_info_assistente, info_assistente)
        palavra_encontrada = obter_palavra(palavra_encontrada, mapeamento_palavras_info_assistente)

        palavra_processo = palavra_encontrada

        py.click(cordenada_codigo_carteira_x, cordenada_codigo_carteira_y)
        time.sleep(0.5)

        tab()
        copy()
        nome = name()

        shift_tab()
        


        processos = {
            "codigo": codigo,
            "nome": nome,
            "tipo": palavra_processo,
            "data": data,
            "hora": hora,
            "data_hora_bot": [f"{data} {hora}"],
            "visto": False,
            "verificar": False,
            "resolvido": False,
            "removido": False,
            "visto_data_hora": [],
            "resolvido_data_hora": []
        }


        dados_existentes.append(processos)

        salvar_dados(dados_existentes, caminho_arquivo)

        if palavra_processo == "PRIMEIRO CONTATO":
            save_data(caminho_coletar_dados, cordenadas)
        else:
            py.press("down")
        

    
