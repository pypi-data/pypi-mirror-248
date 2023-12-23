print('''import random
def mc(f, a, b, N):
    samples = 0
    inside_f = 0
    for _ in range(N):
        x = random.uniform(a, b)
        y = random.uniform(a, b)

        if y <= f(x):
            inside_f += 1
        samples += 1
    int_result = (inside_f/samples)*(b - a)*f(b)
    return int_result

def f(x):
    return x**2
a = 0 #lower lim
b = 1 #upper lim

N = 100000 # num of try

ans = mc(f, a, b, N)
print(ans)

''')
