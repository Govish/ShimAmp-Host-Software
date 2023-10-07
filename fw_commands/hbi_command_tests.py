import struct #have to use this to pack float

HOST_COMMAND = 0x01

COMMAND_TEST_BYTE_CODE = 0
COMMAND_TEST_UINT32_CODE = 1
COMMAND_TEST_INT32_CODE = 2
COMMAND_TEST_FLOAT_CODE = 3
COMMAND_TEST_STRING_CODE = 4

def send_command_test_byte():
    #don't include SOF and EOF characters here--leave that for COBS
    #payload only contains register that we wanna request from
    print("     > Commanding test byte")
    message = [HOST_COMMAND, 2, COMMAND_TEST_BYTE_CODE, 0xAA]
    return message

def send_command_test_uint32():
    print("     > Commanding test uint32")
    
    uint_bytes = int.to_bytes(0xFFABCD00, length=4, byteorder='big')
    message = [HOST_COMMAND, 5, COMMAND_TEST_UINT32_CODE]
    message += list(uint_bytes)
    return message

def send_command_test_int32():
    print("     > Commanding test int32")
    
    int_bytes = int.to_bytes(-31415, length=4, byteorder='big', signed=True)
    message = [HOST_COMMAND, 5, COMMAND_TEST_INT32_CODE]
    message += list(int_bytes)
    return message

def send_command_test_float():
    print("     > Commanding test float")
    
    float_bytes = struct.pack(">f", 123.25)
    message = [HOST_COMMAND, 5, COMMAND_TEST_FLOAT_CODE]
    message += list(float_bytes)
    return message

def send_command_test_string():
    print("     > Commanding test string")

    #pop in the correct payload length after adding the string
    message = [HOST_COMMAND, 0, COMMAND_TEST_STRING_CODE]
    message += list(bytes("Congrats! You decoded this message correctly!\r\n", "ASCII"))
    message[1] = len(message) - 2
    return message

#have a dictionary that maps a command string to a function
#said function will transmit an appropriate amount of bytes over the serial port
COMMANDS_TESTS = {
    'COMMAND_TEST_BYTE' : send_command_test_byte,
    'COMMAND_TEST_UINT32' : send_command_test_uint32,
    'COMMAND_TEST_INT32' : send_command_test_int32,
    'COMMAND_TEST_FLOAT' : send_command_test_float,
    'COMMAND_TEST_STRING' : send_command_test_string,
}