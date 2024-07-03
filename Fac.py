import xml.etree.ElementTree as ET
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import os
import platform
import glob

# Función para buscar el archivo XML en la carpeta de descargas
def buscar_archivo_xml(carpeta_descargas):
    archivos_xml = glob.glob(os.path.join(carpeta_descargas, '*.xml'))
    if archivos_xml:
        return archivos_xml[0]
    else:
        return None

# Función para extraer datos del XML
def extraer_datos_xml(archivo_xml):
    tree = ET.parse(archivo_xml)
    root = tree.getroot()
    
    namespaces = {
        'dte': 'http://www.sat.gob.gt/dte/fel/0.2.0', 
    }

    # Extraer datos generales
    datos_generales = root.find('.//dte:DatosGenerales', namespaces)
    fecha_hora_emision = datos_generales.get('FechaHoraEmision')
    tipo = datos_generales.get('Tipo')

    # Extraer datos del emisor
    emisor = root.find('.//dte:Emisor', namespaces)
    nit_emisor = emisor.get('NITEmisor')
    direccion_emisor = emisor.find('.//dte:Direccion', namespaces).text

    # Extraer datos del receptor
    receptor = root.find('.//dte:Receptor', namespaces)
    nombre_receptor = receptor.get('NombreReceptor')
    id_receptor = receptor.get('IDReceptor')

    # Extraer los ítems
    items = root.findall('.//dte:Item', namespaces)
    lista_items = []
    for item in items:
        descripcion = item.find('.//dte:Descripcion', namespaces).text
        cantidad = int(float(item.find('.//dte:Cantidad', namespaces).text))
        precio_unitario = int(float(item.find('.//dte:PrecioUnitario', namespaces).text))
        total = int(float(item.find('.//dte:Total', namespaces).text))
        lista_items.append({
            'descripcion': descripcion,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'total': total
        })

    # Extraer el elemento GranTotal
    total = root.find('.//dte:Totales', namespaces)
    monto_total = int(float(total.find('dte:GranTotal', namespaces).text))

    return {
        'fecha_hora_emision': fecha_hora_emision,
        'tipo': tipo,
        'nit_emisor': nit_emisor,
        'direccion_emisor': direccion_emisor,
        'nombre_receptor': nombre_receptor,
        'id_receptor': id_receptor,
        'items': lista_items,
        'monto_total': monto_total
    }

# Función para centrar texto
def draw_centered_text(c, text, y_position, page_width):
    text_width = c.stringWidth(text, "Helvetica-Bold", 14)
    x_position = (page_width - text_width) / 2
    c.drawString(x_position, y_position, text)

# Función para crear el PDF
def crear_pdf(datos, pdf_filename="recibo.pdf"):

    # Tamaño de la página en puntos (10 cm de ancho por 29.7 cm de largo)
    page_width = 10 * cm
    page_height = 29.7 * cm

    # Crear un archivo PDF
    c = canvas.Canvas(pdf_filename, pagesize=(page_width, page_height))

    # Márgenes y posiciones iniciales
    x_margin = 10
    y_start = page_height - 20
    line_spacing = 10
    y_position = y_start

     # Logo y encabezado
    logo_path = "Logo.jpeg"  # Cambia esto a la ruta de tu imagen de logo
    logo_width = 80  # Ajusta el ancho de tu logo
    logo_height = 80  # Ajusta la altura de tu logo
    c.drawImage(logo_path, x_margin + 20, y_position - 75, width=logo_width, height=logo_height)

    
    c.drawString(page_width - 110, y_position - 15, "FACT")
    c.setFont("Helvetica", 8)
    y_position -= 30
    c.drawString(page_width - 130, y_position, f"Fecha: {datos['fecha_hora_emision'].split('T')[0]}")
    y_position -= line_spacing
    c.drawString(page_width - 130, y_position, f"Hora: {datos['fecha_hora_emision'].split('T')[1]}")
    y_position -= line_spacing
    c.drawString(page_width - 130, y_position, f"NIT: {datos['nit_emisor']}")
    y_position -= line_spacing
    c.drawString(page_width - 130, y_position, f"Dirección: {datos['direccion_emisor'][:18]}")
    y_position -= line_spacing
    c.drawString(page_width - 132, y_position, f"{datos['direccion_emisor'][30:]}")

    # Información del receptor
    y_position -= 20
    c.drawString(x_margin, y_position, "Receptor:")
    y_position -= line_spacing
    c.drawString(x_margin + 20, y_position, f"Nombre: {datos['nombre_receptor']}")
    y_position -= line_spacing
    c.drawString(x_margin + 20, y_position, f"ID: {datos['id_receptor']}")

    # Tabla de productos
    y_position -= 20
    c.drawString(x_margin, y_position, "Cant")
    c.drawString(x_margin + 30, y_position, "DESCRIPCION")
    c.drawString(x_margin + 150, y_position, "Precio")
    c.drawString(x_margin + 200, y_position, "total")
    
    y_position -= line_spacing
    for item in datos['items']:
        c.drawString(x_margin + 5, y_position, str(item['cantidad']))
        c.drawString(x_margin + 30, y_position, item['descripcion'])
        c.drawString(x_margin + 150, y_position, str(item['precio_unitario']))
        c.drawString(x_margin + 200, y_position, str(item['total']))
        y_position -= line_spacing

    # Monto total
    y_position -= 20
    c.setLineWidth(2)
    c.line(150, 665, 250, 665)
    c.drawString(x_margin + 175, y_position + 10, "Total:")
    c.drawString(x_margin + 200, y_position + 10, str(datos['monto_total']))

    # Guardar el PDF
    c.save()

# Función para imprimir el PDF
def imprimir_pdf(file_path):
    system_name = platform.system()
    if system_name == "Windows":
        os.startfile(file_path, "print")
    elif system_name == "Darwin":  # macOS
        os.system(f"lp {file_path}")
    elif system_name == "Linux":
        os.system(f"lp {file_path}")

def Facturacion():
    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    
    # Buscar el archivo XML en la carpeta de descargas
    archivo_xml = buscar_archivo_xml(carpeta_descargas)
    
    if archivo_xml:
        datos = extraer_datos_xml(archivo_xml)
        
        pdf_filename = "recibo.pdf"
        crear_pdf(datos, pdf_filename)

        # Imprimir el PDF
        #imprimir_pdf(pdf_filename)

        # Borrar el archivo XML
        os.remove(archivo_xml)
    else:
        print("No se encontró ningún archivo XML en la carpeta de descargas.")

# Llamar a la función de facturación
Facturacion()
