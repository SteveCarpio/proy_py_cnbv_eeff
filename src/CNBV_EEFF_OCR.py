import os
from pdf2image import convert_from_path
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_pdf(pdf_path):
    """Convierte PDF en texto usando OCR."""
    print(f"Procesando: {pdf_path}")
    texto_total = ""
    try:
        # ------------------------------------------------------------------------------------
        # DPI       Calidad de imagen	OCR (Tesseract)	 Tamaño de archivo	Velocidad
        # 100–150	Baja	            Baja	         Pequeño            Muy rápido
        # 200	    Aceptable	        Aceptable	     Moderado	        Rápido
        # 300	    Alta (óptima)	    Muy buena	     Mayor	            Más lento
        #400–600+	Muy alta	Ligeramente mejor	     Muy grande	        Mucho más lento
        pages = convert_from_path(pdf_path, dpi=300, poppler_path=r'C:\poppler\Library\bin')
        # ------------------------------------------------------------------------------------
        
        for page_num, page in enumerate(pages):
            text = pytesseract.image_to_string(page, lang='spa')  # 'eng' si es inglés
            texto_total += f"\n\n--- Página {page_num+1} ---\n\n{text}"
    except Exception as e:
        print(f"Error procesando {pdf_path}: {e}")
    return texto_total

def procesar_lista_pdfs(lista_rutas):
    """Procesa una lista de PDFs."""
    resultados = {}
    for pdf in lista_rutas:
        texto = ocr_pdf(pdf)
        resultados[pdf] = texto
    return resultados

# Ejemplo de uso:
if __name__ == "__main__":
    lista_pdfs = [
        "documentos/docu1.pdf",
        "documentos/docu2.pdf"
    ]
    resultados_ocr = procesar_lista_pdfs(lista_pdfs)

    # Guardar resultados en archivos de texto
    for pdf, texto in resultados_ocr.items():
        nombre_txt = os.path.splitext(os.path.basename(pdf))[0] + ".txt"
        with open(f"output_textos/{nombre_txt}", "w", encoding="utf-8") as f:
            f.write(texto)

    print("Todos los documentos fueron procesados.")
