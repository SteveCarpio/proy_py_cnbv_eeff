# ----------------------------------------------------------------------------------------
#  PASO5: CREA INFORME FINAL A PARTIR DE LOS EXCEL CREADOS "DATOS" y "TOTALES"
#         Solo creará el informe para trimestrales, para el resto se saldrá del proceso
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.CNBV_variables as sTv
from   cfg.CNBV_librerias import *

# ----------------------------------------------------------------------------------------
#                              FUNCIONES
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Función: funcion_crea_excelSalida ------------------------------------------------------
# ----------------------------------------------------------------------------------------
def funcion_crea_excelSalida(archivo_destino):
    print(f'   Creado excel FINAL vació: {archivo_destino}')

    # Crear un nuevo archivo Excel para el resumen
    wb = Workbook()
    
    # Cambio el nombre de la hoja1 predeterminada a RESUMEN
    ws1 = wb.active
    ws1.title = "RESUMEN"

    # Agregar otras hojas 
    #ws2 = wb.create_sheet(title="TOTALES_2")

    # Guardar el archivo Excel
    wb.save(archivo_destino)

# ----------------------------------------------------------------------------------------
# Funcion: funcion_copia_excelSalida -----------------------------------------------------
# ----------------------------------------------------------------------------------------
def funcion_copia_excelSalida(par_archivo_origen, par_nombre_hoja_origen, par_archivo_destino, par_nombre_hoja_destino ):
    print(f'   Copiando hoja {par_nombre_hoja_destino} al excel FINAL')

    # Leer el contenido de la hoja de origen
    df = pd.read_excel(par_archivo_origen, sheet_name=par_nombre_hoja_origen)

    # Escribir el contenido en la hoja de destino
    with pd.ExcelWriter(par_archivo_destino, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name=par_nombre_hoja_destino, index=False)

# ----------------------------------------------------------------------------------------
# Funcion: funcion_resumen_tipo1 ---------------------------------------------------------
# ----------------------------------------------------------------------------------------
def funcion_resumen_tipo1(par_archivo_destino, var_EJERCICIO, var_TRIMESTRE, var_TipoDes):
    print(f'   Creando resumen TIPO1 ')

    # Leer DataFrame
    df = pd.read_excel(par_archivo_destino, sheet_name="DATA")
    var_regis = len(df)  # Número de registros de los fondos leídos
    var_fecha = dt.now()

    # Ruta del archivo de Excel
    archivo_destinox = par_archivo_destino

    # Cargar el libro existente
    libro = openpyxl.load_workbook(par_archivo_destino)
    hoja = libro['RESUMEN']
 
    # Escribir en el libro resumen1
    hoja['A1']  = "WEBSCARPING: CNBV_EEFF"
    hoja['B3']  = "RESUMEN"
    hoja['C5']  = "Fecha de Proceso:"
    hoja['D5']  = var_fecha
    hoja['C6']  = "URL monitorizada"
    hoja['D6']  = sTv.var_WEBSCRAPING
    hoja['C7']  = "Tipo de Descarga"
    hoja['D7']  = var_TipoDes
    hoja['C9']  = "Ejercicio"
    hoja['D9']  = var_EJERCICIO 
    hoja['C10']  = "Número de Trimestre"
    hoja['D10']  = int(var_TRIMESTRE)
    hoja['C12'] = "Ruta Informes"
    hoja['D12'] = sTv.var_RutaInforme
    hoja['C13'] = "Ruta de Excel"
    hoja['D13'] = sTv.var_RutaXls
    hoja['C15'] = "Número de fondos"
    hoja['D15'] = var_regis
    #hoja['A15'] = "---"
   
    # Guardar los cambios en el archivo Excel
    libro.save(par_archivo_destino)

# ----------------------------------------------------------------------------------------
# Funcion: funcion_resumen_tipo2 ---------------------------------------------------------
# ----------------------------------------------------------------------------------------
def funcion_resumen_tipo2(par_archivo_destino):
    print(f'   Creando resumen TIPO2 ')

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
# Funcion: funcion_crea_excelTotales2 ----------------------------------------------------
# ----------------------------------------------------------------------------------------
def funcion_crea_excelTotales2(par_archivo_origen1, par_archivo_origen2, par_archivo_destino,par_nombre_hoja_destino):
    print(f'   Creando hoja TOTALES2 en el excel FINAL ')

    # Leer los excel de entrada
    df_dat = pd.read_excel(par_archivo_origen1, sheet_name="DATA")
    df_tot = pd.read_excel(par_archivo_origen2, sheet_name="TOTALES")
    df_res = pd.merge(df_dat, df_tot, on='Iden')

    df_transposed = df_res.pivot(index=["Iden", "FEnvio", "ClavePizarra", "Periodo", "Taxonomia"], columns="ColumnaA", values="ColumnaB").reset_index()
    df_transposed.columns.name = None  # Elimina el nombre de las columnas

    # Escribir el contenido en la hoja de destino
    with pd.ExcelWriter(par_archivo_destino, engine='openpyxl', mode='a') as writer:
        df_transposed.to_excel(writer, sheet_name=par_nombre_hoja_destino, index=False)

# ----------------------------------------------------------------------------------------
# Funcion: funcion_formatea_excelFinal ----------------NO FUNCIONA------------------------
# ----------------------------------------------------------------------------------------
def funcion_formatea_excelFinal2(par_archivo_destino):
    print(f'   Formateando excel FINAL ')
    par_archivo_destino = 'C:\\MisCompilados\\PROY_CNBV_EEFF\\INFORMES\\CNBV_EEFF_Trime_3_2024_1_Final.xlsx'
    # Cargar el excel FINAL    
    wb = openpyxl.load_workbook(par_archivo_destino)
    ws = wb["TOTALES2"]  # Selecciona la hoja "TOTALES2"
    # 1. Colorear un rango de celdas
    fill_color = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Color amarillo
    for row in ws.iter_rows(min_row=1, max_row=1, min_col=1, max_col=12):
        for cell in row:
            cell.fill = fill_color
    # 2. Poner en negrita un rango de celdas (por ejemplo, la fila de encabezados)
    bold_font = Font(bold=True)
    for cell in ws[1]:
        cell.font = bold_font
    # 3. Inmovilizar la primera columna
    ws.freeze_panes = "A1"  # Inmoviliza la primera columna
    # 4. Ajustar el tamaño de las columnas en un rango
    for col in range(1, 13):  # Ajustar las columnas A a D
        col_letter = get_column_letter(col)
        ws.column_dimensions[col_letter].width = 15  # Ancho de 15
    # Guardar el archivo Excel
    wb.save(par_archivo_destino)

# ----------------------------------------------------------------------------------------
#                             INICIO DE PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso5(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes):

    # Ruta del archivo origen, destino y final
    archivo_origen1 = f"{sTv.var_RutaInforme}{var_NombreSalida}_Datos.xlsx"
    archivo_origen2 = f"{sTv.var_RutaInforme}{var_NombreSalida}_Totales.xlsx"
    archivo_destino = f"{sTv.var_RutaInforme}{var_NombreSalida}_Final.xlsx"

    try:
        if not os.path.exists(archivo_origen1):
            raise FileNotFoundError(Fore.RED + f"¡Archivo no encontrado! {archivo_origen1}\n")
    except FileNotFoundError as e:
        print(e)
        sys.exit(0)
    try:
        if not os.path.exists(archivo_origen2):
            raise FileNotFoundError(Fore.RED + f"¡Archivo no encontrado! {archivo_origen2}\n")
    except FileNotFoundError as e:
        print(e)
        sys.exit(0)

    # Solo vale si TRIMESTRAL = 1, no vale para MENSUAL ni ANUAL
    if var_TIPODESCARGA != 1:
        print(" --- Fin del proceso --- ")
        sys.exit()
    # ------

    funcion_crea_excelSalida(archivo_destino)
    funcion_copia_excelSalida(archivo_origen1, "DATA",    archivo_destino, "DATA")
    funcion_copia_excelSalida(archivo_origen2, "TOTALES", archivo_destino, "TOTALES1")
    funcion_resumen_tipo1(archivo_destino, var_EJERCICIO, var_TRIMESTRE, var_TipoDes)
    #funcion_resumen_tipo2(archivo_destino)  revisar los resultados de "RESULTADOS_1"
    funcion_crea_excelTotales2(archivo_origen1, archivo_origen2, archivo_destino, "TOTALES2")
    #funcion_formatea_excelFinal2(archivo_destino)   STV: da error por lo que sea se queda bloqueado el excel final
  
