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
    contador_id = 1  # Atributo de clase para generar un ID único por empleado

    def __init__(self, nombre, direccion, telefono, email, salario):
        super().__init__(nombre, direccion, telefono, email)
        self.id = Empleado.contador_id
        Empleado.contador_id += 1
        self.salario = salario

    def presentarse(self):
        return f"Soy {self.nombre}."

# Clase para manejar la base de datos
class BaseDeDatos:
    def __init__(self):
        self.conexion = conectar_db()

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")

    # Método para agregar un empleado
    def agregar_empleado(self, empleado):
        cursor = self.conexion.cursor()
        sql_persona = "INSERT INTO personas (nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s)"
        valores_persona = (empleado.nombre, empleado.direccion, empleado.telefono, empleado.email)
        cursor.execute(sql_persona, valores_persona)

        sql_empleado = "INSERT INTO empleados (id, salario) VALUES (%s, %s)"
        valores_empleado = (empleado.id, empleado.salario)
        cursor.execute(sql_empleado, valores_empleado)

        self.conexion.commit()
        cursor.close()
        print("Empleado agregado correctamente.")

    # Método para modificar un empleado
    def modificar_empleado(self, empleado_id, nuevo_salario):
        cursor = self.conexion.cursor()
        sql = "UPDATE empleados SET salario = %s WHERE id = %s"
        cursor.execute(sql, (nuevo_salario, empleado_id))
        self.conexion.commit()
        cursor.close()
        print("Empleado modificado correctamente.")

    # Método para eliminar un empleado
    def eliminar_empleado(self, empleado_id):
        cursor = self.conexion.cursor()
        sql_empleado = "DELETE FROM empleados WHERE id = %s"
        cursor.execute(sql_empleado, (empleado_id,))

        sql_persona = "DELETE FROM personas WHERE id = %s"
        cursor.execute(sql_persona, (empleado_id,))

        self.conexion.commit()
        cursor.close()
        print("Empleado eliminado correctamente.")

# Función para mostrar el menú y procesar las opciones
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
            # Agregar empleado
            nombre = input("Ingrese el nombre del empleado: ")
            direccion = input("Ingrese la dirección del empleado: ")
            telefono = input("Ingrese el teléfono del empleado: ")
            email = input("Ingrese el email del empleado: ")
            salario = float(input("Ingrese el salario del empleado: "))
            empleado = Empleado(nombre, direccion, telefono, email, salario)
            db.agregar_empleado(empleado)

        elif opcion == "2":
            # Modificar empleado
            empleado_id = int(input("Ingrese el ID del empleado a modificar: "))
            nuevo_salario = float(input("Ingrese el nuevo salario del empleado: "))
            db.modificar_empleado(empleado_id, nuevo_salario)

        elif opcion == "3":
            # Eliminar empleado
            empleado_id = int(input("Ingrese el ID del empleado a eliminar: "))
            db.eliminar_empleado(empleado_id)

        elif opcion == "4":
            # Salir
            db.cerrar_conexion()
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

# Ejecución del programa
if __name__ == "__main__":
    menu()
