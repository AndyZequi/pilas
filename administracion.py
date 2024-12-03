import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def ventana_admin():
    def cargar_empleados(filtro=None, orden=None):
        """Carga la lista de empleados con filtros y orden opcional."""
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        query = "SELECT nombre, departamento, sueldo FROM empleados"
        
        if filtro:
            query += f" WHERE departamento = ?"
        if orden:
            query += f" ORDER BY sueldo {orden}"
        
        if filtro:
            cursor.execute(query, (filtro,))
        else:
            cursor.execute(query)
        
        empleados = cursor.fetchall()
        conn.close()
        return empleados

    def mostrar_empleados():
        """Actualiza la lista de empleados según el filtro o el orden seleccionado."""
        departamento = filtro_departamento.get()
        orden_sueldo = filtro_orden_sueldo.get()
        
        orden = "ASC" if orden_sueldo == "Menor a Mayor" else "DESC" if orden_sueldo == "Mayor a Menor" else None
        empleados = cargar_empleados(departamento if departamento != "Todos" else None, orden)
        
        lista_empleados.delete(*lista_empleados.get_children())
        for empleado in empleados:
            lista_empleados.insert("", "end", values=empleado)

    def buscar_por_nombre():
        """Busca empleados por nombre."""
        nombre = entrada_busqueda_nombre.get().lower()
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, departamento, sueldo FROM empleados WHERE LOWER(nombre) LIKE ?", (f"%{nombre}%",))
        empleados = cursor.fetchall()
        conn.close()

        lista_empleados.delete(*lista_empleados.get_children())
        for empleado in empleados:
            lista_empleados.insert("", "end", values=empleado)

    def mostrar_ventas():
        """Muestra las ventas realizadas."""
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        cursor.execute("SELECT producto, cantidad, precio, fecha FROM ventas")
        ventas = cursor.fetchall()
        conn.close()

        ventana_ventas = tk.Toplevel(ventana)
        ventana_ventas.title("Historial de Ventas")
        ventana_ventas.geometry("600x400")
        ventana.configure(bg="#2C1466")
        
        lista_ventas = ttk.Treeview(ventana_ventas, columns=("Producto", "Cantidad", "Precio", "Fecha"), show="headings")
        lista_ventas.heading("Producto", text="Producto")
        lista_ventas.heading("Cantidad", text="Cantidad")
        lista_ventas.heading("Precio", text="Precio")
        lista_ventas.heading("Fecha", text="Fecha")
        lista_ventas.pack(fill=tk.BOTH, expand=True, pady=10)

        for venta in ventas:
            lista_ventas.insert("", "end", values=venta)

    def mostrar_inventario():
        """Muestra el inventario actual."""
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, cantidad FROM productos")
        inventario = cursor.fetchall()
        conn.close()

        ventana_inventario = tk.Toplevel(ventana)
        ventana_inventario.title("Inventario")
        ventana_inventario.geometry("400x300")
        ventana_inventario.configure(bg="#2C1466")

        lista_inventario = ttk.Treeview(ventana_inventario, columns=("Producto", "Cantidad"), show="headings")
        lista_inventario.heading("Producto", text="Producto")
        lista_inventario.heading("Cantidad", text="Cantidad")
        lista_inventario.pack(fill=tk.BOTH, expand=True, pady=10)

        for item in inventario:
            lista_inventario.insert("", "end", values=item)

    def calcular_nomina():
        """Calcula la nómina de un empleado."""
        def procesar_nomina():
            """Procesa y muestra el desglose de la nómina."""
            empleado = seleccion_empleado.get()
            if not empleado:
                messagebox.showerror("Error", "Seleccione un empleado.")
                return

            # Obtiene datos del empleado
            conn = sqlite3.connect("sistema.db")
            cursor = conn.cursor()
            cursor.execute("SELECT departamento, sueldo FROM empleados WHERE nombre = ?", (empleado,))
            datos = cursor.fetchone()
            conn.close()

            if not datos:
                messagebox.showerror("Error", "Empleado no encontrado.")
                return

            departamento, sueldo_base = datos
            bonificacion = 500 if departamento == "Bodega" else 700 if departamento == "Ventas" else 600
            asistencia_completa = 100  # Bonificación por asistencia semanal

            # Obtiene descuentos manuales
            descuento = float(entrada_descuento.get()) if entrada_descuento.get() else 0

            total = sueldo_base + bonificacion + asistencia_completa - descuento

            # Generar ticket
            ticket = f"""
            ---------------------------------
            TICKET DE NÓMINA
            Empleado: {empleado}
            Departamento: {departamento}
            Sueldo Base: ${sueldo_base:.2f}
            Bonificación: ${bonificacion:.2f}
            Asistencia: ${asistencia_completa:.2f}
            Descuento: -${descuento:.2f}
            ---------------------------------
            Total: ${total:.2f}
            ---------------------------------
            """
            messagebox.showinfo("Nómina Generada", ticket)
            ventana_nomina.destroy()

        # Ventana para calcular la nómina
        ventana_nomina = tk.Toplevel(ventana)
        ventana_nomina.title("Cálculo de Nómina")
        ventana_nomina.geometry("400x300")
        ventana_nomina.configure(bg="#2C1466")

        tk.Label(ventana_nomina, text="Selecciona Empleado", font=("Typewriter_Condensed", 14), bg="#2C1466", fg="#fdfdff").pack(pady=10)
        seleccion_empleado = ttk.Combobox(ventana_nomina, values=[e[0] for e in cargar_empleados()], font=("Helvetica", 12))
        seleccion_empleado.pack(pady=5)

        tk.Label(ventana_nomina, text="Descuento (opcional)", font=("Typewriter_Condensed", 12), bg="#2C1466", fg="#fdfdff").pack(pady=10)
        entrada_descuento = tk.Entry(ventana_nomina, font=("Helvetica", 12))
        entrada_descuento.pack(pady=5)

        tk.Button(ventana_nomina, text="Calcular Nómina", font=("Haettenschweiler", 14, "bold"), bg="#007BFF", fg="black", command=procesar_nomina).pack(pady=20)

    # Configuración de la ventana principal
    ventana = tk.Tk()
    ventana.title("Área de Administración")
    ventana.geometry("800x800")
    ventana.configure(bg="#2C1466")

    # Lista de empleados
    tk.Label(ventana, text="Lista de Empleados", font=("Haettenschweiler", 24, "bold"), bg="#2C1466", fg="#fdfdff").pack(pady=10)
    lista_empleados = ttk.Treeview(ventana, columns=("Nombre", "Departamento", "Sueldo"), show="headings")
    lista_empleados.heading("Nombre", text="Nombre")
    lista_empleados.heading("Departamento", text="Departamento")
    lista_empleados.heading("Sueldo", text="Sueldo")
    lista_empleados.pack(fill=tk.BOTH, expand=True, pady=10)

    # Filtros y Búsquedas
    tk.Label(ventana, text="Filtrar por Departamento", bg="#2C1466", fg="#fdfdff").pack(pady=5)
    filtro_departamento = ttk.Combobox(ventana, values=["Todos", "Ventas", "Recursos Humanos", "Contabilidad", "Bodega", "Atención al Cliente"], state="readonly")
    filtro_departamento.current(0)
    filtro_departamento.pack(pady=5)

    tk.Label(ventana, text="Ordenar por Sueldo",bg="#2C1466", fg="#fdfdff").pack(pady=5)
    filtro_orden_sueldo = ttk.Combobox(ventana, values=["Sin Orden", "Menor a Mayor", "Mayor a Menor"], state="readonly")
    filtro_orden_sueldo.current(0)
    filtro_orden_sueldo.pack(pady=5)

    tk.Button(ventana, text="Aplicar Filtros", command=mostrar_empleados, bg="#f2ea14", fg="black", font=("Haettenschweiler", 16,)).pack(pady=10)

    tk.Label(ventana, text="Buscar Empleado por Nombre", bg="#2C1466", fg="#fdfdff").pack(pady=5)
    entrada_busqueda_nombre = tk.Entry(ventana)
    entrada_busqueda_nombre.pack(pady=5)
    tk.Button(ventana, text="Buscar", command=buscar_por_nombre,  bg="#f29314", fg="black", font=("Haettenschweiler", 16)).pack(pady=5)

    # Botones adicionales
    tk.Button(ventana, text="Ver Ventas", command=mostrar_ventas, bg="#f24e13", fg="black", font=("Haettenschweiler", 16)).pack(pady=10)
    tk.Button(ventana, text="Ver Inventario", command=mostrar_inventario, bg="#f21313", fg="black", font=("Haettenschweiler", 16)).pack(pady=10)
    tk.Button(ventana, text="Cálculo de Nóminas", command=calcular_nomina, bg="#ca0000", fg="black", font=("Haettenschweiler", 16)).pack(pady=10)

    mostrar_empleados()  # Cargar empleados al inicio
    ventana.mainloop()
