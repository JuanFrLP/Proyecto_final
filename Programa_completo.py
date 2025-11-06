from openpyxl import Workbook, load_workbook
import customtkinter as ctk
from tkinter import messagebox
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
    def leer_entero_str(valor, minimo=None):
        try:
            n = int(valor)
            if minimo is not None and n < minimo:
                return None
            return n
        except:
            return None

    @staticmethod
    def leer_float_str(valor, minimo=None):
        try:
            f = float(valor)
            if minimo is not None and f < minimo:
                return None
            return f
        except:
            return None


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
                # Elimina todas las filas excepto la primera
                hoja.delete_rows(2, hoja.max_row - 1)

        wb.save(self.nombre_archivo)

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
        id_sesion = hoja.max_row  # correlativo
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

        # --- Asignar ID y ordenar automáticamente ---
        self.contador_id = (max((h["id"] for h in self.inventario), default=0) + 1)
        if self.inventario:
            self.inventario = self.ordenar_por_codigo_color(self.inventario)
            self.inventario = self.ordenar_por_marca_con_menos_stock(self.inventario)
            self.inventario = self.ordenar_por_tipo(self.inventario)
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

    # ---- Alertas ----
    def avisar_stock_bajo_gui(self, hilo):
        if hilo["cantidad"] <= self.stock_minimo:
            messagebox.showwarning("Stock bajo",
                                   f"Código: {hilo['codigo_color']}\n"
                                   f"Tipo: {hilo['descripcion']}\n"
                                   f"Unidades: {hilo['cantidad']}")

    # ---- Apoyo de negocio (sin inputs/prints) ----
    def existe_marca_codigo(self, marca, codigo):
        return any(h["marca"].lower() == marca.lower() and str(h["codigo_color"]) == str(codigo)
                   for h in self.inventario)

    def obtener_por_marca_codigo(self, marca, codigo):
        for h in self.inventario:
            if h["marca"].lower() == marca.lower() and str(h["codigo_color"]) == str(codigo):
                return h
        return None

    # ---- CRUD de Hilos (usados por la GUI) ----
    def registrar_hilo_gui(self, marca, tipo, codigo_color, cantidad, precio_unitario, proveedor):
        # Validar duplicado en misma marca
        if self.existe_marca_codigo(marca, codigo_color):
            return False, "Ese código de color ya existe para esta marca."

        hilo = {
            "id": self.contador_id,
            "marca": marca,
            "codigo_color": str(codigo_color),
            "descripcion": tipo,  # mapeo UI "Tipo" -> Excel "Descripción"
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "proveedor": proveedor
        }
        self.inventario.append(hilo)
        self.contador_id += 1

        # Reordenamientos y guardado
        self.inventario = self.ordenar_por_codigo_color(self.inventario)
        self.inventario = self.ordenar_por_marca_con_menos_stock(self.inventario)
        self.inventario = self.ordenar_por_tipo(self.inventario)
        self.guardar_todo()
        return True, f"Hilo guardado. ID: {hilo['id']}"

    def modificar_hilo_gui(self, marca, codigo_color, nueva_marca=None, nuevo_tipo=None,
                           nueva_cantidad=None, nuevo_precio=None, nuevo_proveedor=None):
        h = self.obtener_por_marca_codigo(marca, codigo_color)
        if not h:
            return False, "No se encontró el hilo con esa Marca y Código."

        # Si cambia la marca y/o el código, validar que no choque con otro existente
        destino_marca = nueva_marca.strip() if (nueva_marca is not None and nueva_marca.strip() != "") else h["marca"]
        destino_codigo = str(codigo_color)  # no estamos cambiando código en este formulario

        if (destino_marca.lower() != h["marca"].lower()) and self.existe_marca_codigo(destino_marca, destino_codigo):
            return False, "Ya existe ese código en la nueva marca."

        h["marca"] = destino_marca
        if (nuevo_tipo is not None) and nuevo_tipo.strip() != "":
            h["descripcion"] = nuevo_tipo.strip()
        if (nueva_cantidad is not None) and nueva_cantidad != "":
            n = Utilidades.leer_entero_str(nueva_cantidad, minimo=0)
            if n is None:
                return False, "Cantidad inválida."
            h["cantidad"] = n
            self.avisar_stock_bajo_gui(h)
        if (nuevo_precio is not None) and nuevo_precio != "":
            f = Utilidades.leer_float_str(nuevo_precio, minimo=0.0)
            if f is None:
                return False, "Precio inválido."
            h["precio_unitario"] = f
        if (nuevo_proveedor is not None) and nuevo_proveedor.strip() != "":
            h["proveedor"] = nuevo_proveedor.strip()

        # Ordenar/guardar
        self.inventario = self.ordenar_por_codigo_color(self.inventario)
        self.inventario = self.ordenar_por_marca_con_menos_stock(self.inventario)
        self.inventario = self.ordenar_por_tipo(self.inventario)
        self.guardar_todo()
        return True, "Cambios guardados."

    def eliminar_hilo_gui(self, marca, codigo_color):
        h = self.obtener_por_marca_codigo(marca, codigo_color)
        if not h:
            return False, "No se encontró el hilo con esa Marca y Código."
        if h["cantidad"] != 0:
            return False, "No se puede eliminar: aún hay unidades."
        self.inventario.remove(h)
        self.guardar_todo()
        return True, "Hilo eliminado."

    def registrar_compra_gui(self, marca, codigo_color, cantidad, costo_unitario):
        h = self.obtener_por_marca_codigo(marca, codigo_color)
        if not h:
            return False, "No se encontró el hilo con esa Marca y Código."
        if cantidad < 1:
            return False, "Cantidad inválida."

        h["cantidad"] += cantidad
        self.historial_compras.append({
            "codigo_color": str(codigo_color),
            "marca": h["marca"],
            "descripcion": h["descripcion"],
            "cantidad": cantidad,
            "costo_unitario": costo_unitario,
            "total": round(cantidad * costo_unitario, 2)
        })
        self.avisar_stock_bajo_gui(h)

        # Ordenar/guardar
        self.inventario = self.ordenar_por_codigo_color(self.inventario)
        self.inventario = self.ordenar_por_marca_con_menos_stock(self.inventario)
        self.inventario = self.ordenar_por_tipo(self.inventario)
        self.guardar_todo()
        return True, "Compra registrada y stock actualizado."

    def registrar_venta_gui(self, marca, codigo_color, cantidad):
        h = self.obtener_por_marca_codigo(marca, codigo_color)
        if not h:
            return False, "No se encontró el hilo con esa Marca y Código."
        if cantidad < 1:
            return False, "Cantidad inválida."
        if cantidad > h["cantidad"]:
            return False, "No alcanza el stock para esa venta."

        h["cantidad"] -= cantidad
        total = round(cantidad * h["precio_unitario"], 2)
        self.historial_ventas.append({
            "codigo_color": str(codigo_color),
            "marca": h["marca"],
            "descripcion": h["descripcion"],
            "cantidad": cantidad,
            "total": total
        })
        self.avisar_stock_bajo_gui(h)

        # Ordenar/guardar
        self.inventario = self.ordenar_por_codigo_color(self.inventario)
        self.inventario = self.ordenar_por_marca_con_menos_stock(self.inventario)
        self.inventario = self.ordenar_por_tipo(self.inventario)
        self.guardar_todo()
        return True, f"Venta registrada. Total: Q{total:.2f}"

    # ---- Reportes simples (devuelven listas) ----
    def reporte_inventario(self):
        return list(self.inventario)

    def reporte_ventas(self):
        return list(self.historial_ventas)

    def reporte_compras(self):
        return list(self.historial_compras)

    # ORDENAMIENTOS
    def ordenar_por_codigo_color(self, inventario):
        if not inventario:
            return inventario

        grupos = {}
        for hilo in inventario:
            marca = hilo["marca"]
            grupos.setdefault(marca, []).append(hilo)

        inventario_ordenado = []
        for marca, lista in sorted(grupos.items(), key=lambda x: x[0].lower()):
            lista_ordenada = self._quick_sort_codigo(lista)
            inventario_ordenado.extend(lista_ordenada)
        return inventario_ordenado

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

    def ordenar_por_marca_con_menos_stock(self, inventario):
        resumen = {}
        for hilo in inventario:
            marca = hilo["marca"]
            cantidad = int(hilo["cantidad"])
            resumen[marca] = resumen.get(marca, 0) + cantidad

        lista_aux = [{**h, "total_marca": resumen[h["marca"]]} for h in inventario]

        n = len(lista_aux)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if lista_aux[j]["total_marca"] < lista_aux[min_idx]["total_marca"]:
                    min_idx = j
            lista_aux[i], lista_aux[min_idx] = lista_aux[min_idx], lista_aux[i]

        for h in lista_aux:
            del h["total_marca"]

        return lista_aux

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


# SISTEMA (usuarios + sesión)
class SistemaDeInventario:
    def __init__(self, archivo_excel=NOMBRE_ARCHIVO, permitir_venta_empleado=PERMITIR_VENTA_EMPLEADO):
        self.excel = GestorExcel(archivo_excel)
        self.excel.asegurar_estructura()
        self.excel.reparar_estructura()
        self.inventario = InventarioHilos(self.excel, stock_minimo=STOCK_MINIMO)
        self.sesion = SesionUsuario(self.excel)
        self.usuarios = self._cargar_usuarios()
        self.permitir_venta_empleado = permitir_venta_empleado
        self.id_sesion_activa = None
        self.usuario_actual = None  # dict con usuario y rol

    def _cargar_usuarios(self):
        return [{"usuario": f[0], "password": f[1], "rol": str(f[2]).lower()}
                for f in self.excel.cargar_hoja(HOJA_USUARIOS)]

    def validar_credenciales(self, usr, pwd):
        for u in self.usuarios:
            if u["usuario"] == usr and u["password"] == pwd:
                return u
        return None

    def abrir_sesion(self, usuario_dict):
        self.usuario_actual = usuario_dict
        self.id_sesion_activa = self.sesion.abrir_sesion(usuario_dict["usuario"], usuario_dict["rol"])

    def cerrar_sesion(self):
        if self.id_sesion_activa is not None:
            self.sesion.cerrar_sesion(self.id_sesion_activa)
        self.id_sesion_activa = None
        self.usuario_actual = None


# INTERFAZ GRÁFICA (CustomTkinter)
class AppGUI:
    def __init__(self):
        # Estilos
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Sistema
        self.sys = SistemaDeInventario()

        # Ventana
        self.root = ctk.CTk()
        self.root.title("Tienda de Hilos Arcoíris")
        try:
            self.root.state("zoomed")
        except:
            self.root.geometry("1200x700")

        # Frames
        self.frame_actual = None
        self._build_login()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    # ---------- Layout helpers ----------
    def clear_frame(self):
        if self.frame_actual is not None:
            self.frame_actual.pack_forget()
            self.frame_actual.destroy()
        self.frame_actual = ctk.CTkFrame(self.root)
        self.frame_actual.pack(expand=True, fill="both")

    def header(self, parent, titulo="Tienda de Hilos Arcoíris"):
        encabezado = ctk.CTkFrame(parent, height=80, fg_color="#1e1e1e")
        encabezado.pack(fill="x")
        lbl = ctk.CTkLabel(encabezado, text=titulo, font=("Arial", 32, "bold"), text_color="#ffcc70")
        lbl.pack(pady=15)
        return encabezado

    def row_entry(self, parent, etiqueta, var: ctk.StringVar, width=280):
        cont = ctk.CTkFrame(parent, fg_color="transparent")
        cont.pack(pady=8)
        lbl = ctk.CTkLabel(cont, text=etiqueta, font=("Arial", 16))
        lbl.pack(side="left", padx=10)
        ent = ctk.CTkEntry(cont, textvariable=var, width=width, height=35)
        ent.pack(side="left")
        return ent

    def boton_volver(self, parent, destino):
        ctk.CTkButton(parent, text="↩ Volver", command=destino, width=250, height=40).pack(pady=10)

    # ---------- Pantallas ----------
    def _build_login(self):
        self.clear_frame()
        self.header(self.frame_actual, "Tienda de Hilos Arcoíris")

        login_frame = ctk.CTkFrame(self.frame_actual)
        login_frame.pack(expand=True, ipadx=20, ipady=20)

        ctk.CTkLabel(login_frame, text="Inicio de sesión", font=("Arial", 24, "bold")).pack(pady=20)

        v_user = ctk.StringVar()
        v_pass = ctk.StringVar()
        self.row_entry(login_frame, "Usuario", v_user)
        self.row_entry(login_frame, "Contraseña", v_pass)

        def hacer_login():
            usr = v_user.get().strip()
            pwd = v_pass.get().strip()
            u = self.sys.validar_credenciales(usr, pwd)
            if not u:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
                return
            self.sys.abrir_sesion(u)
            messagebox.showinfo("Bienvenido", f"Sesión iniciada como {u['rol']}.")
            self._build_menu()

        ctk.CTkButton(login_frame, text="Entrar", width=220, height=40, command=hacer_login).pack(pady=15)

    def _build_menu(self):
        self.clear_frame()
        self.header(self.frame_actual)

        tipo = "ADMINISTRADOR" if self.sys.usuario_actual["rol"] == "admin" else "EMPLEADO"
        ctk.CTkLabel(self.frame_actual, text=f"Usuario: {self.sys.usuario_actual['usuario']}  |  Rol: {tipo}",
                     font=("Arial", 16, "italic"), text_color="lightblue").pack(pady=(12, 2))

        ctk.CTkLabel(self.frame_actual, text="MENÚ PRINCIPAL", font=("Arial", 26, "bold")).pack(pady=10)

        # Opciones según rol
        opciones = []
        if self.sys.usuario_actual["rol"] == "admin":
            opciones = [
                ("Registrar nuevo hilo", self.ui_registrar_hilo),
                ("Buscar hilo", self.ui_buscar_hilo),
                ("Modificar información", self.ui_modificar_hilo),
                ("Eliminar hilo", self.ui_eliminar_hilo),
                ("Registrar compra / reabastecimiento", self.ui_registrar_compra),
                ("Registrar venta", self.ui_registrar_venta),
                ("Reportes y consultas", self.ui_reportes),
                ("Mostrar inventario completo", self.ui_inventario),
                ("Cerrar sesión y salir", self.on_close)
            ]
        else:
            opciones = [
                ("Buscar hilo", self.ui_buscar_hilo),
                ("Registrar venta", self.ui_registrar_venta if PERMITIR_VENTA_EMPLEADO else self._no_permitido),
                ("Reportes y consultas", self.ui_reportes),
                ("Mostrar inventario completo", self.ui_inventario),
                ("Cerrar sesión y salir", self.on_close)
            ]

        botones = ctk.CTkFrame(self.frame_actual, fg_color="transparent")
        botones.pack(pady=10)
        for texto, cmd in opciones:
            ctk.CTkButton(botones, text=texto, command=cmd, width=420, height=42, font=("Arial", 16)).pack(pady=7)

        ctk.CTkButton(self.frame_actual, text="↩ Cerrar sesión", fg_color="#444", hover_color="#666",
                      command=self._logout, width=280, height=38).pack(pady=10)

    def _logout(self):
        self.sys.cerrar_sesion()
        self._build_login()

    def _no_permitido(self):
        messagebox.showwarning("Restringido", "Ventas solo permitidas al administrador.")

    # ---------- Subpantallas ----------
    def ui_registrar_hilo(self):
        self.clear_frame()
        self.header(self.frame_actual, "Registrar nuevo hilo")
        form = ctk.CTkFrame(self.frame_actual)
        form.pack(pady=10)

        v_marca = ctk.StringVar()
        v_tipo = ctk.StringVar()          # se guarda en Excel como "Descripción"
        v_codigo = ctk.StringVar()
        v_cantidad = ctk.StringVar()
        v_precio = ctk.StringVar()
        v_proveedor = ctk.StringVar()

        self.row_entry(form, "Marca", v_marca)
        self.row_entry(form, "Tipo", v_tipo)
        self.row_entry(form, "Código de color", v_codigo)
        self.row_entry(form, "Cantidad", v_cantidad)
        self.row_entry(form, "Precio por unidad", v_precio)
        self.row_entry(form, "Proveedor", v_proveedor)

        def confirmar():
            datos = { "Marca": v_marca.get().strip(),
                      "Tipo": v_tipo.get().strip(),
                      "Código": v_codigo.get().strip(),
                      "Cantidad": v_cantidad.get().strip(),
                      "Precio": v_precio.get().strip(),
                      "Proveedor": v_proveedor.get().strip() }

            if any(v == "" for v in datos.values()):
                messagebox.showwarning("Atención", "Por favor llena todos los campos.")
                return

            n_cant = Utilidades.leer_entero_str(datos["Cantidad"], minimo=0)
            n_prec = Utilidades.leer_float_str(datos["Precio"], minimo=0.0)
            if n_cant is None or n_prec is None:
                messagebox.showwarning("Atención", "Cantidad o precio inválido.")
                return

            ok, msg = self.sys.inventario.registrar_hilo_gui(
                datos["Marca"], datos["Tipo"], datos["Código"], n_cant, n_prec, datos["Proveedor"]
            )
            if ok:
                messagebox.showinfo("Éxito", msg)
                self._build_menu()
            else:
                messagebox.showwarning("Atención", msg)

        ctk.CTkButton(form, text="Guardar hilo", command=confirmar, width=260, height=42).pack(pady=15)
        self.boton_volver(self.frame_actual, self._build_menu)

    def ui_buscar_hilo(self):
        self.clear_frame()
        self.header(self.frame_actual, "Buscar Hilo")
        form = ctk.CTkFrame(self.frame_actual)
        form.pack(pady=10)

        v_marca = ctk.StringVar()
        v_codigo = ctk.StringVar()
        self.row_entry(form, "Marca", v_marca)
        self.row_entry(form, "Código de color", v_codigo)

        result_box = ctk.CTkTextbox(self.frame_actual, width=900, height=220)
        result_box.pack(pady=10)

        def buscar():
            marca = v_marca.get().strip()
            codigo = v_codigo.get().strip()
            if marca == "" or codigo == "":
                messagebox.showwarning("Atención", "Llene Marca y Código.")
                return
            h = self.sys.inventario.obtener_por_marca_codigo(marca, codigo)
            result_box.delete("1.0", "end")
            if h:
                result_box.insert("end",
                    f"ID: {h['id']}\nMarca: {h['marca']}\nCódigo: {h['codigo_color']}\n"
                    f"Tipo: {h['descripcion']}\nCantidad: {h['cantidad']}\n"
                    f"Precio: Q{h['precio_unitario']:.2f}\nProveedor: {h['proveedor']}\n")
            else:
                result_box.insert("end", "No se encontró el hilo.")

        ctk.CTkButton(form, text="Buscar", command=buscar, width=220, height=40).pack(pady=12)
        self.boton_volver(self.frame_actual, self._build_menu)

    def ui_modificar_hilo(self):
        self.clear_frame()
        self.header(self.frame_actual, "Modificar Hilo")
        form = ctk.CTkFrame(self.frame_actual)
        form.pack(pady=10)

        v_marca = ctk.StringVar()
        v_codigo = ctk.StringVar()
        v_nueva_marca = ctk.StringVar()
        v_nuevo_tipo = ctk.StringVar()
        v_nueva_cantidad = ctk.StringVar()
        v_nuevo_precio = ctk.StringVar()
        v_nuevo_prov = ctk.StringVar()

        self.row_entry(form, "Marca (actual)", v_marca)
        self.row_entry(form, "Código de color (actual)", v_codigo)
        self.row_entry(form, "Nueva marca (opcional)", v_nueva_marca)
        self.row_entry(form, "Nuevo tipo (opcional)", v_nuevo_tipo)
        self.row_entry(form, "Nueva cantidad (opcional)", v_nueva_cantidad)
        self.row_entry(form, "Nuevo precio (opcional)", v_nuevo_precio)
        self.row_entry(form, "Nuevo proveedor (opcional)", v_nuevo_prov)

        def confirmar():
            m = v_marca.get().strip()
            c = v_codigo.get().strip()
            if m == "" or c == "":
                messagebox.showwarning("Atención", "Marca y Código actuales son obligatorios.")
                return

            ok, msg = self.sys.inventario.modificar_hilo_gui(
                m, c,
                nueva_marca=v_nueva_marca.get(),
                nuevo_tipo=v_nuevo_tipo.get(),
                nueva_cantidad=v_nueva_cantidad.get(),
                nuevo_precio=v_nuevo_precio.get(),
                nuevo_proveedor=v_nuevo_prov.get()
            )
            if ok:
                messagebox.showinfo("Éxito", msg)
                self._build_menu()
            else:
                messagebox.showwarning("Atención", msg)

        ctk.CTkButton(form, text="Guardar cambios", command=confirmar, width=260, height=42).pack(pady=15)
        self.boton_volver(self.frame_actual, self._build_menu)

    def ui_eliminar_hilo(self):
        self.clear_frame()
        self.header(self.frame_actual, "Eliminar Hilo")
        form = ctk.CTkFrame(self.frame_actual)
        form.pack(pady=10)

        v_marca = ctk.StringVar()
        v_codigo = ctk.StringVar()
        self.row_entry(form, "Marca", v_marca)
        self.row_entry(form, "Código de color", v_codigo)

        def confirmar():
            ok, msg = self.sys.inventario.eliminar_hilo_gui(v_marca.get().strip(), v_codigo.get().strip())
            if ok:
                messagebox.showinfo("Éxito", msg)
                self._build_menu()
            else:
                messagebox.showwarning("Atención", msg)

        ctk.CTkButton(form, text="Eliminar hilo", command=confirmar, width=240, height=40).pack(pady=12)
        self.boton_volver(self.frame_actual, self._build_menu)

    def ui_registrar_compra(self):
        self.clear_frame()
        self.header(self.frame_actual, "Registrar Compra / Reabastecimiento")
        form = ctk.CTkFrame(self.frame_actual)
        form.pack(pady=10)

        v_marca = ctk.StringVar()
        v_codigo = ctk.StringVar()
        v_cantidad = ctk.StringVar()
        v_costo = ctk.StringVar()

        self.row_entry(form, "Marca", v_marca)
        self.row_entry(form, "Código de color", v_codigo)
        self.row_entry(form, "Cantidad comprada", v_cantidad)
        self.row_entry(form, "Costo por unidad", v_costo)

        def confirmar():
            m = v_marca.get().strip()
            c = v_codigo.get().strip()
            cant = Utilidades.leer_entero_str(v_cantidad.get().strip(), minimo=1)
            costo = Utilidades.leer_float_str(v_costo.get().strip(), minimo=0.0)
            if any(x in (None, "") for x in [m, c, cant, costo]):
                messagebox.showwarning("Atención", "Complete los datos correctamente.")
                return
            ok, msg = self.sys.inventario.registrar_compra_gui(m, c, cant, costo)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self._build_menu()
            else:
                messagebox.showwarning("Atención", msg)

        ctk.CTkButton(form, text="Registrar compra", command=confirmar, width=240, height=40).pack(pady=12)
        self.boton_volver(self.frame_actual, self._build_menu)

    def ui_registrar_venta(self):
        self.clear_frame()
        self.header(self.frame_actual, "Registrar Venta")
        form = ctk.CTkFrame(self.frame_actual)
        form.pack(pady=10)

        v_marca = ctk.StringVar()
        v_codigo = ctk.StringVar()
        v_cantidad = ctk.StringVar()

        self.row_entry(form, "Marca", v_marca)
        self.row_entry(form, "Código de color", v_codigo)
        self.row_entry(form, "Cantidad vendida", v_cantidad)

        def confirmar():
            m = v_marca.get().strip()
            c = v_codigo.get().strip()
            cant = Utilidades.leer_entero_str(v_cantidad.get().strip(), minimo=1)
            if any(x in (None, "") for x in [m, c, cant]):
                messagebox.showwarning("Atención", "Complete los datos correctamente.")
                return
            ok, msg = self.sys.inventario.registrar_venta_gui(m, c, cant)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self._build_menu()
            else:
                messagebox.showwarning("Atención", msg)

        ctk.CTkButton(form, text="Registrar venta", command=confirmar, width=240, height=40).pack(pady=12)
        self.boton_volver(self.frame_actual, self._build_menu)

    def ui_reportes(self):
        self.clear_frame()
        self.header(self.frame_actual, "Reportes y Consultas")
        cont = ctk.CTkFrame(self.frame_actual)
        cont.pack(pady=10)

        # Botones de reporte
        btns = ctk.CTkFrame(cont, fg_color="transparent")
        btns.pack(pady=6)
        out = ctk.CTkTextbox(self.frame_actual, width=1000, height=350)
        out.pack(pady=10)

        def rep_inv():
            out.delete("1.0", "end")
            data = self.sys.inventario.reporte_inventario()
            if not data:
                out.insert("end", "No hay hilos registrados.\n")
                return
            for h in data:
                out.insert("end", f"ID:{h['id']} | Marca:{h['marca']} | Código:{h['codigo_color']} | "
                                  f"Tipo:{h['descripcion']} | Cant:{h['cantidad']} | "
                                  f"Precio:Q{h['precio_unitario']:.2f} | Prov:{h['proveedor']}\n")

        def rep_ven():
            out.delete("1.0", "end")
            data = self.sys.inventario.reporte_ventas()
            if not data:
                out.insert("end", "Aún no hay ventas.\n")
                return
            for v in data:
                out.insert("end", f"{v['marca']} | {v['codigo_color']} | {v['descripcion']} | "
                                  f"{v['cantidad']} | Total Q{v['total']:.2f}\n")

        def rep_com():
            out.delete("1.0", "end")
            data = self.sys.inventario.reporte_compras()
            if not data:
                out.insert("end", "Aún no hay compras.\n")
                return
            for c in data:
                out.insert("end", f"{c['marca']} | {c['codigo_color']} | {c['descripcion']} | "
                                  f"{c['cantidad']} | Costo Q{c['costo_unitario']:.2f} | "
                                  f"Total Q{c['total']:.2f}\n")

        ctk.CTkButton(btns, text="Inventario", command=rep_inv, width=180, height=34).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Historial Ventas", command=rep_ven, width=180, height=34).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Historial Compras", command=rep_com, width=180, height=34).pack(side="left", padx=6)

        self.boton_volver(self.frame_actual, self._build_menu)

    def ui_inventario(self):
        self.clear_frame()
        self.header(self.frame_actual, "Inventario Completo")

        out = ctk.CTkTextbox(self.frame_actual, width=1100, height=460)
        out.pack(pady=10)

        data = self.sys.inventario.reporte_inventario()
        if not data:
            out.insert("end", "No hay hilos registrados.\n")
        else:
            out.insert("end", f"{'ID':<4} {'Marca':<15} {'Código':<10} {'Tipo':<18} {'Cant.':<7} {'Precio(Q)':<10} {'Proveedor'}\n")
            out.insert("end", "-" * 90 + "\n")
            for h in data:
                out.insert("end",
                           f"{h['id']:<4} {h['marca']:<15} {h['codigo_color']:<10} {h['descripcion']:<18} "
                           f"{h['cantidad']:<7} {h['precio_unitario']:<10.2f} {h['proveedor']}\n")

        self.boton_volver(self.frame_actual, self._build_menu)

    # ---------- cierre ----------
    def on_close(self):
        # Cierra sesión si estaba abierta
        try:
            self.sys.cerrar_sesion()
        except:
            pass
        self.root.destroy()


# MAIN
if __name__ == "__main__":
    AppGUI()