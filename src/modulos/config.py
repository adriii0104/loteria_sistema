import requests
from modulos.dict import sesion_usuario, urls


def notification():
    url = 'http://127.0.0.1:5000/notifications'

    response = requests.get(url)

    if response.status_code == 200:
        respuesta = response.json()
        if respuesta['msj'] is None:
            return False
        else:
            return respuesta['msj']


def connection():
    status = 0
    try:
        for i, z in enumerate(urls):
            response = requests.get(z)
            if response.status_code == 200:
                status += 1
        if status == 7:
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
            return None
    else:
        return "error"


def register(
    nombre_banca_data, prefijo_data, dia_pago_data, monto_pago_data, tipo_software_data,
    pago_pale_data, pago_tripleta_data, puntos_primera_data, puntos_segunda_data, puntos_tercera_data,
    nombre_dueno_data, nombre_sucursal_data, telefono_principal_data, email_principal_data, usuario_data,
    password_data, id_banca_data, id_sucursal_data
):

    url = 'http://127.0.0.1:5000/user/register/auto'

    dataregister = {
        'nombre_banca': nombre_banca_data,
        'prefijo': prefijo_data,
        'dia_pago': dia_pago_data,
        'monto_pago': monto_pago_data,
        'tipo_software': tipo_software_data,
        'pago_pale': pago_pale_data,
        'pago_tripleta': pago_tripleta_data,
        'puntos_primera': puntos_primera_data,
        'puntos_segunda': puntos_segunda_data,
        'puntos_tercera': puntos_tercera_data,
        'nombre_dueno': nombre_dueno_data,
        'nombre_sucursal': nombre_sucursal_data,
        'telefono_principal': telefono_principal_data,
        'email_principal': email_principal_data,
        'usuario': usuario_data,
        'password': password_data,
        'id_banca': id_banca_data,
        'id_sucursal': id_sucursal_data
    }

    response = requests.post(url, json=dataregister, verify=False)

    if response.status_code == 200:
        respuesta = response.json()
        if respuesta['data'] == "Exist":
            return "Existent"

        elif respuesta['data']:
            return True

        else:
            return False
    else:
        return False


# benjon
def registrar_sucursal_data(id_banca):

    url = 'http://127.0.0.1:5000/registersucursal/post'

    data = {
        'id_banca': id_banca
    }

    response = requests.post(url, json=data, verify=False)

    if response.status_code == 200:
        respuesta = response.json()
        print(respuesta)


def count_numbers(id_banca, id_sucursal):

    url = 'http://127.0.0.1:5000/Hycbkxuhd/sykksxnns/ywfkxshkm/mbw'

    data = {
        'id_banca': id_banca, 'id_sucursal': id_sucursal
    }

    response = requests.post(url, json=data, verify=False)

    if response.status_code == 200:
        respuesta = response.json()

        if respuesta['response'] == True:
            response = respuesta['response']
            mas_jugado = respuesta['numero_mas_jugado']
            cantidad = respuesta['cantidad_mas_jugado']
            return response, mas_jugado, cantidad
        else:
            return False


def procesar_numeros(len_monto, selected_lotteries, total_jugado, amounts, chosen_numbers, selected, checkbox_selected, resultados):
    data = {
        'nombre_banca': sesion_usuario['nombre_banca'],
        'id_banca': sesion_usuario['id_banca'],
        'id_sucursal': sesion_usuario['id_sucursal'],
        'len_montos': len_monto,
        'selected_lotteries': selected_lotteries,
        'total_jugado': total_jugado,
        'amount': amounts,
        'chosen_numbers': chosen_numbers,
        'checkbox_selected_names': selected,
        'checkbox_selected_lotteries': checkbox_selected,
        'resultados': resultados
    }
    url = 'http://127.0.0.1:5000/data/numbers'

    response = requests.post(url, json=data, verify=False)

    if response.status_code == 200:
        respuesta = response.json()
        print(respuesta)

        if respuesta['response'] == True and respuesta['error'] == False:
            return True, respuesta['idticket']
        elif respuesta['error'] == True:
            return False, respuesta['response']
        else:
            return False, "Error"


def copy_config(id_ticket, id_banca, id_sucursal):
    # Concatena el parámetro id_banca a la URL

    url = f'http://127.0.0.1:5000/copy?id_ticket={id_ticket}&id_banca={id_banca}&id_sucursal={id_sucursal}'

    response = requests.get(url)

    if response.status_code == 200:
        respuesta = response.json()
        if respuesta['data'] is None:
            return False
        else:
            return respuesta['jugadas'], respuesta['montos']
    else:
        print(f"Error: {response.status_code}")


def cobrar_ticket(id_ticket):
    try:
        data = {
            'pago_punto': sesion_usuario.get('pago_punto'),
            'pago_tripleta': sesion_usuario.get('pago_tripleta'),
            'puntos_primera': sesion_usuario.get('puntos_primera'),
            'puntos_segunda': sesion_usuario.get('puntos_segunda'),
            'puntos_tercera': sesion_usuario.get('puntos_tercera'),
            'id_banca': sesion_usuario.get('id_banca'),
            'id_sucursal': sesion_usuario.get('id_sucursal'),
            'id_ticket': id_ticket
        }

        url = 'http://127.0.0.1:5000/verificar_ganadores/route/post'

        response = requests.post(url, json=data, verify=False)

        if response.status_code == 200:
            respuesta = response.json()
            if respuesta is not None:
                return respuesta
    except Exception as e:
        print(e)



def eliminar_ticket(id_ticket):
    try:
        url = 'http://127.0.0.1:5000/tickets'  # Reemplaza esto con la URL correcta para eliminar un ticket

        data = {
            'id_ticket': id_ticket, 'id_banca': sesion_usuario['id_banca'], 'id_sucursal': sesion_usuario['id_sucursal']
        }

        response = requests.post(url, json=data, verify=False)

        if response.status_code == 200:
            respuesta = response.json()
            return respuesta
        else:
            return False
    except Exception as e:
        return False