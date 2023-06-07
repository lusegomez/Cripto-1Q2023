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

    shadowX, shadowY = 0,0
    shadow = []
    shadowBuffer = ""
    bufferOccupiedSize = 0
    tupleBuffer = None
    for y in range(height):
        for x in range(width): ##iterate whole carrier
            pixel_bits = int_to_bits(carrier[x, y])
            fragment = f"{pixel_bits[-LSB:]}"

            if shadowBuffer == "":
                shadowBuffer = fragment #+ '0' * (8-LSB)
                bufferOccupiedSize += LSB
            else:
                shadowBuffer = shadowBuffer[:bufferOccupiedSize] + fragment #+ '0' * (8-bufferOccupiedSize-LSB)
                bufferOccupiedSize += LSB
                if bufferOccupiedSize == 8:
                    if tupleBuffer is None:
                        tupleBuffer = bits_to_int(shadowBuffer)
                    else:
                        shadow.append((tupleBuffer, bits_to_int(shadowBuffer)))
                        tupleBuffer = None
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
                            print("Error, image too small to contain shadow")
                            exit(1)
    print("Error, image too small to contain shadow")
    exit(1)


# original, when it was applying a bmp to other n bmps:
# def recover_shadow(shadow, carriers, LSB, width, height):
#     shadowX, shadowY = 0,0
#     shadowBuffer = ""
#     bufferOccupiedSize = 0
#     for i in range(len(carriers)):     ##iterate through carriers
#         for y in range(height):
#             for x in range(width): ##iterate whole carrier
#                 pixel_bits = int_to_bits(carriers[i][x, y])
#                 fragment = f"{pixel_bits[-LSB:]}"
#
#                 if shadowBuffer == "":
#                     shadowBuffer = fragment #+ '0' * (8-LSB)
#                     bufferOccupiedSize += LSB
#                 else:
#                     shadowBuffer = shadowBuffer[:bufferOccupiedSize] + fragment #+ '0' * (8-bufferOccupiedSize-LSB)
#                     bufferOccupiedSize += LSB
#                     if bufferOccupiedSize == 8:
#                         shadow[shadowX, shadowY] = bits_to_int(shadowBuffer)
#                         shadowBuffer = ""
#                         bufferOccupiedSize = 0
#                         if shadowX < width-1:
#                             shadowX += 1
#                         else:
#                             if shadowY < height-1:
#                                 shadowX = 0
#                                 shadowY += 1
#                             else:
#                                 print(f"done writing shadow\nstopped in:\ncarrier {i}\ncarrier pos x{x} y{y}")
#                                 return

#old stuff:

## execution


'''
if distribute_or_recovery == "d":
    carrier1 = Image.open(output_dir + "/1cat.bmp")
    carrier2 = Image.open(output_dir + "/2penguin.bmp")
    carrier3 = Image.open(output_dir + "/3sunflower.bmp")
    carrier4 = Image.open(output_dir + "/4dog.bmp")
    carrier5 = Image.open(output_dir + "/5kangaroo.bmp")
elif distribute_or_recovery == "r":
    carrier1 = Image.open(output_dir + "/edited_cat.bmp")
    carrier2 = Image.open(output_dir + "/edited_penguin.bmp")
    carrier3 = Image.open(output_dir + "/edited_sunflower.bmp")
    carrier4 = Image.open(output_dir + "/edited_dog.bmp")
    carrier5 = Image.open(output_dir + "/edited_kangaroo.bmp")
else:
    carrier1 = None
    carrier2 = None
    carrier3 = None
    carrier4 = None
    carrier5 = None
    exit(1)
'''
'''
# copy to allow modify of files
width, height = carrier1.size
carrier1Copy = carrier1.copy()
carrier2Copy = carrier2.copy()
carrier3Copy = carrier3.copy()
carrier4Copy = carrier4.copy()
carrier5Copy = carrier5.copy()

carrier1PixelData = carrier1Copy.load()
carrier2PixelData = carrier2Copy.load()
carrier3PixelData = carrier3Copy.load()
carrier4PixelData = carrier4Copy.load()
carrier5PixelData = carrier5Copy.load()

carriers_data = [carrier1PixelData, carrier2PixelData, carrier3PixelData, carrier4PixelData, carrier5PixelData]
'''
### done preparing data
'''
LSB = None
if k in [3, 4]:
    LSB = 4
elif k in [5, 6, 7, 8]:
    LSB = 2
else:
    print("Error deciding which LSB to use")
    exit(1)
'''

'''
if distribute_or_recovery == "d":
    ### set data
    image = Image.open("./yoda.bmp")
    np_image = np.array(image)
    image_sharing = Shamir(3, 4)
    shadows = image_sharing.generate_shadows(np_image)

    #shadow = Image.open(image_file)
    shadow = shadows[0]
    binary_data = shadow.tobytes()
    shadowBinaryString = ' '.join(format(byte, '08b') for byte in binary_data)

    apply_shadow(shadowBinaryString, carriers_data, LSB)

    exit(0)
elif distribute_or_recovery == "r":
    recovered_shadow = Image.new("L", (width, height))

    recover_shadow(recovered_shadow.load(), carriers_data, LSB)
    recovered_shadow.save(output_dir + "/recovered_shadow.bmp")
'''