# ----------------------------------------------------------------------------------------
#  PASO2: CREA XLS CON LA LINEA CURL
# ----------------------------------------------------------------------------------------

import cfg.CNBV_Barrido_config as sTv
from   cfg.CNBV_Barrido_config import *

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
