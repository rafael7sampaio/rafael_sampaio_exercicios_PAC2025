import json
import logging
import os
import socket
import threading

from detector import detect_personal_data, detect_suspicious_social_engineering


HOST = "127.0.0.1"
PORT = 5555

clients = {}
groups = {}
clients_lock = threading.Lock()

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "server.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

personal_logger = logging.getLogger("personal_data_logger")
personal_handler = logging.FileHandler(os.path.join(LOG_DIR, "personal_data.log"), encoding="utf-8")
personal_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
personal_logger.addHandler(personal_handler)
personal_logger.setLevel(logging.WARNING)

suspicious_logger = logging.getLogger("suspicious_logger")
suspicious_handler = logging.FileHandler(os.path.join(LOG_DIR, "suspicious.log"), encoding="utf-8")
suspicious_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
suspicious_logger.addHandler(suspicious_handler)
suspicious_logger.setLevel(logging.WARNING)


def send_json(client_socket: socket.socket, data: dict) -> None:
    """Envia um dicionário em formato JSON para o cliente."""
    try:
        message = json.dumps(data).encode("utf-8")
        client_socket.sendall(message + b"\n")
    except Exception as error:
        logging.error("Erro ao enviar JSON: %s", error)


def broadcast(data: dict, exclude_socket: socket.socket | None = None) -> None:
    """Envia uma mensagem para todos os clientes ligados, exceto um opcional."""
    disconnected = []

    with clients_lock:
        for client_socket in list(clients.keys()):
            if client_socket != exclude_socket:
                try:
                    send_json(client_socket, data)
                except Exception as error:
                    logging.error("Erro no broadcast: %s", error)
                    disconnected.append(client_socket)

    for sock in disconnected:
        remove_client(sock)


def send_private_message(sender_socket: socket.socket, target_username: str, text: str) -> None:
    sender_name = clients[sender_socket]["username"]

    with clients_lock:
        for client_socket, info in clients.items():
            if info["username"] == target_username:
                send_json(client_socket, {
                    "type": "private",
                    "from": sender_name,
                    "message": text,
                })
                send_json(sender_socket, {
                    "type": "system",
                    "message": f"Mensagem privada enviada para {target_username}.",
                })
                return

    send_json(sender_socket, {
        "type": "error",
        "message": f"Utilizador '{target_username}' não encontrado.",
    })


def send_group_message(sender_socket: socket.socket, group_name: str, text: str) -> None:
    sender_name = clients[sender_socket]["username"]

    if group_name not in groups:
        send_json(sender_socket, {
            "type": "error",
            "message": f"Grupo '{group_name}' não existe.",
        })
        return

    members = groups[group_name]
    sent = False

    with clients_lock:
        for client_socket, info in clients.items():
            if info["username"] in members and client_socket != sender_socket:
                send_json(client_socket, {
                    "type": "group",
                    "group": group_name,
                    "from": sender_name,
                    "message": text,
                })
                sent = True

    if sent:
        send_json(sender_socket, {
            "type": "system",
            "message": f"Mensagem enviada para o grupo '{group_name}'.",
        })
    else:
        send_json(sender_socket, {
            "type": "error",
            "message": f"Nenhum membro ativo no grupo '{group_name}'.",
        })


def create_group(sender_socket: socket.socket, group_name: str, members: list[str]) -> None:
    creator = clients[sender_socket]["username"]
    member_set = set(members)
    member_set.add(creator)
    groups[group_name] = member_set

    send_json(sender_socket, {
        "type": "system",
        "message": f"Grupo '{group_name}' criado com membros: {', '.join(sorted(member_set))}",
    })


def list_users(client_socket: socket.socket) -> None:
    with clients_lock:
        usernames = [info["username"] for info in clients.values()]

    send_json(client_socket, {
        "type": "system",
        "message": f"Utilizadores online: {', '.join(sorted(usernames))}",
    })


def list_groups(client_socket: socket.socket) -> None:
    if not groups:
        send_json(client_socket, {
            "type": "system",
            "message": "Não existem grupos criados.",
        })
        return

    group_info = []
    for group_name, members in groups.items():
        group_info.append(f"{group_name} ({', '.join(sorted(members))})")

    send_json(client_socket, {
        "type": "system",
        "message": "Grupos:\n" + "\n".join(group_info),
    })


def handle_checked_message(client_socket: socket.socket, username: str, message: str, mode: str = "public", target: str | None = None) -> bool:
    findings = detect_personal_data(message)
    suspicious_matches = detect_suspicious_social_engineering(message)

    if suspicious_matches:
        suspicious_logger.warning(
            "[SUSPEITO] user=%s mode=%s target=%s message=%s patterns=%s",
            username,
            mode,
            target,
            message,
            suspicious_matches,
        )

    if findings:
        personal_logger.warning(
            "[DADOS_PESSOAIS] user=%s mode=%s target=%s message=%s findings=%s",
            username,
            mode,
            target,
            message,
            findings,
        )

        send_json(client_socket, {
            "type": "blocked",
            "message": "Mensagem bloqueada: foram detetados possíveis dados pessoais sensíveis.",
            "details": findings,
        })
        return True

    if mode == "public":
        broadcast({
            "type": "chat",
            "from": username,
            "message": message,
        }, exclude_socket=client_socket)
    elif mode == "private":
        send_private_message(client_socket, target, message)
    elif mode == "group":
        send_group_message(client_socket, target, message)

    logging.info("Mensagem aceite de %s: %s", username, message)
    return True


def process_message(client_socket: socket.socket, raw_message: str) -> bool:
    username = clients[client_socket]["username"]

    if raw_message.lower() == "exit":
        send_json(client_socket, {
            "type": "system",
            "message": "A desligar do servidor...",
        })
        remove_client(client_socket)
        return False

    if raw_message.startswith("/users"):
        list_users(client_socket)
        return True

    if raw_message.startswith("/groups"):
        list_groups(client_socket)
        return True

    if raw_message.startswith("/pm "):
        parts = raw_message.split(" ", 2)
        if len(parts) < 3:
            send_json(client_socket, {
                "type": "error",
                "message": "Uso correto: /pm <utilizador> <mensagem>",
            })
            return True

        target_username, text = parts[1], parts[2]
        return handle_checked_message(client_socket, username, text, mode="private", target=target_username)

    if raw_message.startswith("/creategroup "):
        parts = raw_message.split(" ", 2)
        if len(parts) < 3:
            send_json(client_socket, {
                "type": "error",
                "message": "Uso correto: /creategroup <nome_grupo> <user1,user2,...>",
            })
            return True

        group_name = parts[1]
        members = [user.strip() for user in parts[2].split(",") if user.strip()]
        create_group(client_socket, group_name, members)
        return True

    if raw_message.startswith("/groupmsg "):
        parts = raw_message.split(" ", 2)
        if len(parts) < 3:
            send_json(client_socket, {
                "type": "error",
                "message": "Uso correto: /groupmsg <grupo> <mensagem>",
            })
            return True

        group_name, text = parts[1], parts[2]
        return handle_checked_message(client_socket, username, text, mode="group", target=group_name)

    return handle_checked_message(client_socket, username, raw_message, mode="public")


def remove_client(client_socket: socket.socket) -> None:
    with clients_lock:
        if client_socket in clients:
            username = clients[client_socket]["username"]
            address = clients[client_socket]["address"]

            logging.info("Cliente desconectado: %s - %s", username, address)
            print(f"[DESCONECTADO] {username} - {address}")

            del clients[client_socket]

            broadcast({
                "type": "system",
                "message": f"{username} saiu do chat.",
            })

            try:
                client_socket.close()
            except Exception:
                pass


def handle_client(client_socket: socket.socket, address: tuple) -> None:
    try:
        send_json(client_socket, {
            "type": "system",
            "message": "Bem-vindo. Introduz o teu nome de utilizador:",
        })

        username_data = client_socket.recv(1024).decode("utf-8").strip()

        if not username_data:
            client_socket.close()
            return

        with clients_lock:
            existing_usernames = [info["username"] for info in clients.values()]
            if username_data in existing_usernames:
                send_json(client_socket, {
                    "type": "error",
                    "message": "Nome de utilizador já está em uso.",
                })
                client_socket.close()
                return

            clients[client_socket] = {
                "username": username_data,
                "address": address,
            }

        logging.info("Novo cliente conectado: %s - %s", username_data, address)
        print(f"[CONECTADO] {username_data} - {address}")

        send_json(client_socket, {
            "type": "system",
            "message": (
                f"Olá, {username_data}! Comandos disponíveis:\n"
                f"/users\n"
                f"/pm <utilizador> <mensagem>\n"
                f"/creategroup <nome_grupo> <user1,user2,...>\n"
                f"/groupmsg <grupo> <mensagem>\n"
                f"/groups\n"
                f"exit"
            ),
        })

        broadcast({
            "type": "system",
            "message": f"{username_data} entrou no chat.",
        }, exclude_socket=client_socket)

        buffer = ""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break

            buffer += data.decode("utf-8")

            while "\n" in buffer:
                raw_message, buffer = buffer.split("\n", 1)
                raw_message = raw_message.strip()

                if raw_message:
                    keep_running = process_message(client_socket, raw_message)
                    if not keep_running:
                        return

    except ConnectionResetError:
        logging.warning("Conexão terminada abruptamente: %s", address)
    except Exception as error:
        logging.error("Erro no cliente %s: %s", address, error)
    finally:
        remove_client(client_socket)


def start_server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    print(f"Servidor a escutar em {HOST}:{PORT}")
    logging.info("Servidor iniciado em %s:%s", HOST, PORT)

    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address), daemon=True)
        thread.start()


if __name__ == "__main__":
    start_server()
