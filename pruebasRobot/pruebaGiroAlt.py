import socket
import time
import programaRobot as pr

HOST = "192.168.20.35"  # IP del robot
PORT = 30002            # Puerto de escucha del robot

socketRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketRob.connect((HOST, PORT))
print("Se ha establecido la conexión con el robot.\n")
#time.sleep(2.0)

pr.initRobot(socketRob)

altura_aproach = 0.050
altura_ficha = 0.01843
altura_girar = 0.03379
pickPruebaRobo = [0.04896, 0.43777, altura_ficha, 2.461, -2.010, -0.167]
aproachPruebaRobo = [0.04896, 0.43777, altura_aproach, 2.461, -2.010, -0.167]
poseIntermedia = [-0.08148, 0.35908, 0.16827, 2.468, -2.047, -0.2]
approachGiro = [-0.38445, 0.44004, altura_aproach, 1.754, -1.547, -1.089]
inicioGiro = [-0.38445, 0.44004, altura_girar, 1.754, -1.547, -1.089]
soltarGiro = [-0.30200, 0.44004, altura_girar, 1.754, -1.547, -1.089]
soltarElevado = [-0.30200, 0.44004, altura_aproach, 1.754, -1.547, -1.089]
aproachRecoger = [-0.31943, 0.43783, altura_aproach, 2.453, -2.053, -0.139]
poseRecoger = [-0.31943, 0.43783, altura_ficha, 2.453, -2.053, -0.139]

def girarFichaAlt(socketRob):

    pr.moverRobotJoint(socketRob, aproachPruebaRobo)

    pr.moverRobotLineal(socketRob, pickPruebaRobo)

    pr.cerrarPinza(socketRob)

    pr.moverRobotLineal(socketRob, aproachPruebaRobo)

    pr.moverRobotJoint(socketRob, poseIntermedia)

    pr.moverRobotJoint(socketRob, approachGiro)

    pr.moverRobotLineal(socketRob, inicioGiro)

    pr.moverRobotLineal(socketRob, soltarGiro)

    pr.abrirPinza(socketRob)

    pr.moverRobotLineal(socketRob, soltarElevado)

    pr.moverRobotJoint(socketRob, aproachRecoger)

    pr.moverRobotLineal(socketRob, poseRecoger)

    pr.cerrarPinza(socketRob)

    pr.moverRobotLineal(socketRob, aproachRecoger)

    pr.moverRobotJoint(socketRob, poseIntermedia)

girarFichaAlt(socketRob)

print("Cerrando conexion con el robot...")
socketRob.close()