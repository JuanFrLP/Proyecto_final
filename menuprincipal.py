inventario = []  # Lista donde se guardan los hilos

#Registrar un nuevo hilo
def registrar_hilo():
    print("\n--- Registrar nuevo hilo ---")
    marca = input("Marca: ")
    codigo_color = input("Código de color: ")
    descripcion = input("Descripción: ")
    cantidad = int(input("Cantidad: "))
    precio_unitario = float(input("Precio unitario: "))
    proveedor = input("Proveedor: ")

    hilo = {
        "marca": marca,
        "codigo_color": codigo_color,
        "descripcion": descripcion,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "proveedor": proveedor
    }

    inventario.append(hilo)
    print("Hilo registrado con éxito.")

    #Buscar hilos por marca, código o descripción
def buscar_hilo():
    print("\n--- Buscar hilo ---")
    criterio = input("Buscar por (marca / código / descripción): ").lower()
    valor = input("Ingrese el valor a buscar: ").lower()

    if criterio in ["código", "codigo"]:
        campo = "codigo_color"
    elif criterio in ["descripcion", "descripción"]:
        campo = "descripcion"
    elif criterio == "marca":
        campo = "marca"
    else:
        print("Criterio no válido. Use: marca, código o descripción.")
        return

    encontrados = [h for h in inventario if valor in h[campo].lower()]

    if encontrados:
        for h in encontrados:
            print(f"Marca: {h['marca']} | Código: {h['codigo_color']} | "
                  f"Descripción: {h['descripcion']} | Cantidad: {h['cantidad']} | "
                  f"Precio: Q{h['precio_unitario']} | Proveedor: {h['proveedor']}")
    else:
        print("No se encontraron coincidencias.")