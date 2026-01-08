from datetime import datetime, date

def obtener_habitaciones_disponibles(check_in, check_out, habitaciones, reservas):

    hab_disponibles = []
    for hab in habitaciones:
        ocupada = False

        for reserva in reservas:
            if hab.id in reserva.habitaciones_ids:
                if not(check_out <= reserva.check_in or check_in >= reserva.check_out):

                    ocupada = True
                    break
        if not ocupada:
            hab_disponibles.append(hab)
    return hab_disponibles

def verificar_disponibilidad_servicio(nombre_servicio, cantidad_necesaria, servicios):

    for servicio in servicios:
        if servicio.nombre == nombre_servicio:
            disponible = servicio.capacidad_total - servicio.ocupado_actual
            return disponible >= cantidad_necesaria
    return False

