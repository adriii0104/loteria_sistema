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
            response=respuesta['response']
            mas_jugado=respuesta['numero_mas_jugado']
            cantidad=respuesta['cantidad_mas_jugado']
            return response, mas_jugado, cantidad
        else:
            return False
        

def procesar_numeros(len_monto, selected_lotteries, total_jugado, amounts, chosen_numbers, selected, checkbox_selected):
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
        'checkbox_selected_lotteries': checkbox_selected 

    }
    url = 'http://127.0.0.1:5000/data/numbers'

    response = requests.post(url, json=data, verify=False)

    if response.status_code == 200:
        respuesta = response.json()
        print(respuesta['error'])

        if respuesta['response'] == True and respuesta['error'] == False:
            return True
        elif respuesta['error'] == True:
            return respuesta['response']
        else:
            return False
        


