import serial
from api import *

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
        if float(distancia)<=60:
            api_alarme(url_alarme, usuario)
    else:
        valor = 0
    print(valor)
    ser.write(str(valor).encode())

ser.close()