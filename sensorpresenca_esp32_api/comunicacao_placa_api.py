import serial
import requests
import datetime
import time
import toml
with open('config.toml', 'r') as file:
    config = toml.load(file)
apiUrl = config['API_PADRAO']
url_get = config['API_GET_STATUS']
url_alarme = config['API_ALARME']

usuario = {
    "Email": config['USUARIO'],
    "Senha": config['SENHA']
}

def enviar_api(url, usuario, distancia):
    try:
        json_data = {"usuario": usuario, 'Distancia': distancia}
        response = requests.post(url, json=json_data)
        response.raise_for_status()
        return response.json()
    except:
        return False

def get_api(url, usuario):
    try:
        response = requests.get(url, json=usuario)
        response.raise_for_status()
        return response.json()
    except:
        return False

def api_alarme(url, usuario):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    json_data = {'usuario': usuario, 'Sensor': 'ativo', 'Momento': current_time}
    requests.post(url, json=json_data)

ser = serial.Serial('/dev/ttyUSB0', 115200)

valor = 0

while True:
    data = ser.readline().decode().strip()
    distancia_index = data.find('Distancia: ')
    distancia = data[distancia_index + 11:]
    print("Distancia:", distancia)
    #response = enviar_api(apiUrl, usuario, distancia)
    status = get_api(url_get, usuario)
    if status != False:
        if status['Status'] == 'Ativado':
            valor = 1
            if status['Sensor'] != 'Ativado':
                valor = 2
        else:
            valor = 0
        #if float(distancia)<=60:
        #    api_alarme(url_alarme, usuario)
    else:
        valor = 0
    print(valor)
    ser.write(str(valor).encode())

ser.close()