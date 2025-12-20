import json
from Clases import Habitacion
from pathlib import Path


def cargar_Habitaciones():
    
    ruta = Path("Yeison.json")  #crear objeto Path
    with ruta.open() as archivo:  #abrir y leer el archivo
        datos = json.load(archivo)
    
    lista_habitaciones=[]

    for hab in datos["habitaciones"]:

        nueva_habitacion = Habitacion(
            hab["id"],
            hab["tipo"],
            hab["vista_mar"],
            hab["piso"]
        )
        lista_habitaciones.append(nueva_habitacion)
    return lista_habitaciones