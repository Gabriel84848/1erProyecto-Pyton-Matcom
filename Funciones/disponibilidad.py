from datetime import date, timedelta

def obtener_habitaciones_disponibles(check_in, check_out, habitaciones, reservas, servicios = None):

    hab_disponibles = []
    for hab in habitaciones:
        ocupada = False

        for reserva in reservas:
            if hab.id in reserva.habitaciones_ids:
                if not(check_out <= reserva.check_in or check_in >= reserva.check_out):

                    ocupada = True
                    break
        
        if ocupada:
            continue
        
        if hab.id == "H204" and servicios:
    
            disponible, _ = verificar_disponibilidad_servicio("desayuno", 1, servicios, reservas, check_in, check_out)
            if not disponible:
    
                continue
        
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

def buscar_hueco_automatico(habitaciones_ids, servicios_seleccionados, noches, habitaciones, servicios, reservas):

    hoy = date.today()
    limite = hoy.replace(year=hoy.year + 2)
    
    inicio = hoy
    while inicio <= limite:
        fin = inicio + timedelta(days=noches)
        if fin > limite:
            break
        
        habitaciones_disponibles = obtener_habitaciones_disponibles(inicio, fin, habitaciones, reservas, servicios)
        
        todas_disponibles = True
        for id_hab in habitaciones_ids:
            disponible = False
            for hab in habitaciones_disponibles:
                if hab.id == id_hab:
                    disponible = True
                    break
            if not disponible:
                todas_disponibles = False
                break

        if todas_disponibles:
    
            servicios_ok = True
            for servicio_str in servicios_seleccionados:
                nombre, cantidad_str = servicio_str.split(':')
                cantidad = int(cantidad_str)
                
                disponible, _ = verificar_disponibilidad_servicio(nombre, cantidad, servicios, reservas, inicio, fin)
                
                if not disponible:
                    servicios_ok = False
                    break
        
            if servicios_ok:
                return inicio, fin
    
        inicio += timedelta(days=1)

    return None, None