import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def enviar_correo(destinatario, usuario, contrasena):
    remitente = 'adriii0104@hotmail.com'
    clave = 'Acd20803@'

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Bienvenido a nuestra familia!"

    # Creamos el contenido del mensaje en formato HTML
    contenido_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                background-color: #f4f4f4;
                color: #333;
            }}

            h1 {{
                color:  #214032;
                text-align: center;
            }}

            p {{
                text-align: justify;
                margin: 20px;
            }}

            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}

            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #0066cc;
                color: #fff;
                text-decoration: none;
                border-radius: 4px;
            }}

            .button:hover {{
                background-color: #0052a3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
        <h1>GRACIAS POR FORMAR PARTE DE NUESTRA FAMILIA.</h1>
        <p>
            GENUINE TE DA LA BIENVENIDA A LA FAMILIA DE BANCAS QUE TE AYUDARÁ A CRECER. <br>
            ESTAMOS CRECIENDO COMO FAMILIA Y QUÉ BUENO QUE TÚ SEAS PARTE DE ESE CRECIMIENTO.<br><br><br>

            Aquí tienes tus credenciales de inicio de sesión: <br>
            usuario: {usuario} <br>
            contraseña: {contrasena} <br><br><br>
            <a href="adriii0104@hotmail.com">
            <button class="button">Contactanos</button></a>
        </p>
        </div>
    </body>
    </html>
    """
    contenido_parte = MIMEText(contenido_html, 'html')
    mensaje.attach(contenido_parte)

    # Adjuntamos el archivo PDF si se proporciona
    archivo_adjunto = 'documents/gnuineterminos.pdf'  # Reemplaza con la ruta del archivo PDF que deseas adjuntar
    if archivo_adjunto:
        with open(archivo_adjunto, 'rb') as archivo:
            adjunto = MIMEApplication(archivo.read(), _subtype='pdf')
        adjunto.add_header('Content-Disposition', f'attachment; filename="{archivo_adjunto}"')
        mensaje.attach(adjunto)

    servidor_smtp = 'smtp-mail.outlook.com'
    puerto_smtp = 587
    servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
    servidor.starttls()

    servidor.login(remitente, clave)
    servidor.send_message(mensaje)
    servidor.quit()
def enviar_correo2(destinatario, usuario, contrasena):
    remitente = 'adriii0104@hotmail.com'
    clave = 'Acd20803@'

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Bienvenido a nuestra familia!"

    # Creamos el contenido del mensaje en formato HTML
    contenido_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                background-color: #f4f4f4;
                color: #333;
            }}

            h1 {{
                color: #214032;
                text-align: center;
            }}

            p {{
                text-align: justify;
                margin: 20px;
            }}

            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}

            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #0066cc;
                color: #fff;
                text-decoration: none;
                border-radius: 4px;
            }}

            .button:hover {{
                background-color: #0052a3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
        <h1>NUEVO REGISTRO DE SUCURSAL.</h1>
        <p>
            HEMOS REGISTRADO TU NUEVA SUCURSAL UBICADA EN ..... <br>
            VEMOS QUE TU NEGOCIO VA CRECIENDO CADA VEZ MAS! NOS ALEGRA ENTERARNOS DE ESO.<br><br><br>

            Aquí tienes tus credenciales de inicio de sesión: <br>
            usuario: {usuario} <br>
            contraseña: {contrasena} <br><br><br>

            A continuación, tendrás a tu disposición algunos de nuestros términos y condiciones
            como proveedores de servicios de lotería:<br>
        </p>
        </div>
    </body>
    </html>
    """
    contenido_parte = MIMEText(contenido_html, 'html')
    mensaje.attach(contenido_parte)


    servidor_smtp = 'smtp-mail.outlook.com'
    puerto_smtp = 587
    servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
    servidor.starttls()

    servidor.login(remitente, clave)
    servidor.send_message(mensaje)
    servidor.quit()


