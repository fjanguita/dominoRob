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

