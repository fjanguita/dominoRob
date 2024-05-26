import socket
import time
import programaRobot as pr

HOST = "169.254.12.28"  # IP del robot
PORT = 30002            # Puerto de escucha del robot

socketRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketRob.connect((HOST, PORT))
print("Se ha establecido la conexión con el robot.\n")
#time.sleep(2.0)

pr.initRobot(socketRob)
time.sleep(2.0)
print("Configuracion del robot finalizada\n")

print("Cerrando Pinza...\n")
pr.cerrarPinza(socketRob)
time.sleep(2.0)

print("Abriendo Pinza...\n")
pr.abrirPinza(socketRob)
time.sleep(2.0)

print("Cerrando conexión con el robot...\n")
socketRob.accept
print("PROCESO FINALIZADO")

