# PROGRAMA QUE SIMULA AL ROBOT

import socket
import time

partida = 1
confirmacion = 1
conexion = 2

direccion = 'localhost'
puertoRcv = 1440
puertoEnv = 1441

socketRcv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketEnv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socketRcv.bind((direccion, puertoRcv))
socketRcv.listen(1)

clienteRcv, direccionRcv = socketRcv.accept()
print("Esperando conexion...")

time.sleep(5.0)

socketEnv.connect((direccion, puertoEnv))

print("Conexion establecida con el robot")

while(partida):
    mensaje = clienteRcv.recv(8).decode()
    if(mensaje != ''):
        if(mensaje == 0):
            partida = 0
        else:
            time.sleep(5.0)
            print("EL ROBOT HA FINALIZADO EL MOVIMIENTO")
            socketEnv.send(str(conexion).encode())

socketEnv.close()
socketRcv.close()
