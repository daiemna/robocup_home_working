#!/bin/bash

~/arduino-1.8.8/arduino \
--upload arduino_test/i2c_test.ino \
--port /dev/ttyUSB0 \
--board arduino:avr:nano:cpu=atmega328old