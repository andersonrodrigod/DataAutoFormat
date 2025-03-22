import pywinctl

def listar_janelas():
    try:
        # Obtém todas as janelas abertas
        janelas = pywinctl.getAllWindows()
        
        if janelas:
            print("Janelas abertas:")
            for janela in janelas:
                print(janela.title)
        else:
            print("Nenhuma janela aberta encontrada.")
    except Exception as e:
        print(f'Ocorreu um erro: {e}')

# Teste para listar todas as janelas abertas
listar_janelas()