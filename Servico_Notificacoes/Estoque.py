from xmlrpc.server import SimpleXMLRPCServer
import threading

fila_imagens = []
fila_lock = threading.Lock()

def adicionar_imagem(nome_imagem):
    print(f"Recebido pedido de adicionar a imagem: {nome_imagem}")
    with fila_lock:
        fila_imagens.append(nome_imagem)
        print(f"Imagem '{nome_imagem}' adicionada ao estoque. Fila atual: {fila_imagens}")
    return f"Imagem '{nome_imagem}' adicionada com sucesso."

def verificar_estoque():
    with fila_lock:
        if fila_imagens:
            print(f"Imagens na fila: {fila_imagens}")
            return fila_imagens
        else:
            print("Nenhuma imagem na fila para ser processada.")
            return []

try:
    server = SimpleXMLRPCServer(("127.0.0.1", 8090))
    print("Serviço de Estoque Iniciado")

    server.register_function(adicionar_imagem, "adicionar_imagem")
    server.register_function(verificar_estoque, "verificar_estoque")

    print("Servidor esperando por conexões...")
    server.serve_forever()

except Exception as e:
    print(f"Erro durante a execução do servidor: {e}")
