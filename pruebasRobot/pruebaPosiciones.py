import socket
import time

HOST = "169.254.12.28"  # IP del robot
PORT = 30002            # Puerto de escucha del robot

poseZonaRobo = [0.16566, 0.57123, 0.51001, 2.466, -2.271, -2.510]
poseZonaFichas = [-0.35850, 0.45191, 0.51014, 2.392, -2.316, -2.464]
poseZonaTablero = [-0.07651, 0.59647, 0.520, 2.445, -2.339, -2.417]

posicionYoloLolo = [0.08737, 0.43265, -0.05488, -0.7854, 2.23561, 0.0]

socketRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketRob.connect((HOST, PORT))
print("Se ha establecido la conexión con el robot.\n")
#time.sleep(2.0)

# socketRob.send(("movej([4.079, -1.291, 0.562, -1.443, -1.471, 5.692], a=1.0, v=0.1, t=4.0)" + "\n").encode())
socketRob.send(("movej(p" + str(posicionYoloLolo) + ", a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

# socketRob.send(("movej(p[0.032, 0.434, 0.303, 2.484, 2.368, 0.077], a=1.0, v=0.1, t=4.0)" + "\n").encode())
# time.sleep(5.0)

socketRob.close()