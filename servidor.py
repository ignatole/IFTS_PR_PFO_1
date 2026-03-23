import socket
import sqlite3
import datetime

# Configuración global
HOST = '127.0.0.1'
PORT = 5000
DB_NAME = 'chat_db.sqlite'

def inicializar_db():
    """Inicializa la base de datos y crea la tabla de mensajes."""
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conexion.commit()
    except sqlite3.Error as e:
        print(f"[ERROR DB] {e}")
    finally:
        if 'conexion' in locals():
            conexion.close()

def guardar_mensaje(contenido, ip_cliente):
    """Guarda recibos en la base SQLite y retorna el timestamp del suceso."""
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        fecha_envio = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, fecha_envio, ip_cliente))
        conexion.commit()
        return fecha_envio
    except sqlite3.Error as e:
        print(f"[ERROR DB] {e}")
        return None
    finally:
        if 'conexion' in locals():
            conexion.close()

def inicializar_socket():
    """Crea y enlaza el socket TCP/IP principal del servidor."""
    # Uso de AF_INET para IPv4 y SOCK_STREAM para TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        servidor.bind((HOST, PORT))
        servidor.listen(5)
        print(f"[*] Servidor escuchando activamente en {HOST}:{PORT}")
        return servidor
    except OSError as e:
        print(f"[ERROR SOCKET] Puerto {PORT} falló: {e}")
        return None

def manejar_conexion(conn, addr):
    """Maneja recepción de datos y responde confirmaciones por cada cliente."""
    ip_cliente = addr[0]
    print(f"\n[+] Nueva conexión: {ip_cliente}:{addr[1]}")
    
    try:
        while True:
            datos = conn.recv(1024)
            if not datos:
                print(f"[-] Cliente {ip_cliente} desconectado.")
                break
            
            mensaje = datos.decode('utf-8')
            print(f"[{ip_cliente}] Recibido: {mensaje}")
            
            fecha = guardar_mensaje(mensaje, ip_cliente)
            respuesta = f"Mensaje recibido: {fecha}" if fecha else "Error en BD."
            conn.sendall(respuesta.encode('utf-8'))
            
    except ConnectionResetError:
        print(f"[!] Conexión perdida repentinamente con {ip_cliente}.")
    finally:
        conn.close()

def iniciar_servidor():
    """Función orquestadora. Levanta DB, red y delega conexiones."""
    inicializar_db()
    server_socket = inicializar_socket()
    
    if not server_socket:
        return 
        
    # Timeout para permitir salida limpia (Ctrl+C) en Windows
    server_socket.settimeout(1.0)
        
    try:
        while True:
            try:
                conn, addr = server_socket.accept()
                conn.settimeout(None)
                manejar_conexion(conn, addr)
            except (socket.timeout, TimeoutError):
                pass
    except KeyboardInterrupt:
        print("\n[!] Ctrl+C presionado. Finalizando...")
    finally:
        print("[-] Apagando el servidor.")
        if server_socket:
            server_socket.close()

if __name__ == '__main__':
    iniciar_servidor()
