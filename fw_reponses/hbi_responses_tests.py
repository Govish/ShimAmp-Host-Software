import struct #have to use this to unpack float


RESPONSE_TEST_BYTE_CODE = 0
RESPONSE_TEST_UINT32_CODE = 1
RESPONSE_TEST_INT32_CODE = 2
RESPONSE_TEST_FLOAT_CODE = 3
RESPONSE_TEST_STRING_CODE = 4

def handle_test_byte(byte_stream):
    print("RECEIVED RESPONSE TO TEST BYTE REQUEST")
    print("     \\==> Response Contents: {contents}, or 0x{contents:02X}".format(contents = byte_stream[0]))

def handle_test_uint32(byte_stream):
    int_bytes = bytes(byte_stream)
    print("RECEIVED RESPONSE TO TEST UINT32 REQUEST")
    print("     \\==> Response Contents: {contents}, or 0x{contents:08X}".format(contents = int.from_bytes(int_bytes, "big"))) #convert bytes to big endian

def handle_test_int32(byte_stream):
    int_bytes = bytes(byte_stream)
    print("RECEIVED RESPONSE TO TEST INT32 REQUEST")
    print("     \\==> Response Contents: {contents}, or 0x{contents:08X}".format(contents = int.from_bytes(int_bytes, "big", signed=True))) #convert bytes to big endian

def handle_test_float(byte_stream):
    float_bytes = bytes(byte_stream)
    received_float = struct.unpack(">f", float_bytes)[0] #convert bytes to big endian float, returns as tuple
    print("RECEIVED RESPONSE TO TEST FLOAT REQUEST")
    print("     \\==> Response Contents: {contents}".format(contents = received_float))

def handle_test_string(byte_stream):
    string_bytes = bytes(byte_stream)
    print("RECEIVED RESPONSE TO TEST STRING REQUEST")
    print("     \\==> Response Contents: {contents}".format(contents = str(string_bytes, encoding="ASCII"))) 

RESPONSE_TEST_MAPPING = {
    RESPONSE_TEST_BYTE_CODE: handle_test_byte,
    RESPONSE_TEST_UINT32_CODE: handle_test_uint32,
    RESPONSE_TEST_INT32_CODE: handle_test_int32,
    RESPONSE_TEST_FLOAT_CODE: handle_test_float,
    RESPONSE_TEST_STRING_CODE: handle_test_string
}