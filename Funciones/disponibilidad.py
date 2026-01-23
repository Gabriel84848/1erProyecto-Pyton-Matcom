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

def verificar_disponibilidad_servicio(nombre_servicio, cantidad_necesaria, servicios, reservas, check_in, check_out):
    
    servicio_obj = None
    for servicio in servicios:
        if servicio.nombre == nombre_servicio:
            servicio_obj = servicio
            break
    
    if not servicio_obj:
        return False, 0
    
    ocupados_en_intervalo = 0
    for reserva in reservas:
        
        if reserva.check_in < check_out and reserva.check_out > check_in: #se superponen
            
            for servicio_str in reserva.servicios_nombres:
                if nombre_servicio in servicio_str:
                    
                    partes = servicio_str.split(':')
                    ocupados_en_intervalo += int(partes[1])
    
    disponible_en_intervalo = servicio_obj.capacidad_total - ocupados_en_intervalo
    return disponible_en_intervalo>=cantidad_necesaria, disponible_en_intervalo

