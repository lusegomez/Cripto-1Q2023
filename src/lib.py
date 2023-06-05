import sys
import os
import numpy as np

def int_to_bits(n):
    bits = bin(n)[2:]
    bits = bits.zfill(8)
    return bits

def bits_to_int(bits):
    integer = int(bits, 2)
    return integer

def replace_last_n_chars(string, patch, n):
    replaced_string = ""
    if len(string) >= n:
        replaced_string = string[:-n] + patch
    else:
        print("error in string patching size")
        exit(1)
    return replaced_string



### verify params
def get_n(directory):
    files = os.listdir(directory)
    return len(files)

def local_verify_params(distribute_or_recovery, image_file, k, output_dir):
    if distribute_or_recovery not in ["d", "r"]:
        raise ValueError("El primer parámetro debe ser 'd' o 'r'.")
    if not os.path.isfile(image_file):
        raise FileNotFoundError(f"No se encontró el archivo: {image_file}")
    if not isinstance(output_dir, str) or not os.path.isdir(output_dir):
        raise NotADirectoryError(f"No es un directorio válido: {output_dir}")
    if not (k > 2 and k <= get_n(output_dir)):
        raise ValueError("k debe ser mayor o igual que 3 y menor o igual que n")

def verify_params():
    if len(sys.argv) != 5:
        raise ValueError("Se requieren 4 argumentos: <operation> <file.bmp> <k> <directory>")

    try:
        distribute_or_recovery = sys.argv[1]
        image_file = sys.argv[2]
        k = int(sys.argv[3])
        output_dir = sys.argv[4]

        local_verify_params(distribute_or_recovery, image_file, k, output_dir)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return distribute_or_recovery, image_file, k, output_dir
### end verify params

MOD = 251

def evaluate_pol(pol, x):
    ret = 0
    for index, a in enumerate(pol):
        ret += a * x**index
    return ret % MOD