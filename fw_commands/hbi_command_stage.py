import struct #have to use this to pack float

HOST_COMMAND = 0x01

COMMAND_STAGE_DISABLE_CODE = 0x10
COMMAND_STAGE_ENABLE_REGULATOR_CODE = 0x11
COMMAND_STAGE_ENABLE_MANUAL_CODE = 0x12
COMMAND_STAGE_ENABLE_AUTOTUNE_CODE = 0x13

COMMAND_STAGE_SET_FSW_CODE = 0x14
COMMAND_STAGE_MANUAL_DRIVE_OFF_CODE = 0x16
COMMAND_STAGE_MANUAL_SET_DRIVE_CODE = 0x1A
COMMAND_STAGE_MANUAL_SET_DUTIES_CODE = 0x1E


def send_command_stage_disable():
    print("TODO")

    # message = [HOST_COMMAND, n, <payload ... >]
    # return message
    return []

def send_command_stage_enable_regulator():
    print("TODO")

    # message = [HOST_COMMAND, n, <payload ... >]
    # return message
    return []

def send_command_stage_enable_manual():
    print("TODO")

    # message = [HOST_COMMAND, n, <payload ... >]
    # return message
    return []

def send_command_stage_enable_autotune():
    print("TODO")

    # message = [HOST_COMMAND, n, <payload ... >]
    # return message
    return []

def send_command_stage_set_fsw():
    print("TODO")

    # message = [HOST_COMMAND, n, <payload ... >]
    # return message
    return []

def send_command_stage_manual_drive_off():
    print("TODO")

    # message = [HOST_COMMAND, n, <payload ... >]
    # return message
    return []

def send_command_stage_manual_set_drive():
    print("TODO")

    # message = [HOST_COMMAND, n, <payload ... >]
    # return message
    return []

def send_command_stage_manual_set_duties():
    print("TODO")

    # message = [HOST_COMMAND, n, <payload ... >]
    # return message
    return []

#have a dictionary that maps a command string to a function
#said function will transmit an appropriate amount of bytes over the serial port
COMMANDS_POWER_STAGE = {
    'COMMAND_STAGE_DISABLE' : send_command_stage_disable,
    'COMMAND_STAGE_ENABLE_REGULATOR' : send_command_stage_enable_regulator,
    'COMMAND_STAGE_ENABLE_MANUAL' : send_command_stage_enable_manual,
    'COMMAND_STAGE_ENABLE_AUTOTUNE' : send_command_stage_enable_autotune,
    'COMMAND_STAGE_SET_FSW' : send_command_stage_set_fsw,
    'COMMAND_STAGE_MANUAL_DRIVE_OFF' : send_command_stage_manual_drive_off,
    'COMMAND_STAGE_MANUAL_SET_DRIVE' : send_command_stage_manual_set_drive,
    'COMMAND_STAGE_MANUAL_SET_DUTIES' : send_command_stage_manual_set_duties,
}