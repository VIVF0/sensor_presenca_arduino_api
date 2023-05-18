//Componentes Eletricos:
const int trigPin = 8;
const int echoPin = 7;
const int buzzer = 10;
const int channel = 0;
const int resolution = 8;
const int led_verde = 6;
const int led_vermelho = 9;

//Variaveis global:
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701
long duration;
float distanceCm;
int valor_recebido=1;

//Funcoes:
void Distance();
void alarme();

void setup() {
  Serial.begin(115200);
  //ledcSetup(channel, 5000, resolution);
  //ledcAttachPin(buzzer, channel);
  pinMode(buzzer,OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(led_vermelho, OUTPUT);
  pinMode(led_verde, OUTPUT);
}

void loop() {
  Distance();
  Serial.println("Distancia: " + String(distanceCm));
  //Puxando Serial
   if(Serial.available() > 0)
  {
    valor_recebido = Serial.read();
  }

  //Caso alarme estiver ligado:
  if(valor_recebido == '1' || valor_recebido == '2'){
    if (distanceCm <= 60) {
        //ledcWriteTone(channel, 1000);
        tone(buzzer,5000);
        digitalWrite(led_vermelho, HIGH);
        digitalWrite(led_verde, LOW);
    }
    if(valor_recebido == '2'){
        alarme();
        valor_recebido = '1';
     }
  //Se o Alarme nao estiver ligado:
  }else{
    alarme();
  } 
  delay(1000);
}

void alarme(){
  //ledcWriteTone(channel, 0);
  noTone(buzzer);
  digitalWrite(led_vermelho, LOW);
  digitalWrite(led_verde, HIGH);
}

void Distance() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);

    distanceCm = duration * SOUND_SPEED / 2;
}
