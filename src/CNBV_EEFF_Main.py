# ----------------------------------------------------------------------------------------
#                        WebScraping CNBV EEFF (Estados Financieros)
#
# Programa que extraerá información contable de los estados financieros la Web de CNBV 
# Autor: Steve Carpio
# Versión: V3 2025
# ----------------------------------------------------------------------------------------

from   cfg.CNBV_librerias import *
from   cfg.CNBV_ayuda     import sTv_ayuda
from   cnbv.CNBV_paso0 import sTv_paso0
from   cnbv.CNBV_paso1 import sTv_paso1
from   cnbv.CNBV_paso2 import sTv_paso2
from   cnbv.CNBV_paso3 import sTv_paso3
from   cnbv.CNBV_paso4 import sTv_paso4
from   cnbv.CNBV_paso5 import sTv_paso5
from   cnbv.CNBV_paso6 import sTv_paso6

var_Parametro = ""
if len(sys.argv) > 1:
    var_Parametro = str(sys.argv[1])

if var_Parametro == "?":
    sTv_ayuda()
    sys.exit(0)

var_Entorno="PRO"
if var_Parametro == "DEV":
    var_Entorno = "DEV"

# Inicializar colorama
init(autoreset=True)

# ----------------------------------------------------------------------------------------
#                                  PARÁMETROS DE ENTRADA
# ----------------------------------------------------------------------------------------
os.system('cls')
print(Fore.MAGENTA + "=" * 94)
print(Fore.MAGENTA + f"  Proceso WebScraping CNBV EEFF                             |  Modo              : {var_Entorno}")
print(Fore.MAGENTA + "                                                            |  Tipo de Descarga  : ? ")
print(Fore.MAGENTA + "    Ingrese los parámetros de entrada                       |  Periodo Trim Anual: ? ")
print(Fore.MAGENTA + "    Escriba otro valor para salir del programa              |  Año de Ejercicio  : ? ")
print(Fore.MAGENTA + "                                                            |  Tipo de Fichero   : ? ")
print(Fore.MAGENTA + "=" * 94 + "\n")

# Indique el tipo de descarga: Ej. 1 (Trimestral) , 2 (Mensual), 3 (Anual)
var_opcion = input(Fore.GREEN + " ¡Indique el Tipo de Descarga! 1 (Trimestral), 2 (Mensual), 3 (Anual) : ")
match var_opcion:
    case "1" | "2" | "3":
        var_TIPODESCARGA = int(var_opcion)
    case _:
        print(Fore.RED + f"\n    ¡Atención! Valor erróneo ({var_opcion}) probar con 1, 2, 3\n")
        sys.exit()

# Indique el trimestre (solo para var_TIPODESCARGA=1): Ej. 1, 2, 3, 4, 4D
var_TRIMESTRE = input(Fore.GREEN + f" ¡Indique el Periodo Trimestral Anual! (1, 2, 3, 4, 4D)               : ")
var_trime_tmp = ["1","2","3","4","4D"]
if str(var_TRIMESTRE) not in str(var_trime_tmp):
    print(Fore.RED + f"\n    ¡Atención! Valor erróneo ({var_TRIMESTRE}) probar con (1, 2, 3, 4, 4D)\n")
    sys.exit()

# Indique el ejercicio: Ej. 2022, 2023, 2024
var_opcion = input(Fore.GREEN + f" ¡Indique el Año de Ejercicio!                                        : ")
if var_opcion.isdigit():
    var_EJERCICIO = int(var_opcion)
    if var_EJERCICIO < 2020 or var_EJERCICIO > 2030:
        print(Fore.RED + "\n    ¡Atención! Año fuera del rango (2020 a 2030)\n")
        sys.exit()
else:
    print(Fore.RED + f"\n    ¡Atención! Valor erróneo ({var_opcion}) probar con (1990 > ... < 2030)\n")
    sys.exit()

# Tipo de Fichero a descargar (1 - excel ,2 pdf , 3 ......)
var_opcion = input(Fore.GREEN + f" ¡Indique el Tipo Fichero para Descargar!  1 (.xlsx), 2 (.pdf)        : ")
match var_opcion:
    case "1" | "2":
        var_TIPOFILE = int(var_opcion)
        if var_TIPOFILE < 1 or var_TIPOFILE > 2:
            print(Fore.RED + "\n    ¡Atención! Valor fuera del rango (1 , 2)\n")
            sys.exit()
    case _:
        print(Fore.RED + f"\n    ¡Atención! Valor erróneo ({var_opcion}) probar con (1 , 2)\n")
        sys.exit()

# ----------------------------------------------------------------------------------------
#                            DEFINIR PARÁMETROS DE APOYO
# ----------------------------------------------------------------------------------------
# Definir el tipo de fichero a exportar
if int(var_TIPOFILE) == 1:
    var_extencion=".xlsx"
    var_extencion2="Excel"
elif int(var_TIPOFILE) == 2:
    var_extencion=".pdf"
    var_extencion2="Pdf"
else:
    var_extencion=".xxx"
    var_extencion2="Desconocido"

# Crear variable de tipo de descarga
if var_TIPODESCARGA == 1:
    var_TipoDes="Trime"
    var_TipoDes2="Trimestral"
elif var_TIPODESCARGA == 2:
    var_TipoDes="Mensu"
    var_TipoDes2="Mensual"
elif var_TIPODESCARGA == 3:
    var_TipoDes="Anual"
    var_TipoDe2=var_TipoDes

# Para evitar que entre el trimestre si es mensual o anual 
if var_TIPODESCARGA != 1:
    var_TRIMESTRE = ""

# Nombres de Salida
var_NombreSalida= f'CNBV_EEFF_{var_TipoDes}_{var_TRIMESTRE}_{var_EJERCICIO}_{var_TIPOFILE}'

var_Fecha = dt.now()
var_Fechas1 = var_Fecha.strftime('%Y-%m-%d')  # Formato "2025-03-04"

# ----------------------------------------------------------------------------------------
#                                  EJECUCIÓN PASOS
# ----------------------------------------------------------------------------------------
var_tit0 = f'CREAR Y LIMPIAR LOS REPOSITORIOS'
var_tit1 = f'NAVEGAR POR LA WEB CNBV Y DESCARGAR LOS CÓDIGOS "HTML"'
var_tit2 = f'CREAR INFORME "DATOS" CON LA LINEA "CURL"'
var_tit3 = f'DESCARGA FICHEROS "...{var_extencion}" A PARTIR DEL EXCEL "DATOS"'
var_tit4 = f'CREAR INFORME "TOTALES" A PARTIR DE LOS EXCEL DESCARGADOS'
var_tit5 = f'CREAR INFORME "FINAL" A PARTIR DE LOS EXCEL "DATOS" y "TOTALES"'
var_tit6 = f'MANDAR POR EMAIL EL INFORME "FINAL" '
var_tit9 = f'EJECUTAR TODOS LOS PASOS'
var_tmp0 = " "
var_tmp1 = " "
var_tmp2 = " "
var_tmp3 = " "
var_tmp4 = " "
var_tmp5 = " "
var_tmp6 = " "
var_tmp9 = " "

while True:
    os.system('cls')
    
    print(Fore.MAGENTA + "=" * 94)
    print(Fore.MAGENTA + "  Proceso WebScraping CNBV EEFF                             |  Modo              : " + var_Entorno)
    print(Fore.MAGENTA + "                                                            |  Tipo de Descarga  : " + var_TipoDes2)
    print(Fore.MAGENTA + "    Ejecutar los pasos del proyecto                         |  Periodo Trim Anual: " + var_TRIMESTRE)
    print(Fore.MAGENTA + "    Escriba otro valor para salir del programa              |  Año de Ejercicio  : " + str(var_EJERCICIO))
    print(Fore.MAGENTA + "                                                            |  Tipo de Fichero   : " + var_extencion2)
    print(Fore.MAGENTA + "=" * 94 + "\n")

    print(Fore.LIGHTWHITE_EX + f'{var_tmp0}   0 = {var_tit0}')
    print(Fore.YELLOW + f'{var_tmp1}   1 = {var_tit1}')
    print(Fore.GREEN + f'{var_tmp2}   2 = {var_tit2}')
    print(Fore.YELLOW + f'{var_tmp3}   3 = {var_tit3}')
    print(Fore.BLUE + f'{var_tmp4}   4 = {var_tit4}')
    print(Fore.BLUE + f'{var_tmp5}   5 = {var_tit5}')
    print(Fore.YELLOW + f'{var_tmp6}   6 = {var_tit6}')
    print(Fore.LIGHTWHITE_EX + f'{var_tmp9}   9 = {var_tit9}') 
    print(Fore.MAGENTA + f'    ? = AYUDA')
    print(Fore.MAGENTA + f'\n                      ¡ Para SALIR escriba otro valor !')
    var_PASO = input(Fore.MAGENTA + "\n>>> ")

    match var_PASO:
        case "0":
            # Ejecución del paso 0
            print(Fore.LIGHTWHITE_EX + f' \n--------------------------------- [ {var_tit0} ]\n ')
            sTv_paso0(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes)
            var_tmp0 = '*'

        case "1":
            # Ejecución del paso 1

            if var_tmp0 != '*':  # Si no ejecuto el paso 0 lo invoco
                # Ejecución del paso 0
                print(Fore.LIGHTWHITE_EX + f' \n--------------------------------- [ {var_tit0} ]\n ')
                sTv_paso0(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes)
                var_tmp0 = '*'

            print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit1} ]\n ')
            sTv_paso1(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA)
            var_tmp1 = '*'

        case "2":        
            # Ejecución del paso 2
            print(Fore.GREEN + f' \n--------------------------------- [ {var_tit2} ]\n ')
            sTv_paso2(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes, var_TIPOFILE, var_extencion)
            var_tmp2 = '*'

        case "3":
            # Ejecución del paso 3 
            print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit3} ]\n ')
            sTv_paso3(var_NombreSalida, var_Entorno)
            var_tmp3 = '*'

        case "4":
            # Ejecución del paso 4 
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit4} ]\n ')
            sTv_paso4(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
            var_tmp4 = '*'
            
        case "5":
            # Ejecución del paso 5 
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit5} ]\n ')
            sTv_paso5(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
            var_tmp5 = '*'

        case "6":
            # Ejecución del paso 6 
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit6} ]\n ')
            sTv_paso6(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes2, var_Fechas1, var_Entorno)
            var_tmp6 = '*'

        case "9":
            print(Fore.LIGHTWHITE_EX + f' \n--------------------------------- [ {var_tit0} ]\n ')
            sTv_paso0(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes)
            print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit1} ]\n ')
            sTv_paso1(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA)
            print(Fore.GREEN + f' \n--------------------------------- [ {var_tit2} ]\n ')
            sTv_paso2(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes, var_TIPOFILE, var_extencion)
            print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit3}]\n ')
            sTv_paso3(var_NombreSalida, var_Entorno)
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit4} ]\n ')
            sTv_paso4(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit5} ]\n ')
            sTv_paso5(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit6} ]\n ')
            sTv_paso6(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes2, var_Fechas1, var_Entorno)
            var_tmp9 = '*'

        case "?":
            sTv_ayuda()

        case _:
            print(Fore.RED + f"    ¡Saliendo del programa!\n")
            sys.exit(0)
    
    continuar = input(Fore.MAGENTA + "\n\n¡Pulse una tecla para continuar! ").strip()
    #if continuar.upper() != "S":
    #    break




        
