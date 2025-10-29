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

        # Leo el excel con la lista filtrada y me quedo solo con el campo "Iden" de los "Activo" sea igual a "S"
        df2 = pd.read_excel(f'{sTv.var_RutaConfig}CNBV_EEFF_Claves_Pizarra.xlsx')
        columna_iden = df2[df2['Activo'] == 'S'][['Iden']]

        ### PASO 1 - # Hacemos el merge (inner join) con df1
        df3 = df1.merge(columna_iden, on='Iden', how='inner')

        ### PASO 2 - # Comprobamos si hay nuevas Claves Pizarra
        idens_df2 = df2['Iden'].unique()          # .unique() evita duplicados, no es estrictamente necesario
        df4 = df1[~df1['Iden'].isin(idens_df2)]   # Filtrar df1: quedarnos con las filas cuyo Iden NO está en idens_df2      
        df4 = df4[['Iden', 'ClavePizarra']] # nos queda solo con esos campos
        if (len(df4) > 0):
            print("\n-------------------- [ ATENCION ] -------------------------")
            print(" Existen nuevas Claves-Pizarra, agregar los datos y volver a ejecutar el proceso.")
            print(" - Añadir el nuevo registro en el file: /srv/apps/MisCompilados/PROY_CNBV_EEFF/CONFIG/CNBV_EEFF_Claves_Pizarra.xlsx")
            print(" - Agregar los valores de 'Iden, ClavePizarra' --> y en la columna ACTIVO = S/N según lo indiquen ")
            print(" ")
            print(df4)
            print(" ")
            sys.exit(0)
            print("------------------------------------------------------------")

        numRegDf = len(df3)
        print(f"Se van a descargar: {numRegDf} ficheros.")
        if numRegDf == 0:
            print(Fore.RED + f"Algo paso con el fichero ({sTv.var_RutaInforme}{var_NombreSalida}_Datos.xlsx) no debe tener registros.\n")
            sys.exit(0)

        var_sumaerrores=0

        # Recorro el DataFrame y invoco la descarga por CMD
        for i, row in df3.iterrows():

            # En modo DEV descargamos solo 10 excel, en PRO se hará una descarga completa.
            if var_Entorno == "DEV":
                if i < 3:
                    var_result, var_error, var_codigo = descargo_ficheros_curl(row['CURL'])
                    print(Fore.YELLOW + f"\n--- Descargando ({i+1}/{numRegDf}): {row['FileXbrl']} ---")
                    print(f"{var_result}\n{var_error}")
                    if var_codigo != 0:
                        var_sumaerrores = var_sumaerrores + 1
            else:
                var_result, var_error, var_codigo = descargo_ficheros_curl(row['CURL'])
                print(Fore.YELLOW + f"\n--- Descargando ({i+1}/{numRegDf}): {row['FileXbrl']} ---")
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


