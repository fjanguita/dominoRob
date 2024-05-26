import socket
import threading
import time

from comandoRobot import comandoRobot
import programaRobot as pr


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
            elif(mensaje == '-1'):
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

def recibirRobot():
    global partida, condicion, continuar, instruccion
    direccion = 'localhost'
    puerto = 1441
    rcvRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvRob.bind((direccion,puerto))
    rcvRob.listen(1)
    print("Esperando conexion del robot...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvRob, direccionRcvRob = rcvRob.accept()
    print("Conexion establecida desde: ", direccionRcvRob,"\n")

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvRob.recv(128).decode()
        if (mensaje != ''):
            print("Se ha recibido el mensaje: ", mensaje,"\n")
            if(mensaje == '0'):
                partida = 0
            else:
                instruccion = int(mensaje)
            with condicion:
                condicion.notify()
        

    print("Cerrando los sockets")
    clienteRcvRob.close()
    rcvRob.close()

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

def conectarRobot():
    direccion = "192.168.20.35"  # IP del robot
    puerto = 30002  
    envRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envRob.connect((direccion, puerto))

    return envRob

if __name__ == "__main__":

    poseZonaRobo = [0.16566, 0.57123, 0.51001, 2.466, -2.271, -2.510]
    poseZonaFichas = [-0.35850, 0.45191, 0.51014, 2.392, -2.316, -2.464]
    poseZonaTablero = [-0.07651, 0.59647, 0.510, 2.445, -2.339, -2.417]

    poseTablero_Alt = [-0.06643, 0.52280, 0.53072, 2.116, 2.481, 2.432]
    poseFichas_Alt = [-0.21752, 0.35151, 0.53071, 2.116, 2.481, 2.432]
    poseRobo_Alt = [0.12311, 0.52280, 0.53072, 2.095, 2.541, 2.421]

    envInt = conectarInterfaz()

    thInt = threading.Thread(target=recibirInterfaz)
    thInt.daemon = True
    thInt.start()

    thAg = threading.Thread(target=recibirAgente)
    thAg.daemon = True
    thAg.start()

    # thRob = threading.Thread(target=recibirRobot)
    # thRob.start()

    while(continuar == 0):
        print("Esperando señal de la Interfaz...")
        time.sleep(2.0)

    envRob = conectarRobot()

    pr.initRobot(envRob)

    envAg = conectarAgente()

    while(partida):
        with condicion:
            condicion.wait()

            if(instruccion == 1):
                print("Cogiendo ficha y colocandola en el tablero...\n")
                pr.ejecutarComando(envRob, instruccion, posePick, posePlace)
                # condicion.wait()
                print("Ficha colocada, notificando a la interfaz...")
                time.sleep(2.0)
                envInt.send('-1'.encode())

            if(instruccion == 2):
                print("Moviendo al robot para robar ficha...\n")
                pr.ejecutarComando(envRob, instruccion, posePick, posePlace)
                # condicion.wait()
                print("Ficha robada. Notificando al agente...\n")
                time.sleep(1.0)
                envAg.send('-1'.encode())

            if(instruccion == 3):
                print("Moviendo al robot hasta 'Zona Robo'...")
                #pr.moverRobotJoint(envRob, poseZonaRobo)
                pr.moverRobotJoint(envRob, poseRobo_Alt)

                # condicion.wait()
                print("Robot en 'Zona Robo'.\n")
                time.sleep(1.0)
                envAg.send('-1'.encode())

            if(instruccion == 4):
                print("Moviendo al robot hasta 'Zona Fichas'...")
                #pr.moverRobotJoint(envRob, poseZonaFichas)
                pr.moverRobotJoint(envRob, poseFichas_Alt)

                # condicion.wait()
                print("Robot en 'Zona Robo'.\n")
                time.sleep(1.0)
                envAg.send('-1'.encode())

            if(instruccion == 5):
                print("Moviendo el robot a 'Zona Tablero'...\n")
                #pr.moverRobotJoint(envRob, poseZonaTablero)
                pr.moverRobotJoint(envRob, poseTablero_Alt)

                # condicion.wait()
                print("Robot en 'Zona Tablero'.\n")
                time.sleep(1.0)
                envAg.send('-1'.encode())
    
    envRob.send('0'.encode())

    thInt.join()
    thAg.join()
    # thRob.join()