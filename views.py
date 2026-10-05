import json
import os
from models import Estudiante

class GestorEstudiantes:
    def __init__(self, ruta="data/estudiantes.json"):
        self.ruta = ruta
        self.estudiantes = []
        self.carnets = set()
        self.cargar()

    def cargar(self):
        if not os.path.exists(self.ruta):
            return
        with open(self.ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        for d in datos:
            estudiante = Estudiante(**d)
            self.estudiantes.append(estudiante)
            self.carnets.add(estudiante.carnet)

    def guardar(self):
        os.makedirs("data", exist_ok=True)
        datos = [e.a_diccionario() for e in self.estudiantes]
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def obtener_por_id(self, id):
        for e in self.estudiantes:
            if e.id == id:
                return e
        return None

    def crear_estudiante(self, carnet, nombre, apellido, materias):
        if carnet in self.carnets:
            return False, "El carnet ya existe"
        if len(self.estudiantes) == 0:
            nuevo_id = 1
        else:
            nuevo_id = self.estudiantes[-1].id + 1
        estudiante = Estudiante(nuevo_id, carnet, nombre, apellido, materias)
        self.estudiantes.append(estudiante)
        self.carnets.add(carnet)
        self.guardar()
        return True, "Estudiante creado"

    def obtener_todos(self):
        return self.estudiantes

    def buscar_estudiantes(self, texto):
        texto = texto.lower()
        resultado = []
        for e in self.estudiantes:
            if texto in e.nombre.lower() or texto in e.apellido.lower() or texto in e.carnet.lower():
                resultado.append(e)
        return resultado

    def actualizar_estudiante(self, id, nombre, apellido, materias):
        estudiante = self.obtener_por_id(id)
        if estudiante is None:
            return False, "Estudiante no encontrado"
        estudiante.nombre = nombre
        estudiante.apellido = apellido
        estudiante.materias = materias
        self.guardar()
        return True, "Estudiante actualizado"

    def eliminar_estudiante(self, id):
        estudiante = self.obtener_por_id(id)
        if estudiante is None:
            return False, "Estudiante no encontrado"
        self.estudiantes.remove(estudiante)
        self.carnets.remove(estudiante.carnet)
        self.guardar()
        return True, "Estudiante eliminado"
