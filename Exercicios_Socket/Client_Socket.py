# ==========================================
# CLIENTE TCP EM PYTHON
# Ligação a um servidor usando SOCKET
# ==========================================

import socket     # biblioteca para comunicação em rede

# -------------------------------
# 1. CRIAR A SOCKET
# -------------------------------
# AF_INET  -> usa IPv4
# SOCK_STREAM -> usa protocolo TCP

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -------------------------------
# 2. DEFINIR DADOS DO SERVIDOR
# -------------------------------

host = "127.0.0.1"   # endereço do servidor (localhost)
porta = 12340        # porta do servidor

# -------------------------------
# 3. CONECTAR AO SERVIDOR
# -------------------------------

clientSocket.connect((host, porta))
print("Ligado ao servidor!")

# ---------------------------------------------------------------
# 4. ENVIAR MENSAGEM AO SERVIDOR + RECEBER RESPOSTA DO SERVIDOR
# ---------------------------------------------------------------
# encode() converte string para bytes
# recv(1024) -> recebe até 1024 bytes
# decode() -> converte bytes para string

while True:
    mensagem = input("Cliente: ")
    clientSocket.send(mensagem.encode())

    if mensagem == "sair":
        print("Cliente terminou a conexão.")
        break

    resposta = clientSocket.recv(1024).decode()

    if resposta == "sair":
        print("Servidor terminou a conexão.")
        break

    print("Servidor:", resposta)

# -------------------------------
# 5. FECHAR A CONEXÃO
# -------------------------------

clientSocket.close()
print("Conexão fechada.")