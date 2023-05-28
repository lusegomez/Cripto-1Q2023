from PIL import Image
from random import randint
from numpy.polynomial.polynomial import Polynomial
import numpy as np
import pandas as pd
from sympy import symbols, expand, Mod

MOD = 251

class ImageSharing:
    def __init__(self):
        df = pd.read_csv('./inverses.csv', index_col='Number')
        inverses = df['Inverse'].to_dict()
        inverses_adjusted = {int(k): v for k, v in inverses.items()}
        self.inverses = inverses_adjusted
        pass
    def generate_shadows(self, image, k):
        shadows = []
        # divide the image into non-overlapping k-pixels blocks (B1, B2, ..., Bl)
        # in this case we use rows qty
        for o in range(image.shape[0]):
            shadows.append([])
        for index, block in enumerate(image):
            polynomial = Polynomial(block)
            # compute n share: vj1 = fj(1), ... , vjn=fj(n); j in [1,l]
            for i in range(1, image.shape[0]+1):
                share = polynomial(i)
                shadows[i-1].append((i,share))
        # output n shadows: Si = v1i || v2i || v3i || ... || vli
        return shadows

    def reconstruct_image(self, shadows):
        num_blocks = len(shadows)
        block_size = len(shadows[0])
        reconstructed = np.array([])
        shares=[[],[],[],[]]
        for s, share in enumerate(shares):
            for o in range(num_blocks):
                share.append(shadows[o][s])
        coefs = []
        # Extract v1j, v2j, ..., vmj from S1, S2, ..., Sm (where Si is the i-th shadow)
        for j in range(block_size):
            t = np.transpose(shares[j])
            coefs.append(self.__gauss_polynomial(t[0], t[1])) #[i for i in range(1, num_blocks + 1)]

        return coefs
     

     ###############################################

    def __solve_linear_system(self, matrix):
        matrix_np = np.array(matrix)
        A = matrix_np[:, :-1]
        b = matrix_np[:, -1]
        # Resolver el sistema de ecuaciones
        solution = np.linalg.solve(A, b)
        return solution

    def __gauss_polynomial(self, x_values, y_values):
        # Verificar que la cantidad de puntos sea igual
        if len(x_values) != len(y_values):
            raise ValueError("La cantidad de puntos x y y no coincide.")
        matrix = []
        for j in range(len(x_values)):
            vector = []
            for i in range(len(x_values)):
                elem = x_values[j]**i % MOD
                vector.append(elem)
            vector.append(y_values[j] % MOD)
            matrix.append(vector)
        solution = self.__solve_linear_system(matrix)
        return solution
    
  