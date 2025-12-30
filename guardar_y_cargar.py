import json
from Clases import Habitacion, Servicio, Reserva
from pathlib import Path
from datetime import datetime


def cargar_datos():
    
    ruta = Path("Yeison.json")  #crear objeto Path
    with ruta.open() as archivo:  #abrir y leer el archivo
        datos = json.load(archivo) #guarda en datos el contenido del json
    
    lista_habitaciones=[]
    for hab in datos["habitaciones"]:

        nueva_habitacion = Habitacion(
            hab["id"],
            hab["tipo"],
            hab["vista_mar"],
            hab["piso"]
        )
        lista_habitaciones.append(nueva_habitacion)

    lista_servicios = []
    for serv in datos['servicios']:
        nuevo_serv = Servicio(
            serv["nombre"],
            serv["capacidad_total"]
        )
        lista_servicios.append(nuevo_serv)
    
    lista_reservas = []
    if "reservas" in datos:
        for res in datos["reservas"]:

            nueva_reserva = Reserva(
                res["cliente"],
                res["habitaciones"],
                res["servicios"],
                res["check_in"],
                res["check_out"]
            )
            lista_reservas.append(nueva_reserva)

    return lista_habitaciones, lista_servicios, lista_reservas
        

def guardar_datos(habitaciones, servicios, reservas):
    
    ruta=Path("Yeison.json")
    
    datos = {}

    lista_habitaciones_dict = []

    for habitacion in habitaciones:
    
        habitacion_dict = {
            "id": habitacion.id,
            "tipo": habitacion.tipo,
            "vista_mar": habitacion.vista_mar,
            "piso": habitacion.piso
        }
        lista_habitaciones_dict.append(habitacion_dict)
    
    datos["habitaciones"] = lista_habitaciones_dict
    
    print("Guardando servicios...")
    lista_servicios_dict = []  
    
    for servicio in servicios:
        
        servicio_dict = {
            "nombre": servicio.nombre,
            "capacidad_total": servicio.capacidad_total
        }
        
        lista_servicios_dict.append(servicio_dict)
    
    datos["servicios"] = lista_servicios_dict
    
    print("Guardando reservas...")
    lista_reservas_dict = []
    
    for reserva in reservas:
        reserva_dict = reserva.to_dict()
        
        lista_reservas_dict.append(reserva_dict)
    
    datos["reservas"] = lista_reservas_dict

    with ruta.open("w") as archivo:
        json.dump(datos, archivo, indent=2) # indent para que quede bonito (saltos de linea etc)\
        print("Todo perfe")