#!/usr/bin/env python3

import unicornhat as UH
import atexit, math, random
from time import sleep

def reset():
	UH.rotation(0)
	UH.brightness(0.2)
	UH.off()

# Begin and end with clear display
reset()
atexit.register(reset)

# Colour definition as on/off RGB tuple
# e.g. (1,0,0) = red
def rgb(n = 0):
	if n < 1 or n > 7:
		n = random.randint(1, 6)
	r = (n & 4) >> 2
	g = (n & 2) >> 1
	b = n & 1
	return (r, g, b)

# Get display coordinates from angle in radians
def pixel(angle):
	return int(round(3.5 + 3.5 * math.sin(angle)))

# Factor used in angular speed step,
# also used for sleep in seconds
step = 0.01

# Parameters for speed and colour change
# x-y phase change preserved if loops * step = integer
loop1, loop2 = 0, 0
speedloops, colourloops = 400, 100

# Initial angles, speeds and colours
circle = math.pi * 2
ax, ay = 0, circle / 4
dx, dy = circle * step, circle * step
cx, cy = (1, 0, 0), (0, 0, 1)
x0, y0 = 0, 0

# Endless loop, stop with Ctrl-C
while True:

	# Locate next scan lines
	x1 = pixel(ax)
	y1 = pixel(ay)

	# Erase previous, draw next scan lines
	kx = tuple(map(lambda k: k * 153, cx))
	ky = tuple(map(lambda k: k * 153, cy))
	for i in range(8):
		UH.set_pixel(i, y0, 0, 0, 0)
		UH.set_pixel(x0, i, 0, 0, 0)
		UH.set_pixel(i, y1, *kx)
		UH.set_pixel(x1, i, *ky)

	# Highlight the intersection
	UH.set_pixel(x1, y1, 255, 255, 255)

	# Remember previous scan lines
	x0, y0 = x1, y1

	# Update display
	UH.show()
	sleep(step)

	# Next angles
	ax += dx
	ay += dy

	# Keep track of time, sort of
	loop1 += 1
	loop2 += 1

	# Change speed every 'speedloops' loops
	if loop1 == speedloops:
		loop1 = 0
		# Preserve angles whilst making sure they don't lose precision
		ax %= circle
		ay %= circle
		# Random speeds, two values from (1,2,3)
		dx, dy = map(lambda i: random.randint(1, 3) * circle * step, range(2))

	# Change colour every 'colourloops' loops
	if loop2 == colourloops:
		loop2 = 0
		# Pick two different colours but not black or white
		cx, cy = map(rgb, random.sample(range(1, 7), 2))
