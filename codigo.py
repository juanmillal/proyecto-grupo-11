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
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    @abstractmethod
    def presentarse(self):
        pass

# Clase Empleado, heredando de Persona
class Empleado(Persona):
    def __init__(self, id, nombre, direccion, telefono, email, salario):
        super().__init__(nombre, direccion, telefono, email)
        self.id = id  # Inicialmente es None; será asignado por la base de datos
        self.salario = salario

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
            sql_empleado = "INSERT INTO empleados (id, salario) VALUES (%s, %s)"
            valores_empleado = (empleado_id, empleado.salario)
            cursor.execute(sql_empleado, valores_empleado)

            self.conexion.commit()
            print(f"Empleado agregado correctamente con ID {empleado_id}.")
        except mysql.connector.Error as err:
            print(f"Error al agregar empleado: {err}")
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

# Función para mostrar el menú principal
def menu():
    db = BaseDeDatos()

    while True:
        print("\nSeleccione una opción:")
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
            empleado = Empleado(None, nombre, direccion, telefono, email, salario)
            db.agregar_empleado(empleado)

        elif opcion == "2":
            empleado_id = validar_int("Ingrese el ID del empleado a modificar: ")
            nuevo_salario = validar_float("Ingrese el nuevo salario del empleado: ")
            db.modificar_empleado(empleado_id, nuevo_salario)

        elif opcion == "3":
            empleado_id = validar_int("Ingrese el ID del empleado a eliminar: ")
            db.eliminar_empleado(empleado_id)

        elif opcion == "4":
            db.cerrar_conexion()
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

# Ejecución del programa
if __name__ == "__main__":
    menu()
