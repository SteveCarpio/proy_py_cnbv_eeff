# ----------------------------------------------------------------------------------------
#  PASO3: DESCARGA FICHEROS VIA CMD CURL
#  Autor: SteveCarpio-2024
# ----------------------------------------------------------------------------------------

import cfg.CNBV_variables as sTv
from   cfg.CNBV_librerias import *

# ----------------------------------------------------------------------------------------
#                                  FUNCIONES
# ----------------------------------------------------------------------------------------
def descargo_ficheros_curl(v_curl):
    proceso = subprocess.run(v_curl, shell=True, capture_output=True, text=True)
    salida_curl = proceso.stdout
    salida_erro = proceso.stderr
    codigo_retorno = proceso.returncode
    return salida_curl, salida_erro, codigo_retorno

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso3(var_NombreSalida, var_Entorno):

    try:
        if not os.path.exists(f'{sTv.var_RutaInforme}{var_NombreSalida}_Datos.xlsx'):
            raise FileNotFoundError(Fore.RED + f"¡Archivo no encontrado! {f'{sTv.var_RutaInforme}{var_NombreSalida}_Datos.xlsx'}\n")

        # Leo el excel con la lista de todos los curl a descargar
        df1 = pd.read_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_Datos.xlsx')
        df1 = df1.rename(columns={'clavepizarra': 'CLAVEPIZARRA'})   #  para poder hacer el inner join


        # Leo el excel con la lista filtrada y me quedo solo con el campo "ClavePizarra" de los "Activo" sea igual a "S"
        df2 = pd.read_excel(f'{sTv.var_RutaConfig}CNBV_EEFF_Claves_Pizarra.xlsx')
        columna_iden = df2[df2['ACTIVO'] == 'S'][['CLAVEPIZARRA']]       # -- stv debe ser por ClavePizarra..

        ### PASO 1 - # Filtramos la tabla DATOS con solo las ClavesPizarra a tratar
        df3 = df1.merge(columna_iden, on='CLAVEPIZARRA', how='inner')    # stv debe ser por ClavePizarra

        ### PASO 2 - # Comprobamos si hay nuevas Claves Pizarra
        idens_df2 = df2['CLAVEPIZARRA'].unique()          # .unique() evita duplicados, no es estrictamente necesario
        df4 = df1[~df1['CLAVEPIZARRA'].isin(idens_df2)]   # Filtrar df1: quedarnos con las filas cuyo Iden NO está en idens_df2      
        df4 = df4[['CLAVEPIZARRA']] # nos queda solo con esos campos
        df4 = df4.reset_index(drop=True)
        df4.index = pd.RangeIndex(start=1, stop=len(df4) + 1, step=1)
        
        # Validación si existe o no Nuevas ClavesPizarra
        if (len(df4) > 0):
            print(f"\n---- ({len(df4)}) CLAVES PIZARRA: Nuevas ---- [ATENCION]")
            df4['ACTIVO'] = 'VALIDAR'   # creo nuevo campo
            print(df4.to_string())
            print(f"\n Existen {len(df4)} nuevas claves pizarra por validar")
            # Concatenamos ambos (el orden de las filas no importa en este momento)
            #df_ClavePizarra_Validar = pd.concat([df2, df4], ignore_index=True)       #  creamos el excel solo con las claves nuevas
            # Ordenamos por ClavePizarra
            #df_ClavePizarra_Validar = df_ClavePizarra_Validar.sort_values('CLAVEPIZARRA').reset_index(drop=True)  # ya no haría falta este paso
            df_ClavePizarra_Validar  = df4.sort_values('CLAVEPIZARRA').reset_index(drop=True)
            # Reemplaza el excel de "CNBV_EEFF_Claves_Pizarra_Validar" con los nuevas ClavesPizarra a validar
            df_ClavePizarra_Validar.to_excel(f'{sTv.var_RutaConfig}CNBV_EEFF_Claves_Pizarra_Validar.xlsx', index=False)

        # Con los DATOS filtrados
        numRegDf = len(df3)
        print(f"\n---- ({numRegDf}) CLAVES PIZARRA: Detectadas ---- [OK]")
        print(" ")

        if numRegDf == 0:
            print(Fore.RED + f"Algo paso con el fichero ({sTv.var_RutaInforme}{var_NombreSalida}_Datos.xlsx) no debe tener registros.\n")
            sys.exit(0)

        print(f"Se van a descargar: {numRegDf} ficheros.")

        # Recorro el DataFrame y invoco la descarga por CMD
        var_sumaerrores=0
        for i, row in df3.iterrows():   # for i, (_, row) in enumerate(df3.iterrows()):
            # En modo DEV descargamos solo N files excel, en PRO se hará una descarga completa.
            if var_Entorno == "DEV":
                if i < 4:   # Solo descargará esos N FILES      # type: ignore   
                    var_result, var_error, var_codigo = descargo_ficheros_curl(row['CURL'])
                    print(Fore.YELLOW + f"\n--- Descargando ({i+1}/{numRegDf}): {row['FileXbrl']} ---") # type: ignore
                    print(f"{var_result}\n{var_error}")
                    if var_codigo != 0:
                        var_sumaerrores = var_sumaerrores + 1
            else:
                var_result, var_error, var_codigo = descargo_ficheros_curl(row['CURL'])
                print(Fore.YELLOW + f"\n--- Descargando ({i+1}/{numRegDf}): {row['FileXbrl']} ---")  # type: ignore
                print(f"{var_result}\n{var_error}")
                if var_codigo != 0:
                    var_sumaerrores = var_sumaerrores + 1

        if var_sumaerrores != 0:
            print(Fore.RED + "¡¡¡ ATENCIÓN !!!")
            print(Fore.RED + f'  En el proceso de descarga han ocurrido ({var_sumaerrores} errores)')
            print(Fore.RED + f'  Revisar la LOG y comparar con el EXCEL {sTv.var_RutaInforme}{var_NombreSalida}.xlsx')
            print(Fore.RED + f'  Pruebe a descarga a mano los files que dan error con sentencia CURL del excel')
            print(Fore.RED + f'        más info:  {sTv.var_sTv1} - {sTv.var_sTv2}')

    except FileNotFoundError as e:
        print(e)
        sys.exit(0)


