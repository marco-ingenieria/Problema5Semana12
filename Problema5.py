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

def merge_sort():
    pass

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
