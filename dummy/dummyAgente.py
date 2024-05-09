import socket
from comandoRobot import comandoRobot
import threading
import time

partida = 1
continuar = 0

def recibirInterfaz():
    global partida, continuar

    direccion = 'localhost'
    puerto = 1424
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

def recibirVision():
    global partida

    direccion = 'localhost'
    puerto = 1435
    rcvInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvInt.bind((direccion, puerto))
    rcvInt.listen(1)
    print("Esperando conexion de Vision...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvInt, direccionRcvInt = rcvInt.accept()
    print("Conexion establecida desde: ", direccionRcvInt,"\n")

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvInt.recv(8).decode()
        if(mensaje != ''):
            print("Se ha recibido un mensaje de Vision: ", mensaje,"\n")

    print("Cerrando los sockets")
    clienteRcvInt.close()
    rcvInt.close()

def conectarInterfaz():
    direccion = 'localhost'
    puerto = 1405
    envInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envInt.connect((direccion, puerto))

def conectarRobot():
    direccion = 'localhost'
    puerto = 1415
    envRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envRob.connect((direccion, puerto))

    return envRob


envInt = conectarInterfaz()

thInt = threading.Thread(target=recibirInterfaz)
thInt.start()
thVis = threading.Thread(target=recibirVision)
thVis.start()

while(continuar == 0):
    print("Esperando señal de la Interfaz...")
    time.sleep(2.0)

envRob = conectarRobot()

msg = comandoRobot(1,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

while(partida):
    key = input("Pulsa Enter para enviar un mensaje...\n")

    envRob.sendall(msg.serialize())

thInt.join()
thVis.join()