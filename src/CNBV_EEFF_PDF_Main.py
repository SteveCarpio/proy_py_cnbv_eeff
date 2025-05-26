import fitz  # PyMuPDF
import pandas as pd
import re

# Lista de etiquetas a buscar
etiquetas = [
    "TOTAL",
    "Total Activo",
    "Total pasivo circulante",
    "Totales cobrados",
    "Importe Facturado",
    "Suma Total",
    "Valor Total"
]

def generar_patrones(etiquetas):
    patrones = []
    for etiqueta in etiquetas:
        # Escapamos los espacios y caracteres especiales en la etiqueta
        etiqueta_regex = re.escape(etiqueta)
        # Creamos una regex para buscar algo como "Etiqueta: $1,000.00" o "Etiqueta 12345"
        patron = rf"{etiqueta_regex}\s*[:\-]?\s*\$?\s*([\d\.,]+)"
        patrones.append((etiqueta, patron))
    return patrones

def extraer_valores_pdf(ruta_pdf, etiquetas):
    patrones = generar_patrones(etiquetas)
    doc = fitz.open(ruta_pdf)
    resultados = []

    for num_pagina, pagina in enumerate(doc, start=1):
        texto = pagina.get_text()
        for etiqueta, patron in patrones:
            matches = re.findall(patron, texto, flags=re.IGNORECASE)
            for match in matches:
                # Limpieza del número
                valor = match.replace(",", "").replace(" ", "")
                try:
                    valor = float(valor)
                    resultados.append({
                        "Página": num_pagina,
                        "Etiqueta": etiqueta,
                        "Valor": valor
                    })
                except ValueError:
                    continue

    df = pd.DataFrame(resultados)
    return df



x1="C:\\MisCompilados\\PROY_CNBV_EEFF\\PDF\\"
x2="Acta_de_asamblea_AGRO_22_300424_con_anexos_1715209778609.pdf"

ruta_pdf = f"{x1}{x2}"  
df_resultados = extraer_valores_pdf(ruta_pdf, etiquetas)
print(df_resultados)
