import socket
from comandoRobot import comandoRobot
import threading
import time

partida = 1
continuar = 0

instruccion = 0

# Creamos un objeto Condition
condicion = threading.Condition()

def recibirInterfaz():
    global partida, continuar, instruccion, condicion

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
            elif( mensaje == '-1' ):
                continuar = 1
            else:
                instruccion = int(mensaje)
            with condicion:
                condicion.notify()

    print("Cerrando los sockets")
    clienteRcvInt.close()
    rcvInt.close()

def recibirVision():
    global partida, continuar, instruccion, condicion

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

def recibirRobot():
    global partida, continuar, instruccion, condicion

    direccion = 'localhost'
    puerto = 1428
    rcvInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvInt.bind((direccion, puerto))
    rcvInt.listen(1)
    print("Esperando conexion de Robot...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvInt, direccionRcvInt = rcvInt.accept()
    print("Conexion establecida desde: ", direccionRcvInt,"\n")

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvInt.recv(8).decode()
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

def conectarInterfaz():
    direccion = 'localhost'
    puerto = 1405
    envInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envInt.connect((direccion, puerto))

    return envInt

def conectarRobot():
    direccion = 'localhost'
    puerto = 1415
    envRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envRob.connect((direccion, puerto))

    return envRob

def conectarVision():
    direccion = 'localhost'
    puerto = 1436
    envVis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envVis.connect((direccion, puerto))

    return envVis


envInt = conectarInterfaz()

thInt = threading.Thread(target=recibirInterfaz)
thInt.start()
thVis = threading.Thread(target=recibirVision)
thVis.start()
thRob = threading.Thread(target=recibirRobot)
thRob.start()

while(continuar == 0):
    print("Esperando señal de la Interfaz...")
    time.sleep(2.0)

envRob = conectarRobot()
envVis = conectarVision()

array_vacio = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
array_ficha = [-0.15488, 0.30106, 0.1648, 2.241, -2.201, 0.0]

poseRobo1 = [-0.28867, 0.38369, -0.04966, 2.163, -2.278, 0.0]
poseRobo2 = [-0.28867, 0.35869, -0.04966, 2.163, -2.278, 0.0]
poseRobo3 = [-0.28867, 0.32369, -0.04966, 2.163, -2.278, 0.0]
poseRobo4 = [-0.28867, 0.28869, -0.04966, 2.163, -2.278, 0.0]
poseRobo5 = [-0.28867, 0.25369, -0.04966, 2.163, -2.278, 0.0]
poseRobo6 = [-0.28867, 0.21869, -0.04966, 2.163, -2.278, 0.0]
poseRobo7 = [-0.28867, 0.18369, -0.04966, 2.163, -2.278, 0.0]

posesRobo = [poseRobo1, poseRobo2, poseRobo3, poseRobo4, poseRobo5, poseRobo6, poseRobo7]

msg = comandoRobot(1,array_vacio,array_vacio)
msg_zona1 = comandoRobot(3,array_vacio,array_vacio)
msg_zona2 = comandoRobot(4,array_vacio,array_vacio)
msg_zona3 = comandoRobot(5,array_vacio,array_vacio)
msg_robar = comandoRobot(2,array_vacio,array_vacio)



# METER MOVIDAS


while(partida):
    with condicion:
        print("\nEsperando instrucciones...\n")
        condicion.wait()

        if(instruccion == 3):
            print("Solicitando al robot que vaya a 'Zona Robo'...\n")
            envRob.send(msg_zona1.serialize())
            condicion.wait()
            print("\nEl robot esta en Zona Robo. Notificando a Vision...\n")
            time.sleep(1.0)
            envVis.send('-1'.encode())

        if(instruccion == 7):
            print("Solicitando al robot que robe 7 fichas...\n")
            for i in range(0,7):
                msg_robar = comandoRobot(2, array_ficha, posesRobo[i])
                envRob.sendall(msg_robar.serialize())
                condicion.wait()
                print("Fichas robadas: ", i+1, "\n")
                time.sleep(1.0)
            
            print("Fichas robadas. Notificando a la interfaz...")
            time.sleep(1.0)
            envInt.send('-1'.encode())
        
        if(instruccion == 4):
            print("Solicitando al robot que vaya a 'Zona Fichas'...\n")
            envRob.send(msg_zona2.serialize())
            condicion.wait()
            print("\nEl robot esta en Zona Fichas. Notificando a Vision...\n")
            time.sleep(1.0)
            envVis.send('4'.encode())

        if(instruccion == 6):
            print("Se va a devolver el doble más alto...\n")
            doble = 6
            time.sleep(1.0)
            envVis.send(str(doble).encode())

        if(instruccion == 5):
            print("Solicitando al robot que vaya a 'Zona Tablero'...\n")
            envRob.send(msg_zona3.serialize())
            condicion.wait()
            print("\nEl robot esta en Zona Tablero. Notificando a Vision...\n")
            time.sleep(1.0)
            envVis.send('5'.encode())

        if(instruccion == 1):
            print("Eligiendo ficha para colocar...\n")
            time.sleep(2.0)

            # LOGICA DEL AGENTE PARA ELEGIR FICHA O ROBAR
            ficha = True
            if( ficha ):
                msg_ficha = comandoRobot(1,array_vacio,array_vacio)
                envRob.sendall(msg_ficha.serialize())
            else: 
                print("No se puede colocar ninguna ficha. El robot va a robar...\n")
                envRob.sendall(msg_robar.serialize())
                

thInt.join()
thVis.join()
thRob.join()