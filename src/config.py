import requests
from dict import sesion_usuario



def login(email_data, password_data):
    url = 'http://127.0.0.1:5000/CS8QHsIdoOXUGTAHtZTZeg+YteqGd5qStna8r/UgWxQ'
    
    
    email = email_data
    
    
    
    password = password_data
    
    
    data = {'email': email, 'password': password}
    
    
    
    response = requests.post(url, json=data, verify=False)
    
    if response.status_code == 200:
        respuesta = response.json()
        valido = respuesta['valid']
        if valido == True:
            sesion_usuario['id_banca'] = respuesta['id_banca']
            sesion_usuario['id_sucursal'] = respuesta['id_sucursal']
            




            
        elif valido == False:
            print(respuesta['message'])
        else:
            print(respuesta['message'])
    


def register():
    url = 'http://127.0.0.1:5000/CS8QHsIdoOXUGTAHtZTZeg+YteqGd5qStna8r/UgWxQ'

    nombre_banca = nombre_banca_data
    persona_a_cargo = persona_a_cargo_data
    numero_contacto = numero_contacto_data_data
    numero_secundario = numero_secundario_data
    email_contacto = email_contacto_data
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
    nm = nm_data
    
    dataregister = {'banca_register': nombre_banca_data, 
                    'persona_a_cargo_register': persona_a_cargo_data,
                    'numero_contacto_register': numero_contacto_data,
                    'numero_secundario_register': numero_secundario_data,
                    'email_contacto_register': email_contacto_data,
                    'prefijo_register': prefijo_data,
                    'dia_pago_register': dia_pago_data,
                    'monto_pago_register': monto_pago_data,
                    'tipo_software_register': tipo_software_data,
                    'pago_pale_register': pago_pale_data,
                    'pago_tripleta_register': pago_tripleta_data,
                    'puntos_primera_register': puntos_primera_register,
                    'puntos_segunda_register': puntos_segunda_data,
                    'puntos_tercera_register': puntos_tercera_data,
                    'nombre_dueno_register': nombre_dueno_data,
                    'nombre_sucursal_register': nombre_sucursal_data,
                    'telefono_principal_register': telefono_principal_data,
                    'email_principal_register': email_principal_data,
                    'usuario_register': usuario_data,
                    'password_register': password_data,
                    'nm_register': nm_data,
                    'persona_a_cargo_register': persona_a_cargo_data,
    
    
    
    
    
    
    
    }