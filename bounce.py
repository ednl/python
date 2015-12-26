#!/usr/bin/env python3

import unicornhat as U
import atexit, random, math
from time import sleep

# Visual parameters
fade = 20	# min=1, max=255 (lower->longer trail, higher->shorter trail)
steps = 20	# min=1 (number of steps from current to next colour)

def reset():
	U.rotation(0)
	U.brightness(0.2)
	U.off()

# Turn pixels off when program is stopped with Ctrl-C
atexit.register(reset)

reset()		# Start with blank canvas
xmin = 0	# pixel grid dimensions
xmax = 7
ymin = 0
ymax = 7

def nextcolour():
	# set at least one colour component "on"
	rgb = random.randint(1, 7)
	return (rgb & 1, (rgb & 2) >> 1, (rgb & 4) >> 2)

def nextspeed():
	# three possible speeds
	return 0.75 + random.randrange(3) * 0.25

def nextangle(sector):
	# sectors are 90 degrees = pi/2 wide
	return (random.random() + sector) * math.pi / 2

# Start in bottom left corner, random angle 0 - 90 degrees
x = xmin
y = ymin
speed = nextspeed()
angle = nextangle(0)
dx = speed * math.cos(angle)
dy = speed * math.sin(angle)

# Initial head of the trail
trail = []
trail.append({'pos': (0, 0), 'lum': 255})
U.set_pixel(0, 0, 255, 255, 255)
U.show()

curcolour = (1, 1, 1)
nxtcolour = curcolour
colourstep = 0

while True:
	x += dx
	y += dy
	# test for boundary
	if x < xmin or x > xmax or y < ymin or y > ymax:
		# bounce with new random speed and angle
		speed = nextspeed()
		if x < xmin and y < ymin:
			# bottom left corner, 0-90 degrees
			x = xmin
			y = ymin
			angle = nextangle(0)
		elif x > xmax and y < ymin:
			# bottom right corner, 90-180 degrees
			x = xmax
			y = ymin
			angle = nextangle(1)
		elif x > xmax and y > ymax:
			# top right corner, 180-270 degrees
			x = xmax
			y = ymax
			angle = nextangle(2)
		elif x < xmin and y > ymax:
			# top left corner, 270-360 degrees
			x = xmin
			y = ymax
			angle = nextangle(3)
		elif y < ymin:
			# bottom edge, 45-135 degrees
			y = ymin
			angle = nextangle(0.5)
		elif x > xmax:
			# right edge, 135-225 degrees
			x = xmax
			angle = nextangle(1.5)
		elif y > ymax:
			# top edge, 225-315 degrees
			y = ymax
			angle = nextangle(2.5)
		elif x < xmin:
			# left edge, 315-405 degrees (405=45)
			x = xmin
			angle = nextangle(3.5)

		dx = speed * math.cos(angle)
		dy = speed * math.sin(angle)

	# integer coordinates
	p = int(math.floor(x + 0.5))	# only correct if xmin >= 0
	q = int(math.floor(y + 0.5))	# only correct if ymin >= 0
	# test if new pixel needs to be lit
	if (p, q) != trail[-1]['pos']:
		i = 0
		while i < len(trail):
			if trail[i]['lum'] == 0:
				# pixel was off, now delete from list
				del trail[i]
				# no need to increment i (should probably use deque instead of list)
			else:
				# attenuate currently lit pixels
				trail[i]['lum'] -= fade
				if trail[i]['lum'] < 0:
					# switch off, delete on next iteration
					trail[i]['lum'] = 0
				i += 1

		# add new head to the trail
		trail.append({'pos': (p, q), 'lum': 255})

	# cycle colour
	frac = colourstep / steps
	r = curcolour[0] + (nxtcolour[0] - curcolour[0]) * frac
	g = curcolour[1] + (nxtcolour[1] - curcolour[1]) * frac
	b = curcolour[2] + (nxtcolour[2] - curcolour[2]) * frac
	colourstep += 1
	if colourstep > steps:
		colourstep = 0
		curcolour = nxtcolour
		nxtcolour = nextcolour()

	# show complete trail
	for a in trail:
		U.set_pixel(a['pos'][0], a['pos'][1],
			int(r * a['lum']),
			int(g * a['lum']),
			int(b * a['lum']))
	U.show()

	# good value for RPi B+ = 0.05
	sleep(0.05)
