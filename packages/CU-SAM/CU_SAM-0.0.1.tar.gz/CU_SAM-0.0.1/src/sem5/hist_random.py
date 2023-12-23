print('''import numpy as np
import matplotlib.pyplot as plt
from numpy import random
N=100000
s=eval(input('value of s: '))
n=eval(input('value of n: '))
z=random.uniform(0,1,N)
w=[np.mean(random.choice(z,s))for i in range(n)]
plt.subplot(1,2,1)
plt.hist(z,bins=50)
plt.title('original array')
plt.xlabel('random numbers')
plt.subplot(1,2,2)
plt.hist(w,bins=50)
plt.title('mean array')
plt.xlabel('random numbers')
plt.show()
''')
