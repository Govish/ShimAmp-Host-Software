import struct #have to use this to unpack float


RESPONSE_STAGE_GET_ENABLE_STATUS_CODE = 0x10
RESPONSE_STAGE_GET_FSW_CODE = 0x14
RESPONSE_STAGE_GET_DRIVE_CODE = 0x1A
RESPONSE_STAGE_GET_DUTIES_CODE = 0x1E

def handle_stage_get_enable_status(byte_stream):
    print("TODO")

def handle_stage_get_fsw(byte_stream):
    print("TODO")

def handle_stage_get_drive_code(byte_stream):
    print("TODO")

def handle_stage_get_duties_code(byte_stream):
    print("TODO")


RESPONSE_STAGE_MAPPING = {
    RESPONSE_STAGE_GET_ENABLE_STATUS_CODE: handle_stage_get_enable_status,
    RESPONSE_STAGE_GET_FSW_CODE: handle_stage_get_fsw,
    RESPONSE_STAGE_GET_DRIVE_CODE: handle_stage_get_drive_code,
    RESPONSE_STAGE_GET_DUTIES_CODE: handle_stage_get_duties_code,
}