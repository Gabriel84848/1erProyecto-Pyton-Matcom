from datetime import datetime

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

    def __init__ (self, nombre, capacidad_total, ocupado_actual = 0):

        self.nombre = nombre
        self.capacidad_total = capacidad_total
        self.ocupado_actual = ocupado_actual
    
    def __str__(self):
        return f"{self.nombre}: {self.ocupado_actual} de {self.capacidad_total} ocupados"
    
    def disponibilidad(self, cantidad_necesaria=1):
        return (self.ocupado_actual + cantidad_necesaria) <= self.capacidad_total 
    
    def ocupar(self, cantidad=1):
        
        if self.disponibilidad(cantidad):
            self.ocupado_actual += cantidad
            return True
        return False
    
    def liberar(self, cantidad = 1):

        if self.ocupado_actual >= cantidad:
            self.ocupado_actual -= cantidad
        else:
            self.ocupado_actual = 0

class Reserva:

    def __init__(self, cliente, habitaciones_ids, servicios_nombres, check_in, check_out):
        self.cliente = cliente
        self.habitaciones_ids = habitaciones_ids 
        self.servicios_nombres = servicios_nombres 

        if isinstance(check_in, str):    #convierte a dtaetime
            self.check_in = datetime.fromisoformat(check_in) 
        else:
            self.check_in = check_in
            
        if isinstance(check_out, str):
            self.check_out = datetime.fromisoformat(check_out)
        else:
            self.check_out = check_out        

    def to_dict(self):
        return {
            "cliente": self.cliente,
            "habitaciones": self.habitaciones_ids,
            "servicios": self.servicios_nombres,
            "check_in": str(self.check_in),
            "check_out": str(self.check_out)}