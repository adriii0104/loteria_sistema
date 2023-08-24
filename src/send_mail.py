import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def enviar_correo(destinatario, usuario, contrasena, email):
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
    <link rel='stylesheet' href='https://cdn-uicons.flaticon.com/uicons-brands/css/uicons-brands.css'>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 0;
        }}

        h1 {{
            color: #214032;
            text-align: center;
            margin-top: 20px;
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

        .button-container {{
            text-align: center;
            margin-top: 30px;
        }}

        .button {{
            display: inline-block;
            padding: 13px 50px;
            background-color: #0066cc;
            color: #fff;
            font-size: 15px;
            text-decoration: none;
            border-radius: 4px;
            border: none;
        }}

        .button:hover {{
            background-color: #0052a3;
        }}

        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background-color: #214032;
            color: #fff;
        }}

    i {{

      display: inline-block;
      width: 30px;
      height: 30px;
      text-decoration: none;
      vertical-align: middle;
      color: white;
    }}
    a{{
      color: white;
    }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Bienvenido a Genuine Finance</h1>
        <p>
            En Genuine Finance, estamos encantados de darte la más cordial bienvenida a nuestra distinguida familia de servicios financieros.
            Es un honor tener la oportunidad de acompañarte en tus objetivos financieros y crecimiento.<br><br>

            A continuación, te presentamos tus credenciales de acceso:<br><br>
            <strong>Usuario:</strong> {usuario}<br>
            <strong>Contraseña:</strong> {contrasena}<br><br>

            <p> 
            Tambien queremos informarle que tenemos una plataforma en la WEB para el monitoreo y mantenimiento de su inversión, la plataforma tiene diversas opciones.<br><br>

            Estas son las credenciales de acceso a la plataforma en la web:
            <strong>Usuario:</strong> {email}
            <strong>Contraseña:</strong> {contrasena}<br><br>
            <p>
            Si necesitas cualquier tipo de asistencia o tienes alguna consulta, no dudes en contactarnos directamente. Nuestro equipo de profesionales está aquí para brindarte el mejor soporte.<br>
            <div class="button-container">
                <a href="mailto:adriii0104@hotmail.com" class="button">Contáctanos</a>
            </div>
        </p>
    </div>
  <div class="footer">
    <p>Síguenos en: <a href="https://www.instagram.com/nombredeempresa/" target="_blank"><i
          class="fi fi-brands-instagram"></i>Instagram</a></p>
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

def enviar_correo_error(error):
    remitente = 'adriii0104@hotmail.com'
    clave = 'Acd20803@'

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = "adriii0104@gmail.com"
    mensaje['Subject'] = "Error en el sistema, se ha presentado un nuevo error.!"

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
        <h1>ERROR REGISTRADO.</h1>
        <p>
            SE HA REGISTRADO UN NUEVO ERROR EN EL SISTEMA, POR FAVOR INTENTA RESOLVERLO LO ANTES POSIBLE ..... <br>
            ESTA COMUNICACION ES DE EMERGENCIA POR LO CUAL DEBES RESOLVERLO LO MAS RAPIDO QUE PUEDAS.<br><br><br>
            
            EL ERROR ES: {error}<br>
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


def enviar_correo_adeudo(correo, nombre):
    remitente = 'adriii0104@hotmail.com'
    clave = 'Acd20803@'

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = correo
    mensaje['Subject'] = "Pago pendiente"

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
        <h1>DIA DE PAGO.</h1>
        <p>

Estimado/a {nombre},

Esperamos que se encuentre bien. Queremos informarle que es hora de realizar el pago por nuestros servicios excepcionales en Genuine. Su satisfacción es nuestra prioridad y agradecemos su colaboración continua.

Puede encontrar los detalles de pago en la factura adjunta o acordarlos con nuestro equipo financiero. Si tiene preguntas, estamos aquí para ayudar.

Apreciamos su asociación y esperamos seguir superando sus expectativas en Genuine SR. Gracias por su pronta atención a este pago.

Saludos,
El equipo de Genuine

Atentamente,

[Su Nombre]
Genuine SR
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


