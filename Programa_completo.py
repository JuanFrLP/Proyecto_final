from openpyxl import Workbook, load_workbook
import os

# VARIABLES GLOBALES
inventario = []
historial_ventas = []
historial_compras = []
usuarios = []  
contador_id = 1
nombre_archivo = "inventario_hilos.xlsx"

# Config de permisos/alertas
PERMITIR_VENTA_EMPLEADO = True
STOCK_MINIMO = 6  # alerta cuando quede <= a este valor


# UTILIDADES
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def leer_entero(mensaje, minimo=None):
    while True:
        val = input(mensaje)
        try:
            n = int(val)
            if minimo is not None and n < minimo:
                print(f"Debe ser un número entero ≥ {minimo}.")
                continue
            return n
        except ValueError:
            print("Entrada inválida. Ingrese un número entero.")


def leer_flotante(mensaje, minimo=None):
    while True:
        val = input(mensaje)
        try:
            f = float(val)
            if minimo is not None and f < minimo:
                print(f"Debe ser un número ≥ {minimo}.")
                continue
            return f
        except ValueError:
            print("Entrada inválida. Ingrese un número (puede usar decimales).")


# EXCEL: ESTRUCTURA Y CARGA
def asegurar_estructura_excel_y_usuarios():

    if os.path.exists(nombre_archivo):
        wb = load_workbook(nombre_archivo)
    else:
        wb = Workbook()

    # Inventario
    if "Inventario de Hilos" not in wb.sheetnames:
        hoja_inv = wb.active
        hoja_inv.title = "Inventario de Hilos"
        hoja_inv.append(["ID", "Marca", "Código de Color", "Descripción",
                         "Cantidad", "Precio Unitario", "Proveedor"])
    else:
        hoja_inv = wb["Inventario de Hilos"]
        if hoja_inv.max_row == 0:
            hoja_inv.append(["ID", "Marca", "Código de Color", "Descripción",
                             "Cantidad", "Precio Unitario", "Proveedor"])

    # Compras
    if "Historial Compras" not in wb.sheetnames:
        hoja_comp = wb.create_sheet("Historial Compras")
        hoja_comp.append(["Código", "Marca", "Descripción", "Cantidad",
                          "Costo Unitario", "Total"])
    else:
        hoja_comp = wb["Historial Compras"]
        if hoja_comp.max_row == 0:
            hoja_comp.append(["Código", "Marca", "Descripción", "Cantidad",
                              "Costo Unitario", "Total"])

    # Ventas
    if "Historial Ventas" not in wb.sheetnames:
        hoja_vent = wb.create_sheet("Historial Ventas")
        hoja_vent.append(["Código", "Marca", "Descripción", "Cantidad", "Total"])
    else:
        hoja_vent = wb["Historial Ventas"]
        if hoja_vent.max_row == 0:
            hoja_vent.append(["Código", "Marca", "Descripción", "Cantidad", "Total"])

    # Usuarios
    if "Usuario s" not in wb.sheetnames:
        hoja_usr = wb.create_sheet("Usuarios")
        hoja_usr.append(["Usuario", "Contraseña", "Rol"])
        hoja_usr.append(["admin", "admin123", "admin"])
        hoja_usr.append(["empleado", "azul321", "user"])
    else:
        hoja_usr = wb["Usuarios"]
        if hoja_usr.max_row < 2:
            hoja_usr.append(["Usuario", "Contraseña", "Rol"])
            hoja_usr.append(["admin", "admin123", "admin"])
            hoja_usr.append(["empleado", "azul321", "user"])

    wb.save(nombre_archivo)


def cargar_usuarios():
    usuarios.clear()
    if not os.path.exists(nombre_archivo):
        asegurar_estructura_excel_y_usuarios()

    wb = load_workbook(nombre_archivo)
    if "Usuarios" not in wb.sheetnames:
        asegurar_estructura_excel_y_usuarios()
        wb = load_workbook(nombre_archivo)

    hoja = wb["Usuarios"]
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        if fila and fila[0]:
            usuarios.append({
                "usuario": str(fila[0]),
                "password": str(fila[1]) if fila[1] is not None else "",
                "rol": str(fila[2]).lower() if fila[2] else "user"
            })


def cargar_inventario():
    global contador_id
    inventario.clear()
    historial_ventas.clear()
    historial_compras.clear()

    if os.path.exists(nombre_archivo):
        wb = load_workbook(nombre_archivo)

        if "Inventario de Hilos" in wb.sheetnames:
            hoja = wb["Inventario de Hilos"]
            for fila in hoja.iter_rows(min_row=2, values_only=True):
                if fila and fila[0] is not None:
                    inventario.append({
                        "id": fila[0],
                        "marca": fila[1],
                        "codigo_color": str(fila[2]),
                        "descripcion": fila[3],
                        "cantidad": int(fila[4]),
                        "precio_unitario": float(fila[5]),
                        "proveedor": fila[6]
                    })

        if "Historial Compras" in wb.sheetnames:
            hoja_compras = wb["Historial Compras"]
            for fila in hoja_compras.iter_rows(min_row=2, values_only=True):
                if fila and fila[0] is not None:
                    historial_compras.append({
                        "codigo_color": str(fila[0]),
                        "marca": fila[1],
                        "descripcion": fila[2],
                        "cantidad": int(fila[3]),
                        "costo_unitario": float(fila[4]),
                        "total": float(fila[5])
                    })

        if "Historial Ventas" in wb.sheetnames:
            hoja_ventas = wb["Historial Ventas"]
            for fila in hoja_ventas.iter_rows(min_row=2, values_only=True):
                if fila and fila[0] is not None:
                    historial_ventas.append({
                        "codigo_color": str(fila[0]),
                        "marca": fila[1],
                        "descripcion": fila[2],
                        "cantidad": int(fila[3]),
                        "total": float(fila[4])
                    })

        if inventario:
            contador_id = max(h["id"] for h in inventario) + 1
        else:
            contador_id = 1


def actualizar_excel():
    if os.path.exists(nombre_archivo):
        wb = load_workbook(nombre_archivo)
    else:
        wb = Workbook()

    # Inventario
    if "Inventario de Hilos" in wb.sheetnames:
        hoja_inv = wb["Inventario de Hilos"]
        if hoja_inv.max_row > 1:
            hoja_inv.delete_rows(2, hoja_inv.max_row - 1)
    else:
        hoja_inv = wb.active
        hoja_inv.title = "Inventario de Hilos"
        hoja_inv.append(["ID", "Marca", "Código de Color", "Descripción",
                         "Cantidad", "Precio Unitario", "Proveedor"])

    for h in inventario:
        hoja_inv.append([h["id"], h["marca"], h["codigo_color"], h["descripcion"],
                         h["cantidad"], h["precio_unitario"], h["proveedor"]])

    # Compras
    if "Historial Compras" in wb.sheetnames:
        hoja_comp = wb["Historial Compras"]
        if hoja_comp.max_row > 1:
            hoja_comp.delete_rows(2, hoja_comp.max_row - 1)
    else:
        hoja_comp = wb.create_sheet("Historial Compras")
        hoja_comp.append(["Código", "Marca", "Descripción", "Cantidad",
                          "Costo Unitario", "Total"])

    for c in historial_compras:
        hoja_comp.append([c["codigo_color"], c["marca"], c["descripcion"],
                          c["cantidad"], c["costo_unitario"], c["total"]])

    # Ventas
    if "Historial Ventas" in wb.sheetnames:
        hoja_vent = wb["Historial Ventas"]
        if hoja_vent.max_row > 1:
            hoja_vent.delete_rows(2, hoja_vent.max_row - 1)
    else:
        hoja_vent = wb.create_sheet("Historial Ventas")
        hoja_vent.append(["Código", "Marca", "Descripción", "Cantidad", "Total"])

    for v in historial_ventas:
        hoja_vent.append([v["codigo_color"], v["marca"], v["descripcion"],
                          v["cantidad"], v["total"]])

    try:
        wb.save(nombre_archivo)
        print("\nArchivo Excel actualizado correctamente.\n")
    except PermissionError:
        print("\nCierra el archivo Excel antes de guardar.\n")


# LOGIN
def login():
    print("=== INICIO DE SESIÓN ===")
    while True:
        usr = input("Usuario: ").strip()
        pwd = input("Contraseña: ").strip()
        for u in usuarios:
            if u["usuario"] == usr and u["password"] == pwd:
                print(f"\nBienvenido, {usr}. Rol: {u['rol']}\n")
                return u["rol"], usr
        print("Credenciales inválidas. Inténtelo de nuevo.\n")

# ALERTA DE STOCK BAJO
def verificar_alerta_stock(hilo):
    if hilo["cantidad"] <= STOCK_MINIMO:
        print("\n ---- ALERTA DE STOCK ----- ")
        print(f"Código: {hilo['codigo_color']}")
        print(f"Descripción: {hilo['descripcion']}")
        print(f"Unidades disponibles: {hilo['cantidad']}\n")


def registrar_hilo():
    global contador_id
    limpiar_pantalla()
    print("=== Registrar Nuevo Hilo ===")
    marca = input("Marca: ").strip()

    while True:
        codigo_color = input("Código de color (solo números): ").strip()
        if not codigo_color.isdigit():
            print("Error: el código de color debe ser numérico.")
            continue
        if any(h["codigo_color"] == codigo_color for h in inventario):
            print("Error: este código de color ya está registrado.")
            continue
        break

    descripcion = input("Descripción: ").strip()
    cantidad = leer_entero("Cantidad: ", minimo=0)
    precio_unitario = leer_flotante("Precio unitario: ", minimo=0.0)
    proveedor = input("Proveedor: ").strip()

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

    print(f"\nHilo registrado con éxito. ID: {hilo['id']}")
    actualizar_excel()


def buscar_hilo():
    limpiar_pantalla()
    print("=== Buscar Hilo ===")
    criterio = input("Buscar por (marca / código / descripción): ").lower().strip()
    valor = input("Ingrese el valor a buscar: ").lower().strip()

    campo = "marca" if criterio == "marca" else "codigo_color" if criterio in ["codigo", "código"] else "descripcion"
    encontrados = [h for h in inventario if valor in str(h[campo]).lower()]

    if encontrados:
        print(f"\nResultados encontrados ({len(encontrados)}):\n")
        for h in encontrados:
            print(f"ID:{h['id']} | Marca:{h['marca']} | Código:{h['codigo_color']} | "
                  f"Descripción:{h['descripcion']} | Cantidad:{h['cantidad']} | "
                  f"Precio:Q{h['precio_unitario']} | Proveedor:{h['proveedor']}")
    else:
        print("No se encontraron coincidencias.")


def modificar_hilo():
    limpiar_pantalla()
    codigo = input("Ingrese el código de color del hilo a modificar: ").strip()

    for h in inventario:
        if h["codigo_color"] == codigo:
            print(f"Hilo encontrado: {h['descripcion']}")
            nueva_marca = input(f"Nueva marca ({h['marca']}): ").strip()
            if nueva_marca:
                h["marca"] = nueva_marca

            nueva_desc = input(f"Nueva descripción ({h['descripcion']}): ").strip()
            if nueva_desc:
                h["descripcion"] = nueva_desc

            try:
                nueva_cantidad = input(f"Nueva cantidad ({h['cantidad']}): ").strip()
                if nueva_cantidad:
                    h["cantidad"] = int(nueva_cantidad)
                    verificar_alerta_stock(h)  # ALERTA SOLO SI SE CAMBIA CANTIDAD
                nuevo_precio = input(f"Nuevo precio ({h['precio_unitario']}): ").strip()
                if nuevo_precio:
                    h["precio_unitario"] = float(nuevo_precio)
            except ValueError:
                print("Entrada inválida. Se mantienen los valores actuales.")

            nuevo_prov = input(f"Nuevo proveedor ({h['proveedor']}): ").strip()
            if nuevo_prov:
                h["proveedor"] = nuevo_prov

            print("Información actualizada correctamente.")
            actualizar_excel()
            return
    print("Hilo no encontrado.")


def eliminar_hilo():
    codigo = input("Ingrese el código de color del hilo a eliminar: ").strip()
    for h in inventario:
        if h["codigo_color"] == codigo:
            if h["cantidad"] == 0:
                inventario.remove(h)
                print("Hilo eliminado.")
                actualizar_excel()
            else:
                print("No se puede eliminar. Aún hay unidades disponibles.")
            return
    print("Hilo no encontrado.")


# COMPRAS Y VENTAS
def registrar_compra():
    print("\n--- Registrar compra/reabastecimiento ---")
    codigo = input("Código de color del hilo: ").strip()
    cantidad = leer_entero("Cantidad comprada: ", minimo=1)
    costo_unitario = leer_flotante("Costo por unidad: ", minimo=0.0)

    for h in inventario:
        if h["codigo_color"] == codigo:
            h["cantidad"] += cantidad
            verificar_alerta_stock(h)  # ALERTA SI SIGUE BAJO LUEGO DE COMPRA
            historial_compras.append({
                "codigo_color": codigo,
                "marca": h["marca"],
                "descripcion": h["descripcion"],
                "cantidad": cantidad,
                "costo_unitario": costo_unitario,
                "total": round(cantidad * costo_unitario, 2)
            })
            print("Compra registrada y cantidad actualizada.")
            actualizar_excel()
            return
    print("Hilo no encontrado.")


def registrar_venta():
    print("\n--- Registrar venta ---")
    codigo = input("Código de color del hilo: ").strip()

    for h in inventario:
        if h["codigo_color"] == codigo:
            print(f"Cantidad disponible: {h['cantidad']} unidades")
            cantidad = leer_entero("Cantidad vendida: ", minimo=1)
            if cantidad > h["cantidad"]:
                print("No hay suficiente stock disponible.")
                return

            # Actualizar inventario
            h["cantidad"] -= cantidad
            verificar_alerta_stock(h)  # ALERTA DESPUES DE VENTA

            # Registrar en historial
            total = round(cantidad * h["precio_unitario"], 2)
            historial_ventas.append({
                "codigo_color": codigo,
                "marca": h["marca"],
                "descripcion": h["descripcion"],
                "cantidad": cantidad,
                "total": total
            })

            print(f"Venta registrada. Total: Q{total:.2f}")
            actualizar_excel()
            return

    print("Hilo no encontrado.")

# REPORTES / CONSULTAS
def reportes():
    print("\n--- Reportes y Consultas ---")
    print("1. Reporte general de inventario")
    print("2. Reporte por marca")
    print("3. Historial de ventas")
    print("4. Historial de compras")
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        mostrar_inventario()
    elif opcion == "2":
        marca = input("Ingrese la marca a consultar: ").lower().strip()
        encontrados = [h for h in inventario if marca in h["marca"].lower()]
        if encontrados:
            for h in encontrados:
                print(f"Marca:{h['marca']} | Código:{h['codigo_color']} | Descripción:{h['descripcion']} | "
                      f"Cantidad:{h['cantidad']} | Precio:Q{h['precio_unitario']}")
        else:
            print("No se encontraron hilos con esa marca.")
    elif opcion == "3":
        print("\n--- Historial de Ventas ---")
        if not historial_ventas:
            print("No hay ventas registradas.")
        else:
            for v in historial_ventas:
                print(f"Marca:{v['marca']} | Código:{v['codigo_color']} | Descripción:{v['descripcion']} | "
                      f"Cantidad:{v['cantidad']} | Total:Q{v['total']:.2f}")
    elif opcion == "4":
        print("\n--- Historial de Compras ---")
        if not historial_compras:
            print("No hay compras registradas.")
        else:
            for c in historial_compras:
                print(f"Marca:{c['marca']} | Código:{c['codigo_color']} | Descripción:{c['descripcion']} | "
                      f"Cantidad:{c['cantidad']} | Costo Unitario:Q{c['costo_unitario']:.2f} | "
                      f"Total:Q{c['total']:.2f}")
    else:
        print("Opción no válida.")


def mostrar_inventario():
    limpiar_pantalla()
    print("=== Inventario Completo ===\n")
    if not inventario:
        print(" No hay hilos registrados.")
    else:
        print(f"{'ID':<4} {'Marca':<15} {'Código':<10} {'Descripción':<20} {'Cant.':<7} {'Precio(Q)':<10} {'Proveedor'}")
        print("-" * 80)
        for h in inventario:
            print(f"{h['id']:<4} {h['marca']:<15} {h['codigo_color']:<10} {h['descripcion']:<20} "
                  f"{h['cantidad']:<7} {h['precio_unitario']:<10.2f} {h['proveedor']}")
        print(f"\nTotal de hilos registrados: {len(inventario)}")


# MENÚS POR ROL
def menu_admin():
    while True:
        print("\n==== MENÚ ADMINISTRADOR ====")
        print("1. Registrar nuevo hilo")
        print("2. Buscar hilo")
        print("3. Modificar información")
        print("4. Eliminar hilo")
        print("5. Registrar compra/reabastecimiento")
        print("6. Registrar venta")
        print("7. Reportes y consultas")
        print("8. Mostrar inventario completo")
        print("9. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_hilo()
        elif opcion == "2":
            buscar_hilo()
        elif opcion == "3":
            modificar_hilo()
        elif opcion == "4":
            eliminar_hilo()
        elif opcion == "5":
            registrar_compra()
        elif opcion == "6":
            registrar_venta()
        elif opcion == "7":
            reportes()
        elif opcion == "8":
            mostrar_inventario()
        elif opcion == "9":
            print("\nAdiós.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


def menu_user():
    while True:
        print("\n==== MENÚ EMPLEADO ====")
        print("1. Buscar hilo")
        print("2. Registrar venta")
        print("3. Reportes y consultas")
        print("4. Mostrar inventario completo")
        print("5. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            buscar_hilo()
        elif opcion == "2" and PERMITIR_VENTA_EMPLEADO:
            registrar_venta()
        elif opcion == "3":
            reportes()
        elif opcion == "4":
            mostrar_inventario()
        elif opcion == "5":
            print("\nAdiós.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


# FUNCIÓN PRINCIPAL
def menu():
    # Estructura base y usuarios
    asegurar_estructura_excel_y_usuarios()
    cargar_usuarios()
    cargar_inventario()

    # Login obligatorio
    rol, _ = login()

    # Redirige según rol
    if rol == "admin":
        menu_admin()
    else:
        menu_user()


# MAIN
if __name__ == "__main__":
    menu()