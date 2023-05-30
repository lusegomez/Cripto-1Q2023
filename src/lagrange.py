import numpy as np
import pandas as pd


def get_inverses():
    df = pd.read_csv('./inverses_mod11.csv', index_col='Number')
    inv = df['Inverse'].to_dict()
    return {int(k): v for k, v in inv.items()}


MOD = 11
inverses = get_inverses()


def calculate_s_n(polypoints):
    lagrange_poly_k = 0
    for i, point in enumerate(polypoints):
        lagrange_i = 1
        for j, point_j in enumerate(polypoints):
            if i != j:
                x_i = polypoints[i][0]
                x_j = polypoints[j][0]
                lagrange_i *= (-x_j * inverses[(x_i - x_j) % MOD])
        lagrange_poly_k += lagrange_i * polypoints[i][1]

    return lagrange_poly_k % MOD


def lagrange(polypoints):
    coefficients = []
    i = 0
    amount_of_points = len(polypoints)
    while i < amount_of_points:
        s_n = calculate_s_n(polypoints)
        coefficients.append(s_n)
        polypoints = calculate_new_polypoints(polypoints, s_n)
        i += 1
    return coefficients


def calculate_new_polypoints(polypoints, s_n):
    polypoints.pop()  # Discard one point
    new_polypoints = []
    while len(polypoints) > 0:
        [old_x, old_y] = polypoints.pop()

        new_y = ((old_y - s_n) * inverses[old_x]) % MOD
        new_polypoints.append([old_x, new_y])
    return new_polypoints


initial_polypoints = [[1, 3], [5, 10], [2, 9]]
print(lagrange(initial_polypoints))
