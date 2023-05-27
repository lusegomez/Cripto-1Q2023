from ImageSharing import ImageSharing
from PIL import Image

import numpy as np

image = np.array([[5,4, 9], [10, 9, 2], [8, 5, 1]])
image_sharing = ImageSharing()



shadows = image_sharing.generate_shadows(image, 3)

reconstructed = image_sharing.reconstruct_image(shadows)

print(reconstructed)