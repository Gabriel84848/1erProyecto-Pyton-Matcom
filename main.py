from guardar_y_cargar import cargar_datos, guardar_datos
from datetime import datetime, date, timedelta
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
        
def crear_reserva(habitaciones, servicios, reservas):
    print("Creando nueva reserva")

def obtener_fechas():
    print("Introduzca las fechas de la reserva")

    while True:
        try:
            print("Check-in")
            fecha_in_str = input("   Fecha (DD-MM-AAAA): ").strip()
            
            #2 guiones para que no se parte el split
            if fecha_in_str.count('-') != 2:
                print("Formato incorrecto. Usa DD-MM-AAAA")
                continue
            
            dia_str, mes_str, ano_str = fecha_in_str.split('-')
            dia = int(dia_str)
            mes = int(mes_str)
            ano = int(ano_str)
            
            check_in = date(ano, mes, dia)
        
            hoy = date.today()

            if check_in < hoy:
                print(f"El check-in no puede ser en el pasado")
                print(f"Hoy es: {hoy.strftime('%d-%m-%Y')}")
                continue

            from datetime import timedelta
            maxima_fecha = hoy.replace(year=hoy.year + 2)
            
            if check_in > maxima_fecha:
                print(f"De aqui a 2 anos pueden pasar muchas cosas")
                print(f"Fecha máxima permitida: {maxima_fecha.strftime('%d-%m-%Y')}")
                continue

            print(f"Check-in valido: {check_in.strftime('%d-%m-%Y')}")
            break
            
        except ValueError:
            print("Fecha invalida. Asegurate de usar numeros correctos")
        except Exception as e:
            print(f"Error: {e}")
    
    while True:
        try:
            print("CHECK-OUT")
            fecha_out_str = input("   Fecha (DD-MM-AAAA): ").strip()
            
            if fecha_out_str.count('-') != 2:
                print("Formato incorrecto. Usa DD-MM-AAAA")
                continue
            
            dia_str, mes_str, ano_str = fecha_out_str.split('-')
            dia = int(dia_str)
            mes = int(mes_str)
            ano = int(ano_str)
            
            
            check_out = date(ano, mes, dia)
            
            if check_out <= check_in:
                print(f"El check-out debe ser despues del check-in")
                print(f"Check-in: {check_in.strftime('%d-%m-%Y')}")
                continue
            
            if (check_out - check_in).days < 1:
                print("La estancia minima es de 1 dia completo")
                continue
            
            print(f"Check-out valido: {check_out.strftime('%d-%m-%Y')}")
            break
            
        except ValueError:
            print("Fecha invalida. Asegurate de usar numeros correctos")
        except Exception as e:
            print(f"Error: {e}")
    
    noches = (check_out - check_in).days
    print("FECHAS CONFIRMADAS:")
    print(f"Check-in:  {check_in.strftime('%d-%m-%Y')}")
    print(f"Check-out: {check_out.strftime('%d-%m-%Y')}")
    print(f"Noches:  {noches}")
    
    return check_in, check_out




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

if True:
    main()


