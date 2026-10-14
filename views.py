"""CONTROLADOR académico: nunca usa print() ni input()."""
from abc import ABC, abstractmethod

from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


class CrudBase(ABC):
    @abstractmethod
    def leer(self): pass

    @abstractmethod
    def obtener(self, id_registro): pass

    @abstractmethod
    def buscar(self, texto): pass

    @abstractmethod
    def siguiente(self): pass

    @abstractmethod
    def crear(self, datos): pass

    @abstractmethod
    def actualizar(self, id_registro, datos): pass

    @abstractmethod
    def eliminar(self, id_registro): pass


def _mayor_id_mas_uno(lista):
    mayor = 0
    for objeto in lista:
        if objeto.id > mayor:
            mayor = objeto.id
    return mayor + 1


# =====================================================================
class EstudianteController(CrudBase):

    def __init__(self, archivo="data/estudiantes.json"):
        self.gestor = GestorJSON(archivo)
        # LISTA de objetos Estudiante
        self.lista = [Estudiante.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([e.a_diccionario() for e in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "carnet"):   # TUPLA fija
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email):
                return f"Email inválido: '{email}'"
            # CONJUNTO: emails de los OTROS estudiantes (pertenencia instantánea)
            if email in {e.email for e in self.lista if e.id != id_actual}:
                return "Ese email ya está registrado"

        if "carnet" in datos:
            carnet = str(datos["carnet"]).strip().upper()
            if carnet == "":
                return "El carnet no puede quedar vacío"
            # CONJUNTO: carnets ya usados, para detectar duplicados al instante
            if carnet in {e.carnet.upper() for e in self.lista if e.id != id_actual}:
                return "Ese carnet ya está registrado"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_estudiante):
        for estudiante in self.lista:
            if estudiante.id == id_estudiante:
                return estudiante
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        if texto == "":
            return []
        encontrados = []
        # TUPLA de campos buscables
        for estudiante in self.lista:
            for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
                if texto in str(getattr(estudiante, campo)).lower():
                    encontrados.append(estudiante)
                    break
        return encontrados

    def siguiente(self):
        return _mayor_id_mas_uno(self.lista)

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error
        estudiante = Estudiante(self.siguiente(),
                                str(datos["nombre"]).strip().title(),
                                str(datos["apellido"]).strip().title(),
                                str(datos["email"]).strip().lower(),
                                str(datos["carnet"]).strip().upper(),
                                str(datos.get("carrera", "")).strip().title())
        self.lista.append(estudiante)
        self.guardar()
        return True, f"Estudiante creado: {estudiante.etiqueta()}"

    def actualizar(self, id_estudiante, datos):
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"
        if not datos:
            return False, "No se indicó ningún cambio"

        # DIFERENCIA de conjuntos: campos que no existen
        desconocidos = set(datos) - {"nombre", "apellido", "email", "carnet", "carrera"}
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_estudiante)      # ANTES de tocar el objeto
        if error:
            return False, error

        for campo, valor in datos.items():
            valor = str(valor).strip()
            if campo in ("nombre", "apellido", "carrera"):
                valor = valor.title()
            elif campo == "email":
                valor = valor.lower()
            elif campo == "carnet":
                valor = valor.upper()
            setattr(estudiante, campo, valor)

        self.guardar()
        return True, f"Estudiante {id_estudiante} actualizado"

    def eliminar(self, id_estudiante):
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"
        self.lista.remove(estudiante)
        self.guardar()
        return True, f"Estudiante {id_estudiante} eliminado"

    def carreras(self):
        """CONJUNTO: carreras distintas, sin repetidos."""
        return sorted({e.carrera for e in self.lista if e.carrera != ""})


# =====================================================================
class MateriaController(CrudBase):

    def __init__(self, archivo="data/materias.json"):
        self.gestor = GestorJSON(archivo)
        self.lista = [Materia.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([m.a_diccionario() for m in self.lista])

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "codigo", "creditos"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "codigo" in datos:
            codigo = str(datos["codigo"]).strip().upper()
            if codigo == "":
                return "El código no puede quedar vacío"
            # CONJUNTO de códigos de las OTRAS materias
            if codigo in {m.codigo.upper() for m in self.lista if m.id != id_actual}:
                return f"Ya existe una materia con código {codigo}"

        if "creditos" in datos:
            creditos = str(datos["creditos"]).strip()
            if not creditos.isdigit() or not (1 <= int(creditos) <= 10):
                return "Los créditos deben ser un entero entre 1 y 10"

        if "cupos" in datos and str(datos["cupos"]).strip() != "":
            cupos = str(datos["cupos"]).strip()
            if not cupos.isdigit() or not (0 <= int(cupos) <= Materia.CUPOS_MAXIMOS):
                return f"Los cupos deben ser un entero entre 0 y {Materia.CUPOS_MAXIMOS}"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_materia):
        for materia in self.lista:
            if materia.id == id_materia:
                return materia
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        if texto == "":
            return []
        return [m for m in self.lista
                if texto in m.nombre.lower() or texto in m.codigo.lower()]

    def siguiente(self):
        return _mayor_id_mas_uno(self.lista)

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error
        cupos = str(datos.get("cupos", "")).strip()
        materia = Materia(self.siguiente(),
                          str(datos["nombre"]).strip(),
                          str(datos["codigo"]).strip().upper(),
                          int(datos["creditos"]),
                          int(cupos) if cupos != "" else Materia.CUPOS_MAXIMOS)
        self.lista.append(materia)
        self.guardar()
        return True, f"Materia creada: {materia.etiqueta()}"

    def actualizar(self, id_materia, datos):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe una materia con id {id_materia}"
        if not datos:
            return False, "No se indicó ningún cambio"

        desconocidos = set(datos) - {"nombre", "codigo", "creditos", "cupos"}
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_materia)
        if error:
            return False, error

        if "nombre" in datos:
            materia.nombre = str(datos["nombre"]).strip()
        if "codigo" in datos:
            materia.codigo = str(datos["codigo"]).strip().upper()
        if "creditos" in datos:
            materia.creditos = int(datos["creditos"])
        if "cupos" in datos:
            materia.cupos = int(datos["cupos"])

        self.guardar()
        return True, f"Materia {id_materia} actualizada"

    def eliminar(self, id_materia):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe una materia con id {id_materia}"
        self.lista.remove(materia)
        self.guardar()
        return True, f"Materia {id_materia} eliminada"

    def materias_sin_cupo(self):
        return [m for m in self.lista if not m.hay_cupo()]


# =====================================================================
class MatriculaController(CrudBase):

    def __init__(self, estudiantes, materias, archivo="data/matriculas.json"):
        # USA a los otros dos controladores (los MISMOS que usa main.py)
        self.estudiantes = estudiantes
        self.materias = materias
        self.gestor = GestorJSON(archivo)
        self.lista = [Matricula.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([m.a_diccionario() for m in self.lista])

    def validar(self, datos):
        try:
            estudiante_id = int(datos.get("estudiante_id", 0))
            materia_id = int(datos.get("materia_id", 0))
        except (TypeError, ValueError):
            return "estudiante_id y materia_id deben ser números enteros"

        periodo = str(datos.get("periodo", "")).strip()
        if periodo == "":
            return "El periodo es obligatorio (ej. 2026-1)"

        if self.estudiantes.obtener(estudiante_id) is None:
            return f"No existe un estudiante con id {estudiante_id}"
        materia = self.materias.obtener(materia_id)
        if materia is None:
            return f"No existe una materia con id {materia_id}"
        if not materia.hay_cupo():
            return f"La materia {materia.codigo} no tiene cupos disponibles"

        # CONJUNTO de TUPLAS: la tupla (estudiante, materia, periodo) identifica
        # una matrícula; se compara junta, no cada dato por separado
        existentes = {(m.estudiante_id, m.materia_id, m.periodo) for m in self.lista}
        if (estudiante_id, materia_id, periodo) in existentes:
            return "Ese estudiante ya está matriculado en esa materia en ese periodo"

        nota = str(datos.get("nota", "")).strip()
        if nota != "" and not Materia.es_nota_valida(nota):
            return "La nota debe ser un número entre 0 y 20"
        return None

    def leer(self):
        return self.lista

    def obtener(self, id_matricula):
        for matricula in self.lista:
            if matricula.id == id_matricula:
                return matricula
        return None

    def buscar(self, texto):
        # Se busca por periodo, ej: "2026-1"
        texto = texto.strip()
        if texto == "":
            return []
        return [m for m in self.lista if texto in m.periodo]

    def siguiente(self):
        return _mayor_id_mas_uno(self.lista)

    def crear(self, datos):
        # datos = {"estudiante_id": 1, "materia_id": 2, "periodo": "2026-1"}
        error = self.validar(datos)
        if error:
            return False, error

        materia = self.materias.obtener(int(datos["materia_id"]))
        nota = str(datos.get("nota", "")).strip()
        matricula = Matricula(self.siguiente(), int(datos["estudiante_id"]),
                              materia.id, str(datos["periodo"]).strip(),
                              float(nota) if nota != "" else None)

        materia.ocupar_cupo()
        self.materias.guardar()              # cupo nuevo en materias.json
        self.lista.append(matricula)
        self.guardar()                       # matrícula en matriculas.json
        return True, f"Matrícula {matricula.id} registrada ({materia.codigo})"

    def actualizar(self, id_matricula, datos):
        return False, "Use 'registrar nota' o retire la matrícula y haga otra"

    def registrar_nota(self, id_matricula, nota):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe la matrícula {id_matricula}"
        if not Materia.es_nota_valida(nota):
            return False, "La nota debe ser un número entre 0 y 20"
        matricula.nota = float(nota)
        self.guardar()
        return True, f"Nota {matricula.nota:g} registrada: {matricula.estado()}"

    def eliminar(self, id_matricula):
        """Retirar matrícula: se borra y el cupo vuelve a la materia."""
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe la matrícula {id_matricula}"

        materia = self.materias.obtener(matricula.materia_id)
        if materia is not None:
            materia.liberar_cupo()
            self.materias.guardar()

        self.lista.remove(matricula)
        self.guardar()
        return True, f"Matrícula {id_matricula} retirada y cupo liberado"

    def retirar_matricula(self, id_matricula):
        return self.eliminar(id_matricula)

    def certificado(self, id_matricula):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return None

        # DICCIONARIOS ÍNDICE {id: objeto}: acceso directo sin recorrer
        indice_est = {e.id: e for e in self.estudiantes.leer()}
        indice_mat = {m.id: m for m in self.materias.leer()}
        estudiante = indice_est.get(matricula.estudiante_id)
        materia = indice_mat.get(matricula.materia_id)

        nota = f"{matricula.nota:g}" if matricula.nota is not None else "sin calificar"
        texto = f"CERTIFICADO #{matricula.id}   periodo: {matricula.periodo}\n"
        if estudiante:
            texto += f"Estudiante: {estudiante.nombre_completo()}   ({estudiante.carnet})\n"
        else:
            texto += "Estudiante: eliminado\n"
        if materia:
            texto += (f"Materia   : {materia.nombre}   ({materia.codigo}) · "
                      f"{materia.creditos} créditos\n")
        else:
            texto += "Materia   : eliminada\n"
        texto += "-" * 42 + "\n"
        texto += f"Nota      : {nota}\n"
        texto += f"Estado    : {matricula.estado()}"
        return texto

    def matriculas_por_estudiante(self):
        """DICCIONARIO de LISTAS: {estudiante_id: [matrículas]} con setdefault."""
        agrupadas = {}
        for matricula in self.lista:
            agrupadas.setdefault(matricula.estudiante_id, []).append(matricula)
        return agrupadas

    def promedio_de_estudiante(self, id_estudiante):
        """Promedio de sus notas registradas, o None si no tiene ninguna."""
        notas = [m.nota for m in self.lista
                 if m.estudiante_id == id_estudiante and m.nota is not None]
        if not notas:
            return None
        return round(sum(notas) / len(notas), 2)

    def total_aprobadas(self):
        return len([m for m in self.lista if m.esta_aprobada()])
