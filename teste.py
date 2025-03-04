from datetime import datetime

# Pegar a data e hora atual e formatar
agora = datetime.now()
agora_formatado = agora.strftime("%Y-%m-%d %H:%M")

# Exibir a data e hora formatada sem os segundos
print("Data e hora atual sem segundos:", agora_formatado)