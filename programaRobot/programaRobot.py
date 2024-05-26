import time

def transformar_angulo(pose):
    orientacion = pose[5]

    if(orientacion > 2.3562):
        orientacion = orientacion - 3.12

    if(pose[5] > -0.7838 and pose[5] < 0.5236):
        pose[3] = 0.243
        pose[4] = 3.14
        pose[5] = 0.0
    elif(pose[5] >= 0.5236 and pose[5] < 1.0472):
        pose[3] = 0.243
        pose[4] = 3.14
        pose[5] = 0.0
    elif(pose[5] >= 1.0472 and pose[5] < 1.5707):
        pose[3] = 0.243
        pose[4] = 3.14
        pose[5] = 0.0
    elif(pose[5] >= 1.5707 and pose[5] < 2.3562):
        pose[3] = 0.243
        pose[4] = 3.14
        pose[5] = 0.0

    return pose

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

    #moverEspera(socketRob)

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
    # pose[2] = 0.025
    # pose[5] = 0.0
    pose[2] = 0.050
    moverRobotJoint(socketRob, pose)

def moverAcercar(socketRob, pose):
    # pose[2] = -0.05488
    # pose[5] = 0.0
    pose[2] = 0.018
    moverRobotLineal(socketRob, pose)

def moverAlejar(socketRob, pose):
    # pose[2] = 0.025
    # pose[5] = 0.0
    pose[2] = 0.050
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

def girarFichaAlt(socketRob):

    altura_aproach = 0.050
    altura_ficha = 0.0180
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

    moverRobotJoint(socketRob, poseIntermedia)

    moverRobotJoint(socketRob, approachGiro)

    moverRobotLineal(socketRob, inicioGiro)

    moverRobotLineal(socketRob, soltarGiro)

    abrirPinza(socketRob)

    moverRobotLineal(socketRob, soltarElevado)

    moverRobotJoint(socketRob, aproachRecoger)

    moverRobotLineal(socketRob, poseRecoger)

    cerrarPinza(socketRob)

    moverRobotLineal(socketRob, aproachRecoger)

    moverRobotJoint(socketRob, poseIntermedia)

def ejecutarComando(socketRob, instruccion, posePick, posePlace):

    # posePick = transformar_angulo(posePick)
    # posePlace = transformar_angulo(posePlace)

    posePick[3] = 0.243
    posePick[4] = 3.14
    posePick[5] = -0.167
    posePlace[3] = 2.008
    posePlace[4] = 2.353
    posePlace[5] = -0.052

    fichaPick(socketRob, posePick)

    if( instruccion == 2 ):
        # ESTO ES DEL ROBOT NUESTRO
        # posePick[3] = 2.232
        # posePick[4] = -2.211
        # posePlace[3] = 2.232
        # posePlace[4] = -2.211
        #fichaGirar(socketRob)

        # ESTO ES DEL ROBOT DE LOS OTROS
        # posePick[3] = 2.461
        # posePick[4] = -2.010
        # posePick[5] = -0.167
        # posePlace[3] = 2.008
        # posePlace[4] = 2.353
        # posePlace[5] = -0.052
        girarFichaAlt(socketRob)

    fichaPlace(socketRob, posePlace)

    moverEspera(socketRob)