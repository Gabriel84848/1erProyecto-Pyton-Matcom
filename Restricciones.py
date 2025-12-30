def verificar_mismo_piso(habitaciones_ids, todas_habitaciones):

    if range(len(habitaciones_ids)) == 0:
        return True
    
    for hab in todas_habitaciones:
        