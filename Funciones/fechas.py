from datetime import date

def obtener_fechas():
    print("Introduce las fechas de la reserva")
    print("Formato: DD-MM-AAAA")
    print("Escribe 'cancelar' en cualquier momento para salir")

    hoy = date.today()
    while True:
        try:
            print("CHECK-IN")

            fecha_in_str = input("   Fecha (DD-MM-AAAA) o 'cancelar': ").strip()

            if fecha_in_str.lower() == 'cancelar':
                print("Cancelado por el usuario")
                return None, None
            
            #2 guiones para que no se parte el split
            if fecha_in_str.count('-') != 2:
                print("Formato incorrecto. Usa DD-MM-AAAA")
                continue
            
            dia_str, mes_str, ano_str = fecha_in_str.split('-')
            dia = int(dia_str)
            mes = int(mes_str)
            ano = int(ano_str)
            
            check_in = date(ano, mes, dia)

            if check_in < hoy:
                print(f"Error: El check-in no puede ser en el pasado.")
                print(f"Hoy es: {hoy.strftime('%d-%m-%Y')}")
                continue
            
            maxima_fecha = hoy.replace(year=hoy.year + 2)
            
            if check_in > maxima_fecha:
                print(f"Error: No se aceptan reservas con más de 2 años de antelación.")
                print(f"Fecha máxima permitida: {maxima_fecha.strftime('%d-%m-%Y')}")
                continue

            print(f"✓ Check-in válido: {check_in.strftime('%d-%m-%Y')}")
            break
            
        except ValueError:
            print("Fecha inválida. Asegúrate de usar números correctos.")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    while True:
        try:
            print("CHECK-OUT")
            fecha_out_str = input("   Fecha (DD-MM-AAAA): ").strip()

            if fecha_out_str.lower() == 'cancelar':
                print("Cancelado por el usuario")
                return None, None
            
            if fecha_out_str.count('-') != 2:
                print("Formato incorrecto. Usa DD-MM-AAAA")
                continue
            
            dia_str, mes_str, ano_str = fecha_out_str.split('-')
            dia = int(dia_str)
            mes = int(mes_str)
            ano = int(ano_str)
            
            
            check_out = date(ano, mes, dia)
            
            if check_out <= check_in:
                print(f"Error: El check-out debe ser después del check-in.")
                print(f"Check-in: {check_in.strftime('%d-%m-%Y')}")
                continue
            
            if (check_out - check_in).days < 1:
                print("Error: La estancia mínima es de 1 día completo.")
                continue
            
            print(f"✓ Check-out válido: {check_out.strftime('%d-%m-%Y')}")
            break
            
        except ValueError:
            print("Fecha inválida. Asegúrate de usar números correctos.")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    noches = (check_out - check_in).days
    print("\n" + "="*30)
    print("FECHAS CONFIRMADAS")
    print("="*30)
    print(f"Check-in:  {check_in.strftime('%d-%m-%Y')}")
    print(f"Check-out: {check_out.strftime('%d-%m-%Y')}")
    print(f"Noches:    {noches}")
    
    return check_in, check_out