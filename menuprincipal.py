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

#Modificar información de un hilo existente
def modificar_hilo():
    print("\n--- Modificar información de un hilo ---")
    codigo = input("Ingrese el código de color del hilo a modificar ")

    for hilo in inventario:
        if hilo["codigo_color"] == codigo:
            print(f"Hilo encontrado: {hilo['descripcion']}")
            print("Deje en blanco si no desea cambiar un dato.")
            nueva_marca = input(f"Nueva marca ({hilo['marca']}): ") or hilo['marca']
            nueva_desc = input(f"Nueva descripción ({hilo['descripcion']}): ") or hilo['descripcion']
            nueva_cantidad = input(f"Nueva cantidad ({hilo['cantidad']}): ")
            nuevo_precio = input(f"Nuevo precio ({hilo['precio_unitario']}): ")
            nuevo_proveedor = input(f"Nuevo proveedor ({hilo['proveedor']}): ") or hilo['proveedor']

            hilo['marca'] = nueva_marca
            hilo['descripcion'] = nueva_desc
            hilo['cantidad'] = int(nueva_cantidad) if nueva_cantidad else hilo['cantidad']
            hilo['precio_unitario'] = float(nuevo_precio) if nuevo_precio else hilo['precio_unitario']
            hilo['proveedor'] = nuevo_proveedor

            print("Información actualizada con éxito.")
            return
    print("No se encontró un hilo con ese código.")