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


def send_command_stage_disable(channel_num = 0, prompt_user = True):
    if(prompt_user):
        valid_channel_num = False
        while(not valid_channel_num):
            #prompt the user for input
            print("Enter the channel number to disable (or nothing for channel 0)")
            try:
                #grab whatever channel the user says
                user_in = input(">>>")
                if(user_in == ""):
                    channel_num = 0
                else:
                    channel_num = int(user_in)

                #try to convert into an int 
                if((channel_num < 0) or (channel_num > 256)):
                    raise IndexError            
            except:
                print("Invalid channel, try again")
            else:
                valid_channel_num = True

    #disable the corresponding channel
    print("DISABLING CHANNEL {chan}".format(chan = channel_num))
    # message = [HOST_COMMAND, n, <payload ... >]
    message = [HOST_COMMAND, 2, COMMAND_STAGE_DISABLE_CODE, channel_num]
    # return message
    return message

def send_command_stage_enable_regulator(channel_num = 0, prompt_user = True):
    if(prompt_user):
        valid_channel_num = False
        while(not valid_channel_num):
            #prompt the user for input
            print("Enter the channel number to start regulating (or nothing for channel 0)")
            try:
                #grab whatever channel the user says
                user_in = input(">>>")
                if(user_in == ""):
                    channel_num = 0
                else:
                    channel_num = int(user_in)

                #try to convert into an int 
                if((channel_num < 0) or (channel_num > 256)):
                    raise IndexError            
            except:
                print("Invalid channel, try again")
            else:
                valid_channel_num = True

    #enable the corresponding channel in regulation mode
    print("ENABLING CHANNEL {chan} IN AUTOMATIC CURRENT REGULATION MODE".format(chan = channel_num))
    # message = [HOST_COMMAND, n, <payload ... >]
    message = [HOST_COMMAND, 2, COMMAND_STAGE_ENABLE_REGULATOR_CODE, channel_num]
    # return message
    return message

def send_command_stage_enable_manual(channel_num = 0, prompt_user = True):
    if(prompt_user):
        #get the channel number from the user
        valid_channel_num = False
        while(not valid_channel_num):
            #prompt the user for input
            print("Enter the channel number to start controlling (or nothing for channel 0)")
            try:
                #grab whatever channel the user says
                user_in = input(">>>")
                if(user_in == ""):
                    channel_num = 0
                else:
                    channel_num = int(user_in)

                #try to convert into an int 
                if((channel_num < 0) or (channel_num > 256)):
                    raise IndexError            
            except:
                print("Invalid channel, try again")
            else:
                valid_channel_num = True
        
        #confirm with the user this is what they wanna do
        valid_confirm_msg = False
        while(not valid_confirm_msg):
            #prompt the user for input
            print("Are you sure you want to enable in manual mode? type 'MANUAL' to confirm, else type anything else")
            #grab the user confirmation message
            confirm_msg = input(">>>")
            if(len(confirm_msg) > 100):
                print("Confirm message too long!")
            else:
                valid_confirm_msg = True

    #enable the corresponding channel in regulation mode
    print("ENABLING CHANNEL {chan} IN MANUAL POWER STAGE CONTROL MODE".format(chan = channel_num))
    # message = [HOST_COMMAND, n, <payload ... >]
    message = [HOST_COMMAND, 2 + len(confirm_msg), COMMAND_STAGE_ENABLE_MANUAL_CODE, channel_num]
    message += list(bytes(confirm_msg, "ASCII"))
    # return message
    return message

def send_command_stage_enable_autotune(channel_num = 0, prompt_user = True):
    if(prompt_user):
        #get the channel number from the user
        valid_channel_num = False
        while(not valid_channel_num):
            #prompt the user for input
            print("Enter the channel number to start autotuning (or nothing for channel 0)")
            try:
                #grab whatever channel the user says
                user_in = input(">>>")
                if(user_in == ""):
                    channel_num = 0
                else:
                    channel_num = int(user_in)

                #try to convert into an int 
                if((channel_num < 0) or (channel_num > 256)):
                    raise IndexError            
            except:
                print("Invalid channel, try again")
            else:
                valid_channel_num = True
        
        #confirm with the user this is what they wanna do
        valid_confirm_msg = False
        while(not valid_confirm_msg):
            #prompt the user for input
            print("Are you sure you want to enable autotuning? type 'TUNE' to confirm, else type anything else")
            #grab the user confirmation message
            confirm_msg = input(">>>")
            if(len(confirm_msg) > 100):
                print("Confirm message too long!")
            else:
                valid_confirm_msg = True

    #enable the corresponding channel in regulation mode
    print("ENABLING CHANNEL {chan} IN AUTOTUNING MODE".format(chan = channel_num))
    # message = [HOST_COMMAND, n, <payload ... >]
    message = [HOST_COMMAND, 2 + len(confirm_msg), COMMAND_STAGE_ENABLE_AUTOTUNE_CODE, channel_num]
    message += list(bytes(confirm_msg, "ASCII"))
    # return message
    return message

def send_command_stage_set_fsw(fsw = 0, prompt_user = True):
    if(prompt_user):
        valid_fsw = False
        while(not valid_fsw):
            #prompt the user for input
            print("Enter the desired switching frequency in Hz")
            try:
                #try to convert the user input into a float
                fsw = float(input(">>>"))          
            except:
                print("Invalid input, try again")
            else:
                valid_fsw = True

    #disable the corresponding channel
    print("Setting switching frequency to {_fsw}".format(_fsw = fsw))
    # message = [HOST_COMMAND, n, <payload ... >]
    message = [HOST_COMMAND, 5, COMMAND_STAGE_SET_FSW_CODE]
    message += list(struct.pack(">f", fsw))
    # return message
    return message

def send_command_stage_manual_drive_off(channel_num = 0, prompt_user = True):
    if(prompt_user):
        valid_channel_num = False
        while(not valid_channel_num):
            #prompt the user for input
            print("Enter the channel number to drive off (or nothing for channel 0)")
            try:
                #grab whatever channel the user says
                user_in = input(">>>")
                if(user_in == ""):
                    channel_num = 0
                else:
                    channel_num = int(user_in)

                #try to convert into an int 
                if((channel_num < 0) or (channel_num > 256)):
                    raise IndexError            
            except:
                print("Invalid channel, try again")
            else:
                valid_channel_num = True

    #drive the corresponding channel
    print("DRIVING CHANNEL {chan} OFF IN MANUAL MODE".format(chan = channel_num))
    # message = [HOST_COMMAND, n, <payload ... >]
    message = [HOST_COMMAND, 2, COMMAND_STAGE_MANUAL_DRIVE_OFF_CODE, channel_num]
    # return message
    return message

def send_command_stage_manual_set_drive(drive = 0, channel_num = 0, prompt_user = True):
    if(prompt_user):
        #get the channel number from the user
        valid_channel_num = False
        while(not valid_channel_num):
            #prompt the user for input
            print("Enter the channel number to drive (or nothing for channel 0)")
            try:
                #grab whatever channel the user says
                user_in = input(">>>")
                if(user_in == ""):
                    channel_num = 0
                else:
                    channel_num = int(user_in)

                #try to convert into an int 
                if((channel_num < 0) or (channel_num > 256)):
                    raise IndexError            
            except:
                print("Invalid channel, try again")
            else:
                valid_channel_num = True
        
        #confirm with the user this is what they wanna do
        valid_drive = False
        while(not valid_drive):
            #prompt the user for input
            print("Enter the desired drive value (-1 to 1)")
            try:
                #try to convert the user input into a float
                drive = float(input(">>>"))          
            except:
                print("Invalid input, try again")
            else:
                valid_drive = True
    
    #drive the corresponding channel
    print("DRIVING CHANNEL {chan} WITH VALUE {_drive} IN MANUAL MODE".format(chan = channel_num, _drive = drive))
    # message = [HOST_COMMAND, n, <payload ... >]
    message = [HOST_COMMAND, 6, COMMAND_STAGE_MANUAL_SET_DRIVE_CODE, channel_num]
    message += list(struct.pack(">f", drive))
    # return message
    return message

def send_command_stage_manual_set_duties(drive_pos = 0, drive_neg = 0, channel_num = 0, prompt_user = True):
    if(prompt_user):
        #get the channel number from the user
        valid_channel_num = False
        while(not valid_channel_num):
            #prompt the user for input
            print("Enter the channel number to drive (or nothing for channel 0)")
            try:
                #grab whatever channel the user says
                user_in = input(">>>")
                if(user_in == ""):
                    channel_num = 0
                else:
                    channel_num = int(user_in)

                #try to convert into an int 
                if((channel_num < 0) or (channel_num > 256)):
                    raise IndexError            
            except:
                print("Invalid channel, try again")
            else:
                valid_channel_num = True
        
        #grab the positive drive the user wants to send
        valid_drive_p = False
        while(not valid_drive_p):
            #prompt the user for input
            print("Enter the desired drive value for the positive half-bridge (0 to 1)")
            try:
                #try to convert the user input into a float
                drive_pos = float(input(">>>"))          
            except:
                print("Invalid input, try again")
            else:
                valid_drive_p = True
        
        #grab the positive drive the user wants to send
        valid_drive_n = False
        while(not valid_drive_n):
            #prompt the user for input
            print("Enter the desired drive value for the negative half-bridge (0 to 1)")
            try:
                #try to convert the user input into a float
                drive_neg = float(input(">>>"))          
            except:
                print("Invalid input, try again")
            else:
                valid_drive_n = True
    
    #drive the corresponding channel
    print("DRIVING CHANNEL {chan} WITH VALUES (+,-), ({dp},{dn}) IN MANUAL MODE".format(chan = channel_num, dp = drive_pos, dn = drive_neg))
    # message = [HOST_COMMAND, n, <payload ... >]
    message = [HOST_COMMAND, 10, COMMAND_STAGE_MANUAL_SET_DUTIES_CODE, channel_num]
    message += list(struct.pack(">f", drive_pos))
    message += list(struct.pack(">f", drive_neg))
    # return message
    return message

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