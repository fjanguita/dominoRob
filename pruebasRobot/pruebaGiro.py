import socket
import time

HOST = "169.254.12.28"  # IP del robot
PORT = 30002            # Puerto de escucha del robot

socketRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketRob.connect((HOST, PORT))
print("Se ha establecido la conexión con el robot.\n")
#time.sleep(2.0)

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

########## COGER LA PIEZA ###################

socketRob.send(("movej([1.57, -1.57, 0.0, -1.57, 0.0, 1.1345], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

# socketRob.send(("movej([4.079, -1.291, 0.562, -1.443, -1.471, 5.692], a=1.0, v=0.1, t=4.0)" + "\n").encode())
socketRob.send(("movej(p[-0.15789, 0.29909, 0.02766, 2.183, -2.231, 0.057], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

# socketRob.send(("movej([4.079, -1.291, 0.562, -1.443, -1.471, 5.692], a=1.0, v=0.1, t=4.0)" + "\n").encode())
socketRob.send(("movel(p[-0.17858, 0.29979, -0.05558, 2.193, -2.222, -0.013], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

comando = "set_tool_digital_out(0, False)\n"
socketRob.send(comando.encode())
time.sleep(0.1)

comando = "set_tool_digital_out(1,True)\n"
socketRob.send(comando.encode())
time.sleep(0.1)

# socketRob.send(("movej([4.079, -1.291, 0.562, -1.443, -1.471, 5.692], a=1.0, v=0.1, t=4.0)" + "\n").encode())
socketRob.send(("movel(p[-0.17858, 0.29979, 0.02766, 2.193, -2.222, -0.013], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

################# COGER LA PIEZA ###################

################# GIRAR LA PIEZA ####################

# IR A POSICION DE GIRO (ALZADA)
socketRob.send(("movej(p[-0.43541, 0.27567, 0.02766, 1.674, -1.664, -0.867], a=1.0, v=0.1, t=3.0)" + "\n").encode())
time.sleep(4.0)

# IR A POSICION DE GIRO
socketRob.send(("movel(p[-0.43541, 0.27567, -0.0100, 1.674, -1.664, -0.867], a=1.0, v=0.1, t=3.0)" + "\n").encode())
time.sleep(4.0)

# IR A POSICION DE SOLTADO (EN GIRO)
socketRob.send(("movel(p[-0.36861, 0.27567, -0.0100, 1.674, -1.664, -0.867], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

# SOLTAR PIEZA GIRADA
comando = "set_tool_digital_out(1, False)\n"
socketRob.send(comando.encode())
time.sleep(0.1)

comando = "set_tool_digital_out(0,True)\n"
socketRob.send(comando.encode())
time.sleep(0.1)

socketRob.send(("movel(p[-0.36861, 0.27567, 0.040, 1.674, -1.664, -0.867], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

# RECOLOCARSE PARA COGERLA
socketRob.send(("movej(p[-0.33865, 0.27411, 0.00285, 2.250, -2.190, 0.0], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

socketRob.send(("movel(p[-0.33865, 0.27411, -0.05456, 2.250, -2.190, 0.0], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

# RECOGER LA PIEZA GIRADA
comando = "set_tool_digital_out(0, False)\n"
socketRob.send(comando.encode())
time.sleep(0.1)

comando = "set_tool_digital_out(1,True)\n"
socketRob.send(comando.encode())
time.sleep(0.1)

socketRob.send(("movel(p[-0.37861, 0.27411, 0.00539, 2.250, -2.190, 0.0], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

################# GIRAR LA PIEZA ####################



socketRob.send(("movej([2.58116, -2.44224, -0.825337, -1.4533, 1.57, 2.1816], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

socketRob.send(("movej(p[-0.15789, 0.29909, 0.02766, 2.183, -2.231, 0.057], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

# socketRob.send(("movej([4.079, -1.291, 0.562, -1.443, -1.471, 5.692], a=1.0, v=0.1, t=4.0)" + "\n").encode())
socketRob.send(("movel(p[-0.17858, 0.29979, -0.05558, 2.193, -2.222, -0.013], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

comando = "set_tool_digital_out(1, False)\n"
socketRob.send(comando.encode())
time.sleep(0.1)

comando = "set_tool_digital_out(0,True)\n"
socketRob.send(comando.encode())
time.sleep(0.1)

print("Cerrando conexion con el robot...")
socketRob.close()