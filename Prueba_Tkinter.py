import customtkinter as ctk
from tkinter import messagebox

# Configuración inicial
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Crear la ventana principal
ventana = ctk.CTk()
ventana.title("MENÚ PRINCIPAL")
ventana.geometry("420x420")

#Función para abrir una nueva ventana con campo de texto 
def abrir_subventana(titulo_ventana, texto_label):
    subventana = ctk.CTkToplevel(ventana)
    subventana.title(titulo_ventana)
    subventana.geometry("400x250")

    label = ctk.CTkLabel(subventana, text=texto_label, font=("Arial", 16))
    label.pack(pady=20)

    entrada = ctk.CTkEntry(subventana, placeholder_text="Escribe aquí...", width=250)
    entrada.pack(pady=10)

    def confirmar():
        texto = entrada.get()
        if texto.strip() == "":
            messagebox.showwarning("Atención", "Por favor, ingresa un texto.")
        else:
            messagebox.showinfo("Confirmado", f"Has ingresado: {texto}")
            subventana.destroy()

    boton_confirmar = ctk.CTkButton(subventana, text="Confirmar", command=confirmar)
    boton_confirmar.pack(pady=10)

    boton_volver = ctk.CTkButton(subventana, text="Volver al menú", command=subventana.destroy)
    boton_volver.pack(pady=5)


# --- Ventana principal ---
titulo = ctk.CTkLabel(ventana, text="MENÚ PRINCIPAL", font=("Arial", 22, "bold"))
titulo.pack(pady=20)

# Opciones del menú
botones = [
    ("1. Registrar nuevo hilo", lambda: abrir_subventana("Registrar Hilo", "Ingrese el nombre del hilo:")),
    ("2. Buscar hilo", lambda: abrir_subventana("Buscar Hilo", "Ingrese el nombre o ID del hilo:")),
    ("3. Modificar información", lambda: abrir_subventana("Modificar Hilo", "Ingrese el ID del hilo a modificar:")),
    ("4. Eliminar hilo", lambda: abrir_subventana("Eliminar Hilo", "Ingrese el ID del hilo a eliminar:")),
    ("5. Mostrar inventario completo", lambda: abrir_subventana("Inventario", "Ingrese filtro o palabra clave:")),
]

# Crear botones dinámicamente
for texto, comando in botones:
    boton = ctk.CTkButton(ventana, text=texto, command=comando, width=250)
    boton.pack(pady=5)

# Botón de salida
boton_salir = ctk.CTkButton(ventana, text="6. Salir", fg_color="red", hover_color="#b30000", width=250, command=ventana.destroy)
boton_salir.pack(pady=15)

# Ejecutar la aplicación
ventana.mainloop()
