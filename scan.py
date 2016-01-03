#!/usr/bin/env python3

import unicornhat as UH
import atexit, math, random
from time import sleep

def reset():
    UH.rotation(0)
    UH.brightness(0.2)
    UH.off()

reset()
atexit.register(reset)

def rgb(n = 0):
    if n < 1 or n > 7:
        n = random.randint(1, 6)
    r = (n & 4) >> 2
    g = (n & 2) >> 1
    b = n & 1
    return (r, g, b)

def pixel(angle):
    return int(round(3.5 + 3.5 * math.sin(angle)))

circle = math.pi * 2
time = 0
step = 0.01
x0, y0 = 0, 0

ax, ay = random.random() * circle, random.random() * circle
vx, vy = random.randint(1, 3) * circle * step,
    random.randint(1, 3) * circle * step
cx, cy = rgb(), rgb()

while True:

    x1 = pixel(ax)
    y1 = pixel(ay)
    for x in range(8):
        UH.set_pixel(x, y0, 0, 0, 0)
        UH.set_pixel(x, y1, *map(lambda i: i * 153, cx))
    for y in range(8):
        UH.set_pixel(x0, y, 0, 0, 0)
        UH.set_pixel(x1, y, *map(lambda i: i * 153, cy))
    UH.set_pixel(x1, y1, 255, 255, 255)
    x0 = x1
    y0 = y1
    UH.show()
    sleep(step)

    time += step
    ax += vx
    ay += vy

    if time >= 5:
        time = 0
        ax %= circle
        ay %= circle
        vx, vy = random.randint(1, 3) * circle * step,
            random.randint(1, 3) * circle * step
        cx, cy = rgb(), rgb()
