
'''
Function to handle any ACK received from the host 
honestly putting in its own file for code cleanliness--basically just this simple single function
'''

ACK_MESSAGE_CODE = 5

#that's all that we need to do for an ACK handler
def handle_ack(byte_stream) :
    print("Device ACKNOWLEDGED previously sent command (command code {code})".format(code = byte_stream[3]))