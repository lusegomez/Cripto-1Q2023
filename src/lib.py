def int_to_bits(n):
    bits = bin(n)[2:]
    bits = bits.zfill(8)
    return bits

def bits_to_int(bits):
    integer = int(bits, 2)
    return integer

def replace_last_four_chars(string, patch):
    replaced_string = ""
    if len(string) >= 4:
        replaced_string = string[:-4] + patch
    else:
        print("error in string patching size")
        exit(1)
    return replaced_string