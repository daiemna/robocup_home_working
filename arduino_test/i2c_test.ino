#include <Wire.h>

#define SLAVE_ADDRESS 0x15
uint8_t memory[255];
uint8_t pointer=0;

void setup(){
    pinMode(13, OUTPUT);
    Serial.begin(9600); // start serial for output
    Wire.setClock(1000000);

    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);

    // define callbacks for i2c communication
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    Serial.println("Ready !");
}

void loop(){
    delay(100);
}

// callback for received data
void receiveData(int byteCount){
    if(Wire.available()){
        pointer = Wire.read();
        Serial.print("received address: ");
        Serial.println(pointer);
    }
    if(Wire.available()){
        memory[pointer] = Wire.read();
        Serial.print("received data: ");
        Serial.println(memory[pointer]);
    }
}

// callback for sending data
void sendData(){
    Serial.print("sending data at ");
    Serial.print(pointer);
    Serial.print(" : ");
    Serial.println(memory[pointer]);
    Wire.write((byte)memory[pointer]);
}