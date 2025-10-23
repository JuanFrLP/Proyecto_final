from openpyxl import Workbook, load_workbook
import os

inventario = []  # Lista donde se guardan los hilos
contador_id = 1  # Contador global para IDs únicos
nombre_archivo = "inventario_hilos.xlsx"

# Limpiar pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Cargar inventario desde Excel y sincronizar ID
def cargar_inventario():
    global contador_id
    if os.path.exists(nombre_archivo):
        wb = load_workbook(nombre_archivo)
        hoja = wb.active
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            if fila[0] is not None:
                hilo = {
                    "id": fila[0],
                    "marca": fila[1],
                    "codigo_color": str(fila[2]),
                    "descripcion": fila[3],
                    "cantidad": fila[4],
                    "precio_unitario": fila[5],
                    "proveedor": fila[6]
                }
                inventario.append(hilo)
        if inventario:
            contador_id = max(h["id"] for h in inventario) + 1

# Actualizar Excel
def actualizar_excel():
    wb = Workbook()
    hoja = wb.active
    hoja.title = "Inventario de Hilos"
    encabezados = ["ID", "Marca", "Código de Color", "Descripción", "Cantidad", "Precio Unitario", "Proveedor"]
    hoja.append(encabezados)

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
    print("\n Archivo Excel actualizado correctamente.\n")

# Registrar nuevo hilo
def registrar_hilo():
    global contador_id
    limpiar_pantalla()
    print("=== Registrar Nuevo Hilo ===")
    marca = input("Marca: ")

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

    while True:
        try:
            cantidad = int(input("Cantidad: "))
            if cantidad < 0:
                print(" La cantidad no puede ser negativa.")
                continue
            break
        except ValueError:
            print(" Ingrese un número entero válido.")

    while True:
        try:
            precio_unitario = float(input("Precio unitario: "))
            if precio_unitario < 0:
                print(" El precio no puede ser negativo.")
                continue
            break
        except ValueError:
            print(" Ingrese un número válido para el precio.")

    proveedor = input("Proveedor: ")

    hilo = {
        "id": contador_id,
        "marca": marca,
        "codigo_color": codigo_color,
        "descripcion": descripcion,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "proveedor": proveedor
    }

    inventario.append(hilo)
    contador_id += 1

    print(f"\n Hilo registrado con éxito. ID asignado: {hilo['id']}")
    actualizar_excel()

# Buscar hilos
def buscar_hilo():
    limpiar_pantalla()
    print("=== Buscar Hilo ===")
    criterio = input("Buscar por (marca / código / descripción): ").lower()
    valor = input("Ingrese el valor a buscar: ").lower()

    if criterio in ["código", "codigo"]:
        campo = "codigo_color"
    elif criterio in ["descripcion", "descripción"]:
        campo = "descripcion"
    elif criterio == "marca":
        campo = "marca"
    else:
        print(" Criterio no válido. Use: marca, código o descripción.")
        return

    encontrados = [h for h in inventario if valor in h[campo].lower()]

    if encontrados:
        print(f"\n Resultados encontrados ({len(encontrados)}):\n")
        for h in encontrados:
            print(f"ID: {h['id']} | Marca: {h['marca']} | Código: {h['codigo_color']} | "
                  f"Descripción: {h['descripcion']} | Cantidad: {h['cantidad']} | "
                  f"Precio: Q{h['precio_unitario']} | Proveedor: {h['proveedor']}")
    else:
        print("\n No se encontraron coincidencias.")

# Modificar hilo
def modificar_hilo():
    limpiar_pantalla()
    print("=== Modificar Hilo ===")
    codigo = input("Ingrese el código de color del hilo a modificar: ")

    for hilo in inventario:
        if hilo["codigo_color"] == codigo:
            print(f"\nHilo encontrado: {hilo['descripcion']}")
            print("Deje en blanco si no desea cambiar un dato.\n")
            nueva_marca = input(f"Nueva marca ({hilo['marca']}): ") or hilo['marca']
            nueva_desc = input(f"Nueva descripción ({hilo['descripcion']}): ") or hilo['descripcion']

            while True:
                nueva_cantidad = input(f"Nueva cantidad ({hilo['cantidad']}): ")
                if nueva_cantidad == "":
                    nueva_cantidad = hilo['cantidad']
                    break
                try:
                    nueva_cantidad = int(nueva_cantidad)
                    if nueva_cantidad < 0:
                        print("La cantidad no puede ser negativa.")
                        continue
                    break
                except ValueError:
                    print("Ingrese un número válido.")

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
                    print("Ingrese un número válido.")

            nuevo_proveedor = input(f"Nuevo proveedor ({hilo['proveedor']}): ") or hilo['proveedor']

            hilo['marca'] = nueva_marca
            hilo['descripcion'] = nueva_desc
            hilo['cantidad'] = nueva_cantidad
            hilo['precio_unitario'] = nuevo_precio
            hilo['proveedor'] = nuevo_proveedor

            print("\n Información actualizada con éxito.")
            actualizar_excel()
            return
    print(" No se encontró un hilo con ese código.")

# Eliminar hilo
def eliminar_hilo():
    limpiar_pantalla()
    print("=== Eliminar Hilo ===")
    codigo = input("Ingrese el código de color del hilo a eliminar: ")

    for hilo in inventario:
        if hilo["codigo_color"] == codigo:
            if hilo["cantidad"] == 0:
                inventario.remove(hilo)
                print("\n Hilo eliminado del inventario.")
                actualizar_excel()
            else:
                print("\n No se puede eliminar. Aún hay unidades disponibles.")
            return
    print(" No se encontró un hilo con ese código.")

# Mostrar inventario completo
def mostrar_inventario():
    limpiar_pantalla()
    print("=== Inventario Completo ===\n")
    if not inventario:
        print(" No hay hilos registrados.")
    else:
        for h in inventario:
            print(f"ID: {h['id']} | Marca: {h['marca']} | Código: {h['codigo_color']} | "
                  f"Descripción: {h['descripcion']} | Cantidad: {h['cantidad']} | "
                  f"Precio: Q{h['precio_unitario']} | Proveedor: {h['proveedor']}")
        print(f"\nTotal de hilos registrados: {len(inventario)}")

# Menú principal
def menu():
    cargar_inventario()  # Cargar inventario y sincronizar IDs al iniciar
    while True:
        print("\n==== MENÚ PRINCIPAL ====")
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
            print("\n Adiós")
            break
        else:
            print(" Opción inválida. Intente de nuevo.")

menu()
