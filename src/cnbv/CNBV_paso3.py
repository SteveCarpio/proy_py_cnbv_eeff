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
        df = pd.read_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_Datos.xlsx')
    except FileNotFoundError as e:
        print(e)
        sys.exit(0)

    numRegDf = len(df)
    if numRegDf == 0:
        print(Fore.RED + f"Algo paso con el fichero ({sTv.var_RutaInforme}{var_NombreSalida}_Datos.xlsx) no debe tener registros.\n")
        sys.exit(0)

    var_sumaerrores=0

    # Recorro el DataFrame y invoco la descarga por CMD
    for i, row in df.iterrows():

        # En modo DEV descargamos solo 10 excel, en PRO se hará una descarga completa.
        if var_Entorno == "DEV":
            if i < 10:
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
