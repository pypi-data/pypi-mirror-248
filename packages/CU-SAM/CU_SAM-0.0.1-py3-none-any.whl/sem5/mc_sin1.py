import mcintegration as mc
import numpy as np
import numpy.random as random
f = lambda x: np.sin(x)

N = 100000  # number of trials
y_min = 0   #lower limit of integration

x = random.uniform(0, np.pi, N)
y_max = np.max(f(x)) + 1 # upper limit of integration(1 is added to minimize errors)
y = random.uniform(y_min, y_max, N)

area = (np.pi - 0)*(y_max - y_min)
n = np.sum([abs(y) < abs(f(x))]) # number of points inside the function curve

int_result = area*(n/N)
print('Integration value of sin(x)[in between 0 to pi]: ',int_result)

