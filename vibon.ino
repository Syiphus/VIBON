// Vibracoes e Ondas 
// Trabalho Experimental - SONAR
// Parte 1. Calibracao do SONAR
// Codigo base (calibration.ino)
// Carlos Vinhais, Out 2021

const int TRIG_PIN = 5;
const int ECHO_PIN = 16;
int val;
const int tempPin = A0;
unsigned long t_eco;
const int N = 10;

String inputString = "";          // user input: distance (mm)
bool stringComplete = false;      // whether the string is complete

void setup() {  
  Serial.begin( 9600 );
  pinMode( TRIG_PIN, OUTPUT );
  pinMode (ECHO_PIN, INPUT );
  inputString.reserve(10); 
}

void loop() {
  if (stringComplete) {

    /* input distance, d (mm) */
    float dist_mm = inputString.toFloat();

    /* mean echo time, time_avg (us) */
    float time_avg = 0.0;
    
    for ( int n = 0; n < N; n++) {      // N measurements
      /* ultrasonic pulse */
      digitalWrite( TRIG_PIN, HIGH );     // SONAR trigger
      delayMicroseconds( 10 );            // wait 10 us
      digitalWrite( TRIG_PIN, LOW );      // end of pulse
      t_eco = pulseIn( ECHO_PIN, HIGH );  // echo time, us
      
      time_avg += float(t_eco);           // accumulate...
      delay(50);                          // wait 50 ms ?
    }
    
    time_avg /= float(N);                   // mean echo time, us
    time_avg /= 1000;                     // mean echo time, ms

    /* send data to serial port */
    Serial.print( dist_mm );
    Serial.print( " " );
    Serial.println( time_avg );

    /* reset user input */
    inputString = "";                       // clear input string
    stringComplete = false;                 // set flag to flase
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    }
    //Leitura da temperatura
    else {
      if(inChar == 'T'){
        val = analogRead(tempPin);
        float mv = ( val/1024.0)*3300;
        float cel = mv/10;
        Serial.print('T');
        Serial.print( " " );
        Serial.print(cel);
      }
      inputString += inChar;
    }
  }
}
