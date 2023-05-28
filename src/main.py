from ImageSharing import ImageSharing
from PIL import Image

import numpy as np

image = np.array(
    [[5,4, 9], [10, 9, 2], [8, 5, 1], [5,2,1]]#, [7,8,9]]
)
image_sharing = ImageSharing()



shadows = image_sharing.generate_shadows(image, 3)

sub = [shadows[0], shadows[2], shadows[1]]

reconstructed = image_sharing.reconstruct_image(sub)

print(shadows)

print(reconstructed)