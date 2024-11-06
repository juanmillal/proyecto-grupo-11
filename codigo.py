from abc import ABC, abstractmethod
import mysql.connector

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

# Clase abstracta Persona
class Persona(ABC):
    def __init__(self, nombre, direccion, telefono, email):
        # Inicializa los atributos de la persona
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    @abstractmethod
    def presentarse(self):
        pass

# Clase Empleado, heredando de Persona
class Empleado(Persona):
    contador_id = 1  # Atributo de clase para generar un ID único por empleado

    def __init__(self, nombre, direccion, telefono, email, salario):
        # Llama al constructor de la clase base (Persona)
        super().__init__(nombre, direccion, telefono, email)
        self.id = Empleado.contador_id  # Asigna un ID único para el empleado
        Empleado.contador_id += 1  # Incrementa el contador para el siguiente empleado
        self.salario = salario  # Asigna el salario al empleado

    def presentarse(self):
        # Método para que el empleado se presente
        return f"Soy {self.nombre}."

# Clase para manejar la base de datos
class BaseDeDatos:
    def __init__(self):
        self.conexion = conectar_db()  # Se conecta a la base de datos

    def cerrar_conexion(self):
        # Cierra la conexión a la base de datos
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")

    # Método para agregar un empleado
    def agregar_empleado(self, empleado):
        cursor = self.conexion.cursor()
        # Inserta los datos de la persona en la tabla "personas"
        sql_persona = "INSERT INTO personas (nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s)"
        valores_persona = (empleado.nombre, empleado.direccion, empleado.telefono, empleado.email)
        cursor.execute(sql_persona, valores_persona)

        # Inserta los datos específicos del empleado (salario) en la tabla "empleados"
        sql_empleado = "INSERT INTO empleados (id, salario) VALUES (%s, %s)"
        valores_empleado = (empleado.id, empleado.salario)
        cursor.execute(sql_empleado, valores_empleado)

        # Realiza el commit de los cambios en la base de datos
        self.conexion.commit()
        cursor.close()  # Cierra el cursor
        print("Empleado agregado correctamente.")

    # Método para modificar un empleado
    def modificar_empleado(self, empleado_id, nuevo_salario):
        cursor = self.conexion.cursor()
        # Actualiza el salario del empleado según su ID
        sql = "UPDATE empleados SET salario = %s WHERE id = %s"
        cursor.execute(sql, (nuevo_salario, empleado_id))
        # Realiza el commit de los cambios
        self.conexion.commit()
        cursor.close()  # Cierra el cursor
        print("Empleado modificado correctamente.")

    # Método para eliminar un empleado
    def eliminar_empleado(self, empleado_id):
        cursor = self.conexion.cursor()
        # Elimina los datos del empleado de la tabla "empleados"
        sql_empleado = "DELETE FROM empleados WHERE id = %s"
        cursor.execute(sql_empleado, (empleado_id,))

        # Elimina los datos del empleado de la tabla "personas"
        sql_persona = "DELETE FROM personas WHERE id = %s"
        cursor.execute(sql_persona, (empleado_id,))

        # Realiza el commit de los cambios
        self.conexion.commit()
        cursor.close()  # Cierra el cursor
        print("Empleado eliminado correctamente.")

# Función para validar datos de tipo float (salarios)
def validar_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))  # Pide un valor de tipo float
            return valor  # Retorna el valor si es válido
        except ValueError:
            print("Por favor ingrese un número válido.")  # Si ocurre un error, pide nuevamente el dato

# Función para validar datos de tipo int (ID del empleado)
def validar_int(mensaje):
    while True:
        try:
            valor = int(input(mensaje))  # Pide un valor de tipo entero
            return valor  # Retorna el valor si es válido
        except ValueError:
            print("Por favor ingrese un número entero válido.")  # Si ocurre un error, pide nuevamente el dato

# Función para validar un email
def validar_email(mensaje):
    while True:
        email = input(mensaje)  # Solicita el email del usuario
        if "@" in email and "." in email:  # Verifica que tenga el formato adecuado
            return email  # Retorna el email si es válido
        else:
            print("Por favor ingrese un email válido.")  # Si no es válido, lo solicita nuevamente

# Función para validar el número de teléfono
def validar_telefono(mensaje):
    while True:
        telefono = input(mensaje)  # Solicita el número de teléfono
        if telefono.isdigit() and 9 <= len(telefono) <= 15:  # Verifica que sea numérico y tenga entre 9 y 15 caracteres
            return telefono  # Retorna el teléfono si es válido
        else:
            print("Por favor ingrese un número de teléfono válido (solo números, entre 9 y 15 dígitos).")

# Función para mostrar el menú y procesar las opciones
def menu():
    db = BaseDeDatos()  # Crea una instancia de la clase BaseDeDatos

    while True:
        # Muestra el menú con las opciones disponibles
        print("\nSeleccione una opción:")
        print("1. Agregar empleado")
        print("2. Modificar salario de empleado")
        print("3. Eliminar empleado")
        print("4. Salir")
        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            # Agregar empleado
            nombre = input("Ingrese el nombre del empleado: ")
            direccion = input("Ingrese la dirección del empleado: ")
            telefono = validar_telefono("Ingrese el teléfono del empleado: ")  # Validación del teléfono
            email = validar_email("Ingrese el email del empleado: ")  # Validación del email
            salario = validar_float("Ingrese el salario del empleado: ")  # Validación del salario
            empleado = Empleado(nombre, direccion, telefono, email, salario)  # Crea un objeto de la clase Empleado
            db.agregar_empleado(empleado)  # Llama al método para agregar el empleado a la base de datos

        elif opcion == "2":
            # Modificar empleado
            empleado_id = validar_int("Ingrese el ID del empleado a modificar: ")  # Validación del ID
            nuevo_salario = validar_float("Ingrese el nuevo salario del empleado: ")  # Validación del nuevo salario
            db.modificar_empleado(empleado_id, nuevo_salario)  # Llama al método para modificar el salario

        elif opcion == "3":
            # Eliminar empleado
            empleado_id = validar_int("Ingrese el ID del empleado a eliminar: ")  # Validación del ID
            db.eliminar_empleado(empleado_id)  # Llama al método para eliminar el empleado

        elif opcion == "4":
            # Salir
            db.cerrar_conexion()  # Cierra la conexión a la base de datos
            print("Saliendo del programa.")  # Imprime mensaje de salida
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")  # Si la opción es incorrecta, muestra un mensaje

# Ejecución del programa
if __name__ == "__main__":
    menu()  # Llama a la función para mostrar el menú
