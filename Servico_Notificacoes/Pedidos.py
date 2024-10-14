import socket
import threading
import os
from PIL import Image, ImageFilter
import xmlrpc.client

HOST = '127.0.0.1'
PORT = 8080
NOTIFICACOES_RPC = 'http://127.0.0.1:8081'
ESTOQUE_RPC = 'http://127.0.0.1:8090'

notificacoes = xmlrpc.client.ServerProxy(NOTIFICACOES_RPC)

estoque = xmlrpc.client.ServerProxy(ESTOQUE_RPC)

def process_image(image_path):
    try:
        image = Image.open(image_path)
        filtered_image_path = "filtered_" + os.path.basename(image_path)
        image = image.filter(ImageFilter.BLUR)
        image.save(filtered_image_path)
        return filtered_image_path
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return None

def handle_client(client_socket, addr):
    print(f"Conexão recebida de {addr}")

    try:
        data = client_socket.recv(1024).decode('utf-8')
        image_name, image_size = data.split('|')
        image_size = int(image_size)
        print(f"Recebendo imagem {image_name} ({image_size} bytes)")

        client_socket.send("READY".encode('utf-8'))

        with open(image_name, 'wb') as f:
            bytes_received = 0
            while bytes_received < image_size:
                chunk = client_socket.recv(1024)
                if not chunk:
                    print("Conexão perdida antes de receber toda a imagem.")
                    break
                f.write(chunk)
                bytes_received += len(chunk)

        print(f"Imagem {image_name} recebida com sucesso.")

        try:
            print(f"Tentando notificar o serviço de estoque com a imagem: {image_name}")
            resposta = estoque.adicionar_imagem(image_name)
            print(f"Resposta do serviço de estoque: {resposta}")
        except Exception as e:
            print(f"Erro ao notificar o serviço de estoque: {e}")

        filtered_image = process_image(image_name)

        if filtered_image:
            notificacoes.enviar_notificacao(f"Imagem {image_name} foi processada com sucesso!")
            client_socket.send(f"Imagem processada e salva como {filtered_image}".encode('utf-8'))
        else:
            client_socket.send("Erro no processamento da imagem.".encode('utf-8'))

    except Exception as e:
        print(f"Erro ao lidar com o cliente {addr}: {e}")
    finally:
        client_socket.close()
        print(f"Conexão com {addr} fechada.")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print("Serviço de Pedidos Iniciado. Aguardando conexões...")

while True:
    client_socket, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()