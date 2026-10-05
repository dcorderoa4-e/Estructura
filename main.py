from controlador import Controlador

controlador = Controlador()

def mostrar(e):
    print(e.id, e.carnet, e.nombre, e.apellido, e.materias, e.notas)

def pedir_materias():
    texto = input("Materias separadas por coma: ")
    return [m.strip() for m in texto.split(",") if m.strip() != ""]

def opcion_crear():
    carnet = input("Carnet: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    materias = pedir_materias()
    ok, mensaje = controlador.crear_estudiante(carnet, nombre, apellido, materias)
    print(mensaje)

def opcion_listar():
    lista = controlador.obtener_todos()
    if len(lista) == 0:
        print("No hay estudiantes")
    for e in lista:
        mostrar(e)

def opcion_buscar():
    texto = input("Buscar: ")
    for e in controlador.buscar_estudiantes(texto):
        mostrar(e)

def opcion_actualizar():
    id = int(input("ID: "))
    nombre = input("Nuevo nombre: ")
    apellido = input("Nuevo apellido: ")
    materias = pedir_materias()
    ok, mensaje = controlador.actualizar_estudiante(id, nombre, apellido, materias)
    print(mensaje)

def opcion_eliminar():
    id = int(input("ID: "))
    ok, mensaje = controlador.eliminar_estudiante(id)
    print(mensaje)

def opcion_agregar_nota():
    id = int(input("ID: "))
    materia = input("Materia: ")
    try:
        nota = float(input("Nota (0-20): "))
    except ValueError:
        print("Escribe un número")
        return
    ok, mensaje = controlador.agregar_nota(id, materia, nota)
    print(mensaje)

def opcion_promedio():
    id = int(input("ID: "))
    ok, resultado = controlador.ver_promedio(id)
    if ok:
        print("Promedio:", round(resultado, 2))
    else:
        print(resultado)

def opcion_en_comun():
    id_a = int(input("ID del primer estudiante: "))
    id_b = int(input("ID del segundo estudiante: "))
    ok, resultado = controlador.estudiantes_en_comun(id_a, id_b)
    if ok:
        print("Materias en común:", resultado if resultado else "ninguna")
    else:
        print(resultado)

def opcion_materias():
    print("Materias ofertadas:", controlador.materias_ofertadas())

def menu():
    while True:
        print("\n--- Sistema de Estudiantes ---")
        print("1. Registrar estudiante")
        print("2. Listar estudiantes")
        print("3. Buscar estudiante")
        print("4. Actualizar estudiante")
        print("5. Eliminar estudiante")
        print("6. Agregar nota")
        print("7. Ver promedio")
        print("8. Materias en común")
        print("9. Materias ofertadas")
        print("0. Salir")
        opcion = input("Elige: ")
        if opcion == "1":
            opcion_crear()
        elif opcion == "2":
            opcion_listar()
        elif opcion == "3":
            opcion_buscar()
        elif opcion == "4":
            opcion_actualizar()
        elif opcion == "5":
            opcion_eliminar()
        elif opcion == "6":
            opcion_agregar_nota()
        elif opcion == "7":
            opcion_promedio()
        elif opcion == "8":
            opcion_en_comun()
        elif opcion == "9":
            opcion_materias()
        elif opcion == "0":
            break
        else:
            print("Opción no válida")

menu()
