"""
SECCIÓN DECLARATIVA
Descripción:
Recursos:
"""

import struct
import os

FORMATO = '<i30s24s16sB'
TAM_REGISTRO = struct.calcsize(FORMATO)

ruta = os.path.join(os.path.dirname(__file__), 'pacientes.dat')

#
#SECCIÓN FUNCIONES
#

#MÓDULO 1
#a
def empaquetar_paciente(dni, apellido, nombre, telefono, prioridad):
    """
    Empaqueta los datos de un paciente en formato binario
    Precondición: dni es un entero, apellido, nombre y telefono son strings, prioridad es un entero de 1 a 3
    Postcondición: paciente_pack es un paquete de bytes para ser escritos en un archivo binario
    """
    #truncado de cadenas largas
    apellido = apellido[0:30]
    nombre = nombre[0:24]
    telefono = telefono[0:16]

    #codificación UTF-8
    apellido_utf8 = apellido.encode('utf-8')
    nombre_utf8 = nombre.encode('utf-8')
    telefono_utf8 = telefono.encode('utf-8')

    paciente_pack = struct.pack(FORMATO, dni, apellido_utf8, nombre_utf8, telefono_utf8, prioridad)
    return paciente_pack

def desempaquetar_paciente(paciente):
    """
    Desempaqueta un bloque de bytes correspondiente a un paciente y devuelve sus datos
    Precondición: paciente es un paquete de bytes provenientes de un archivo binario
    Postcondición: dni es un entero, apellido, nombre y telefono son strings, prioridad es un entero de 1 a 3 y se devuelven como tupla
    """
    dni, apellido, nombre, telefono, prioridad = struct.unpack(FORMATO, paciente)

    #decodificación y removido de ceros de relleno
    apellido_utf8 = apellido.rstrip(b'\x00').decode('utf-8')
    nombre_utf8 = nombre.rstrip(b'\x00').decode('utf-8')
    telefono_utf8 = telefono.rstrip(b'\x00').decode('utf-8')

    #retornamos como tupla en vez de lista porque el paciente es una unidad y no necesitamos mutabilidad
    return (dni, apellido_utf8, nombre_utf8, telefono_utf8, prioridad)

#b
def crear_archivo_pacientes(ruta, lista_pacientes):
    """
    Crea un archivo binario con una lista de pacientes
    Precondición: ruta es un string representando un directorio válido, lista paciente es una tupla de forma dni, apellido, nombre, telefono, prioridad
    Efecto secundario: se crea un archivo binario con un listado de pacientes en la ruta especificada
    """
    with open(ruta, 'wb') as f:
        for paciente in lista_pacientes:
            dni, apellido, nombre, telefono, prioridad = paciente
            f.write(empaquetar_paciente(dni, apellido, nombre, telefono, prioridad))
        f.close()

def leer_paciente(archivo, k):
    """
    Lee la información de un paciente según su posición en el archivo binario
    Precondición: archivo es un handle de archivo, k es un entero positivo
    Postcondición: paciente es un paquete de bytes con los datos del paciente a leer
    """
    archivo.seek(k * TAM_REGISTRO)
    paciente = archivo.read(TAM_REGISTRO)

    return paciente



#MÓDULO 2
#c
def construir_indices(ruta):
    """
    Crea índices para los pacientes del archivo binario, uno según sus nombres y otro según sus DNI
    Precondición: ruta es un string representando un directorio válido
    Postcondición: indice_por_dni es un diccionario con items de la forma {clave: DNI, valor: posición k del registro en el archivo}
                   indice_por_apellido es un diccionario con items de la forma {clave: apellido, valor: lista de posiciones}
    """
    indice_por_dni = {}
    indice_por_apellido = {}
    with open(ruta, 'rb') as f:
        for indice, paciente_pack in enumerate(leer_archivo_pacientes(f)):
            paciente = desempaquetar_paciente(paciente_pack)
            dni = paciente[0]
            apellido = paciente[1]

            indice_por_dni[dni] = indice

            indice_por_apellido[apellido] = indice_por_apellido.get(apellido, [])
            indice_por_apellido[apellido].append(indice)
        f.close()

    return indice_por_dni, indice_por_apellido

def leer_archivo_pacientes(archivo):
    """
    Devuelve cada paciente del archivo binario
    Precondición: archivo es un handle de archivo
    Postcondición: se devuelve un generador que itera sobre los registros de pacientes del archivo (sin desempaquetar)
    """
    i = 0
    paciente_pack = leer_paciente(archivo, i)
    while paciente_pack:
        yield paciente_pack
        i += 1
        paciente_pack = leer_paciente(archivo, i)

#d
def buscar_por_dni(archivo, indice_por_dni, dni):
    paciente_pack = leer_paciente(archivo, indice_por_dni[dni])
    return desempaquetar_paciente(paciente_pack)


#MÓDULO 3
#e
def listar_pacientes_ordenados(ruta, criterio):
    """
    Lee todos los pacientes del archivo binario y devuelve una lista ordenada según el criterio.

    Precondición: es un string apuntando a un archivo binario existente y criterio una cadena de
                    texto: apellido o prioridad.
    Postcondición: Devuelve una lista ordenada de los pacietes segun el criterio. Si el criterio es apellido,
                    se ordena alfabeticamente. Si el criterio es prioridad, se ordena por la prioridad osea
                    del 1 a 3, y los que tengan la misma proridad se los ordena de forma alfabetica por
                    el apellido.
    """
    pacientes = []

    # Lectura y preparación de datos
    with open(ruta, "rb") as f:
        for paciente_pack in leer_archivo_pacientes(f):
            paciente = desempaquetar_paciente(paciente_pack)
            apellido = paciente[1]
            prioridad = paciente[4]

            if criterio == "apellido":
                pacientes.append((apellido.lower(), paciente))
            elif criterio == "prioridad":
                pacientes.append((prioridad, apellido.lower(), paciente))
            else:
                pacientes.append((0, paciente))

    lista_ordenada_pacientes = merge_sort(pacientes)

    #Se desarma la estructura y se devuelven los datos de forma limpia
    resultado = []
    for par in lista_ordenada_pacientes:
        resultado.append(par[-1])

    return resultado

def merge_sort(secuencia):
    """Ordena una secuencia comparándola por divide y vencerás.

    Precondición: secuencia es una lista de elementos comparables entre sí.
    Postcondición: devuelve una nueva lista con los mismos elementos en
                   orden no decreciente; secuencia no se modifica.
    Complejidad: O(n log n) en tiempo, O(n) en espacio auxiliar.
    """
    # --- Prólogo: caso base de la recursión -------------------------
    if len(secuencia) <= 1:
        return list(secuencia)

    # --- Resolución: dividir, recurrir, combinar --------------------
    medio = len(secuencia) >> 1
    mitad_izq = merge_sort(secuencia[:medio])
    mitad_der = merge_sort(secuencia[medio:])
    resultado = _fusionar(mitad_izq, mitad_der)

    # --- Epílogo: devolver la solución del problema -----------------
    return resultado


def _fusionar(izq, der):
    """Fusiona dos listas ordenadas en una sola lista ordenada.

    Precondición: izq y der están ordenadas en forma no decreciente.
    Postcondición: devuelve una nueva lista con todos los elementos
                   de izq y der, en orden no decreciente y estable.
    """
    # --- Prólogo: estructuras de trabajo ----------------------------
    resultado = []
    i, j = 0, 0
    n_izq, n_der = len(izq), len(der)

    # --- Resolución: avanzar ambos punteros tomando el menor --------
    while i < n_izq and j < n_der:
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])

    # --- Epílogo: devolver lista fusionada --------------------------
    return resultado

#f
"""
Justificación: La estabilidad de un algoritmo de ordenamiento garantiza que si dos elementos tienen
la misma clave de ordenación, conservarán el mismo orden relativo original. Para resolver el criterio
de prioridad que te dice de agrupar por prioridad del 1 al 3 y, en si tienen la misma prioridad
ordenar por apellido, se usa una estrategia de dos pasadas consecutivas: En la primer pasada se
ordena la lista completa alfabéticamente por apellido y en la segunda pasada se vuelve a ordenar la
lista pero esta vez por el nivel de prioridad. Si el segundo ordenamiento no fuera estable entonces
cuando se ordena por prioridad se perderia el orden alfabetico que se genero el la primera pasada
cuando se ordeno por apellido entonces no cumpliria con su funcion de ordenar por proridad y
apellido y solo simplemente ordenaria por prioridad haciendo que todos los que tengan la misma
prioridad esten juntos pero no de forma ordenada (alfabeticamente) sino que esten mezclados sin
un orden entre ellos.
"""


#MÓDULO 4
#g
def asignar_agenda(pacientes_del_dia, franjas, disponibilidad):
    """
    Asigna cada paciente a una franja horaria compatible por backtracking.

    Precondicion: pacientes_del_dia es una lista de dicts con clave 'dni';
                  franjas es una lista de identificadores de franja (ej: 9, 9.5, 10...);
                  disponibilidad es un dict {dni: [franjas_válidas]}.
                  Cada franja puede recibir a lo sumo un paciente.
    Postcondicion: devuelve un dict {franja: dni} con una asignacion valida
                   donde cada paciente queda en una franja compatible, o
                   None si no existe ninguna asignacion posible.
    """
    #Prólogo: estado parcial vacio
    asignacion = {}

    #Resolución: explorar desde el primer paciente
    resultado = _backtrack_agenda(pacientes_del_dia, franjas, disponibilidad, asignacion, 0)

    #Epílogo: devolver la asignación encontrada (o None)
    return resultado


def _backtrack_agenda(pacientes_del_dia, franjas, disponibilidad, asignacion, indice):
    """
    Explora recursivamente el árbol de asignaciones posibles.

    Precondicion: pacientes_del_dia es la lista completa; franjas es la lista de franjas disponibles; disponibilidad es el dict
                  de franjas válidas por dni, asignacion es el estado parcial
                  actual (franja -> dni), indice es el paciente a asignar ahora.
    Postcondicion: devuelve una asignacion completa valida que extiende al
                   estado parcial dado, o None si no existe ninguna.
    """
    #Caso base: todos los pacientes fueron asignados
    if indice == len(pacientes_del_dia):
        return dict(asignacion)

    #Caso recursivo: intentar cada franja disponible para este paciente
    paciente = pacientes_del_dia[indice]
    dni = paciente['dni']

    for franja in disponibilidad.get(dni, []):
        if franja not in franjas: #franja no existe en el dia
            continue
        if franja in asignacion: #poda, esta franja ya tiene un paciente asignado
            continue

        asignacion[franja] = dni
        resultado = _backtrack_agenda(pacientes_del_dia, franjas, disponibilidad, asignacion, indice + 1)

        if resultado is not None:
            return resultado
        
        del asignacion[franja]
    return None

#h
def prueba_asignar_agenda():
    """Testea prueba_asignar_agenda con un caso con solucion y uno sobre-restringido."""

    print("Test de prueba_asignar_agenda:")
    pacientes = [
        {'dni': 10000000, 'apellido': 'Garcia',   'nombre': 'Ana'},
        {'dni': 10101010, 'apellido': 'Lopez',    'nombre': 'Luis'},
        {'dni': 11111111, 'apellido': 'Martinez', 'nombre': 'Eva'},
    ]
    franjas = [9, 9.5, 10, 10.5, 11]

    #Caso 1: tiene solucion
    disponibilidad_valida = {
        10000000: [9, 10],
        10101010: [9, 9.5],
        11111111: [10.5, 11],
    }
    resultado = asignar_agenda(pacientes, franjas, disponibilidad_valida)
    print("\nCaso con solución:")
    print(resultado)
    print("Cada paciente tiene una franja valida.")

    #Caso 2: sobre-restringido, sin solucion
    disponibilidad_imposible = {
        10000000: [9],
        10101010: [9],
        11111111: [9],
    }
    resultado_imposible = asignar_agenda(pacientes, franjas, disponibilidad_imposible)
    print("\nCaso sobre-restringido:")
    print(resultado_imposible)

'''

Análisis: backtracking con poda vs. fuerza bruta
    Nota: la fuerza bruta se implementa con una lista de tuplas (franja, dni)
    en lugar de un diccionario. Si se usara un diccionario, asignar dos
    pacientes a la misma franja pisaría el valor anterior,
    devolviendo resultados incorrectos.

    Fuerza bruta recorre el mismo árbol pero verifica unicidad solo al
    llegar a una rama completa (caso base). 

    Con poda (if franja in asignacion), el algoritmo descarta una rama
    completa en cuanto detecta que la franja ya está ocupada, sin explorar
    los pacientes que vienen despues.
    
    Caso con solucion (Ana:[9, 10], Luis:[9, 9.5], Eva:[10.5, 11]):
      - Fuerza bruta: 6 intentos. Llega al caso base con cada combinación
        completa y recién ahí verifica si hay franjas repetidas.
      - Con poda: exploró 4 intentos. Ana tomo la 9, Luis intento la 9
        (poda), tomó la 9.5, Eva tomó la 10.5 entonces solucion encontrada.
        Las 4 combinaciones restantes no se exploraron.

    Caso imposible (los tres solo pueden a las 9):
      - Fuerza bruta: 3 intentos. Llega al caso base con [(9,Ana),(9,Luis),
        (9,Eva)], detecta las franjas repetidas y devuelve None.
      - Con poda: exploró 2 intentos. Ana tomó la 9, Luis intentó la 9
        (poda) y no tuvo más opciones. Eva nunca fue evaluada.
        Backtrack a Ana, no mas opciones entonces devuelve None.
    '''

prueba_asignar_agenda()



#
#SECCIÓN ALGORÍTMICA (Integración)
#

#1. Prólogo
ruta_pacientes = os.path.join(os.path.dirname(__file__), 'pacientes_integracion.dat')
franjas = [9.0, 10.0, 11.0, 12.0, 13.0]

# Definición de pacientes para la integración (DNI, Apellido, Nombre, Teléfono, Prioridad)
pacientes_iniciales = [
    (12345678, "Perez", "Juan", "11223344", 2),
    (23456789, "Gomez", "Maria", "22334455", 1),
    (34567890, "Rodriguez", "Pedro", "33445566", 3),
    (45678901, "Lopez", "Ana", "44556677", 1),
    (56789012, "Martinez", "Carlos", "55667788", 2)
]

disponibilidad = {
    12345678: [9.0, 10.0],
    23456789: [10.0, 11.0],
    34567890: [11.0, 12.0],
    45678901: [9.0, 11.0],
    56789012: [12.0, 13.0]
}

#2. Resolución
#i
# Guardamos los pacientes en el archivo binario
crear_archivo_pacientes(ruta_pacientes, pacientes_iniciales)

# Construimos los índices sobre el archivo binario (Módulo 2)
indice_por_dni, indice_por_apellido = construir_indices(ruta_pacientes)

# Obtenemos la lista de pacientes ordenada por prioridad y apellido (Módulo 3)
pacientes_ordenados_tuplas = listar_pacientes_ordenados(ruta_pacientes, "prioridad")

# Convertimos las tuplas de pacientes al formato de diccionario requerido por el Módulo 4
pacientes_del_dia = []
for p in pacientes_ordenados_tuplas:
    pacientes_del_dia.append({
        'dni': p[0],
        'apellido': p[1],
        'nombre': p[2],
        'telefono': p[3],
        'prioridad': p[4]
    })

# Asignamos la agenda utilizando backtracking (Módulo 4)
agenda_asignada = asignar_agenda(pacientes_del_dia, franjas, disponibilidad)

#3. Epílogo
print("\n=== Agenda del Día ===")
if agenda_asignada:
    print(f"Se logró asignar una agenda compatible para los {len(pacientes_del_dia)} pacientes:")
    # Para mostrar la agenda ordenada por franja horaria
    franjas_ordenadas = sorted(agenda_asignada.keys())
    
    # Abrimos el archivo para buscar los datos completos de los pacientes usando el índice
    with open(ruta_pacientes, 'rb') as f:
        for franja in franjas_ordenadas:
            dni_paciente = agenda_asignada[franja]
            # Buscamos el paciente por DNI directamente en el archivo binario usando el índice (Módulo 2)
            paciente = buscar_por_dni(f, indice_por_dni, dni_paciente)
            dni, apellido, nombre, telefono, prioridad = paciente
            print(f"  Horario {franja:4.1f} hs -> Paciente: {apellido}, {nombre} (DNI: {dni}, Prioridad: {prioridad})")
else:
    print("No se encontró una asignación de agenda compatible con la disponibilidad de los pacientes.")

# Limpieza del archivo de pacientes de integración
if os.path.exists(ruta_pacientes):
    os.remove(ruta_pacientes)



#4 Test
if __name__ == '__main__':
    print("Evaluación - Módulo 3")

    # 1.Prólogo: Definir un archivo de prueba y datos desordenados
    RUTA_TEST = "pacientes_test.dat"

    datos_prueba = [
        (40000000, "Pérez", "Juan", "11223344", 2),
        (20000000, "Alvarez", "Anahí", "55667788", 1),
        (30000000, "Gonzales", "María", "99001122", 1),
        (10000000, "Blanco", "Carlos", "33445566", 3),
        (50000000, "Alvarez", "Bruno", "44556677", 2)
    ]

    print("Creando archivo de prueba")
    crear_archivo_pacientes(RUTA_TEST, datos_prueba)

    try:
        #Evaluación del criterio apellido
        print("\nEvaluando criterio apellido")

        resultado_modulo_apellido = listar_pacientes_ordenados(RUTA_TEST, "apellido")

        resultado_esperado_apellido = sorted(datos_prueba, key=lambda p: p[1].lower())

        # Validación algorítmica
        for i in range(len(resultado_modulo_apellido)):
            assert resultado_modulo_apellido[i][0] == resultado_esperado_apellido[i][0]

        print("El criterio 'apellido' coincide exactamente con sorted().")

        # Evaluación del criterio prioridad
        print("\nEvaluando criterio prioridad")

        resultado_modulo_prioridad = listar_pacientes_ordenados(RUTA_TEST, "prioridad")

        resultado_esperado_prioridad = sorted(
            datos_prueba,
            key=lambda p: (p[4], p[1].lower())
        )

        # Validación algorítmica
        for i in range(len(resultado_modulo_prioridad)):
            assert resultado_modulo_prioridad[i][0] == resultado_esperado_prioridad[i][0]
        print("El criterio prioridad coincide exactamente con sorted().")
        print("\nTodas las pruebas del modulo 3 pasaron correctamente.")

    except AssertionError:
        #Si en algun punto no son iguales el sorted y el ordenamiento hecho entonces imprime esto
        print("\nEl orden obtenido no es igual al de sorted().")

    finally:
        # Limpieza del archivo temporal en el disco
        if os.path.exists(RUTA_TEST):
            os.remove(RUTA_TEST)
            print("\nArchivo de prueba borrado con éxito.")