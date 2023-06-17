from lib import *

#distribute_or_recovery, image_file, k, output_dir = verify_params()

def apply_shadow(shadow, carrierData, copy, index, LSB, height, width):
    shadowPosition = 0
    # a = len(shadow)
    # print(a)
    for y in range(height):
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
    cant_bytes_needed = cant_numbers * (6-LSB)
    total = width * height
    total_offset = total - cant_bytes_needed
    x_offset = int(total_offset % width)
    y_offset = int(total_offset // width)

    x_offset -= 100
    y_offset -= 0

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
            # pixel_bits = int_to_bits(carrier[y, x])

            fragment = f"{pixel_bits[-LSB:]}"

            if shadowBuffer == "":
                shadowBuffer = fragment #+ '0' * (8-LSB)
                bufferOccupiedSize += LSB
            else:
                shadowBuffer = shadowBuffer[:bufferOccupiedSize] + fragment
                # shadowBuffer = fragment + shadowBuffer[:bufferOccupiedSize]

                bufferOccupiedSize += LSB
                if bufferOccupiedSize == 8:
                    # if len(a_i) < tuples_to_read:
                    #     a_i.append(bits_to_int(shadowBuffer))
                    # else:
                    #     shadow.append((a_i[a_i_index] , bits_to_int(shadowBuffer)))
                    #     a_i_index += 1
                    #
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

                    if shadowX < width-1:
                        shadowX += 1
                    else:
                        if shadowY < height-1:
                            shadowX = 0
                            shadowY += 1
                        else:
                            # print(f"done writing shadow\nstopped in:\ncarrier pos x{x} y{y}")
                            # return shadow
                            print("Error, image too small to contain full shadow")
                            exit(1)
        x_offset=0
    print("Error, image too small to contain shadow")
    exit(1)