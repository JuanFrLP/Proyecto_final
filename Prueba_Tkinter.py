import customtkinter as ctk
from tkinter import messagebox

# CONFIGURACIÓN GENERAL
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Tienda de Hilos Arcoíris")
ventana.state('zoomed')

# FUNCIÓN PARA CREAR ENCABEZADO GLOBAL
def crear_encabezado(frame_destino):
    encabezado = ctk.CTkFrame(frame_destino, height=80, fg_color="#1e1e1e")
    encabezado.pack(fill="x")

    titulo = ctk.CTkLabel(
        encabezado,
        text="Tienda de Hilos Arcoíris",
        font=("Arial", 32, "bold"),
        text_color="#ffcc70"
    )
    titulo.pack(pady=15)

# FRAME DE SELECCIÓN DE USUARIO
frame_usuario = ctk.CTkFrame(ventana)
frame_usuario.pack(expand=True, fill="both")

crear_encabezado(frame_usuario)

label_bienvenida = ctk.CTkLabel(
    frame_usuario,
    text="Seleccione tipo de usuario",
    font=("Arial", 24, "bold")
)
label_bienvenida.pack(pady=60)

usuario_actual = ctk.StringVar(value="")

def seleccionar_usuario(tipo):
    usuario_actual.set(tipo)
    frame_usuario.pack_forget()
    mostrar_menu()

btn_empleado = ctk.CTkButton(
    frame_usuario,
    text="Entrar como EMPLEADO",
    width=300,
    height=50,
    font=("Arial", 18),
    command=lambda: seleccionar_usuario("empleado")
)
btn_empleado.pack(pady=15)

btn_admin = ctk.CTkButton(
    frame_usuario,
    text="Entrar como ADMINISTRADOR",
    width=300,
    height=50,
    font=("Arial", 18),
    command=lambda: seleccionar_usuario("administrador")
)
btn_admin.pack(pady=15)

btn_salir = ctk.CTkButton(
    frame_usuario,
    text="Salir del sistema",
    width=300,
    height=45,
    font=("Arial", 16),
    fg_color="red",
    hover_color="#b30000",
    command=ventana.destroy
)
btn_salir.pack(pady=30)

# FRAMES PRINCIPALES
frame_menu = ctk.CTkFrame(ventana)
frame_submenu = ctk.CTkFrame(ventana)

# FUNCIONES PRINCIPALES
def mostrar_menu():
    frame_submenu.pack_forget()
    frame_menu.pack(expand=True, fill="both")

    for widget in frame_menu.winfo_children():
        widget.destroy()

    crear_encabezado(frame_menu)

    tipo = usuario_actual.get()
    label_usuario = ctk.CTkLabel(
        frame_menu,
        text=f"Usuario: {tipo.upper()}",
        font=("Arial", 18, "italic"),
        text_color="lightblue"
    )
    label_usuario.pack(pady=(20, 10))

    titulo = ctk.CTkLabel(frame_menu, text="MENÚ PRINCIPAL", font=("Arial", 28, "bold"))
    titulo.pack(pady=10)

    # Menú diferente según usuario
    if tipo == "empleado":
        opciones = [
            ("1. Buscar hilo", buscar_hilo),
            ("2. Registrar venta", registrar_venta),
            ("3. Reportes y consultas", reportes_consultas),
            ("4. Mostrar inventario completo", inventario_completo),
            ("5. Salir", ventana.destroy)
        ]
    elif tipo == "administrador":
        opciones = [
            ("1. Registrar nuevo hilo", registrar_hilo),
            ("2. Buscar hilo", buscar_hilo),
            ("3. Modificar información", modificar_hilo),
            ("4. Eliminar hilo", eliminar_hilo),
            ("5. Registrar compra/reabastecimiento", registrar_compra),
            ("6. Registrar venta", registrar_venta),
            ("7. Reportes y consultas", reportes_consultas),
            ("8. Mostrar inventario completo", inventario_completo),
            ("9. Salir", ventana.destroy)
        ]
    else:
        opciones = []

    for texto, comando in opciones:
        boton = ctk.CTkButton(frame_menu, text=texto, command=comando, width=400, height=40, font=("Arial", 16))
        boton.pack(pady=8)

    ctk.CTkButton(frame_menu, text="↩ Volver a selección de usuario",
                  fg_color="#444", hover_color="#666",
                  width=300, height=40,
                  command=volver_a_selector).pack(pady=15)

def volver_a_selector():
    frame_menu.pack_forget()
    frame_usuario.pack(expand=True, fill="both")

# SUBPANTALLAS DE PRUEBA
def registrar_hilo():
    frame_menu.pack_forget()
    frame_submenu.pack(expand=True, fill="both")
    for w in frame_submenu.winfo_children():
        w.destroy()

    crear_encabezado(frame_submenu)
    titulo = ctk.CTkLabel(frame_submenu, text="Registrar nuevo hilo", font=("Arial", 26, "bold"))
    titulo.pack(pady=20)

    campos = {
        "Marca": ctk.StringVar(),
        "Tipo": ctk.StringVar(),
        "Código de color": ctk.StringVar(),
        "Cantidad": ctk.StringVar(),
        "Precio por unidad": ctk.StringVar()
    }

    for etiqueta, var in campos.items():
        cont = ctk.CTkFrame(frame_submenu, fg_color="transparent")
        cont.pack(pady=10)
        lbl = ctk.CTkLabel(cont, text=etiqueta, font=("Arial", 16))
        lbl.pack(side="left", padx=10)
        ent = ctk.CTkEntry(cont, textvariable=var, width=250, height=35)
        ent.pack(side="left")

    def confirmar():
        datos = {c: v.get().strip() for c, v in campos.items()}
        if any(v == "" for v in datos.values()):
            messagebox.showwarning("Atención", "Por favor llena todos los campos.")
            return
        resumen = "\n".join([f"{k}: {v}" for k, v in datos.items()])
        messagebox.showinfo("Registro exitoso", f"Hilo registrado con los siguientes datos:\n\n{resumen}")
        mostrar_menu()

    ctk.CTkButton(frame_submenu, text="Guardar hilo", command=confirmar, width=250, height=40).pack(pady=20)
    ctk.CTkButton(frame_submenu, text="↩ Volver", command=mostrar_menu, width=250, height=40).pack(pady=10)


def buscar_hilo():
    frame_menu.pack_forget()
    frame_submenu.pack(expand=True, fill="both")
    for w in frame_submenu.winfo_children():
        w.destroy()

    crear_encabezado(frame_submenu)
    titulo = ctk.CTkLabel(frame_submenu, text="Buscar Hilo", font=("Arial", 26, "bold"))
    titulo.pack(pady=20)

    campos = {
        "Marca": ctk.StringVar(),
        "Código de color": ctk.StringVar()
    }

    for etiqueta, var in campos.items():
        cont = ctk.CTkFrame(frame_submenu, fg_color="transparent")
        cont.pack(pady=10)
        lbl = ctk.CTkLabel(cont, text=etiqueta, font=("Arial", 16))
        lbl.pack(side="left", padx=10)
        ent = ctk.CTkEntry(cont, textvariable=var, width=250, height=35)
        ent.pack(side="left")

    def confirmar():
        datos = {c: v.get().strip() for c, v in campos.items()}
        if any(v == "" for v in datos.values()):
            messagebox.showwarning("Atención", "Por favor llena ambos campos.")
            return
        messagebox.showinfo("Resultado", f"Buscando hilo:\nMarca: {datos['Marca']}\nCódigo: {datos['Código de color']}")
        mostrar_menu()

    ctk.CTkButton(frame_submenu, text="Buscar", command=confirmar, width=250, height=40).pack(pady=20)
    ctk.CTkButton(frame_submenu, text="↩ Volver", command=mostrar_menu, width=250, height=40).pack(pady=10)


def modificar_hilo():
    frame_menu.pack_forget()
    frame_submenu.pack(expand=True, fill="both")
    for w in frame_submenu.winfo_children():
        w.destroy()

    crear_encabezado(frame_submenu)
    titulo = ctk.CTkLabel(frame_submenu, text="Modificar Hilo", font=("Arial", 26, "bold"))
    titulo.pack(pady=20)

    campos = {
        "Marca": ctk.StringVar(),
        "Código de color": ctk.StringVar(),
        "Nuevo tipo": ctk.StringVar(),
        "Nuevo precio": ctk.StringVar()
    }

    for etiqueta, var in campos.items():
        cont = ctk.CTkFrame(frame_submenu, fg_color="transparent")
        cont.pack(pady=10)
        lbl = ctk.CTkLabel(cont, text=etiqueta, font=("Arial", 16))
        lbl.pack(side="left", padx=10)
        ent = ctk.CTkEntry(cont, textvariable=var, width=250, height=35)
        ent.pack(side="left")

    def confirmar():
        datos = {c: v.get().strip() for c, v in campos.items()}
        if any(v == "" for v in datos.values()):
            messagebox.showwarning("Atención", "Por favor llena todos los campos.")
            return
        messagebox.showinfo("Modificación", f"Hilo {datos['Marca']} ({datos['Código de color']}) actualizado.")
        mostrar_menu()

    ctk.CTkButton(frame_submenu, text="Guardar cambios", command=confirmar, width=250, height=40).pack(pady=20)
    ctk.CTkButton(frame_submenu, text="↩ Volver", command=mostrar_menu, width=250, height=40).pack(pady=10)


def eliminar_hilo():
    frame_menu.pack_forget()
    frame_submenu.pack(expand=True, fill="both")
    for w in frame_submenu.winfo_children():
        w.destroy()

    crear_encabezado(frame_submenu)
    titulo = ctk.CTkLabel(frame_submenu, text="Eliminar Hilo", font=("Arial", 26, "bold"))
    titulo.pack(pady=20)

    campos = {
        "Marca": ctk.StringVar(),
        "Código de color": ctk.StringVar()
    }

    for etiqueta, var in campos.items():
        cont = ctk.CTkFrame(frame_submenu, fg_color="transparent")
        cont.pack(pady=10)
        lbl = ctk.CTkLabel(cont, text=etiqueta, font=("Arial", 16))
        lbl.pack(side="left", padx=10)
        ent = ctk.CTkEntry(cont, textvariable=var, width=250, height=35)
        ent.pack(side="left")

    def confirmar():
        datos = {c: v.get().strip() for c, v in campos.items()}
        if any(v == "" for v in datos.values()):
            messagebox.showwarning("Atención", "Por favor llena ambos campos.")
            return
        messagebox.showinfo("Eliminado", f"Hilo {datos['Marca']} ({datos['Código de color']}) eliminado.")
        mostrar_menu()

    ctk.CTkButton(frame_submenu, text="Eliminar hilo", command=confirmar, width=250, height=40).pack(pady=20)
    ctk.CTkButton(frame_submenu, text="↩ Volver", command=mostrar_menu, width=250, height=40).pack(pady=10)


def registrar_compra():
    frame_menu.pack_forget()
    frame_submenu.pack(expand=True, fill="both")
    for w in frame_submenu.winfo_children():
        w.destroy()

    crear_encabezado(frame_submenu)
    titulo = ctk.CTkLabel(frame_submenu, text="Registrar Compra / Reabastecimiento", font=("Arial", 26, "bold"))
    titulo.pack(pady=20)

    campos = {
        "Marca": ctk.StringVar(),
        "Código de color": ctk.StringVar(),
        "Cantidad comprada": ctk.StringVar(),
        "Precio de compra": ctk.StringVar(),
        "Proveedor": ctk.StringVar()
    }

    for etiqueta, var in campos.items():
        cont = ctk.CTkFrame(frame_submenu, fg_color="transparent")
        cont.pack(pady=10)
        lbl = ctk.CTkLabel(cont, text=etiqueta, font=("Arial", 16))
        lbl.pack(side="left", padx=10)
        ent = ctk.CTkEntry(cont, textvariable=var, width=250, height=35)
        ent.pack(side="left")

    def confirmar():
        datos = {c: v.get().strip() for c, v in campos.items()}
        if any(v == "" for v in datos.values()):
            messagebox.showwarning("Atención", "Por favor completa todos los campos.")
            return
        resumen = "\n".join([f"{k}: {v}" for k, v in datos.items()])
        messagebox.showinfo("Compra registrada", f"Datos de compra:\n\n{resumen}")
        mostrar_menu()

    ctk.CTkButton(frame_submenu, text="Registrar compra", command=confirmar, width=250, height=40).pack(pady=20)
    ctk.CTkButton(frame_submenu, text="↩ Volver", command=mostrar_menu, width=250, height=40).pack(pady=10)


def registrar_venta():
    frame_menu.pack_forget()
    frame_submenu.pack(expand=True, fill="both")
    for w in frame_submenu.winfo_children():
        w.destroy()

    crear_encabezado(frame_submenu)
    titulo = ctk.CTkLabel(frame_submenu, text="Registrar Venta", font=("Arial", 26, "bold"))
    titulo.pack(pady=20)

    campos = {
        "Marca": ctk.StringVar(),
        "Código de color": ctk.StringVar(),
        "Cantidad vendida": ctk.StringVar(),
        "Precio unitario": ctk.StringVar(),
        "Nombre del cliente": ctk.StringVar()
    }

    for etiqueta, var in campos.items():
        cont = ctk.CTkFrame(frame_submenu, fg_color="transparent")
        cont.pack(pady=10)
        lbl = ctk.CTkLabel(cont, text=etiqueta, font=("Arial", 16))
        lbl.pack(side="left", padx=10)
        ent = ctk.CTkEntry(cont, textvariable=var, width=250, height=35)
        ent.pack(side="left")

    def confirmar():
        datos = {c: v.get().strip() for c, v in campos.items()}
        if any(v == "" for v in datos.values()):
            messagebox.showwarning("Atención", "Por favor completa todos los campos.")
            return
        try:
            total = float(datos["Cantidad vendida"]) * float(datos["Precio unitario"])
        except:
            total = 0
        messagebox.showinfo("Venta registrada",
                            f"Cliente: {datos['Nombre del cliente']}\n"
                            f"Hilo: {datos['Marca']} ({datos['Código de color']})\n"
                            f"Cantidad: {datos['Cantidad vendida']}\n"
                            f"Total: Q{total:.2f}")
        mostrar_menu()

    ctk.CTkButton(frame_submenu, text="Registrar venta", command=confirmar, width=250, height=40).pack(pady=20)
    ctk.CTkButton(frame_submenu, text="↩ Volver", command=mostrar_menu, width=250, height=40).pack(pady=10)


def reportes_consultas():
    frame_menu.pack_forget()
    frame_submenu.pack(expand=True, fill="both")
    for w in frame_submenu.winfo_children():
        w.destroy()

    crear_encabezado(frame_submenu)
    titulo = ctk.CTkLabel(frame_submenu, text="Reportes y Consultas", font=("Arial", 26, "bold"))
    titulo.pack(pady=20)

    campos = {
        "Tipo de reporte": ctk.StringVar(),
        "Fecha inicial": ctk.StringVar(),
        "Fecha final": ctk.StringVar()
    }

    for etiqueta, var in campos.items():
        cont = ctk.CTkFrame(frame_submenu, fg_color="transparent")
        cont.pack(pady=10)
        lbl = ctk.CTkLabel(cont, text=etiqueta, font=("Arial", 16))
        lbl.pack(side="left", padx=10)
        ent = ctk.CTkEntry(cont, textvariable=var, width=250, height=35)
        ent.pack(side="left")

    def confirmar():
        datos = {c: v.get().strip() for c, v in campos.items()}
        if any(v == "" for v in datos.values()):
            messagebox.showwarning("Atención", "Por favor completa los campos.")
            return
        messagebox.showinfo("Consulta generada", f"Reporte: {datos['Tipo de reporte']}\n"
                                                 f"Desde: {datos['Fecha inicial']}\n"
                                                 f"Hasta: {datos['Fecha final']}")
        mostrar_menu()

    ctk.CTkButton(frame_submenu, text="Generar reporte", command=confirmar, width=250, height=40).pack(pady=20)
    ctk.CTkButton(frame_submenu, text="↩ Volver", command=mostrar_menu, width=250, height=40).pack(pady=10)


def inventario_completo():
    frame_menu.pack_forget()
    frame_submenu.pack(expand=True, fill="both")
    for w in frame_submenu.winfo_children():
        w.destroy()

    crear_encabezado(frame_submenu)
    titulo = ctk.CTkLabel(frame_submenu, text="Inventario Completo", font=("Arial", 26, "bold"))
    titulo.pack(pady=30)

    texto = (
        "Aquí se mostraría el inventario completo.\n"
        "Por ahora es solo una pantalla de prueba.\n\n"
        "Ejemplo:\n"
        "Marca: Omega | Tipo: Seda | Color: #45 | Cantidad: 24 | Precio: Q15.50"
    )

    ctk.CTkLabel(frame_submenu, text=texto, font=("Arial", 16), justify="center").pack(pady=40)
    ctk.CTkButton(frame_submenu, text="↩ Volver", command=mostrar_menu, width=250, height=40).pack(pady=10)

# EJECUCIÓN DEL PROGRAMA
ventana.mainloop()
