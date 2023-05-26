import sys
import os

def get_n(directory):
    files = os.listdir(directory)
    return len(files)

def verify_params(distribute_or_recovery, image_file, k, output_dir):
    if distribute_or_recovery not in ["d", "r"]:
        raise ValueError("El primer parámetro debe ser 'd' o 'r'.")
    if not os.path.isfile(image_file):
        raise FileNotFoundError(f"No se encontró el archivo: {image_file}")
    if not isinstance(output_dir, str) or not os.path.isdir(output_dir):
        raise NotADirectoryError(f"No es un directorio válido: {output_dir}")
    if not (k > 2 and k <= get_n(output_dir)):
        raise ValueError("k debe ser mayor o igual que 3 y menor o igual que n")
        
if len(sys.argv) != 5:
    raise ValueError("Se requieren 4 argumentos: <operation> <file.bmp> <k> <directory>")

try:
    distribute_or_recovery = sys.argv[1]
    image_file = sys.argv[2]
    k = int(sys.argv[3])
    output_dir = sys.argv[4]

    verify_params(distribute_or_recovery, image_file, k, output_dir)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

