from Funciones.disponibilidad import obtener_habitaciones_disponibles
    
def validar_seleccion_habitaciones(habitaciones_ids, habitaciones, reservas, check_in, check_out, servicios=None):
   
    if len(habitaciones_ids) > 2:
        return False, "Maximo 2 habitaciones por reserva", []
    
    if len(habitaciones_ids) == 0:
        return False, "Debe seleccionar al menos una habitacion", []
    
    disponibles = obtener_habitaciones_disponibles(check_in, check_out, habitaciones, reservas, servicios)

    habitaciones_validas = []
    
    #Verificar que existe
    for id_hab in habitaciones_ids:
        existe = None
        for hab in habitaciones:
            if hab.id == id_hab:
                existe = hab
                break
        
        if existe is None:
            return False, f"Habitacion '{id_hab}' no existe", []
        
        #Que esta disponible
        disponible = None
        for hab in disponibles:
            if hab.id == id_hab:
                disponible = hab
                break
        
        if disponible is None:
            if id_hab == "H204" and servicios:
                tiene_desayuno, _ = verificar_disponibilidad_servicio("desayuno", 1, servicios, reservas, check_in, check_out)
                
                if not tiene_desayuno:
                    return False, f"Suite H204 no disponible: No hay desayunos en esas fechas", []
            
            return False, f"Habitacion '{id_hab}' no disponible en esas fechas", []
        
        habitaciones_validas.append(disponible)
        
    #Validar mismo piso
    if len(habitaciones_validas) == 2:
        if habitaciones_validas[0].piso != habitaciones_validas[1].piso:
            return False, "Las habitaciones estan en pisos diferentes", []
    
    return True, "Habitaciones validas", habitaciones_validas