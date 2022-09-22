import struct

# Convert hex strings to ints and doubles in Big-Endian and Little-Endian


def conv_int_BE(s):
    return struct.unpack('>I', bytes.fromhex(s))[0]

def conv_int_LE(s):
    return struct.unpack('<I', bytes.fromhex(s))[0]

def conv_double_LE(s):
    return struct.unpack('<d', bytes.fromhex(s))[0]

def conv_double_BE(s):
    return struct.unpack('>d', bytes.fromhex(s))[0]