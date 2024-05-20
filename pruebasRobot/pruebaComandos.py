import socket
import time

HOST = "169.254.12.28"  # IP del robot
PORT = 30002            # Puerto de escucha del robot

socketRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketRob.connect((HOST, PORT))
print("Se ha establecido la conexión con el robot.\n")
#time.sleep(2.0)

# socketRob.send(("movej([4.079, -1.291, 0.562, -1.443, -1.471, 5.692], a=1.0, v=0.1, t=4.0)" + "\n").encode())
socketRob.send(("movej([1.57, -1.57, 0.0, -1.57, 0.0, 1.1345], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

# socketRob.send(("movej(p[0.032, 0.434, 0.303, 2.484, 2.368, 0.077], a=1.0, v=0.1, t=4.0)" + "\n").encode())
# time.sleep(5.0)

socketRob.close()