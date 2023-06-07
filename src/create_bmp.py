import pandas as pd
from PIL import Image
SIZE = (500,500)

image = Image.open("7carpincho.jpeg")
image = image.resize(SIZE)
image = image.convert("L")

image.save("7carpincho.bmp")

image.show()
