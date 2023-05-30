from ImageSharing import Shamir
from PIL import Image

import numpy as np

image = np.array(
     [[5,4, 9], [10, 9, 2], [8, 5, 1], [5,2,1]]
)

#image = Image.open("./yoda.bmp")
np_image = np.array(image)

#print(np_image.shape)
#flat = np_image.reshape(-1, 3)
#print(flat.shape)
#print(flat)

image_sharing = Shamir(3, 4)

shadows = image_sharing.generate_shadows(image)

sub = [shadows[0], shadows[2], shadows[1]]

reconstructed = image_sharing.reconstruct_image(sub)

print(shadows)

print(reconstructed)