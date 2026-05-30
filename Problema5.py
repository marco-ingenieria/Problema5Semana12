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
def empaquetar_paciente():
    pass

def desempaquetar_paciente():
    pass

#b
def crear_archivo_pacientes(ruta, lista_pacientes):
    pass

def leer_paciente(archivo, k):
    pass



#MÓDULO 2
#c
def construir_indices(ruta):
    indice_por_dni = {}

    indice_por_apellido = {}

#d
def buscar_por_dni(archivo, indice_por_dni, dni):
    pass


#MÓDULO 3
#e
def listar_pacientes_ordenados():
   pass

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
Justificación:
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
