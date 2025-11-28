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
    print(f"\nSe han leído {len(df_curl)} registros para: df_curl")
    print(f"Se han leído {len(df_tot1)} registros para: df_tot1")
    print(f"Se han leído {len(df_tot2)} registros para: df_tot2")
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

# Delete Oracle: Borro los registros de un periodo
def borrar_resgistros(conexion, cursor, periodo, tabla_ora):
    sql_contar = f"SELECT COUNT(*) FROM {tabla_ora} WHERE PERIODO = :v_PERIODO"
    cursor.execute(sql_contar, v_PERIODO=periodo)
    filas_a_eliminar, = cursor.fetchone()
    if filas_a_eliminar > 0: 
        sql_delete = f"DELETE FROM {tabla_ora} WHERE PERIODO = :v_PERIODO"
        cursor.execute(sql_delete, v_PERIODO=periodo)
        conexion.commit()
        filas_eliminadas = cursor.rowcount
        print(f"AVISO: existen: {filas_eliminadas}, registros del periodo: {periodo}, en la tabla: {tabla_ora}")
        print("Se procede a lanzar el DELETE de esos registros antes de lanzar el UPDATE")
    else:
        print(f"OK: NO existen datos del periodo:{periodo}, en la tabla:{tabla_ora}, se procede a hacer el UPDATE")

# Update Oracle: CNBV_EEFF_FILECURL
def subir_oracle_curl(conexion, cursor, df_curl_ordenado):
    tab_ora = sTv.var_Ora_TAB3   # type: ignore
    if len(df_curl_ordenado) > 0:
        print(f"UPDATE ORACLE {tab_ora}: se van a subir {len(df_curl_ordenado)} registros\n")      
        print(df_curl_ordenado)
        
        # Recorro el DataFrame registro por registro
        for index, row in df_curl_ordenado.iterrows():
            v_Periodo         = row['Periodo']
            v_ClavePizarra    = row['ClavePizarra']
            v_Iden            = row['Iden']
            v_FEnvio          = row['FEnvio']
            v_Taxonomia       = row['Taxonomia']
            v_FileXbrl        = row['FileXbrl']
            v_TipoFile        = row['TipoFile']
            v_CURL            = row['CURL']

            # Normalizar NaN/NaT a None
            if pd.isna(v_Iden):     #  revisar, en codigo ori bolsas no da error
                v_Iden = None

            try:
                # Ejecutar INSERT con binds nombrados (oracledb)
                sql = f"""
                INSERT INTO {tab_ora}               
                    (Periodo, ClavePizarra, Iden, FEnvio, Taxonomia, FileXbrl, TipoFile, CURL)
                VALUES
                    (:Periodo, :ClavePizarra, :Iden, :FEnvio, :Taxonomia, :FileXbrl, :TipoFile, :CURL)
                """  
                params = {
                    "Periodo": v_Periodo, 
                    "ClavePizarra": v_ClavePizarra, 
                    "Iden": v_Iden, 
                    "FEnvio": v_FEnvio, 
                    "Taxonomia": v_Taxonomia, 
                    "FileXbrl": v_FileXbrl, 
                    "TipoFile": v_TipoFile, 
                    "CURL": v_CURL
                }
                cursor.execute(sql, params) 

                print(Fore.CYAN + f"Registro {index + 1} insertado en el servidor PYTHON ORACLE ({v_Periodo})")  
                print(Fore.WHITE + f"  {v_Periodo} - {v_ClavePizarra} - {v_Iden} - {v_FEnvio} - {v_Taxonomia} - {v_FileXbrl}")
                print(Fore.WHITE + f"  {v_TipoFile} - {v_CURL}\n")
            except Exception as e:
                # Puedes afinar el manejo según el código de error (duplicado, constraint, etc.)
                print(Fore.RED + f"Registro {index + 1} no insertado en el servidor PYTHON ORACLE: {e}") 
                print(Fore.WHITE + f"  {v_Periodo} - {v_ClavePizarra} - {v_Iden} - {v_FEnvio} - {v_Taxonomia} - {v_FileXbrl}")
                print(Fore.WHITE + f"  {v_TipoFile} - {v_CURL}\n")

        # Oracle, Confirma los cambios
        conexion.commit() 
    else:
        print(f"No hay datos para subir a la tabla oracle:  {tab_ora}")                       

# Update Oracle: CNBV_EEFF_TOTALES1
def subir_oracle_tot1(conexion, cursor, df_tot1_ordenado):
    tab_ora = sTv.var_Ora_TAB1   # type: ignore
    if len(df_tot1_ordenado) > 0:
        print(f"\nUPDATE ORACLE {tab_ora}: se van a subir {len(df_tot1_ordenado)} registros\n")
        print(df_tot1_ordenado)
        df_tot1_ordenado['FEnvio'] = pd.to_datetime(df_tot1_ordenado['FEnvio'], errors='coerce')

    else:
        print(f"No hay datos para subir a la tabla oracle:  {tab_ora}")                           

# Update Oracle: CNBV_EEFF_TOTALES2
def subir_oracle_tot2(conexion, cursor, df_tot2_ordenado):
    tab_ora = sTv.var_Ora_TAB2   # type: ignore
    if len(df_tot2_ordenado) > 0:
        print(f"\nUPDATE ORACLE {tab_ora}: se van a subir {len(df_tot2_ordenado)} registros\n")    
        print(df_tot2_ordenado)
        df_tot2_ordenado['FEnvio'] = pd.to_datetime(df_tot2_ordenado['FEnvio'], errors='coerce')

    else:
        print(f"No hay datos para subir a la tabla oracle:  {tab_ora}")                           


# ----------------------------------------------------------------------------------------
#                             INICIO DE PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso7(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE):

    print(f"Variables: {var_NombreSalida}_Final.xlsx - {var_EJERCICIO} - {var_TRIMESTRE}")

    # Valida que siga conectado a oracle
    conexion = None
    cursor   = None

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

        if (conexion != None) or (cursor != None):
            
            borrar_resgistros(conexion, cursor, f"{var_EJERCICIO} - {var_TRIMESTRE}", sTv.var_Ora_TAB1)  # type: ignore

            subir_oracle_curl(conexion, cursor, df_curl_ordenado)
            subir_oracle_tot1(conexion, cursor, df_tot1_ordenado)
            subir_oracle_tot2(conexion, cursor, df_tot2_ordenado)

        # Cierro de conexiones Oracle y libero memoria
        Oracle_Cerrar_Conexion(conexion, cursor)
    else:

        print(f"\n ¡ No existe el file: {ruta_excel} !")
        print(f" ¡ No podemos subir datos a Oracle de los Estados Financieros !")

    
    
