from views import GestorEstudiantes

class Controlador:
    def __init__(self):
        self.gestor = GestorEstudiantes()

    def crear_estudiante(self, carnet, nombre, apellido, materias):
        return self.gestor.crear_estudiante(carnet, nombre, apellido, materias)

    def obtener_todos(self):
        return self.gestor.obtener_todos()

    def buscar_estudiantes(self, texto):
        return self.gestor.buscar_estudiantes(texto)

    def actualizar_estudiante(self, id, nombre, apellido, materias):
        return self.gestor.actualizar_estudiante(id, nombre, apellido, materias)

    def eliminar_estudiante(self, id):
        return self.gestor.eliminar_estudiante(id)

    def agregar_nota(self, id, materia, nota):
        estudiante = self.gestor.obtener_por_id(id)
        if estudiante is None:
            return False, "Estudiante no encontrado"
        if not isinstance(nota, (int, float)) or nota < 0 or nota > 20:
            return False, "La nota debe ser un número entre 0 y 20"
        estudiante.notas[materia] = nota
        self.gestor.guardar()
        return True, "Nota agregada"

    def ver_promedio(self, id):
        estudiante = self.gestor.obtener_por_id(id)
        if estudiante is None:
            return False, "Estudiante no encontrado"
        return True, estudiante.promedio()

    def materias_ofertadas(self):
        materias = set()
        for e in self.gestor.obtener_todos():
            materias.update(e.materias)
        return materias

    def estudiantes_en_comun(self, id_a, id_b):
        a = self.gestor.obtener_por_id(id_a)
        b = self.gestor.obtener_por_id(id_b)
        if a is None or b is None:
            return False, "Estudiante no encontrado"
        return True, set(a.materias) & set(b.materias)
