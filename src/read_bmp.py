from PIL import Image

f = open("yoda.bmp")
image = Image.open("yoda.bmp")

width, height = image.size
binary_data = image.tobytes()

binary_string = ' '.join(format(byte, '08b') for byte in binary_data[:width])
print(binary_string)
