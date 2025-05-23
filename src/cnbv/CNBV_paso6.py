# ----------------------------------------------------------------------------------------
#  PASO6: MANDA POR EMAIL EL INFORME FINAL
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.CNBV_variables as sTv
from   cfg.CNBV_librerias import *

# ----------------------------------------------------------------------------------------
#                              FUNCIONES
# ----------------------------------------------------------------------------------------

# Función para cambiar los colores en las etiquetas TR HTML
def aplicar_colores_alternos(tabla_html):
    soup = BeautifulSoup(tabla_html, "html.parser")
    filas = soup.find_all("tr")
    for i, fila in enumerate(filas[1:]):  # saltamos la cabecera (filas[0])
        color = "#f2f2f2" if i % 2 == 0 else "#ffffff"  # (gris=f2f2f2 verdeAgua=f2fff3)
        estilo_existente = fila.get("style", "")
        fila["style"] = f"{estilo_existente} background-color: {color};"

    return str(soup)

def alinear_columnas_derecha(html_tabla, indices_derecha):
    soup = BeautifulSoup(html_tabla, "html.parser")
    filas = soup.find_all("tr")[1:]  # saltamos la cabecera

    for fila in filas:
        celdas = fila.find_all(["td", "th"])
        for idx in indices_derecha:
            if idx < len(celdas):
                estilo = celdas[idx].get("style", "")
                celdas[idx]["style"] = f"{estilo} text-align: right;"

    return str(soup)

# Función envió de Email
def enviar_email_con_adjunto(destinatarios_to, destinatarios_cc, asunto, cuerpo, ruta, nombre_archivo, df1, df2):
    # Configuración del servidor SMTP (Zimbra)
    smtp_server = 'zimbra.tda-sgft.com'
    smtp_port = 25  
    correo_remitente = 'publicacionesbolsasmx@tda-sgft.com'  
    contrasenia = 'tu_contraseña'  # no procede

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = correo_remitente
    mensaje['To'] = ", ".join(destinatarios_to)
    mensaje['Cc'] = ", ".join(destinatarios_cc)
    mensaje['Subject'] = asunto
    
    # Combinar destinatarios principales y en copia
    todos_destinatarios = destinatarios_to + destinatarios_cc 

    # Convertir el DataFrame a HTML - escape=False para que tenga en cuenta las etiquetas HTML
   
    # Función para aplicar colores alternos
    tabla_html1 = aplicar_colores_alternos(df1.to_html(index=True, escape=False))
    tabla_html2 = aplicar_colores_alternos(df2.to_html(index=True, escape=False))
    # Función para alinear a la derecha x columnas
    tabla_html1 = alinear_columnas_derecha(tabla_html1, indices_derecha=[2])
    tabla_html2 = alinear_columnas_derecha(tabla_html2, indices_derecha=[4, 5, 6, 7, 8, 9, 10])

    # Cuerpo del correo usando HTML y CSS
    cuerpo_html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
            }}
            .content {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            h2 {{
                color: #20b2aa;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 8px 12px;
                text-align: left;
                border: 1px solid #ddd;
            }}
            th {{
                background-color: #20b2aa;
                color: white;
            }}
            tr:nth-child(even) {{
				background-color: #f2f2f2;
			}}
			tr:nth-child(odd) {{
				background-color: #ffffff;
			}}
        </style>
    </head>
    <body>
        <div class="content">
            
            <h2>INFORME TRIMESTRAL DE LOS ESTADOS FINANCIEROS DE CNBV</h2>
            <p>{cuerpo}</p>

            <br><br>
            <h3>Cuadro Resumen Total por Concepto</h3>
            {tabla_html1}  <!-- Aquí se inserta el DF convertido a HTML  #59a62c=#20b2aa -->
            <p></p><br><p></p><br>

            <h3>Cuadro Resumen Total por ClavePizarra</h3>
            {tabla_html2}  <!-- Aquí se inserta el DF convertido a HTML  #59a62c=#20b2aa -->
            <p></p><br><p></p><br>
            
            <p>  </p><br><p></p>
            <i> ** Este email fue enviado desde un proceso automático desde TdA. Por favor, no responder a este email. ** </i>
            
            
                <p>
                    <br><br>
                    <br><br>
                    <br><br>
                    <br><br>

                    <table style="border: none; padding: 10px; border-spacing: 2px; width: 600px; table-layout: fixed;">
                        <tr>
                            <td style="width: 150px; padding-right: 10px; vertical-align: middle; border: 1px solid white;">
                                <img src="https://www.tda-sgft.com/TdaWeb/images/logotipo.gif" alt="Titulización de Activos S.G.F.T., S.A" style="vertical-align: middle;">
                            </td>
                            <td style="width: 450px; padding-left: 10px; vertical-align: middle; border: 1px solid white;">
                                <pre>
 Titulización de Activos S.G.F.T., S.A.
 C/Orense, 58 - 5ª Planta
 28020 Madrid
 Tel.: 91 702 08 08
 Fax:  91 308 68 54             
 e-mail: publicacionesbolsasmx@tda-sgft.com
 http://www.tda-sgft.com       </pre>
                            </td>
                        </tr>
                    </table>
                </p>
            
            
        </div>
    </body>
    </html>
    """
    # El cuerpo del mensaje en formato: html
    mensaje.attach(MIMEText(cuerpo_html, 'html'))

    # El cuerpo del mensaje en formato: TXT
    #mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Combinar la ruta con el nombre del archivo
    archivo_completo = os.path.join(ruta, nombre_archivo)
    print(f'- Se adjunta al email el file: {archivo_completo}')

    # Adjuntar el archivo Excel  --- HEMOS DECIDIDO NO MANDAR EL EXCEL
    try:
        with open(archivo_completo, 'rb') as archivo:
            # Crear el objeto MIME para el archivo adjunto
            adjunto = MIMEApplication(archivo.read(), _subtype='xlsx')
            adjunto.add_header('Content-Disposition', 'attachment', filename=nombre_archivo)
            mensaje.attach(adjunto)
    except Exception as e:
        print(f"Error al adjuntar el archivo: {e}")

    # Enviar el correo
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as servidor:
            servidor.sendmail(correo_remitente, todos_destinatarios, mensaje.as_string())
        print(f"- Correo enviado exitosamente a: {', '.join(todos_destinatarios)}")
    except Exception as e:
        print(f"- Error al enviar el correo: {e}")

# Función Leer excel y convertirlos en DataFrame
def sTv_paso6_formatea_DF(df_TOTALES1, df_TOTALES2):
    
    v1="Total de activos"
    v2="Total de activos circulantes"
    v3="Total de capital contable"
    v4="Total de pasivos circulantes"
    v5="Total pasivos"
    v6="Utilidad (pérdida) de operación"
    v7="Utilidad (pérdida) neta"
    
    # Crear DF 1 - Totales Global ----------------------------------------
    df_TOTALES1["ColumnaB"] = pd.to_numeric(df_TOTALES1["ColumnaB"], errors="coerce").fillna(0)
    total_1 = df_TOTALES1[df_TOTALES1["ColumnaA"] == v1]["ColumnaB"].sum()
    total_2 = df_TOTALES1[df_TOTALES1["ColumnaA"] == v2]["ColumnaB"].sum()
    total_3 = df_TOTALES1[df_TOTALES1["ColumnaA"] == v3]["ColumnaB"].sum()
    total_4 = df_TOTALES1[df_TOTALES1["ColumnaA"] == v4]["ColumnaB"].sum()
    total_5 = df_TOTALES1[df_TOTALES1["ColumnaA"] == v5]["ColumnaB"].sum()
    total_6 = df_TOTALES1[df_TOTALES1["ColumnaA"] == v6]["ColumnaB"].sum()
    total_7 = df_TOTALES1[df_TOTALES1["ColumnaA"] == v7]["ColumnaB"].sum()
    # Crear un DF de salida
    df_1 = pd.DataFrame({
        "Concepto": [v1, v2, v3, v4, v5, v6, v7],
        "Total": [total_1, total_2, total_3, total_4, total_5, total_6, total_7]
    })
    df_1.index = range(1, len(df_1) + 1)  # empiece por el indice 1
    df_1["Total"] = df_1["Total"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    print(df_1)

    # Crear DF 2 - Totales Resumen ------------------------------------------
    df_2=df_TOTALES2
    # Elimino campos
    df_2.drop(columns=["Iden"], inplace=True)
    df_2.drop(columns=["Periodo"], inplace=True)
    df_2.drop(columns=["Taxonomia"], inplace=True)
    # Convierto a fecha y luego solo muestro AAAA-MM-DD
    df_2["FEnvio"] = pd.to_datetime(df_2["FEnvio"], errors='coerce')
    df_2["FEnvio"] = df_2["FEnvio"].dt.strftime("%Y-%m-%d")
    # Convierto variables a numéricas
    df_2[v1] = pd.to_numeric(df_2[v1], errors="coerce").fillna(0)
    df_2[v2] = pd.to_numeric(df_2[v2], errors="coerce").fillna(0)
    df_2[v3] = pd.to_numeric(df_2[v3], errors="coerce").fillna(0)
    df_2[v4] = pd.to_numeric(df_2[v4], errors="coerce").fillna(0)
    df_2[v5] = pd.to_numeric(df_2[v5], errors="coerce").fillna(0)
    df_2[v6] = pd.to_numeric(df_2[v6], errors="coerce").fillna(0)
    df_2[v7] = pd.to_numeric(df_2[v7], errors="coerce").fillna(0)
    # Empiece por el indice 1
    df_2.index = range(1, len(df_2) + 1)
    # Formato miles
    df_2[v1] = df_2[v1].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df_2[v2] = df_2[v2].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df_2[v3] = df_2[v3].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df_2[v4] = df_2[v4].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df_2[v5] = df_2[v5].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df_2[v6] = df_2[v6].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df_2[v7] = df_2[v7].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    print(df_2)
    print(" ")

    return df_1, df_2


# ----------------------------------------------------------------------------------------
#                             INICIO DE PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso6(var_NombreSalida, var_EJERCICIO, var_TRIMESTRE, var_TIPODESCARGA, var_TipoDes2, var_Fechas1):

    # Ruta del archivo origen, destino y final
    archivo_destino = f"{sTv.var_RutaInforme}{var_NombreSalida}_Final.xlsx"

    try:
        if not os.path.exists(archivo_destino):
            raise FileNotFoundError(Fore.RED + f"¡Archivo no encontrado! {archivo_destino}\n")
    except FileNotFoundError as e:
        print(e)
        sys.exit(0)

    # Solo vale si TRIMESTRAL = 1, no vale para MENSUAL ni ANUAL
    if var_TIPODESCARGA != 1:
        print(" --- Fin del proceso --- ")
        sys.exit()

    df_TOTALES1 = pd.read_excel(archivo_destino,sheet_name="TOTALES1")
    df_TOTALES2 = pd.read_excel(archivo_destino,sheet_name="TOTALES2")
    df1, df2 = sTv_paso6_formatea_DF(df_TOTALES1, df_TOTALES2)

    destinatarios_cc = ['carpios@tda-sgft.com']
    #destinatarios_to = ['repcomun@tda-sgft.com']
    destinatarios_to = ['carpios@tda-sgft.com']
    #destinatarios_to = ['stv.madrid@gmail.com']

    asunto = f'Informe Trimestral de los Estados Financieros de CNBV  {var_EJERCICIO}.{var_TRIMESTRE}.{var_TipoDes2} | Tda Update '

    cuerpo=f'Fecha Informe: <b>{var_Fechas1}</b> <br>Ejercicio: <b>{var_EJERCICIO}</b> <br>Trimestre: <b>{var_TRIMESTRE}</b> <br>Tipo de Descarga: <b>{var_TipoDes2}</b>'

    enviar_email_con_adjunto(destinatarios_to, destinatarios_cc, asunto, cuerpo,  sTv.var_RutaInforme, f"{var_NombreSalida}_Final.xlsx", df1, df2)
  