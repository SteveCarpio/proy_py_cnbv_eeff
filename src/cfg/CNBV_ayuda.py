# ----------------------------------------------------------------------------------------
#  AYUDA: Ayuda del programa
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.CNBV_variables as sTv
from   cfg.CNBV_librerias import *

# ----------------------------------------------------------------------------------------
#                                  CUADRO DE AYUDA
# ----------------------------------------------------------------------------------------
def sTv_ayuda():
    os.system("cls")
    print(Fore.MAGENTA + "=" * 96)
    print(Fore.MAGENTA + "                               Proceso WebScraping CNBV EEFF\n")
    print(Fore.MAGENTA + " Este programa ha sido desarrollado en Python y utiliza Google Chrome (a través de herramientas")
    print(Fore.MAGENTA + " de automatización como Selenium o similares) para establecer una conexión con el sitio web de ")
    print(Fore.MAGENTA + " la Comisión Nacional Bancaria y de Valores (CNBV).\n")
    print(Fore.MAGENTA + " El objetivo principal del programa es automatizar la recolección de Estados Financieros ")
    print(Fore.MAGENTA + " disponibles en formato Excel. A través de filtros predefinidos, el sistema realiza una búsqueda")
    print(Fore.MAGENTA + " específica en el portal de la CNBV, localiza los archivos Excel disponibles, extrae la ")
    print(Fore.MAGENTA + " información relevante y genera un nuevo archivo Excel consolidado con los datos obtenidos.\n")
    print(Fore.MAGENTA + " Una vez finalizado el proceso de extracción y consolidación, el programa genera un informe ")
    print(Fore.MAGENTA + " resumen y lo envía por correo electrónico, incluyendo como adjunto el archivo Excel generado.")
    print(Fore.MAGENTA + "=" * 96)
    print("")
    print(Fore.WHITE + "Servidor:")
    print(Fore.WHITE + "    IP: 10.10.30.55 (Python)")
    print(Fore.WHITE + "    Usuario: Fiduciario")
    print(Fore.WHITE + "    Contraseña: Gestionada por Cerberus")
    print("")
    print(Fore.WHITE + "Ruta raíz:")
    print(Fore.WHITE + "    C:\\MisCompilados\\PROY_CNBV_EEFF\\")
    print("")
    print(Fore.WHITE + "Ejecución:")
    print(Fore.WHITE + "    CNV_EEFF_Main.exe ")
    print("")
    print(Fore.WHITE + "Parámetros [? | PRO | DEV] (opcional):")
    print(Fore.WHITE + "    [vació]: Muestra el menú actual y se procesa en modo DEV")
    print(Fore.WHITE + "    ?: Muestra la ayuda del programa")
    print(Fore.WHITE + "    PRO: Se procesará todos los emisores que estén activos en la CNBV")
    print(Fore.WHITE + "    DEV: Se procesará solo 10 emisores para hacer una previsualización")
    print("")
    print(Fore.WHITE + "Planificación:")
    print(Fore.WHITE + "    Su ejecución será AD-DOC solicitada por el usuario")
    print("")
    print(Fore.WHITE + "Pasos de ejecución:")
    print("")
    print(Fore.YELLOW + "    1) NAVEGAR POR LA WEB CNBV Y DESCARGAR LOS CÓDIGOS 'HTML'")
    print(Fore.WHITE + "        Este paso abrirá el navegador Chrome y será ejecutado automáticamente")
    print(Fore.WHITE + "        Es importe que en este paso no se toque el explorador de internet")
    print("")
    print(Fore.GREEN + "    2) CREAR INFORME 'DATOS' CON LA LINEA 'CURL'")
    print(Fore.WHITE + "        Este paso leerá el code de los html descargados para crear un documentos excel")
    print(Fore.WHITE + "        con la línea curl que será usada más adelante")
    print("")
    print(Fore.YELLOW + "    3) DESCARGA FICHEROS 'xlsx | pdf' A PARTIR DEL EXCEL 'DATOS'")
    print(Fore.WHITE + "        Este paso usará el informe DATOS que tiene la línea curl para hacer una descarga")
    print(Fore.WHITE + "        del tipo de fichero seleccionado 'excel o pdf' ")
    print("")
    print(Fore.BLUE + "    4) CREAR INFORME 'TOTALES' A PARTIR DE LOS EXCEL DESCARGADOS")
    print(Fore.WHITE + "        Este paso extraerá la información de Estados Financieros de todos los excel ")
    print(Fore.WHITE + "        que se han descargado, filtrando por las hojas y filas definidas por el usuario")
    print("")
    print(Fore.BLUE + "    5) CREAR INFORME 'FINAL' A PARTIR DE LOS EXCEL 'DATOS' y 'TOTALES'")
    print(Fore.WHITE + "        Este paso creará un informe FINAL con los datos de los resúmenes creados ordenados")
    print(Fore.WHITE + "        y diferenciados por hojas independientes ")
    print(Fore.WHITE + "        * Se añade la creación de cuadros de resumen que no están terminados ")
    print("")
    print(Fore.YELLOW + "    6) MANDAR POR EMAIL EL INFORME 'FINAL' ")
    print(Fore.WHITE + "        Este paso mandará vía email el informe FINAL a REPCOMUN")
    print(Fore.WHITE + "        adjunto se mandará el excel con los EEFF y una tabla descriptiva en el cuerpo del email ")
    print("")
    print(Fore.WHITE + "Dependencias importantes:")
    print("")
    print(Fore.WHITE + "    - Google Chrome:")
    print(Fore.WHITE + "        Es fundamental tener instalada una versión estable (no Beta).")
    print("")
    print(Fore.WHITE + "    - ChromeDriver:")
    print(Fore.WHITE + "        Debe coincidir con la versión de Google Chrome instalada.")
    print(Fore.WHITE + "        Ruta del binario: C:\\MisCompilados\\cfg\\chromedriver-win32\\chromedriver.exe")
    print(Fore.WHITE + "        Para otras versiones: C:\\MisCompilados\\cfg\\chromedriver-win32\\1??\\")
    print("")
    print(Fore.WHITE + "    - Acceso a las URL:")
    print(Fore.WHITE + "        https://xbrl.cnbv.gob.mx/visorXbrl.html#/enviosInformacionFinanciera")
    print("")
    print(Fore.WHITE + "    - Acceso SMTP de TDA:")
    print(Fore.WHITE + "        Se debe tener acceso a: zimbra.tda-sgft.com por el puerto 25 ")
    print("")

    print(Fore.MAGENTA + "=" * 94)
    print(Fore.WHITE + "  Para más ayuda, contactar con: SteveCarpio 'carpios@tda-sgft.com' (stv.madrid@gmail.com) ")
    print(Fore.WHITE + "  Versión 3 - 2025")
    print(Fore.MAGENTA + "=" * 94)