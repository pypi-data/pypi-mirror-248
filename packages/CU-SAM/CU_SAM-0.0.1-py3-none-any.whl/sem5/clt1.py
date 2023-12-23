print(''' import numpy
import matplotlib.pyplot as plt

# number of sample
num = [1000, 5000, 10000, 15000] 
# list of sample means
means = [] 

# Generating 10, 100, 500, 1000 random numbers from -100 to 100
# taking their mean and appending it to list means.
for j in num:
	# Generating seed to get same result 
	# every time the loop is run
	numpy.random.seed(1)
	x = [numpy.mean(numpy.random.randint(-100, 100, j)) for _i in range(5000)]
	means.append(x)
k = 0

# plotting all the means in one figure
fig, ax = plt.subplots(2, 2, figsize =(8, 8))
for i in range(0, 2):
	for j in range(0, 2):
		# Histogram for each x stored in means
		ax[i, j].hist(means[k], 10, density = True)
		ax[i, j].set_title(label = num[k])
		k = k + 1
plt.show()''')
