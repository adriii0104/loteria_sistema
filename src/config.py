import requests

url = 'http://127.0.0.1:5000/CS8QHsIdoOXUGTAHtZTZeg+YteqGd5qStna8r/UgWxQ'


email = input("Inserte su email ")

print("\n")

password = input("Password ")


data = {'email': email, 'password': password}



response = requests.post(url, json=data, verify=False)

if response.status_code == 200:
    respuesta = response.json()
    valido = respuesta['valid']
    if valido == True:
        print(respuesta['message'])
    elif valido == False:
        print(respuesta['message'])
    else:
        print(respuesta['message'])
    


    