"""VISTA académica: solo menús, input() y print()."""
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import EstudianteController, MateriaController, MatriculaController

estudiantes = EstudianteController()
materias = MateriaController()
matriculas = MatriculaController(estudiantes, materias)    # los MISMOS controladores


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    """Sirve para los tres modelos: cada uno sabe mostrarse (polimorfismo)."""
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


def editar(controlador, objeto, campos):
    """Pide los campos a cambiar y llama al controlador (lo usan estudiantes y materias)."""
    imprimir_info(f"Editando: {objeto.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")
    cambios = {}
    for campo in campos:
        nuevo = input(f"{campo.capitalize()} [{getattr(objeto, campo)}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo
    mostrar_resultado(*controlador.actualizar(objeto.id, cambios))


# ---------------------------- ESTUDIANTES ----------------------------
def crear_estudiante():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {"nombre": input("Nombre: "), "apellido": input("Apellido: "),
             "email": input("Email: "), "carnet": input("Carnet (ej. EST2026001): "),
             "carrera": input("Carrera: ")}
    mostrar_resultado(*estudiantes.crear(datos))
    pausa()


def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "Todavía no hay estudiantes.")
    pausa()


def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, email, carnet o carrera: ")
    mostrar_lista(estudiantes.buscar(termino), f"Nadie coincide con '{termino}'.")
    pausa()


def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    id_est = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_est)
    if estudiante is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(estudiante)
        promedio = matriculas.promedio_de_estudiante(id_est)
        imprimir_info(f"Promedio: {promedio if promedio is not None else 'sin notas'}")
    pausa()


def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    estudiante = estudiantes.obtener(pedir_entero("Id: "))
    if estudiante is None:
        imprimir_error("No encontrado")
        return pausa()
    editar(estudiantes, estudiante, ("nombre", "apellido", "email", "carnet", "carrera"))
    pausa()


def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    estudiante = estudiantes.obtener(pedir_entero("Id: "))
    if estudiante is None:
        imprimir_error("No encontrado")
        return pausa()
    imprimir_info(f"Se eliminará: {estudiante.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*estudiantes.eliminar(estudiante.id))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# ---------------------------- MATERIAS ----------------------------
def crear_materia():
    imprimir_titulo("CREAR MATERIA")
    datos = {"nombre": input("Nombre: "), "codigo": input("Código (ej. MAT101): "),
             "creditos": input("Créditos (1-10): "),
             "cupos": input("Cupos (Enter = 30): ")}
    mostrar_resultado(*materias.crear(datos))
    pausa()


def listar_materias():
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer(), "Todavía no hay materias.")
    pausa()


def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    mostrar_lista(materias.buscar(input("Nombre o código: ")), "Sin coincidencias.")
    pausa()


def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")
    materia = materias.obtener(pedir_entero("Id: "))
    if materia is None:
        imprimir_error("No encontrada")
    else:
        mostrar_detalle(materia)
    pausa()


def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")
    materia = materias.obtener(pedir_entero("Id: "))
    if materia is None:
        imprimir_error("No encontrada")
        return pausa()
    editar(materias, materia, ("nombre", "codigo", "creditos", "cupos"))
    pausa()


def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA")
    materia = materias.obtener(pedir_entero("Id: "))
    if materia is None:
        imprimir_error("No encontrada")
        return pausa()
    imprimir_info(f"Se eliminará: {materia.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*materias.eliminar(materia.id))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# ---------------------------- MATRÍCULAS ----------------------------
def matricular():
    imprimir_titulo("MATRICULAR")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Materias:")
    mostrar_lista(materias.leer())

    datos = {"estudiante_id": pedir_entero("\nId del estudiante: "),
             "materia_id": pedir_entero("Id de la materia: "),
             "periodo": input("Periodo (ej. 2026-1): ")}
    if datos["estudiante_id"] is None or datos["materia_id"] is None:
        imprimir_error("Los ids deben ser números enteros")
        return pausa()
    mostrar_resultado(*matriculas.crear(datos))
    pausa()


def listar_matriculas():
    imprimir_titulo("MATRÍCULAS")
    mostrar_lista(matriculas.leer(), "Todavía no hay matrículas.")
    pausa()


def registrar_nota():
    imprimir_titulo("REGISTRAR NOTA")
    id_mat = pedir_entero("Id de la matrícula: ")
    if id_mat is None:
        imprimir_error("El id debe ser un número entero")
        return pausa()
    nota = input("Nota (0-20): ").replace(",", ".")
    mostrar_resultado(*matriculas.registrar_nota(id_mat, nota))
    pausa()


def ver_certificado():
    imprimir_titulo("CERTIFICADO")
    texto = matriculas.certificado(pedir_entero("Id de la matrícula: "))
    if texto is None:
        imprimir_error("No existe esa matrícula")
    else:
        print(texto)
    pausa()


def retirar_matricula():
    imprimir_titulo("RETIRAR MATRÍCULA")
    id_mat = pedir_entero("Id de la matrícula: ")
    if id_mat and confirmar("Se liberará el cupo. ¿Confirma?"):
        mostrar_resultado(*matriculas.retirar_matricula(id_mat))
    else:
        imprimir_info("Operación cancelada")
    pausa()


def matriculas_de_estudiante():
    imprimir_titulo("MATRÍCULAS DE UN ESTUDIANTE")
    id_est = pedir_entero("Id del estudiante: ")
    lista = matriculas.matriculas_por_estudiante().get(id_est, [])
    mostrar_lista(lista, "Ese estudiante no tiene matrículas.")
    promedio = matriculas.promedio_de_estudiante(id_est)
    if promedio is not None:
        imprimir_info(f"Promedio: {promedio}")
    pausa()


def resumen():
    imprimir_titulo("RESUMEN")
    print(f"  Estudiantes       : {len(estudiantes.leer())}")
    print(f"  Carreras          : {', '.join(estudiantes.carreras()) or '-'}")
    print(f"  Materias          : {len(materias.leer())}")
    sin = materias.materias_sin_cupo()
    print(f"  Materias sin cupo : {', '.join(m.codigo for m in sin) or 'ninguna'}")
    print(f"  Matrículas        : {len(matriculas.leer())}")
    print(f"  Aprobadas         : {matriculas.total_aprobadas()}")
    pausa()


# ---------------------------- MENÚS ----------------------------
MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante), "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante), "4": ("Ver por id", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante), "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}
MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia), "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia), "4": ("Ver por id", ver_materia),
    "5": ("Actualizar", actualizar_materia), "6": ("Eliminar", eliminar_materia),
    "0": ("Volver", None),
}
MENU_MATRICULAS = {
    "1": ("Matricular", matricular), "2": ("Ver todas", listar_matriculas),
    "3": ("Registrar nota", registrar_nota), "4": ("Ver certificado", ver_certificado),
    "5": ("Retirar matrícula", retirar_matricula),
    "6": ("Matrículas de un estudiante", matriculas_de_estudiante),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _f) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()
        tecla = input("Opción: ").strip()
        if tecla not in opciones:
            imprimir_error("Opción no válida")
            pausa()
            continue
        _texto, funcion = opciones[tecla]
        if funcion is None:
            break
        funcion()


def main():
    while True:
        imprimir_titulo("SISTEMA ACADÉMICO")
        print("  1. Estudiantes\n  2. Materias\n  3. Matrículas\n  4. Resumen\n  0. Salir\n")
        tecla = input("Opción: ").strip()
        if tecla == "1":
            ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2":
            ejecutar_menu("MATERIAS", MENU_MATERIAS)
        elif tecla == "3":
            ejecutar_menu("MATRÍCULAS", MENU_MATRICULAS)
        elif tecla == "4":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
