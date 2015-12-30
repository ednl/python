#!/usr/bin/env python3

import unicornhat as UH
import atexit, random
from time import sleep

def reset():
	UH.rotation(0)
	UH.brightness(0.2)
	UH.off()

# Turn lights off when program is stopped with Ctrl-C
atexit.register(reset)

reset()			# Start with blank canvas
colour = True	# True = use colour, False = white pixels
blink = []		# List of currently blinking pixels

def fade(p):
	# Blink speed different for every light
	p['z'] += p['dz']
	# Check min/max
	if p['z'] >= 255:
		# Reverse from fade in to fade out
		p['z'] = 255
		p['dz'] *= -1
	elif p['z'] <= 0:
		# Done, turn off pixel
		p['z'] = 0
		p['dz'] = 0
	return(p)

while True:
	# Remove from list if turned off (dz == 0)
	blink = filter(lambda p: p['dz'], blink)
	# Update brightness
	blink = list(map(fade, blink))

	# Try to add a blinky light
	x, y = random.randrange(8), random.randrange(8)
	# But only if this pixel is currently off
	if UH.get_pixel(x, y) == (0, 0, 0):
		# Blink speed (step size from 0 to 255 and back)
		dz = random.randint(1, 10)
		if colour:
			# RGB vector composed of 3 fractions 0..1
			# Fractions limited to range 0.6-1.0 to keep it bright
			# Step size 0.2 for "web palette"
			c = tuple(map(lambda i: random.randint(3, 5) / 5, range(3)))
		else:
			# White
			c = (1, 1, 1)
		blink.append({'x': x, 'y': y, 'z': dz, 'dz': dz, 'c': c})

	# Draw pixels
	for p in blink:
		rgb = tuple(map(lambda c: int(c * p['z']), p['c']))
		UH.set_pixel(p['x'], p['y'], *rgb)
	UH.show()

	# Uncomment and increase value for slower blinking
	#sleep(0.01)
