from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime
import webbrowser


def generar_recibo(added_elements, chosen_numbers, amount, total_precio, archivo_pdf_azar, idticket, loterias):
    # Cantidad de elementos a agregar
    elementos_agregados = added_elements

    # Tamaño de página personalizado
    altura_elemento = 7  # Altura de cada elemento
    margen_superior = 47  # Margen superior para el contenido del recibo
    margen_inferior = 28  # Margen inferior para el contenido del recibo

    # Calcular la altura total de la página en función del número de loterías y elementos agregados
    altura_loterias = len(loterias) * altura_elemento
    altura_total = margen_superior + altura_loterias + (elementos_agregados * altura_elemento) + margen_inferior

    # Tamaño de página personalizado
    width, height = 75 * mm, altura_total * mm

    # Verificar si es necesario agregar una nueva página si el contenido supera el tamaño de la página actual
    if altura_total > height:
        c.showPage()  # Agregar una nueva página
        altura_total = margen_superior + altura_loterias + (elementos_agregados * altura_elemento) + margen_inferior
        height = altura_total * mm

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
    c.drawString(4 * mm, (altura_total - 23) * mm, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

    c.setFont("Helvetica", 7)  # Restauras la fuente y tamaño normal

    line_height = 8  # Altura de cada línea de texto
    x = 17 * mm  # Coordenada x inicial

    # Imprimir loterías
    y_loterias = (altura_total - 28) * mm  # Coordenada y inicial para las loterías
    for loteria in loterias:
        c.drawString(x, y_loterias, loteria)
        y_loterias -= line_height  # Mover hacia abajo para la siguiente línea de texto

    c.setFont("Helvetica-Bold", 7)  # Restauras la fuente y tamaño normal

    # Imprimir números jugados
    y_numeros_jugados = y_loterias - (line_height * 2)  # Coordenada y inicial para los números jugados
    for i in range(elementos_agregados):
        numero = i + 1
        elemento = f"{numero}) {chosen_numbers[i]}"
        c.drawString(4 * mm, y_numeros_jugados, elemento)
        # Resto del dibujo del elemento...
        c.drawString(60 * mm, y_numeros_jugados, amount[i])  # Monto fijo para cada elemento
        y_numeros_jugados -= altura_elemento  # Mover hacia abajo para la siguiente línea de texto

    c.setFont("Helvetica-Bold", 7)
    c.drawString(10 * mm, (altura_total - (45 + altura_loterias + (elementos_agregados * altura_elemento))) * mm,
                 f"TOTAL APOSTADO RD$:       {total_precio}")
    c.setFont("Helvetica", 5)
    c.drawString(0 * mm, (altura_total - (40 + altura_loterias + (elementos_agregados * altura_elemento))) * mm,
                 f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    # Guardar el recibo y finalizar el lienzo del PDF
    c.showPage()
    c.save()
    webbrowser.open_new_tab(archivo_pdf_azar)
