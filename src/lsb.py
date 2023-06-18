from lib import *

def apply_shadow(shadow, carrierData, copy, index, LSB, height, width, k):
    shadowPosition = 0

    tuples_to_read = (width * height) / (2*k-2)

    cant_numbers = tuples_to_read * 2
    cant_bytes_needed = cant_numbers * (6-LSB) #6-4=2 , 6-2=4 -> LSB2 needs 4bytes, LSB4 needs 2bytes
    total = width * height
    total_offset = total - cant_bytes_needed
    x_offset = int(total_offset % width)
    y_offset = int(total_offset // width)
    # x_offset += 4
    y_offset += 0

    for y in range(y_offset, height):
        for x in range(width): ##iterate whole carrier
            pixel_bits = int_to_bits(carrierData[x,y])

            patch = ""
            if LSB == 4:
                patch = f"{shadow[shadowPosition]}{shadow[shadowPosition+1]}{shadow[shadowPosition+2]}{shadow[shadowPosition+3]}"
            elif LSB == 2:
                patch = f"{shadow[shadowPosition]}{shadow[shadowPosition + 1]}"
            shadowPosition += LSB
            carrierData[x, y] = bits_to_int(replace_last_n_chars(pixel_bits, patch, LSB)) # re-write last N digits of carrier

            if shadowPosition == len(shadow):
                print(f"done reading shadow, position {shadowPosition}\ncarrier pos x{x} y{y}")
                editedCarrier = f"./images/{index+1}_edited.bmp"
                copy.save(editedCarrier)

                change_reserved_bit(editedCarrier, index+1)

                return
            if shadow[shadowPosition] == " ":
                shadowPosition += 1
    print("Error, carrier is not big enough for shadow")
    exit(1)


def recover_shadow(carrier, LSB, width, height, k):
    if (width * height) % (2*k-2) != 0:
        print("Error, wrong K for this image size")
        exit(1)
    tuples_to_read = (width * height) / (2*k-2)

    cant_numbers = tuples_to_read * 2
    cant_bytes_needed = cant_numbers * (6-LSB) #6-4=2 , 6-2=4 -> LSB2 needs 4bytes, LSB4 needs 2bytes
    total = width * height
    total_offset = total - cant_bytes_needed
    x_offset = int(total_offset % width)
    y_offset = int(total_offset // width)

    # x_offset += 4
    y_offset += 0
    # x_offset = 0
    # y_offset = 100

    shadowX, shadowY = 0,0
    shadow = []
    shadowBuffer = ""
    bufferOccupiedSize = 0
    tupleBuffer = None
    # a_i = []
    # a_i_index = 0
    for y in range(y_offset, height):
        for x in range(x_offset, width): ##iterate whole carrier
            pixel_bits = int_to_bits(carrier[x, y])

            fragment = f"{pixel_bits[-LSB:]}"

            if shadowBuffer == "":
                shadowBuffer = fragment
                bufferOccupiedSize += LSB
            else:
                shadowBuffer = shadowBuffer[:bufferOccupiedSize] + fragment

                bufferOccupiedSize += LSB
                if bufferOccupiedSize == 8:
                    if tupleBuffer is None:
                        tupleBuffer = bits_to_int(shadowBuffer)
                    else:
                        shadow.append([tupleBuffer, bits_to_int(shadowBuffer)])
                        tupleBuffer = None
                    #
                    shadowBuffer = ""
                    bufferOccupiedSize = 0
                    if len(shadow) == tuples_to_read:
                        print(f"\ndone recovering shadow\nstopped in:\ncarrier pos x{x} y{y}")
                        return shadow

                    # if shadowX < width-1:
                    #     shadowX += 1
                    # else:
                    #     if shadowY < height-1:
                    #         shadowX = 0
                    #         shadowY += 1
                    #     else:
                    #         # print(f"done writing shadow\nstopped in:\ncarrier pos x{x} y{y}")
                    #         # return shadow
                    #         print("Error, image too small to contain full shadow")
                    #         exit(1)
        x_offset=0
    print("Error, image too small to contain shadow")
    return shadow
    # exit(1)