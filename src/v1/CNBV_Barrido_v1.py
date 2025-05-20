# ----------------------------------------------------------------------------------------
#  PASO0: VALIDAR REQUISITOS PREVIOS 
# ----------------------------------------------------------------------------------------

import cfg.CNBV_Barrido_config as sTv
from   cfg.CNBV_Barrido_config import *

# ----------------------------------------------------------------------------------------
#                                  FUNCIONES
# ----------------------------------------------------------------------------------------

# Función: Valida estructura de directorios CNBV
def valida_carpetas(ruta_carpeta):
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        print(f'Carpeta creada: {ruta_carpeta}')
    else:
        print(f'Validando carpeta: {ruta_carpeta}')

# Función: Borrar files creados CNBV
def borrar_archivos(ruta_carpeta, patron):
    # Construir la ruta completa con el patrón
    ruta_completa = os.path.join(ruta_carpeta, patron)
    
    # Encontrar todos los archivos que coincidan con el patrón
    archivos = glob.glob(ruta_completa)
    
    # Borrar cada archivo encontrado
    for archivo in archivos:
        os.remove(archivo)
        print(f'Archivo borrado: {archivo}')

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

# Valida carpetas de CNBV
valida_carpetas(sTv.var_RutaRaiz)
valida_carpetas(sTv.var_RutaWebFiles)
valida_carpetas(sTv.var_RutaInforme)
valida_carpetas(sTv.var_RutaXls)

# Borra files descargados de CNBV
borrar_archivos(sTv.var_RutaWebFiles, f'{sTv.var_NombreSalida}_*.html')
borrar_archivos(sTv.var_RutaXls, f'{sTv.var_TipoDes}_{sTv.var_EJERCICIO}_{sTv.var_TRIMESTRE}__*.xlsx')
borrar_archivos(sTv.var_RutaInforme, f'{sTv.var_NombreSalida}_Datos.xlsx')
borrar_archivos(sTv.var_RutaInforme, f'{sTv.var_NombreSalida}_Final.xlsx')
borrar_archivos(sTv.var_RutaInforme, f'{sTv.var_NombreSalida}_Totales.xlsx')

print(" Requisitos previos ok ")

# ----------------------------------------------------------------------------------------
#  PASO1: WEBSCRAPING DE LA WEB CNBV
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
#                                    INICIO WEB SCRAPPING
# ----------------------------------------------------------------------------------------

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)          # desde WWW
driver = webdriver.Chrome(service=Service(sTv.var_CHROMEDRIVER)) # desde Local solo esta linea
driver.get(sTv.var_WEBSCRAPING)

# Hago un pause largo porque la web tarda mucho en cargar
print("Damos tiempo a cargar la WEB 1")
time.sleep(15)
driver.maximize_window
print("Damos tiempo a cargar la WEB 2")
time.sleep(5)

# Cargo la pestaña de tipo de descarga: Trimestral, Mensual o Anual
var_pestaniaWeb=f'//*[@id="contenedorFormatos"]/header/ul/li[{sTv.var_TIPODESCARGA}]/a'
web_tipoDescarga=driver.find_element(By.XPATH,var_pestaniaWeb)
web_tipoDescarga.click()
time.sleep(5)

# Cargo los valores de las Celdas de entrada: Ejecrcicio
web_celdaTxt1=driver.find_element(By.XPATH,'//*[@id="contenedorFormatos"]/div[2]/div/div/div[3]/select')
web_celdaTxt1.send_keys(sTv.var_EJERCICIO)
time.sleep(2)

# Cargo los valores de las Celdas de entrada: Trimestre
if sTv.var_TIPODESCARGA == 1:
    web_celdaTxt2=driver.find_element(By.XPATH,'//*[@id="contenedorFormatos"]/div[2]/div/div/div[4]/select')
    web_celdaTxt2.send_keys(sTv.var_TRIMESTRE)
    time.sleep(2)

# Cargo el maximo de elementos de la web a 20, no pongo 50 pq el orden de las cajas varian
web_numElem = driver.find_element(By.XPATH, '//*[@id="tablaInfEnviada_length"]/label/select')
web_numElem.send_keys(20)          
time.sleep(5)

# Obtener el valor Maximo de paginas **** STV: si no existe mas de 5 pag deberia hacer un TRY y q el valor web_NumMaximoPag sea 5
lnk1=driver.find_element(By.XPATH,'//*[@id="tablaInfEnviada_paginate"]/span/a[6]')
web_NumMaximoPag = lnk1.text
web_NumMaximoPag = int(web_NumMaximoPag) 
print(f'---------------------------------------- \n Número de paginas a navegar {web_NumMaximoPag}')

# Hago click en las paginas siguientes, primero en las 5 cajas fijas luego se refresca el N pagina en la caja 5
for i in range(1,web_NumMaximoPag + 1):
    if i < 6:    
        # Hago click en las primeras 5 cajas que son fijas
        web_paginas=f'//*[@id="tablaInfEnviada_paginate"]/span/a[{i}]'
    else:
        # Hago click en la 4 caja que es dinamica para cada pagina cuando se hizo click en la 5pag
        web_paginas=f'//*[@id="tablaInfEnviada_paginate"]/span/a[4]'

    if i == web_NumMaximoPag -1:
        web_paginas=f'//*[@id="tablaInfEnviada_paginate"]/span/a[5]'

    if i == web_NumMaximoPag:
        web_paginas=f'//*[@id="tablaInfEnviada_paginate"]/span/a[6]'
        
    lnk2=driver.find_element(By.XPATH,web_paginas)
    print(f" ------------------")
    print(f" Click pagina {i} link fijado")
    try:
        lnk2.click()
        print(f" Click pagina {i} link clickeado")
        time.sleep(4)
    except:
        print(" Hubo un error o se acabaron las paginas")
        break

    # Extraer el cofigo HTML entero
    page_source = driver.find_element("xpath", "//*").get_attribute("outerHTML") 
    salidaHtml=f'{sTv.var_RutaWebFiles}{sTv.var_NombreSalida}_{i}.html'
    with open(salidaHtml, "w", encoding="utf-8") as file:
        file.write(page_source)
    print(f' Descarga({i}/{web_NumMaximoPag}): {salidaHtml}')

driver.quit()

# ----------------------------------------------------------------------------------------
#  PASO2: CREA XLS CON LA LINEA CURL
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

# Realizar la busqueda de todos los ficheros HTML según el patrón seleccionado
var_Patron=f'{sTv.var_NombreSalida}*.html'
var_ArchivosHtml = glob.glob(f'{sTv.var_RutaWebFiles}{var_Patron}')
var_ArchivosSort = sorted(var_ArchivosHtml, key=os.path.getctime)
var_ArchivosTota = len(var_ArchivosHtml)
var_listaFinal = []

print(f'\nNúmero de ficheros a Analizar para. \nTipoDescarga:{sTv.var_TipoDes} \nAño:{sTv.var_EJERCICIO} \nTrimestre:{sTv.var_TRIMESTRE} \nTotalFiles:{var_ArchivosTota}\n')

for i in range(0,var_ArchivosTota):
    
    # Leer el contenido del HTML
    with open(var_ArchivosSort[i], "r", encoding="utf-8") as file:
        html_content = file.read()

    # Crear un objeto BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Buscar el bloque de código HTML que contiene la cadena "<tr role="row"
    # target_block = soup.find_all("tr", {"role": "row"})
    target_block1 = soup.find_all(class_="even")
    target_block2 = soup.find_all(class_="odd")
    target_block = target_block1 + target_block2

    # Recorro cada lista, es un objeto bs4 creado por 'soup'
    for j in range(0, len(target_block)):

        # Convierto target_block que es un objeto bs4 a string para hacer el 'replace'
        var_cadena1 = str(target_block[j])
        
        # Quito la parte de texto que no me sirve
        var_cadena2 = var_cadena1.replace('<tr class="odd" role="row"><td class="sorting_1"><a href="javascript: abaxXBRL.controller.AbaxXBRLInfFinancieraController' \
                                            '.mostrarDocumentoInstanciaDataTable(', "").replace('<tr class="even" role="row"><td class="sorting_1"><a href="javascript: ' \
                                            'abaxXBRL.controller.AbaxXBRLInfFinancieraController.mostrarDocumentoInstanciaDataTable(',"").replace(');"><i class="fa fa-' \
                                            'search-plus text-muted" style="color:#18AFA4"></i></a></td><td>',"###").replace('</td><td>',"###").replace('</td>' \
                                            '</tr>',f'###{sTv.var_EJERCICIO}_{sTv.var_TipoDes}{sTv.var_TRIMESTRE}### .....' )

        # Añadimos todos los valores a la lista-string final con todos resultados
        var_listaFinal.append(var_cadena2)

    # Limpiamos las variables, no es necesario en python pero queda bien
    del target_block1,target_block2,target_block,soup,html_content


# Recorremos una nueva ListaFinal2 separando cada valor del delimitador '###'
var_listaFinal2 = []
for k in range(len(var_listaFinal)):
    var_listaFinal2.append(var_listaFinal[k].split('###'))

# Creamos un DataFrame 'df' con los valores de la lista 'var_listaFinal2'
var_Columnas1 = ['FileCurl','FEnvio','ClavePizarra','Periodo','Taxonomia','Filtro','CURL']
df = pd.DataFrame(var_listaFinal2, columns=var_Columnas1)

# Dividir el contenido del campo1
df[['FileXbrl', 'Iden']] = df['FileCurl'].str.extract(r"'([^']*)','([^']*)'")

# Creo el campo TipoFile
df['TipoFile'] = sTv.var_TIPOFILE

# Borro campos que ya no son necesarios
df = df.drop(columns=['FileCurl'])

# Reorganizo el orden los campos del Dataframe
var_Columnas2 = ['Iden','FEnvio','ClavePizarra','Periodo','Taxonomia','Filtro','FileXbrl','TipoFile','CURL']
df = df[var_Columnas2]

# Hago un sort por el campo 'FEnvio'
df = df.sort_values(by='FEnvio')

# Reiniciar el índice comenzando desde 1
df.reset_index(drop=True, inplace=True)  # Primero eliminamos el índice anterior
df.index = range(1, len(df) + 1)  # Creamos un índice que comienza en 1

# Crear el campo CURL
cont = 0
for i, row in df.iterrows():
    cont = cont + 1
    v_emisorid=row['Iden']
    v_nonfile1=row['FileXbrl']
    v_nonfile1=v_nonfile1.replace("&","^&")
    v_nonfile2=v_nonfile1.split()[0] + sTv.var_extencion
    v_nonfile2=v_nonfile2.replace("%20","_")
    v_nonfile2=v_nonfile2.replace("^&","_")
    v_nonfile2=v_nonfile2.replace(";","_")
    v_curl1='cmd.exe /c curl --request POST --url https://xbrl.cnbv.gob.mx/DocumentoInstancia/BajarArchivoDocumentoInstancia --ssl-no-revoke --header\
    "content-type: application/x-www-form-urlencoded" --data idDocIns='
    v_curl2=" --data tipoArchivo="
    v_curl3=' --data "nombreArchivo='
    v_curl4=' --output '
    df.at[i,'CURL'] = f'{v_curl1}{v_emisorid}{v_curl2}{sTv.var_TIPOFILE}{v_curl3}{v_nonfile1}"{v_curl4}{sTv.var_RutaXls}{sTv.var_TipoDes}_{sTv.var_EJERCICIO}_{sTv.var_TRIMESTRE}___{v_emisorid}_{v_nonfile2}'

# Resultado Final.
print(df)

# Creo un excel con el resultado del DataFrame
df.to_excel(f'{sTv.var_RutaInforme}{sTv.var_NombreSalida}_Datos.xlsx',sheet_name='DATA', index=False)

# ----------------------------------------------------------------------------------------
#  PASO3: DESCARGA FICHEROS VIA CMD CURL
# ----------------------------------------------------------------------------------------

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
          
# ----------------------------------------------------------------------------------------
#  PASO4: CREAR INFORME DE TOTALES FILTRADOS
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
#                             INICIO DE PROGRAMA
# ----------------------------------------------------------------------------------------

# Solo vale si TRIMESTRAL = 1, no vale para MENSUAL ni ANUAL
if sTv.var_TIPODESCARGA != 1:
    print(" --- Fin del proceso --- ")
    sys.exit()
# ------

resultados = []
var_cont=0
var_cont_total=len(glob.glob(f'{sTv.var_RutaXls}{sTv.var_TipoDes}_{sTv.var_EJERCICIO}_{sTv.var_TRIMESTRE}__*.xlsx'))

# Iterar sobre todos los archivos en la carpeta
for archivo in os.listdir(sTv.var_RutaXls):
    if archivo.endswith('.xlsx') and archivo.startswith(sTv.var_TipoDes):
        var_cont = var_cont + 1
        var_Iden= archivo.split("_")[5]  # Extraigo de la posición el IDEN
        print(f'Procesando ({var_cont}/{var_cont_total}): {archivo}')
        
        # Leer libros del archivo Excel
        ruta_archivo = os.path.join(sTv.var_RutaXls, archivo)
        df1 = pd.read_excel(ruta_archivo, sheet_name=sTv.var_libro1)
        df2 = pd.read_excel(ruta_archivo, sheet_name=sTv.var_libro2)

        # Filtrar las filas donde la celda tiene el valor "xxxxx"
        filtro1 = df1[df1.isin(['Total de activos circulantes']).any(axis=1)]
        filtro2 = df1[df1.isin(['Total de activos']).any(axis=1)]
        filtro3 = df1[df1.isin(['Total de pasivos circulantes']).any(axis=1)]
        filtro4 = df1[df1.isin(['Total pasivos']).any(axis=1)]
        filtro5 = df1[df1.isin(['Total de capital contable']).any(axis=1)]
        filtro6 = df2[df2.isin(['Utilidad (pérdida) de operación']).any(axis=1)]
        filtro7 = df2[df2.isin(['Utilidad (pérdida) neta']).any(axis=1)]

        # Creo una lista con el resultado de todas las listas filtradas
        filtroX = [filtro1, filtro2, filtro3, filtro4, filtro5, filtro6, filtro7]

        var_cont2=0

        # Recorremos las listas agrupdas
        for i,lista in enumerate(filtroX):
            var_cont2 = var_cont2 + 1
            # Identificamos el libro de deonde extraer los datos
            if var_cont2 == 6 or var_cont2 == 7:
                var_libroX = sTv.var_libro2
            else:
                var_libroX = sTv.var_libro1

            # Recorro la listaX y obtener el valor total filtrado
            for j, row in lista.iterrows():
                valor_columna_0 = row.iloc[0]  # La columna A
                valor_columna_1 = row.iloc[1]  # La columna B
                valor_columna_2 = row.iloc[2]  # La columna C
                
                # Insertamos el valor localizdo en un nueva lista con los resultados
                resultados.append([var_Iden,var_libroX,valor_columna_0,valor_columna_1, valor_columna_2,archivo])
        
# Crear un DataFrame con los resultados encontrados
df_resultados = pd.DataFrame(resultados, columns=['Iden','Hoja','ColumnaA','ColumnaB','ColumnaC','File'])

# Creo un excel con el resultado del DataFrame
df_resultados.to_excel(f'{sTv.var_RutaInforme}{sTv.var_NombreSalida}_Totales.xlsx',sheet_name='TOTALES', index=False)

# ----------------------------------------------------------------------------------------
#  PASO5: CREA INFORME FINAL A PARTIR DE LOS EXCEL CREADOS "DATOS" y "TOTALES"
# ----------------------------------------------------------------------------------------

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

print(" ------- [ FIN ] -------")
