# Propuesta Formativa Obligatoria

## TP: Implementación de un Chat Básico Cliente-Servidor con Sockets y Base de Datos

### 🎯 Objetivo
Aprender a configurar un servidor de sockets en Python que reciba mensajes de clientes, los almacene en una base de datos y envíe confirmaciones, aplicando buenas prácticas de modularización y manejo de errores. 

> **Nota:** Utilizar los comentarios para explicar las configuraciones en el servidor.

---

### 💻 Requerimientos

#### Servidor
Debe cumplir con las siguientes características:
- Crear un socket que escuche en `localhost:5000`.
- Usar **funciones separadas** para:
  - Inicializar el socket.
  - Aceptar conexiones y recibir mensajes.
  - Guardar cada mensaje en una base de datos **SQLite** con los campos: `id`, `contenido`, `fecha_envio`, `ip_cliente`.
  - Manejar errores (ej. puerto ocupado, DB no accesible).
- Responder al cliente con el texto: `"Mensaje recibido: <timestamp>"`.

#### Cliente
Debe cumplir con las siguientes características:
- Tener la capacidad de conectarse al servidor y enviar **múltiples mensajes** de forma continua hasta que el usuario escriba la palabra clave `éxito` para salir.
- Mostrar por pantalla la respuesta recibida del servidor para cada mensaje.

---

### 💡 Recomendaciones
- Utilizar el módulo integrado `sqlite3` de Python para la base de datos.
- Comentar cada sección clave del código (ej: `# Configuración del socket TCP/IP`).
- Ejecutar pruebas locales asegurándose de levantar primero el servidor en una terminal, y luego el cliente en otra.

---

### 📅 Condiciones de Entrega
- **Apertura de la actividad:** 22/4
- **Cierre de la actividad:** 29/4
- **Modo de entrega:** Subir el enlace del repositorio de código con la solución propuesta (GitHub / Bitbucket). 
- *Alternativa:* En caso de no usar repositorios, subir un archivo comprimido (`.zip`, `.rar`) con los scripts de la solución.
