#include <Roomba.h>

Roomba roomba(&Serial1);
int p=0;

void iniciar(){
  roomba.driveDirect(-100,100);
  roomba.driveDirect(-100,100);
  delay(100);
  roomba.driveDirect(100,-100);
  delay(100);
}
void avanza(){
  roomba.driveDirect(50,50);
  roomba.driveDirect(50,50);  
}

void reversa(){
  roomba.driveDirect(-50,-50);
}

void giro_izq(){
  roomba.driveDirect(-30,30);
  delay(1000);
}

void giro_der(){
  roomba.driveDirect(30,-30);
  delay(1000);
}

void parar(){
  roomba.driveDirect(0,0);
  delay(500);
  Serial.println("9");
}

void met_while(){
  while(p==49){
    avanza();
    if(p==50){
      Serial.println("2");
      reversa();
      delay(1000);
    }

    if(p==52){
      Serial.println("4");
      giro_izq();
      //delay(10000);
      parar();
    }

    if(p==53){
      Serial.println("5");
      giro_der();
      //delay(10000);
      parar();
    }

    if(p==51){
      //Serial.println("3");
      parar();
      delay(1000);
    }
  }
}

void setup()
{

  Serial.begin(9600);
  Serial.println("Recibido");

  roomba.start();
  roomba.safeMode();

}

void loop(){
  //Serial.println("Recibido");
  
  if(Serial.available()>0){
    //iniciar();
    
    p=Serial.read();

    //met_while();
    //avanza();
    if(p == 51){
      Serial.println("1");
      avanza();
      
    }
    
    if(p==50){
      Serial.println("2");
      reversa();
      delay(1000);
    }

    if(p==52){
      Serial.println("4");
      giro_izq();
      delay(1000);
      parar();
    }

    if(p==53){
      Serial.println("5");
      giro_der();
      delay(1000);
      parar();
    }

    if(p==49){
      Serial.println("3");
      parar();
      delay(1000);
    }
  }
  delay(100);
}




