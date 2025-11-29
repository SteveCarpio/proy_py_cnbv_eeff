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
def borrar_resgistros(conexion, cursor, tabla_ora, periodo):
    print(f"\nINICIO: DELETE ORACLE ({tabla_ora}): se validará si se borrán o no registros\n") 
    sql_contar = f"SELECT COUNT(*) FROM {tabla_ora} WHERE PERIODO = :v_PERIODO"
    cursor.execute(sql_contar, v_PERIODO=periodo)
    filas_a_eliminar, = cursor.fetchone()
    print(f"ORACE:({tabla_ora}) - PERIODO:({periodo}) - REGISTROS:({filas_a_eliminar})")
    if filas_a_eliminar > 0: 
        sql_delete = f"DELETE FROM {tabla_ora} WHERE PERIODO = :v_PERIODO"
        cursor.execute(sql_delete, v_PERIODO=periodo)
        conexion.commit()
        filas_eliminadas = cursor.rowcount
        print(f"AVISO: Existen:{filas_eliminadas} registros de este periodo, se lanzará el DELETE y luego el UPDATE")
    else:
        print(f"OK: NO existen registros se procede a hacer el UPDATE")
    print(f"\nFIN: DELETE ORACLE ({tabla_ora}): se valido si se borrán o no registros\n") 

# Update Oracle: CNBV_EEFF_FILECURL
def subir_oracle_curl(conexion, cursor, tabla_ora, df_curl_ordenado):

    if len(df_curl_ordenado) > 0:
        print(f"\nINICIO: UPDATE ORACLE ({tabla_ora}): se van a subir ({len(df_curl_ordenado)}) registros\n")      
        df_curl_ordenado['FEnvio'] = pd.to_datetime(df_curl_ordenado['FEnvio'], errors='coerce')
        
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
            if pd.isna(v_Iden): v_Iden = None

            try:
                # Ejecutar INSERT con binds nombrados (oracledb)
                sql = f"""
                INSERT INTO {tabla_ora}               
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

                print(Fore.CYAN + f"Registro {index + 1} insertado en el servidor PYTHON ORACLE ({tabla_ora}:{v_Periodo})")  
                print(Fore.WHITE + f"  {v_Periodo} - {v_ClavePizarra} - {v_Iden} - {v_FEnvio} - {v_Taxonomia} - {v_FileXbrl}")
                print(Fore.WHITE + f"  {v_TipoFile} - {v_CURL}\n")
                 
            except Exception as e:
                # Puedes afinar el manejo según el código de error (duplicado, constraint, etc.)
                print(Fore.RED + f"******* Registro {index + 1} ERROR: no insertado en el servidor PYTHON ORACLE: {e} ********") 
                print(Fore.WHITE + f"  {v_Periodo} - {v_ClavePizarra} - {v_Iden} - {v_FEnvio} - {v_Taxonomia} - {v_FileXbrl}")
                print(Fore.WHITE + f"  {v_TipoFile} - {v_CURL}\n")

        print(f"FIN: UPDATE ORACLE ({tabla_ora}): se han subido ({len(df_curl_ordenado)}) registros\n")

        # Oracle, Confirma los cambios
        conexion.commit() 
    else:
        print(f"No hay datos para subir a la tabla oracle:  {tabla_ora}")                       

# Update Oracle: CNBV_EEFF_TOTALES1
def subir_oracle_tot1(conexion, cursor, tabla_ora, df_tot1_ordenado):
    #tab_ora = sTv.var_Ora_TAB1   # type: ignore
  
    if len(df_tot1_ordenado) > 0:
        print(f"\nINICIO: UPDATE ORACLE ({tabla_ora}): se van a subir ({len(df_tot1_ordenado)}) registros\n")      
        
        # Recorro el DataFrame registro por registro
        for index, row in df_tot1_ordenado.iterrows():
            v_Periodo         = row['Periodo']
            v_Iden            = row['Iden']
            v_Hoja            = row['Hoja']
            v_ColumnaA        = row['ColumnaA']
            v_ColumnaB        = row['ColumnaB']
            v_ColumnaC        = row['ColumnaC']
            v_FileX           = row['File']

            # Normalizar NaN/NaT a None
            if pd.isna(v_ColumnaA): v_ColumnaA = None
            if pd.isna(v_ColumnaB): v_ColumnaB = 0
            if pd.isna(v_ColumnaC): v_ColumnaC = 0

            try:
                # Ejecutar INSERT con binds nombrados (oracledb)
                sql = f"""
                INSERT INTO {tabla_ora}               
                    (Periodo, Iden, Hoja, ColumnaA, ColumnaB, ColumnaC, FileX)
                VALUES
                    (:Periodo, :Iden, :Hoja, :ColumnaA, :ColumnaB, :ColumnaC, :FileX)
                """  
                params = {
                    "Periodo":  v_Periodo, 
                    "Iden":     v_Iden, 
                    "Hoja":     v_Hoja, 
                    "ColumnaA": v_ColumnaA, 
                    "ColumnaB": v_ColumnaB, 
                    "ColumnaC": v_ColumnaC, 
                    "FileX":    v_FileX
                }
                cursor.execute(sql, params) 

                print(Fore.CYAN + f"Registro {index + 1} insertado en el servidor PYTHON ORACLE ({tabla_ora}:{v_Periodo})")  
                print(Fore.WHITE + f"  {v_Periodo} - {v_Iden} - {v_Hoja} - {v_ColumnaA} - {v_ColumnaB} - {v_ColumnaC} - {v_FileX}\n")
                
            except Exception as e:
                # Puedes afinar el manejo según el código de error (duplicado, constraint, etc.)
                print(Fore.RED + f"******* Registro {index + 1} ERROR: no insertado en el servidor PYTHON ORACLE: {e} ********") 
                print(Fore.WHITE + f"  {v_Periodo} - {v_Iden} - {v_Hoja} - {v_ColumnaA} - {v_ColumnaB} - {v_ColumnaC} - {v_FileX}\n")

        print(f"FIN: UPDATE ORACLE ({tabla_ora}): se han subido ({len(df_tot1_ordenado)}) registros\n") 

        # Oracle, Confirma los cambios
        conexion.commit() 
    else:
        print(f"No hay datos para subir a la tabla oracle:  {tabla_ora}")                           

# Update Oracle: CNBV_EEFF_TOTALES2
def subir_oracle_tot2(conexion, cursor, tabla_ora, df_tot2_ordenado):

    if len(df_tot2_ordenado) > 0:
        print(f"\nINICIO: UPDATE ORACLE ({tabla_ora}): se van a subir ({len(df_tot2_ordenado)}) registros\n")      
        df_tot2_ordenado['FEnvio'] = pd.to_datetime(df_tot2_ordenado['FEnvio'], errors='coerce')
        
        # Recorro el DataFrame registro por registro
        for index, row in df_tot2_ordenado.iterrows():
            v_Periodo               = row['Periodo']
            v_ClavePizarra          = row['ClavePizarra']
            v_Iden                  = row['Iden']
            v_FEnvio                = row['FEnvio']
            v_Taxonomia             = row['Taxonomia']
            v_TActivos              = row['TActivos']
            v_TActivosCirculantes   = row['TActivosCirculantes']
            v_TCapitalContable      = row['TCapitalContable']
            v_TPasivosCirculantes   = row['TPasivosCirculantes']
            v_TPasivos              = row['TPasivos']
            v_UtilPerdOperacion     = row['UtilPerdOperacion']
            v_UtilPerdNeta          = row['UtilPerdNeta']

            # Normalizar NaN/NaT a None or cero
            if pd.isna(v_Iden): v_Iden = None
            if pd.isna(v_TActivos): v_TActivos = 0
            if pd.isna(v_TActivosCirculantes): v_TActivosCirculantes = 0
            if pd.isna(v_TCapitalContable): v_TCapitalContable = 0
            if pd.isna(v_TPasivosCirculantes): v_TPasivosCirculantes = 0
            if pd.isna(v_TPasivos): v_TPasivos = 0
            if pd.isna(v_UtilPerdOperacion): v_UtilPerdOperacion = 0
            if pd.isna(v_UtilPerdNeta): v_UtilPerdNeta = 0

            try:
                # Ejecutar INSERT con binds nombrados (oracledb)
                sql = f"""
                INSERT INTO {tabla_ora}               
                    (Periodo, ClavePizarra, Iden, FEnvio, Taxonomia, TActivos, TActivosCirculantes, TCapitalContable, 
                    TPasivosCirculantes, TPasivos, UtilPerdOperacion, UtilPerdNeta)
                VALUES
                    (:Periodo, :ClavePizarra, :Iden, :FEnvio, :Taxonomia, :TActivos, :TActivosCirculantes, :TCapitalContable, 
                    :TPasivosCirculantes, :TPasivos, :UtilPerdOperacion, :UtilPerdNeta)
                """  
                params = {
                    "Periodo": v_Periodo,              # 1
                    "ClavePizarra": v_ClavePizarra, 
                    "Iden": v_Iden, 
                    "FEnvio": v_FEnvio, 
                    "Taxonomia": v_Taxonomia, 
                    "TActivos": v_TActivos, 
                    "TActivosCirculantes": v_TActivosCirculantes, 
                    "TCapitalContable": v_TCapitalContable,
                    "TPasivosCirculantes": v_TPasivosCirculantes,
                    "TPasivos": v_TPasivos,
                    "UtilPerdOperacion": v_UtilPerdOperacion,
                    "UtilPerdNeta": v_UtilPerdNeta
                }
                cursor.execute(sql, params) 

                print(Fore.CYAN + f"Registro {index + 1} insertado en el servidor PYTHON ORACLE ({tabla_ora}:{v_Periodo})")  
                print(Fore.WHITE + f"  {v_Periodo} - {v_ClavePizarra} - {v_Iden} - {v_FEnvio} - {v_Taxonomia} - {v_TActivos} - {v_TActivosCirculantes}")
                print(Fore.WHITE + f"  {v_TCapitalContable} - {v_TPasivosCirculantes} - {v_TPasivos} - {v_UtilPerdOperacion} - {v_UtilPerdNeta}\n")
                 
            except Exception as e:
                # Puedes afinar el manejo según el código de error (duplicado, constraint, etc.)
                print(Fore.RED + f"******* Registro {index + 1} ERROR: no insertado en el servidor PYTHON ORACLE: {e} ********") 
                print(Fore.WHITE + f"  {v_Periodo} - {v_ClavePizarra} - {v_Iden} - {v_FEnvio} - {v_Taxonomia} - {v_TActivos} - {v_TActivosCirculantes}")
                print(Fore.WHITE + f"  {v_TCapitalContable} - {v_TPasivosCirculantes} - {v_TPasivos} - {v_UtilPerdOperacion} - {v_UtilPerdNeta}\n")

        print(f"FIN: UPDATE ORACLE ({tabla_ora}): se han subido ({len(df_tot2_ordenado)}) registros\n")

        # Oracle, Confirma los cambios
        conexion.commit() 
    else:
        print(f"No hay datos para subir a la tabla oracle:  {tabla_ora}")   
                         


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
            tabla_curl = sTv.var_Ora_TAB3 # type: ignore
            tabla_tot1 = sTv.var_Ora_TAB1 # type: ignore
            tabla_tot2 = sTv.var_Ora_TAB2 # type: ignore
            periodo = f"{var_EJERCICIO} - {var_TRIMESTRE}"
            
            print(f"\n------------ PASO1: {tabla_curl} ------------\n")
            borrar_resgistros(conexion, cursor, tabla_curl, periodo)
            subir_oracle_curl(conexion, cursor, tabla_curl, df_curl_ordenado)

            print(f"\n------------ PASO2: {tabla_tot1} ------------\n")   
            borrar_resgistros(conexion, cursor, tabla_tot1, periodo) 
            subir_oracle_tot1(conexion, cursor, tabla_tot1, df_tot1_ordenado)

            print(f"\n------------ PASO3: {tabla_tot2} ------------\n")
            borrar_resgistros(conexion, cursor, tabla_tot2, periodo)
            subir_oracle_tot2(conexion, cursor, tabla_tot2, df_tot2_ordenado)

        # Cierro de conexiones Oracle y libero memoria
        Oracle_Cerrar_Conexion(conexion, cursor)
    else:

        print(f"\n ¡ No existe el file: {ruta_excel} !")
        print(f" ¡ No podemos subir datos a Oracle de los Estados Financieros !")

    
    
