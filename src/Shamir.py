from lib import *
from random import randint
from lagrange import lagrange

class Shamir:
    def __init__(self, k, n):
        df = pd.read_csv('./inverses.csv', index_col='Number')
        inverses = df['Inverse'].to_dict()
        inverses_adjusted = {int(k): v for k, v in inverses.items()}
        self.inverses = inverses_adjusted
        self.k = k
        self.n = n
        if k > n:
            print("Error, k must be smaller or equal than n")
            exit(1)
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
            # ri = randint(1, 250) # != 0 y != 251
            ri = 3

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
                tup = (mij, dij)
                shadows[j-1].append(tup)
                # shadows.append(mij)
                # shadows.append(dij)
        return shadows


    def reconstruct_image(self, shadows, shadowNumbers):
        #Ejemplo de shadows
        # s1 = [(m11, d11), (m21, d21), (m31, d31), (m41, d41)]
        # s2 = [(m12, d12), (m22, d22), (m32, d32), (m42, d42)]

        # M = []
        # D = []
        # for shadow in shadows:
        #     M.append([])
        #     D.append([])
        #     for i in range(len(shadows[0])):
        #         M[i].append(shadow[i][0])
        #         D[i].append(shadow[i][1])

        M = [ [shadow[i][0] for shadow in shadows] for i in range(len(shadows[0])) ]
        D = [ [shadow[i][1] for shadow in shadows] for i in range(len(shadows[0])) ]
        
        polypoints_M = []
        polypoints_D = []
        for i in range(len(M)):
            points = []
            for j in range(len(M[0])):
                points.append([shadowNumbers[j], M[i][j]])
            polypoints_M.append(points)

        for i in range(len(D)):
            points = []
            for j in range(len(D[0])):
                points.append([shadowNumbers[j], D[i][j]])
            polypoints_D.append(points)

        f_coeffs = []
        g_coeffs = []
        for i, element in enumerate(polypoints_M):
            f_coeffs.append(lagrange(element))
        for i, element in enumerate(polypoints_D):
            g_coeffs.append(lagrange(element))


        # print("f_coeffs")
        # print(f_coeffs)
        # print("g_coeffs")
        # print(g_coeffs)
        validated = False
        for r in range(1, 250):
            if validated:
                break
            for i in range(len(f_coeffs)):
                equation_1 = (r * f_coeffs[i][0] + g_coeffs[i][0]) % MOD
                equation_2 = (r * f_coeffs[i][1] + g_coeffs[i][1]) % MOD

                if equation_1 != 0 or equation_2 != 0:
                    validated = False
                    break
                else:
                    validated = True

        if not validated:
            print("Error, one of the Shadows was cheated")
            # exit(1)

        recovered = []


        #remove trailing 0s
        for i, element in enumerate(f_coeffs):
            f = f_coeffs[i][:self.k]
            # f = f[2:]
            g = g_coeffs[i][:self.k]
            g = g[2:]
            B = f + g
            recovered.append(B)

        return recovered

     ###############################################
  