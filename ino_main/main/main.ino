
//***************             Humidade solo               ***************

#define SECO 500 //VALOR MEDIDO COM O SOLO SECO 
#define MOLHADO 160 //VALOR MEDIDO COM O SOLO MOLHADO
#define VAZIO 20
#define CHEIO 9 

int TRIG = 7; // ********
int ECHO = 8; // ********

unsigned long start_t;
unsigned long end_t;
unsigned long delta_t;

double sampling_rate = 20;
double speed_of_sound = 349.10;
double max_distance = 4;
unsigned long max_delta_t = max_distance*pow(10,6)/speed_of_sound;

double distance;

int percSoloSeco = 0; //MENOR PERCENTUAL DO SOLO SECO 
int percSoloMolhado = 100; //MAIOR PERCENTUAL DO SOLO MOLHADO 

int percReservVazio = 0; //MENOR PERCENTUAL DO SOLO SECO 
int percReservCheio = 100; //MAIOR PERCENTUAL DO SOLO MOLHADO 
 

//    Configuração Sensor1
const int pinoSensor1 = A0; //PINO UTILIZADO PELO SENSOR
int valorLido1; //VARIÁVEL QUE ARMAZENA O PERCENTUAL DE UMIDADE DO SOLO

//    Configuração Sensor2
const int pinoSensor2 = A1; //PINO UTILIZADO PELO SENSOR
int valorLido2; //VARIÁVEL QUE ARMAZENA O PERCENTUAL DE UMIDADE DO SOLO



//***************                 SETUP                   ***************
void setup(){

 Serial.begin(9600); //INICIALIZA A SERIAL
 //Serial.println("Lendo a umidade do solo..."); //IMPRIME O TEXTO NO MONITOR SERIAL


 pinMode(TRIG, OUTPUT); //****
 pinMode(ECHO, INPUT);   //*****   
 digitalWrite(TRIG, LOW);  //*******

 delay(2000); //INTERVALO DE 2 SEGUNDOS
}

//***************                  LOOP                   ***************
void loop(){ 
//    Leitura do Serial
   if (Serial.available()) { //VERIFICA SE RECEBEU INFORMAÇÃO PELO SERIAL
    char lido = char(Serial.read()); //ARMAZENA O VALOR RECEBIDO PELO SERIAL

//    Leitura de informação do Sensor1
    if (lido == '1') {
       valorLido1 = constrain(analogRead(pinoSensor1),MOLHADO,SECO); //MANTÉM valorLido1 DENTRO DO INTERVALO (ENTRE MOLHADO E SECO)
       valorLido1 = map(valorLido1,MOLHADO,SECO,percSoloMolhado,percSoloSeco); //EXECUTA A FUNÇÃO "map" DE ACORDO COM OS PARÂMETROS PASSADOS
       //Serial.print("Umidade do solo: "); //IMPRIME O TEXTO NO MONITOR SERIAL
       Serial.println(valorLido1); //IMPRIME NO MONITOR SERIAL O PERCENTUAL DE UMIDADE DO SOLO
       //Serial.println("%"); //IMPRIME O CARACTERE NO MONITOR SERIAL
       delay(1000);  //INTERVALO DE 1 SEGUNDO
    }
   if (lido == '2') {
      valorLido2 = constrain(analogRead(pinoSensor2),MOLHADO,SECO); //MANTÉM valorLido1 DENTRO DO INTERVALO (ENTRE MOLHADO E SECO)
      valorLido2 = map(valorLido2,MOLHADO,SECO,percSoloMolhado,percSoloSeco); //EXECUTA A FUNÇÃO "map" DE ACORDO COM OS PARÂMETROS PASSADOS
      //Serial.print("Umidade do solo: "); //IMPRIME O TEXTO NO MONITOR SERIAL
      Serial.println(valorLido2); //IMPRIME NO MONITOR SERIAL O PERCENTUAL DE UMIDADE DO SOLO
      //Serial.println("%"); //IMPRIME O CARACTERE NO MONITOR SERIAL
      delay(1000);  //INTERVALO DE 1 SEGUNDO
    }
  
  if (lido == 'a') {
     digitalWrite(TRIG, HIGH);
     delayMicroseconds(10);
     digitalWrite(TRIG, LOW);
  
     while(digitalRead(ECHO) == LOW) start_t = micros();
  
     while(digitalRead(ECHO) == HIGH 
          && micros() - start_t < max_delta_t) end_t = micros();
  
     if(end_t - start_t < max_delta_t) {
      delta_t = end_t - start_t;
      distance = (0.5*delta_t*speed_of_sound)/pow(10,4);
    } else {
      distance = -1;
    }

    distance = map(distance,CHEIO,VAZIO,percReservCheio,percReservVazio); //EXECUTA A FUNÇÃO "map" DE ACORDO COM OS PARÂMETROS PASSADOS
  
    Serial.println(distance);
    delay(int(1000/sampling_rate));

  }
 }
}
