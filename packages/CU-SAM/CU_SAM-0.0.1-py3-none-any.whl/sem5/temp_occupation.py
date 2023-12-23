print('''import numpy as np
import matplotlib.pyplot as plt
T = np.linspace(10, 1000, 1000)
mu = 0.45
E = [0.44, 0.46]
k = 8.617*10**(-5)
def nE1(T):
    return 1/(np.exp((E[0]-mu)/(k*T))+1)
def nE2(T):
    return 1/(np.exp((E[1]-mu)/(k*T))+1)
plt.plot(k*T, nE1(T), 'r--', label='E=0.44')
plt.plot(k*T, nE2(T), 'g', label='E=0.46')
plt.axhline(0.5)
plt.xlabel(r'Temperature')
plt.ylabel(r"Average of $n_{E}$")
plt.title(r'Distribution of mean occupation number for different energy')
plt.legend()
plt.show()
''')







