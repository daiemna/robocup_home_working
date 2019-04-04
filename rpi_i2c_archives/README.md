![travi-ci](https://travis-ci.com/daiemna/roboz.svg?branch=master)

## for python=3.5 env
* for raspbarry pi libs `conda config --add channels rpi`

## test for i2c drivers.
* test assumes that arduino nano is connected to raspberry pi by serial.
* check `upload_test_code.sh` before running the test.
* then `make test`


## install blutooth
* pair remote by `bluetoothctl`
* for evdev :
  * `sudo apt install -y libbluetooth-dev libglib2.0-dev libreadline-dev`
  * `pip install evdev bluepy`