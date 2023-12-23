print('''import numpy as np
import matplotlib.pyplot as plt

n = 1
x = lambda n: np.mean(np.random.uniform(1, 7, size = n))
xx = [x(n) for i in range(1000)]

plt.subplot(2, 2, 1)
plt.hist(xx, bins=50, label='n = 1')

plt.legend()
plt.xlabel('mean of samples')
plt.ylabel('frequency of occurance')

n = 2
x = lambda n: np.mean(np.random.uniform(1, 7, size = n))
xx = [x(n) for i in range(1000)]

plt.subplot(2, 2, 2)
plt.hist(xx, bins=50, label='n = 2')

plt.legend()
plt.xlabel('mean of samples')
plt.ylabel('frequency of occurance')

n = 5
x = lambda n: np.mean(np.random.uniform(1, 7, size = n))
xx = [x(n) for i in range(1000)]

plt.subplot(2, 2, 3)
plt.hist(xx, bins=50, label='n = 5')

plt.legend()
plt.xlabel('mean of samples')
plt.ylabel('frequency of occurance')

n = 100
x = lambda n: np.mean(np.random.uniform(1, 7, size = n))
xx = [x(n) for i in range(1000)]

plt.subplot(2, 2, 4)
plt.hist(xx, bins=50, label='n = 100')

plt.legend()
plt.xlabel('mean of samples')
plt.ylabel('frequency of occurance')
plt.suptitle('Proof of Cenral Limit Theorem for a die')
plt.show()'''
)
