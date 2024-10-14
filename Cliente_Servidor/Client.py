import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))

    try:
        message = "Hello, Server!"
        client.send(message.encode('utf-8'))

        response = client.recv(1024).decode('utf-8')
        print(f"Resposta do servidor: {response}")

    finally:
        client.close()

if __name__ == "__main__":
    start_client()
