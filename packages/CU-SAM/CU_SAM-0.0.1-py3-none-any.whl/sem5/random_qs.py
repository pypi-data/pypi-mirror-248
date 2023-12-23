import numpy as np
from numpy.random import uniform, choice

N = 10000
s = 20   # selected sample numbers

n = eval(input('n = '))
z = uniform(0, 1, N)
w = [choice(z, s) for _ in range(n)]

mu = np.mean(w)
print('mu = ',mu)

std = np.std(w)
print('Standard deviation = ',std)
k4 = np.mean([(w[i] - np.mean(w))**4 for i in range(20)])
mu4 = (k4/std**4 - 3)
print('k4 = ',k4)
print('mu4 = ',mu4)


