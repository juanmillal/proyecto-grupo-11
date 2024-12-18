import mysql.connector
from abc import ABC, abstractmethod
import hashlib
import requests  # Importar requests para el manejo de APIs

# Clase para manejar interacciones con APIs
class APIService:
    def __init__(self, base_url, api_key=None):
        """Inicializa el servicio API con la URL base y una clave opcional."""
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint, params=None):
        """Realiza una solicitud GET al endpoint especificado."""
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def post(self, endpoint, data=None):
        """Realiza una solicitud POST al endpoint especificado con datos JSON."""
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"} if self.api_key else {}
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def put(self, endpoint, data=None):
        """Realiza una solicitud PUT al endpoint especificado con datos JSON."""
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"} if self.api_key else {}
        response = requests.put(url, headers=headers, json=data)
        return response.json()

    def delete(self, endpoint):
        """Realiza una solicitud DELETE al endpoint especificado."""
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        response = requests.delete(url, headers=headers)
        return response.status_code

# Función para conectar a la base de datos
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Cambiar si tienes contraseña para root
            database="trabajo11"
        )
        print("Conexión exitosa a la base de datos.")
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar: {err}")
        return None

# Función para cifrar la contraseña con SHA256
def cifrar_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()

# Clase abstracta Persona
class Persona(ABC):
    def __init__(self, nombre, direccion, telefono, email):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    @abstractmethod
    def presentarse(self):
        pass

# Clase Empleado, heredando de Persona
class Empleado(Persona):
    def __init__(self, id, nombre, direccion, telefono, email, salario, rut, contraseña, rol):
        super().__init__(nombre, direccion, telefono, email)
        self.id = id
        self.salario = salario
        self.rut = rut
        self.contraseña = contraseña
        self.rol = rol  # 'admin' o 'usuario'

    def presentarse(self):
        return f"Soy {self.nombre}, empleado con ID {self.id} y mi salario es {self.salario}."

# Clase para manejar la base de datos
class BaseDeDatos:
    def __init__(self):
        self.conexion = conectar_db()
        if not self.conexion:
            raise Exception("No se pudo conectar a la base de datos.")

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")

    # Método para verificar si ya existe un administrador en la base de datos
    def existe_administrador(self):
        if not self.conexion:
            print("La conexión a la base de datos no está disponible.")
            return False

        try:
            cursor = self.conexion.cursor()
            sql = "SELECT COUNT(*) FROM empleados WHERE rol = 'admin'"
            cursor.execute(sql)
            resultado = cursor.fetchone()

            # Si el conteo es mayor que 0, existe al menos un administrador
            return resultado[0] > 0
        except mysql.connector.Error as err:
            print(f"Error al verificar administrador: {err}")
            return False
        finally:
            cursor.close()

    # Método para agregar un empleado a la base de datos
    def agregar_empleado(self, empleado):
        if not self.conexion:
            print("La conexión a la base de datos no está disponible.")
            return

        try:
            cursor = self.conexion.cursor()

            # Inserta los datos en la tabla personas
            sql_persona = "INSERT INTO personas (nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s)"
            valores_persona = (empleado.nombre, empleado.direccion, empleado.telefono, empleado.email)
            cursor.execute(sql_persona, valores_persona)

            # Obtiene el ID generado automáticamente para la persona
            empleado_id = cursor.lastrowid

            # Inserta los datos en la tabla empleados
            sql_empleado = "INSERT INTO empleados (id, salario, rut, contraseña, rol) VALUES (%s, %s, %s, %s, %s)"
            valores_empleado = (empleado_id, empleado.salario, empleado.rut, empleado.contraseña, empleado.rol)
            cursor.execute(sql_empleado, valores_empleado)

            self.conexion.commit()
            print(f"Empleado agregado correctamente con ID {empleado_id}.")
        except mysql.connector.Error as err:
            print(f"Error al agregar empleado: {err}")
        finally:
            cursor.close()

    # Método para verificar el rol de un usuario
    def verificar_usuario(self, rut, contraseña):
        if not self.conexion:
            print("La conexión a la base de datos no está disponible.")
            return None

        try:
            cursor = self.conexion.cursor()

            # Verificar si el RUT y la contraseña coinciden
            sql = "SELECT contraseña, rol FROM empleados WHERE rut = %s"
            cursor.execute(sql, (rut,))
            resultado = cursor.fetchone()

            if resultado:
                # Compara la contraseña cifrada
                contrasena_db = resultado[0]
                if contrasena_db == cifrar_contraseña(contraseña):  # Cifra la contraseña y la compara
                    return resultado[1]  # Devuelve el rol del usuario
                else:
                    print("Contraseña incorrecta.")
                    return None
            else:
                print("Usuario no encontrado.")
                return None
        except mysql.connector.Error as err:
            print(f"Error al verificar usuario: {err}")
            return None
        finally:
            cursor.close()

    # Método para modificar el salario de un empleado
    def modificar_empleado(self, empleado_id, nuevo_salario):
        if not self.conexion:
            print("La conexión a la base de datos no está disponible.")
            return

        try:
            cursor = self.conexion.cursor()
            sql = "UPDATE empleados SET salario = %s WHERE id = %s"
            cursor.execute(sql, (nuevo_salario, empleado_id))
            self.conexion.commit()
            print("Empleado modificado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al modificar empleado: {err}")
        finally:
            cursor.close()

    # Método para eliminar un empleado
    def eliminar_empleado(self, empleado_id):
        if not self.conexion:
            print("La conexión a la base de datos no está disponible.")
            return

        try:
            cursor = self.conexion.cursor()
            sql_empleado = "DELETE FROM empleados WHERE id = %s"
            cursor.execute(sql_empleado, (empleado_id,))

            sql_persona = "DELETE FROM personas WHERE id = %s"
            cursor.execute(sql_persona, (empleado_id,))

            self.conexion.commit()
            print("Empleado eliminado correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al eliminar empleado: {err}")
        finally:
            cursor.close()

# Funciones de validación de datos
def validar_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print("Por favor ingrese un número válido.")

def validar_int(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("Por favor ingrese un número entero válido.")

def validar_email(mensaje):
    while True:
        email = input(mensaje)
        if "@" in email and "." in email:
            return email
        else:
            print("Por favor ingrese un email válido.")

def validar_telefono(mensaje):
    while True:
        telefono = input(mensaje)
        if telefono.isdigit() and 9 <= len(telefono) <= 15:
            return telefono
        else:
            print("Por favor ingrese un número de teléfono válido (solo números, entre 9 y 15 dígitos).")

# Función para confirmar la contraseña
def ingresar_contraseña():
    while True:
        contraseña = input("Ingrese la contraseña: ")
        confirmar_contraseña = input("Confirme la contraseña: ")
        if contraseña == confirmar_contraseña:
            return contraseña
        else:
            print("Las contraseñas no coinciden. Intente nuevamente.")

# Menú para administradores
def menu_admin(db):
    while True:
        print("\nMenú de Administrador:")
        print("1. Agregar empleado")
        print("2. Modificar salario de empleado")
        print("3. Eliminar empleado")
        print("4. Salir")
        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del empleado: ")
            direccion = input("Ingrese la dirección del empleado: ")
            telefono = validar_telefono("Ingrese el teléfono del empleado: ")
            email = validar_email("Ingrese el email del empleado: ")
            salario = validar_float("Ingrese el salario del empleado: ")
            rut = input("Ingrese el RUT del empleado: ")
            contraseña = ingresar_contraseña()  # Llamada a la nueva función
            contraseña_cifrada = cifrar_contraseña(contraseña)
            rol = input("Ingrese el rol del empleado ('admin' o 'usuario'): ")

            empleado = Empleado(
                id=None,  # Se genera automáticamente en la base de datos
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                email=email,
                salario=salario,
                rut=rut,
                contraseña=contraseña_cifrada,
                rol=rol
            )

            db.agregar_empleado(empleado)

        elif opcion == "2":
            empleado_id = validar_int("Ingrese el ID del empleado cuyo salario desea modificar: ")
            nuevo_salario = validar_float("Ingrese el nuevo salario del empleado: ")
            db.modificar_empleado(empleado_id, nuevo_salario)

        elif opcion == "3":
            empleado_id = validar_int("Ingrese el ID del empleado que desea eliminar: ")
            db.eliminar_empleado(empleado_id)

        elif opcion == "4":
            print("Saliendo del menú de administrador.")
            break

        else:
            print("Opción no válida, por favor intente de nuevo.")

# Menú para usuarios (solo pueden consultar datos)
def menu_usuario():
    while True:
        print("\nMenú de Usuario:")
        print("1. Ver empleados")
        print("2. Ver proyectos")
        print("3. Salir")
        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            print("Funcionalidad de consulta de empleados aún no implementada.")
        elif opcion == "2":
            print("Funcionalidad de consulta de proyectos aún no implementada.")
        elif opcion == "3":
            print("Saliendo del menú de usuario.")
            break
        else:
            print("Opción no válida.")

def verificar_y_agregar_administrador(db):
    """
    Verifica si existe un administrador en la base de datos. 
    Si no existe, solicita los datos para agregar uno.
    """
    if not db.existe_administrador():
        print("No se ha encontrado ningún administrador en la base de datos.")
        print("Debe registrar un administrador para continuar.")

        # Solicitar datos del administrador
        nombre = input("Ingrese el nombre del administrador: ")
        direccion = input("Ingrese la dirección del administrador: ")
        telefono = validar_telefono("Ingrese el teléfono del administrador: ")
        email = validar_email("Ingrese el email del administrador: ")
        salario = validar_float("Ingrese el salario del administrador: ")
        rut = input("Ingrese el RUT del administrador: ")
        contraseña = ingresar_contraseña()
        contraseña_cifrada = cifrar_contraseña(contraseña)
        rol = 'admin'

        # Crear un objeto Empleado
        admin = Empleado(
            id=None,  # Se genera automáticamente en la base de datos
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            email=email,
            salario=salario,
            rut=rut,
            contraseña=contraseña_cifrada,
            rol=rol
        )

        # Agregar administrador a la base de datos
        db.agregar_empleado(admin)
        print("Administrador registrado correctamente.")
    else:
        print("Ya existe al menos un administrador en la base de datos.")


# Instancias de servicios API
json_placeholder = APIService("https://jsonplaceholder.typicode.com")
serper = APIService("https://api.serper.dev", api_key="6dd0dc45bb8e7193c5b6fd88309a56b12ed82817")

# Funciones para manejar interacciones con JSONPlaceholder
def menu_jsonplaceholder():
    """Menú para manejar datos desde JSONPlaceholder."""
    print("\nMenú de JSONPlaceholder:")
    print("1. Ver posts")
    print("2. Crear un nuevo post")
    print("3. Actualizar un post")
    print("4. Eliminar un post")
    print("5. Volver")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        # Solicita los primeros 5 posts
        posts = json_placeholder.get("posts")
        for post in posts[:5]:
            print(f"ID: {post['id']}, Título: {post['title']}")
    elif opcion == "2":
        # Crea un nuevo post
        nuevo_post = {
            "title": input("Título: "),
            "body": input("Contenido: "),
            "userId": 1
        }
        post_creado = json_placeholder.post("posts", nuevo_post)
        print("Post creado:", post_creado)
    elif opcion == "3":
        # Actualiza un post existente
        post_id = input("ID del post a actualizar: ")
        actualizado = {
            "title": input("Nuevo título: "),
            "body": input("Nuevo contenido: ")
        }
        post_actualizado = json_placeholder.put(f"posts/{post_id}", actualizado)
        print("Post actualizado:", post_actualizado)
    elif opcion == "4":
        # Elimina un post existente
        post_id = input("ID del post a eliminar: ")
        resultado = json_placeholder.delete(f"posts/{post_id}")
        print("Post eliminado:", resultado)
    elif opcion == "5":
        # Vuelve al menú principal
        return

# Función para manejar búsquedas con Serper.dev
def menu_serper():
    """Realiza búsquedas utilizando Serper.dev."""
    print("\nBúsqueda con Serper.dev:")
    query = input("Ingrese el término de búsqueda: ")
    resultados = serper.post("search", {"q": query})
    print("Resultados:")
    for resultado in resultados.get("organic", [])[:5]:
        print(f"Título: {resultado['title']}, URL: {resultado['link']}")

def menu_jsonplaceholder():
    """Menú para manejar datos desde JSONPlaceholder."""
    print("\nMenú de JSONPlaceholder:")
    print("1. Ver posts")
    print("2. Crear un nuevo post")
    print("3. Actualizar un post")
    print("4. Eliminar un post")
    print("5. Volver")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        # Solicita los primeros 5 posts
        posts = json_placeholder.get("posts")
        for post in posts[:5]:
            print(f"ID: {post['id']}, Título: {post['title']}")
    elif opcion == "2":
        # Crea un nuevo post
        nuevo_post = {
            "title": input("Título: "),
            "body": input("Contenido: "),
            "userId": 1
        }
        post_creado = json_placeholder.post("posts", nuevo_post)
        print("Post creado:", post_creado)
    elif opcion == "3":
        # Actualiza un post existente
        post_id = input("ID del post a actualizar: ")
        actualizado = {
            "title": input("Nuevo título: "),
            "body": input("Nuevo contenido: ")
        }
        post_actualizado = json_placeholder.put(f"posts/{post_id}", actualizado)
        print("Post actualizado:", post_actualizado)
    elif opcion == "4":
        # Elimina un post existente
        post_id = input("ID del post a eliminar: ")
        resultado = json_placeholder.delete(f"posts/{post_id}")
        print("Post eliminado:", resultado)
    elif opcion == "5":
        # Vuelve al menú principal
        return

def menu_serper():
    """Realiza búsquedas utilizando Serper.dev."""
    print("\nBúsqueda con Serper.dev:")
    query = input("Ingrese el término de búsqueda: ")  # Término a buscar
    resultados = serper.post("search", {"q": query})  # Realiza la búsqueda con el término ingresado
    
    # Imprime toda la respuesta para depurar
    print("Respuesta completa de Serper.dev:")
    print(resultados)
    
    # Muestra los primeros 5 resultados de búsqueda (si están disponibles)
    print("\nResultados:")
    if "organic" in resultados:
        for resultado in resultados["organic"][:5]:
            print(f"Título: {resultado.get('title')}, URL: {resultado.get('link')}")
    else:
        print("No se encontraron resultados o la clave 'organic' no está presente en la respuesta.")


# Menú principal
def menu():
    """Muestra el menú principal del programa."""
    db = BaseDeDatos()  # Instancia la conexión con la base de datos
    verificar_y_agregar_administrador(db)

    while True:
        print("\nSeleccione una opción:")
        print("1. Iniciar sesión")
        print("2. Consultar datos desde JSONPlaceholder")
        print("3. Realizar una búsqueda con Serper.dev")
        print("4. Salir")
        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            # Maneja el inicio de sesión
            rut = input("Ingrese el RUT del empleado: ")
            contraseña = input("Ingrese la contraseña del empleado: ")
            rol = db.verificar_usuario(rut, contraseña)

            if rol:
                print(f"Acceso concedido. Rol: {rol}")
                if rol == 'admin':
                    menu_admin(db)
                else:
                    menu_usuario()
            else:
                print("Login fallido.")

        elif opcion == "2":
            menu_jsonplaceholder()

        elif opcion == "3":
            menu_serper()

        elif opcion == "4":
            db.cerrar_conexion()
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida, por favor intente de nuevo.")

# Funciones de menú específicas por rol
def menu_admin(db):
    """Menú exclusivo para administradores."""
    print("Menú del administrador")

def menu_usuario():
    """Menú exclusivo para usuarios normales."""
    print("Menú del usuario")

# Inicia el programa
if __name__ == "__main__":
    menu()
