from smbus2 import SMBusWrapper
import time
import logging

log = logging.getLogger(__name__)

class I2CBus(SMBusWrapper):
    EOS = ord('\0')
    baud = 100000.0

    def __init__(self, address, bus_number=1, auto_cleanup=True, force=False):
        SMBusWrapper.__init__(self, bus_number, auto_cleanup, force)
        self.bus = None
        self.address = address
        self.ddelay = 0.05
        log.debug("delay after r/w : {}".format(self.ddelay))
    
    def writeNumber(self, value, at=0):
        if self.bus is None:
            self.__enter__();
        try:
            ret = self.bus.write_byte_data(self.address, at, value)
            time.sleep(self.ddelay)
        except OSError as e:
            log.error("Write error: {}".format(e))
            ret = -1
        return ret

    def readNumber(self, at=0):
        if self.bus is None:
            self.__enter__();
        try:
            # self.bus.write_byte(self.address, at)
            ret = self.bus.read_byte_data(self.address, at)
            time.sleep(self.ddelay)
        except OSError as e:
            log.error("Read error: {}".format(e))
            ret = -1
        return ret
    
    def writeSequence(self, seq):
        return [self.writeNumber(value, i) for i, value in enumerate(seq)]

    def readSequence(self, length):
        return [self.readNumber(at=i) for i in range(length)]

    def writeString(self, string):
        # i = 0
        status = [self.writeNumber(ord(value), i) for i, value in enumerate(string)]
        self.writeNumber(ord('\0'), len(string))
        return status
    
    def readString(self):
        string = ''
        i = 0
        b = self.readNumber(i)
        log.debug("char {} : {}".format(i, b))
        while not b == I2CBus.EOS:
            string += chr(b)
            i += 1
            b = self.readNumber(i)
            log.debug("char {} : {}".format(i, b))
        return string

    def __repr__(self):
        return "SMBUS : {}, address : {}".format(self.bus_number, self.address)