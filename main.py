from guardar_y_cargar import cargar_datos, guardar_datos
from datetime import timedelta, date
import os
from Funciones.fechas import obtener_fechas
from Funciones.disponibilidad import obtener_habitaciones_disponibles, verificar_disponibilidad_servicio
from Funciones.verificaciones import validar_seleccion_habitaciones, pedir_si_no_cancelar
from Clases import Reserva
from Funciones.disponibilidad import buscar_hueco_automatico

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def Menu():

    print("\nBLUE GATE HOTEL - Sistema de Reservas")
    
    print("1. Ver catálogo de habitaciones")
    print("2. Ver servicios del hotel")
    print("3. Ver reservas existentes")
    print("4. Crear nueva reserva")
    print("5. Cancelar reserva existente")
    print("6. Buscar hueco automático")
    print("7. Salir")

    return input("Selecciona una opción (1-7): ")

def ver_habitaciones(habitaciones):
    clear()
    print("Catálogo de Habitaciones")

    print("PISO 1:")
    count=0
    for hab in habitaciones:
        if hab.piso == 1:
            count +=1
            print(f"{count}: {hab}")
    
    print("PISO 2:")
    count=0
    for hab in habitaciones:
        if hab.piso == 2:
            count +=1
            print(f"{count}: {hab}")

def ver_servicios(servicios):
    clear()
    print("Servicios del Hotel")

    print(f"\n{'SERVICIO':<15} {'CAPACIDAD':<10}")
    for servicio in servicios:
        print(f"{servicio.nombre.capitalize():<15} "
              f"{servicio.capacidad_total:<10}")

def ver_reservas(reservas):
    clear()
    print("RESERVAS EXISTENTES")
    
    if len(reservas) == 0:
        print("No hay reservas registradas.")
        return
    
    for i in range(len(reservas)):
        reserva = reservas[i]
        print(f"[{i+1}] Cliente: {reserva.cliente}")
        print(f"Fechas: {reserva.check_in.strftime('%d-%m-%Y')} al {reserva.check_out.strftime('%d-%m-%Y')}")

        habitaciones_texto = ", ".join(reserva.habitaciones_ids)
        print(f"Habitaciones: {habitaciones_texto}") 

        if reserva.servicios_nombres:
            servicios_texto = ", ".join(reserva.servicios_nombres)
            print(f"Servicios: {servicios_texto}")
        else:
            print("Servicios: Ninguno")

def cancelar_reserva(reservas, servicios, habitaciones):
    clear()
    print("CANCELAR RESERVA")
    
    if not reservas:
        print("No hay reservas para cancelar.")
        return
    
    print("Reservas actuales:")
    for i in range(len(reservas)):
        reserva = reservas[i]
        habitaciones_texto = ", ".join(reserva.habitaciones_ids)
        print(f"[{i+1}] {reserva.cliente} - {habitaciones_texto} ({reserva.check_in.strftime('%d-%m-%Y')})")
    
    print()
    
    try:
        seleccion = input("Ingresa el número de la reserva a cancelar (o '0' para volver): ").strip()
            
        if seleccion == "0":
            print("Operación cancelada.")
            return
            
        numero = int(seleccion)
        if numero < 1 or numero > len(reservas):
            print(f"Por favor, ingresa un número entre 1 y {len(reservas)}.")
            return
            
    except ValueError:
        print("Por favor, ingresa un número válido.")
        return
    #la fijamos
    reserva_a_cancelar = reservas[numero - 1]
    
    clear()
    print("RESERVA SELECCIONADA:")
    print(f"Cliente: {reserva_a_cancelar.cliente}")
    print(f"Habitaciones: {', '.join(reserva_a_cancelar.habitaciones_ids)}")
    print(f"Fechas: {reserva_a_cancelar.check_in.strftime('%d-%m-%Y')} al {reserva_a_cancelar.check_out.strftime('%d-%m-%Y')}")
    
    if reserva_a_cancelar.servicios_nombres:
        print(f"Servicios: {', '.join(reserva_a_cancelar.servicios_nombres)}")
    else:
        print(f"Servicios: Ninguno")
    
    print()
    confirmar = pedir_si_no_cancelar("¿Estás seguro de cancelar esta reserva? (si/no): ").strip().lower()
    
    if confirmar == "si":

        reservas.pop(numero - 1)
        clear()
        print("Reserva cancelada exitosamente.")
        print("Las habitaciones y servicios han sido liberados.")
        guardar_datos(habitaciones, servicios, reservas)
    else:
        clear()
        print("Cancelación cancelada por el usuario.")

def main():

    print("BLUE GATE HOTEL - Sistema de Reservas")
    habitaciones, servicios, reservas = cargar_datos()

    while True:
        clear()
        opcion = Menu()

        if opcion == "1":
            clear()
            ver_habitaciones(habitaciones)
            input("\nPresiona Enter para volver al menú")
        
        elif opcion == "2":
            clear()
            ver_servicios(servicios)
            input("\nPresiona Enter para volver al menú")

        elif opcion == "3":
            clear()
            ver_reservas(reservas)
            input("\nPresiona Enter para volver al menú")

        elif opcion == "4":
            clear()
            crear_reserva(habitaciones, servicios, reservas)
        
        elif opcion == "5":
            clear()
            cancelar_reserva(reservas, servicios, habitaciones)
            input("\nPresiona Enter para volver al menú...")
        
        elif opcion == "6":
            clear()
            buscar_hueco_interfaz(habitaciones, servicios, reservas)

        elif opcion == "7":
            clear()
            print("Saliendo...")
            break
        
        else:
            print("Opción no válida. Inténtalo de nuevo.")
            input("\nPresiona Enter para volver al menú...")

def crear_reserva(habitaciones, servicios, reservas):
    clear()
    print("NUEVA RESERVA")
    print("Escribe 'cancelar' en cualquier momento para salir.")

    cliente = input("\nNombre del cliente: ").strip()
    if cliente.lower() == "cancelar":
        print("Reserva cancelada.")
        return
    if not cliente:
        print("Debes introducir un nombre para la reserva.")
        input("Presiona Enter para volver al menú...")
        return
    
    check_in, check_out = obtener_fechas()

    if check_in is None or check_out is None:
        print("Fechas canceladas.")
        input("Presiona Enter para volver al menú...")
        return

    habitaciones_disponibles = obtener_habitaciones_disponibles(check_in, check_out, habitaciones, reservas, servicios)

    if not habitaciones_disponibles:
        print("No hay habitaciones disponibles para esas fechas.")
        input("Presiona Enter para continuar...")
        return
    
    clear()
    print("HABITACIONES DISPONIBLES:")

    print("\nPISO 1:")
    for hab in habitaciones_disponibles:
        if hab.piso == 1:
            print(f"  {hab}")
    
    print("\nPISO 2:")
    for hab in habitaciones_disponibles:
        if hab.piso == 2:  
            print(f"  {hab}")

    suite_en_lista = False
    for hab in habitaciones_disponibles:
        if hab.id == "H204":
            suite_en_lista = True
            break

    if suite_en_lista:
        print("SUITE H204 DISPONIBLE (incluye desayuno obligatorio)")
    
    print("\n" + "="*50)
    print("SELECCIÓN DE HABITACIONES")
    print("="*50)
    print("Máximo 2 habitaciones, y deben estar en el mismo piso.")
    print("Ingresa los IDs separados por comas (ejemplo: H101,H104)")
    print("O escribe 'cancelar' para salir.")

    while True:
    
        ids_input = input(">> ").strip().upper()

        if ids_input.lower() == "cancelar":
            print("Reserva cancelada.")
            return
        
        partes = ids_input.split(',')
        habitaciones_ids_limpios = []
        for parte in partes:
            id_limpio = parte.strip()
            if id_limpio:  
                habitaciones_ids_limpios.append(id_limpio)

        valido, mensaje, habitaciones_validas =  validar_seleccion_habitaciones(habitaciones_ids_limpios, habitaciones, reservas, check_in, check_out, servicios)

        if not valido: #se parte y da el por que
            print(f"Error: {mensaje}")
            continue
        
        print(f"✓ {mensaje}") #retorna

        print("\nHabitaciones seleccionadas:")
        for hab in habitaciones_validas:
            print(f"  • {hab}")
        
        #confirmamos habs
        respuesta = pedir_si_no_cancelar("\n¿Confirmar estas habitaciones? (si/no): ").strip().lower()
        if respuesta == 'cancelar': 
            print("Reserva cancelada.")
            return
        if respuesta == 'si':
            habitaciones_seleccionadas = habitaciones_ids_limpios
            break
        else:
            print("Selección cancelada. Ingresa las habitaciones nuevamente.")
            continue

    clear()
    print("SERVICIOS DEL HOTEL")

    _, desayunos_disponibles = verificar_disponibilidad_servicio("desayuno", 0, servicios, reservas, check_in, check_out)
    _, masajes_disponibles = verificar_disponibilidad_servicio("masaje", 0, servicios, reservas, check_in, check_out)
    
    print("\nDisponibilidad durante tu estancia:")
    print(f"  • Desayuno: {desayunos_disponibles} disponible(s)")
    print(f"  • Masaje: {masajes_disponibles} disponible(s)")
    
    servicios_seleccionados = []
    
    #SUIT
    if "H204" in habitaciones_seleccionadas:
        total_habitaciones = len(habitaciones_seleccionadas)
        
        servicios_seleccionados.append("desayuno:1")
        print("✓ Desayuno AUTOMÁTICO incluido para la suite H204")

        if total_habitaciones == 2:

            if desayunos_disponibles >= 2:
                respuesta = pedir_si_no_cancelar("¿Añadir desayuno para la otra habitación? (si/no/cancelar): ")
                if respuesta == "cancelar":
                    print("Reserva cancelada.")
                    return
                elif respuesta == "si":
                    servicios_seleccionados = ["desayuno:2"]
                    print("✓ Desayuno añadido para ambas habitaciones")
                else:
                    print("Solo la suite tendrá desayuno.")
        else:
            print("Solo reservaste la suite.")
    #NO SUIT
    else:

        print("\n" + "="*40)
        print("SERVICIO DE DESAYUNOS")
        print("="*40)

        total_habitaciones = len(habitaciones_seleccionadas)

        if desayunos_disponibles <= 0:
            print("No hay desayunos disponibles en estas fechas.")
            
            respuesta = pedir_si_no_cancelar("¿Deseas continuar con la reserva sin desayuno? (si/no): ")
            
            if respuesta == "no" or respuesta =="cancelar":
                print("Reserva cancelada por el usuario.")
                return
            
            print("Continuando sin desayuno...")

        else:
            if total_habitaciones == 1:

                respuesta = pedir_si_no_cancelar("¿Incluir desayuno? (si/no/cancelar): ")
                if respuesta == "cancelar":
                    print("Reserva cancelada.")
                    return
                elif respuesta == "si":
                    disponible, _ = verificar_disponibilidad_servicio("desayuno", 1, servicios, reservas, check_in, check_out)
                    if disponible:
                        servicios_seleccionados.append("desayuno:1")
                        print("✓ Desayuno añadido: 1 servicio")
                    else:
                        print("No hay desayunos disponibles")

            else: #2 hab
                
                while True:
                    try:
                        print(f"\nDesayunos disponibles: {desayunos_disponibles}")
                        print("¿Cuántos desayunos deseas en tu reserva?")
                        cantidad = int(input("  Cantidad (0, 1 o 2): "))

                        if cantidad <0 or cantidad >2:
                            print("Debe ser 0, 1 o 2.")
                            continue
                        if cantidad == 0:
                            print("sin desayuno")
                            break
                        if cantidad > desayunos_disponibles:
                            print(f"Error: Solo hay {desayunos_disponibles} desayuno(s) disponible(s).")
                            continue

                        disponible, _ = verificar_disponibilidad_servicio("desayuno", cantidad, servicios, reservas, check_in, check_out)
                        
                        if cantidad == 1:
                            
                            if disponible:    
                                servicios_seleccionados.append("desayuno:1")
                                print("✓ Desayuno añadido: 1 servicio")
                                print("  (Solo 1 habitación tendrá desayuno)")
                                break
                            else:
                                print("No hay desayunos disponibles")
                        elif cantidad == 2:
                
                            if disponible: 
                                servicios_seleccionados.append("desayuno:2")
                                print("✓ Desayuno añadido: 2 servicios")
                                print("  (Ambas habitaciones tendrán desayuno)")
                                break
                            else:
                                print("No hay 2 desayunos disponibles")    
                    except ValueError:
                        print("Ingresa un número (0, 1 o 2).")
    
    clear()
    print("="*40)
    print("SERVICIO DE MASAJES")
    print("="*40)

    if masajes_disponibles <= 0:
        print("No hay masajes disponibles en estas fechas.")
        
        respuesta = pedir_si_no_cancelar("¿Deseas continuar con la reserva sin masaje? (si/no): ")
        
        if respuesta == "no" or respuesta == "cancelar":
            print("Reserva cancelada por el usuario.")
            return
        print("Continuando sin masaje...")
    
    else:
        total_habitaciones = len(habitaciones_seleccionadas)

        if total_habitaciones == 1:
            respuesta = pedir_si_no_cancelar("¿Incluir masaje? (si/no/cancelar): ")
            if respuesta == "cancelar":
                print("Reserva cancelada.")
                return
            elif respuesta == "si":
                disponible, _ = verificar_disponibilidad_servicio("masaje", 1, servicios, reservas, check_in, check_out)
                if disponible:
                    servicios_seleccionados.append("masaje:1")
                    print("✓ Masaje añadido: 1 servicio")
                else:
                    print("No hay masajes disponibles")

        else:  # 2 habitaciones
            while True:
                try:
                    print(f"\nMasajes disponibles: {masajes_disponibles}")
                    print("¿Cuántos masajes deseas en tu reserva?")
                    cantidad = int(input("  Cantidad (0, 1 o 2): "))

                    if cantidad < 0 or cantidad > 2:
                        print("Debe ser 0, 1 o 2.")
                        continue
                    if cantidad == 0:
                        print("sin masaje")
                        break
                    if cantidad > masajes_disponibles:
                        print(f"Error: Solo hay {masajes_disponibles} masaje(s) disponible(s).")
                        continue
                    
                    disponible, _ = verificar_disponibilidad_servicio("masaje", cantidad, servicios, reservas, check_in, check_out)

                    if cantidad == 1:
                        
                        if disponible:
                            servicios_seleccionados.append("masaje:1")
                            print("✓ Masaje añadido: 1 servicio")
                            print("  (Solo 1 habitación tendrá masaje)")
                            break
                        else:
                            print("No hay masajes disponibles")
                    elif cantidad == 2:
                        
                        if disponible:
                            servicios_seleccionados.append("masaje:2")
                            print("✓ Masaje añadido: 2 servicios")
                            print("  (Ambas habitaciones tendrán masaje)")
                            break
                        else:
                            print("No hay 2 masajes disponibles")
                except ValueError:
                    print("Ingresa un número (0, 1 o 2).")
    
    clear()
    print("=" * 50)
    print("RESUMEN DE RESERVA")
    print("=" * 50)
    print(f"Cliente: {cliente}")
    print(f"Fechas: {check_in.strftime('%d-%m-%Y')} al {check_out.strftime('%d-%m-%Y')}")
    print(f"Habitaciones: {', '.join(habitaciones_seleccionadas)}")
    
    if servicios_seleccionados:
        servicios_texto = ', '.join(servicios_seleccionados)
        print(f"Servicios: {servicios_texto}")
    else:
        print("Servicios: Ninguno")
    
    respuesta = pedir_si_no_cancelar("\n¿Confirmar la reserva? (si/no/cancelar): ")
    if respuesta == "cancelar":
        print("Reserva cancelada.")
        return
    elif respuesta == "si":
    
        nueva_reserva = Reserva(
            cliente=cliente,
            habitaciones_ids=habitaciones_seleccionadas,
            servicios_nombres=servicios_seleccionados,
            check_in=check_in,
            check_out=check_out
        )
        reservas.append(nueva_reserva)
        clear()
        print("\n¡RESERVA CREADA EXITOSAMENTE!")
        
        guardar_datos(habitaciones, servicios, reservas)
        
        print("\nDetalles de la reserva:")
        print(f"  • Cliente: {cliente}")
        print(f"  • Fechas: {check_in.strftime('%d-%m-%Y')} a {check_out.strftime('%d-%m-%Y')}")
        print(f"  • Habitaciones: {', '.join(habitaciones_seleccionadas)}")
        if servicios_seleccionados:
            servicios_texto = ', '.join(servicios_seleccionados)
            print(f"  • Servicios: {servicios_texto}")
        else:
            print("  • Servicios: Ninguno")
    else:
        print("\nReserva cancelada por el usuario.")
    
    input("\nPresiona Enter para volver al menú...")

def buscar_hueco_interfaz(habitaciones, servicios, reservas):
    clear()
    print("BUSCAR HUECO AUTOMÁTICO")
    print("Escribe 'cancelar' en cualquier momento para salir.")
    
    print("\nIngresa los IDs de habitaciones separados por coma (ejemplo: H101,H104)")
    ids_input = input(">> ").strip().upper()
    if ids_input.lower() == "cancelar":
        return
    
    partes = ids_input.split(',')
    habitaciones_ids = []
    for parte in partes:
        id_limpio = parte.strip()
        if id_limpio:
            habitaciones_ids.append(id_limpio)

    valido, mensaje, habitaciones_validas = validar_seleccion_habitaciones(habitaciones_ids, habitaciones, reservas, date.today(), date.today() + timedelta(days=1), servicios)
    
    if not valido:
        print("Error:", mensaje)
        input("\nPresiona Enter para continuar...")
        return
    
    clear()
    print("CONFIGURACIÓN DE DESAYUNOS")

    tiene_suite = "H204" in habitaciones_ids

    if len(habitaciones_ids) == 1:
        if tiene_suite:
            
            desayunos = 1
            print("La suite H204 incluye 1 desayuno obligatorio.")
        else:
            respuesta = pedir_si_no_cancelar("¿Incluir desayuno? (si/no/cancelar): ")
            if respuesta == "cancelar":
                return
            elif respuesta == "si":
                desayunos = 1
            else:
                desayunos = 0

    else:  # 2 habitaciones
        if tiene_suite:
            print("La suite H204 incluye 1 desayuno obligatorio.")
            respuesta = pedir_si_no_cancelar("¿Añadir desayuno para la otra habitación? (si/no/cancelar): ")
            if respuesta == "cancelar":
                return
            elif respuesta == "si":
                desayunos = 2
            else:
                desayunos = 1
        else:
            while True:
                try:
                    cantidad_input = input("Cantidad de desayunos (0, 1 o 2): ").strip()
                    if cantidad_input.lower() == "cancelar":
                        return
                    cantidad = int(cantidad_input)
                    if cantidad < 0 or cantidad > 2:
                        print("Debe ser 0, 1 o 2.")
                        continue
                    if cantidad > len(habitaciones_ids):
                        print(f"No puedes pedir {cantidad} desayunos para {len(habitaciones_ids)} habitación(es).")
                        continue
                    desayunos = cantidad
                    break
                except ValueError:
                    print("Ingresa un número (0, 1 o 2).")

    clear()
    print("CONFIGURACIÓN DE MASAJES")

    if len(habitaciones_ids) == 1:
        respuesta = pedir_si_no_cancelar("¿Incluir masaje? (si/no/cancelar): ")
        if respuesta == "cancelar":
            return
        elif respuesta == "si":
            masajes = 1
        else:
            masajes = 0
    else:  # 2 habitaciones
        while True:
            try:
                cantidad_input = input("Cantidad de masajes (0, 1 o 2): ").strip()
                if cantidad_input.lower() == "cancelar":
                    return
                cantidad = int(cantidad_input)
                if cantidad < 0 or cantidad > 2:
                    print("Debe ser 0, 1 o 2.")
                    continue
                if cantidad > len(habitaciones_ids):
                    print(f"No puedes pedir {cantidad} masajes para {len(habitaciones_ids)} habitación(es).")
                    continue
                masajes = cantidad
                break
            except ValueError:
                print("Ingresa un número (0, 1 o 2).")

    # Construir lista de servicios
    servicios_seleccionados = []
    if desayunos > 0:
        servicios_seleccionados.append(f"desayuno:{desayunos}")
    if masajes > 0:
        servicios_seleccionados.append(f"masaje:{masajes}")
    
    clear()
    print("DURACIÓN DE LA ESTANCIA")
    noches_input = input("¿Cuántas noches deseas reservar? ").strip()
    if noches_input.lower() == "cancelar":
        return
    
    try:
        noches = int(noches_input)
        if noches < 1:
            print("Debe ser al menos 1 noche.")
            input("Presiona Enter para continuar...")
            return
    except ValueError:
        print("Debe ser un número.")
        input("Presiona Enter para continuar...")
        return
    
    print(f"\nBuscando disponibilidad para {noches} noches...")
    
    inicio, fin = buscar_hueco_automatico(habitaciones_ids, servicios_seleccionados, noches, habitaciones, servicios, reservas)
    
    clear()
    if inicio is None:
        print("No se encontró disponibilidad en los próximos 2 años.")
    else:
        print("\n" + "="*40)
        print("DISPONIBILIDAD ENCONTRADA")
        print("="*40)
        print(f"  Check-in:  {inicio.strftime('%d-%m-%Y')}")
        print(f"  Check-out: {fin.strftime('%d-%m-%Y')}")
        print(f"  Noches:    {noches}")
        print(f"  Habitaciones: {', '.join(habitaciones_ids)}")
        if servicios_seleccionados:
            print(f"  Servicios: {', '.join(servicios_seleccionados)}")
    
        respuesta = pedir_si_no_cancelar("\n¿Deseas crear una reserva con estas fechas? (si/no/cancelar): ")
        
        if respuesta == "cancelar":
            print("Operación cancelada.")
        elif respuesta == "si":
            clear()
            while True:
                cliente = input("Nombre del cliente para la reserva: ").strip()
                if cliente.lower() == "cancelar":
                    print("Reserva cancelada.")
                    break
                
                if not cliente:
                    print("El nombre del cliente no puede estar vacío.")
                    continue
                
                nueva_reserva = Reserva(cliente=cliente, habitaciones_ids=habitaciones_ids, servicios_nombres=servicios_seleccionados, check_in=inicio, check_out=fin)
                
                reservas.append(nueva_reserva)
                guardar_datos(habitaciones, servicios, reservas)
                
                clear()
                print("\n¡RESERVA CREADA EXITOSAMENTE!")
                print("Detalles de la reserva:")
                print(f"  • Cliente: {cliente}")
                print(f"  • Fechas: {inicio.strftime('%d-%m-%Y')} a {fin.strftime('%d-%m-%Y')}")
                print(f"  • Habitaciones: {', '.join(habitaciones_ids)}")
                if servicios_seleccionados:
                    servicios_texto = ', '.join(servicios_seleccionados)
                    print(f"  • Servicios: {servicios_texto}")
                break
    
    input("\nPresiona Enter para volver al menú...")


if True:
    main()