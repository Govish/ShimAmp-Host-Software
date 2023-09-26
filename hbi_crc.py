from crc import Calculator, Configuration

def init_crc(_poly, _init, _xor):
    poly = _poly
    init = _init
    xor = _xor

    crc_config = Configuration(
        width=16,
        polynomial=_poly,
        init_value=_init,
        final_xor_value=_xor
    )

    return Calculator(crc_config, optimized=True)

def append_crc(crc_calc, byte_sequence):
    #have to compute byte sequence into this special type
    crc_val = crc_calc.checksum(bytes(byte_sequence)) #compute the CRC value given the input sequence
    crc_bytes = crc_val.to_bytes(2, 'big') #grab the individual bytes of the CRC value

    byte_sequence.append(crc_bytes[0]) #append to input array -> high byte
    byte_sequence.append(crc_bytes[1]) #append to input array -> low byte
    
    return crc_val #return the CRC value

def validate_crc(crc_calc, byte_sequence):
    return crc_calc.verify(bytes(byte_sequence), 0)