from Shamir import Shamir
from lib import *
from lsb import apply_shadow, recover_shadow

distribute_or_recovery, image_file, k, output_dir = verify_params()

# open files
carriers = []
n=0
for filename in os.listdir(output_dir):
    if os.path.isfile(os.path.join(output_dir, filename)):
        if filename.endswith(".bmp"):
            image = f"{output_dir}/{filename}"
            # carrier = Image.open(image)
            carriers.append(Image.open(image))
            n += 1

if len(carriers) < 1:
    print("error, need more files in" + output_dir)
    exit(1)

#shallow copy to allow modification of files
width, height = carriers[0].size
carriers_data = []
copies = []
for c in carriers:
    copies.append(c.copy())
    carriers_data.append(copies[-1].load())


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
if distribute_or_recovery == "d":
    image = Image.open(image_file)
    np_image = np.array(image)
    #create Shamir object
    image_sharing = Shamir(k, n)
    #generate Shadows
    shadows = image_sharing.generate_shadows(np_image)

    # apply LSB of each shadow to a cover file
    for index, s in enumerate(shadows):
        shadow_simplified = " ".join([bin(value)[2:].zfill(8) for tuple_ in s for value in tuple_])
        apply_shadow(shadow_simplified, carriers_data[index], copies[index], index, LSB, height, width)

    print("done")
    exit(0)

elif distribute_or_recovery == "r":
    recovered_shadow = Image.new("L", (width, height))
    
    recover_shadow(recovered_shadow.load(), carriers_data, LSB, width, height)
    
    recovered_shadow.save(f"{output_dir}/{image_file}")


#
# #image = np.array(
# #     [[5,4, 9], [10, 9, 2], [8, 5, 1], [5,2,1]]
# #)
#
# image = Image.open("./yoda.bmp")
# np_image = np.array(image)
#
#
# image_sharing = Shamir(3, 4)
#
# shadows = image_sharing.generate_shadows(np_image)
#
#
# #sub = [shadows[0], shadows[2], shadows[1]]
# #print(shadows[0])



#reconstructed = image_sharing.reconstruct_image(sub)

#print(shadows)

#print(reconstructed)