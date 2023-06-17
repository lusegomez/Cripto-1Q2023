import pandas as pd
from PIL import Image
SIZE = (140,140)

image = Image.open("./images/og/140x140/zebra.jpg")
image = image.resize(SIZE)
image = image.convert("L")

image.save("./images/og/140x140/8zebra.bmp")

# image.show()
