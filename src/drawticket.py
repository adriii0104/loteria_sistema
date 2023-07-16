from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import uuid
from datetime import datetime

id = uuid.uuid4()
idgen = str(id)
idgen = idgen[:10]
nuevo = idgen.replace("-", "")
ticket = "BFSSP01"
idticket = nuevo.upper() + ticket
archivo_pdf_azar = nuevo + ".pdf"

def generar_recibo(nombre, concepto, monto):
    # Cantidad de elementos a agregar
    elementos_agregados = 15

    # Tamaño de página personalizado
    altura_elemento = 7  # Altura de cada elemento
    margen_superior = 47  # Margen superior para el contenido del recibo
    margen_inferior = 28  # Margen inferior para el contenido del recibo
    altura_total = margen_superior + (elementos_agregados * altura_elemento) + margen_inferior
    width, height = 75 * mm, altura_total * mm

    # Crear un archivo PDF con el tamaño de página personalizado
    c = canvas.Canvas(archivo_pdf_azar, pagesize=(width, height))

    # Configuraciones de fuente y tamaño
    c.setFont("Helvetica-Bold", 8)  # Aquí estableces la fuente y tamaño en negrita

    # Contenido del recibo
    c.drawString(31 * mm, (altura_total - 10) * mm, "BFS SP#01")

    c.setFont("Helvetica", 6)  # Restauras la fuente y tamaño normal

    c.drawString(4 * mm, (altura_total - 17) * mm, f"TICKET :  {idticket}")

    c.drawString(4 * mm, (altura_total - 21) * mm, f"FECHA :  {datetime.now().strftime('%d/%m/%Y - %I:%M:%S %p')}")
    # Resto del contenido del recibo...

    c.setLineWidth(0.01)  # Grosor de línea de 2 puntos

    # Dibujar línea horizontal
    c.drawString(4 * mm, (altura_total - 23) * mm, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

    c.setFont("Helvetica-Bold", 7)  # Restauras la fuente y tamaño normal
    c.drawString(17 * mm, (altura_total - 28) * mm, f"KING-NOCHE (19/07/2023 - 7:25 PM)")
    
    c.setFont("Helvetica", 6)  # Restauras la fuente y tamaño normal

    # Agregar elementos numerados automáticamente
    for i in range(elementos_agregados):
        numero = i + 1
        elemento = f"{numero}) Elemento {numero}"
        c.drawString(4 * mm, (altura_total - (38 + (i * altura_elemento))) * mm, elemento)
        # Resto del dibujo del elemento...
        c.drawString(60 * mm, (altura_total - (38 + (i * altura_elemento))) * mm, " 50.00")  # Monto fijo para cada elemento
    c.setFont("Helvetica-Bold", 7)
    c.drawString(10 * mm, (altura_total - (45 + (elementos_agregados * altura_elemento))) * mm, f"TOTAL APOSTADO RD$:       130.00")
    c.setFont("Helvetica", 5) 
    c.drawString(0 * mm, (altura_total - (40 + (elementos_agregados * altura_elemento))) * mm, f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    c.drawString(0 * mm, (altura_total - (49 + (elementos_agregados * altura_elemento))) * mm, f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    c.setFont("Helvetica", 5) 
    c.drawString(5 * mm, (altura_total - (55 + (elementos_agregados * altura_elemento))) * mm, "- SI FALTAN MENOS DE 15 MINUTOS PARA LA QUE LA LOTERIA SALGA")
    c.drawString(5 * mm, (altura_total - (57 + (elementos_agregados * altura_elemento))) * mm, "  NO SE EMITIRAN DEVOLUCIONES.")
    c.drawString(5 * mm, (altura_total - (60 + (elementos_agregados * altura_elemento))) * mm, "- ESTA JUGADA CADUCA EN 30 DIAS.")
    c.setFont("Helvetica-Bold", 5) 
    c.drawString(20 * mm, (altura_total - (66 + (elementos_agregados * altura_elemento))) * mm, "NO OLVIDE REVISAR SU TICKET!.")
    c.setFont("Helvetica", 5) 
    c.drawString(20 * mm, (altura_total - (69 + (elementos_agregados * altura_elemento))) * mm, "GRACIAS POR SU JUGADA. SUERTE!.")

    # Guardar el recibo y finalizar el lienzo del PDF
    c.showPage()
    c.save()

# Ejemplo de uso
generar_recibo("John Doe", "Venta de productos", "$100.00")
