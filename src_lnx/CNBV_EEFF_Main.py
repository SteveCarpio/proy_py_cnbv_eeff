# ----------------------------------------------------------------------------------------
#                        WebScraping CNBV EEFF (Estados Financieros)
#
# Programa que extraerá información contable de los estados financieros la Web de CNBV 
# Autor: Steve Carpio
# Versión: V3 2025
# .\venv\Scripts\activate
# ----------------------------------------------------------------------------------------

from   cfg.CNBV_librerias import *
from   cfg.CNBV_ayuda  import sTv_ayuda
from   cnbv.CNBV_paso0 import sTv_paso0
from   cnbv.CNBV_paso1 import sTv_paso1
from   cnbv.CNBV_paso2 import sTv_paso2
from   cnbv.CNBV_paso3 import sTv_paso3
from   cnbv.CNBV_paso4 import sTv_paso4
from   cnbv.CNBV_paso5 import sTv_paso5
from   cnbv.CNBV_paso6 import sTv_paso6


# ==================================================================================================
# FUNCIONES APOYO
# ==================================================================================================
def op1_tipo_descarga(var_opcion):
    match var_opcion:
        case "1" | "2" | "3":
            var_TIPODESCARGA = int(var_opcion)

            # Crear variable de tipo de descarga
            if var_TIPODESCARGA == 1:
                var_TipoDes="Trime"
                var_TipoDes2="Trimestral"
            elif var_TIPODESCARGA == 2:
                var_TipoDes="Mensu"
                var_TipoDes2="Mensual"
            elif var_TIPODESCARGA == 3:
                var_TipoDes="Anual"
                var_TipoDes2=var_TipoDes

            return var_TIPODESCARGA, var_TipoDes, var_TipoDes2
        case _:
            print(Fore.RED + f"\n    ¡Atención! Valor erróneo ({var_opcion}) probar con 1, 2, 3\n")
            sys.exit()

def op2_trimestre_descarga(var_opcion):
    var_trime_tmp = ["1","2","3","4","4D"]
    if str(var_opcion) not in str(var_trime_tmp):
        print(Fore.RED + f"\n    ¡Atención! Valor erróneo ({var_opcion}) probar con (1, 2, 3, 4, 4D)\n")
        sys.exit()
    var_TRIMESTRE = str(var_opcion)
    return var_TRIMESTRE

def op3_ejercicio_descarga(var_opcion):
    if var_opcion.isdigit():
        var_EJERCICIO = int(var_opcion)
        if var_EJERCICIO < 2020 or var_EJERCICIO > 2030:
            print(Fore.RED + "\n    ¡Atención! Año fuera del rango (2020 a 2030)\n")
            sys.exit()
        return var_EJERCICIO
    else:
        print(Fore.RED + f"\n    ¡Atención! Valor erróneo ({var_opcion}) probar con (1990 > ... < 2030)\n")
        sys.exit()

def op4_tipo_fichero(var_opcion):
    match var_opcion:
        case "1" | "2":
            var_TIPOFILE = int(var_opcion)
            if var_TIPOFILE < 1 or var_TIPOFILE > 2:
                print(Fore.RED + "\n    ¡Atención! Valor fuera del rango (1 , 2)\n")
                sys.exit()

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

            return var_TIPOFILE, var_extencion, var_extencion2 
        case _:
            print(Fore.RED + f"\n    ¡Atención! Valor erróneo ({var_opcion}) probar con (1 , 2)\n")
            sys.exit()

# ==================================================================================================
# FUNCION: LANZADOR CON MENÚ
# ==================================================================================================
def lanzador_con_menu():
    print("Inicio: Lanzador con Menú")
    var_Parametro = ""

    if len(sys.argv) > 1:
        var_Parametro = str(sys.argv[1])

    if var_Parametro == "?":
        sTv_ayuda()
        sys.exit(0)

    var_Entorno="DEV"
    if var_Parametro == "PRO":
        var_Entorno = "PRO"

    # Inicializar colorama
    init(autoreset=True)
    
    print(f"Se ejecutará en modo: {var_Entorno} ")

    # -------------------------------
    #     PARÁMETROS DE ENTRADA
    # -------------------------------
    #os.system('clear')
    print(" ")
    print(Fore.MAGENTA + "=" * 94)
    print(Fore.MAGENTA + f"  Proceso WebScraping CNBV EEFF                             |  Modo              : {var_Entorno}")
    print(Fore.MAGENTA + "                                                            |  Tipo de Descarga  : ? ")
    print(Fore.MAGENTA + "    Ingrese los parámetros de entrada                       |  Periodo Trim Anual: ? ")
    print(Fore.MAGENTA + "    Escriba otro valor para salir del programa              |  Año de Ejercicio  : ? ")
    print(Fore.MAGENTA + "                                                            |  Tipo de Fichero   : ? ")
    print(Fore.MAGENTA + "=" * 94 + "\n")

    # Indique el tipo de descarga: Ej. 1 (Trimestral) , 2 (Mensual), 3 (Anual)
    var_opcion = input(Fore.GREEN + " ¡Indique el Tipo de Descarga! 1 (Trimestral), 2 (Mensual), 3 (Anual) : ")
    var_TIPODESCARGA, var_TipoDes, var_TipoDes2= op1_tipo_descarga(var_opcion)

    # Indique el trimestre (solo para var_TIPODESCARGA=1): Ej. 1, 2, 3, 4, 4D
    var_opcion = input(Fore.GREEN + f" ¡Indique el Periodo Trimestral Anual! (1, 2, 3, 4, 4D)               : ")
    var_TRIMESTRE = op2_trimestre_descarga(var_opcion)

    # Indique el ejercicio: Ej. 2022, 2023, 2024
    var_opcion = input(Fore.GREEN + f" ¡Indique el Año de Ejercicio!                                        : ")
    var_EJERCICIO = op3_ejercicio_descarga(var_opcion)

    # Tipo de Fichero a descargar (1 - excel ,2 pdf , 3 ......)
    var_opcion = input(Fore.GREEN + f" ¡Indique el Tipo Fichero para Descargar!  1 (.xlsx), 2 (.pdf)        : ")
    var_TIPOFILE, var_extencion, var_extencion2 = op4_tipo_fichero(var_opcion)

    # -----------------------------------
    #     DEFINIR PARÁMETROS DE APOYO
    # -----------------------------------

    # Para evitar que entre el trimestre si es mensual o anual 
    if var_TIPODESCARGA != 1:
        var_TRIMESTRE = ""
    # Nombres de Salida y fechas
    var_NombreSalida= f'CNBV_EEFF_{var_TipoDes}_{var_TRIMESTRE}_{var_EJERCICIO}_{var_TIPOFILE}'
    var_Fecha = dt.now()
    var_Fechas1 = var_Fecha.strftime('%Y-%m-%d')  # Formato "2025-03-04"

    # -------------------------
    #      EJECUCIÓN PASOS
    # -------------------------
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
        os.system('clear')
        
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
                    print(Fore.LIGHTWHITE_EX + f' \n--------------------------------- [ {var_tit0} ] Paso-0 \n ')
                    sTv_paso0(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes)
                    var_tmp0 = '*'

                print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit1} ] Paso-1 \n ')
                sTv_paso1(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA)
                var_tmp1 = '*'

            case "2":        
                # Ejecución del paso 2
                print(Fore.GREEN + f' \n--------------------------------- [ {var_tit2} ] Paso-2 \n ')
                sTv_paso2(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes, var_TIPOFILE, var_extencion)
                var_tmp2 = '*'

            case "3":
                # Ejecución del paso 3 
                print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit3} ] Paso-3 \n ')
                sTv_paso3(var_NombreSalida, var_Entorno)
                var_tmp3 = '*'

            case "4":
                # Ejecución del paso 4 
                print(Fore.BLUE + f' \n--------------------------------- [ {var_tit4} ] Paso-4 \n ')
                sTv_paso4(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
                var_tmp4 = '*'
                
            case "5":
                # Ejecución del paso 5 
                print(Fore.BLUE + f' \n--------------------------------- [ {var_tit5} ] Paso-5 \n ')
                sTv_paso5(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
                var_tmp5 = '*'

            case "6":
                # Ejecución del paso 6 
                print(Fore.BLUE + f' \n--------------------------------- [ {var_tit6} ] Paso-6 \n ')
                sTv_paso6(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes2, var_Fechas1, var_Entorno)
                var_tmp6 = '*'

            case "9":
                print(Fore.LIGHTWHITE_EX + f' \n--------------------------------- [ {var_tit0} ] Paso-0 \n ')
                #sTv_paso0(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes)
                print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit1} ] Paso-1 \n ')
                #sTv_paso1(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA)
                print(Fore.GREEN + f' \n--------------------------------- [ {var_tit2} ] Paso-2 \n ')
                #sTv_paso2(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes, var_TIPOFILE, var_extencion)
                print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit3}] Paso-3 \n ')
                #sTv_paso3(var_NombreSalida, var_Entorno)
                print(Fore.BLUE + f' \n--------------------------------- [ {var_tit4} ] Paso-4 \n ')
                #sTv_paso4(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
                print(Fore.BLUE + f' \n--------------------------------- [ {var_tit5} ] Paso-5 \n ')
                #sTv_paso5(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes)
                print(Fore.BLUE + f' \n--------------------------------- [ {var_tit6} ] Paso-6 \n ')
                #sTv_paso6(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes2, var_Fechas1, var_Entorno)
                var_tmp9 = '*'

            case "?":
                sTv_ayuda()

            case _:
                print(Fore.RED + f"    ¡Saliendo del programa!\n")
                sys.exit(0)
        
        continuar = input(Fore.MAGENTA + "\n\n¡Pulse una tecla para continuar! ").strip()
        #if continuar.upper() != "S":
        #    break

# ==================================================================================================
# FUNCION: LANZADOR SIN MENÚ
# ==================================================================================================
def lanzador_sin_menu():

    print("Inicio: Lanzador sin Menú")






# ==================================================================================================
# INICIO DEL PROGRAMA
# ==================================================================================================

var_NumParametros = len(sys.argv)
var_NumParametros = var_NumParametros - 1
print(f"Número de parámetros: {var_NumParametros}")

# Ejecución en MODO con MENÚ
if var_NumParametros == 0 or var_NumParametros == 1:
    print(f"Parámetro 0: {str(sys.argv[0])} ")
    if var_NumParametros == 1:
        print(f"Parámetro 1: {str(sys.argv[1])} ")
    lanzador_con_menu()

# Ejecución en MODO sin MENÚ
if var_NumParametros == 5:
    var_par1 = str(sys.argv[1])
    var_par2 = str(sys.argv[2])
    var_par3 = str(sys.argv[3])
    var_par4 = str(sys.argv[4])
    var_par5 = str(sys.argv[5])
    print(f"Parámetro 0: {str(sys.argv[0])} ")
    print(f"Parámetro 1: {var_par1} ")
    print(f"Parámetro 2: {var_par2} ")
    print(f"Parámetro 3: {var_par3} ")
    print(f"Parámetro 4: {var_par4} ")
    print(f"Parámetro 5: {var_par5} ")
    
    lanzador_sin_menu()

# Mensaje de ERROR de parametros
if var_NumParametros != 0 and var_NumParametros != 1 and var_NumParametros != 5:
    print("ERROR: Número de parámetros incorrecto")
    print("      - sin parámetros   = Ejecución en modo DEV     con Menú, ej: CNBV_EEFF_Main.py")
    print("      - con 1 parámetro  = Ejecución en modo DEV/PRO con Menú, ej: CNBV_EEFF_Main.py PRO")
    print("      - con 5 parámetros = Ejecución en modo DEV/PRO sin Menú, ej: CNBV_EEFF_Main.py DEV 1 1 2023 1")



        
