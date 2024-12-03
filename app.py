import tkinter as tk
from tkinter import messagebox
from database import inicializar_bd, verificar_usuario
from ventas import ventana_ventas
from administracion import ventana_admin

# Ventana inicial para seleccionar tipo de usuario
def ventana_seleccion_usuario():
    def abrir_login(tipo):
        ventana.destroy()
        ventana_login(tipo)

    ventana = tk.Tk()
    ventana.title("Sistema Empresarial - Selección de Usuario")
    ventana.geometry("650x450")
    ventana.configure(bg="#2C1466")  # Fondo gris claro

    # Título
    tk.Label(ventana, text="Selecciona tu tipo de usuario", font=("Coffee Fills", 24, "bold"), bg="#2C1466", fg="#F3EEFF").pack(pady=40)

    # Botones para seleccionar tipo de usuario
    tk.Button(ventana, text="Ventas", width=20, height=2, font=("Haettenschweiler", 18), bg="#f2fa05", fg="#0E0E0C", command=lambda: abrir_login("ventas")).pack(pady=10)
    tk.Button(ventana, text="Administración", width=20, height=2, font=("Haettenschweiler", 18), bg="#f2b60d", fg="#0E0E0C", command=lambda: abrir_login("admin")).pack(pady=10)

    ventana.mainloop()

# Ventana de login
def ventana_login(tipo_usuario):
    def verificar_login():
        usuario = entrada_usuario.get()
        contrasena = entrada_password.get()
        tipo_verificado = verificar_usuario(usuario, contrasena)
        if tipo_verificado == tipo_usuario:
            ventana.destroy()
            if tipo_usuario == "ventas":
                ventana_ventas()
            elif tipo_usuario == "admin":
                ventana_admin()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos o tipo de usuario no coincide.")

    ventana = tk.Tk()
    ventana.title(f"Login - {tipo_usuario.capitalize()}")
    ventana.geometry("350x350")
    ventana.configure(bg="#2C1466")  # Fondo gris claro

    # Título de la ventana de login
    tk.Label(ventana, text=f"Inicia sesión como {tipo_usuario.capitalize()}", font=("Happy Memories", 18, "bold"), bg="#2C1466", fg="#F3EEFF").pack(pady=20)

    # Campos de entrada
    tk.Label(ventana, text="Usuario", font=("Typewriter_Condensed", 12), bg="#2C1466", fg="#F3EEFF").pack(pady=5)
    entrada_usuario = tk.Entry(ventana, font=("Typewriter_Condensed", 12), bd=2)
    entrada_usuario.pack(pady=5, padx=30, fill='x')

    tk.Label(ventana, text="Contraseña", font=("Typewriter_Condensed", 12), bg="#2C1466", fg="#F3EEFF").pack(pady=5)
    entrada_password = tk.Entry(ventana, show="*", font=("Helvetica", 12), bd=2)
    entrada_password.pack(pady=5, padx=30, fill='x')

    # Botón para iniciar sesión
    tk.Button(ventana, text="Iniciar sesión", font=("Haettenschweiler", 12), bg="#eefa09", fg="#0E0E0C", width=20, height=2, command=verificar_login).pack(pady=20)

    ventana.mainloop()

# Punto de inicio del programa
if __name__ == "__main__":
    inicializar_bd()  # Inicializar la base de datos
    ventana_seleccion_usuario()
