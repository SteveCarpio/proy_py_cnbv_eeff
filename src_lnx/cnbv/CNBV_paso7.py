# ----------------------------------------------------------------------------------------
#  PASO7: SUBIR DATOS ORACLE
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.CNBV_variables as sTv
from   cfg.CNBV_librerias import *
from   cfg.CNBV_conection import *

# ----------------------------------------------------------------------------------------
#                             FUNCIONES VARIAS
# ----------------------------------------------------------------------------------------
# Lectua del EXCEL de Entrada
def lectura_df(var_NombreSalida):
    df_curl = pd.read_excel(f"{sTv.var_RutaInforme}{var_NombreSalida}_Final.xlsx",  sheet_name="DATA")
    df_tot1 = pd.read_excel(f"{sTv.var_RutaInforme}{var_NombreSalida}_Final.xlsx",  sheet_name="TOTALES1")
    df_tot2 = pd.read_excel(f"{sTv.var_RutaInforme}{var_NombreSalida}_Final.xlsx",  sheet_name="TOTALES2")
    return df_curl, df_tot1, df_tot2

# Tratamiento de los DF de entrada
def tratamiento_df(df_curl, df_tot1, df_tot2, var_EJERCICIO, var_TRIMESTRE):
    df_tot1["Periodo"] = f"{var_EJERCICIO} - {var_TRIMESTRE}"
    df_tot2.columns = ['Iden', 'FEnvio', 'ClavePizarra', 'Periodo', 'Taxonomia', 'TActivos', 'TActivosCirculantes',   # Renombro las columnas
                        'TCapitalContable', 'TPasivosCirculantes', 'TPasivos', 'UtilPerdOperacion', 'UtilPerdNeta']
    # Re-Organización de columnas
    col_curl_orden = ['Periodo', 'ClavePizarra', 'Iden', 'FEnvio', 'Taxonomia', 'FileXbrl', 'TipoFile', 'CURL']
    col_tot1_orden = ['Periodo', 'Iden', 'Hoja', 'ColumnaA', 'ColumnaB', 'ColumnaC', 'File']
    col_tot2_orden = ['Periodo', 'ClavePizarra', 'Iden', 'FEnvio', 'Taxonomia', 'TActivos', 'TActivosCirculantes', 
                        'TCapitalContable', 'TPasivosCirculantes', 'TPasivos', 'UtilPerdOperacion', 'UtilPerdNeta']
    # Re-Ordenación de columnas
    df_curl = df_curl.reindex(columns=col_curl_orden)
    df_tot1 = df_tot1.reindex(columns=col_tot1_orden)
    df_tot2 = df_tot2.reindex(columns=col_tot2_orden)
    # Ordenación del contenido de la tabla
    df_curl_ordenado = df_curl.sort_values(['ClavePizarra', 'FEnvio'], ascending=[True, False])
    df_tot1_ordenado = df_tot1.sort_values(['Iden'], ascending=[True])
    df_tot2_ordenado = df_tot2.sort_values(['ClavePizarra', 'FEnvio'], ascending=[True, False])
    # Resetar el valor del indice 
    df_curl_ordenado = df_curl_ordenado.reset_index(drop=True)
    df_tot1_ordenado = df_tot1_ordenado.reset_index(drop=True)
    df_tot2_ordenado = df_tot2_ordenado.reset_index(drop=True)
    return df_curl_ordenado, df_tot1_ordenado, df_tot2_ordenado

def subir_oracle_curl(df_curl_ordenado):
    if len(df_curl_ordenado) > 0:
        print(f"Subir datos a la tabla Oracle: {sTv.var_Ora_TAB3}")                 # type: ignore
        print(df_curl_ordenado)
    else:
        print(f"No hay datos para subir a la tabla oracle:  {sTv.var_Ora_TAB3}")    # type: ignore

def subir_oracle_tot1(df_tot1_ordenado):
    if len(df_tot1_ordenado) > 0:
        print(f"Subir datos a la tabla Oracle: {sTv.var_Ora_TAB1}")                 # type: ignore
        print(df_tot1_ordenado)
    else:
        print(f"No hay datos para subir a la tabla oracle:  {sTv.var_Ora_TAB1}")    # type: ignore

def subir_oracle_tot2(df_tot2_ordenado):
    if len(df_tot2_ordenado) > 0:
        print(f"Subir datos a la tabla Oracle: {sTv.var_Ora_TAB2}")                 # type: ignore
        print(df_tot2_ordenado)
    else:
        print(f"No hay datos para subir a la tabla oracle:  {sTv.var_Ora_TAB2}")    # type: ignore


# ----------------------------------------------------------------------------------------
#                             INICIO DE PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso7(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE):     #, var_TIPODESCARGA, var_TipoDes2, var_Fechas1, var_Entorno):
    print("Paso7 - Subir datos oracle")
    print(f"{var_NombreSalida}_Final.xlsx")
    print(var_EJERCICIO)      # año
    print(var_TRIMESTRE)      # 1,2,3,4,4D
    #print(var_TIPODESCARGA)  # 1,2
    #print(var_TipoDes2)      # Trimestral
    #print(var_Fechas1)       # 2025-11-26
    #print(var_Entorno)       # DEV / PRO

    # Verificar si existe el file de entrada
    ruta_excel = Path(f"{sTv.var_RutaInforme}{var_NombreSalida}_Final.xlsx")            # type: ignore
    if ruta_excel.exists():
        # Lectua del EXCEL a un DATAFRAME 
        df_curl, df_tot1, df_tot2 = lectura_df(var_NombreSalida) 
        # Tratamiento de los DATAFRAMES
        df_curl_ordenado, df_tot1_ordenado, df_tot2_ordenado = tratamiento_df(df_curl, df_tot1, df_tot2, var_EJERCICIO, var_TRIMESTRE)

        # Oracle, Parámetros de conexión:
        oracle_dns = sTv.var_Ora_DNS    # type: ignore
        oracle_uid = sTv.var_Ora_UID    # type: ignore
        oracle_pwd = sTv.var_Ora_PWD    # type: ignore

        # Establecer Conexión Oracle:
        conexion, cursor = Oracle_Establece_Conexion(oracle_dns, oracle_uid, oracle_pwd)

        # Valida que siga conectado a oracle
        if (conexion != None) or (cursor != None):

            subir_oracle_curl(df_curl_ordenado)
            subir_oracle_tot1(df_tot1_ordenado)
            subir_oracle_tot2(df_tot2_ordenado)

        # Cierro de conexiones Oracle y libero memoria
        Oracle_Cerrar_Conexion(conexion, cursor)
    else:

        print(f"\n ¡ No existe el file: {ruta_excel} !")
        print(f" ¡ No podemos subir datos a Oracle de los Estados Financieros !")

    
    
