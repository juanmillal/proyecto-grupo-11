from abc import ABC, abstractmethod

# Clase abstracta Persona
class Persona(ABC):  # La clase abstracta 'Persona' define una plantilla básica
    def __init__(self, nombre, direccion, telefono, email):
        # Constructor que inicializa los atributos básicos para cualquier persona
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    @abstractmethod
    def presentarse(self):  # Método abstracto que obliga a las subclases a implementar 'presentarse'
        pass

# Clase Empleado, heredando de Persona
class Empleado(Persona):  # 'Empleado' es una subclase que hereda de 'Persona'
    contador_id = 1  # Atributo de clase para generar un ID único por empleado

    def __init__(self, nombre, direccion, telefono, email, salario):
        # Llamamos al constructor de la clase base 'Persona' con 'super()'
        super().__init__(nombre, direccion, telefono, email)
        # Asignación de un ID único al empleado
        self.id = Empleado.contador_id
        Empleado.contador_id += 1
        # Atributos específicos de 'Empleado'
        self.salario = salario
        self.departamento = None  # Inicialmente el empleado no tiene departamento
        self.proyectos = []  # Lista de proyectos en los que participa el empleado

    def asignar_departamento(self, departamento):  # Asigna un departamento al empleado
        self.departamento = departamento

    def asignar_proyecto(self, proyecto):  # Añade un proyecto a la lista de proyectos del empleado
        if proyecto not in self.proyectos:  # Evita duplicados en la lista de proyectos
            self.proyectos.append(proyecto)

    def presentarse(self):  # Implementación del método abstracto de 'Persona'
        return f"Soy {self.nombre}, trabajo en {self.departamento.nombre if self.departamento else 'N/A'}."

    def __str__(self):  # Representación en cadena del empleado
        return f"Empleado[{self.id}]: {self.nombre}, Email: {self.email}, Departamento: {self.departamento.nombre if self.departamento else 'N/A'}"

# Clase Departamento
class Departamento:
    def __init__(self, nombre, gerente):
        # Inicialización de los atributos del departamento
        self.nombre = nombre
        self.gerente = gerente
        self.empleados = []  # Lista de empleados en el departamento

    def agregar_empleado(self, empleado):  # Agrega un empleado al departamento
        self.empleados.append(empleado)  # Añade al empleado a la lista de empleados
        empleado.asignar_departamento(self)  # Asigna este departamento al empleado

    def __str__(self):  # Representación en cadena del departamento
        return f"Departamento: {self.nombre}, Gerente: {self.gerente}, Empleados: {len(self.empleados)}"

# Clase Proyecto
class Proyecto:
    def __init__(self, nombre, descripcion, fecha_inicio):
        # Inicialización de los atributos del proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.empleados = []  # Lista de empleados asignados al proyecto
        self.registros_tiempo = []  # Composición: lista de registros de tiempo

    def asignar_empleado(self, empleado):  # Asigna un empleado al proyecto
        self.empleados.append(empleado)  # Añade al empleado a la lista de empleados
        empleado.asignar_proyecto(self)  # Añade el proyecto a la lista de proyectos del empleado

    def agregar_registro_tiempo(self, registro):  # Añade un registro de tiempo al proyecto
        self.registros_tiempo.append(registro)

    def __str__(self):  # Representación en cadena del proyecto
        return f"Proyecto: {self.nombre}, Fecha de inicio: {self.fecha_inicio}, Empleados asignados: {len(self.empleados)}"

# Clase RegistroTiempo
class RegistroTiempo:
    def __init__(self, empleado, proyecto, fecha, horas, descripcion):
        # Inicialización de los atributos del registro de tiempo
        self.empleado = empleado
        self.proyecto = proyecto
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion

    def __str__(self):  # Representación en cadena del registro de tiempo
        return f"{self.fecha} - {self.empleado.nombre} en {self.proyecto.nombre}: {self.horas} horas - {self.descripcion}"

# Ejemplo de uso
if __name__ == "__main__":
    # Crear algunos empleados
    emp1 = Empleado("Juan Pérez", "Calle Falsa 123", "123456789", "juan@empresa.com", 50000)
    emp2 = Empleado("Ana López", "Avenida Siempre Viva 456", "987654321", "ana@empresa.com", 55000)

    # Crear un departamento y asignar empleados
    depto = Departamento("Desarrollo Sostenible", "Carlos Mendoza")
    depto.agregar_empleado(emp1)  # Asignar 'emp1' al departamento
    depto.agregar_empleado(emp2)  # Asignar 'emp2' al departamento

    # Crear un proyecto y asignar empleados
    proyecto = Proyecto("EcoProyecto", "Desarrollo de energías renovables", "2024-10-01")
    proyecto.asignar_empleado(emp1)  # Asignar 'emp1' al proyecto
    proyecto.asignar_empleado(emp2)  # Asignar 'emp2' al proyecto

    # Registrar horas trabajadas en el proyecto
    registro1 = RegistroTiempo(emp1, proyecto, "2024-10-25", 8, "Investigación de paneles solares")
    registro2 = RegistroTiempo(emp2, proyecto, "2024-10-26", 7, "Desarrollo de prototipos")
    proyecto.agregar_registro_tiempo(registro1)  # Añadir el registro1 al proyecto
    proyecto.agregar_registro_tiempo(registro2)  # Añadir el registro2 al proyecto

    # Mostrar información
    print(emp1.presentarse())  # Muestra la presentación de 'emp1'
    print(emp2.presentarse())  # Muestra la presentación de 'emp2'
    print(depto)  # Muestra información del departamento
    print(proyecto)  # Muestra información del proyecto
    print(registro1)  # Muestra información del registro de tiempo 1
    print(registro2)  # Muestra información del registro de tiempo2

