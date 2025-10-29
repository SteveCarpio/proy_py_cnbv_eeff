# ----------------------------------------------------------------------------------------
#  PASO4: CREAR INFORME DE TOTALES FILTRADOS
#  Autor: SteveCarpio-2024
# ----------------------------------------------------------------------------------------

import cfg.CNBV_variables as sTv
from   cfg.CNBV_librerias import *

# ----------------------------------------------------------------------------------------
#                             INICIO DE PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso4(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes):

    # Solo vale si TRIMESTRAL = 1, no vale para MENSUAL ni ANUAL
    if var_TIPODESCARGA != 1:
        print(" --- Fin del proceso --- ")
        sys.exit()
    # ------

    resultados = []
    var_cont=0
    var_cont_total=len(glob.glob(f'{sTv.var_RutaXls}{var_TipoDes}_{var_EJERCICIO}_{var_TRIMESTRE}__*.xlsx'))

    if var_cont_total == 0:
        print(Fore.RED + f"¡No existen ficheros Excel ({sTv.var_RutaXls}{var_TipoDes}_{var_EJERCICIO}_{var_TRIMESTRE}__*.xlsx).\n")
        sys.exit(0)

    # Iterar sobre todos los archivos en la carpeta
    #for archivo in os.listdir(sTv.var_RutaXls): 
    for archivo_full in glob.glob(f'{sTv.var_RutaXls}{var_TipoDes}_{var_EJERCICIO}_{var_TRIMESTRE}__*.xlsx'):
        archivo = os.path.basename(archivo_full)
        if archivo.endswith('.xlsx') and archivo.startswith(var_TipoDes):
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

            # Recorremos las listas agrupadas
            for i,lista in enumerate(filtroX):
                var_cont2 = var_cont2 + 1
                # Identificamos el libro de donde extraer los datos
                if var_cont2 == 6 or var_cont2 == 7:
                    var_libroX = sTv.var_libro2
                else:
                    var_libroX = sTv.var_libro1

                # Recorro la listaX y obtener el valor total filtrado
                for j, row in lista.iterrows():
                    valor_columna_0 = row.iloc[0]  # La columna A
                    valor_columna_1 = row.iloc[1]  # La columna B
                    valor_columna_2 = row.iloc[2]  # La columna C
                    
                    # Insertamos el valor localizado en un nueva lista con los resultados
                    resultados.append([var_Iden,var_libroX,valor_columna_0,valor_columna_1, valor_columna_2,archivo])
            
    # Crear un DataFrame con los resultados encontrados
    df_resultados = pd.DataFrame(resultados, columns=['Iden','Hoja','ColumnaA','ColumnaB','ColumnaC','File'])

    # Creo un excel con el resultado del DataFrame
    df_resultados.to_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_Totales.xlsx',sheet_name='TOTALES', index=False)
