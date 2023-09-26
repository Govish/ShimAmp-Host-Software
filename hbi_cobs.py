
START_OF_FRAME = 0xFF
END_OF_FRAME = 0x00

def encode(byte_sequence):

    #add some additional overhead bytes
    byte_sequence.insert(0, START_OF_FRAME) #start of frame
    byte_sequence.insert(1, 0) #next SOF character in sequence (filled later)
    byte_sequence.insert(2, 0) #next EOF character in sequence (filled later)
    byte_sequence.append(END_OF_FRAME) #end of frame

    next_sof_char_index = len(byte_sequence) - 1
    next_eof_char_index = len(byte_sequence) - 1
    
    #iterate from back to front, start at byte just before EOF, end at byte just before overhead bytes
    #more or less copying the firmware implementation of cobs--see more in-depth docs there
    for i in range(len(byte_sequence) - 2, 2, -1): #note end index is exclusive
        #encode any SOF characters we see
        if(byte_sequence[i] == START_OF_FRAME):
            byte_sequence[i] = next_sof_char_index - i
            next_sof_char_index = i

        #encode any EOF characters we run into
        elif(byte_sequence[i] == END_OF_FRAME):
            byte_sequence[i] = next_eof_char_index - i
            next_eof_char_index = i
    
    #at index 1, point to the first SOF char we see in our message
    byte_sequence[1] = next_sof_char_index - 1 #subtracting 1 since we're placing this at the first index

    #at index 2, point to the first EOF char we see in our message
    byte_sequence[2] = next_eof_char_index - 2 #subtracting 2 since we're placing this at the second index

def decode(byte_sequence):
    #last character should be an EOF
    if(byte_sequence.pop(len(byte_sequence) - 1) != END_OF_FRAME):
        byte_sequence.clear()
        return
    
    #first character should be an SOF
    if(byte_sequence.pop(0) != START_OF_FRAME):
        byte_sequence.clear()
        return
    
    #get the indices of the next start/end of frame characters in encoded message
    next_sof_char_index = byte_sequence.pop(0) - 2 #since there's gonna be 2 more bytes until the start of payload
    next_eof_char_index = byte_sequence.pop(0) - 1 #since there's gonna be 1 more byte until start of payload

    #go through the message and replace characters as necessary
    for i in range(len(byte_sequence)):
        #if this byte should be a start of frame character, compute the index of the next one and replace the current spot in the message
        if(next_sof_char_index == i):
            next_sof_char_index += byte_sequence[i]
            byte_sequence[i] = START_OF_FRAME
        
        #do a similar thing with the EOF character
        elif(next_eof_char_index == i):
            next_eof_char_index += byte_sequence[i]
            byte_sequence[i] = END_OF_FRAME

    #ensure that the delimiter pointers finish up by pointing to the end of the message
    if(next_eof_char_index != len(byte_sequence)):
        byte_sequence.clear()
        return
    
    if(next_sof_char_index != len(byte_sequence)):
        byte_sequence.clear()
        return