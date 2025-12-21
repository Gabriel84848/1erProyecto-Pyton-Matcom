
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
        
class Servicio:

    def __init__ (self, nombre, capacidad_total):

        self.nombre = nombre
        self.capacidad_total = capacidad_total
        self.ocupado_actual = 0
    
    def __str__(self):
        return f"{}"