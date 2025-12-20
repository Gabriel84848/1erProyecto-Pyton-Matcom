
class Habitacion:

    def __init__ (self, id_habitacion, tipo, vista_mar, piso):
        
        self.id = id_habitacion
        self.tipo = tipo
        self.vista_mar = vista_mar
        self.piso = piso

    def __str__ (self):

        if self.vista_mar:
            return f"{self.id} ({self.tipo}) - Piso {self.piso} - Vista al mar"
        else:
            return f"{self.id} ({self.tipo}) - Piso {self.piso} - Sin vista al mar"