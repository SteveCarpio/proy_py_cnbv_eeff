# ----------------------------------------------------------------------------------------
#                                  WEB SCRAPING CNBV "BARRIDO"
#
# Programa que extraerá información contable de la Web de Cnbv de los fondos de Mexico
# Pependencias: Abajo listo las librerías necesarias para su ejecución
# Autor: SteveCarpio-2024
# ----------------------------------------------------------------------------------------

# Librerias invocadas en los PASOS del programa :      # LO P0 P1 P2 P3 P4 P5 #
import os                                              # lo p0 -- p2 -- p4 p5 #
import sys                                             # lo -- -- -- -- p4    #
import glob                                            # -- p0 -- p2 -- p4    #
import time                                            # -- -- p1             #
import pandas as pd                                    # -- -- -- p2 p3 p4 p5 #
import subprocess                                      # -- -- -- -- p3       #
from selenium import webdriver                         # -- -- p1             #
from selenium.webdriver.chrome.service import Service  # -- -- p1             #
from selenium.webdriver.common.by import By            # -- -- p1             #
from bs4 import BeautifulSoup                          # -- -- -- p2          #
from openpyxl import Workbook                          # -- -- -- -- -- -- p5 #
from openpyxl import load_workbook                     # -- -- -- -- -- -- p5 #
from datetime import datetime as dt                    # -- -- -- -- -- -- p5 #

# ----------------------------------------------------------------------------------------
#                                  API GOOGLE CHROME
# ----------------------------------------------------------------------------------------
var_CHROMEDRIVER="C:/MisCompilados/cfg/chromedriver-win32/chromedriver.exe"
var_WEBSCRAPING="https://xbrl.cnbv.gob.mx/visorXbrl.html#/enviosInformacionFinanciera"

# ----------------------------------------------------------------------------------------
#                          PARAMETROS DE ENTRADA POR TECLADO
# ----------------------------------------------------------------------------------------

os.system('cls')
print(f" WebScraping: CNBV Barrido\n -----------------------------\n")

# Indique el tipo de descarga: Ej. 1 (Trimestral) , 2 (Mensual), 3 (Anual)
var_TIPODESCARGA = int(input(f" ¡Indique el Tipo de Descarga! 1 (Tri), 2 (Men) o 3 (Anu): "))
if var_TIPODESCARGA < 1 or var_TIPODESCARGA > 3:
    print("    ¡Atención! Valor fuera del rango (1,2,3)")
    sys.exit()

# Indique el ejercicio: Ej. 2022, 2023, 2024
var_EJERCICIO = int(input(f" ¡Indique el año de Ejercicio! : "))
if var_EJERCICIO < 1990 or var_EJERCICIO > 2030:
    print("    ¡Atención! Año fuera del rango")
    sys.exit()

# Indique el trimestre (solo para var_TIPODESCARGA=1): Ej. 1, 2, 3, 4, 4D
var_TRIMESTRE = input(f" ¡Indique el Trimestre! 1, 2, 3, 4, 4D: ")
var_trime_tmp = ["1","2","3","4","4D"]

if str(var_TRIMESTRE) not in str(var_trime_tmp):
    print(f"    ¡Atención! Valor debe ser (1, 2, 3, 4, 4D) {var_TRIMESTRE}")
    sys.exit()

# Tipo de Fichero a descargar (1 - excel ,2 pdf , 3 ......)
var_TIPOFILE = int(input(f" ¡Indique el Tipo Fichero! 1 (xlsx), 2 (pdf): "))
if var_TIPOFILE < 1 or var_TIPOFILE > 2:
    print("    ¡Atención! Valor fuera del rango (1 , 2)")
    sys.exit()

# -----
os.system('cls')
print(f'Parámetros seleccionados: \n')
print(f' TIPO DE DESCARGA: {var_TIPODESCARGA}')
print(f' AÑO DE EJERCICIO: {var_EJERCICIO}')
print(f' TRIMESTRE ANUAL : {var_TRIMESTRE}')
print(f' TIPO DE FICHERO : {var_TIPOFILE}')
continuar = "n"
continuar = input("\n¿ EJECUTAMOS EL PROCESO (s/n) ?: \n")
if continuar == "s" or continuar == "S":

    # ----------------------------------------------------------------------------------------
    #                                  PARAMETROS DE APOYO
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

    # Rutas
    var_RutaRaiz='C:\\MisCompilados\\CNBV_Barrido\\' 
    var_RutaWebFiles=f'{var_RutaRaiz}WEBFILES\\'
    var_RutaInforme=f'{var_RutaRaiz}INFORMES\\'
    var_RutaXls=f'{var_RutaRaiz}XLS\\'

    # Nombres de Salida
    var_NombreSalida= f'CNBV_Barrido_{var_TipoDes}_{var_TRIMESTRE}_{var_EJERCICIO}'
    var_libro1="210000"
    var_libro2="310000"
    var_sTv1="SteveCarpio-2024"
    var_sTv2="stv.madrid@gmail.com" 
else:
    print(" --- Exit del programa --- ")
    sys.exit()