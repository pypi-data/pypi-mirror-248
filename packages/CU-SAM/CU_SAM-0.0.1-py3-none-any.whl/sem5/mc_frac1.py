print('''import mcintegration as mci
def f(x):
    return x/(1+x)**3

a = 0
b = 1
N = 100000

ext = ((-2*b+1)/(2*(1+b)**2))
print('exact: ', ext)
res = mci.mc(f,a,b,N)
print('calc: ',res)

''')
