import logging

log = logging.getLogger(__name__)

sent_number = 110
sent_left = 121
sent_right = 1
sent_string = 'Hello!'
loc=33
write_sequence = [13,0,1,13,0,0]

def test_send_number(i2c_left):
    log.debug("Testing send number")
    assert i2c_left.writeNumber(sent_number, at=loc) == None

def test_read_number(i2c_left):
    log.debug("Testing read number")
    i2c_left.writeNumber(sent_left, at=loc)
    number1 = i2c_left.readNumber(at=loc)
    assert sent_left == number1

def test_read_write_seq(i2c_left):
    log.debug("Testing read/write sequence")
    s_seq = i2c_left.writeSequence(write_sequence)
    assert all(map(lambda x: x == None, s_seq))

    read_seq = i2c_left.readSequence(len(write_sequence))
    assert all(map(lambda x: x[0] == x[1], zip(read_seq, write_sequence)))

def test_write_string(i2c_left, caplog):
    log.debug("Testing write string")
    string = i2c_left.writeString(sent_string)
    log.debug("char res : {}".format(string))
    assert all(map(lambda x: x == None, string))

def test_read_string(i2c_left):
    log.debug("Testing read string")
    i2c_left.writeString(sent_string)
    recived_string = i2c_left.readString()
    assert sent_string == recived_string
