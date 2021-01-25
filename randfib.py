# Random Fibonacci Sequence
# https://en.wikipedia.org/wiki/Random_Fibonacci_sequence
# https://www.numberphile.com/videos/random-fibonacci-numbers

import math
import random
random.seed()

viswanath = 1.131_988_248_794_3

n = decade = 0
p = q = mod = 1
while (n < 1_000_000):
    tmp = p
    if random.randint(0, 1):
        p += q
    else:
        p -= q
    q = tmp
    n += 1
    if n % mod == 0:
        if p:
            root = math.exp(math.log(abs(p)) / n)
            print(n, root, abs(root - viswanath))
        else:
            print(n, p)
        decade += 1
        if decade == 9:
            mod *= 10
            decade = 0
