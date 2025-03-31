import pygetwindow as gw
import pyautogui
import time

def focar_janela(titulo):
    janela = gw.getWindowsWithTitle(titulo)
    
    if janela:
        janela[0].activate()  # Ativa a janela encontrada
    else:
        print(f"Janela com título '{titulo}' não encontrada.")

# Exemplo de uso
time.sleep(2)  # Dá tempo para a janela ser aberta antes de ativar
focar_janela("Bloco de Notas")  # Substitua pelo título da sua janela
