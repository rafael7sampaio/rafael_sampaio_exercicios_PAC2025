import json
import socket
import threading


HOST = "127.0.0.1"
PORT = 5555


def display_message(payload: dict) -> None:
    msg_type = payload.get("type", "")

    if msg_type == "chat":
        print(f"\n[{payload['from']}] {payload['message']}")
    elif msg_type == "private":
        print(f"\n[PRIVADO de {payload['from']}] {payload['message']}")
    elif msg_type == "group":
        print(f"\n[GRUPO:{payload['group']} | {payload['from']}] {payload['message']}")
    elif msg_type == "system":
        print(f"\n[SISTEMA] {payload['message']}")
    elif msg_type == "blocked":
        print(f"\n[BLOQUEADA] {payload['message']}")
        details = payload.get("details", {})
        if details:
            print("[DETALHES]")
            for key, value in details.items():
                print(f" - {key}: {value}")
    elif msg_type == "error":
        print(f"\n[ERRO] {payload['message']}")
    else:
        print(f"\n{payload}")


def receive_messages(client_socket: socket.socket) -> None:
    buffer = ""

    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                print("\n[INFO] Ligação ao servidor terminada.")
                break

            buffer += data.decode("utf-8")

            while "\n" in buffer:
                raw_message, buffer = buffer.split("\n", 1)

                if raw_message.strip():
                    try:
                        payload = json.loads(raw_message)
                        display_message(payload)
                    except json.JSONDecodeError:
                        print(raw_message)

        except Exception:
            print("\n[ERRO] Não foi possível receber mensagens do servidor.")
            break


def start_client() -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print(f"Ligado ao servidor {HOST}:{PORT}")
    except Exception as error:
        print(f"Não foi possível ligar ao servidor: {error}")
        return

    try:
        welcome = client_socket.recv(1024).decode("utf-8")
        try:
            payload = json.loads(welcome.strip())
            print(f"[SISTEMA] {payload['message']}")
        except Exception:
            print(welcome)

        username = input("Nome de utilizador: ").strip()
        client_socket.sendall(username.encode("utf-8"))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
        receive_thread.start()

        while True:
            message = input()

            if not message.strip():
                continue

            client_socket.sendall((message + "\n").encode("utf-8"))

            if message.lower() == "exit":
                break

    except KeyboardInterrupt:
        print("\nA sair...")
        try:
            client_socket.sendall(b"exit\n")
        except Exception:
            pass
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
