import sqlite3

# Inicializar la base de datos
def inicializar_bd():
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
    """)

    # Crear tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL
        )
    """)

    # Crear tabla de empleados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            departamento TEXT NOT NULL,
            sueldo REAL NOT NULL
        )
    """)


    # Insertar datos iniciales si no existen
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO usuarios (tipo, usuario, contrasena) VALUES (?, ?, ?)
        """, [
            ("ventas", "ventas1", "1234"),
            ("admin", "admin1", "admin123")
        ])

    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos = [
            ("Pila Solar Premium Rosa", 50), ("Pila Solar Premium Azul", 40), 
            ("Pila Solar Básica Negra", 70), ("Pila Solar Básica Verde", 60),
            ("Panel Solar Portátil Compacto", 20), ("Panel Solar Portátil XL", 15),
            ("Pila Solar de Alta Capacidad", 25), ("Pila Solar con Carga Rápida", 30),
            ("Pila Solar para Emergencias", 35), ("Pila Solar para Uso Diario", 45),
            ("Pila Solar Estándar", 50), ("Pila Solar para Teléfonos", 60),
            ("Pila Solar para Tablets", 55), ("Pila Solar para Laptops", 10),
            ("Pila Solar Portátil", 40), ("Panel Solar de Sobremesa", 20),
            ("Panel Solar Premium", 15), ("Cargador Solar Universal", 70),
            ("Cargador Solar Compacto", 65), ("Batería Solar Modular", 30),
            ("Batería Solar Ultra-Liviana", 25), ("Panel Solar Doméstico", 10),
            ("Panel Solar para Camping", 35), ("Panel Solar para Viajes", 30),
            ("Pila Solar Compacta", 50), ("Pila Solar Resistente al Agua", 45),
            ("Pila Solar con Puerto USB", 60), ("Pila Solar con Lámpara", 25),
            ("Kit Solar Básico", 40), ("Kit Solar Avanzado", 20)
        ]
        cursor.executemany("""
            INSERT INTO productos (nombre, cantidad) VALUES (?, ?)
        """, productos)

    cursor.execute("SELECT COUNT(*) FROM empleados")
    if cursor.fetchone()[0] == 0:
        empleados = [
            # Bodega
            ("Juan Pérez", "Bodega", 8000), ("María Gómez", "Bodega", 7800),
            ("Carlos Sánchez", "Bodega", 7900), ("Ana López", "Bodega", 8100),
            ("Luis Ramírez", "Bodega", 8000), ("José Martínez", "Bodega", 7700),
            ("Isabel Torres", "Bodega", 7600), ("Miguel Díaz", "Bodega", 7800),
            # Atención al Cliente
            ("Carmen Silva", "Atención al Cliente", 7500), ("Javier Ortega", "Atención al Cliente", 7400),
            ("Laura Núñez", "Atención al Cliente", 7600), ("Pablo Reyes", "Atención al Cliente", 7500),
            ("Lidia Soto", "Atención al Cliente", 7400),
            # Recursos Humanos
            ("Sofía Peña", "Recursos Humanos", 9000), ("Roberto Blanco", "Recursos Humanos", 8900),
            ("Daniela Vega", "Recursos Humanos", 8800), ("Fernando Ruiz", "Recursos Humanos", 9200),
            ("Lucía Jiménez", "Recursos Humanos", 9100), ("Andrés Salas", "Recursos Humanos", 8800),
            # Contabilidad
            ("Gloria Ramos", "Contabilidad", 8500), ("Ricardo Flores", "Contabilidad", 8600),
            ("Marta Herrera", "Contabilidad", 8700), ("Raúl Castro", "Contabilidad", 8500),
            ("Claudia Paredes", "Contabilidad", 8400), ("Diego Montalvo", "Contabilidad", 8600),
            # Ventas
            ("Camila Luna", "Ventas", 7000), ("Oscar Medina", "Ventas", 7100),
            ("Adriana Quintana", "Ventas", 7200), ("José Ávila", "Ventas", 7300),
            ("Natalia Prado", "Ventas", 7400), ("Enrique Márquez", "Ventas", 7200),
            ("Elena Vargas", "Ventas", 7100), ("Francisco Cortés", "Ventas", 7000),
            ("María Fernández", "Ventas", 7300), ("Santiago Aguilar", "Ventas", 7400),
            ("Jorge Vázquez", "Ventas", 7100), ("Valeria Navarro", "Ventas", 7000),
            ("Ignacio Herrera", "Ventas", 7200), ("Patricia Morales", "Ventas", 7300),
            ("Alonso García", "Ventas", 7400)
        ]
        cursor.executemany("""
            INSERT INTO empleados (nombre, departamento, sueldo) VALUES (?, ?, ?)
        """, empleados)

    conn.commit()
    conn.close()

# Función para verificar usuario
def verificar_usuario(usuario, contrasena):
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tipo FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None
