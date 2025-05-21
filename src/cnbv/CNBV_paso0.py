# ----------------------------------------------------------------------------------------
#  PASO0: VALIDAR REQUISITOS PREVIOS 
#  Autor: SteveCarpio-2024
# ----------------------------------------------------------------------------------------

import cfg.CNBV_variables as sTv
from   cfg.CNBV_librerias import *

# ----------------------------------------------------------------------------------------
#                                  FUNCIONES
# ----------------------------------------------------------------------------------------

# Función: Valida estructura de directorios CNBV
def valida_carpetas(ruta_carpeta):
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        print(f'Carpeta creada: {ruta_carpeta}')
    else:
        print(f'Validando carpeta: {ruta_carpeta}')

# Función: Borrar files creados CNBV
def borrar_archivos(ruta_carpeta, patron):
    # Construir la ruta completa con el patrón
    ruta_completa = os.path.join(ruta_carpeta, patron)
    
    # Encontrar todos los archivos que coincidan con el patrón
    archivos = glob.glob(ruta_completa)
    
    # Borrar cada archivo encontrado
    for archivo in archivos:
        os.remove(archivo)
        print(f'Archivo borrado: {archivo}')

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso0(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes):
    # Valida carpetas de CNBV
    valida_carpetas(sTv.var_RutaRaiz)
    valida_carpetas(sTv.var_RutaWebFiles)
    valida_carpetas(sTv.var_RutaInforme)
    valida_carpetas(sTv.var_RutaXls)

    # Borra files descargados de CNBV
    borrar_archivos(sTv.var_RutaWebFiles, f'*.html')      #  f'{var_NombreSalida}_*.html'
    borrar_archivos(sTv.var_RutaXls, f'*.xlsx')           #  f'{var_TipoDes}_{var_EJERCICIO}_{var_TRIMESTRE}__*.xlsx'
    borrar_archivos(sTv.var_RutaInforme, f'{var_NombreSalida}_Datos.xlsx')
    borrar_archivos(sTv.var_RutaInforme, f'{var_NombreSalida}_Final.xlsx')
    borrar_archivos(sTv.var_RutaInforme, f'{var_NombreSalida}_Totales.xlsx')

    print(" Requisitos previos ok ")
