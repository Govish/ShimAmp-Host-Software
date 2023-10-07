
HOST_REQUEST = 0x02

REQUEST_STAGE_ENABLE_STATUS_CODE = 0x10
REQUEST_STAGE_GET_FSW_CODE = 0x14
REQUEST_STAGE_GET_DRIVE_CODE = 0x1A
REQUEST_STAGE_GET_DUTIES_CODE = 0x1E



def send_request_stage_enable_status():
    print("TODO")

    # message = [HOST_REQUEST, n, <payload ... >]
    # return message
    return []

def send_request_stage_get_fsw():
    print("TODO")

    # message = [HOST_REQUEST, n, <payload ... >]
    # return message
    return []

def send_request_stage_get_drive():
    print("TODO")

    # message = [HOST_REQUEST, n, <payload ... >]
    # return message
    return []

def send_request_stage_get_duties():
    print("TODO")

    # message = [HOST_REQUEST, n, <payload ... >]
    # return message
    return []


#have a dictionary that maps a command string to a function
#said function will transmit an appropriate amount of bytes over the serial port
REQUESTS_POWER_STAGE = {
    'REQUEST_STAGE_ENABLE_STATUS' : send_request_stage_enable_status,
    'REQUEST_STAGE_GET_FSW' : send_request_stage_get_fsw,
    'REQUEST_STAGE_GET_DRIVE' : send_request_stage_get_drive,
    'REQUEST_STAGE_GET_DUTIES' : send_request_stage_get_duties,
}