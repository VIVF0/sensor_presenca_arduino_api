# Sensor de Presença Arduino API
Link Wokwi: https://wokwi.com/projects/363547799830028289 

A Sensor de Presença Arduino API é um projeto que consiste em uma API desenvolvida em Python com Flask. A API recebe uma solicitação POST contendo um email e senha do usuário e retorna o estado do alarme do usuário. Esse estado é então enviado para uma placa Arduino Uno usando a biblioteca pySerial. Com base no estado do alarme, a placa Arduino executa diferentes ações, como acionar um buzzer e controlar um LED.

### Funcionamento
A API recebe uma solicitação POST contendo o email e senha do usuário.

A API verifica as credenciais do usuário e consulta o estado do alarme no banco de dados MongoDB.

Se o alarme estiver ativo, a API envia um valor de controle (1) para a placa Arduino Uno através da porta serial para ativar o sensor de presença.

A placa Arduino Uno possui um sensor sonar que mede a distância de objetos em frente a ele.

Se a distância medida for igual ou inferior a 60 cm, o buzzer é acionado e o LED verde é aceso.

Caso contrário, se a distância for maior que 60 cm, o LED verde permanece aceso.

Se o alarme estiver desligado no banco de dados, a API envia um valor de controle (2) para a placa Arduino Uno para manter apenas o LED verde aceso.

### Pré-requisitos
Antes de executar o projeto, certifique-se de ter os seguintes pré-requisitos instalados em sua máquina:

Python 3.10.11: [Download Python](https://www.python.org/downloads/release/python-31011/)

MongoDB: Instale e configure o MongoDB em seu ambiente. Certifique-se de ter as credenciais de acesso corretas.

### Como Usar
Clone o repositório para sua máquina local:
```
git clone https://github.com/VIVF0/sensor_presenca_arduino_api.git
```
Navegue até o diretório do projeto:
```
cd sensor_presenca_arduino_api
```
Instale as dependências do projeto executando o seguinte comando:
```
pip install -r requirements.txt
```

No arquivo API/app.py, atualize as informações de conexão com o banco de dados MongoDB, como o nome do banco, host, porta e credenciais de acesso.

Conecte a placa Arduino Uno ao seu computador usando um cabo USB.

### Carregue o programa hcsr04_serial_buzzer_led/hcsr04_serial_buzzer_led.ino para a placa Arduino Uno usando a IDE do Arduino.

#### Execute o arquivo app.py para iniciar a API:
```
python API/app.py
```
#### Execute o arquivo main.py para se comunicar com a placa (Lembre de verificar a porta que a placa está sendo reconhecida pelo sistema):
```
python arduino_communication/main.py
```

#### Licença
Este projeto está licenciado sob a licença MIT.

Agora você pode usar a Sensor de Presença Arduino API para controlar o alarme e executar ações com base na presença detectada pelo sensor sonar da placa Arduino Uno.
