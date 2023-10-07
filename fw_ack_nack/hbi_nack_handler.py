
'''
Function to handle any NACK received from the host 
Basically print out the specific NACK code received
'''

NACK_MESSAGE_CODE = 4
NACK_MAPPING = {
    0: "UNKNOWN ERROR",
    1: "INTERNAL FIRMWARE ERROR",
    2: "INVALID MESSAGE CRC",
    3: "UNKNOWN MESSAGE TYPE",
    4: "INVALID MESSAGE SIZE",
    5: "UNKNOWN COMMAND CODE",
    6: "UNKNOWN REQUEST CODE",
    7: "COMMAND VALUE OUT OF RANGE",
    8: "COMMAND EXECUTION FAILED",
    9: "SYSTEM BUSY"
}

def handle_nack(byte_stream) :
    if(byte_stream[2] > 0): #if we have some nack information in our payload
        if(byte_stream[3] in NACK_MAPPING): #index of message that contains nack type
            print("Received NACK message with the following reason:")
            print("     ==>", NACK_MAPPING[byte_stream[3]])
    else:
        print("Received NACK message with UNKNOWN REASON")
