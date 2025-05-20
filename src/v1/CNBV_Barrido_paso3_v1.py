# ----------------------------------------------------------------------------------------
#  PASO3: DESCARGA FICHEROS VIA CMD CURL
# ----------------------------------------------------------------------------------------

import cfg.CNBV_Barrido_config as sTv
from   cfg.CNBV_Barrido_config import *

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

var_sumaerrores=0

# Leo el excel con la lista de todos los curl a descargar
df = pd.read_excel(f'{sTv.var_RutaInforme}{sTv.var_NombreSalida}_Datos.xlsx')
numRegDf = len(df)

# Recorro el DataFrame y invoco la descarga por CMD
for i, row in df.iterrows():
    var_result, var_error, var_codigo = descargo_ficheros_curl(row['CURL'])
    print(f"--------------------- Descargando ({i+1}/{numRegDf}): {row['FileXbrl']} ---------------------")
    print(f"Resultado de curl:{var_result}")
    print(f"Resultado de warn\n{var_error}")
    print(f"Código de retorno: {var_codigo}")
    if var_codigo != 0:
        var_sumaerrores = var_sumaerrores + 1

if var_sumaerrores != 0:
    print("¡¡¡ ATENCION !!!")
    print(f'  En el proceso de descarga han ocurrido ({var_sumaerrores} errores)')
    print(f'  Revisar la LOG y comparar con el EXCEL {sTv.var_RutaInforme}{sTv.var_NombreSalida}.xlsx')
    print(f'  Pruebe a descarga a mano los files que dan error con sentencia CURL del excel')
    print(f'        más info:  {sTv.var_sTv1} - {sTv.var_sTv2}')
