from PIL import Image
from lib import *

distribute_or_recovery, image_file, k, output_dir = verify_params()

def apply_shadow(shadow, carriers):
    shadowPosition = 0
    for i in [0,1,2]:     ##iterate through carriers
        for y in range(height):
            for x in range(width): ##iterate whole carrier
                pixel_bits = int_to_bits(carriers[i][x,y])
                patch = f"{shadow[shadowPosition]}{shadow[shadowPosition+1]}{shadow[shadowPosition+2]}{shadow[shadowPosition+3]}"
                shadowPosition += 4
                carriers[i][x, y] = bits_to_int(replace_last_four_chars(pixel_bits, patch)) # re-write last 4 digits of carrier

                if shadowPosition == len(shadowBinaryString):
                    print(f"done reading shadow, position {shadowPosition}\ncarrier {i}\ncarrier pos x{x} y{y}")
                    editedCarrier1 = output_dir + "/edited_cat.bmp"
                    editedCarrier2 = output_dir + "/edited_penguin.bmp"
                    editedCarrier3 = output_dir + "/edited_sunflower.bmp"
                    carrier1Copy.save(editedCarrier1)
                    carrier2Copy.save(editedCarrier2)
                    carrier3Copy.save(editedCarrier3)
                    return
                if shadowBinaryString[shadowPosition] == " ":
                    shadowPosition += 1


def recover_shadow(shadow, carriers):
    shadowX, shadowY = 0,0
    shadowBuffer = ""
    for i in [0,1,2]:     ##iterate through carriers
        print(f"i: {i}")
        for y in range(height):
            print(f"{y}")
            for x in range(width): ##iterate whole carrier
                # print(shadowBuffer)
                pixel_bits = int_to_bits(carriers[i][x, y])
                fragment = f"{pixel_bits[-4:]}"
                if shadowBuffer == "":
                    shadowBuffer = fragment + "0000"
                else:
                    shadowBuffer = shadowBuffer[:4] + fragment
                    shadow[shadowX, shadowY] = bits_to_int(shadowBuffer)
                    shadowBuffer = ""
                    if shadowX < width-1:
                        shadowX += 1
                    else:
                        if shadowY < height-1:
                            shadowX = 0
                            shadowY += 1
                        else:
                            print(f"done writing shadow\nstopped in:\ncarrier {i}\ncarrier pos x{x} y{y}")
                            return


## execution

if distribute_or_recovery == "d":
    carrier1 = Image.open(output_dir + "/1cat.bmp")
    carrier2 = Image.open(output_dir + "/2penguin.bmp")
    carrier3 = Image.open(output_dir + "/3sunflower.bmp")
elif distribute_or_recovery == "r":
    carrier1 = Image.open(output_dir + "/edited_cat.bmp")
    carrier2 = Image.open(output_dir + "/edited_penguin.bmp")
    carrier3 = Image.open(output_dir + "/edited_sunflower.bmp")
else:
    carrier1 = None
    carrier2 = None
    carrier3 = None
    exit(1)

# copy to allow modify of files
width, height = carrier1.size
carrier1Copy = carrier1.copy()
carrier2Copy = carrier2.copy()
carrier3Copy = carrier3.copy()

carrier1PixelData = carrier1Copy.load()
carrier2PixelData = carrier2Copy.load()
carrier3PixelData = carrier3Copy.load()

carriers_data = [carrier1PixelData, carrier2PixelData, carrier3PixelData]
### done preparing data

if distribute_or_recovery == "d":
    ### set data
    shadow = Image.open(image_file)
    binary_data = shadow.tobytes()
    shadowBinaryString = ' '.join(format(byte, '08b') for byte in binary_data)

    apply_shadow(shadowBinaryString, carriers_data)
    exit(0)
elif distribute_or_recovery == "r":
    recovered_shadow = Image.new("L", (width, height))
    recover_shadow(recovered_shadow.load(), carriers_data)
    recovered_shadow.save(output_dir + "/recovered_shadow.bmp")
