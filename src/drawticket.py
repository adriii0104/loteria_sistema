from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime
import pytz
import webbrowser



# Definir la zona horaria para la República Dominicana (Atlántico Oriental)
timezone_RD = pytz.timezone('America/Santo_Domingo')

# Obtener la hora actual en la zona horaria de la República Dominicana
now_RD = datetime.now(timezone_RD)

def generar_recibo(nombre_banca ,added_elements, chosen_numbers, amount, total_precio, archivo_pdf_azar, idticket, loterias):
    # Cantidad de elementos a agregar
    elementos_agregados = added_elements

    # Tamaño de página personalizado
    altura_elemento = 8  # Altura de cada elemento
    margen_superior = 28  # Margen superior para el contenido del recibo
    margen_inferior = 35  # Margen inferior para el contenido del recibo

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
    c.drawString(24 * mm, (altura_total - 15) * mm, nombre_banca)

    c.setFont("Helvetica", 6)  # Restauras la fuente y tamaño normal

    c.drawString(4 * mm, (altura_total - 22) * mm, f"TICKET :  {idticket}")

    c.drawString(4 * mm, (altura_total - 25) * mm, f"FECHA :  {now_RD.strftime('%Y-%m-%d %H:%M:%S')}")
    # Resto del contenido del recibo...

    c.setLineWidth(0.01)  # Grosor de línea de 2 puntos

    # Dibujar línea horizontal
    c.drawString(4 * mm, (altura_total - 27) * mm, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

    c.setFont("Helvetica-Bold", 7)  # Restauras la fuente y tamaño normal

    line_height = 8  # Altura de cada línea de texto
    x = 22.5 * mm  # Coordenada x inicial

    # Imprimir loterías
    y_loterias = (altura_total - 30) * mm  # Coordenada y inicial para las loterías
    for loteria in loterias:
        c.drawString(x, y_loterias, loteria)
        y_loterias -= line_height  # Mover hacia abajo para la siguiente línea de texto

    c.setFont("Helvetica-Bold", 7)  # Restauras la fuente y tamaño normal

    # Imprimir números jugados
    y_numeros_jugados = y_loterias - (line_height * 2)  # Coordenada y inicial para los números jugados
    for i in range(elementos_agregados):
        numero = i + 1
        numeros_jugados = chosen_numbers[i]
        elemento = f"{numero}) {numeros_jugados}"
        c.drawString(4 * mm, y_numeros_jugados, elemento)
        # Resto del dibujo del elemento...
        c.drawString(60 * mm, y_numeros_jugados, amount[i])  # Monto fijo para cada elemento
        y_numeros_jugados -= altura_elemento  # Mover hacia abajo para la siguiente línea de texto
        y_numeros_jugados -= 10  # Espacio vertical de 2 unidades entre elementos

    c.setFont("Helvetica-Bold", 7)
    if (altura_loterias >= 32):
        altura_loterias = 23
        print(altura_loterias)
    c.drawString(10 * mm, (altura_total - (31 + altura_loterias + (elementos_agregados * altura_elemento))) * mm,
                 f"TOTAL APOSTADO RD$:       {total_precio}")
    c.setFont("Helvetica", 5)
    c.drawString(0 * mm, (altura_total - (27 + altura_loterias + (elementos_agregados * altura_elemento))) * mm,
                 f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    
    c.drawString(0 * mm, (altura_total - (35 + altura_loterias + (elementos_agregados * altura_elemento))) * mm,
                 f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    
    c.drawString(10 * mm, (altura_total - (40 + altura_loterias + (elementos_agregados * altura_elemento))) * mm,
                 f"REVISE SU TICKET")
    
    c.drawString(10 * mm, (altura_total - (43 + altura_loterias + (elementos_agregados * altura_elemento))) * mm,
                 f"PASADO 15 MINUTOS NO SE ADMITEN DEVOLUCIONES")
    
    c.drawString(10 * mm, (altura_total - (46 + altura_loterias + (elementos_agregados * altura_elemento))) * mm,
                 f"ESTE TICKET ES VALIDO POR 30 DIAS")
    
    c.drawString(10 * mm, (altura_total - (49 + altura_loterias + (elementos_agregados * altura_elemento))) * mm,
                 f"GRACIAS POR PREFERIRNOS - SUERTE -")

    # Guardar el recibo y finalizar el lienzo del PDF
    c.showPage()
    c.save()
    webbrowser.open_new_tab(archivo_pdf_azar)
