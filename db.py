import sqlite3 as sql
import hashlib

def conectar ():
    return sql.connect("mi_agenda.db")
    # Abre (o crea si no existe) el archivo mi_agenda.db y devuelve la conexión.

    # Esta función se usa cada vez que quieras hablar con la base de datos.
def crear_tabla():
    conexion = conectar() # Abre la conexión
    cursor = conexion.cursor() # Crea un cursor para ejecutar comandos SQL
    cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    contraseña TEXT NOT NULL
)
""")

    conexion.commit()
    conexion.close()
    
def insertar_usuario(usuario, contraseña):
    conexion = conectar()
    cursor = conexion.cursor()
    contraseña_hash = hashlib.sha256(contraseña.encode()).hexdigest()  # Hashea la contraseña
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    existente = cursor.fetchone()
    if existente:
        conexion.close()
        return False  # Usuario ya existe
    else:
        cursor.execute("INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)", (usuario, contraseña_hash))
        conexion.commit()
        conexion.close()
        return True  # Usuario registrado exitosamente

    
def validar_usuario(usuario, contraseña):
    conexion = conectar ()
    cursor = conexion.cursor()
    #Encriptar la contraseña guardada
    contraseña_hash = hashlib.sha256(contraseña.encode()).hexdigest()
    cursor.execute("SELECT * FROM usuarios WHERE usuario =? AND contraseña=?", (usuario, contraseña_hash))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

def crear_tabla_tareas():
    conexion = sql.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            tarea TEXT
        )
    """)
    conexion.commit()
    conexion.close()

def insertar_tarea(usuario, tarea):
    conexion = sql.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO tareas (usuario, tarea) VALUES (?, ?)", (usuario, tarea))
    conexion.commit()
    conexion.close()

def obtener_tareas(usuario):
    conexion = sql.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT tarea FROM tareas WHERE usuario=?", (usuario,))
    tareas = [fila[0] for fila in cursor.fetchall()]
    conexion.close()
    return tareas

def eliminar_tarea(usuario, tarea):
    conexion = sql.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM tareas WHERE usuario=? AND tarea=?", (usuario, tarea))
    conexion.commit()
    conexion.close()

