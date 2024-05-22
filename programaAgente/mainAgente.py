import socket
from comandoRobot import comandoRobot
from comandoVision import comandoVision
import threading
import time
import struct
import numpy as np
import math

partida = 1
continuar = 0

instruccion = 0

# Creamos un objeto Condition
condicion = threading.Condition()

def recibirInterfaz():
    global partida, continuar, instruccion, condicion

    direccion = 'localhost'
    puerto = 1424
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
            elif( mensaje == '-1' ):
                continuar = 1
            else:
                instruccion = int(mensaje)
            with condicion:
                condicion.notify()

    print("Cerrando los sockets")
    clienteRcvInt.close()
    rcvInt.close()


def recibirVision():
    global partida, continuar, instruccion, condicion, fichas_vis, num_piezas
    direccion = 'localhost'
    puerto = 1435
    rcvInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvInt.bind((direccion, puerto))
    rcvInt.listen(1)
    print("Esperando conexion de Vision...\n")

    # Bloquea hasta que recibe una conexion
    clienteRcvInt, direccionRcvInt = rcvInt.accept()
    print("Conexion establecida desde: ", direccionRcvInt,"\n")

    # Bucle para manejar la llegada de mensajes
    while(partida):
        mensaje = clienteRcvInt.recv(8).decode()
        if (mensaje != ''):
            estructura = comandoVision.deserialize(mensaje)
            print("Se ha recibido el mensaje:\n   ", estructura.array,"\n   ", estructura.comando,"\n   ", estructura.Npiezas,"\n")

            fichas_vis = estructura.array
            instruccion = estructura.comando
            num_piezas = estructura.Npiezas

            with condicion:
                condicion.notify()
                
    print("Cerrando los sockets")
    clienteRcvInt.close()
    rcvInt.close()


def recibirRobot():
    global partida, continuar, instruccion, condicion

    direccion = 'localhost'
    puerto = 1428
    rcvInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcvInt.bind((direccion, puerto))
    rcvInt.listen(1)
    print("Esperando conexion de Robot...\n")

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

    print("Cerrando los sockets")
    clienteRcvInt.close()
    rcvInt.close()

def conectarInterfaz():
    direccion = 'localhost'
    puerto = 1405
    envInt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envInt.connect((direccion, puerto))

    return envInt

def conectarRobot():
    direccion = 'localhost'
    puerto = 1415
    envRob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envRob.connect((direccion, puerto))

    return envRob

def conectarVision():
    direccion = 'localhost'
    puerto = 1436
    envVis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    envVis.connect((direccion, puerto))

    return envVis


envInt = conectarInterfaz()

thInt = threading.Thread(target=recibirInterfaz)
thInt.daemon = True
thInt.start()
thVis = threading.Thread(target=recibirVision)
thVis.daemon = True
thVis.start()
thRob = threading.Thread(target=recibirRobot)
thRob.daemon = True
thRob.start()

while(continuar == 0):
    print("Esperando señal de la Interfaz...")
    time.sleep(2.0)

envRob = conectarRobot()
envVis = conectarVision()

array_vacio = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
msg = comandoRobot(1,array_vacio,array_vacio)
msg_zona1 = comandoRobot(3,array_vacio,array_vacio)
msg_zona2 = comandoRobot(4,array_vacio,array_vacio)
msg_zona3 = comandoRobot(5,array_vacio,array_vacio)
msg_robar = comandoRobot(2,array_vacio,array_vacio)


#### AGENTE 
class Ficha:
    def __init__(self, valorA, valorB, coorX=0, coorY=0, orientacion=0.0, spin=False):
        self.valorA = valorA
        self.valorB = valorB
        self.coorX = coorX
        self.coorY = coorY
        self.orientacion = orientacion
        self.spin = spin
        self.grosor= 0.03

    def ver(self):
        spin_texto = "girada" if self.spin else "no girada"
        orientacion_grados = math.degrees(self.orientacion) % 360
        return f"Ficha: {self.valorA}-{self.valorB}, {spin_texto}, Posición: ({self.coorX}, {self.coorY}), Orientación: {orientacion_grados} grados"

class Ficha_Robo:
    def __init__(self, coorX, coorY, orientacion):
        self.coorX = coorX
        self.coorY = coorY
        self.orientacion = orientacion

    def __repr__(self):
        return f"Ficha_Robo(coorX={self.coorX}, coorY={self.coorY}, orientacion={self.orientacion})"
    
    @staticmethod
    def procesar_fichas(array_fichas):
        # Verify that the array length is a multiple of 3 since each ficha has three data points
        if len(array_fichas) % 3 != 0:
            raise ValueError("Array length must be a multiple of 3.")

        fichas = []
        for i in range(0, len(array_fichas), 3):
            coorX = array_fichas[i]
            coorY = array_fichas[i + 1]
            orientacion = array_fichas[i + 2]
            ficha = Ficha_Robo(coorX, coorY, orientacion)
            fichas.append(ficha)
        
        return fichas

class RecFichas:
    @classmethod
    def deserialize(cls, data):
        # Primeros 4 bytes contienen la cantidad de fichas
        cantidad_fichas = struct.unpack("i", data[:4])[0]
        # El resto de los datos contiene los valores flotantes de las fichas
        formato = "f" * 5 * cantidad_fichas
        fichas_datos = struct.unpack(formato, data[4:])
        # Crear lista de fichas a partir de los datos desempaquetados
        fichas = [list(fichas_datos[i * 5:(i + 1) * 5]) for i in range(cantidad_fichas)]
        return fichas

class Agente:
    def __init__(self):
        self.fichas_juego = []  # Fichas en el espacio de juego
        self.fichas_disponibles = []  # Fichas disponibles del agente
        self.fichas_nuevas_juego = []  # Fichas nuevas en el espacio de juego
        self.extremos= [] #Extremos del juego
        self.fichas_seleccionadas_para_jugar = [] #Fichas elegidas
        self.fichas_ayuda=[]
        self.robo_set = []

    def añadir_fichas_desde_arrays(self, arrays_fichas, es_disponible=True):
        destino = self.fichas_disponibles if es_disponible else self.fichas_nuevas_juego
        for array_ficha in arrays_fichas:
            if len(array_ficha) == 5:
                valorA, valorB, coorX, coorY, orientacion = array_ficha
                # Verificar si la ficha ya existe en el destino SOLO si son fichas disponibles
                if es_disponible:
                    ficha_existe = any(ficha.valorA == valorA and ficha.valorB == valorB and 
                                       ficha.coorX == coorX and ficha.coorY == coorY and 
                                       math.isclose(ficha.orientacion, orientacion, abs_tol=1e-9) for ficha in self.fichas_disponibles)
                    if not ficha_existe:
                        nueva_ficha = Ficha(valorA, valorB, coorX, coorY, orientacion)
                        destino.append(nueva_ficha)
                    else:
                        print(f"Ficha {valorA}-{valorB} en posición ({coorX}, {coorY}) con orientación {math.degrees(orientacion) % 360} grados ya existe en fichas disponibles, no se añade nuevamente.")
                else:
                    # Para fichas de juego, se añade sin verificar duplicados
                    nueva_ficha = Ficha(valorA, valorB, coorX, coorY, orientacion)
                    destino.append(nueva_ficha)
            else:
                print("Error: Uno de los arrays proporcionados no tiene el formato correcto.")

    def ver_fichas(self, es_disponible=True):
        destino = self.fichas_disponibles if es_disponible else self.fichas_juego
        for ficha in destino:
            print(ficha.ver())

    def ver_fichas_nuevas_juego(self):
        print("Fichas nuevas en el espacio de juego:")
        for ficha in self.fichas_nuevas_juego:
            print(ficha.ver())

    def añadir_fichas_robo_desde_array(self, array_fichas):
        fichas_robo = Ficha_Robo.procesar_fichas(array_fichas)
        self.robo_set.extend(fichas_robo)
        print(f"Fichas de robo añadidas: {fichas_robo}")

    def encontrar_ficha_de_mayor_valor(fichas_seleccionadas_para_jugar):#CAMBIAR LA FUNCIÓN OTRA DONDE ELIGE FICHAS
        # Filtra las fichas que tienen el mismo valor en A y B
        fichas_con_valores_iguales = [ficha for ficha in fichas_seleccionadas_para_jugar if ficha.valorA == ficha.valorB]
        
        if not fichas_con_valores_iguales:
            print("No hay fichas con valores iguales en A y B.")
            return None
        
        # Encuentra la ficha con el mayor valor repetido
        ficha_de_mayor_valor = max(fichas_con_valores_iguales, key=lambda ficha: ficha.valorA)
        
        return ficha_de_mayor_valor
    
    def comprueba_fin_juego(self):
        # Calcular el total de fichas (disponibles + en juego).
        total_fichas = len(self.fichas_disponibles) + len(self.fichas_juego)

        # Calcular el número de fichas desconocidas restando el total de fichas conocidas de 21.
        fichas_desconocidas = 21 - total_fichas

        # Comprobar si no hay fichas desconocidas.
        if fichas_desconocidas == 0:
            print("El juego se ha cerrado.")
            
            # Calcular la suma de todos los valorA y valorB de las fichas disponibles.
            suma_valores_disponibles = sum(ficha.valorA + ficha.valorB for ficha in self.fichas_disponibles)
            
            print(f"Suma de los valores de las fichas disponibles: {suma_valores_disponibles}")
            return True
        else:
            print(f"El juego aún no se ha cerrado. Fichas desconocidas restantes: {fichas_desconocidas}")
            return False

    def actualizar_estado_juego(self):
        # Identificar fichas nuevas comparando fichas_nuevas_juego con el estado anterior en fichas_juego
        fichas_nuevas_reales = [ficha_nueva for ficha_nueva in self.fichas_nuevas_juego 
                                if not any(ficha_nueva.valorA == ficha.valorA and 
                                           ficha_nueva.valorB == ficha.valorB and
                                           ficha_nueva.coorX == ficha.coorX and
                                           ficha_nueva.coorY == ficha.coorY and
                                           math.isclose(ficha_nueva.orientacion, ficha.orientacion, abs_tol=1e-9) 
                                           for ficha in self.fichas_juego)] 
        cantidad_fichas_nuevas = len(fichas_nuevas_reales)
        print("Cantidad fichas nuevas juego:", cantidad_fichas_nuevas)
        if cantidad_fichas_nuevas == 0:#REVISAR
            print("No hay fichas nuevas reales para actualizar el juego.")
            
        # Actualizar los extremos según la cantidad y posición de las fichas nuevas
        if not self.fichas_juego:  # Si es el inicio del juego
             self.extremos = [self.fichas_nuevas_juego[0], self.fichas_nuevas_juego[0]]
        elif cantidad_fichas_nuevas >= 1:
            # Determinar la posición de las fichas nuevas para ajustar los extremos
            mitad_array = len(self.fichas_nuevas_juego) // 2
            indices_nuevas = [self.fichas_nuevas_juego.index(ficha) for ficha in fichas_nuevas_reales]
            if cantidad_fichas_nuevas == 1:
                if indices_nuevas[0] < mitad_array:
                    self.extremos[0] = fichas_nuevas_reales[0]  # Nueva ficha como extremo izquierdo
                else:
                    self.extremos[1] = fichas_nuevas_reales[0]  # Nueva ficha como extremo derecho
            else:  # cantidad_fichas_nuevas == 2
                # Ordenar las fichas nuevas por su índice para decidir los extremos
                fichas_ordenadas_por_posicion = sorted(fichas_nuevas_reales, key=lambda x: indices_nuevas[fichas_nuevas_reales.index(x)])
                self.extremos = [fichas_ordenadas_por_posicion[0], fichas_ordenadas_por_posicion[1]]
        if self.extremos:
            print("\nFichas en los extremos del juego después de actualizar:")
            print("Extremo izquierdo:", self.extremos[0].ver())
            print("Extremo derecho:", self.extremos[1].ver())

        self.fichas_juego.clear()
        self.fichas_juego = self.fichas_nuevas_juego.copy()
        self.fichas_nuevas_juego.clear()

        juego_terminado=self.comprueba_fin_juego()#MIRAR COMO SE CIERRA EL JUEGO Y BLOQUEA SELECCIONAR FICHA PARA JUGAR
        # FUNCION ACTUALIZAR ESTADO JUEGO TIENE QUE TERMINAR AQUI

        # ESTE BLOQUE IF-ELSE VA FUERA DE LA FUNCIÓN
        if not juego_terminado:
            self.comprobar_ficha_para_jugar()
            print("\nFichas en el espacio de juego después de actualizar sin contar con la nueva elegida:")
            self.ver_fichas(es_disponible=False)
            print("....")
        else:
            print("\nFin NO SE ELIGE FICHA")

    def comprobar_ficha_para_jugar(self):
        self.fichas_seleccionadas_para_jugar.clear()
        self.fichas_ayuda=[]
        self.loc_extremo_iz=False
        if not self.extremos:
            print("No hay extremos definidos aún.")
            return None
        valor_izquierdo, valor_derecho = self.extremos[0].valorA, self.extremos[1].valorB

        for i, ficha in enumerate(self.fichas_disponibles):
            if ficha.valorA == valor_izquierdo or ficha.valorB == valor_izquierdo:
                self.fichas_ayuda.append((i, 'izquierdo'))
                self.fichas_seleccionadas_para_jugar.append(ficha)
                print(f"Opción de ficha para jugar lado izq: {ficha.valorA}-{ficha.valorB}")
            if ficha.valorA == valor_derecho or ficha.valorB == valor_derecho:
            # Evitar duplicados si la ficha encaja en ambos lados
                if not (ficha.valorA == valor_izquierdo or ficha.valorB == valor_izquierdo):
                    self.fichas_ayuda.append((i, 'derecho'))
                    self.fichas_seleccionadas_para_jugar.append(ficha)
                print(f"Opción de ficha para jugar lado der: {ficha.valorA}-{ficha.valorB}")

       
        if not self.fichas_seleccionadas_para_jugar:
            return False
        else: 
            return True
    
    def seleccionar_ficha_para_robar(self):
        if self.robo_set:
            next_ficha_robo = self.robo_set.pop(0)  # Tomamos la primera y la quitamos
            print(f"Tomando ficha de robo: {next_ficha_robo.coorX}, {next_ficha_robo.coorY}, {math.degrees(next_ficha_robo.orientacion)} grados")
            if self.fichas_disponibles:
                last_ficha = self.fichas_disponibles[-1]
                next_posX = last_ficha.coorX + 2
                next_posY = last_ficha.coorY
                next_orient = last_ficha.orientacion
            else: # No se debería llegar nunca pero por si acaso
                next_posX, next_posY, next_orient = 0, -3, math.pi / 2
            print(f"Tomando ficha de robo: Posición donde irá: ({next_posX}, {next_posY}), Orientación: {math.degrees(next_orient)%360} grados")
        else:
            print("No hay fichas disponibles para jugar ni para robar.")# Aqui llamaríamos a función que envíe pasar

    def seleccionar_ficha_para_jugar(self):
            # ESTO HAY QUE SACARLO DE AQUÍ Y HACERLO UNA FUNCIÓN NUEVA
        if self.robo_set:
            next_ficha_robo = self.robo_set.pop(0)  # Tomamos la primera y la quitamos
            print(f"Tomando ficha de robo: {next_ficha_robo.coorX}, {next_ficha_robo.coorY}, {math.degrees(next_ficha_robo.orientacion)} grados")
            if self.fichas_disponibles:
                last_ficha = self.fichas_disponibles[-1]
                next_posX = last_ficha.coorX + 2
                next_posY = last_ficha.coorY
                next_orient = last_ficha.orientacion
            else: # No se debería llegar nunca pero por si acaso
                next_posX, next_posY, next_orient = 0, -3, math.pi / 2
            print(f"Tomando ficha de robo: Posición donde irá: ({next_posX}, {next_posY}), Orientación: {math.degrees(next_orient)%360} grados")
        else:
            print("No hay fichas disponibles para jugar ni para robar.")#Aqui llamaríamos a función que envíe pasar

        ficha_elegida=self.elegir_ficha_mas_adecuada()

        if ficha_elegida:
            print(f"Ficha definitiva seleccionada para jugar: {ficha_elegida.valorA}-{ficha_elegida.valorB}")
            self.buscar_ficha(ficha_elegida)
            self.buscar_extremo(ficha_elegida)
            self.fichas_disponibles.remove(ficha_elegida)
            if len(self.fichas_disponibles) == 0:
                print("¡Has ganado el juego al quedarte sin fichas!")
                return
        
            print("Fichas disponibles después de jugar:")
            self.ver_fichas(es_disponible=True)

    def buscar_ficha(self,ficha_elegida):
        try:
            indice_ficha = self.fichas_disponibles.index(ficha_elegida) 
        except ValueError:
            print("NO SE ENCONTRÓ EL ÍNDICE")
        ficha_sel=self.fichas_disponibles[indice_ficha] 
        print(f"Antigua POSICION: {ficha_sel.valorA}-{ficha_sel.valorB} en posición ({ficha_sel.coorX}, {ficha_sel.coorY}) con orientación {math.degrees(ficha_sel.orientacion) % 360} ")

    def buscar_extremo(self,ficha_elegida):  
    # Buscar el índice de la ficha elegida en fichas_disponibles
        try:
            indice_ficha = self.fichas_disponibles.index(ficha_elegida)
        except ValueError:
            print("NO SE ENCONTRÓ EL ÍNDICE")
        ficha_def=self.fichas_disponibles[indice_ficha]
        # Buscar el índice en fichas_posibles para determinar el extremo
        for ficha in self.fichas_ayuda:
            if ficha[0] == indice_ficha:#ficha[0] es el identificado y ficha[1] el extremo recorre hasta que encuentra el índice y saca el extremo asociado
                print(f"La ficha {ficha_elegida.valorA}-{ficha_elegida.valorB} puede jugarse en el extremo {ficha[1]}.")
                
                if ficha[1]=="izquierdo":
                    print("Considerada como izquierdo")
                    if ficha_def.valorA==self.extremos[0].valorA and ficha_def.valorA!=ficha_def.valorB:#si tenemos a y b pos vertical y no es ficha doble va arriba y la giramos
                        if (self.extremos[0].orientacion==math.pi/2 or self.extremos[0].orientacion==3*math.pi/2) and self.extremos[0].valorA!=self.extremos[0].valorB:
                            ficha_def.orientacion=self.extremos[0].orientacion+math.pi
                            ficha_def.coorX=self.extremos[0].coorX
                            ficha_def.coorY=self.extremos[0].coorY+2
                        #si es ficha doble va la izquierda y se gira para juntar a con el valor giramos a la izquierda 3pi/2
                        elif (self.extremos[0].orientacion==math.pi/2 or self.extremos[0].orientacion==3*math.pi/2) and self.extremos[0].valorA==self.extremos[0].valorB:
                            ficha_def.orientacion=self.extremos[0].orientacion+3*math.pi/2
                            ficha_def.coorX=self.extremos[0].coorX-2
                            ficha_def.coorY=self.extremos[0].coorY 
                        #si está en horizontal giramos pi      
                        elif (self.extremos[0].orientacion==0 or self.extremos[0].orientacion==math.pi):
                            ficha_def.orientacion=self.extremos[0].orientacion+math.pi
                            ficha_def.coorX=self.extremos[0].coorX-2
                            ficha_def.coorY=self.extremos[0].coorY
                    

                    if ficha_def.valorB==self.extremos[0].valorA and ficha_def.valorA!=ficha_def.valorB:
                        #si la ficha está vertical y no es doble subimos solo en Y
                        if (self.extremos[0].orientacion==math.pi/2 or self.extremos[0].orientacion==3*math.pi/2) and self.extremos[0].valorA!=self.extremos[0].valorB:
                            ficha_def.orientacion=self.extremos[0].orientacion
                            ficha_def.coorX=self.extremos[0].coorX
                            ficha_def.coorY=self.extremos[0].coorY+2#PENSAR como hacer si la pone hacia abajo!!!!!!!!!
                        #si es ficha doble va la izquierda y se gira para juntar a con el valor giramos a la izquierda 3pi/2
                        elif (self.extremos[0].orientacion==math.pi/2 or self.extremos[0].orientacion==3*math.pi/2) and self.extremos[0].valorA==self.extremos[0].valorB:
                            ficha_def.orientacion=self.extremos[0].orientacion+3*math.pi/2
                            ficha_def.coorX=self.extremos[0].coorX-2
                            ficha_def.coorY=self.extremos[0].coorY 
                        #si está en horizontal mantenemos pi      
                        elif (self.extremos[0].orientacion==0 or self.extremos[0].orientacion==math.pi):
                            ficha_def.orientacion=self.extremos[0].orientacion
                            ficha_def.coorX=self.extremos[0].coorX-2
                            ficha_def.coorY=self.extremos[0].coorY
                            
 
                    if ficha_def.valorA==ficha_def.valorB:#Si es ficha doble giramos pi/2
                        ficha_def.orientacion=self.extremos[0].orientacion+math.pi/2
                        if self.extremos[0].orientacion==math.pi/2 or self.extremos[0].orientacion==3*math.pi/2:#si la ficha anterior es vertical subimos
                            ficha_def.coorX=self.extremos[0].coorX
                            ficha_def.coorY=self.extremos[0].coorY+2
                        else:#si no nos movemos a la izquierda
                            ficha_def.coorX=self.extremos[0].coorX-1.5
                            ficha_def.coorY=self.extremos[0].coorY
                    
                if ficha[1]=="derecho":
                    print("Considerada como derecho")
                    if ficha_def.valorB==self.extremos[1].valorB and ficha_def.valorA!=ficha_def.valorB:
                        if (self.extremos[1].orientacion==math.pi/2 or self.extremos[1].orientacion==3*math.pi/2) and self.extremos[1].valorA!=self.extremos[1].valorB:
                            ficha_def.orientacion=self.extremos[1].orientacion+math.pi
                            ficha_def.coorX=self.extremos[1].coorX
                            ficha_def.coorY=self.extremos[1].coorY-2
                        #si es ficha doble va la izquierda y se gira para juntar a con el valor giramos a la izquierda 3pi/2
                        elif (self.extremos[1].orientacion==math.pi/2 or self.extremos[1].orientacion==3*math.pi/2) and self.extremos[1].valorA==self.extremos[1].valorB:
                            ficha_def.orientacion=self.extremos[1].orientacion+3*math.pi/2
                            ficha_def.coorX=self.extremos[1].coorX+2
                            ficha_def.coorY=self.extremos[1].coorY 
                        #si está en horizontal giramos pi      
                        elif (self.extremos[1].orientacion==0 or self.extremos[1].orientacion==math.pi):
                            ficha_def.orientacion=self.extremos[1].orientacion+math.pi
                            ficha_def.coorX=self.extremos[1].coorX+2
                            ficha_def.coorY=self.extremos[1].coorY

                    if ficha_def.valorA==self.extremos[1].valorB and ficha_def.valorA!=ficha_def.valorB:
                        #si la ficha está vertical y no es doble subimos solo en Y
                        if (self.extremos[1].orientacion==math.pi/2 or self.extremos[1].orientacion==3*math.pi/2) and self.extremos[1].valorA!=self.extremos[1].valorB:
                            ficha_def.orientacion=self.extremos[1].orientacion
                            ficha_def.coorX=self.extremos[1].coorX
                            ficha_def.coorY=self.extremos[1].coorY-2#PENSAR como hacer si la pone hacia abajo!!!!!!!!!
                        #si es ficha doble va la izquierda y se gira para juntar a con el valor giramos a la izquierda 3pi/2
                        elif (self.extremos[1].orientacion==math.pi/2 or self.extremos[1].orientacion==3*math.pi/2) and self.extremos[1].valorA==self.extremos[1].valorB:
                            ficha_def.orientacion=self.extremos[1].orientacion+3*math.pi/2
                            ficha_def.coorX=self.extremos[1].coorX+2
                            ficha_def.coorY=self.extremos[1].coorY 
                        #si está en horizontal mantenemos pi      
                        elif (self.extremos[1].orientacion==0 or self.extremos[1].orientacion==math.pi):
                            ficha_def.orientacion=self.extremos[1].orientacion
                            ficha_def.coorX=self.extremos[1].coorX+2
                            ficha_def.coorY=self.extremos[1].coorY

                    if ficha_def.valorA==ficha_def.valorB:#si tenemos ficha doble giramos pi/2
                        ficha_def.orientacion=self.extremos[1].orientacion+math.pi/2
                        if self.extremos[1].orientacion==math.pi/2 or self.extremos[1].orientacion==3*math.pi/2:#si la ficha está vertical bajamos
                            ficha_def.coorX=self.extremos[1].coorX
                            ficha_def.coorY=self.extremos[1].coorY-2
                        else:#si no nos movemos a la derecha
                            ficha_def.coorX=self.extremos[1].coorX+1.5
                            ficha_def.coorY=self.extremos[1].coorY
                print(f"NUEVA POSICION: {ficha_def.valorA}-{ficha_def.valorB} en posición ({ficha_def.coorX}, {ficha_def.coorY}) con orientación {math.degrees(ficha_def.orientacion) % 360} ")


    def elegir_ficha_mas_adecuada(self):
        # Verifica si hay fichas seleccionadas para jugar
        if not self.fichas_seleccionadas_para_jugar:
            print("No hay fichas seleccionadas para jugar.")
            return None
        
        ficha_mas_adecuada=self.encontrar_ficha_de_mayor_valor()
        #Selecciona ficha doble
        if ficha_mas_adecuada:
            return ficha_mas_adecuada
        #Si no Selecciona la ficha con el mayor valor total
        ficha_mas_adecuada = max(self.fichas_seleccionadas_para_jugar, key=lambda ficha: ficha.valorA + ficha.valorB)
        print(f"Ficha más adecuada seleccionada para jugar: {ficha_mas_adecuada.valorA}-{ficha_mas_adecuada.valorB}")
        return ficha_mas_adecuada

def convertir_a_array(Array_str,Npiezas):
    tamaño = len(Array_str)
    array = np.zeros(shape=(Npiezas,5))
    pieza = 0
    valor = 0

    i=0
    while i<tamaño:
        num = ''
        while Array_str[i] != ' ' and Array_str[i] != '[' and Array_str[i] != ']' and Array_str[i] != '\n':
            num = num + Array_str[i]  #Si se trata de parte de un número lo añadimos a la cadena
            i=i+1  #Se avanza en el elemento de la cadena
        if num != '':
            array[pieza][valor] = float(num)

            #Cambiamos posición en el array    
            valor = valor + 1
            if valor >= 5:
                valor = 0
                pieza = pieza + 1

        i=i+1  #Se avanza en el elemento de la cadena

    return array

# Función para recibir mensajes y enviar una confirmación al agente
def recibir_y_confirmararray(conn):
    try:
        Npiezas = int(conn.recv(4096).decode())
        print('Número de fichas:', Npiezas)
        Array_str = conn.recv(4096).decode()
        array = convertir_a_array(Array_str,Npiezas)
        print(array)

        mensaje_confirmacion = 'He recibido correctamente los datos.'
        conn.send(mensaje_confirmacion.encode())
        return array
    
    except struct.error as e:
        print('Error al desempaquetar los datos:', e)
    except ConnectionError:
        print('Error de conexión con el cliente.')
    except Exception as e:
        print('Error inesperado:', e)

def recibir_y_confirmar(conn):
    try:
        mensaje = conn.recv(1024).decode()
        if mensaje:
            print('Mensaje recibido:', mensaje)
            mensaje_confirmacion = 'He recibido el mensaje: ' + mensaje
            conn.send(mensaje_confirmacion.encode())
            return mensaje  # Retornar el mensaje recibido
    except ConnectionAbortedError:
        print('La conexión se ha cerrado desde el lado del cliente.')
    except ConnectionResetError:
        print('La conexión se ha restablecido desde el lado del cliente.')

def quien_empieza(conn):
    try:
        mensaje = conn.recv(1024).decode()
        if mensaje:
            print('Mensaje recibido:', mensaje)
            mensaje_confirmacion = 'He recibido el mensaje: ' + mensaje
            conn.send(mensaje_confirmacion.encode())
            return mensaje
    except ConnectionAbortedError:
        print('La conexión se ha cerrado desde el lado del cliente.')
    except ConnectionResetError:
        print('La conexión se ha restablecido desde el lado del cliente.')

def procesar_array_fichas(array_fichas):
    # Buscar el índice del separador 999
    indice_separador = array_fichas.index('999')

    # Dividir el array en fichas de juego y fichas disponibles
    fichas_juego_array = array_fichas[:indice_separador]
    fichas_disponibles_array = array_fichas[indice_separador + 1:]

    # Convertir los arrays en listas de fichas
    fichas_juego = [fichas_juego_array[i:i+5] for i in range(0, len(fichas_juego_array), 5)]
    fichas_disponibles = [fichas_disponibles_array[i:i+5] for i in range(0, len(fichas_disponibles_array), 5)]

    # Procesar fichas de juego
    print("Procesando fichas de juego:")
    agente.añadir_fichas_desde_arrays(fichas_juego, es_disponible=False)

    # Procesar fichas disponibles
    print("Procesando fichas disponibles:")
    agente.añadir_fichas_desde_arrays(fichas_disponibles, es_disponible=True)

    agente.actualizar_estado_juego()
    print("Se ha actualizado el estado")

def recibir_conjunto_fichas():
    print("\nIngresa los datos de la ficha separados por comas (valorA, valorB, coorX, coorY, orientacion):")
    datos_ficha = input()
    datos_ficha = [float(x.strip()) for x in datos_ficha.split(',')]  # Convierte la entrada a una lista de valores numéricos

    print("¿Son estas fichas del espacio de juego o fichas disponibles? (juego/disponibles):")
    tipo_fichas = input().strip().lower()  # Captura y normaliza la entrada del usuario

    if len(datos_ficha) == 5:
        if tipo_fichas == "juego" or tipo_fichas == "disponibles":
            es_disponible = True if tipo_fichas == "disponibles" else False
            # Creamos la ficha con los datos proporcionados
            nueva_ficha = Ficha(*datos_ficha)
            # Obtenemos las posiciones y la orientación de la pieza a coger y donde ponerla
            #coorX_actual, coorY_actual, orientacion_actual = nueva_ficha.coorX, nueva_ficha.coorY, nueva_ficha.orientacion
            #coorX_calculada, coorY_calculada, orientacion_calculada = nueva_ficha.calcular_nueva_posicion()
            # Añadimos la ficha al conjunto correspondiente
            agente.añadir_fichas_desde_arrays([datos_ficha], es_disponible=es_disponible)

            #print(f"POSICION RECOGIDA PIEZA: ({coorX_actual}, {coorY_actual}), Orientación: {math.degrees(orientacion_actual) % 360} grados")
            #print(f"POSICION DEJAR PIEZA: ({coorX_calculada}, {coorY_calculada}), Orientación: {math.degrees(orientacion_calculada) % 360} grados")
        else:
            print("Error: Tipo de fichas no reconocido. Se esperaba 'juego' o 'disponibles'.")
    else:
        print("Error: Los datos proporcionados no tienen el formato correcto.")

    # Actualizar visualización de fichas según el tipo
    print("\nFichas actualizadas:")
    if tipo_fichas == "juego":
        print("Fichas en el espacio de juego:")
        agente.ver_fichas(es_disponible=False)
    elif tipo_fichas == "disponibles":
        print("Fichas disponibles:")
        agente.ver_fichas(es_disponible=True)

    agente.actualizar_estado_juego()

def quitarcorchetes(lista):
    resultado = []
    for elemento in lista:
        if isinstance(elemento, list):  # Comprueba si el elemento es una lista
            resultado.extend(elemento)  # Extiende la lista resultado con los elementos de la sublista
        else:
            resultado.append(elemento)  # Añade el elemento no lista al resultado
    return resultado

global agente
agente = Agente()


Pos1=[ 0, 0, 0]
Pos2=[ 2, 0, 0]
Pos3=[ 4, 0, 0]
Pos4=[ 6, 0, 0]
Pos5=[ 8, 0, 0]
Pos6=[ 10, 0, 0]
Pos7=[ 12, 0, 0]
# YA ESTA DEFINIDO EN ROBOT 
Posicion_inicial=[Pos1, Pos2, Pos3, Pos4, Pos5, Pos6, Pos7]
####


while(partida):
    with condicion:
        print("\nEsperando instrucciones...\n")
        condicion.wait()
        fichas_juego_Vis=convertir_a_array(fichas_vis,num_piezas)
        agente.añadir_fichas_desde_arrays(fichas_juego_Vis, es_disponible=False) 
        #LOGICA DEL AGENTE PARA ELEGIR FICHA O ROBAR
        agente.actualizar_estado_juego()
        # Instruccion principal de desarrollo del turno
        if(instruccion == 1):
            print("Eligiendo ficha para colocar...\n")
            time.sleep(2.0)
            #KIKO HACE FOTO Y AGREGAMOS ARRAY A FICHAS JUEGO
            
            agente.añadir_fichas_desde_arrays(fichas_juego_Vis, es_disponible=False) 
            # LOGICA DEL AGENTE PARA ELEGIR FICHA O ROBAR
            agente.actualizar_estado_juego()# la parte en la que se elije la de robar se saca paponerla  AQUI
            ficha = True # LA FUNCION DE ANTES SACA RETURN LA ficha pickplace 
            if( ficha ):
                # MANDA AL ROBOT POSICION DE FICHA Y POSICION DE COLOCAR
                msg_ficha = comandoRobot(1,array_vacio,array_vacio)
                envRob.sendall(msg_ficha.serialize())
            else: 
                print("No se puede colocar ninguna ficha. El robot va a robar...\n")
                
                # Mover al robot a la zona de robo
                envVis.send('3'.encode())
                condicion.wait()
                envRob.send(msg_zona1.serialize())
                condicion.wait()

                # Confirma a vision que robot esta en zona robo
                envVis.send('-1'.encode())
                condicion.wait()

                # Recibe fichas en zona robo para elegir una
                if(instruccion == 8):
                    # No hay fichas disponibles y el robot pasa turno
                    envVis.send('-1'.encode())
                else:
                    # AQUI
                    #Elige ficha para robar y se la manda al robot 
                    envRob.sendall(msg_robar.serialize())

                    # Espera a que el robot robe una ficha
                    condicion.wait()
                    # Inicia secuencia para obtener foto de las fichas
                    envVis('4'.encode())

        if(instruccion == 3):
            print("Solicitando al robot que vaya a 'Zona Robo'...\n")
            envRob.send(msg_zona1.serialize())
            condicion.wait()
            print("\nEl robot esta en Zona Robo. Notificando a Vision...\n")
            time.sleep(1.0)
            envVis.send('-1'.encode())
            #ESTA ES LA PARTE PARA AGREGAR FICHAS DE ROBO UNA VEZ SE HACE LA IMAGEN
            fichas_robo=agente.añadir_fichas_robo_desde_array(fichas_vis) #HECHO 
            time.sleep(0.5)

        if(instruccion == 7):
            print("Solicitando al robot que robe 7 fichas...\n")
            print("Solicitando al robot que vaya a 'Zona CENTRO TABLERO'...\n")
            envRob.send(msg_zona3.serialize())
            condicion.wait()
            print("\nEl robot esta en Zona Tablero. Notificando a Vision...\n")
            time.sleep(1.0)
            envVis.send('-1'.encode())
            time.sleep(0.5)
            fichas_robo=agente.añadir_fichas_robo_desde_array(fichas_vis) #HECHO 

            for i in range(1,8):
                next_ficha_robo =agente.robo_set.pop(0)
                next_posX = Posicion_inicial[i][1]#No sé si esto es correcto
                next_posY = Posicion_inicial[i][2]
                next_orient = Posicion_inicial[i][3]
                array_coger=[0,0,next_ficha_robo.coorX, next_ficha_robo.coorY, next_ficha_robo.orientacion]
                array_dejar=[0,0, next_posX, next_posY, next_orient]
                msg_robar = comandoRobot(2,array_coger,array_dejar)
                envRob.sendall(msg_robar.serialize())
                condicion.wait()
                print("Fichas robadas: ", i, "\n")
                time.sleep(1.0)
            
            print("Fichas robadas. Notificando a la interfaz...")
            time.sleep(1.0)
            envVis.send('-1'.encode())#hecho creo
        
        # Mueve al robot a la zona de fichas para actualizar las fichas disponibles
        if(instruccion == 4):
            print("Solicitando al robot que vaya a 'Zona Fichas'...\n")
            envRob.send(msg_zona2.serialize())
            condicion.wait()
            print("\nEl robot esta en Zona Fichas. Notificando a Vision...\n")
            time.sleep(1.0)
            envVis.send('4'.encode())

            # ESPERA MENSAJE DE VISION CON LAS FICHAS
            condicion.wait()
            agente.añadir_fichas_desde_arrays(fichas_vis, es_disponible=True) #HECHO
            # ACTUALIZAR FICHAS DISPONIBLES
            envVis.send('-1'.encode())# hecho pero con duda 

        # Actualiza fichas disponibles y elige el doble mas alto entre las fichas disponibles
        if(instruccion == 6):
            agente.añadir_fichas_desde_arrays(fichas_vis, es_disponible=True) #HECHO
            print("Se va a devolver el doble más alto...\n")
            doble = agente.encontrar_ficha_de_mayor_valor(agente.fichas_disponibles)
            time.sleep(1.0)
            envVis.send(doble.encode())#hecho

        if(instruccion == 5):
            print("Solicitando al robot que vaya a 'Zona Tablero'...\n")
            envRob.send(msg_zona3.serialize())
            condicion.wait()
            print("\nEl robot esta en Zona Tablero. Notificando a Vision...\n")
            time.sleep(1.0)
            agente.añadir_fichas_robo_desde_array(fichas_vis)
            agente.actualizar_estado_juego()
            envVis.send('-1'.encode()) #hecho

thInt.join()
thVis.join()
thRob.join()