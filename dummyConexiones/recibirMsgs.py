import socket

partida = '1'

direccion = 'localhost'
puerto = 10000

rcvInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rcvInt.bind((direccion, puerto))
rcvInt.listen(1)
print("Esperando conexion de Vision...\n")

# Bloquea hasta que recibe una conexion
clienteRcvInt, direccionRcvInt = rcvInt.accept()
print("Conexion establecida desde: ", direccionRcvInt,"\n")

# Bucle para manejar la llegada de mensajes
while(partida):
    mensaje = clienteRcvInt.recv(1024)
    datos = mensaje.decode()
    print("Se ha recibido el mensaje: ", datos,"\n")
    partida = int(mensaje)

print("Cerrando los sockets")
clienteRcvInt.close()
rcvInt.close()