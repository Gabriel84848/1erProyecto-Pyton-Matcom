from guardar_y_cargar import cargar_datos, guardar_datos
from datetime import datetime, date
import os
from Funciones.fechas import obtener_fechas
from Funciones.disponibilidad import obtener_habitaciones_disponibles, verificar_disponibilidad_servicio
from Funciones.verificaciones import validar_seleccion_habitaciones
from Clases import Reserva

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def Menu():

    print("\nBLUE GATE HOTEL - Reservas")
    
    print("1. habitaciones disponibles")
    print("2. ver Servicios del hotel ")
    print("3. ver Reservas existentes")
    print("4. Crear nueva reserva ")
    print("5. Cancelar reserva existente")
    print("6. Guardar cambios")
    print("7. Salir")
    print("8. Test")

    return input("selecciona una opcion (1 - 7): ")

def ver_habitaciones(habitaciones):

    print("Habitaciones disponibles")

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
    print("Servicios del hotel")

    print("Disponibilidad:")
    print(f"\n{"SERVICIO":<15} {"TOTAL":<10} {"DISPONIBLE":<12} {"OCUPADOS":<10}")

    for servicio in servicios:
        disponibles = servicio.capacidad_total - servicio.ocupado_actual

        print(f"{servicio.nombre.capitalize():<15} "
              f"{servicio.capacidad_total:<10} "
              f"{disponibles:<12} "
              f"{servicio.ocupado_actual:<10}")


def main():

    print("BLUE GATE HOTEL - Reservas")
    habitaciones, servicios, reservas = cargar_datos()

    while True:
        clear()
        opcion = Menu()

        if opcion == "1":
            clear()
            ver_habitaciones(habitaciones)
            input("\nPresiona Enter para volver al menu")

        elif opcion == "2":
            clear()
            ver_servicios(servicios)
            input("\nPresiona Enter para volver al menu")
        
        elif opcion == "4":
            clear()
            crear_reserva(habitaciones, servicios, reservas)
        
        elif opcion == "6":
            clear()
            guardar_datos(habitaciones, servicios, reservas)
            print("Datos guardados exitosamente!")
            input("\nPresiona Enter para volver al menu")

        elif opcion == "7":
            clear()
            print("Saliste")
            break
        
        elif opcion =="8":
            clear()
            print("Probando fechas")
            check_in, check_out = obtener_fechas()
            print(f"   Check-in: {check_in}")
            print(f"   Check-out: {check_out}")
            input("Presiona Enter para volver al menú")
        else:
            print("NO")
            input("\nPresiona Enter para volver al menu")

def crear_reserva(habitaciones, servicios, reservas):
    print("NUEVA RESERVA")

    cliente = input("\n Nombre del cliente:").strip()
    if not cliente:
        print("Tienes que introducir tu nombre")
        input("Presiona Enter para volver al menú...")
        return
    
    print("Fechas de la reserva")
    check_in, check_out = obtener_fechas()

    if check_in is None or check_out is None:
        print("Fechas canceladas")
        input("Presiona Enter para volver al menú...")
        return

    habitaciones_disponibles = obtener_habitaciones_disponibles(check_in, check_out, habitaciones, reservas)

    if not habitaciones_disponibles:
        print("No hay habitaciones disponibles para esas fechas")
        input("Enter para continuar...")
        return

    #chequear disponibilidad suite
    suite_h204 = None
    for hab in habitaciones_disponibles:
        if hab.id == "H204":
            if verificar_disponibilidad_servicio("desayuno", 1, servicios):
                suite_h204 = hab
            break
    
    print("HABITACIONES DISPONIBLES:")

    print("\nPISO 1:")
    for hab in habitaciones_disponibles:
        if hab.piso == 1 and hab.id != "H204":  
            print(f"  {hab}")
    
    print("\nPISO 2:")
    for hab in habitaciones_disponibles:
        if hab.piso == 2 and hab.id != "H204":  
            print(f"  {hab}")

    if suite_h204:
        print("SUITE DISPONIBLE (incluye desayuno automatico):")
        print(f"{suite_h204}")
    
    print("SELECCION DE HABITACIONES")
    print("Maximo 2 y deben estar en el mismo piso")

    while True:
        print("Ingresa Ids separados por coma (ej: H101,H104 )")
        ids_input = input(">> ").strip().upper()
        
        partes = ids_input.split(',')
        habitaciones_ids_limpios = []
        for parte in partes:
            id_limpio = parte.strip()
            if id_limpio:  
                habitaciones_ids_limpios.append(id_limpio)

        valido, mensaje, habitaciones_validas =  validar_seleccion_habitaciones(habitaciones_ids_limpios, habitaciones, reservas, check_in, check_out)

        if not valido: #se parte y da el por que
            print(f"{mensaje}")
            continue
        print(f"{mensaje}") #retorna

        print("Habitaciones seleccionadas:")
        for hab in habitaciones_validas:
            print(f">> {hab}")
        
        #confirmamos habs
        confirmar = input("\n¿Confirmar estas habitaciones? (si/no): ").strip().lower()
        if confirmar == 'si':
            habitaciones_seleccionadas = habitaciones_ids_limpios
            break
        else:
            print("Seleccion cancelada, ingresa las habitaciones nuevamente")
            continue

    print("Servicios del hotel")
    
    print("Disponibilidad actual:")
    for servicio in servicios:
        disponible = servicio.capacidad_total - servicio.ocupado_actual
        print(f"  {servicio.nombre.capitalize()}: {disponible} disponibles")

    servicios_seleccionados = []
    
    #SUIT
    if "H204" in habitaciones_seleccionadas:
        total_habitaciones = len(habitaciones_seleccionadas)
        
        servicios_seleccionados.append("desayuno:1")
        print(f"Desayuno AUTOMATICO incluido para la suite H204")

        if total_habitaciones == 2:

            if verificar_disponibilidad_servicio("desayuno", 1, servicios):
                
                if input("Anadir desayuno para la otra habitación? (s/n): ").strip().lower() == "s":
                
                    servicios_seleccionados = ["desayuno:2"]
                    print("Desayuno añadido para ambas habitaciones")
                else:
                    print("Solo la suite tendra desayuno")
            else:
                print("No hay desayunos disponibles para la otra habitacion")
                print("Solo la suite tendra desayuno")
        else:
            print("Solo reservaste la suite")
    #NO SUIT
    else:

        print("Servicio de desayunos")

        total_habitaciones = len(habitaciones_seleccionadas)
        
        if total_habitaciones == 1:

            if input("Incluir desayuno? (si/no): ").strip().lower() == "si":
                
                if verificar_disponibilidad_servicio("desayuno", 1, servicios):
                    servicios_seleccionados.append("desayuno:1")
                    print("Desayuno anadido: 1 servicio")
                else:
                    print("No hay desayunos disponibles")
            else:
                print("Sin desayuno")

        else: #2 hab
            
            while True:
                try:
                    print("Cuantos desayunos deseas en tu reserva?")
                    cantidad = int(input(" Cantidad (0, 1 o 2): "))

                    if cantidad <0 or cantidad >2:
                        print("Debe ser 0, 1 o 2")
                        continue
                    if cantidad == 0:
                        print("sin desayuno")
                        break
                    if cantidad == 1:
                        if verificar_disponibilidad_servicio("desayuno", cantidad, servicios):
                            
                            servicios_seleccionados.append("desayuno:1")
                            print("Desayuno anadido: 1 servicio")
                            print("Solo 1 habitacion tendra desayuno")
                            break
                        else:
                            print("No hay desayunos disponibles")
                    elif cantidad == 2:
                        if verificar_disponibilidad_servicio("desayuno", cantidad, servicios):
                            
                            servicios_seleccionados.append("desayuno:2")
                            print("Desayuno anadido: 2 servicio")
                            print("Las 2 habitaciones tendran desayuno")
                            break
                        else:
                            print("No hay 2 desayunos disponibles")    
                except ValueError:
                    print("Ingresa un numero (0, 1 o 2)")
                    
        print("Servicio de masajes")

        if input(" Incluir masaje? (si/no):").strip().lower() == "si":
            while True:
                try:
                    cantidad = int(input("   Cantidad (1 o 2): "))
                
                    if cantidad not in [1, 2]:
                        print("Debe ser 1 o 2")
                        continue
                    
                    if verificar_disponibilidad_servicio("masaje", cantidad, servicios):
                        servicios_seleccionados.append(f"masaje:{cantidad}")
                        print(f"Masaje anadido: {cantidad} servicio(s)")
                        break
                    
                    else:
                        print("No hay esa cantidad de servicios de masaje disponibles")
                except ValueError:
                    print("Ingresa un numero (1 o 2)")
        else:
            print("Sin servicio de masaje")
    
    print("RESUMEN DE RESERVA")
    print(f"Cliente: {cliente}")
    print(f"Fechas: {check_in.strftime('%d-%m-%Y')} al {check_out.strftime('%d-%m-%Y')}")
    print(f"Habitaciones: {', '.join(habitaciones_seleccionadas)}")
    if servicios_seleccionados:
        servicios_texto = ', '.join(servicios_seleccionados)
        print("Servicios: " + servicios_texto)
    else:
        print("Servicios: Ninguno")
    
    confirmar_reserva = input("\n¿Confirmar la reserva? (si/no): ").strip().lower()
    if confirmar_reserva == 'si':
        
        for servicio_str in servicios_seleccionados:
            nombre, cantidad_str = servicio_str.split(':')
            cantidad_int = int(cantidad_str)
            
            for servicio in servicios:
                if servicio.nombre == nombre:
                    if servicio.ocupar(cantidad_int): #para aprovechar la func disponibilidad
                        print(f"{nombre.capitalize()}: {cantidad_int} unidad(es) ocupada(s)")
                    else:
                        print(f"Error al ocupar {nombre}") 
        
        nueva_reserva = Reserva(
            cliente=cliente,
            habitaciones_ids=habitaciones_seleccionadas,
            servicios_nombres=servicios_seleccionados,
            check_in=check_in,
            check_out=check_out
        )
        reservas.append(nueva_reserva)
        print("\nRESERVA CREADA EXITOSAMENTE!")
        
        print("\nDetalles de la reserva:")
        print(f"  • Cliente: {cliente}")
        print(f"  • Fechas: {check_in.strftime('%d-%m-%Y')} a {check_out.strftime('%d-%m-%Y')}")
        print(f"  • Habitaciones: {', '.join(habitaciones_seleccionadas)}")
        if servicios_seleccionados:
            servicios_texto = ', '.join(servicios_seleccionados)
            print(f"Servicios: {servicios_texto}")
        else:
            print("Servicios: Ninguno")
    else:
        print("\nReserva cancelada por el usuario")
    
    input("\nPresiona Enter para volver al menu...")
    
            

if True:
    main()


