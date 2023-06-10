import requests

apiUrl = 'http://172.17.0.3:5000/api/presenca'
url_get = 'http://172.17.0.3:5000/api/usuario'
url_cadastro = 'http://172.17.0.3:5000/api/cadastro_usuario'

def envia_usuario(email,senha,url):
    json={'Email':email,'Senha':senha}
    response = requests.get(url, json=json)
    response.raise_for_status()
    return response.json()

def cadastra_usuario_api(email,nome,senha,url):
    json={'Email':email,'Senha':senha,'Nome':nome}
    response = requests.get(url, json=json)
    response.raise_for_status()
    return response.json()

def atualiza_alarme(id,status='Ativado',sensor='Ativado',buzzer='Ativado'):
    global apiUrl
    json={'Email':id,'status':status,'estado_sensor':sensor,'estado_buzzer':buzzer}
    response = requests.post(apiUrl, json=json)
    response.raise_for_status()
    return response.json()