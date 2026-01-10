#!/usr/bin/env python3

# Zeckendorf's theorem = "base fibonacci"
# https://en.wikipedia.org/wiki/Zeckendorf%27s_theorem
# Numberphile with Tony Padilla:
#   https://www.youtube.com/watch?v=S5FTe5KP2Cw

end = 100
fib = [1, 2]
while True:
    next = sum(fib[-2:])
    if next >= end:
        break
    fib.append(next)

zeck = [[] for _ in range(len(fib))]
for n in range(1, end):
    x = n
    for i in range(len(fib))[::-1]:
        if fib[i] <= x:
            zeck[i].append(n)
            x -= fib[i]

for i in range(len(fib)):
	print(zeck[i])
