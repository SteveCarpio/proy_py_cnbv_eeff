# ----------------------------------------------------------------------------------------
#  PASO2: CREA XLS CON LA LINEA CURL
#  Autor: SteveCarpio-2024
# ----------------------------------------------------------------------------------------

import cfg.CNBV_variables as sTv
from   cfg.CNBV_librerias import *

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso2(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TipoDes, var_TIPOFILE, var_extencion):

    # Realizar la búsqueda de todos los ficheros HTML
    var_Patron=f'{var_NombreSalida}*.html'
    var_ArchivosHtml = glob.glob(f'{sTv.var_RutaWebFiles}{var_Patron}')
    var_ArchivosSort = sorted(var_ArchivosHtml, key=os.path.getctime)
    var_ArchivosTota = len(var_ArchivosHtml)
    var_listaFinal = []

    if var_ArchivosTota == 0:
        print(Fore.RED + "No existen datos para analizar, compruebe haber ejecutado los pasos anteriores\n")
        sys.exit()

    print(f'TipoDescarga: {var_TipoDes} \nAño: {var_EJERCICIO} \nTrimestre: {var_TRIMESTRE} \nTotalFiles: {var_ArchivosTota}\n')

    for i in range(0,var_ArchivosTota):
        # Leer el contenido del HTML
        with open(var_ArchivosSort[i], "r", encoding="utf-8") as file:
            html_content = file.read()
        # Parsear un objeto para analizar el HTML
        soup = BeautifulSoup(html_content, "html.parser")
        # Buscamos en el HTML las clases=even/odd y creamos una lista bs4
        target_block1 = soup.find_all(class_="even")
        target_block2 = soup.find_all(class_="odd")
        target_block = target_block1 + target_block2

        # Recorro cada lista, en un objeto bs4 creado por 'soup'
        for j in range(0, len(target_block)):
            # Convierto target_block bs4 a un String para hacer el 'replace'
            var_cadena1 = str(target_block[j])
            # De las lineas filtradas (class=even/odd) además solo leo las lineas que tengan esa cadena "javascript"
            if "javascript" in var_cadena1: 
                # Quitamos la parte de texto que no sirve, en algunos casos reemplazamos por "" y otro por ### 
                var_cadena2 = var_cadena1.replace('<tr class="odd" role="row"><td class="sorting_1"><a href="javascript: abaxXBRL.controller.AbaxXBRLInfFinancieraController' \
                                                  '.mostrarDocumentoInstanciaDataTable(',"")
                var_cadena3 = var_cadena2.replace('<tr class="even" role="row"><td class="sorting_1"><a href="javascript: abaxXBRL.controller.AbaxXBRLInfFinancieraController' \
                                                  '.mostrarDocumentoInstanciaDataTable(',"")
                # He puesto el valor "XxX1" porque para que este separado el resultado de esta cadena con la siguiente y quede como resultado
                # valor -->  ###XxX1### en unos registros, en otros registros saldrá   ###<i>etiquetas html no filtradasXXXX ###
                # Luego el valor de este "campo" delimitado por ### se eliminara mas abajo. será el campo DF "xx"
                var_cadena4 = var_cadena3.replace(');"><i class="fa fa-search-plus text-muted" style="color:#18AFA4"></i></a></td><td>',"###XxX1") 
                var_cadena5 = var_cadena4.replace('</td><td>',"###")
                var_cadena6 = var_cadena5.replace('</td></tr>',f'###{var_EJERCICIO}_{var_TipoDes}{var_TRIMESTRE}### .....')
                # Añadimos todos los valores a la lista-string final con todos resultados
                var_listaFinal.append(var_cadena6)

        # Limpiamos las variables, no es necesario en python pero queda bien
        del target_block1,target_block2,target_block,soup,html_content

        # Recorremos una nueva ListaFinal2 separando cada valor del delimitador '###' <-----
        var_listaFinal2 = []
        for k in range(len(var_listaFinal)):
            var_listaFinal2.append(var_listaFinal[k].split('###'))

    # Creamos un DataFrame 'df' con los valores de la lista 'var_listaFinal2'
    var_Columnas1 = ['FileCurl','xx','FEnvio','ClavePizarra','Periodo','Taxonomia','Filtro','CURL']
    df = pd.DataFrame(var_listaFinal2, columns=var_Columnas1)

    # Dividir el contenido del campo1
    df[['FileXbrl', 'Iden']] = df['FileCurl'].str.extract(r"'([^']*)','([^']*)'")

    # Creo el campo TipoFile
    df['TipoFile'] = var_TIPOFILE

    # Borro campos que ya no son necesarios
    df = df.drop(columns=['FileCurl'])
    df = df.drop(columns=['xx'])  

    # Reorganizo el orden los campos del Dataframe
    var_Columnas2 = ['Iden','FEnvio','ClavePizarra','Periodo','Taxonomia','Filtro','FileXbrl','TipoFile','CURL']
    df = df[var_Columnas2]

    # Hago un sort por el campo 'FEnvio'
    df = df.sort_values(by='FEnvio')

    # Reiniciar el índice comenzando desde 1
    df.reset_index(drop=True, inplace=True)  # Primero eliminamos el índice anterior
    df.index = range(1, len(df) + 1)         # Creamos un índice que comienza en 1

    # Recorremos el DF creado para crear el campo CURL
    cont = 0
    for i, row in df.iterrows():
        cont = cont + 1
        v_emisorid=row['Iden']
        v_nonfile1=row['FileXbrl']
        v_nonfile1=v_nonfile1.replace("&","^&")
        v_nonfile2=v_nonfile1.split()[0] + var_extencion
        v_nonfile2=v_nonfile2.replace("%20","_")
        v_nonfile2=v_nonfile2.replace("^&","_")
        v_nonfile2=v_nonfile2.replace(";","_")
        v_curl1='cmd.exe /c curl --request POST --url https://xbrl.cnbv.gob.mx/DocumentoInstancia/BajarArchivoDocumentoInstancia --ssl-no-revoke --header\
        "content-type: application/x-www-form-urlencoded" --data idDocIns='
        v_curl2=" --data tipoArchivo="
        v_curl3=' --data "nombreArchivo='
        v_curl4=' --output '
        df.at[i,'CURL'] = f'{v_curl1}{v_emisorid}{v_curl2}{var_TIPOFILE}{v_curl3}{v_nonfile1}"{v_curl4}{sTv.var_RutaXls}{var_TipoDes}_{var_EJERCICIO}_{var_TRIMESTRE}___{v_emisorid}_{v_nonfile2}'

    # Resultado Final.
    print(df)

    # Creo un excel con el resultado del DataFrame
    df.to_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_Datos.xlsx',sheet_name='DATA', index=False)
    