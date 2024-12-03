import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

def ventana_ventas():
    def inicializar_tabla_ventas():
        """Crea la tabla de historial de ventas si no existe."""
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                fecha TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def cargar_productos():
        """Carga la lista de productos del inventario."""
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, cantidad FROM productos")
        productos = cursor.fetchall()
        conn.close()
        return productos

    def actualizar_stock():
        """Actualiza la tabla de inventario."""
        lista_stock.delete(*lista_stock.get_children())
        for producto, cantidad in cargar_productos():
            lista_stock.insert("", "end", values=(producto, cantidad))

    def buscar_producto():
        """Filtra los productos según el término de búsqueda."""
        termino = entrada_busqueda.get().lower()
        lista_stock.delete(*lista_stock.get_children())
        for producto, cantidad in cargar_productos():
            if termino in producto.lower():
                lista_stock.insert("", "end", values=(producto, cantidad))

    def abrir_ventana_venta():
        """Abre una ventana nueva para realizar una venta."""
        def procesar_venta():
            """Registra la venta y genera un ticket."""
            producto = seleccion_producto.get()
            try:
                cantidad = int(entrada_cantidad.get())
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número entero.")
                return

            precio_unitario = 50  # Precio fijo de ejemplo (puedes cambiarlo a dinámico)
            
            conn = sqlite3.connect("sistema.db")
            cursor = conn.cursor()

            # Verificar stock disponible
            cursor.execute("SELECT cantidad FROM productos WHERE nombre = ?", (producto,))
            stock_actual = cursor.fetchone()
            if not stock_actual:
                messagebox.showerror("Error", "El producto no existe.")
                conn.close()
                return

            if stock_actual[0] >= cantidad:
                nuevo_stock = stock_actual[0] - cantidad
                cursor.execute("UPDATE productos SET cantidad = ? WHERE nombre = ?", (nuevo_stock, producto))
                
                # Registrar venta en la tabla de ventas
                total_precio = cantidad * precio_unitario
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    INSERT INTO ventas (producto, cantidad, precio, fecha) 
                    VALUES (?, ?, ?, ?)
                """, (producto, cantidad, total_precio, fecha_actual))
                conn.commit()

                # Generar ticket
                ticket = f"""
                ---------------------------------
                TICKET DE COMPRA
                Fecha: {fecha_actual}
                Producto: {producto}
                Cantidad: {cantidad}
                Precio Unitario: ${precio_unitario:.2f}
                Total: ${total_precio:.2f}
                ---------------------------------
                """
                messagebox.showinfo("Venta Realizada", ticket)
                actualizar_stock()
                ventana_venta.destroy()
            else:
                messagebox.showerror("Error", "Cantidad no disponible en inventario.")
            conn.close()

        # Crear la ventana para realizar la venta
        ventana_venta = tk.Toplevel(ventana)
        ventana_venta.title("Realizar Venta")
        ventana_venta.geometry("400x400")
        ventana_venta.configure(bg="#2C1466")

        tk.Label(ventana_venta, text="Selecciona producto", bg="#2C1466", fg="white", font=("Typewriter_Condensed", 20)).pack(pady=10)
        seleccion_producto = ttk.Combobox(ventana_venta, values=[p[0] for p in cargar_productos()], font=("Typewriter_Condensed", 12))
        seleccion_producto.pack(pady=5)

        tk.Label(ventana_venta, text="Cantidad", bg="#2C1466", fg="white", font=("Typewriter_Condensed", 20)).pack(pady=10)
        entrada_cantidad = tk.Entry(ventana_venta, font=("Helvetica", 12))
        entrada_cantidad.pack(pady=5)

        tk.Button(ventana_venta, text="Hacer Venta", font=("Typewriter_Condensed", 20, "bold"), bg="#faf609", fg="black", command=procesar_venta).pack(pady=20)

    # Configurar ventana principal
    ventana = tk.Tk()
    ventana.title("Área de Ventas")
    ventana.geometry("800x600")
    ventana.configure(bg="#2C1466")

    # Inicializar tabla de ventas
    inicializar_tabla_ventas()

    # Inventario
    tk.Label(ventana, text="Inventario de Productos", font=("Haettenschweiler", 24, "bold"), bg="#2C1466", fg="#fdfdff").pack(pady=10)
    lista_stock = ttk.Treeview(ventana, columns=("Producto", "Cantidad"), show="headings")
    lista_stock.heading("Producto", text="Producto")
    lista_stock.heading("Cantidad", text="Cantidad")
    lista_stock.pack(pady=10, fill=tk.BOTH, expand=True)

    actualizar_stock()

    # Búsqueda de productos
    tk.Label(ventana, text="Buscar producto", font=("Haettenschweiler", 20), bg="#fa4a09").pack(pady=10)
    entrada_busqueda = tk.Entry(ventana, font=("Helvetica", 12))
    entrada_busqueda.pack(pady=5, padx=20, fill=tk.X)
    tk.Button(ventana, text="Buscar", font=("Haettenschweiler", 20), bg="#fa9209", fg="#11121e", command=buscar_producto).pack(pady=10)

    # Botón para abrir ventana de ventas
    tk.Button(ventana, text="Realizar Venta", font=("Haettenschweiler", 20, "bold"), bg="#faf609", fg="#11121e", command=abrir_ventana_venta).pack(pady=20)

    ventana.mainloop()
