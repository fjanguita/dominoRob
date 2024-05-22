import struct
import numpy as np

class comandoVision:
    def __init__(self, comando, Npiezas, array=None):
        self.comando = comando
        self.Npiezas = Npiezas
        # Si no se proporciona un array, inicializar con arrays de 5 dimensiones llenos de ceros
        self.array = array if array is not None else np.zeros((Npiezas, 5), dtype=float)

    def serialize(self):
        # El formato de la estructura es un tipoComando seguido de un entero Npiezas y luego 5 floats por cada pieza
        formato = "ii" + "f" * (5 * self.Npiezas)
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