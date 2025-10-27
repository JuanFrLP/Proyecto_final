import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("MENÚ PRINCIPAL")
ventana.geometry("400x420")

titulo = ctk.CTkLabel(ventana, text="MENÚ PRINCIPAL", font=("Arial", 22, "bold"))
titulo.pack(pady=20)

def registrar_hilo():
    messagebox.showinfo("Registrar", "Opción 1 seleccionada")

def buscar_hilo():
    messagebox.showinfo("Buscar", "Opción 2 seleccionada")

def modificar_info():
    messagebox.showinfo("Modificar", "Opción 3 seleccionada")

def eliminar_hilo():
    messagebox.showinfo("Eliminar", "Opción 4 seleccionada")

def mostrar_inventario():
    messagebox.showinfo("Inventario", "Opción 5 seleccionada")

def salir():
    ventana.destroy()

boton1 = ctk.CTkButton(ventana, text="1. Registrar nuevo hilo", command=registrar_hilo, width=250)
boton1.pack(pady=5)

boton2 = ctk.CTkButton(ventana, text="2. Buscar hilo", command=buscar_hilo, width=250)
boton2.pack(pady=5)

boton3 = ctk.CTkButton(ventana, text="3. Modificar información", command=modificar_info, width=250)
boton3.pack(pady=5)

boton4 = ctk.CTkButton(ventana, text="4. Eliminar hilo", command=eliminar_hilo, width=250)
boton4.pack(pady=5)

boton5 = ctk.CTkButton(ventana, text="5. Mostrar inventario completo", command=mostrar_inventario, width=250)
boton5.pack(pady=5)

boton6 = ctk.CTkButton(ventana, text="6. Salir", command=salir, fg_color="red", hover_color="#b30000", width=250)
boton6.pack(pady=15)

ventana.mainloop()
