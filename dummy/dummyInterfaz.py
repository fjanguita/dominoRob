import socket
import threading
import time

partida = 1
conexiones = []
recibidos = 0
continuar = 0
instruccion = 0
empiezaRobot = False

condicion = threading.Condition()

def recibirRobot():
    global partida, recibidos, condicion, continuar, instruccion
    
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
            if(mensaje == '0'):
                partida = 0
            elif (mensaje == '-1'):
                continuar = 1
            else:
                instruccion = int(mensaje)
            with condicion:
                condicion.notify()

    print("Cerrando los sockets")
    clienteRcvRob.close()
    rcvRob.close()

def recibirAgente():
    global partida, recibidos, continuar, condicion, instruccion
    
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
            if(mensaje == '0'):
                partida = 0
            elif (mensaje == '-1'):
                continuar = 1
            else:
                instruccion = int(mensaje)
            with condicion:
                condicion.notify()

    print("Cerrando los sockets")
    clienteRcvAg.close()
    rcvAg.close()

def recibirVision():
    global partida, recibidos, continuar, condicion, instruccion
    
    direccion = '0.0.0.0'
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
            if(mensaje == '0'):
                partida = 0
            elif (mensaje == '-1'):
                continuar = 1
            else:
                instruccion = int(mensaje)
            with condicion:
                condicion.notify()

    print("Cerrando los sockets")
    clienteRcvRob.close()
    rcvRob.close()

direccionRob = 'localhost'
puertoRob = 1414
envRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccionAg = 'localhost'
puertoAg = 1424
envAg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccionVis = '169.254.12.33'
puertoVis = 1434
envVis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


msg = '-1'
fin = '0'

thRob = threading.Thread(target=recibirRobot)
thRob.daemon = True
thRob.start()
thAg = threading.Thread(target=recibirAgente)
thAg.daemon = True
thAg.start()
thVis = threading.Thread(target=recibirVision)
thVis.daemon = True
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
      
key = input("Pulsa Enter para finalizar el setup...\n")

envAg.send(msg.encode())
envRob.send(msg.encode())
envVis.send(msg.encode())


### PREPARACION DE PARTIDA ###

input("Roba 7 fichas y pulsa Enter para iniciar la partida!\n")
time.sleep(1.0)

print("El robot va a robar sus 7 fichas...")

envVis.send('7'.encode())

print("Esperando a que finalice la fase de robo...")
with condicion:
    condicion.wait()

print("El doble mas alto del robot es: ", instruccion)

dobles = int(input("Introduce el numero de tu ficha doble más alta: "))

if( dobles > instruccion ):
    print("Tienes el doble mas alto, empiezas tu\n")
else:
    print("El robot tiene el doble mas alto. Empieza el robot\n")
    empiezaRobot = True

while(partida):
    with condicion:
        if(empiezaRobot):
            envVis.send('1'.encode())
            print("El robot va a ejecutar su turno...\n")
            condicion.wait()
            print("El robot ha finalizado su turno.\n")
            time.sleep(2.0)
    
    empiezaRobot = True
    key = input("Tu turno. Juega ficha o roba. \nPulsa Enter para pasar el turno al robot o 'q' para terminar\n")
    if(key == 'q'):
        partida = False
        envRob.send(fin.encode())
        envAg.send(fin.encode())
        envVis.send(fin.encode())



# while(partida):
#     key = input("Pulsa Enter para enviar un mensaje...\nIntroduce 'q' para terminar\n")
#     if(key == 'q'):
#         envRob.send(fin.encode())
#         envAg.send(fin.encode())
#         envVis.send(fin.encode())

#         partida = False
#     else:
#         envAg.send(msg.encode())
#         envRob.send(msg.encode())
#         envVis.send(msg.encode())

thRob.join()
thAg.join()
thVis.join()
