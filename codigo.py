# Clase base para Empleado
class Empleado:
    contador_id = 1

    def __init__(self, nombre, direccion, telefono, email, salario):
        self.id = Empleado.contador_id
        Empleado.contador_id += 1
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.salario = salario
        self.departamento = None
        self.proyectos = []

    def asignar_departamento(self, departamento):
        self.departamento = departamento

    def asignar_proyecto(self, proyecto):
        if proyecto not in self.proyectos:
            self.proyectos.append(proyecto)

    def __str__(self):
        return f"Empleado[{self.id}]: {self.nombre}, Email: {self.email}, Departamento: {self.departamento.nombre if self.departamento else 'N/A'}"

# Clase Departamento
class Departamento:
    def __init__(self, nombre, gerente):
        self.nombre = nombre
        self.gerente = gerente
        self.empleados = []

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)
        empleado.asignar_departamento(self)

    def __str__(self):
        return f"Departamento: {self.nombre}, Gerente: {self.gerente}, Empleados: {len(self.empleados)}"

# Clase Proyecto
class Proyecto:
    def __init__(self, nombre, descripcion, fecha_inicio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.empleados = []

    def asignar_empleado(self, empleado):
        self.empleados.append(empleado)
        empleado.asignar_proyecto(self)

    def __str__(self):
        return f"Proyecto: {self.nombre}, Fecha de inicio: {self.fecha_inicio}, Empleados asignados: {len(self.empleados)}"

# Clase RegistroTiempo para las horas trabajadas
class RegistroTiempo:
    def __init__(self, empleado, proyecto, fecha, horas, descripcion):
        self.empleado = empleado
        self.proyecto = proyecto
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion

    def __str__(self):
        return f"{self.fecha} - {self.empleado.nombre} en {self.proyecto.nombre}: {self.horas} horas - {self.descripcion}"

# Ejemplo de uso
if __name__ == "__main__":
    # Crear algunos empleados
    emp1 = Empleado("Juan Pérez", "Calle Falsa 123", "123456789", "juan@empresa.com", 50000)
    emp2 = Empleado("Ana López", "Avenida Siempre Viva 456", "987654321", "ana@empresa.com", 55000)

    # Crear un departamento y asignar empleados
    depto = Departamento("Desarrollo Sostenible", "Carlos Mendoza")
    depto.agregar_empleado(emp1)
    depto.agregar_empleado(emp2)

    # Crear un proyecto y asignar empleados
    proyecto = Proyecto("EcoProyecto", "Desarrollo de energías renovables", "2024-10-01")
    proyecto.asignar_empleado(emp1)
    proyecto.asignar_empleado(emp2)

    # Registrar horas trabajadas
    registro1 = RegistroTiempo(emp1, proyecto, "2024-10-25", 8, "Investigación de paneles solares")
    registro2 = RegistroTiempo(emp2, proyecto, "2024-10-26", 7, "Desarrollo de prototipos")

    # Mostrar información
    print(emp1)
    print(emp2)
    print(depto)
    print(proyecto)
    print(registro1)
    print(registro2)
