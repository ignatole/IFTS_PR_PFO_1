import socket

# Configuración del servidor de destino
HOST = '127.0.0.1'
PORT = 5000

def iniciar_cliente():
    """Conecta al servidor, envía mensajes y recibe confirmaciones en bucle."""
    # Configuración del socket TCP/IP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        cliente.connect((HOST, PORT))
        print(f"[*] Conectado al Servidor en {HOST}:{PORT}")
        print("    -> Escribí tu mensaje y presioná Enter para enviar.")
        print("    -> Escribí 'éxito' para desconectarte.")
        print("-" * 60)
        
        while True:
            mensaje = input("\nVos > ").strip()
            
            if mensaje.lower() in ['éxito', 'exito']:
                print("[*] Saliendo...")
                break
            
            if not mensaje:
                continue
                
            cliente.sendall(mensaje.encode('utf-8'))
            respuesta_bytes = cliente.recv(1024)
            
            if not respuesta_bytes:
                print("[!] El servidor ha cerrado la conexión.")
                break
                
            print(f"Servidor > {respuesta_bytes.decode('utf-8')}")
            
    except ConnectionRefusedError:
        print(f"[ERROR CRÍTICO] Servidor no encontrado en {HOST}:{PORT}")
    except KeyboardInterrupt:
        print("\n[!] Salida forzada por teclado (Ctrl+C). Cerrando...")
    except Exception as e:
        print(f"[ERROR INESPERADO] {e}")
    finally:
        cliente.close()
        print("[-] Socket cerrado.")

if __name__ == '__main__':
    iniciar_cliente()
