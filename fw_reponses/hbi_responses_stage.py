import struct #have to use this to unpack float


RESPONSE_STAGE_GET_ENABLE_STATUS_CODE = 0x10
RESPONSE_STAGE_GET_FSW_CODE = 0x14
RESPONSE_STAGE_GET_DRIVE_CODE = 0x1A
RESPONSE_STAGE_GET_DUTIES_CODE = 0x1E


def handle_stage_get_enable_status(byte_stream):
    #define enumeration to enable status
    enable_status_mapping = {
        0xFF: "UNINITIALIZED",
        0x00: "DISABLED",
        0x01: "ENABLED - AUTOMATIC CURRENT REGULAITON",
        0x02: "ENABLED - MANUAL CONTROL",
        0x03: "ENABLED - AUTOTUNING"
    }

    #notify the user of received message; sanity check message format
    print("RECEIVED RESPONSE TO GET_ENABLE_STATUS")
    if(len(byte_stream) != 2): #message code gets sliced out
        print("     \\==> INVALID RESPONSE SIZE")
        return
    
    #decode the enable status from the enumeration
    enable_status = "UNKNOWN ENABLE STATE"
    if(byte_stream[1] in enable_status_mapping):
        enable_status = enable_status_mapping[byte_stream[1]]
    
    #print to the user
    print("     \\==> Channel {chan} Enable Status: {stat}".format(chan = byte_stream[0], stat = enable_status))



def handle_stage_get_fsw(byte_stream):
    #notify the user of received message; sanity check message format
    print("RECEIVED RESPONSE TO GET_FSW")
    if(len(byte_stream) != 4): #message code gets sliced out
        print("     \\==> INVALID RESPONSE SIZE")
        return
    
    #decode the switching frequency
    fsw_bytes = bytes(byte_stream)
    fsw = struct.unpack(">f", fsw_bytes)[0] #convert bytes to big endian float, returns as tuple
    
    #print to the user
    print("     \\==> Stages are switching at {_fsw:.4f} MHz".format(_fsw = fsw/1e6))



def handle_stage_get_drive_code(byte_stream):
    #notify the user of received message; sanity check message format
    print("RECEIVED RESPONSE TO GET_ENABLE_STATUS")
    if(len(byte_stream) != 5): #message code gets sliced out
        print("     \\==> INVALID RESPONSE SIZE")
        return
    
    #decode the drive from the received byte stream
    drive_bytes = bytes(byte_stream[1:5])
    drive = struct.unpack(">f", drive_bytes)[0] #convert bytes to big endian float, returns as tuple
    
    #print to the user
    print("     \\==> Channel {chan} output drive: {_drive:.3f}".format(chan = byte_stream[0], _drive = drive))



def handle_stage_get_duties_code(byte_stream):
    #notify the user of received message; sanity check message format
    print("RECEIVED RESPONSE TO GET_ENABLE_STATUS")
    if(len(byte_stream) != 9): #message code gets sliced out
        print("     \\==> INVALID RESPONSE SIZE")
        return
    
    #decode the half-bridge drives from the received byte stream
    dp_bytes = bytes(byte_stream[1:5])
    dn_bytes = bytes(byte_stream[5:9])
    drive_pos = struct.unpack(">f", dp_bytes)[0] #convert bytes to big endian float, returns as tuple
    drive_neg = struct.unpack(">f", dn_bytes)[0] #convert bytes to big endian float, returns as tuple
    
    
    #print to the user
    print("     \\==> Channel {chan} Bridge Drives:".format(chan = byte_stream[0]))
    print("         --> Positive Half Bridge: {pos:.3f}".format(pos = drive_pos))
    print("         --> Negative Half Bridge: {neg:.3f}".format(neg = drive_neg))


RESPONSE_STAGE_MAPPING = {
    RESPONSE_STAGE_GET_ENABLE_STATUS_CODE: handle_stage_get_enable_status,
    RESPONSE_STAGE_GET_FSW_CODE: handle_stage_get_fsw,
    RESPONSE_STAGE_GET_DRIVE_CODE: handle_stage_get_drive_code,
    RESPONSE_STAGE_GET_DUTIES_CODE: handle_stage_get_duties_code,
}