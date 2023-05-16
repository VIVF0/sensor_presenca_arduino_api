#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

//Componentes Eletricos:
const int trigPin = 2;
const int echoPin = 15;
const int buzzer = 13;
const int channel = 0;
const int resolution = 8;
const int led_verde = 12;
const int led_vermelho = 4;
float distanceCm;
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701
long duration;

//Wifi:
const char* ssid=""; //Nome da Rede
const char* password = ""; //Senha da Rede
HTTPClient http;

//URLs API:
const char* apiUrl = ""; //URL da API para envio da Distancia
const char* url_get = ""; //URL da API para Status do Alarme

//Usuario:
const char* usuario_nome = ""; //Email do Usuario
const char* usuario_senha = ""; //Senha do Usuario sem Criptografia

//Envia para API a distancia quando for detectado presenca
void postToAPI();
//Calcula Distancia:
float Distance();
//Verifica se o alarme foi ligado pelo usuario consultando a API
bool checkStatusActivated();
//Conecta no WIFI:
void conecta_wifi();

void setup() {
  Serial.begin(115200);
  ledcSetup(channel, 5000, resolution);
  ledcAttachPin(buzzer, channel);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(led_vermelho, OUTPUT);
  pinMode(led_verde, OUTPUT);
  conecta_wifi();
}

void loop() {
  Serial.println(Distance());
    if (checkStatusActivated()) {
      if (Distance() <= 60) {
        postToAPI();
        ledcWriteTone(channel, 1000);
        digitalWrite(led_vermelho, HIGH);
        digitalWrite(led_verde, LOW);
      } else {
        ledcWriteTone(channel, 0);
        digitalWrite(led_vermelho, LOW);
        digitalWrite(led_verde, HIGH);
      }
    } else {
      digitalWrite(led_vermelho, LOW);
      digitalWrite(led_verde, HIGH);
    }
  delay(1000);
}

void conecta_wifi(){
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
}

void postToAPI() {
    http.begin(apiUrl);

    http.addHeader("Content-Type", "application/json");

    const size_t capacity = JSON_OBJECT_SIZE(3);
    DynamicJsonDocument jsonDoc(capacity);
    jsonDoc["distancia"] = Distance();
    jsonDoc["usuario"] = usuario_nome;
    jsonDoc["senha"] = usuario_senha;
    String jsonString;
    serializeJson(jsonDoc, jsonString);

    int httpResponseCode = http.POST(jsonString);

    if (httpResponseCode > 0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);

        String response = http.getString();
        Serial.println(response);
    } else {
        Serial.println("Error on HTTP request");
    }
    http.end();
}

float Distance() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);

    distanceCm = duration * SOUND_SPEED / 2;
    return distanceCm;
}

bool checkStatusActivated() {
    http.begin(url_get);

    // Create JSON payload with username and password
    const size_t capacity = JSON_OBJECT_SIZE(2);
    StaticJsonDocument<capacity> jsonDoc;
    jsonDoc["usuario"] = usuario_nome;
    jsonDoc["senha"] = usuario_senha;

    String jsonString;
    serializeJson(jsonDoc, jsonString);

    // Set the Content-Type header to application/json
    http.addHeader("Content-Type", "application/json");

    // Send the POST request with the JSON payload
    int httpResponseCode = http.POST(jsonString);

    if (httpResponseCode == HTTP_CODE_OK) {
        String response = http.getString();

        // Parse JSON response
        const size_t capacity = JSON_OBJECT_SIZE(1) + 20;
        StaticJsonDocument<capacity> jsonDoc;
        deserializeJson(jsonDoc, response);

        // Check the value of the "status" key
        const char* statusValue = jsonDoc["status"];
        http.end();

        if (String(statusValue) == "ativado") {
            return true;
        } else {
            return false;
        }
    } else {
        http.end();
        return false;
    }
}
