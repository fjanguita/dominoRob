import socket
from comandoRobot import comandoRobot
import threading

partida = 1
lock = threading.Lock()

def recibirInterfaz():
    global partida

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
    while partida:
        mensaje = clienteRcvInt.recv(8).decode()
        print("Se ha recibido el mensaje: ", mensaje,"\n")
        try:
            partida = int(mensaje)
        except:
            print("Mensaje recibido NO VALIDO\n")

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

conectarInterfaz()

thInt = threading.Thread(target=recibirInterfaz)
thInt.start()

conectarRobot()

msg = comandoRobot(1,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

while partida:
    with lock:
        if partida == 0:
            break
    # Espera la entrada del usuario antes de enviar un mensaje
    key = input("Pulsa Enter para enviar un mensaje...\n")
    # Envía el mensaje solo si la entrada es correcta
    if key == "":
        # Aquí deberías enviar el mensaje
        pass

# Espera a que el hilo de recepción termine
thInt.join()