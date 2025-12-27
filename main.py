from guardar_y_cargar import cargar_Habitaciones, guardar_reservas

#def console.clear pero en pyton

def Menu():

    print("\nBLUE GATE HOTEL - Reservas")
    
    print("1. habitaciones disponibles")
    print("2. ver Servicios del hotel ")
    print("3. ver Reservas existentes")
    print("4. Crear nueva reserva ")
    print("5. Cancelar reserva existente")
    print("6. Guardar cambios")

    return input("selecciona una opcion (1 - 6): ")
    
def main():

    print("BLUE GATE HOTEL - Reservas")

    habitaciones, servicios, reservas = cargar_Habitaciones()

    print(f"\n ESTADISTICAS DEL HOTEL")
    print(f"habitaciones: {len(habitaciones)}")
    print(f"servicios: {len(servicios)}")
    print(f"reservas: {len(reservas)}")

    if habitaciones:
        
        print(f"primera habitacion")
        print(f"{habitaciones[0]}")

        print(f"servicios disponibles")
        for servicio in servicios:
            print(f"primera habitacion")
        print(f"{servicio}")

if "a":
    main()


