import logging
import time
log = logging.getLogger(__name__)
# import json
from pyi2c import I2CBus
from pyi2c.utils import fjson
turn_on_led = [13,1,1,255,255]
turn_off_led = [13,1,0,255,255]
PWM_STATE = 2
ANALOG_READ = 3
OUTPUT = 1
def test_led(i2c_left, i2c_right):
    log.debug("LED test!")
    for i in range(2):
        i2c_left.writeSequence(turn_on_led)
        time.sleep(1)
        i2c_right.writeSequence(turn_on_led)
        time.sleep(1)

        i2c_left.writeSequence(turn_off_led)
        time.sleep(1)
        i2c_right.writeSequence(turn_off_led)
        time.sleep(1)

def test_motors(i2c_right, devices_config):
    
    for device in devices_config['devices']:
        component_name = device.get('components', {})[0].get('name', None)
        if device['type'] == 'arduino' and component_name == 'motor':
            sdevice = device
            log.debug("motor components: \n{}".format(fjson(sdevice)))
            for comp in sdevice['components']:
                if comp['name'] == 'motor' and comp['side'] == 'left':
                    left_motor = comp
                elif comp['name'] == 'motor' and comp['side'] == 'right':
                    right_motor = comp
            break
    log.debug("left motor:\n{}".format(fjson(left_motor)))
    log.debug("right motor:\n{}".format(fjson(right_motor)))

    # i2c_dev = I2CBus(0x15, bus_number=1)
    # 12c_dev.__enter__()

    # init_seq = [
    #         left_motor['pins']['direction'][0], OUTPUT, 0,
    #         left_motor['pins']['direction'][1], OUTPUT, 1,
    #         left_motor['pins']['enable'], PWM_STATE, 1,
    #         right_motor['pins']['direction'][0], OUTPUT, 0,
    #         right_motor['pins']['direction'][1], OUTPUT, 1,
    #         right_motor['pins']['enable'], PWM_STATE, 1,
    #         255,255
    # ]
    def motors_forward_speed(s):
        return [
            left_motor['pins']['direction'][0], OUTPUT, 0,
            left_motor['pins']['direction'][1], OUTPUT, 1,
            left_motor['pins']['enable'], PWM_STATE, s,
            right_motor['pins']['direction'][0], OUTPUT, 0,
            right_motor['pins']['direction'][1], OUTPUT, 1,
            right_motor['pins']['enable'], PWM_STATE, s,
            255,255
        ]
    def motors_backward_speed(s):
        return [
            left_motor['pins']['direction'][0], OUTPUT, 1,
            left_motor['pins']['direction'][1], OUTPUT, 0,
            left_motor['pins']['enable'], PWM_STATE, s,
            right_motor['pins']['direction'][0], OUTPUT, 1,
            right_motor['pins']['direction'][1], OUTPUT, 0,
            right_motor['pins']['enable'], PWM_STATE, s,
            255,255
        ]
    def motors_left_turn_speed(s):
        return [
            left_motor['pins']['direction'][0], OUTPUT, 1,
            left_motor['pins']['direction'][1], OUTPUT, 0,
            left_motor['pins']['enable'], PWM_STATE, s,
            right_motor['pins']['direction'][0], OUTPUT, 0,
            right_motor['pins']['direction'][1], OUTPUT, 1,
            right_motor['pins']['enable'], PWM_STATE, s,
            255,255
        ]
    def motors_right_turn_speed(s):
        return [
            left_motor['pins']['direction'][0], OUTPUT, 0,
            left_motor['pins']['direction'][1], OUTPUT, 1,
            left_motor['pins']['enable'], PWM_STATE, s,
            right_motor['pins']['direction'][0], OUTPUT, 1,
            right_motor['pins']['direction'][1], OUTPUT, 0,
            right_motor['pins']['enable'], PWM_STATE, s,
            255,255
        ]
    stop_seq = [
            left_motor['pins']['direction'][0], OUTPUT, 0,
            left_motor['pins']['direction'][1], OUTPUT, 0,
            left_motor['pins']['enable'], PWM_STATE, 0,
            right_motor['pins']['direction'][0], OUTPUT, 0,
            right_motor['pins']['direction'][1], OUTPUT, 0,
            right_motor['pins']['enable'], PWM_STATE, 0,
            255,255
    ]
    i2c_right.writeSequence(motors_forward_speed(0))
    for i in range(20, 255, 20):
        log.debug("motors speed: {}".format(i))
        i2c_right.writeSequence(motors_forward_speed(i))
        time.sleep(1)
    i2c_right.writeSequence(motors_backward_speed(255))
    time.sleep(1)
    i2c_right.writeSequence(motors_left_turn_speed(255))
    time.sleep(1)
    i2c_right.writeSequence(motors_right_turn_speed(255))
    time.sleep(1)
    i2c_right.writeSequence(stop_seq)
    
    # 12c_dev.__exit__()
        
    
    