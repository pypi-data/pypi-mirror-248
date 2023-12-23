print('''import numpy as np
import matplotlib.pyplot as plt
n=10000
N=range(1,n)
x=np.random.choice([0,1],size=n)
y=[np.sum(x[:i])/i for i in N]
z=[1-x for x in y]
plt.subplot(1,2,1)
plt.plot(N,y,label='fraction of head')
plt.plot(N,z,label='fraction of tail')
plt.legend()
plt.xlabel('no of trials')
#plt.title('Simulation of coin toss')
x=np.random.choice([0,1],size=n)
y=[np.sum(x[:i])/i for i in N]
z=[1-x for x in y]
plt.axhline(0.5)
plt.subplot(1,2,2)
plt.plot(N,y,label='fraction of tail')
plt.plot(N,z,label='fraction of head')
plt.legend()
plt.axhline(0.5)
plt.xlabel('no of trials')
plt.suptitle('Simulation of coin toss')
plt.show()'''
)
