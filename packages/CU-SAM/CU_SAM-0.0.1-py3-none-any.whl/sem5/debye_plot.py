print('''import numpy as np
import matplotlib.pyplot as plt
from numpy import random
def f(x):
    return x**4*np.exp(x)/(np.exp(x)-1)**2

def MC(f, a, b, N):
    x = random.uniform(a, b, N)
    return (b - a)*np.mean(f(x))
temperature = np.linspace(1, 40, 1000)
N = 100000

theta_D = [4, 10]

Debye1 = [3*(T/theta_D[0])**3*MC(f, 0, theta_D[0]/T, N) for T in temperature]
Debye2 = [3*(T/theta_D[1])**3*MC(f, 0, theta_D[1]/T, N) for T in temperature]

plt.plot(temperature, Debye1, label='4K')
plt.plot(temperature, Debye2, label='10K')
plt.legend()
plt.xlabel('Temperature')
plt.title('Distribution of f(T) at two different temperature')
plt.ylabel('f(T)')
plt.show()
''')
