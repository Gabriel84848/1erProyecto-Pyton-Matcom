from datetime import date

def obtener_fechas():
    print("Introduzca las fechas de la reserva")
    print("Escribe 'cancelar' en cualquier momento para salir")

    hoy = date.today()
    while True:
        try:
            print("Check-in")

            fecha_in_str = input("   Fecha (DD-MM-AAAA) o 'cancelar': ").strip()

            if fecha_in_str.lower() == 'cancelar':
                print("Cancelado por usuario")
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
                print(f"El check-in no puede ser en el pasado")
                print(f"Hoy es: {hoy.strftime('%d-%m-%Y')}")
                continue
            
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

            if fecha_out_str.lower() == 'cancelar':
                print("Cancelado por usuario")
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
