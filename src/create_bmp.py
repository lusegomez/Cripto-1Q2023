import pandas as pd
from PIL import Image
SIZE = (500, 500)

from PIL import Image

image = Image.open("yoda.jpg")
image = image.resize(SIZE)
image = image.convert("L")

image.save("imagen.bmp")

image.show()
