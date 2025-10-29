# ----------------------------------------------------------------------------------------
#  PASO1: WEBSCRAPING DE LA WEB CNBV
#  Autor: SteveCarpio-2024
# ----------------------------------------------------------------------------------------

import cfg.CNBV_variables as sTv
from   cfg.CNBV_librerias import *

# ----------------------------------------------------------------------------------------
#                                    INICIO WEB SCRAPPING
# ----------------------------------------------------------------------------------------

def sTv_paso1(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA):

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)          # desde WWW
    driver = webdriver.Chrome(service=Service(sTv.var_CHROMEDRIVER)) # desde Local solo esta linea
    driver.maximize_window()
    driver.get(sTv.var_WEBSCRAPING)

    # Hago un pause largo porque la web tarda mucho en cargar
    print("Damos tiempo a cargar la WEB 1")
    time.sleep(15)
    print("Damos tiempo a cargar la WEB 2")
    time.sleep(5)

    # Cargo la pestaña de tipo de descarga: Trimestral, Mensual o Anual
    print("Cargamos el prompt (Seleccione Periodicidad) : Trimestral ¡Ojo Solo esta activo para Trimestral! ")
    var_pestaniaWeb=f'//*[@id="contenedorFormatos"]/div[2]/div[1]/div[1]/select'
    web_tipoDescarga=driver.find_element(By.XPATH,var_pestaniaWeb)
    web_tipoDescarga.send_keys("Trimestral")
    time.sleep(5)

    # Cargo los valores de las Celdas de entrada: Ejercicio
    print(f"Cargamos el prompt (Ejercicio) : {var_EJERCICIO} ")
    web_celdaTxt1=driver.find_element(By.XPATH,'//*[@id="contenedorFormatos"]/div[2]/div[2]/div/div[3]/select') 
    web_celdaTxt1.send_keys(var_EJERCICIO)  # sTv: automatizar esto
    time.sleep(5)
   

    # Cargo los valores de las Celdas de entrada: Trimestre
    if var_TIPODESCARGA == 1:
        web_celdaTxt2=driver.find_element(By.XPATH,'//*[@id="contenedorFormatos"]/div[2]/div[2]/div/div[4]/div[1]/select')                                         
        web_celdaTxt2.send_keys(var_TRIMESTRE)
        time.sleep(2)

    # Cargo el máximo de elementos de la web a 10, no pongo MAS pq el orden de las cajas varían
    print("Cargamos el prompt (Mostrar) : 10 registros por página ")
    web_numElem = driver.find_element(By.XPATH, '//*[@id="tablaInfEnviada_length"]/label/select')
    web_numElem.send_keys("10")          
    time.sleep(5)
    
    # Obtener el valor Maximo de paginas **** STV: si no existe mas de 5 pag debería hacer un TRY y q el valor web_NumMaximoPag sea 5
    lnk1=driver.find_element(By.XPATH,'//*[@id="tablaInfEnviada_paginate"]/span/a[6]')
    web_NumMaximoPag = lnk1.text
    web_NumMaximoPag = int(web_NumMaximoPag) 
    print(f'---------------------------------------- \n Número de paginas a navegar {web_NumMaximoPag}')


    if (web_NumMaximoPag * 10) < 500:
        # SI EL TOTAL DE REGISTROS ES INFERIOR A 500 SE PODRÁ LEER 1 PAGINA A NAVEGAR
        print(f" Hay {web_NumMaximoPag} paginas X 10 = ({web_NumMaximoPag * 10}) son menos de (500) registros a leer: ")

        # Cargo el filtro por 500 registros 
        print(" Cargamos el prompt (Mostrar) : 500 registros por página ")
        var_mostrar=f'//*[@id="tablaInfEnviada_length"]/label/select'
        web_mostrar=driver.find_element(By.XPATH,var_mostrar)
        web_mostrar.send_keys("500")
        time.sleep(10)
        
        # Extraer el código HTML entero
        page_source = driver.find_element("xpath", "//*").get_attribute("outerHTML") 
        salidaHtml=f'{sTv.var_RutaWebFiles}{var_NombreSalida}_1.html'
        with open(salidaHtml, "w", encoding="utf-8") as file:
            file.write(page_source)
        print(f' Descarga: {salidaHtml}')

    else:
        # Hago click en las paginas siguientes, primero en las 5 cajas fijas luego se refresca el N pagina en la caja 5
        for i in range(1,web_NumMaximoPag + 1):
            if i < 6:    
                # Hago click en las primeras 5 cajas que son fijas
                web_paginas=f'//*[@id="tablaInfEnviada_paginate"]/span/a[{i}]'
            else:
                # Hago click en la 4 caja que es dinámica para cada pagina cuando se hizo click en la 5pag
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
                print(f" Click pagina {i} link clicked")
                time.sleep(4)
            except:
                print(" Hubo un error o se acabaron las paginas")
                break

            # Extraer el código HTML entero
            page_source = driver.find_element("xpath", "//*").get_attribute("outerHTML") 
            salidaHtml=f'{sTv.var_RutaWebFiles}{var_NombreSalida}_{i}.html'
            with open(salidaHtml, "w", encoding="utf-8") as file:
                file.write(page_source)
            print(f' Descarga({i}/{web_NumMaximoPag}): {salidaHtml}')

    driver.quit()
