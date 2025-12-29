from guardar_y_cargar import cargar_Habitaciones, guardar_reservas
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
    habitaciones, servicios, reservas = cargar_Habitaciones()

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
        
        else:
            print("NO")
            input("\nPresiona Enter para volver al menu")

if True:
    main()


