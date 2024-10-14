import socket
import os

HOST = '127.0.0.1'
PORT = 8080
IMAGE_PATH = 'pikachuFeio.png'

def send_image(image_path):
    try:
        if not os.path.exists(image_path):
            print(f"Arquivo {image_path} não encontrado.")
            return

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        image_size = os.path.getsize(image_path)
        if image_size == 0:
            print(f"Erro: o arquivo {image_path} está vazio.")
            return

        image_info = f"{os.path.basename(image_path)}|{image_size}"
        client_socket.send(image_info.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        if response != "READY":
            print("Erro: Servidor não está pronto para receber a imagem.")
            return

        with open(image_path, 'rb') as f:
            bytes_sent = 0
            while bytes_sent < image_size:
                chunk = f.read(1024)
                if not chunk:
                    break
                client_socket.send(chunk)
                bytes_sent += len(chunk)

        print(f"Imagem {image_path} enviada com sucesso.")

        response = client_socket.recv(1024).decode('utf-8')
        print(f"Resposta do servidor: {response}")

    except Exception as e:
        print(f"Erro ao enviar imagem: {e}")
    finally:
        client_socket.close()

send_image(IMAGE_PATH)