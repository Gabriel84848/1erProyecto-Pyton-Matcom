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

    def __init__ (self, nombre, capacidad_total):

        self.nombre = nombre
        self.capacidad_total = capacidad_total
    
    def __str__(self):
        return f"{self.nombre}: capacidad {self.capacidad_total}"
    
class Reserva:

    def __init__(self, cliente, habitaciones_ids, servicios_nombres, check_in, check_out):
        self.cliente = cliente
        self.habitaciones_ids = habitaciones_ids 
        self.servicios_nombres = servicios_nombres 

        if isinstance(check_in, str):  #convierte a date
            temp = datetime.fromisoformat(check_in)
            self.check_in = temp.date() 
        elif isinstance(check_in, datetime):
            self.check_in = check_in.date()  
        else:
            self.check_in = check_in 
            
        if isinstance(check_out, str):
            temp = datetime.fromisoformat(check_out)
            self.check_out = temp.date()  
        elif isinstance(check_out, datetime):
            self.check_out = check_out.date()  
        else:
            self.check_out = check_out         

    def to_dict(self):
        return {
            "cliente": self.cliente,
            "habitaciones": self.habitaciones_ids,
            "servicios": self.servicios_nombres,
            "check_in": str(self.check_in),
            "check_out": str(self.check_out)}