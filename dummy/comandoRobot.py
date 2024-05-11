import struct

class comandoRobot:
    def __init__(self, comando, pick, place):
        self.tipoComando = comando
        self.posePick = pick
        self.posePlace = place

    def serialize(self):
        # El formato de la estructura es un tipoComando seguido de 6 floats y luego otros 6 floats
        formato = "i" + "f" * 6 + "f" * 6
        # Empaqueta los datos en formato binario
        return struct.pack(formato, self.tipoComando, *self.posePick, *self.posePlace)

    @classmethod
    def deserialize(cls, data):
        # Desempaqueta los datos binarios
        formato = "i" + "f" * 6 + "f" * 6
        decimal_places = 3
        unpacked_data = struct.unpack(formato, data)
        tipoComando = unpacked_data[0]
        posePick = [round(num, decimal_places) for num in unpacked_data[1:7]]
        posePlace = [round(num, decimal_places) for num in unpacked_data[7:]]
        return cls(tipoComando, posePick, posePlace)