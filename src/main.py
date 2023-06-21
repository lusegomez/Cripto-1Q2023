import io

from Shamir import Shamir
from lib import *
from lsb import apply_shadow, recover_shadow


distribute_or_recovery, image_file, k, output_dir = verify_params()


# open files
carriers = []
fileNames = []
n=0
for filename in os.listdir(output_dir):
    if os.path.isfile(os.path.join(output_dir, filename)):
        if filename.endswith(".bmp"):
            image = f"{output_dir}/{filename}"
            carriers.append(Image.open(image))
            fileNames.append(filename)
            n += 1

if len(carriers) < 1:
    print("error, need more files in" + output_dir)
    exit(1)

#shallow copy to allow modification of files
width, height = carriers[0].size
carriers_data = []
carriers_byte_arrays = []
copies = []
for c in carriers:
    copies.append(c.copy())
    carriers_data.append(copies[-1].load())

    carriers_byte_arrays.append(c.tobytes())


#config LSB
LSB = None
if k in [3, 4]:
    LSB = 4
elif k in [5, 6, 7, 8]:
    LSB = 2
else:
    print("Error deciding which LSB to use")
    exit(1)


#START
#create Shamir object
image_sharing = Shamir(k, n)

if distribute_or_recovery == "d":
    image = Image.open(image_file)
    np_image = np.array(image)
    #generate Shadows
    shadows = image_sharing.generate_shadows(np_image)

    # apply LSB of each shadow to a cover file
    for index, s in enumerate(shadows):
        shadow_simplified = " ".join([bin(value)[2:].zfill(8) for tuple_ in s for value in tuple_])
        apply_shadow(shadow_simplified, carriers_data[index], copies[index], index, LSB, height, width, k)

    print("done")
    exit(0)

elif distribute_or_recovery == "r":
    recovered_secret = Image.new("L", (width, height))
    secret_data = recovered_secret.load()

    shadows = []
    shadowNumbers = []

    for index, carrier in enumerate(carriers_data):
        shadow = recover_shadow(carrier, LSB, width, height, k, carriers_byte_arrays[index])
        shadows.append(shadow)
        shadowNumbers.append(read_reserved_bit(f"{output_dir}/{fileNames[index]}"))


    recovered_blocks = image_sharing.reconstruct_image(shadows, shadowNumbers)
    recovered_blocks = np.array(recovered_blocks).flatten()
    recovered_blocks = np.resize(recovered_blocks, (height, width))

    for i in range(height):
        for j in range(width):
            secret_data[j, i] = int(recovered_blocks[i][j])

    recovered_secret.save(f"{output_dir}/output/{image_file}")

exit(0)