# ----------------------------------------------------------------------------------------
#  PASO5: CREA INFORME FINAL A PARTIR DE LOS EXCEL CREADOS "DATOS" y "TOTALES"
# ----------------------------------------------------------------------------------------

import cfg.CNBV_Barrido_config as sTv
from   cfg.CNBV_Barrido_config import *

# ----------------------------------------------------------------------------------------
#                             PARAMETROS DE APOYO
# ----------------------------------------------------------------------------------------

# Ruta del archivo origen, destino y final
archivo_origen1 = f"{sTv.var_RutaInforme}{sTv.var_NombreSalida}_Datos.xlsx"
archivo_origen2 = f"{sTv.var_RutaInforme}{sTv.var_NombreSalida}_Totales.xlsx"
archivo_destino = f"{sTv.var_RutaInforme}{sTv.var_NombreSalida}_Final.xlsx"

# ----------------------------------------------------------------------------------------
#                              FUNCIONES
# ----------------------------------------------------------------------------------------
# Funcion: funcion_crea_excelSalida
def funcion_crea_excelSalida():
    print(f'Creado el excel vacio: {archivo_destino}')

    # Crear un nuevo archivo Excel para el resumen
    wb = Workbook()
    
    # Cambio el nombre de la hoja1 predeterminada a RESUMEN
    ws1 = wb.active
    ws1.title = "RESUMEN"

    # Agregar otras hojas 
    #ws2 = wb.create_sheet(title="DATAx")
    #ws3 = wb.create_sheet(title="TOTALESx")

    # Guardar el archivo Excel
    wb.save(archivo_destino)

# Funcion: funcion_copia_excelSalida
def funcion_copia_excelSalida(par_archivo_origen, par_nombre_hoja_origen, par_archivo_destino, par_nombre_hoja_destino ):
    print(f'Copiando la hoja {par_nombre_hoja_destino} al excel Final')

    # Leer el contenido de la hoja de origen
    df = pd.read_excel(par_archivo_origen, sheet_name=par_nombre_hoja_origen)

    # Escribir el contenido en la hoja de destino
    with pd.ExcelWriter(par_archivo_destino, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name=par_nombre_hoja_destino, index=False)

# Funcion: funcion_resumen_tipo1
def funcion_resumen_tipo1(par_archivo_destino):
    print(f'Creando resumen de parámetros ')
    # Leer DataFrame
    df = pd.read_excel(par_archivo_destino, sheet_name="DATA")
    var_regis = len(df)  # Número de registros de los fondos leídos
    var_fecha = dt.now()

    # Ruta del archivo de Excel
    archivo_destinox = par_archivo_destino

    # Cargar el libro existente
    libro = load_workbook(par_archivo_destino)
    hoja = libro['RESUMEN']

    # Escribir en el libro resumen1
    hoja['A1']  = "WEBSCARPING: CNBV_BARRIDO"
    hoja['B3']  = "RESUMEN"
    hoja['C5']  = "Fecha de Proceso:"
    hoja['D5']  = var_fecha
    hoja['C6']  = "URL monitorizada"
    hoja['D6']  = sTv.var_WEBSCRAPING
    hoja['C7']  = "Tipo de Descarga"
    hoja['D7']  = sTv.var_TipoDes
    hoja['C9']  = "Ejercicio"
    hoja['D9']  = sTv.var_EJERCICIO 
    hoja['C10']  = "Número de Trimestre"
    hoja['D10']  = sTv.var_TRIMESTRE
    hoja['C12'] = "Ruta Informes"
    hoja['D12'] = sTv.var_RutaInforme
    hoja['C13'] = "Ruta de Excel"
    hoja['D13'] = sTv.var_RutaXls
    hoja['C15'] = "Número de fondos"
    hoja['D15'] = var_regis
    #hoja['A15'] = "---"
   
    # Guardar los cambios en el archivo Excel
    libro.save(par_archivo_destino)

# Funcion: funcion_resumen_tipo2
def funcion_resumen_tipo2(par_archivo_destino):
    print(f'Creando resumen totales agrupados 1 ')

    # Leer DataFrame
    df_ori = pd.read_excel(par_archivo_destino, sheet_name="TOTALES")
    df = df_ori.head(7)
    df = df.reset_index(drop=True)
    df = df[['Hoja','ColumnaA','ColumnaB']]
  
    # Cargar el libro existente
    libro = load_workbook(par_archivo_destino)
    hoja = libro['RESUMEN']

    # Encontrar la última fila ocupada
    ultima_fila = hoja.max_row + 2

    # Escribir textos y cabecera
    hoja.cell(row=ultima_fila, column=2, value="RESULTADOS_1")
    hoja.cell(row=ultima_fila + 2, column=3, value="NOMBRE HOJA")
    hoja.cell(row=ultima_fila + 2, column=4, value="TOTALES")
    hoja.cell(row=ultima_fila + 2, column=5, value="SUMA")


    # Escribir el DataFrame en la hoja, comenzando en la última fila + 1
    for r_idx, row in df.iterrows():
        #print(f'r_idx:{r_idx} row:{row}')
        for c_idx, value in enumerate(row):
            #print(f'c_idx:{c_idx} value:{value}')
            hoja.cell(row=ultima_fila + r_idx + 3, column=c_idx + 3, value=value)

    # Guardar los cambios en el archivo Excel
    libro.save(par_archivo_destino)

# ----------------------------------------------------------------------------------------
#                             INICIO DE PROGRAMA
# ----------------------------------------------------------------------------------------

# Solo vale si TRIMESTRAL = 1, no vale para MENSUAL ni ANUAL
if sTv.var_TIPODESCARGA != 1:
    print(" --- Fin del proceso --- ")
    sys.exit()
# ------

funcion_crea_excelSalida()
funcion_copia_excelSalida(archivo_origen1, "DATA",    archivo_destino, "DATA")
funcion_copia_excelSalida(archivo_origen2, "TOTALES", archivo_destino, "TOTALES")
funcion_resumen_tipo1(archivo_destino)
funcion_resumen_tipo2(archivo_destino)
#  añadir más cuadros de resumen
