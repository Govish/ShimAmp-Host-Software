
HOST_REQUEST = 0x02

REQUEST_STAGE_ENABLE_STATUS_CODE = 0x10
REQUEST_STAGE_GET_FSW_CODE = 0x14
REQUEST_STAGE_GET_DRIVE_CODE = 0x1A
REQUEST_STAGE_GET_DUTIES_CODE = 0x1E



def send_request_stage_enable_status(channel_num = 0, prompt_user = True):
    if(prompt_user):
        valid_channel_num = False
        while(not valid_channel_num):
            #prompt the user for input
            print("Enter the channel number to query (or nothing for channel 0)")
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

    print("     > Requesting power stage enable status from channel {chan}".format(chan = channel_num))
    # message = [HOST_REQUEST, n, <payload ... >]
    message = [HOST_REQUEST, 2, REQUEST_STAGE_ENABLE_STATUS_CODE, channel_num]
    # return message
    return message

def send_request_stage_get_fsw():
    print("     > Requesting switching frequency")
    # message = [HOST_REQUEST, n, <payload ... >]
    message = [HOST_REQUEST, 1, REQUEST_STAGE_GET_FSW_CODE]
    # return message
    return message

def send_request_stage_get_drive(channel_num = 0, prompt_user = True):
    if(prompt_user):
        valid_channel_num = False
        while(not valid_channel_num):
            #prompt the user for input
            print("Enter the channel number to query (or nothing for channel 0)")
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
    print("     > Requesting stage drive from channel {chan}".format(chan = channel_num))
    # message = [HOST_REQUEST, n, <payload ... >]
    message = [HOST_REQUEST, 2, REQUEST_STAGE_GET_DRIVE_CODE, channel_num]
    # return message
    return message

def send_request_stage_get_duties(channel_num = 0, prompt_user = True):
    if(prompt_user):
        valid_channel_num = False
        while(not valid_channel_num):
            #prompt the user for input
            print("Enter the channel number to query (or nothing for channel 0)")
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
    
    print("     > Requesting bridge duty cycles from channel {chan}".format(chan = channel_num))
    # message = [HOST_REQUEST, n, <payload ... >]
    message = [HOST_REQUEST, 2, REQUEST_STAGE_GET_DUTIES_CODE, channel_num]
    # return message
    return message


#have a dictionary that maps a command string to a function
#said function will transmit an appropriate amount of bytes over the serial port
REQUESTS_POWER_STAGE = {
    'REQUEST_STAGE_ENABLE_STATUS' : send_request_stage_enable_status,
    'REQUEST_STAGE_GET_FSW' : send_request_stage_get_fsw,
    'REQUEST_STAGE_GET_DRIVE' : send_request_stage_get_drive,
    'REQUEST_STAGE_GET_DUTIES' : send_request_stage_get_duties,
}