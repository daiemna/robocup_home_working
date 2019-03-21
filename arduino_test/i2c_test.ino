#include <Wire.h>

#define SLAVE_ADDRESS 0x15
#define PWM_STATE 2
#define ANALOG_READ 3

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
    for(int i=1; i <= 85; ++i){
        uint8_t pin = memory[3 * (i-1)], 
                state = memory[3 * (i-1) + 1], 
                value = memory[3 * (i-1) + 2];
        if(pin == 255 && state == 255){
            break;
        }
        if(state == INPUT){
            pinMode(pin, INPUT);
            memory[3 * (i-1) + 2] = digitalRead(pin);
        }else if(state == OUTPUT){
            pinMode(pin, OUTPUT);
            digitalWrite(pin, value == HIGH);
        }else if(state == PWM_STATE){
            pinMode(pin, OUTPUT);
            analogWrite(pin, value);
        }else if(state == ANALOG_READ){
            pinMode(pin, INPUT);
            memory[3 * (i-1) + 2] = analogRead(pin);
        }
    }
}

// callback for received data
void receiveData(int byteCount){
    if(Wire.available()){
        pointer = Wire.read();
        // Serial.print("received address: ");
        // Serial.println(pointer);
    }
    if(Wire.available()){
        memory[pointer] = Wire.read();
        // Serial.print("received data: ");
        // Serial.println(memory[pointer]);
    }
}

// callback for sending data
void sendData(){
    // Serial.print("sending data at ");
    // Serial.print(pointer);
    // Serial.print(" : ");
    // Serial.println(memory[pointer]);
    Wire.write((byte)memory[pointer]);
}