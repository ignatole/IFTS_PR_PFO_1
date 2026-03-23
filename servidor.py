import socket
import sqlite3
import datetime

# Configuración global del servidor
HOST = '127.0.0.1'
PORT = 5000
DB_NAME = 'chat_db.sqlite'

def inicializar_db():
    """Inicializa la base de datos y crea la tabla si no existe."""
    try:
        # Conexión a la base de datos SQLite
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        # OBTENER CAMBIOS: Creación de la tabla con los campos solicitados en el TP
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
        print(f"[ERROR DB] No se pudo acceder o crear la base de datos: {e}")
    finally:
        if 'conexion' in locals():
            conexion.close()

def guardar_mensaje(contenido, ip_cliente):
    """Guarda un mensaje en la base de datos SQLite y retorna el timestamp."""
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        # Obtenemos el timestamp actual para registrar la hora exacta
        fecha_envio = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        # Insertamos el registro parseado en la DB
        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, fecha_envio, ip_cliente))
        
        conexion.commit()
        return fecha_envio
    except sqlite3.Error as e:
        print(f"[ERROR DB] Error al intentar guardar el mensaje: {e}")
        return None
    finally:
        if 'conexion' in locals():
            conexion.close()

def inicializar_socket():
    """Crea y enlaza el socket principal del servidor."""
    # Configuración del socket TCP/IP
    # Se usa AF_INET para IPv4 y SOCK_STREAM para TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # SO_REUSEADDR permite reiniciar el servidor sin que tire el error de puerto ocupado si se acaba de cerrar
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Enlazamos la IP y el PUERTO
        servidor.bind((HOST, PORT))
        # Habilitamos la recepción de conexiones (5 en cola máx)
        servidor.listen(5)
        print(f"[*] Servidor iniciado y escuchando activamente en {HOST}:{PORT}")
        return servidor
    except OSError as e:
        # Manejo de error si el puerto está en uso por otra app
        print(f"[ERROR SOCKET] El puerto {PORT} está ocupado o bloqueado: {e}")
        return None

def manejar_conexion(conn, addr):
    """Maneja la recepción de mensajes, guardado en DB y respuesta al cliente."""
    # Extraemos la IP de la tupla del cliente (índice 0)
    ip_cliente = addr[0]
    print(f"\n[+] Nueva conexión entrante desde: {ip_cliente}:{addr[1]}")
    
    try:
        while True:
            # Esperamos recibir datos (hasta 1024 bytes por tanda)
            datos = conn.recv(1024)
            
            # Si datos está vacío, significa que el cliente cerró la conexión
            if not datos:
                print(f"[-] El cliente {ip_cliente} se ha desconectado de forma limpia.")
                break
            
            # Decodificamos de bytes a string
            mensaje_texto = datos.decode('utf-8')
            print(f"[{ip_cliente}] Mensaje recibido: {mensaje_texto}")
            
            # Guardado en base de datos
            fecha_guardado = guardar_mensaje(mensaje_texto, ip_cliente)
            
            # Respuesta enviada de vuelta al cliente para confirmación
            if fecha_guardado:
                respuesta = f"Mensaje recibido: {fecha_guardado}"
            else:
                respuesta = "Mensaje recibido, pero hubo un error en la Base de Datos."
                
            # Mandamos la cadena de respuesta devuelta en bytes
            conn.sendall(respuesta.encode('utf-8'))
            
    except ConnectionResetError:
        # Se ataja por si el cliente mata el proceso de la terminal inesperadamente ("corte de luz")
        print(f"[!] Conexión perdida repentinamente con {ip_cliente}.")
    finally:
        # Aseguramos dejar la memoria limpia cerrando este socket hijo
        conn.close()

def iniciar_servidor():
    """Función principal (Entry point) que orquesta todo el modelo."""
    # Paso 1: Levantar archivo DB y tablas
    inicializar_db()
    
    # Paso 2: Configurar red
    server_socket = inicializar_socket()
    
    # Si hubo error de puertos no seguimos ejecutando
    if server_socket is None:
        return 
        
    # [FIX WINDOWS] Timeout de 1 seg para que el bucle se destrabe y reciba el Ctrl+C
    server_socket.settimeout(1.0)
        
    try:
        while True:
            try:
                # Bloque síncrono: el script hace "pausa" acá hasta que se asome un cliente
                conn, addr = server_socket.accept()
                
                # Le quitamos el timeout al cliente particular para no cortar su conexión
                conn.settimeout(None)
                
                # Para este TP básico, procesamos el cliente hasta que cierre, 
                # y luego el `while` permite aceptar al siguiente cliente. 
                manejar_conexion(conn, addr)
            except socket.timeout:
                # Pasa cada segundo si no hay clientes. Permite leer el Ctrl+C.
                pass
            except TimeoutError:
                pass
            
    except KeyboardInterrupt:
        print("\n[!] Has presionado Ctrl+C. Deteniendo el servidor...")
    finally:
        print("[-] Apagando el socket principal...")
        server_socket.close()
        print("[-] Bye!")

if __name__ == '__main__':
    iniciar_servidor()
