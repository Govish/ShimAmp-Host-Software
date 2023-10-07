#python library utilities
import serial
import serial.tools.list_ports
import sys #for exit()

#comms and message encoding utilitites
import hbi_crc
import hbi_cobs

#command and request generators
import fw_requests.hbi_requests_tests as hbi_requests_tests
import fw_commands.hbi_command_tests as hbi_commands_tests
import fw_requests.hbi_requests_stage as hbi_request_stage
import fw_commands.hbi_command_stage as hbi_commands_stage

#firmware message handlers
import fw_ack_nack.hbi_nack_handler as hbi_nack_handler
import fw_ack_nack.hbi_command_ack_handler as hbi_ack_handler
import fw_reponses.hbi_response_handler as hbi_response_handler

# ============================================ STARTUP UTILITIES ==========================================
def serial_connect():
    print("Available Serial Ports:")
    comports = serial.tools.list_ports.comports()
    for i in range(len(comports)):
        print(" [{index}]: {comname}".format(index = i, comname = comports[i].device))
    
    print("Connect to a port by typing its index:")
    valid_port = False
    while(not valid_port):
        try:
            serial_index = int(input(">>>"))
            if(serial_index < 0) or (serial_index >= len(comports)):
                raise IndexError
            else:
                #try to connect to the port the user provided 
                #connect with 115200 baud, 8N1, 5 second receive timeout
                comms = serial.Serial(comports[serial_index].device, baudrate=115200, timeout=5)              
        except:
            print("Something went wrong trying to connect to that port")
        else:
            valid_port = True
    
    print("########## Successfully connected to {port} at 115200 Baud ##########".format(port = comms.name))
    return comms

def get_endpoint_id():
    print("Enter the ID of the endpoint (0-255):")
    valid_id = False
    while(not valid_id):
        try:
            ep_id = int(input(">>>"))
            if(ep_id < 0) or (ep_id >= 256):
                raise IndexError            
        except:
            print("Invalid endpoint ID")
        else:
            valid_id = True
    
    print("########## Communicating with device at address {id} ##########".format(id = ep_id))
    return ep_id

#=================================================== MAIN ACTION LOOP ================================================

def action_loop():
    valid_action = False
    while(not valid_action):
        #prompt the user for input
        print("Enter [Desired Action Code] | 'lc' to list command codes | 'lr' to list request codes | 'exit' to close")
        action = input(">>>")
        
        if(action in actions): #valid command we can execute
            print("\\==> EXECUTING VALID COMMAND")
            return actions[action] #return the function that the user wants to run
        
        else: #invalid command
            print("     \\--> Invalid action code, try again")

#==================================== HELP AND UTILITY COMMANDS =================================
#maintain this function signature, so we can call all functions this way
def list_commands():
    print("Allowable command keys:")
    for command_key in commands:
        print(" >", command_key)

    #empty message to send to the firmware 
    return []

def list_request():
    print("Allowable request keys:")
    for request_key in requests:
        print(" >", request_key)

    #empty message to send to the firmware 
    return []

def exit_app():
    sys.exit("### Host program terminated through user action ###")

    #empty message to send to the firmware  (though should never get here)
    return []

#==================================== MESSAGE ENCODING AND DISPATCH =================================
def pack_and_send_message(crc_calc, serial_comms, bytes_sequence):
    print("Sending message to ID {id}".format(id = bytes_sequence[0]))

    crc_val = hbi_crc.append_crc(crc_calc, bytes_sequence) #compute and append the appropriate CRC bytes to the message
    print("     > Computed and appended CRC value: 0x{_crc_val:04X}".format(_crc_val = crc_val))
    print("     > Message contents as follows:")
    for i in range(len(bytes_sequence)):
        print("         [{index}] -> 0x{value:02X}".format(index = i, value = bytes_sequence[i]))
    
    hbi_cobs.encode(bytes_sequence) #COBS encode our message with the appropriate
    print("     > Computed COBS encoding of byte sequence")
    print("     > Message contents as follows:")
    for i in range(len(bytes_sequence)):
        print("         [{index}] -> 0x{value:02X}".format(index = i, value = bytes_sequence[i]))

    serial_comms.write(bytes_sequence) #write the bytes out to the serial port
    print("     Sent data over serial")

#==================================== INITIAL MESSAGE DECODING AND DISPATCH ===================================
def decode_dispatch(byte_array):
    try:
        byte_array = byte_array[byte_array.index(hbi_cobs.START_OF_FRAME):] #slice the array from the SOF to the end 
    except:
        print("No response to parse")
    
    #if we don't have any bytes, don't continue the function
    if(len(byte_array) <= 0):
        return
    
    byte_array = list(byte_array) #convert byte_array into a list type
    print("Received the following over comms link:")
    for i in range(len(byte_array)):
        print("         [{index}] -> 0x{value:02X}".format(index = i, value = byte_array[i]))

    #we have bytes to decode --> try COBS decoding
    print("...message length {length} --> Decoding".format(length = len(byte_array)))
    hbi_cobs.decode(byte_array) 
    if(len(byte_array) <= 0):
        print("COBS Decode UNSUCCESSFUL")
        return #don't continue if COBS decode wasn't successful
    print("COBS Decode SUCCESSFUL - message contents as follows:")
    for i in range(len(byte_array)):
        print("         [{index}] -> 0x{value:02X}".format(index = i, value = byte_array[i]))

    #COBS decode successful, validate CRC
    print("Validating CRC")
    crc_valid = hbi_crc.validate_crc(CRC_CALC, byte_array)
    if(not crc_valid):
       print('      \\==> CRC INVALID')
       return
    print("     \\==> CRC VALID")

    #CRC valid, dispatch message to the appropriate handler
    if(byte_array[1] in message_handlers):
        print("Dispatching received message from Device {id} appropriately".format(id = byte_array[0]))
        message_handlers[byte_array[1]](byte_array)
    else:
        print("Received uncategorized message from Device {id}".format(id = byte_array[0]))

#==================================== MAIN FUNCTION =================================
if __name__ == "__main__":
    print()
    print()
    print("##################################################################")
    print("Barebones Python Interface Tool for Shim Amplifiers")
    print("By Ishaan Govindarajan 2023")
    print("##################################################################")

    #connect to a serial port
    print()
    COMMS = serial_connect()
    print()

    #get endpoint ID that we wanna chat with
    print()
    ENDPOINT_ID = get_endpoint_id()
    print()
    
    #create a CRC calculator for CRC-16/AUG-CCITT
    CRC_CALC = hbi_crc.init_crc(0x1021, 0x1D0F, 0)

    #maintain a dictionary mapping of command codes to commands
    commands = {}
    commands.update(hbi_commands_tests.COMMANDS_TESTS) #add additional command codes this way
    commands.update(hbi_commands_stage.COMMANDS_POWER_STAGE)

    #maintain a dictionary mapping of request codes to requests
    requests = {}
    requests.update(hbi_requests_tests.REQUESTS_TESTS) #add additional request codes this way
    requests.update(hbi_request_stage.REQUESTS_POWER_STAGE)

    #concatenate all those into acceptable actions
    actions = {}
    actions.update(commands)
    actions.update(requests)
    actions.update({'lc':list_commands})
    actions.update({'lr':list_request})
    actions.update({'exit':exit_app})

    #create a dictionary that maps different firwmare --> host messages to appropriate callback functions
    message_handlers = {}
    message_handlers.update({hbi_nack_handler.NACK_MESSAGE_CODE: hbi_nack_handler.handle_nack})
    message_handlers.update({hbi_ack_handler.ACK_MESSAGE_CODE: hbi_ack_handler.handle_ack})
    message_handlers.update({hbi_response_handler.RESPONSE_MESSAGE_CODE: hbi_response_handler.handle_response})

    #we got here, basically go through the user entry infinite loop
    while(True):
        #quickly flush the serial buffer
        COMMS.reset_input_buffer()

        #get the user input for which particular action they want to execute
        action_to_do = action_loop()
        message = action_to_do() # execute the particular action, and get the message the action wants to send to the firmware (if it exists)

        #create some whitespace
        print()
        print()
        
        #if the particular action wants us to send a message to firmware
        if(len(message) > 0):
            #prepend the message with the endpoint ID
            message.insert(0, ENDPOINT_ID)

            #checksum, encode, and send the message
            pack_and_send_message(CRC_CALC, COMMS, message)

            #read from serial until we get an END OF FRAME character
            #have to do some casting and converting to make the `read_until()' work as expected
            rx_bytes = COMMS.read_until(expected=chr(hbi_cobs.END_OF_FRAME).encode('ASCII')) #read until we get an end of frame
            
            #decode and handle the received message from the firmware
            decode_dispatch(rx_bytes)

            #create some whitespace
            print()
            print()
