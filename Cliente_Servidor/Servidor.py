import socket
import threading

connections = []

def handle_client(client_socket, address):
    print(f"Nova conexão de {address}")
    connections.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Recebido de {address}: {message}")

            response = f"Hello, Client! Conexões ativas: {len(connections)}"
            client_socket.send(response.encode('utf-8'))
    except ConnectionResetError:
        print(f"Conexão com {address} encerrada.")
    finally:
        connections.remove(client_socket)
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    print("Servidor ouvindo na porta 8080...")

    while True:
        client_socket, addr = server.accept()

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()