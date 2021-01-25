# Random Fibonacci Sequence
# https://en.wikipedia.org/wiki/Random_Fibonacci_sequence
# https://www.numberphile.com/videos/random-fibonacci-numbers

import math
import random
random.seed()

viswanath = 1.131_988_248_794_3

n = div = 0
fib1 = fib2 = mod = 1
while (n < 1_000_000):
    tmp = fib1
    if random.randint(0, 1):
        fib1 += fib2
    else:
        fib1 -= fib2
    fib2 = tmp
    n += 1
    if n % mod == 0:
        if fib1:
            root = math.exp(math.log(abs(fib1)) / n)
            print(n, root, abs(root - viswanath))
        else:
            print(n, 0)
        div += 1
        if div == 9:
            mod *= 10
            div = 0
