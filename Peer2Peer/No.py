import socket
import threading

class PeerNode:
    def __init__(self, node_id, host='127.0.0.1', port=8080):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.connections = []

    def handle_peer(self, peer_socket, address):
        print(f"Conexão recebida de {address}")
        self.connections.append(peer_socket)

        try:
            while True:
                message = peer_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Mensagem recebida de {address}: {message}")

                response = f"Hello from Node {self.node_id}!"
                peer_socket.send(response.encode('utf-8'))
        except ConnectionResetError:
            print(f"Conexão com {address} encerrada.")
        finally:
            self.connections.remove(peer_socket)
            peer_socket.close()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Nó {self.node_id} escutando na porta {self.port}...")

        while True:
            peer_socket, addr = server.accept()
            threading.Thread(target=self.handle_peer, args=(peer_socket, addr)).start()

    def connect_to_peer(self, peer_host, peer_port):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((peer_host, peer_port))
        self.connections.append(peer_socket)
        print(f"Conectado ao nó no endereço {peer_host}:{peer_port}")

        message = f"Hello from Node {self.node_id}!"
        peer_socket.send(message.encode('utf-8'))

        response = peer_socket.recv(1024).decode('utf-8')
        print(f"Resposta do nó: {response}")

    def start(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.daemon = True
        server_thread.start()

        while True:
            command = input("Digite o endereço de um nó para conectar (host:port) ou 'exit' para sair: ")
            if command == 'exit':
                break
            try:
                peer_host, peer_port = command.split(':')
                peer_port = int(peer_port)
                self.connect_to_peer(peer_host, peer_port)
            except Exception as e:
                print(f"Erro ao se conectar ao nó: {e}")


if __name__ == "__main__":
    node_id = input("Digite o identificador do nó: ")
    port = int(input("Digite a porta para o nó escutar (por exemplo, 8081, 8082, etc): "))
    node = PeerNode(node_id=node_id, port=port)
    node.start()
