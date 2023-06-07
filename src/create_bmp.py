import pandas as pd
from PIL import Image
SIZE = (4,4)

image = Image.open("yoda.jpg")
image = image.resize(SIZE)
image = image.convert("L")

image.save("yoda.bmp")

image.show()
