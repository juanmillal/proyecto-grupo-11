from abc import ABC, abstractmethod
import mysql.connector

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Deja vacío si no tienes contraseña para root
            database="trabajo11"  # Nombre de la base de datos
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
        self.departamento_id = None  # Inicialmente el empleado no tiene departamento

    def asignar_departamento(self, departamento_id):
        self.departamento_id = departamento_id

    def presentarse(self):
        return f"Soy {self.nombre}."


# Clase Departamento
class Departamento:
    def __init__(self, nombre, gerente):
        self.nombre = nombre
        self.gerente = gerente

# Clase Proyecto
class Proyecto:
    def __init__(self, nombre, descripcion, fecha_inicio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio

# Clase RegistroTiempo
class RegistroTiempo:
    def __init__(self, empleado_id, proyecto_id, fecha, horas, descripcion):
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion


# Clase para manejar la base de datos
class BaseDeDatos:
    def __init__(self):
        self.conexion = conectar_db()

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")

    def insertar_persona(self, persona):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO personas (nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s)"
        valores = (persona.nombre, persona.direccion, persona.telefono, persona.email)
        cursor.execute(sql, valores)
        self.conexion.commit()
        cursor.close()

    def insertar_empleado(self, empleado):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO empleados (id, salario) VALUES (%s, %s)"
        valores = (empleado.id, empleado.salario)
        cursor.execute(sql, valores)
        self.conexion.commit()
        cursor.close()

    def insertar_departamento(self, departamento):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO departamentos (id, nombre, gerente) VALUES (%s, %s, %s)"
        cursor.execute(sql, (1, departamento.nombre, departamento.gerente))  # Cambia el ID según necesites
        self.conexion.commit()
        cursor.close()

    def obtener_empleados(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM empleados")
        empleados = cursor.fetchall()
        cursor.close()
        return empleados

    def agregar_registro_tiempo(self, registro):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO registros_tiempo (empleado_id, proyecto_id, fecha, horas, descripcion) VALUES (%s, %s, %s, %s, %s)"
        valores = (registro.empleado_id, registro.proyecto_id, registro.fecha, registro.horas, registro.descripcion)
        cursor.execute(sql, valores)
        self.conexion.commit()
        cursor.close()

# Ejemplo de uso
if __name__ == "__main__":
    db = BaseDeDatos()
    
    # Crear empleados
    emp1 = Empleado("Juan Pérez", "Calle Falsa 123", "123456789", "juan@empresa.com", 50000)
    emp2 = Empleado("Ana López", "Avenida Siempre Viva 456", "987654321", "ana@empresa.com", 55000)

    # Guardar empleados en la base de datos
    db.insertar_persona(emp1)
    db.insertar_persona(emp2)
    db.insertar_empleado(emp1)
    db.insertar_empleado(emp2)

    # Crear y guardar departamento
    depto = Departamento("Desarrollo Sostenible", "Carlos Mendoza")
    db.insertar_departamento(depto)

    # Agregar registros de tiempo
    registro1 = RegistroTiempo(emp1.id, 1, "2024-10-25", 8, "Investigación de paneles solares")
    registro2 = RegistroTiempo(emp2.id, 1, "2024-10-26", 7, "Desarrollo de prototipos")
    db.agregar_registro_tiempo(registro1)
    db.agregar_registro_tiempo(registro2)

    # Obtener y mostrar empleados
    empleados = db.obtener_empleados()
    for empleado in empleados:
        print(empleado)

    # Cerrar conexión
    db.cerrar_conexion()
