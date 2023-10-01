import serial
import hbi_crc
import hbi_cobs
import struct #have to use this to pack float


'''
Message formatting:
 *  A message packet is formatted as the following (proper specification doc to come):
 *
 *  Index	Abbreviation	Value Range		Description
 *   [0]		ID			0x0 - 0xFF		Node Address
 *   [1]		MTYPE		0x0 - 0x0F		Message type
 *   [2]		PLEN		0x1 - 0xF8		Message Payload Length
 *   [3]		PL0			0x0 - 0xFF		Payload byte 0, typically command or request code
 *   [4]		PL1			0x0 - 0xFF		Payload byte 1
 *    ...
 *   [n-2]		PLn			0x0 - 0xFF		Payload byte n
 *   [n-1]		CRCh		0x0 - 0xFF		CRC high byte
 *   [n]		CRCl		0x0	- 0xFF		CRC low byte
 *
 *
 *   Some notes on the specific bytes of the message:
 *   	- ID
 *   		... is the ID of the node; typically configured via dip switches on the board
 *   		as of now the protocol can support 256 nodes
 *
 *   	- MTYPE
 *   		...top 5 bits of this message are RESERVED - will either expand this to more ID bits or other message types (or who knows that's why they're reserved i guess)
 *   		Message types are as follows:
 *   			0x0 --> HOST_COMMAND_ALL_DEVICES: host writes this ADDRESSING ALL DEVICES ON BUS; useful for ARMing all amplifiers on the bus
 *   				\--> NO DEVICES WILL ACK OR NACK THIS MESSAGE!
 *   				\--> formatted just like any other command message
 *   			0x1 --> HOST_COMMAND_TO_DEVICE: host writes this to write parameters to the device; payload contains the particular command and the parameter values associated with the command
 *   			0x2 --> HOST_REQUEST_FROM_DEVICE: host writes this to read parameters to device; payload contains a code corresponding to a value the host wants to read
 *   			0x3 --> reserved
 *   			0x4 --> DEVICE_NACK_HOST_MESSAGE: node responds with this message type when there was some issue with the previous packet (payload will contain message descrption)
 *   			0x5 --> DEVICE_ACK_HOST_COMMAND: node responds with this message when host command successfully received/written; payload mirrors payload written to device
 *   			0x6 --> DEVICE_RESPONSE_HOST_REQUEST:node responds with this message with the data host requested; data delivered in message payload
 *   			0x7 --> reserved
 *
 *   	- PLEN
 *   		...payload length of the particular message packet--all messages have a payload length between 1-248 bytes
 *   			--> 248 computed by subtracting PROTOCOL_OVERHEAD from MAX_UNENCODED_LENGTH
 *   		if payload length out of bounds, this causes device to NACK with a corresponding error message
 *
 *   	- PLx
 *   		...payload bits of the message
 *   		for NACK messages, here are some following payload codes
 *				- 0x0	-->	unknown error
 *   			- 0x01	--> invalid CRC
 *   			- 0x02	--> invalid message size
 *   			- 0x03	--> unknown command code
 *   			- 0x04	--> unknown request code
 *   			- 0x05	--> command value out of range
 *   			- 0x06	--> command execution failed
 *   			- 0x07 	--> system busy
 *
 *   	- CRCh & CRCl
 *   		... are the high and low bytes of CRC-16/AUG-CCITT, a common 16-bit CRC, applied to the message
 *   		the CRC is computed least significant byte to most significant byte, from least significant bit to most significant bit
 *   		crc polynomial: 0x1021
 *   		crc seed: 0x1D0F
 *   		crc xor_out: 0x0000 (i.e. don't need to xor the CRC result
 '''

HOST_COMMAND = 0x01

COMMAND_TEST_BYTE_CODE = 0
COMMAND_TEST_UINT32_CODE = 1
COMMAND_TEST_INT32_CODE = 2
COMMAND_TEST_FLOAT_CODE = 3
COMMAND_TEST_STRING_CODE = 4

def send_command_test_byte(crc_calc, serial_comms, dest_id):
    #don't include SOF and EOF characters here--leave that for COBS
    #payload only contains register that we wanna request from
    print("     > Commanding test byte to ID {num}".format(num = dest_id))
    message = [dest_id, HOST_COMMAND, 2, COMMAND_TEST_BYTE_CODE, 0xAA]
    pack_and_send_message(crc_calc, serial_comms, message)

def send_command_test_uint32(crc_calc, serial_comms, dest_id):
    print("     > Commanding test uint32 to ID {num}".format(num = dest_id))
    
    uint_bytes = int.to_bytes(0xFFABCD00, length=4, byteorder='big')
    message = [dest_id, HOST_COMMAND, 5, COMMAND_TEST_UINT32_CODE]
    message += list(uint_bytes)
    pack_and_send_message(crc_calc, serial_comms, message)

def send_command_test_int32(crc_calc, serial_comms, dest_id):
    print("     > Commanding test int32 to ID {num}".format(num = dest_id))
    
    int_bytes = int.to_bytes(-31415, length=4, byteorder='big', signed=True)
    message = [dest_id, HOST_COMMAND, 5, COMMAND_TEST_INT32_CODE]
    message += list(int_bytes)
    pack_and_send_message(crc_calc, serial_comms, message)

def send_command_test_float(crc_calc, serial_comms, dest_id):
    print("     > Commanding test float to ID {num}".format(num = dest_id))
    
    float_bytes = struct.pack(">f", 123.25)
    message = [dest_id, HOST_COMMAND, 5, COMMAND_TEST_FLOAT_CODE]
    message += list(float_bytes)
    pack_and_send_message(crc_calc, serial_comms, message)

def send_command_test_string(crc_calc, serial_comms, dest_id):
    print("     > Commanding test string to ID {num}".format(num = dest_id))

    #pop in the correct payload length after adding the string
    message = [dest_id, HOST_COMMAND, 0, COMMAND_TEST_STRING_CODE]
    message += list(bytes("Congrats! You decoded this message correctly!\r\n", "ASCII"))
    message[2] = len(message) - 3
    pack_and_send_message(crc_calc, serial_comms, message)

def pack_and_send_message(crc_calc, serial_comms, bytes_sequence):
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

#have a dictionary that maps a command string to a function
#said function will transmit an appropriate amount of bytes over the serial port
COMMANDS_TESTS = {
    'COMMAND_TEST_BYTE' : send_command_test_byte,
    'COMMAND_TEST_UINT32' : send_command_test_uint32,
    'COMMAND_TEST_INT32' : send_command_test_int32,
    'COMMAND_TEST_FLOAT' : send_command_test_float,
    'COMMAND_TEST_STRING' : send_command_test_string,
}