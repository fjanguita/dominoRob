import socket
import threading
import time
import torch
import numpy as np
from matplotlib import pyplot as plt
import ctypes
import os
import math
import socket
import sys
import select
import threading
import struct

class comandoVision:
    def __init__(self, comando, Npiezas, array=None):
        self.comando = comando
        self.Npiezas = Npiezas
        # Si no se proporciona un array, inicializar con arrays de 5 dimensiones llenos de ceros
        self.array = array if array is not None else np.zeros((Npiezas, 5), dtype=float)

    def serialize(self):
        # El formato de la estructura es un tipoComando seguido de un entero Npiezas y luego 5 floats por cada pieza
        narray = 5*self.Npiezas
        formato = "ii" + "f" * narray#* (5 * self.Npiezas)
        # Aplanar la lista de listas para que sea un solo array de floats
        flat_array = self.array.flatten()
        # Empaquetar los datos en formato binario
        return struct.pack(formato, self.comando, self.Npiezas, *flat_array)

    @classmethod
    def deserialize(cls, data):
        # Primero desempaquetar los dos primeros enteros
        int_format = "ii"
        int_size = struct.calcsize(int_format)
        comando, Npiezas = struct.unpack(int_format, data[:int_size])
        # Luego desempaquetar los floats, que son 5 por cada pieza
        float_format = "f" * (5 * Npiezas)
        floats = struct.unpack(float_format, data[int_size:])
        # Convertir el array plano de floats en una lista de listas
        array = np.array(floats).reshape((Npiezas, 5))
        return cls(comando, Npiezas, array)

# Apartado para la visualización de fotos
indice_actual = 0


# Dirección y puerto del servidor
addressIN =  ('0.0.0.0',5004)
addressOut = ('192.168.43.97', 5003)


real_width  = 30.5 # Largo real mm
real_height = 19.2  # Ancho real mm a 405mm

# Variable global para almacenar los datos recibidos
data_recv = ""
lock = threading.Lock()

#Cargar Red Neuronal


def px_mm(x, y,z=405):
    global real_height
    global real_width

    xmm = x / real_width
    ymm = y / real_height
    return xmm, ymm

def obtener_imagenes_en_carpeta(carpeta):
    imagenes = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith('.jpg') or archivo.endswith('.png') or archivo.endswith('.jpeg'):
            imagenes.append(archivo)
    imagenes.sort()
    return imagenes



def angulo_fichas(centros_nums, fichas_guardadas):
    Nfichas = np.size(fichas_guardadas, 0)
    angulos = np.zeros(shape=(Nfichas))

    for i in range(Nfichas):
        pos0 = int(fichas_guardadas[i][0])
        pos1 = int(fichas_guardadas[i][1])
        x = centros_nums[pos1][0] - centros_nums[pos0][0]
        y = centros_nums[pos1][1] - centros_nums[pos0][1]
        angulos[i] = math.atan2(y, x)
        if centros_nums[pos1][0] > centros_nums[pos0][0]:
            angulos[i] = 180 - angulos[i]

    return angulos

def punto_medio_fichas(array_Agente, nPiezas, results_sorted, zona, width):
    nP =0
    pos_piezas   = np.zeros(shape=(nPiezas,4))    #Valores de posición de las piezas
   
    if zona == 0:
        calibx = 522.80
        caliby = 123.1-50
        z = 530.71
    elif zona == 1:
        calibx = 522.80
        caliby = -66.43-50
        z = 530.71
    else:
        calibx = -217.42
        caliby = 351.51-50
        z = 530.71

    #cálculo de número de piezas y números
    for i in range(np.size(results_sorted['name'])): #Determinamos número de piezas y números para darle el tamaño requerido a los arrays
        if (results_sorted['name'][i] == 'Domino-Pieces'):
            pos_piezas[nP][0]=results_sorted['xmin'][i]     #Colocamos el xmin en la primera posición
            pos_piezas[nP][1]=results_sorted['xmax'][i]     #Colocamos el xmax en la segunda posición
            pos_piezas[nP][2]=results_sorted['ymin'][i]     #Colocamos el ymin en la tercera posición
            pos_piezas[nP][3]=results_sorted['ymax'][i]     #Colocamos el ymax en la cuarta posición
            nP = nP +1

    for i in range(nPiezas):
        array_Agente[i][3] = 320-((pos_piezas[i][0] + pos_piezas[i][1])/2)
        array_Agente[i][2] = ((pos_piezas[i][2] + pos_piezas[i][3])/2)-240
        array_Agente[i][3] = calcular_dimencion_real(z,width,array_Agente[i][3],0,calibx)/1000
        array_Agente[i][2] = calcular_distancia_y(array_Agente[i][2], caliby,zona)/1000

    return array_Agente

def calcular_dimencion_real(z, width, xmax, xmin, calibx):
    alpha = 60  # Ángulo de apertura de la cámara
    betaRad = math.radians(alpha / 2)
    dimension_real = calibx - ((float(z) + 30.3213232) * 2 * (xmax - xmin) * math.tan(betaRad)) / (1.62286 * width)
    return dimension_real

def calcular_distancia_y(y_med, caliby,zona):
    if  zona == 0:
        print ('y: ', y_med/16.2, ' Calibración: ', caliby)
        y = caliby + y_med / 1.62
    elif zona == 1:
        print ('Pixeles: ', y_med, ' Calibración: ', caliby)
        y = caliby - y_med / 1.92
    else:
        print ('Pixeles: ', y_med, ' Calibración: ', caliby)
        y = -(caliby + y_med / 1.92)
    return y

def calcular_punto_medio(resultados_ordenados, array_Agente):
    puntos_por_id = {}
    nP = 0
    for index, fila in resultados_ordenados.iterrows():
        name = fila['name']
        if name == 'Domino-Pieces':
            id_ = len(puntos_por_id) + 1
            xmin = fila['xmin']
            xmax = fila['xmax']
            ymin = fila['ymin']
            ymax = fila['ymax']
            Nnum = 0
            if id_ not in puntos_por_id:
                puntos_por_id[id_] = {'numeros': []}
            for index2, fila2 in resultados_ordenados.iterrows():
                if fila2['name']!= 'Domino-Pieces':
                    x_medio = int((fila2['xmin'] + fila2['xmax']) / 2)
                    y_medio = int((fila2['ymin'] + fila2['ymax']) / 2)
                    confidence = round(fila2['confidence'], 2)
                    if xmin < x_medio < xmax and ymin < y_medio < ymax and Nnum <= 1:
                        xmm,ymm = px_mm(x_medio,y_medio)
                        puntos_por_id[id_]['numeros'].append({"x": x_medio, "y": y_medio, "numero": fila2['name'], "confidence": confidence})
                        array_Agente[nP][Nnum] = int(fila2['name'])
                        Nnum = Nnum + 1
                        if (Nnum == 2):
                            Nnum = 0
            nP = nP + 1

    return puntos_por_id, array_Agente

def dibujar_lineas(imagen, puntos_por_id, array_Agente, nPiezas):
    angulos = {}
    ang_rad = np.zeros(shape=(nPiezas, 1))
    n = 0
    for id_, info in puntos_por_id.items():
        numeros = info['numeros']
        if not numeros:  # Verificar si la lista de números está vacía
            continue  # Pasar a la siguiente iteración del bucle si no hay números
        numeros_ordenados = sorted(numeros, key=lambda x: x['x'])
        
        # Obtener el primer y último punto de la línea
        try:
            punto_inicial = (numeros_ordenados[0]['x'], numeros_ordenados[0]['y'])
            punto_final = (numeros_ordenados[-1]['x'], numeros_ordenados[-1]['y'])
        except IndexError:
            continue  # Pasar a la siguiente iteración del bucle si no hay suficientes números
        
        
        # Calcular el ángulo entre la línea y el eje X
        dx = punto_final[0] - punto_inicial[0]
        dy = punto_final[1] - punto_inicial[1]
        angulo_rad = np.arctan2(dy, dx)

        angulo_grados = np.degrees(angulo_rad)
        angulo_grados = round(angulo_grados, 2)
        if punto_final[1] > punto_inicial[1]:
            if punto_final[0] > punto_inicial[0]:
                angulo_grados = 180 - angulo_grados
        else:
            if punto_final[0] > punto_inicial[0]:
                angulo_grados = -angulo_grados

        # Almacenar el ángulo asociado a cada ID
        angulos[id_] = angulo_grados
        # Agregar el ángulo al diccionario existente puntos_por_id
        info['angulo'] = angulo_grados
        # Agregamos al array que se enviará al agente el ángulo
        array_Agente[n][4] = angulo_rad
        n = n + 1

    return imagen, angulos, puntos_por_id, array_Agente

def sim_YOLO_FichasRobot(instruccion,zona):
    fichas = np.array([[4, 1, -0.315, 0.140, 1.5708],
                       [2, 3, -0.315, 0.170, 1.5708],
                       [1, 1, -0.315, 0.190, 1.5708],
                       [3, 4, -0.315, 0.220, 1.5708],
                       [3, 1, -0.315, 0.250, 1.5708],
                       [3, 3, -0.315, 0.280, 1.5708]])
    nPiezas = 6
    comando = instruccion
    robot = comandoVision(comando, nPiezas, fichas)
    serialized_data = robot.serialize()
    print(f"Serialized Data: {serialized_data}")

    deserialized_robot = comandoVision.deserialize(serialized_data)
    print(f"Deserialized Data: comando={deserialized_robot.comando}, Npiezas={deserialized_robot.Npiezas}, array={deserialized_robot.array}")

    return serialized_data, nPiezas

def sim_YOLO_ROBAR(instruccion,zona):
    fichas = np.array([0, 0, 0.043036, 0.39247,  0.033321])
    nPiezas = 1
    comando = instruccion
    robot = comandoVision(comando, nPiezas, fichas)
    serialized_data = robot.serialize()
    print(f"Serialized Data: {serialized_data}")

    deserialized_robot = comandoVision.deserialize(serialized_data)
    print(f"Deserialized Data: comando={deserialized_robot.comando}, Npiezas={deserialized_robot.Npiezas}, array={deserialized_robot.array}")

    return serialized_data, nPiezas

def sim_YOLO_TABLERO(instruccion,zona):
    fichas = np.array([[6, 6, 0.0, 0.49153, 0],
                       [6, 4, 0.0, 0.53000, 0],
                       [4, 2, 0.0, 0.57000, 0]])
    nPiezas = 3
    comando = instruccion
    robot = comandoVision(comando, nPiezas, fichas)
    serialized_data = robot.serialize()
    print(f"Serialized Data: {serialized_data}")

    deserialized_robot = comandoVision.deserialize(serialized_data)
    print(f"Deserialized Data: comando={deserialized_robot.comando}, Npiezas={deserialized_robot.Npiezas}, array={deserialized_robot.array}")

    return serialized_data, nPiezas

def sim_YOLO_ROBAR_inicio(instruccion,zona):
    fichas = np.array([[0, 0, 0.045974, 0.49153, 0.032247],
                       [0, 0, 0.080869, 0.43813,-0.033321],
                       [0, 0, 0.079753, 0.48742,-0.033321],
                       [0, 0, 0.080331, 0.39186, 0],
                       [0, 0, 0.047698, 0.54272, -0.099669],
                       [0, 0, 0.079107, 0.54021, -0.034469],
                       [0, 0, 0.045725, 0.44469, -0.13255],
                       [0, 0, 0.043036, 0.39247,  0.033321]])
    nPiezas = 8
    comando = instruccion
    robot = comandoVision(comando, nPiezas, fichas)
    serialized_data = robot.serialize()
    print(f"Serialized Data: {serialized_data}")

    deserialized_robot = comandoVision.deserialize(serialized_data)
    print(f"Deserialized Data: comando={deserialized_robot.comando}, Npiezas={deserialized_robot.Npiezas}, array={deserialized_robot.array}")

    return serialized_data, nPiezas

def centro_nums(results_sorted,nPiezas):
    nP =0
    nNum = 0
    for i in range(np.size(results_sorted['name'])): #Determinamos número de piezas y números para darle el tamaño requerido a los arrays
        if (results_sorted['name'][i] != 'Domino-Pieces'):
            nNum = nNum +1

    pos_nums   = np.zeros(shape=(nNum,4))    #Valores de posición de los números
    pos_piezas   = np.zeros(shape=(nPiezas,4))    #Valores de posición de las piezas
    num_name = np.zeros(shape=(nNum,1))
    #cálculo de número de piezas y números
    for i in range(np.size(results_sorted['name'])): #Determinamos número de piezas y números para darle el tamaño requerido a los arrays
        if (results_sorted['name'][i] != 'Domino-Pieces'):
            pos_nums[nP][0]=results_sorted['xmin'][i]     #Colocamos el xmin en la primera posición
            pos_nums[nP][1]=results_sorted['xmax'][i]     #Colocamos el xmax en la segunda posición
            pos_nums[nP][2]=results_sorted['ymin'][i]     #Colocamos el ymin en la tercera posición
            pos_nums[nP][3]=results_sorted['ymax'][i]     #Colocamos el ymax en la cuarta posición
            num_name[nP] = results_sorted['name'][i]
            nP = nP +1
        else:
            pos_piezas[nP][0]=results_sorted['xmin'][i]     #Colocamos el xmin en la primera posición
            pos_piezas[nP][1]=results_sorted['xmax'][i]     #Colocamos el xmax en la segunda posición
            pos_piezas[nP][2]=results_sorted['ymin'][i]     #Colocamos el ymin en la tercera posición
            pos_piezas[nP][3]=results_sorted['ymax'][i]     #Colocamos el ymax en la cuarta posición

    centros = np.zeros(shape=(nP,2))
    for i in range(nP):
        centros[i][0] = (pos_nums[i][0] + pos_nums[i][1])/2
        centros[i][1] = (pos_nums[i][2] + pos_nums[i][3])/2
    
    return centros, nP, pos_piezas, num_name

def Numeros_a_piezas(results_sorted,array_Agente, nPiezas):
    piezas_guardada = np.zeros(shape=(nPiezas,2))   #Para tener el recuento de los números guardados en cada pieza
    centros,nNums,pos_piezas, num_name = centro_nums(results_sorted,nPiezas)
    for i in range(nPiezas):                #Se estudia en cada número obtenido en cámara si está dentro de los límites de una pieza
         
        n=0                                 #Para contabilizar el número de valores en cada pieza (no ha de superar los 2 valores)
        for j in range(nNums): 
            if (centros[j][0]<pos_piezas[i][1]) and (centros[j][0]>pos_piezas[i][0]) and (centros[j][1]<pos_piezas[i][3]) and (centros[j][1]>pos_piezas[i][2]):
                array_Agente[i][n] = int(num_name[j])
                piezas_guardada[i][n] = j
                n=n+1
    return array_Agente



partida = 1
continuar = 0
instruccion = 0

# Creamos un objeto Condition
condicion = threading.Condition()

def recibirInterfaz():
    global partida,continuar,instruccion, condicion

    direccion = '0.0.0.0'
    puerto = 1434
    rcvInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvInt.bind((direccion, puerto))
    rcvInt.listen(1)
    print("Esperando conexion de la interfaz...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvInt, direccionRcvInt = rcvInt.accept()
    print("Conexion establecida desde: ", direccionRcvInt,"\n")

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvInt.recv(8).decode()
        
        if (mensaje != ''):
            print("Se ha recibido el mensaje: ", mensaje,"\n")
            if(mensaje == '0'):
                partida = 0
            elif(mensaje == '-1'):
                continuar = 1
            else:
                instruccion = int(mensaje)
            with condicion:
                condicion.notify()

def recibirAgente():
    global partida,continuar,instruccion, condicion

    direccion = '0.0.0.0'
    puerto = 1436
    rcvInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvInt.bind((direccion, puerto))
    rcvInt.listen(1)
    print("Esperando conexion de la interfaz...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvInt, direccionRcvInt = rcvInt.accept()
    print("Conexion establecida desde: ", direccionRcvInt,"\n")

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvInt.recv(8).decode()
        # print("Se ha recibido el mensaje: ", mensaje,"\n")
        # try:
        #     partida = int(mensaje)
        # except:
        #     print("Mensaje recibido NO VALIDO\n")
        if (mensaje != ''):
            print("Se ha recibido el mensaje: ", mensaje,"\n")
            if(mensaje == '0'):
                partida = 0
            elif(mensaje == '-1'):
                continuar = 1
            else:
                instruccion = int(mensaje)
            with condicion:
                condicion.notify()

    print("Cerrando los sockets")
    clienteRcvInt.close()
    rcvInt.close()

def conectarInterfaz():
    direccion = '192.168.20.14'
    puerto = 1406
    envInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envInt.connect((direccion, puerto))

    return envInt

def conectarAgente():
    direccion = '192.168.20.14'
    puerto = 1435
    envAg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envAg.connect((direccion, puerto))

    return envAg

envInt = conectarInterfaz()

thInt = threading.Thread(target=recibirInterfaz)
thInt.daemon = True
thInt.start()
thAg = threading.Thread(target=recibirAgente)
thAg.daemon = True
thAg.start()

while(continuar == 0):
    print("Esperando señal de la Interfaz...")
    time.sleep(2.0)

envAg = conectarAgente()
msgAgente = '1'

while(partida):
    with condicion:
        print('Dentro del programa...')
        condicion.wait()

        if(instruccion == 3):
            zona = 1
            print("Solicitando al agente que mueva al robot hasta 'Zona Robo'...")
            instr = comandoVision(3,1,np.zeros(shape=(1,5)))
            envAg.send(instr.serialize())

            condicion.wait()
            print("Robot en 'Zona Robo'. Enviando imagen...")
            time.sleep(2.0)

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA EL AGENTE
            # SI NO HAY FICHAS DE ROBO, ENVIAR AL AGENTE UN '8'
            data, nPiezas = sim_YOLO_ROBAR(instruccion,zona)

            if( nPiezas == 0 ):
                instr = comandoVision(8,1,np.zeros(shape=(1,5)))
                envAg.send(instr.serialize())
                condicion.wait()
                envInt.send('-1'.encode())
            else:
                envAg.send(data)

        if(instruccion == 4):
            zona = 2

            print("Solicitando al agente que mueva al robot hasta 'Zona Fichas'...")
            instr = comandoVision(4,1,np.zeros(shape=(1,5)))
            envAg.send(instr.serialize())

            condicion.wait()
            print("Robot en 'Zona Fichas'. Enviando imagen...")

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA EL AGENTE
            data, nPiezas = sim_YOLO_FichasRobot(instruccion,zona)

            time.sleep(2.0)
            envAg.send(data)

            # ESPERA A QUE EL AGENTE ACTUALICE SUS FICHAS
            condicion.wait()
            # ENVIA CONFIRMACION A INTERFAZ PARA FINALIZAR TURNO
            envInt.send('-1'.encode())


        if(instruccion == 1):
            zona = 0

            print("Solicitando al agente que mueva al robot hasta 'Zona Tablero'...")
            instr = comandoVision(5,1,np.zeros(shape=(1,5)))
            envAg.send(instr.serialize())

            condicion.wait()
            print("Robot en 'Zona Tablero'. Enviando imagen...")

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA EL AGENTE
            data, nPiezas = sim_YOLO_TABLERO(instruccion,zona)

            time.sleep(2.0)
            envAg.send(data)
            
        

        # Instruccion 7 comienza la secuencia inicial de robo
        if(instruccion == 7):
            zona = 1

            print("Solicitando al agente que mueva al robot a 'Zona Robo'...\n")
            instr = comandoVision(3,1,np.zeros(shape=(1,5)))
            envAg.send(instr.serialize())

            # Espera confirmacion de que el robot está en zona de robo
            condicion.wait()
            print("Robot en 'Zona Robo'. Enviando imagen al agente...\n")

            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA ENVIAR FICHAS DE ROBO AL AGENTE
            data, nPiezas = sim_YOLO_ROBAR_inicio(instruccion,zona)
            #data, nPiezas = sim_YOLO(instruccion,zona)

            time.sleep(2.0)
            # CAMBIAR EL '7' POR VUESTRO MENSAJE FORMATEADO CON UN 7 EN EL CAMPO DE INSTRUCCION
            envAg.send(data)

            # ESPERA A QUE EL ROBOT TENGA TODAS SUS FICHAS PARA HACERLE UNA FOTO
            condicion.wait()
            instr = comandoVision(4,1,np.zeros(shape=(1,5)))
            envAg.send(instr.serialize())
            condicion.wait()
            print("Fichas del robot listas. Enviando imagen al agente...\n")
            
            zona = 2
            # PROCESAR IMAGENES Y FORMATEAR EL MENSAJE PARA ENVIAR FICHAS DISPONIBLES AL AGENTE
            # CAMBIAR EL '6' POR VUESTRO MENSAJE FORMATEADO CON UN 6 EN EL CAMPO DE INSTRUCCION
            data, nPiezas = sim_YOLO_FichasRobot(6,zona)
            #data, nPiezas = sim_YOLO(instruccion,zona)
            envAg.send(data)

            # ESPERA A QUE EL AGENTE LE DIGA EL DOBLE MAS ALTO
            condicion.wait()
            doble = str(instruccion)

            # Devuelve el doble mas alto a la interfaz
            envInt.send(doble.encode())



thInt.join()
thAg.join()