# ----------------------------------------------------------------------------------------
#                                  VARIABLES DE APOYO
# Descripción: Variables necesarias para la ejecución del proceso.
# Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
#                          API GOOGLE CHROME
# ----------------------------------------------------------------------------------------
var_CHROMEDRIVER="/srv/apps/MisCompilados/.cfg/chromedriver/chromedriver"

# ----------------------------------------------------------------------------------------
#                          URL WEB-SCRAPING
# ----------------------------------------------------------------------------------------
var_WEBSCRAPING="https://xbrl.cnbv.gob.mx/visorXbrl.html#/enviosInformacionFinanciera"

# ----------------------------------------------------------------------------------------
#                          RUTAS DE APOYO
# ----------------------------------------------------------------------------------------
var_RutaRaiz='/srv/apps/MisCompilados/PROY_CNBV_EEFF/'
var_RutaWebFiles=f'{var_RutaRaiz}WEBFILES/'
var_RutaInforme=f'{var_RutaRaiz}INFORMES/'
var_RutaConfig=f'{var_RutaRaiz}CONFIG/'
var_RutaXls=f'{var_RutaRaiz}XLS/'

# ----------------------------------------------------------------------------------------
#                          VARIABLES ORACLE
# ----------------------------------------------------------------------------------------
var_Ora_DNS="COMUN" 
var_Ora_UID="PYDATA"
var_Ora_PWD="PYDATA"
var_Ora_TAB1="P_CNBV_EEFF_TOTALES1"
var_Ora_TAB2="P_CNBV_EEFF_TOTALES2"
var_Ora_TAB3="P_CNBV_EEFF_FILECURL"

# ----------------------------------------------------------------------------------------
#                          HOJAS DEL EXCEL
# ----------------------------------------------------------------------------------------
var_libro1="210000"
var_libro2="310000"

# ----------------------------------------------------------------------------------------
#                          AUTOR
# ----------------------------------------------------------------------------------------
var_sTv1="SteveCarpio-2024"
var_sTv2="stv.madrid@gmail.com" 
