import socket

# Configuración del servidor de destino
HOST = '127.0.0.1'
PORT = 5000

def iniciar_cliente():
    """Conecta al servidor, permite enviar mensajes y recibe las confirmaciones en bucle."""
    
    # Configuración del socket TCP/IP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Intento de conexión con la tupla (Host, Puerto)
        cliente.connect((HOST, PORT))
        print(f"[*] Conectado exitosamente al Servidor en {HOST}:{PORT}")
        print("    -> Escribí tu mensaje y presioná Enter para enviar.")
        print("    -> Escribí 'éxito' para desconectarte.")
        print("-" * 60)
        
        while True:
            # Lectura del mensaje desde el input de la terminal
            mensaje = input("\nVos > ")
            
            # Validación de salida (corte por consigna del TP)
            # Usamos lower() para que detecte 'Éxito', 'exito', 'EXITO' por igual
            if mensaje.strip().lower() in ['éxito', 'exito']:
                print("[*] Palabra clave detectada. Cerrando conexión...")
                break
            
            # Prevenir envío de mensajes vacíos que puedan causar bugs
            if not mensaje.strip():
                print("[!] No podés enviar un mensaje vacío.")
                continue
                
            # Envío del texto parseado a bytes al servidor
            cliente.sendall(mensaje.encode('utf-8'))
            
            # Esperamos que el servidor nos conteste la confirmación de llegada y guardado
            # Nos detendremos acá (bloqueo) hasta que llegue esa respuesta
            respuesta_bytes = cliente.recv(1024)
            
            # Si recv me tira vacío, significa que el servidor cerró repentinamente la conexión
            if not respuesta_bytes:
                print("[!] El servidor ha cerrado la conexión.")
                break
                
            # Mostrar la respuesta decodificada enviada por el server
            respuesta_texto = respuesta_bytes.decode('utf-8')
            print(f"Servidor > {respuesta_texto}")
            
    except ConnectionRefusedError:
        print(f"[ERROR CRÍTICO] Conexión rechazada. Verificá que el archivo 'servidor.py' esté corriendo en {HOST}:{PORT}.")
    except KeyboardInterrupt:
        print("\n[!] Salida forzada por teclado (Ctrl+C). Cerrando el cliente...")
    except Exception as e:
        print(f"[ERROR INESPERADO] {e}")
    finally:
        # Limpiamos recursos cerrando comunicación
        cliente.close()
        print("[-] Socket de red cerrado exitosamente.")

if __name__ == '__main__':
    iniciar_cliente()
