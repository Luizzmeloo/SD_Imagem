from xmlrpc.server import SimpleXMLRPCServer

def enviar_notificacao(mensagem):
    print(f"Notificação recebida: {mensagem}")
    return True

server = SimpleXMLRPCServer(("127.0.0.1", 8081))
print("Serviço de Notificações iniciado")

server.register_function(enviar_notificacao, "enviar_notificacao")
server.serve_forever()