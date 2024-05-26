import socket
import time
import programaRobot as pr

HOST = "169.254.20.35"  # IP del robot
PORT = 30002            # Puerto de escucha del robot

socketRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketRob.connect((HOST, PORT))
print("Se ha establecido la conexión con el robot.\n")

pose1 = [-0.00193, 0.37800, 0.12272, 2.926, -1.144, 0.0]
pose2 = [0.13415, 0.26674, 0.12272, 2.926, -1.144, 0.0]
pose3 = [-0.08589, 0.26674, 0.12272, 2.926, -1.144, 0.0]

poseHome = [-0.20743, 0.26641, 0.13850, 3.110, 0.0, -0.038]


pr.moverRobotJoint(socketRob, poseHome)

print("Moviendo el robot para dibujar un triangulo...\n")
time.sleep(2.0)

pr.moverRobotJoint(socketRob, pose1)
print("Robot en Vertice 1\n")

pr.moverRobotLineal(socketRob, pose2)
print("Robot en Vertice 2\n")

pr.moverRobotLineal(socketRob, pose3)
print("Robot en Vertice 3\n")

pr.moverRobotLineal(socketRob, pose1)
print("Volviendo a Home...\n")

pr.moverRobotJoint(socketRob, poseHome)

socketRob.close()
print("PROCESO FINALIZADO\n")