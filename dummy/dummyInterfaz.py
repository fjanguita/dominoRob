import socket
import threading
import time

partida = 1
conexiones = []
recibidos = 0

def recibirRobot():
    global partida, recibidos
    
    direccion = 'localhost'
    puerto = 1404
    rcvRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvRob.bind((direccion, puerto))
    rcvRob.listen(1)
    print("Esperando conexion del robot...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvRob, direccionRcvRob = rcvRob.accept()
    print("Conexion establecida desde: ", direccionRcvRob,"\n")
    recibidos = recibidos + 1

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvRob.recv(8).decode()
        if (mensaje != ''):
            print("Se ha recibido el mensaje: ", mensaje,"\n")
            partida = int(mensaje)

    print("Cerrando los sockets")
    clienteRcvRob.close()
    rcvRob.close()

def recibirAgente():
    global partida, recibidos
    
    direccion = 'localhost'
    puerto = 1405
    rcvAg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvAg.bind((direccion, puerto))
    rcvAg.listen(1)
    print("Esperando conexion del Agente...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvAg, direccionRcvAg = rcvAg.accept()
    print("Conexion establecida desde: ", direccionRcvAg,"\n")
    recibidos = recibidos + 1

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvAg.recv(8).decode()
        # print("Se ha recibido el mensaje: ", mensaje,"\n")
        # try:
        #     partida = int(mensaje)
        # except:
        #     pass
        if (mensaje != ''):
            print("Se ha recibido el mensaje: ", mensaje,"\n")
            partida = int(mensaje)

    print("Cerrando los sockets")
    clienteRcvAg.close()
    rcvAg.close()

def recibirVision():
    global partida, recibidos
    
    direccion = 'localhost'
    puerto = 1406
    rcvRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvRob.bind((direccion, puerto))
    rcvRob.listen(1)
    print("Esperando conexion de Vision...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvRob, direccionRcvRob = rcvRob.accept()
    print("Conexion establecida desde: ", direccionRcvRob,"\n")
    recibidos = recibidos + 1

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvRob.recv(8).decode()
        if (mensaje != ''):
            print("Se ha recibido el mensaje: ", mensaje,"\n")
            partida = int(mensaje)

    print("Cerrando los sockets")
    clienteRcvRob.close()
    rcvRob.close()

direccionRob = 'localhost'
puertoRob = 1414
envRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccionAg = 'localhost'
puertoAg = 1424
envAg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccionVis = 'localhost'
puertoVis = 1434
envVis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


msg = '1'
fin = '0'

thRob = threading.Thread(target=recibirRobot)
thRob.start()
thAg = threading.Thread(target=recibirAgente)
thAg.start()
thVis = threading.Thread(target=recibirVision)
thVis.start()

while(recibidos < 3):
    print("Esperando conexión de todos los módulos...\nModulos recibidos: ",recibidos,"\n")
    time.sleep(2.0)

print("\n\n---TODOS LOS MODULOS RECIBIDOS---\n\n")

while(len(conexiones) < 3):
    print("Estableciendo conexión con todos los modulosModulos conectados: ", len(conexiones), "\n")

    try:
        if('Rob' not in conexiones):
            envRob.connect((direccionRob, puertoRob))
            conexiones.append('Rob')
        if('Ag' not in conexiones):
            envAg.connect((direccionAg, puertoAg))
            conexiones.append('Ag')
        if('Vis' not in conexiones):
            envVis.connect((direccionVis, puertoVis))
            conexiones.append('Vis')
    except:
        print("No se ha podido establecer la conexión")

    time.sleep(2.0)
      

while(partida):
    key = input("Pulsa Enter para enviar un mensaje...\nIntroduce 'q' para terminar\n")
    if(key == 'q'):
        envRob.send(fin.encode())
        envAg.send(fin.encode())
        envVis.send(fin.encode())

        partida = False
    else:
        envAg.send(msg.encode())
        envRob.send(msg.encode())
        envVis.send(msg.encode())

thRob.join()
thAg.join()
thVis.join()
