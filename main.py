from guardar_y_cargar import cargar_datos, guardar_datos
from datetime import datetime, date
import os

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
    
    #implementar
    habitaciones_disponibles = obtener_habitaciones_disponibles(check_in, check_out, habitaciones, reservas)

    if not habitaciones_disponibles:
        print("No hay habitaciones disponibles para esas fechas")
        input("Enter para continuar...")
        return
    
    #implementar
    suite_h204 = None
    for hab in habitaciones_disponibles:
        
        if hab.id == "H204":
            
            if verificar_disponibilidad_servicio("desayuno", 1, servicios):
                suite_h204 = hab
            break
    
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
    
    print("Seleccion de habitaciones")
    print("Maximo 2 y deben estar en el mismo piso")

    habitaciones_seleccionadas = []

    while True:
        print("Ingresa Ids separados por coma (ej: H101,H104 )")
        ids_input = input(">> ").strip().upper()
        
        partes = ids_input.split(',')
        
        habitaciones_ids_limpios = []

        for parte in partes:
            id_limpio = parte.strip()
            if id_limpio:  
                habitaciones_ids_limpios.append(id_limpio)

        if len(habitaciones_ids_limpios) == 0:
            print("Debes ingresar al menos 1 habitacion")
            continue 

        if len(habitaciones_ids_limpios) > 2:
            print("Maximo 2 habitaciones por reserva") 
            continue
        
        #implementar
        if not validar_mismo_piso(habitaciones_ids_limpios, habitaciones):
            print("Todas las habitaciones deben estar en el mismo piso")
            continue

        habitaciones_seleccionadas = habitaciones_ids_limpios
        break

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
                    
            #implementar
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

            if input("Incluir desayuno? (s/n): ").strip().lower() == "s":
                
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
                
                    if cantidad == 1:
                    
                        if verificar_disponibilidad_servicio("masaje", 1, servicios):
                            servicios_seleccionados.append("masaje:1")
                            print("Masaje anadido: 1 servicio")
                            break
                        else:
                            print("No hay servicio de masaje disponible")
                
                    elif cantidad == 2:
                    
                        if verificar_disponibilidad_servicio("masaje", 2, servicios):
                            servicios_seleccionados.append("masaje:2")
                            print("Masaje anadido: 2 servicios")
                            break
                    else:
                        print("No hay 2 servicios de masaje disponibles")
                except ValueError:
                    print("Ingresa un numero (1 o 2)")
        else:
            print("Sin servicio de masaje")
            




        
        




if True:
    main()


