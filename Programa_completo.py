from openpyxl import Workbook, load_workbook

inventario = []  # Lista donde se guardan los hilos

# Función para actualizar Excel
def actualizar_excel():
    nombre_archivo = "inventario_hilos.xlsx"

    try:    
        wb = load_workbook(nombre_archivo)
        hoja = wb.active
        if hoja.max_row > 1:
            hoja.delete_rows(2, hoja.max_row - 1)  # Borra todo excepto encabezados
    except FileNotFoundError:
        wb = Workbook()
        hoja = wb.active
        hoja.title = "Inventario de Hilos"
        encabezados = ["ID", "Marca", "Código de Color", "Descripción", "Cantidad", "Precio Unitario", "Proveedor"]
        hoja.append(encabezados)

    # Agregar los datos actualizados
    for hilo in inventario:
        hoja.append([
            hilo["id"],
            hilo["marca"],
            hilo["codigo_color"],
            hilo["descripcion"],
            hilo["cantidad"],
            hilo["precio_unitario"],
            hilo["proveedor"]
        ])

    wb.save(nombre_archivo)
    print("Archivo Excel actualizado correctamente.")

# Función para generar ID único
def generar_id():
    return len(inventario) + 1

# Registrar un nuevo hilo
def registrar_hilo():
    print("\n--- Registrar nuevo hilo ---")
    marca = input("Marca: ")

    # Validar código de color numérico y único
    while True:
        codigo_color = input("Código de color (solo números): ")
        if not codigo_color.isdigit():
            print("Error: el código de color debe ser numérico.")
            continue
        if any(h["codigo_color"] == codigo_color for h in inventario):
            print("Error: este código de color ya está registrado.")
            continue
        break

    descripcion = input("Descripción: ")

    # Validar cantidad
    while True:
        try:
            cantidad = int(input("Cantidad: "))
            if cantidad < 0:
                print("Cantidad no puede ser negativa.")
                continue
            break
        except ValueError:
            print("Ingrese un número entero válido para cantidad.")

    # Validar precio unitario
    while True:
        try:
            precio_unitario = float(input("Precio unitario: "))
            if precio_unitario < 0:
                print("El precio no puede ser negativo.")
                continue
            break
        except ValueError:
            print("Ingrese un precio válido (número).")

    proveedor = input("Proveedor: ")

    hilo = {
        "id": generar_id(),
        "marca": marca,
        "codigo_color": codigo_color,
        "descripcion": descripcion,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "proveedor": proveedor
    }

    inventario.append(hilo)
    print("Hilo registrado con éxito.")
    actualizar_excel()

# Buscar hilos por marca, código o descripción
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
            print(f"ID: {h['id']} | Marca: {h['marca']} | Código: {h['codigo_color']} | "
                  f"Descripción: {h['descripcion']} | Cantidad: {h['cantidad']} | "
                  f"Precio: Q{h['precio_unitario']} | Proveedor: {h['proveedor']}")
    else:
        print("No se encontraron coincidencias.")

# Modificar información de un hilo existente
def modificar_hilo():
    print("\n--- Modificar información de un hilo ---")
    codigo = input("Ingrese el código de color del hilo a modificar: ")

    for hilo in inventario:
        if hilo["codigo_color"] == codigo:
            print(f"Hilo encontrado: {hilo['descripcion']}")
            print("Deje en blanco si no desea cambiar un dato.")
            nueva_marca = input(f"Nueva marca ({hilo['marca']}): ") or hilo['marca']
            nueva_desc = input(f"Nueva descripción ({hilo['descripcion']}): ") or hilo['descripcion']

            # Cantidad
            while True:
                nueva_cantidad = input(f"Nueva cantidad ({hilo['cantidad']}): ")
                if nueva_cantidad == "":
                    nueva_cantidad = hilo['cantidad']
                    break
                try:
                    nueva_cantidad = int(nueva_cantidad)
                    if nueva_cantidad < 0:
                        print("Cantidad no puede ser negativa.")
                        continue
                    break
                except ValueError:
                    print("Ingrese un número válido para cantidad.")

            # Precio unitario
            while True:
                nuevo_precio = input(f"Nuevo precio ({hilo['precio_unitario']}): ")
                if nuevo_precio == "":
                    nuevo_precio = hilo['precio_unitario']
                    break
                try:
                    nuevo_precio = float(nuevo_precio)
                    if nuevo_precio < 0:
                        print("Precio no puede ser negativo.")
                        continue
                    break
                except ValueError:
                    print("Ingrese un número válido para el precio.")

            nuevo_proveedor = input(f"Nuevo proveedor ({hilo['proveedor']}): ") or hilo['proveedor']

            hilo['marca'] = nueva_marca
            hilo['descripcion'] = nueva_desc
            hilo['cantidad'] = nueva_cantidad
            hilo['precio_unitario'] = nuevo_precio
            hilo['proveedor'] = nuevo_proveedor

            print("Información actualizada con éxito.")
            actualizar_excel()
            return
    print("No se encontró un hilo con ese código.")

# Eliminar hilo si no hay unidades disponibles
def eliminar_hilo():
    print("\n--- Eliminar hilo ---")
    codigo = input("Ingrese el código de color del hilo a eliminar: ")

    for hilo in inventario:
        if hilo["codigo_color"] == codigo:
            if hilo["cantidad"] == 0:
                inventario.remove(hilo)
                print("Hilo eliminado del inventario.")
                actualizar_excel()
            else:
                print("No se puede eliminar. Aún hay unidades disponibles.")
            return
    print("No se encontró un hilo con ese código.")

# Mostrar inventario completo
def mostrar_inventario():
    print("\n--- Inventario de hilos ---")
    if not inventario:
        print("No hay hilos registrados.")
    else:
        for h in inventario:
            print(f"ID: {h['id']} | Marca: {h['marca']} | Código: {h['codigo_color']} | "
                  f"Descripción: {h['descripcion']} | Cantidad: {h['cantidad']} | "
                  f"Precio: Q{h['precio_unitario']} | Proveedor: {h['proveedor']}")

# Menú principal
def menu():
    while True:
        print("\n---- MENÚ PRINCIPAL ----")
        print("1. Registrar nuevo hilo")
        print("2. Buscar hilo")
        print("3. Modificar información")
        print("4. Eliminar hilo")
        print("5. Mostrar inventario completo")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_hilo()
        elif opcion == "2":
            buscar_hilo()
        elif opcion == "3":
            modificar_hilo()
        elif opcion == "4":
            eliminar_hilo()
        elif opcion == "5":
            mostrar_inventario()
        elif opcion == "6":
            print("Adiós.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

menu()
