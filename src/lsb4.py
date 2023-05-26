from PIL import Image
from lib import *

distribute_or_recovery, image_file, k, output_dir = verify_params()

### set data

# if(distribute_or_recovery == "d"):
shadow = Image.open(image_file)
width, height = shadow.size
binary_data = shadow.tobytes()
shadowBinaryString = ' '.join(format(byte, '08b') for byte in binary_data)
shadowPixelData = shadow.load()


carrier1 = Image.open(output_dir + "/1cat.bmp")
carrier1Copy = carrier1.copy()
carrier2 = Image.open(output_dir + "/2penguin.bmp")
carrier2Copy = carrier2.copy()
carrier3 = Image.open(output_dir + "/3sunflower.bmp")
carrier3Copy = carrier3.copy()

carrier1OriginalPixelData = carrier1.load()
carrier1PixelData = carrier1Copy.load()
carrier2PixelData = carrier2Copy.load()
carrier3PixelData = carrier3Copy.load()

carriers_data = [carrier1PixelData, carrier2PixelData, carrier3PixelData]

### done preparing data


def apply_shadow(shadow, carriers):
    shadowPosition = 0
    for i in [0,1,2]:     ##iterate through carriers
        for y in range(height):
            for x in range(width): ##iterate whole carrier
                pixel_bits = int_to_bits(carriers[i][x,y])
                patch = f"{shadow[shadowPosition]}{shadow[shadowPosition+1]}{shadow[shadowPosition+2]}{shadow[shadowPosition+3]}"
                shadowPosition = shadowPosition+4
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
                    shadowPosition = shadowPosition+1

apply_shadow(shadowBinaryString, carriers_data)


