from openpyxl import Workbook, load_workbook
import os
from datetime import datetime

# CONFIGURACIÓN
NOMBRE_ARCHIVO = "inventario_hilos.xlsx"
PERMITIR_VENTA_EMPLEADO = True
STOCK_MINIMO = 6  # alerta cuando quede <= a este valor

# Nombres de hojas en Excel
HOJA_INVENTARIO = "Inventario_Hilos"
HOJA_COMPRAS = "Historial_Compras"
HOJA_VENTAS = "Historial_Ventas"
HOJA_USUARIOS = "Usuarios"
HOJA_SESIONES = "Sesiones_Usuarios"


# UTILIDADES
class Utilidades:
    @staticmethod
    def limpiar_pantalla():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
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
                print("Error, intente con un número entero")

    @staticmethod
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
                print("Error, intente con un número ")


# MANEJO DE EXCEL
class GestorExcel:
    def __init__(self, archivo):
        self.nombre_archivo = archivo

    def asegurar_estructura(self):
        if os.path.exists(self.nombre_archivo):
            wb = load_workbook(self.nombre_archivo)
        else:
            wb = Workbook()

        # Si el libro viene vacío, usa la hoja activa como Inventario
        if HOJA_INVENTARIO not in wb.sheetnames:
            hoja_inv = wb.active
            hoja_inv.title = HOJA_INVENTARIO
            hoja_inv.append(["ID", "Marca", "Código de Color", "Descripción", "Cantidad", "Precio Unitario", "Proveedor"])

        # Crear/asegurar el resto de hojas
        definiciones = {
            HOJA_COMPRAS: ["Código", "Marca", "Descripción", "Cantidad", "Costo Unitario", "Total"],
            HOJA_VENTAS: ["Código", "Marca", "Descripción", "Cantidad", "Total"],
            HOJA_USUARIOS: ["Usuario", "Contraseña", "Rol"],
            HOJA_SESIONES: ["ID Sesión", "Usuario", "Rol", "Fecha y Hora de Inicio", "Fecha y Hora de Cierre"]
        }

        for hoja, encabezados in definiciones.items():
            if hoja not in wb.sheetnames:
                nueva = wb.create_sheet(hoja)
                nueva.append(encabezados)
                if hoja == HOJA_USUARIOS:
                    # usuarios por defecto
                    nueva.append(["admin", "admin123", "admin"])
                    nueva.append(["empleado", "azul321", "user"])
            else:
                obj = wb[hoja]
                if obj.max_row == 0:
                    obj.append(encabezados)

        wb.save(self.nombre_archivo)

    def cargar_hoja(self, nombre_hoja):
        if not os.path.exists(self.nombre_archivo):
            self.asegurar_estructura()
        wb = load_workbook(self.nombre_archivo)
        if nombre_hoja not in wb.sheetnames:
            return []
        hoja = wb[nombre_hoja]
        return [fila for fila in hoja.iter_rows(min_row=2, values_only=True) if fila and fila[0] is not None]

    def guardar_hoja(self, nombre_hoja, encabezados, datos):
        if os.path.exists(self.nombre_archivo):
            wb = load_workbook(self.nombre_archivo)
        else:
            wb = Workbook()
        if nombre_hoja not in wb.sheetnames:
            hoja = wb.create_sheet(nombre_hoja)
            hoja.append(encabezados)
        else:
            hoja = wb[nombre_hoja]
            if hoja.max_row > 1:
                hoja.delete_rows(2, hoja.max_row - 1)
        for fila in datos:
            hoja.append(fila)
        wb.save(self.nombre_archivo)

    def reparar_estructura(self):
        if not os.path.exists(self.nombre_archivo):
            print("No hay archivo Excel para reparar.")
            return

        wb = load_workbook(self.nombre_archivo)

        hojas_principales = [HOJA_INVENTARIO, HOJA_COMPRAS, HOJA_VENTAS]
        encabezados_validos = {
            HOJA_INVENTARIO: ["ID", "Marca", "Código de Color", "Descripción", "Cantidad", "Precio Unitario", "Proveedor"],
            HOJA_COMPRAS: ["Código", "Marca", "Descripción", "Cantidad", "Costo Unitario", "Total"],
            HOJA_VENTAS: ["Código", "Marca", "Descripción", "Cantidad", "Total"]
        }

        for hoja_nombre in hojas_principales:
            if hoja_nombre not in wb.sheetnames:
                continue

            hoja = wb[hoja_nombre]
            # Detectar encabezados incorrectos en filas posteriores
            filas_erroneas = []
            for i, fila in enumerate(hoja.iter_rows(values_only=True), start=1):
                if fila and any(isinstance(v, str) and v.strip() in encabezados_validos[hoja_nombre] for v in fila):
                    if i != 1:  # Si no es la primera fila (encabezado correcto)
                        filas_erroneas.append(i)

            # Borrar filas con encabezados repetidos
            if filas_erroneas:
                print(f"Corrigiendo encabezados duplicados en '{hoja_nombre}'...")
                # Elimina todas las filas excepto la primera
                hoja.delete_rows(2, hoja.max_row - 1)

        wb.save(self.nombre_archivo)
        print("Archivo Excel reparado correctamente.\n")

# SESIONES
class SesionUsuario:
    def __init__(self, gestor_excel: GestorExcel):
        self.excel = gestor_excel

    def abrir_sesion(self, usuario, rol):
        wb = load_workbook(self.excel.nombre_archivo)
        if HOJA_SESIONES not in wb.sheetnames:
            hoja = wb.create_sheet(HOJA_SESIONES)
            hoja.append(["ID Sesión", "Usuario", "Rol", "Fecha y Hora de Inicio", "Fecha y Hora de Cierre"])
        hoja = wb[HOJA_SESIONES]
        id_sesion = hoja.max_row  # correlativo (la fila 1 es encabezado)
        inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hoja.append([id_sesion, usuario, rol, inicio, ""])
        wb.save(self.excel.nombre_archivo)
        return id_sesion

    def cerrar_sesion(self, id_sesion):
        wb = load_workbook(self.excel.nombre_archivo)
        if HOJA_SESIONES not in wb.sheetnames:
            return
        hoja = wb[HOJA_SESIONES]
        cierre = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for fila in hoja.iter_rows(min_row=2):
            if fila[0].value == id_sesion:
                hoja.cell(row=fila[0].row, column=5, value=cierre)
                break
        wb.save(self.excel.nombre_archivo)

# INVENTARIO / COMPRAS / VENTAS / REPORTES
class InventarioHilos:
    def __init__(self, gestor_excel: GestorExcel, stock_minimo=STOCK_MINIMO):
        self.excel = gestor_excel
        self.stock_minimo = stock_minimo
        self.inventario = []
        self.historial_ventas = []
        self.historial_compras = []
        self.contador_id = 1
        self.cargar_todo()

    def cargar_todo(self):
        self.inventario.clear()
        self.historial_ventas.clear()
        self.historial_compras.clear()

        # --- Inventario ---
        for fila in self.excel.cargar_hoja(HOJA_INVENTARIO):
            try:
                id_val = int(fila[0])
            except (ValueError, TypeError):
                continue
            try:
                cantidad_val = int(fila[4])
            except (ValueError, TypeError):
                cantidad_val = 0
            try:
                precio_val = float(fila[5])
            except (ValueError, TypeError):
                precio_val = 0.0

            self.inventario.append({
                "id": id_val,
                "marca": fila[1],
                "codigo_color": str(fila[2]),
                "descripcion": fila[3],
                "cantidad": cantidad_val,
                "precio_unitario": precio_val,
                "proveedor": fila[6]
            })

        # --- Historial de Compras ---
        for f in self.excel.cargar_hoja(HOJA_COMPRAS):
            try:
                cant = int(f[3])
                costo = float(f[4])
                total = float(f[5])
            except (ValueError, TypeError):
                continue
            self.historial_compras.append({
                "codigo_color": str(f[0]),
                "marca": f[1],
                "descripcion": f[2],
                "cantidad": cant,
                "costo_unitario": costo,
                "total": total
            })

        # --- Historial de Ventas ---
        for f in self.excel.cargar_hoja(HOJA_VENTAS):
            try:
                cant = int(f[3])
                total = float(f[4])
            except (ValueError, TypeError):
                continue
            self.historial_ventas.append({
                "codigo_color": str(f[0]),
                "marca": f[1],
                "descripcion": f[2],
                "cantidad": cant,
                "total": total
            })

        # --- Asignar ID y aplicar ordenamientos automáticos ---
        self.contador_id = (max((h["id"] for h in self.inventario), default=0) + 1)

        if self.inventario:
            # 1️ Agrupar por marca y ordenar los códigos (Quick Sort)
            self.inventario = self.ordenar_por_codigo_color(self.inventario)

            # 2️  Ordenar por marcas con menor cantidad total (Selection Sort)
            self.inventario = self.ordenar_por_marca_con_menos_stock(self.inventario)

            # 3️ Ordenar por tipo de hilo (alfabéticamente) (Shell Sort)
            self.inventario = self.ordenar_por_tipo(self.inventario)

            # Guardado automáticamente el orden resultante en el archivo Excel
            self.guardar_todo()



    def guardar_todo(self):
        datos_inv = [
            [h["id"], h["marca"], h["codigo_color"], h["descripcion"], h["cantidad"], h["precio_unitario"], h["proveedor"]]
            for h in self.inventario
        ]
        datos_comp = [
            [c["codigo_color"], c["marca"], c["descripcion"], c["cantidad"], c["costo_unitario"], c["total"]]
            for c in self.historial_compras
        ]
        datos_vent = [
            [v["codigo_color"], v["marca"], v["descripcion"], v["cantidad"], v["total"]]
            for v in self.historial_ventas
        ]

        self.excel.guardar_hoja(
            HOJA_INVENTARIO,
            ["ID", "Marca", "Código de Color", "Descripción", "Cantidad", "Precio Unitario", "Proveedor"],
            datos_inv
        )
        self.excel.guardar_hoja(
            HOJA_COMPRAS,
            ["Código", "Marca", "Descripción", "Cantidad", "Costo Unitario", "Total"],
            datos_comp
        )
        self.excel.guardar_hoja(
            HOJA_VENTAS,
            ["Código", "Marca", "Descripción", "Cantidad", "Total"],
            datos_vent
        )
        print("\nListo, el archivo se actualizó.\n")

    # ---- Alertas ----
    def avisar_stock_bajo(self, hilo):
        if hilo["cantidad"] <= self.stock_minimo:
            print("\n ---STOCK BAJO--- ")
            print(f"Código: {hilo['codigo_color']}")
            print(f"Descripción: {hilo['descripcion']}")
            print(f"Unidades disponibles: {hilo['cantidad']}\n")

    # ---- CRUD de Hilos ----
    def registrar_hilo(self):
        while True:
            Utilidades.limpiar_pantalla()
            print("=== Registrar Nuevo Hilo ===")
            marca = input("Marca (o 'salir' para volver): ").strip()
            if marca.lower() == "salir":
                print("\nRegresando al menú...")
                break

            while True:
                codigo_color = input("Código de color (solo números): ").strip()
                if codigo_color.lower() == "salir":
                    print("\nRegresando al menú...")
                    return
                if not codigo_color.isdigit():
                    print("El código debe ser numérico.")
                    continue

                #Verificar si ya existe el mismo código en la misma marca
                if any(h["codigo_color"] == codigo_color and h["marca"].lower() == marca.lower() for h in self.inventario):
                    print("Ese código de color ya existe para esta marca.")
                    continue

                break


            descripcion = input("Descripción: ").strip()
            cantidad = Utilidades.leer_entero("Cantidad: ", minimo=0)
            precio_unitario = Utilidades.leer_flotante("Precio unitario: ", minimo=0.0)
            proveedor = input("Proveedor: ").strip()

            hilo = {
                "id": self.contador_id,
                "marca": marca,
                "codigo_color": codigo_color,
                "descripcion": descripcion,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "proveedor": proveedor
            }
            self.inventario.append(hilo)
            self.contador_id += 1

            print(f"\nHilo guardado. ID: {hilo['id']}")
            self.guardar_todo()
             # Reordenar y guardar el inventario actualizado automáticamente
            self.inventario = self.ordenar_por_codigo_color(self.inventario)
            self.inventario = self.ordenar_por_marca_con_menos_stock(self.inventario)
            self.inventario = self.ordenar_por_tipo(self.inventario)
            self.guardar_todo()


    def buscar_hilo(self):
        Utilidades.limpiar_pantalla()
        print("=== Buscar Hilo ===")

        marca = input("Ingrese la marca (o deje vacío para omitir): ").strip().lower()
        codigo_color = input("Ingrese el código de color (o deje vacío para omitir): ").strip().lower()

        resultados = self.inventario

    # Filtrar por marca si se indicó
        if marca:
            resultados = [h for h in resultados if marca in h["marca"].lower()]

    # Filtrar por código si se indicó
        if codigo_color:
            resultados = [h for h in resultados if codigo_color in str(h["codigo_color"]).lower()]

        if resultados:
            print(f"\nResultados encontrados ({len(resultados)}):\n")
            for h in resultados:
                print(f"ID:{h['id']} | Marca:{h['marca']} | Código:{h['codigo_color']} | "
                        f"Descripción:{h['descripcion']} | Cantidad:{h['cantidad']} | "
                        f"Precio:Q{h['precio_unitario']} | Proveedor:{h['proveedor']}")
        else:
            print("No se encontraron hilos con los criterios ingresados.")

    def busqueda_avanzada(self):
        Utilidades.limpiar_pantalla()
        print("=== BÚSQUEDA AVANZADA ===")
        print("1. Búsqueda lineal por código")
        print("2. Búsqueda binaria por código (requiere lista ordenada)")
        print("3. Búsqueda por hashing (tabla de dispersión)")
        print("4. Volver")
        op = input("Elegí una opción (1-4): ").strip()

        if op == "4":
            return

        marca = input("Ingrese la marca del hilo: ").strip().lower()
        codigo = input("Ingrese el código de color: ").strip().lower()

        # Filtrar solo los hilos de esa marca
        inventario_filtrado = [h for h in self.inventario if h["marca"].lower() == marca]
        if not inventario_filtrado:
            print(f"No se encontraron hilos de la marca '{marca}'.")
            return

        res = None

        # BÚSQUEDA LINEAL
        if op == "1":
            for h in inventario_filtrado:
                if str(h["codigo_color"]).lower() == codigo:
                    res = h
                    break

        # BÚSQUEDA BINARIA
        elif op == "2":
            lista_ordenada = sorted(inventario_filtrado, key=lambda x: str(x["codigo_color"]).lower())
            izq, der = 0, len(lista_ordenada) - 1
            while izq <= der:
                mid = (izq + der) // 2
                if str(lista_ordenada[mid]["codigo_color"]).lower() == codigo:
                    res = lista_ordenada[mid]
                    break
                elif str(lista_ordenada[mid]["codigo_color"]).lower() < codigo:
                    izq = mid + 1
                else:
                    der = mid - 1

        # BÚSQUEDA HASH
        elif op == "3":
            tabla = {str(h["codigo_color"]).lower(): h for h in inventario_filtrado}
            res = tabla.get(codigo)

        else:
            print("Opción inválida.")
            return

        # Resultado
        if res:
            print("\n--- Hilo encontrado ---")
            print(f"ID: {res['id']} | Marca: {res['marca']} | Código: {res['codigo_color']} | "
                f"Descripción: {res['descripcion']} | Cantidad: {res['cantidad']} | "
                f"Precio: Q{res['precio_unitario']} | Proveedor: {res['proveedor']}")
        else:
            print(f"No se encontró el hilo con el código '{codigo}' en la marca '{marca}'.")


    def modificar_hilo(self):
        Utilidades.limpiar_pantalla()
        codigo = input("Código de color del hilo a modificar: ").strip()

        for h in self.inventario:
            if h["codigo_color"] == codigo:
                print(f"Hilo: {h['descripcion']}")
                nueva_marca = input(f"Nueva marca ({h['marca']}): ").strip() or h["marca"]
                nueva_desc = input(f"Nueva descripción ({h['descripcion']}): ").strip() or h["descripcion"]

                try:
                    nueva_cantidad = input(f"Nueva cantidad ({h['cantidad']}): ").strip()
                    if nueva_cantidad:
                        h["cantidad"] = int(nueva_cantidad)
                        self.avisar_stock_bajo(h)
                    nuevo_precio = input(f"Nuevo precio ({h['precio_unitario']}): ").strip()
                    if nuevo_precio:
                        h["precio_unitario"] = float(nuevo_precio)
                except ValueError:
                    print("Dato inválido, se mantiene lo anterior.")

                nuevo_prov = input(f"Nuevo proveedor ({h['proveedor']}): ").strip() or h["proveedor"]
                h.update({"marca": nueva_marca, "descripcion": nueva_desc, "proveedor": nuevo_prov})
                print("Listo, cambios guardados.")
                self.guardar_todo()
                return
        print("Código no encontrado")

    def eliminar_hilo(self):
        codigo = input("Código de color del hilo a eliminar: ").strip()
        for h in self.inventario:
            if h["codigo_color"] == codigo:
                if h["cantidad"] == 0:
                    self.inventario.remove(h)
                    print("Hilo eliminado.")
                    self.guardar_todo()
                else:
                    print("No se puede eliminar: todavía hay unidades.")
                return
        print("Código no encontrado")

    # ---- Compras y Ventas ----
    def registrar_compra(self):
        while True:
            print("\n--- Registrar compra/reabastecimiento ---")
            codigo = input("Código de color (o 'salir'): ").strip()
            if codigo.lower() == "salir":
                print("\nRegresando al menú...")
                break
            cantidad = Utilidades.leer_entero("Cantidad comprada: ", minimo=1)
            costo_unitario = Utilidades.leer_flotante("Costo por unidad: ", minimo=0.0)

            for h in self.inventario:
                if h["codigo_color"] == codigo:
                    h["cantidad"] += cantidad
                    self.avisar_stock_bajo(h)
                    self.historial_compras.append({
                        "codigo_color": codigo,
                        "marca": h["marca"],
                        "descripcion": h["descripcion"],
                        "cantidad": cantidad,
                        "costo_unitario": costo_unitario,
                        "total": round(cantidad * costo_unitario, 2)
                    })
                    print("Compra guardada y stock actualizado.")
                    # Reordenar inventario automáticamente tras registrar una compra
                    self.inventario = self.ordenar_por_codigo_color(self.inventario)
                    self.inventario = self.ordenar_por_marca_con_menos_stock(self.inventario)
                    self.inventario = self.ordenar_por_tipo(self.inventario)
                    self.guardar_todo()
                    break
            else:
                print("Código no encontrado")

    def registrar_venta(self):
        while True:
            print("\n--- Registrar venta ---")
            codigo = input("Código de color (o 'salir'): ").strip()
            if codigo.lower() == "salir":
                print("\nRegresando al menú...")
                break

            for h in self.inventario:
                if h["codigo_color"] == codigo:
                    print(f"Disponible: {h['cantidad']} unidades")
                    cantidad = Utilidades.leer_entero("Cantidad vendida: ", minimo=1)
                    if cantidad > h["cantidad"]:
                        print("No te alcanza el stock para esa venta.")
                        break

                    h["cantidad"] -= cantidad
                    self.avisar_stock_bajo(h)

                    total = round(cantidad * h["precio_unitario"], 2)
                    self.historial_ventas.append({
                        "codigo_color": codigo,
                        "marca": h["marca"],
                        "descripcion": h["descripcion"],
                        "cantidad": cantidad,
                        "total": total
                    })

                    print(f"Venta guardada. Total: Q{total:.2f}")
                    # Reordenar inventario automáticamente tras registrar una venta
                    self.inventario = self.ordenar_por_codigo_color(self.inventario)
                    self.inventario = self.ordenar_por_marca_con_menos_stock(self.inventario)
                    self.inventario = self.ordenar_por_tipo(self.inventario)
                    self.guardar_todo()
                    break
            else:
                print("Código no encontrado")

    # ---- Reportes ----
    def reportes(self):
        print("\n--- Reportes y Consultas ---")
        print("1. Reporte general de inventario")
        print("2. Reporte por marca")
        print("3. Historial de ventas")
        print("4. Historial de compras")
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            self.mostrar_inventario()
        elif opcion == "2":
            marca = input("Marca a consultar: ").lower().strip()
            encontrados = [h for h in self.inventario if marca in h["marca"].lower()]
            if encontrados:
                for h in encontrados:
                    print(f"Marca:{h['marca']} | Código:{h['codigo_color']} | Desc:{h['descripcion']} | "
                          f"Cantidad:{h['cantidad']} | Precio:Q{h['precio_unitario']}")
            else:
                print("No hay hilos de esa marca.")
        elif opcion == "3":
            print("\n--- Historial de Ventas ---")
            if not self.historial_ventas:
                print("Aún no hay ventas.")
            else:
                for v in self.historial_ventas:
                    print(f"{v['marca']} | {v['codigo_color']} | {v['descripcion']} | {v['cantidad']} | Q{v['total']:.2f}")
        elif opcion == "4":
            print("\n--- Historial de Compras ---")
            if not self.historial_compras:
                print("Aún no hay compras.")
            else:
                for c in self.historial_compras:
                    print(f"{c['marca']} | {c['codigo_color']} | {c['descripcion']} | {c['cantidad']} | Q{c['total']:.2f}")
        else:
            print("Opción no válida.")

    def mostrar_inventario(self):
        Utilidades.limpiar_pantalla()
        print("=== Inventario Completo ===\n")
        if not self.inventario:
            print("No hay hilos registrados.")
        else:
            print(f"{'ID':<4} {'Marca':<15} {'Código':<10} {'Descripción':<20} {'Cant.':<7} {'Precio(Q)':<10} {'Proveedor'}")
            print("-" * 80)
            for h in self.inventario:
                print(f"{h['id']:<4} {h['marca']:<15} {h['codigo_color']:<10} {h['descripcion']:<20} "
                      f"{h['cantidad']:<7} {h['precio_unitario']:<10.2f} {h['proveedor']}")
            print(f"\nTotal de hilos: {len(self.inventario)}")

    #  MÉTODOS DE ORDENAMIENTO AUTOMÁTICO DEL INVENTARIO
    # QUICK SORT

    def ordenar_por_codigo_color(self, inventario):
        if not inventario:
            return inventario

        # 1 Agrupar hilos por marca
        grupos = {}
        for hilo in inventario:
            marca = hilo["marca"]
            grupos.setdefault(marca, []).append(hilo)

        inventario_ordenado = []

        # 2️ Ordenar los códigos de color dentro de cada grupo (Quick Sort)
        for marca, lista in sorted(grupos.items(), key=lambda x: x[0].lower()):
            lista_ordenada = self._quick_sort_codigo(lista)
            inventario_ordenado.extend(lista_ordenada)

        return inventario_ordenado

    # Función auxiliar interna: aplica Quick Sort recursivo dentro de cada marca
    def _quick_sort_codigo(self, lista):
        if len(lista) <= 1:
            return lista
        pivote = lista[len(lista) // 2]
        try:
            p_color = int(pivote["codigo_color"])
        except ValueError:
            p_color = 0

        menores, iguales, mayores = [], [], []
        for x in lista:
            try:
                color = int(x["codigo_color"])
            except ValueError:
                color = 0
            if color < p_color:
                menores.append(x)
            elif color == p_color:
                iguales.append(x)
            else:
                mayores.append(x)

        return (self._quick_sort_codigo(menores) +
                iguales +
                self._quick_sort_codigo(mayores))

    # MÉTODO 2: SELECTION SORT POR MARCA CON MENOR STOCK
    def ordenar_por_marca_con_menos_stock(self, inventario):
        # Calcular total de unidades por marca
        resumen = {}
        for hilo in inventario:
            marca = hilo["marca"]
            cantidad = int(hilo["cantidad"])
            resumen[marca] = resumen.get(marca, 0) + cantidad

        # Crear lista auxiliar con total_marca
        lista_aux = [
            {**h, "total_marca": resumen[h["marca"]]} for h in inventario
        ]

        # Aplicar Selection Sort según total_marca
        n = len(lista_aux)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if lista_aux[j]["total_marca"] < lista_aux[min_idx]["total_marca"]:
                    min_idx = j
            lista_aux[i], lista_aux[min_idx] = lista_aux[min_idx], lista_aux[i]

        # Eliminar el campo auxiliar antes de devolver la lista
        for h in lista_aux:
            del h["total_marca"]

        return lista_aux

    # MÉTODO 3: SHELL SORT POR TIPO DE HILO

    def ordenar_por_tipo(self, inventario):
        lista_ordenada = inventario[:]
        n = len(lista_ordenada)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = lista_ordenada[i]
                j = i
                while j >= gap and lista_ordenada[j - gap]["descripcion"].lower() > temp["descripcion"].lower():
                    lista_ordenada[j] = lista_ordenada[j - gap]
                    j -= gap
                lista_ordenada[j] = temp
            gap //= 2
        return lista_ordenada


# SISTEMA (login + menús)
class SistemaDeInventario:
    def __init__(self, archivo_excel=NOMBRE_ARCHIVO, permitir_venta_empleado=PERMITIR_VENTA_EMPLEADO):
        self.excel = GestorExcel(archivo_excel)
        self.excel.asegurar_estructura()
        self.excel.reparar_estructura()
        self.inventario = InventarioHilos(self.excel, stock_minimo=STOCK_MINIMO)
        self.sesion = SesionUsuario(self.excel)
        self.usuarios = self._cargar_usuarios()
        self.permitir_venta_empleado = permitir_venta_empleado

    def _cargar_usuarios(self):
        return [{"usuario": f[0], "password": f[1], "rol": str(f[2]).lower()} for f in self.excel.cargar_hoja(HOJA_USUARIOS)]

    def iniciar_sesion(self):
        print("=== INICIO DE SESIÓN ===")
        while True:
            usr = input("Usuario: ").strip()
            pwd = input("Contraseña: ").strip()
            for u in self.usuarios:
                if u["usuario"] == usr and u["password"] == pwd:
                    print(f"\n¡Bienvenido, {usr}! Rol: {u['rol']}\n")
                    id_sesion = self.sesion.abrir_sesion(usr, u["rol"])
                    return u["rol"], id_sesion
            print("Usuario o contraseña incorrectos\n")

    # ---- Menú Admin (completo) ----
    def menu_admin(self, id_sesion):
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
            print("9. Búsqueda avanzada")
            print("10. Salir")
            opcion = input("Elegí una opción: ").strip()

            if opcion == "1":
                self.inventario.registrar_hilo()
            elif opcion == "2":
                self.inventario.buscar_hilo()
            elif opcion == "3":
                self.inventario.modificar_hilo()
            elif opcion == "4":
                self.inventario.eliminar_hilo()
            elif opcion == "5":
                self.inventario.registrar_compra()
            elif opcion == "6":
                self.inventario.registrar_venta()
            elif opcion == "7":
                self.inventario.reportes()
            elif opcion == "8":
                self.inventario.mostrar_inventario()
            elif opcion == "9":
                self.inventario.busqueda_avanzada()
            elif opcion == "10":
                self.sesion.cerrar_sesion(id_sesion)
                print("\nsesión cerrada. Nos vemos")
                break
            else:
                print("Esa opción no existe, prueba")

    # ---- Menú Empleado (completo) ----
    def menu_empleado(self, id_sesion):
        while True:
            print("1. Buscar hilo")
            print("2. Búsqueda avanzada")  
            print("3. Registrar venta")
            print("4. Reportes y consultas")
            print("5. Mostrar inventario completo")
            print("6. Salir")
            opcion = input("Elegí una opción: ").strip()

            if opcion == "1":
                self.inventario.buscar_hilo()
            elif opcion == "2":
                self.inventario.busqueda_avanzada()
            elif opcion == "3":
                if self.permitir_venta_empleado:
                    self.inventario.registrar_venta()
                else:
                    print("Por ahora, ventas solo las hace el admin.")
            elif opcion == "4":
                self.inventario.reportes()
            elif opcion == "5":
                self.inventario.mostrar_inventario()
            elif opcion == "6":
                self.sesion.cerrar_sesion(id_sesion)
                print("\nSesión cerrada. ¡Gracias!")
                break
            else:
                print("Esa opción no existe, probá otra.")

    # ---- Arranque ----
    def ejecutar(self):
        rol, id_sesion = self.iniciar_sesion()
        if rol == "admin":
            self.menu_admin(id_sesion)
        else:
            self.menu_empleado(id_sesion)


# MAIN
if __name__ == "__main__":
    app = SistemaDeInventario()
    app.ejecutar()