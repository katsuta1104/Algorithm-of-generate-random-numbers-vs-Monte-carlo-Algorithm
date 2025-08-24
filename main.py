import matplotlib.pyplot as plt
import random
import math
import sys

err = []
cnt = 0
N = 1000000
M = 100
Ns = list(range(1,N+1))

#メルセンヌツイスタ
def mersenne_twister(seed):
    return random.random()

#平方採中法
def Middle_square(seed,digits = 8):
    x = seed
    while True:
        s = str(x*x).zfill(2*digits)
        mid = s[(len(s)//2 - digits//2):(len(s)//2 + digits//2)]
        x = int(mid)
        yield x / (10**digits)
gen_mid = Middle_square(12345678)

#線形合同法
def Linear_Congruential_Generator(seed,a = 214013 ,c = 2531011,m = 2**32):
    x = seed % m
    while True:
        x = (x*a+c)%m
        yield x / m
gen_lcg = Linear_Congruential_Generator(1)

#XORshift
def xorshift32(seed):
    x = seed & 0xffffffff
    while True:
        x ^= (x << 13) & 0xffffffff
        x ^= (x >> 17) & 0xffffffff
        x ^= (x << 5) & 0xffffffff
        yield x / 2**32
gen_xor = xorshift32(1)



def gen_err_avg(func):
    arr = [[0.0]*N for _ in range(M)]
    for k in range(M):
        random.seed(k)
        current_sum = 0

        for i in range(N):
            if func is Middle_square:
                val = next(gen_mid)
            elif func is Linear_Congruential_Generator:
                val = next(gen_lcg)
            elif func is xorshift32:
                val = next(gen_xor)
            else:
                val = func(k)
            current_sum += val
            arr[k][i] = abs(0.5- current_sum/(i+1))
    
    err = [sum(errs)/M for errs in zip(*arr)]
    return err

def print_progress(ch):
    print(f"Finished: {ch}",file = sys.stderr)

err_expected = [1/math.sqrt(6*math.pi*n) for n in Ns]
err_m = gen_err_avg(mersenne_twister)
print_progress("Mersenne Twister")
err_mid = gen_err_avg(Middle_square)
print_progress("Middle Square")
err_lcg = gen_err_avg(Linear_Congruential_Generator)
print_progress("Linear Congruential Generator")
err_xor = gen_err_avg(xorshift32)
print_progress("XORshift")

tmp = 1
Xray = []
while 10**tmp <= N:
    Xray.append(int(10**tmp))
    tmp += 1.0

fig = plt.figure()
ax = plt.subplot(1,1,1)
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xticks(Xray)
ax.set_xticklabels(Xray,rotation=45, ha='right')
ax.set_title("Quality of Rondom Number vs Monte Carlo (x,y log ver.)")

ax.plot(Ns,err_expected,label = "expected 1/√6nπ",linestyle="dotted")
ax.plot(Ns,err_m,label = "Mersenne twister")
ax.plot(Ns,err_mid,label = "Middle Square")
ax.plot(Ns,err_lcg,label = "Linear Congruential Generator")
ax.plot(Ns,err_xor,label = "XORshift32")
ax.set_xlabel("Iteration count (log)")
ax.set_ylabel("Absolute difference from the expected value (log)")
ax.legend()
ax.grid()
plt.show()
