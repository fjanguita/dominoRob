import socket
import time
import threading
import comandoRobot
from comandoVision import deserialize
import programaRobot as pr

condicion = threading.Condition()
partida = 1

def recibirVision():
    global instruccion, fichas_vis, num_piezas, condicion
    direccion = '0.0.0.0'
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
        mensaje = clienteRcvInt.recv(1024)
        if (mensaje != ''):
            comando, Npiezas, array = deserialize(mensaje)
            print("Se ha recibido el mensaje:\n   ", array,"\n   ", comando,"\n   ", Npiezas,"\n")

            fichas_vis = array
            instruccion = comando
            num_piezas = Npiezas

            with condicion:
                condicion.notify()
                
    print("Cerrando los sockets")
    clienteRcvInt.close()
    rcvInt.close()

HOST = "localhost"  # IP del robot
PORT = 1440            # Puerto de escucha del robot

thVis = threading.Thread(target=recibirVision)
thVis.daemon = True
thVis.start()

altura_camara = 0.510
array_vacio = []
poseZonaRobo = [0.16566, 0.57123, altura_camara, 2.466, -2.271, -2.510]
poseZonaFichas = [-0.35850, 0.45191, altura_camara, 2.392, -2.316, -2.464]
poseZonaTablero = [-0.07651, 0.59647, altura_camara, 2.445, -2.339, -2.417]

socketRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketRob.connect((HOST, PORT))
print("Se ha establecido la conexión con el robot.\n")

while(partida):
    condicion.wait()
    if( instruccion == 5 ):
        print("Moviendo robot a zona de Tablero...\n")
        msg = comandoRobot(instruccion, poseZonaTablero, array_vacio)
        socketRob.sendall(msg.serialize())

    if( instruccion == 1):
        print("Colocando ficha en el tablero...\n")
        posePlace = [0.1, 0.420, 0.20, 3.14, 0.0, 0.0]
        posePick = [fichas_vis[0][2], fichas_vis[0][3], 0.0, 3.14, 0.0, 0.0]
        msg = comandoRobot(instruccion, posePick, posePlace)
        socketRob.sendall(msg.serialize())

        partida = 0
         
thVis.join()

socketRob.close()