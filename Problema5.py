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
    pass

#h
def prueba_asignar_agenda():
    pass



#
#SECCIÓN ALGORÍTMICA (Integración)
#

#1. Prólogo

#2. Resolución
#i

#3. Epílogo


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