import socket
import threading
from comandoRobot import comandoRobot
import time

partida = 1
continuar = 0

def recibirInterfaz():
    global partida, continuar
    direccion = 'localhost'
    puerto = 1414
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

def recibirAgente():
    global partida
    direccion = 'localhost'
    puerto = 1415
    rcvAg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvAg.bind((direccion,puerto))
    rcvAg.listen(1)
    print("Esperando conexion del agente...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvAg, direccionRcvAg = rcvAg.accept()
    print("Conexion establecida desde: ", direccionRcvAg,"\n")

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvAg.recv(1024)
        if(mensaje != b''):
            print("Mensaje serializado: ", mensaje, "\n")
            estructura = comandoRobot.deserialize(mensaje)
            print("Se ha recibido el mensaje:\n   ", estructura.tipoComando,"\n   ", estructura.posePick,"\n   ", estructura.posePlace,"\n")

    print("Cerrando los sockets")
    clienteRcvAg.close()
    rcvAg.close()

def recibirDummy():
    global partida
    direccion = 'localhost'
    puerto = 1441
    rcvDum = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvDum.bind((direccion,puerto))
    rcvDum.listen(1)
    print("Esperando conexion del robot...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvDum, direccionRcvDum = rcvDum.accept()
    print("Conexion establecida desde: ", direccionRcvDum,"\n")

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvDum.recv(128).decode()
        if(mensaje != ''):
            if(mensaje == '2'):
                print("CONEXION ESTABLECIDA CON EL ROBOT\n")
            else:
                print("EL ROBOT HA FINALIZADO SU MOVIMIENTO\n")
        

    print("Cerrando los sockets")
    clienteRcvDum.close()
    rcvDum.close()

def conectarInterfaz():
    direccion = 'localhost'
    puerto = 1404
    envInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envInt.connect((direccion, puerto))

def conectarDummy():
    direccion = 'localhost'
    puerto = 1440
    envDum = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envDum.connect((direccion, puerto))

    return envDum

if __name__ == "__main__":

    envInt = conectarInterfaz()

    thInt = threading.Thread(target=recibirInterfaz)
    thInt.start()

    thAg = threading.Thread(target=recibirAgente)
    thAg.start()

    thDum = threading.Thread(target=recibirDummy)
    thDum.start()

    while(continuar == 0):
        print("Esperando señal de la Interfaz...")
        time.sleep(2.0)

    envDum = conectarDummy()

    while(partida):
        print("Esperando comandos de movimiento...")
        time.sleep(5.0)
    
    envDum.send('0'.encode())

    thInt.join()
    thAg.join()
    thDum.join()
