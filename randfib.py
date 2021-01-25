# Random Fibonacci Sequence
# https://en.wikipedia.org/wiki/Random_Fibonacci_sequence
# https://www.numberphile.com/videos/random-fibonacci-numbers

import math
import random
random.seed()

v = 1.131_988_248_794_3

i = j = 0
p = q = m = 1
while (i < 1_000_000):
    t = p
    if random.randint(0, 1) == 0:
        p += q
    else:
        p -= q
    q = t
    i += 1
    if i % m == 0:
        if p != 0:
            r = math.exp(math.log(abs(p)) / i)
            print(i, r, abs(r - v))
        else:
            print(i, p)
        j += 1
        if j == 9:
            m *= 10
            j = 0
