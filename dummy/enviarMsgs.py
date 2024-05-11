import socket

direccion = 'localhost'
puerto = 10000
envS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
envS.connect((direccion, puerto))

key = input("Escribe mensaje")
envS.send(key.encode())

envS.close()