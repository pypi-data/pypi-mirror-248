print('''import numpy as np
import matplotlib.pyplot as plt
T=np.linspace(100,2000,100)
E=[0.05,0.10,0.15]
k=8.617*10**(-5)
def f1(E):
    return (2/np.sqrt(np.pi))*(1/(k*T)**(3/2))*np.sqrt(E[0])*np.exp(-E[0]/(k*T))
def f2(E):
    return (2/np.sqrt(np.pi))*(1/(k*T)**(3/2))*np.sqrt(E[1])*np.exp(-E[1]/(k*T))
def f3(E):
    return (2/np.sqrt(np.pi))*(1/(k*T)**(3/2))*np.sqrt(E[2])*np.exp(-E[2]/(k*T))
plt.plot(T,f1(E),'--',label='E=0.05')
plt.plot(T,f2(E),'+',label='E=0.10')
plt.plot(T,f3(E),label='E=0.15')
plt.legend()
plt.xlabel('Temperature')
plt.ylabel('f(E,T)')
plt.title('MB distribution at various Temperatures')
plt.show()
''')
