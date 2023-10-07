
HOST_REQUEST = 0x02

REQUEST_TEST_BYTE_CODE = 0
REQUEST_TEST_UINT32_CODE = 1
REQUEST_TEST_INT32_CODE = 2
REQUEST_TEST_FLOAT_CODE = 3
REQUEST_TEST_STRING_CODE = 4

def send_request_test_byte():
    #don't include SOF and EOF characters here--leave that for COBS
    #payload only contains register that we wanna request from
    print("     > Requesting test byte")
    message = [HOST_REQUEST, 1, REQUEST_TEST_BYTE_CODE]
    return message

def send_request_test_uint32():
    print("     > Requesting test uint32")
    message = [HOST_REQUEST, 1, REQUEST_TEST_UINT32_CODE]
    return message

def send_request_test_int32():
    print("     > Requesting test int32")
    message = [HOST_REQUEST, 1, REQUEST_TEST_INT32_CODE]
    return message

def send_request_test_float():
    print("     > Requesting test float")
    message = [HOST_REQUEST, 1, REQUEST_TEST_FLOAT_CODE]
    return message

def send_request_test_string():
    print("     > Requesting test string")
    message = [HOST_REQUEST, 1, REQUEST_TEST_STRING_CODE]
    return message

#have a dictionary that maps a command string to a function
#said function will transmit an appropriate amount of bytes over the serial port
REQUESTS_TESTS = {
    'REQUEST_TEST_BYTE' : send_request_test_byte,
    'REQUEST_TEST_UINT32' : send_request_test_uint32,
    'REQUEST_TEST_INT32' : send_request_test_int32,
    'REQUEST_TEST_FLOAT' : send_request_test_float,
    'REQUEST_TEST_STRING' : send_request_test_string,
}