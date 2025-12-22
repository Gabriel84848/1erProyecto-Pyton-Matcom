import json
from Clases import Habitacion, Servicio
from pathlib import Path


def cargar_Habitaciones():
    
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
        

def guardar_reservas(lista_reservas):
    
    ruta=Path("Yeison.json")

    with ruta.open() as archivo:
        datos = json.load(archivo)

    reservas_a_dicts = []
    for reserva in lista_reservas:
        reservas_a_dicts.append(reserva.to_dict())

    datos["reservas"] = reservas_a_dicts #remplazamos el val de la key reservas

    with ruta.open("w") as archivo:
        json.dump(datos, archivo, indent=2) # indent para que quede bonito (saltos de linea etc)