import socket
from comandoRobot import comandoRobot
import threading
import time

partida = 1
continuar = 0

def recibirInterfaz():
    global partida,continuar

    direccion = 'localhost'
    puerto = 1434
    rcvInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvInt.bind((direccion, puerto))
    rcvInt.listen(1)
    print("Esperando conexion de la interfaz...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvInt, direccionRcvInt = rcvInt.accept()
    print("Conexion establecida desde: ", direccionRcvInt,"\n")

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvInt.recv(8).decode()
        # print("Se ha recibido el mensaje: ", mensaje,"\n")
        # try:
        #     partida = int(mensaje)
        # except:
        #     print("Mensaje recibido NO VALIDO\n")
        if (mensaje != ''):
            print("Se ha recibido el mensaje: ", mensaje,"\n")
            if(mensaje == '0'):
                partida = 0
            else:
                continuar = int(mensaje)

    print("Cerrando los sockets")
    clienteRcvInt.close()
    rcvInt.close()

def conectarInterfaz():
    direccion = 'localhost'
    puerto = 1406
    envInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envInt.connect((direccion, puerto))

    return envInt

def conectarAgente():
    direccion = 'localhost'
    puerto = 1435
    envAg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envAg.connect((direccion, puerto))

    return envAg


envInt = conectarInterfaz()

thInt = threading.Thread(target=recibirInterfaz)
thInt.start()

while(continuar == 0):
    print("Esperando señal de la Interfaz...")
    time.sleep(2.0)

envAg = conectarAgente()
msgAgente = '1'

while(partida):
    key = input("Pulsa Enter para enviar un mensaje...\n")

    envAg.send(msgAgente.encode())

thInt.join()