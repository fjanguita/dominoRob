import socket
import threading
from comandoRobot import comandoRobot
import time

partida = 1
continuar = 0

instruccion = 0
posePick = []
posePlace = []

# Creamos un objeto Condition
condicion = threading.Condition()

def recibirInterfaz():
    global partida, continuar, condicion, instruccion
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
            elif (mensaje == '1'):
                continuar = 1
            else:
                instruccion = int(mensaje)
            with condicion:
                condicion.notify()

    print("Cerrando los sockets")
    clienteRcvInt.close()
    rcvInt.close()

def recibirAgente():
    global partida, continuar, instruccion, condicion, posePick, posePlace
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

        if (mensaje != b''):
            estructura = comandoRobot.deserialize(mensaje)
            print("Se ha recibido el mensaje:\n   ", estructura.tipoComando,"\n   ", estructura.posePick,"\n   ", estructura.posePlace,"\n")
            instruccion = estructura.tipoComando
            posePick = estructura.posePick
            posePlace = estructura.posePlace
            with condicion:
                condicion.notify()

    print("Cerrando los sockets")
    clienteRcvAg.close()
    rcvAg.close()

def recibirDummy():
    global partida, condicion, continuar, instruccion
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
        if (mensaje != ''):
            print("Se ha recibido el mensaje: ", mensaje,"\n")
            if(mensaje == '0'):
                partida = 0
            elif (mensaje == '1'):
                continuar = 1
            else:
                instruccion = int(mensaje)
            with condicion:
                condicion.notify()
        

    print("Cerrando los sockets")
    clienteRcvDum.close()
    rcvDum.close()

def conectarInterfaz():
    direccion = 'localhost'
    puerto = 1404
    envInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envInt.connect((direccion, puerto))

    return envInt

def conectarAgente():
    direccion = 'localhost'
    puerto = 1428
    envAg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envAg.connect((direccion, puerto))

    return envAg

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
    envAg = conectarAgente()

    while(partida):
        with condicion:
            condicion.wait()

            if(instruccion == 1):
                print("Cogiendo ficha y colocandola en el tablero...\n")
                envDum.send('1'.encode())
                condicion.wait()
                print("Ficha colocada, notificando a la interfaz...")
                time.sleep(2.0)
                envInt.send('1'.encode())

            if(instruccion == 2):
                print("Moviendo al robot para robar ficha...\n")
                envDum.send('7'.encode())
                condicion.wait()
                print("Ficha robada. Notificando al agente...\n")
                time.sleep(1.0)
                envAg.send('1'.encode())

            if(instruccion == 3):
                print("Moviendo al robot hasta 'Zona Robo'...")
                envDum.send('3'.encode())

                condicion.wait()
                print("Robot en 'Zona Robo'.\n")
                time.sleep(1.0)
                envAg.send('1'.encode())

            if(instruccion == 4):
                print("Moviendo al robot hasta 'Zona Fichas'...")
                envDum.send('4'.encode())

                condicion.wait()
                print("Robot en 'Zona Robo'.\n")
                time.sleep(1.0)
                envAg.send('1'.encode())

            if(instruccion == 5):
                print("Moviendo el robot a 'Zona Tablero'...\n")
                envDum.send('5'.encode())
                condicion.wait()
                print("Robot en 'Zona Tablero'.\n")
                time.sleep(1.0)
                envAg.send('1'.encode())
    
    envDum.send('0'.encode())

    thInt.join()
    thAg.join()
    thDum.join()
