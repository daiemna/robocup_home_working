import pytest
from pyi2c import I2CBus
from pyi2c import utils

@pytest.fixture(scope="module")
def i2c_left():
    bus = I2CBus(0x15, bus_number=1)
    # bus.ddelay = 0.05
    bus.__enter__()
    return bus

@pytest.fixture(scope="module")
def i2c_right():
    bus = I2CBus(0x05, bus_number=1)
    bus.__enter__()
    return bus

@pytest.fixture(scope="module")
def devices_config():
    return utils.load_yaml('config/pin_config.yml')