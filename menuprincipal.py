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