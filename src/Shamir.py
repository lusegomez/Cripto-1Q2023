from PIL import Image
from random import randint
from numpy.polynomial.polynomial import Polynomial
import numpy as np
import pandas as pd
from sympy import symbols, expand, Mod
from lib import evaluate_pol, MOD



class Shamir:
    def __init__(self, k, n):
        df = pd.read_csv('./inverses.csv', index_col='Number')
        inverses = df['Inverse'].to_dict()
        inverses_adjusted = {int(k): v for k, v in inverses.items()}
        self.inverses = inverses_adjusted
        self.k = k
        self.n = n
        pass


    def generate_shadows(self, image):
        shadows = [[] for _ in range(self.n)]
        flat = image.flatten()
        t = 2 * self.k - 2
        # divide the image into t non-overlapping 2k-2 pixels blocks (B1, B2, ..., Bl)
        if len(flat) % t != 0:
            print("error in image size, not divisible by 2k-2")
            exit(1)
        blocks = np.array_split(flat, len(flat) / t)
        f = []
        g = []
        vij = []

        for index, block in enumerate(blocks):
            a = []
            for i in range(self.k):
                a.append(block[i])
            if a[0] == 0 or a[0] == 251:
                a[0] = 1
            if a[1] == 0 or a[1] == 251:
                a[1] = 1
            f.append(a)

            b = []
            ri = randint(1, 250) # != 0 y != 251
            # ri = 77

            b0 =  (- ri * a[0] ) % MOD
            if b0 != 0 and b0 != 251:
                b.append(b0)
            else:
                b.append(1)

            b1 =  (- ri * a[1] ) % MOD
            if b1 != 0 and b1 != 251:
                b.append(b1) #b[1]
            else:
                b.append(1)

            for i in range(self.k-2):
                b.append(block[self.k + i])
            g.append(b)

            for j in range(1, self.n+1): #1...n
                mij = evaluate_pol(a, j)
                dij = evaluate_pol(b, j)
                shadows[j-1].append({mij, dij})
                # shadows.append(mij)
                # shadows.append(dij)

        return shadows


    def reconstruct_image(self, shadows):
        num_blocks = len(shadows)
        if num_blocks < self.k:
            print("error in num blocks, need at least K to decipher")
            exit(1)
        block_size = len(shadows[0])
        reconstructed = np.array([])
        shares = [[] for _ in range(block_size)]
        for s, share in enumerate(shares):
            for o in range(self.k):
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


    '''
    def generate_shadows(self, image):
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
        print("done generating shadows")
        return shadows

    def reconstruct_image(self, shadows):
        num_blocks = len(shadows)
        if num_blocks < self.k:
            print("error in num blocks, need at least K to decipher")
            exit(1)
        block_size = len(shadows[0])
        reconstructed = np.array([])
        shares = [[] for _ in range(block_size)]
        for s, share in enumerate(shares):
            for o in range(self.k):
                share.append(shadows[o][s])
        coefs = []
        # Extract v1j, v2j, ..., vmj from S1, S2, ..., Sm (where Si is the i-th shadow)
        for j in range(block_size):
            t = np.transpose(shares[j])
            coefs.append(self.__gauss_polynomial(t[0], t[1])) #[i for i in range(1, num_blocks + 1)]

        return coefs
     '''
  