import requests
from dict import sesion_usuario, urls


def connection():
    try:
        for i in urls:
            response = requests.get(i)
            if response.status_code == 200:
                return True
            else:
                return False
    except requests.exceptions.ConnectionError:
        return False




def login(email_data, password_data):
    url = 'http://127.0.0.1:5000/CS8QHsIdoOXUGTAHtZTZeg+YteqGd5qStna8r/UgWxQ'

    email = email_data.lower()
    password = password_data

    data = {'email': email, 'password': password}

    # Realiza una solicitud POST a la URL de la API
    response = requests.post(url, json=data, verify=False)

    if response.status_code == 200:
        respuesta = response.json()
        valido = respuesta['valid']
        if valido == "admin":
            log = "admin"
            return log
        elif valido == True:
            # Actualiza la sesión del usuario con información de la respuesta
            sesion_usuario['id_banca'] = respuesta['id_banca']
            sesion_usuario['id_sucursal'] = respuesta['id_sucursal']
            sesion_usuario['nombre_banca'] = respuesta['nombre_banca']
            sesion_usuario['pago_pale'] = respuesta['pago_pale']
            sesion_usuario['pago_tripleta'] = respuesta['pago_tripleta']
            sesion_usuario['puntos_primera'] = respuesta['puntos_primera']
            sesion_usuario['puntos_segunda'] = respuesta['puntos_segunda']
            sesion_usuario['puntos_tercera'] = respuesta['puntos_tercera']
            sesion_usuario['numero_principal'] = respuesta['numero_principal']
            return True
        elif valido == False:
            # Mensaje de error si el inicio de sesión no fue válido
            return False
        else:
            # Mensaje de error si la respuesta no es válida
            return False
    else:
        log = "error"
        return "error"


def register(nombre_banca_data, prefijo_data, dia_pago_data, monto_pago_data, tipo_software_data,
             pago_pale_data, pago_tripleta_data, puntos_primera_data, puntos_segunda_data, puntos_tercera_data,
             nombre_dueno_data, nombre_sucursal_data, telefono_principal_data, email_principal_data, usuario_data,
             password_data, id_banca_data, id_sucursal_data

             ):

    url = 'http://127.0.0.1:5000/user/register/auto'

    nombre_banca = nombre_banca_data
    prefijo = prefijo_data
    dia_pago = dia_pago_data
    monto_pago = monto_pago_data
    tipo_software = tipo_software_data
    pago_pale = pago_pale_data
    pago_tripleta = pago_tripleta_data
    puntos_primera = puntos_primera_data
    puntos_segunda = puntos_segunda_data
    puntos_tercera = puntos_tercera_data
    nombre_dueno = nombre_dueno_data
    nombre_sucursal = nombre_sucursal_data
    telefono_principal = telefono_principal_data
    email_principal = email_principal_data
    usuario = usuario_data
    password = password_data
    id_banca = id_banca_data
    id_sucursal = id_sucursal_data

    dataregister = {
        'banca': nombre_banca,
        'prefijo': prefijo,
        'dia_pago': dia_pago,
        'monto_pago': monto_pago,
        'tipo_software': tipo_software,
        'pago_pale': pago_pale,
        'pago_tripleta': pago_tripleta,
        'puntos_primera': puntos_primera,
        'puntos_segunda': puntos_segunda,
        'puntos_tercera': puntos_tercera,
        'nombre_dueno': nombre_dueno,
        'nombre_sucursal': nombre_sucursal,
        'telefono_principal': telefono_principal,
        'email_principal': email_principal,
        'usuario': usuario,
        'password': password,
        'id_banca': id_banca,
        'id_sucursal': id_sucursal
    }
    response = requests.post(url, json=dataregister, verify=False)

    if response.status_code == 200:
        respuesta = response.json()
        if respuesta['data']:
            return True
        else:
            return False
    else:
        return False
