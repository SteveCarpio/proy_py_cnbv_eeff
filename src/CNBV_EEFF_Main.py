# ----------------------------------------------------------------------------------------
#                        WebScraping CNBV EEFF (Estados Financieros)
#
# Programa que extraerá información contable de los estados financieros la Web de CNBV 
# Autor: SteveCarpio
# Versión: V3 2025
# ----------------------------------------------------------------------------------------

from   cfg.CNBV_librerias_v2 import *
from   cnbv.CNBV_paso0_v2 import sTv_paso0
from   cnbv.CNBV_paso1_v3 import sTv_paso1
from   cnbv.CNBV_paso2_v3 import sTv_paso2
from   cnbv.CNBV_paso3_v2 import sTv_paso3
from   cnbv.CNBV_paso4_v2 import sTv_paso4
from   cnbv.CNBV_paso5_v2 import sTv_paso5

os.system('cls')
print(f"WebScraping: CNBV v3.0 \n")

# Indique el tipo de descarga: Ej. 1 (Trimestral) , 2 (Mensual), 3 (Anual)
var_opcion = input(f" ¡Indique el Tipo de Descarga! 1 (Trimestral), 2 (Mensual), 3 (Anual) : ")
match var_opcion:
    case "1" | "2" | "3":
        var_TIPODESCARGA = int(var_opcion)
    case _:
        print(f"    ¡Atención! Valor erróneo ({var_opcion}) probar con 1, 2, 3")
        sys.exit()

# Indique el trimestre (solo para var_TIPODESCARGA=1): Ej. 1, 2, 3, 4, 4D
var_TRIMESTRE = input(f" ¡Indique el Periodo Trimestral Anual! (1, 2, 3, 4, 4D)               : ")
var_trime_tmp = ["1","2","3","4","4D"]
if str(var_TRIMESTRE) not in str(var_trime_tmp):
    print(f"    ¡Atención! Valor erróneo ({var_TRIMESTRE}) probar con (1, 2, 3, 4, 4D)")
    sys.exit()

# Indique el ejercicio: Ej. 2022, 2023, 2024
var_opcion = input(f" ¡Indique el Año de Ejercicio!                                        : ")
if var_opcion.isdigit():
    var_EJERCICIO = int(var_opcion)
    if var_EJERCICIO < 1990 or var_EJERCICIO > 2030:
        print("    ¡Atención! Año fuera del rango")
        sys.exit()
else:
    print(f"    ¡Atención! Valor erróneo ({var_opcion}) probar con (1990 > ... < 2030)")
    sys.exit()

# Tipo de Fichero a descargar (1 - excel ,2 pdf , 3 ......)
var_opcion = input(f" ¡Indique el Tipo Fichero para Descargar!  1 (.xlsx), 2 (.pdf)        : ")
match var_opcion:
    case "1" | "2":
        var_TIPOFILE = int(var_opcion)
        if var_TIPOFILE < 1 or var_TIPOFILE > 2:
            print("    ¡Atención! Valor fuera del rango (1 , 2)")
            sys.exit()
    case _:
        print(f"    ¡Atención! Valor erróneo ({var_opcion}) probar con (1 , 2)")
        sys.exit()
# ----------------------------------------------------------------------------------------
#                                  PARÁMETROS DE APOYO
# ----------------------------------------------------------------------------------------
# Definir el tipo de fichero a exportar
if int(var_TIPOFILE) == 1:
    var_extencion=".xlsx"
elif int(var_TIPOFILE) == 2:
    var_extencion=".pdf"
else:
    var_extencion=".xxx"

# Crear variable de tipo de descarga
if var_TIPODESCARGA == 1:
    var_TipoDes="Trime"
elif var_TIPODESCARGA == 2:
    var_TipoDes="Mensu"
elif var_TIPODESCARGA == 3:
    var_TipoDes="Anual"

# Para evitar que entre el trimestre si es mensual o anual 
if var_TIPODESCARGA != 1:
    var_TRIMESTRE = ""



# -----
os.system('cls')
print(f'Parámetros seleccionados: \n')
print(f'   TIPO DE DESCARGA   : {var_TIPODESCARGA} - {var_TipoDes}')
print(f'   PERIODO TRIMESTRAL : {var_TRIMESTRE}')
print(f'   AÑO DE EJERCICIO   : {var_EJERCICIO}')
print(f'   TIPO DE FICHERO    : {var_TIPOFILE} - {var_extencion}')
continuar = "n"
continuar = input("\n      ¿Ejecutamos el proceso (s/n)?\n>>> ")

if continuar not in ("s","S"): 
    print(" --- Exit del programa. --- ")
    sys.exit()
    


# Nombres de Salida
var_NombreSalida= f'CNBV_EEFF_{var_TipoDes}_{var_TRIMESTRE}_{var_EJERCICIO}_{var_TIPOFILE}'


# ----------------------------------------------------------------------------------------
#                                  EJECUCION PASOS
# ----------------------------------------------------------------------------------------
var_tit0 = f'CREAR Y LIMPIAR LOS REPOSITORIOS'
var_tit1 = f'NAVEGAR POR LA WEB CNBV Y DESCARGAR LOS CÓDIGOS "HTML"'
var_tit2 = f'CREAR INFORME "DATOS" CON LA LINEA "CURL"'
var_tit3 = f'DESCARGA FICHEROS "...{var_extencion}" A PARTIR DEL EXCEL "DATOS"'
var_tit4 = f'CREAR INFORME "TOTALES" A PARTIR DE LOS EXCEL DESCARGADOS'
var_tit5 = f'CREAR INFORME "FINAL" A PARTIR DE LOS EXCEL "DATOS" y "TOTALES"'
var_tit9 = f'EJECUTAR TODOS LOS PASOS'
var_tmp0 = " "
var_tmp1 = " "
var_tmp2 = " "
var_tmp3 = " "
var_tmp4 = " "
var_tmp5 = " "
var_tmp9 = " "

while True:
    os.system('cls')
    print(f'Ingresa el paso a Ejecutar: [ CNBV_EEFF_{var_TipoDes}_{var_TRIMESTRE}_{var_EJERCICIO}_{var_TIPOFILE}_......xlsx ] \n')
    print(f'{var_tmp0}   0 = {var_tit0}')
    print(f'{var_tmp1}   1 = {var_tit1}')
    print(f'{var_tmp2}   2 = {var_tit2}')
    print(f'{var_tmp3}   3 = {var_tit3}')
    print(f'{var_tmp4}   4 = {var_tit4}')
    print(f'{var_tmp5}   5 = {var_tit5}')
    print(f'{var_tmp9}   9 = {var_tit9}') 
    print(f'\n                      ¡ Para SALIR escriba otro valor !')
    var_PASO = input("\n>>> ")

    match var_PASO:
        case "0":
            # Ejecución del paso 0
            print(f' \n--------------------------------- [ {var_tit0} ]\n ')
            sTv_paso0(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes)
            var_tmp0 = '*'

        case "1":
            # Ejecución del paso 1
            print(f' \n--------------------------------- [ {var_tit1} ]\n ')
            sTv_paso1(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA)
            var_tmp1 = '*'

        case "2":        
            # Ejecución del paso 2
            print(f' \n--------------------------------- [ {var_tit2} ]\n ')
            sTv_paso2(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes, var_TIPOFILE, var_extencion)
            var_tmp2 = '*'

        case "3":
            # Ejecución del paso 3 
            print(f' \n--------------------------------- [ {var_tit3} ]\n ')
            sTv_paso3(var_NombreSalida)
            var_tmp3 = '*'

        case "4":
            # Ejecución del paso 4 
            print(f' \n--------------------------------- [ {var_tit4} ]\n ')
            sTv_paso4(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
            var_tmp4 = '*'
            
        case "5":
            # Ejecución del paso 5 
            print(f' \n--------------------------------- [ {var_tit5} ]\n ')
            sTv_paso5(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
            var_tmp5 = '*'

        case "9":
            print(f' \n--------------------------------- [ {var_tit0} ]\n ')
            sTv_paso0(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes)
            print(f' \n--------------------------------- [ {var_tit1} ]\n ')
            sTv_paso1(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA)
            print(f' \n--------------------------------- [ {var_tit2} ]\n ')
            sTv_paso2(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes, var_TIPOFILE, var_extencion)
            print(f' \n--------------------------------- [ {var_tit3}]\n ')
            sTv_paso3(var_NombreSalida)
            print(f' \n--------------------------------- [ {var_tit4} ]\n ')
            sTv_paso4(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
            print(f' \n--------------------------------- [ {var_tit5} ]\n ')
            sTv_paso5(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
            var_tmp9 = '*'

        case _:
            print(f"    ¡Atención! Valor erróneo ({var_PASO}) probar con (0, 1, 2, 3, 4, 5, 9)")
    
    continuar = input("\n\n¿Quiere continuar con otro paso o salimos del programa?:  S/N >>> ").strip()
    if continuar.upper() != "S":
        break

print("\n------------- [ FIN ] ------------- ")


        
