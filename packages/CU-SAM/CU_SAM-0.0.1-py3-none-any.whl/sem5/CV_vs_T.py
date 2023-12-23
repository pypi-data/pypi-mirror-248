print('''import numpy as np
import matplotlib.pyplot as plt
from numpy import random
T = np.linspace(1, 50, 1000)
theta_E = [10, 20]
def cv1(T):
    return (((theta_E[0]/T)**2)*np.exp(theta_E[0]/T))/(np.exp(theta_E[0]/T)-1)**2
def cv2(T):
    return (((theta_E[1]/T)**2)*np.exp(theta_E[1]/T))/(np.exp(theta_E[1]/T)-1)**2
plt.plot(T, cv1(T), '--', label='10K')
plt.plot(T, cv2(T), label='20K')
plt.xlabel(r'Temperature')
plt.ylabel(r"$\frac{c_{v}}{3R}$")
plt.title(r'$\frac{c_{v}}{3R}$ distribution for different temperature(Einstenin theory)')
plt.legend()
plt.show()
''')
