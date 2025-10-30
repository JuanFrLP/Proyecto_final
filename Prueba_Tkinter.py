import customtkinter as ctk
from tkinter import messagebox

#CONFIGURACIÓN GENERAL
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Tienda de Hilos Arcoíris")
ventana.state('zoomed')

#FUNCIÓN PARA CREAR ENCABEZADO GLOBAL
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

#FRAME DE SELECCIÓN DE USUARIO
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

#FRAMES PRINCIPALES
frame_menu = ctk.CTkFrame(ventana)
frame_submenu = ctk.CTkFrame(ventana)

#FUNCIONES PRINCIPALES
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

    #MENÚ DIFERENTE SEGÚN USUARIO
    if tipo == "empleado":
        opciones = [
            ("1. Buscar hilo", lambda: abrir_subpantalla("Buscar Hilo")),
            ("2. Registrar venta", lambda: abrir_subpantalla("Registrar Venta")),
            ("3. Reportes y consultas", lambda: abrir_subpantalla("Reportes y Consultas")),
            ("4. Mostrar inventario completo", lambda: abrir_subpantalla("Inventario Completo")),
            ("5. Salir", ventana.destroy)
        ]
    elif tipo == "administrador":
        opciones = [
            ("1. Registrar nuevo hilo", lambda: abrir_subpantalla("Registrar Hilo")),
            ("2. Buscar hilo", lambda: abrir_subpantalla("Buscar Hilo")),
            ("3. Modificar información", lambda: abrir_subpantalla("Modificar Hilo")),
            ("4. Eliminar hilo", lambda: abrir_subpantalla("Eliminar Hilo")),
            ("5. Registrar compra/reabastecimiento", lambda: abrir_subpantalla("Registrar Compra/Reabastecimiento")),
            ("6. Registrar venta", lambda: abrir_subpantalla("Registrar Venta")),
            ("7. Reportes y consultas", lambda: abrir_subpantalla("Reportes y Consultas")),
            ("8. Mostrar inventario completo", lambda: abrir_subpantalla("Inventario Completo")),
            ("9. Salir", ventana.destroy)
        ]
    else:
        opciones = []

    # Crear botones del menú
    for texto, comando in opciones:
        boton = ctk.CTkButton(frame_menu, text=texto, command=comando, width=400, height=40, font=("Arial", 16))
        boton.pack(pady=8)

    # Botón para volver al selector de usuario
    boton_volver = ctk.CTkButton(frame_menu, text="↩ Volver a selección de usuario",
                                 fg_color="#444", hover_color="#666",
                                 width=300, height=40,
                                 command=volver_a_selector)
    boton_volver.pack(pady=15)

def volver_a_selector():
    frame_menu.pack_forget()
    frame_usuario.pack(expand=True, fill="both")

#SUBPANTALLAS
def abrir_subpantalla(titulo):
    frame_menu.pack_forget()
    frame_submenu.pack(expand=True, fill="both")

    for widget in frame_submenu.winfo_children():
        widget.destroy()

    crear_encabezado(frame_submenu)

    label = ctk.CTkLabel(frame_submenu, text=titulo, font=("Arial", 26, "bold"))
    label.pack(pady=40)

    entrada = ctk.CTkEntry(frame_submenu, placeholder_text="Escribe aquí...", width=350, height=40)
    entrada.pack(pady=20)

    def confirmar():
        texto = entrada.get().strip()
        if not texto:
            messagebox.showwarning("Atención", "Por favor, ingresa un texto.")
        else:
            messagebox.showinfo("Confirmado", f"Has ingresado: {texto}")
            mostrar_menu()

    boton_confirmar = ctk.CTkButton(frame_submenu, text="Confirmar", command=confirmar, width=250, height=40)
    boton_confirmar.pack(pady=10)

    boton_volver = ctk.CTkButton(frame_submenu, text="↩ Volver al menú principal",
                                 width=250, height=40, command=mostrar_menu)
    boton_volver.pack(pady=10)

#EJECUCIÓN DEL PROGRAMA
ventana.mainloop()
