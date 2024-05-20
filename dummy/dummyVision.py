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
    global partida,continuar,instruccion, condicion

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
            elif(mensaje == '-1'):
                continuar = 1
            else:
                instruccion = int(mensaje)
            with condicion:
                condicion.notify()

def recibirAgente():
    global partida,continuar,instruccion, condicion

    direccion = 'localhost'
    puerto = 1436
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
thInt.daemon = True
thInt.start()
thAg = threading.Thread(target=recibirAgente)
thAg.daemon = True
thAg.start()

while(continuar == 0):
    print("Esperando señal de la Interfaz...")
    time.sleep(2.0)

envAg = conectarAgente()
msgAgente = '1'

while(partida):
    with condicion:
        condicion.wait()

        if(instruccion == 3):
            print("Solicitando al agente que mueva al robot hasta 'Zona Robo'...")
            envAg.send('3'.encode())

            condicion.wait()
            print("Robot en 'Zona Robo'. Enviando imagen...")

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA EL AGENTE

            time.sleep(2.0)
            envAg.send('7'.encode())

        if(instruccion == 4):
            print("Solicitando al agente que mueva al robot hasta 'Zona Fichas'...")
            envAg.send('4'.encode())

            condicion.wait()
            print("Robot en 'Zona Fichas'. Enviando imagen...")

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA EL AGENTE

            time.sleep(2.0)
            envAg.send('6'.encode())
            condicion.wait()
            dobles = instruccion
            print("Obtenido el doble mas alto, notificando a interfaz...\n")
            time.sleep(1.0)
            envInt.send(str(dobles).encode())

        if(instruccion == 1):
            print("Solicitando al agente que mueva al robot hasta 'Zona Tablero'...")
            envAg.send('5'.encode())

            condicion.wait()
            print("Robot en 'Zona Fichas'. Enviando imagen...")

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA EL AGENTE

            time.sleep(2.0)
            envAg.send('1'.encode())

thInt.join()
thAg.join()