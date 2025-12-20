from guardar_y_cargar import cargar_Habitaciones

habitaciones = cargar_Habitaciones()
print(f"Hay {len(habitaciones)} habitaciones")

print(f"lista de habitaciones:")

for i in habitaciones:
    print(f"{i}")