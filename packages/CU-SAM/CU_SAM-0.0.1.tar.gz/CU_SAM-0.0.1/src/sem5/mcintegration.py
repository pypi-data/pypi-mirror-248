print('Monte Carlo integration module...')
print('import this as \033[32m from mcintegration import mc \033[0m')
print('Use: \033[32m mc(func, low_lim, up_lim, trials)\033[0m')
import random
def mc(f, a, b, N):
    samples = 0
    inside_f = 0
    for _ in range(N):
        x = random.uniform(a, b)
        y = random.uniform(f(a), f(b))

        if y <= f(x):
            inside_f += 1
        samples += 1
    int_result = (inside_f/samples)*(b - a)*f(b)
    return int_result
