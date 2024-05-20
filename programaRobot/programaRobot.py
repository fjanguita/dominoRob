import time

def initRobot(socketRob):

    print("Configurando el robot...\n")

    comando = "set_analog_outputdomain(1, 0)\n"
    socketRob.send(comando.encode())
    time.sleep(0.1)

    comando = "set_standard_analog_input_domain(0, 1)\n"
    socketRob.send(comando.encode())
    time.sleep(0.1)

    comando = "set_tool_analog_input_domain(1, 0)\n"
    socketRob.send(comando.encode())
    time.sleep(0.1)

    comando = "set_tool_digital_input_action(0, \"freedrive\")\n"
    socketRob.send(comando.encode())
    time.sleep(0.1)

    comando = "set_tool_digital_out(1, False)\n"
    socketRob.send(comando.encode())
    time.sleep(0.1)

    comando = "set_tool_digital_out(0,True)\n"
    socketRob.send(comando.encode())
    time.sleep(0.1)

    moverEspera(socketRob)

    abrirPinza(socketRob)

    print("Configuración del robot lista.\n")

def cerrarPinza(socketRob):
    comando = "set_tool_digital_out(0, False)\n"
    socketRob.send(comando.encode())
    time.sleep(0.1)

    comando = "set_tool_digital_out(1,True)\n"
    socketRob.send(comando.encode())
    time.sleep(0.1)

def abrirPinza(socketRob):
    comando = "set_tool_digital_out(1, False)\n"
    socketRob.send(comando.encode())
    time.sleep(0.1)

    comando = "set_tool_digital_out(0,True)\n"
    socketRob.send(comando.encode())
    time.sleep(0.1)

def moverRobotJoint(socketRob, pose):
    comando = "movej(p" + str(pose) + ", a=1.0, v=0.1, t=4.0)\n"
    socketRob.send(comando.encode())
    time.sleep(5.0)

def moverRobotLineal(socketRob, pose):
    comando = "movel(p" + str(pose) + ", a=1.0, v=0.1, t=4.0)\n"
    socketRob.send(comando.encode())
    time.sleep(5.0)

def moverHome(socketRob):
    poseHome = []
    moverRobotJoint(socketRob, poseHome)

def moverEspera(socketRob):
    comando = "movej([1.5708, -2.0199, -0.9119, -1.7787, 1.5696, 1.1582], a=1.0, v=0.1, t=4.0)\n"
    socketRob.send(comando.encode())
    time.sleep(5.0)

def moverAproximacion(socketRob, pose):
    pose[2] = 0.025
    pose[5] = 0.0
    moverRobotJoint(socketRob, pose)

def moverAcercar(socketRob, pose):
    pose[2] = -0.05488
    pose[5] = 0.0
    moverRobotLineal(socketRob, pose)

def moverAlejar(socketRob, pose):
    pose[2] = 0.025
    pose[5] = 0.0
    moverRobotLineal(socketRob, pose)

def fichaPick(socketRob, posePick):
    moverAproximacion(socketRob, posePick)

    moverAcercar(socketRob, posePick)

    cerrarPinza(socketRob)

    moverAlejar(socketRob, posePick)

def fichaPlace(socketRob, posePlace):
    moverAproximacion(socketRob, posePlace)

    moverAcercar(socketRob, posePlace)

    abrirPinza(socketRob)

    moverAlejar(socketRob, posePlace)

def fichaGirar(socketRob):
    # IR A POSICION DE GIRO (ALZADA)
    poseInitGiro = [-0.43541, 0.27567, 0.02766, 1.674, -1.664, -0.867]
    moverRobotJoint(socketRob, poseInitGiro)

    # IR A POSICION DE GIRO
    poseStartGiro = [-0.43541, 0.27567, -0.0100, 1.674, -1.664, -0.867]
    moverRobotLineal(socketRob, poseStartGiro)

    # IR A POSICION DE SOLTADO (EN GIRO)
    poseFinGiro = [-0.36861, 0.27567, -0.0100, 1.674, -1.664, -0.867]
    moverRobotLineal(socketRob, poseFinGiro)

    # SOLTAR PIEZA GIRADA
    abrirPinza(socketRob)

    # RECOLOCARSE PARA COGERLA
    poseRecogerElevada = [-0.36861, 0.27567, 0.040, 1.674, -1.664, -0.867]
    moverRobotLineal(socketRob, poseRecogerElevada)

    poseRecogerOrientada = [-0.33865, 0.27411, 0.00285, 2.250, -2.190, 0.0]
    moverRobotJoint(socketRob, poseRecogerOrientada)

    poseRecoger = [-0.33865, 0.27411, -0.05456, 2.250, -2.190, 0.0]
    moverRobotLineal(socketRob, poseRecoger)

    # RECOGER LA PIEZA GIRADA
    cerrarPinza(socketRob)

    moverAlejar(socketRob, poseRecoger)

def ejecutarComando(socketRob, instruccion, posePick, posePlace):
    fichaPick(socketRob, posePick)

    if( instruccion == 2 ):
        fichaGirar(socketRob)

    fichaPlace(socketRob, posePlace)

    moverEspera(socketRob)