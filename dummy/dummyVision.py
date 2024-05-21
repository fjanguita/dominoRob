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
            time.sleep(2.0)

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA EL AGENTE
            # SI NO HAY FICHAS DE ROBO, ENVIAR AL AGENTE UN '8'

            if( False ):
                envAg.send('8'.encode())
                condicion.wait()
                envInt.send('-1'.encode())
            else:
                envAg.send('3'.encode())

        if(instruccion == 4):
            print("Solicitando al agente que mueva al robot hasta 'Zona Fichas'...")
            envAg.send('4'.encode())

            condicion.wait()
            print("Robot en 'Zona Fichas'. Enviando imagen...")

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA EL AGENTE

            time.sleep(2.0)
            envAg.send('4'.encode())

            # ESPERA A QUE EL AGENTE ACTUALICE SUS FICHAS
            condicion.wait()
            # ENVIA CONFIRMACION A INTERFAZ PARA FINALIZAR TURNO
            envInt.send('-1'.encode())


        if(instruccion == 1):
            print("Solicitando al agente que mueva al robot hasta 'Zona Tablero'...")
            envAg.send('5'.encode())

            condicion.wait()
            print("Robot en 'Zona Fichas'. Enviando imagen...")

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA EL AGENTE

            time.sleep(2.0)
            envAg.send('1'.encode())

        # Instruccion 7 comienza la secuencia inicial de robo
        if(instruccion == 7):
            print("Solicitando al agente que mueva al robot a 'Zona Robo'...\n")
            envAg.send('3'.encode())

            # Espera confirmacion de que el robot está en zona de robo
            condicion.wait()
            print("Robot en 'Zona Robo'. Enviando imagen al agente...\n")

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA ENVIAR FICHAS DE ROBO AL AGENTE

            time.sleep(2.0)
            # CAMBIAR EL '7' POR VUESTRO MENSAJE FORMATEADO CON UN 7 EN EL CAMPO DE INSTRUCCION
            envAg.send('7'.encode())

            # ESPERA A QUE EL ROBOT TENGA TODAS SUS FICHAS PARA HACERLE UNA FOTO
            condicion.wait()
            print("Fichas del robot listas. Enviando imagen al agente...\n")

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA ENVIAR FICHAS DISPONIBLES AL AGENTE
            # CAMBIAR EL '6' POR VUESTRO MENSAJE FORMATEADO CON UN 6 EN EL CAMPO DE INSTRUCCION
            envAg.send('6'.encode())

            # ESPERA A QUE EL AGENTE LE DIGA EL DOBLE MAS ALTO
            condicion.wait()
            doble = str(instruccion)

            # Devuelve el doble mas alto a la interfaz
            envInt.send(doble.encode())



thInt.join()
thAg.join()