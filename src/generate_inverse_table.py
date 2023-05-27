import pandas as pd
def generate_multiplicative_inverses(mod):
    inverses = {}
    for num in range(1, mod):
        for inv in range(1, mod):
            if (num * inv) % mod == 1:
                inverses[num] = inv
                break
    return inverses

mod = 251
inverses = generate_multiplicative_inverses(mod)

df = pd.DataFrame.from_dict(inverses, orient='index', columns=['Inverse'])
df.index.name = 'Number'

filename = 'inverses.csv'
df.to_csv(filename)
