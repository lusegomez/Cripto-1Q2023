import pandas as pd
from PIL import Image
SIZE = (12, 12)

image = Image.open("yoda.jpg")
image = image.resize(SIZE)
image = image.convert("L")

image.save("yoda.bmp")

image.show()
