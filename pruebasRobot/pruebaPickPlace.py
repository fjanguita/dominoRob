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

socketRob.send(("movel(p[-0.15789, 0.29909, 0.02766, 2.183, -2.231, 0.057], a=1.0, v=0.1, t=4.0)" + "\n").encode())
time.sleep(5.0)

socketRob.send(("movej([1.57, -1.57, 0.0, -1.57, 0.0, 1.1345], a=1.0, v=0.1, t=4.0)" + "\n").encode())
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