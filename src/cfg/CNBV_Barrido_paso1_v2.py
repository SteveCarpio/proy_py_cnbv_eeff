# ----------------------------------------------------------------------------------------
#  PASO1: WEBSCRAPING DE LA WEB CNBV
#  Autor: SteveCarpio-2024
# ----------------------------------------------------------------------------------------

import cfg.CNBV_Barrido_variables_v2 as sTv
from   cfg.CNBV_Barrido_librerias_v2 import *

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
    var_pestaniaWeb=f'//*[@id="contenedorFormatos"]/header/ul/li[{var_TIPODESCARGA}]/a'
    web_tipoDescarga=driver.find_element(By.XPATH,var_pestaniaWeb)
    web_tipoDescarga.click()
    time.sleep(5)

    # Cargo los valores de las Celdas de entrada: Ejercicio
    # Cargo los valores de las Celdas de entrada: Ejercicio
    web_celdaTxt1=driver.find_element(By.XPATH,'//*[@id="contenedorFormatos"]/div[2]/div/div/div[3]/select')
    web_celdaTxt1.send_keys(var_EJERCICIO)
    time.sleep(2)

    # Cargo los valores de las Celdas de entrada: Trimestre
    if var_TIPODESCARGA == 1:
        web_celdaTxt2=driver.find_element(By.XPATH,'//*[@id="contenedorFormatos"]/div[2]/div/div/div[4]/select')
        web_celdaTxt2.send_keys(var_TRIMESTRE)
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
        salidaHtml=f'{sTv.var_RutaWebFiles}{var_NombreSalida}_{i}.html'
        with open(salidaHtml, "w", encoding="utf-8") as file:
            file.write(page_source)
        print(f' Descarga({i}/{web_NumMaximoPag}): {salidaHtml}')

    driver.quit()
