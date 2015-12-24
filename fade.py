#!/usr/bin/env python3

import unicornhat as U
import atexit, random
from time import sleep

def reset():
	U.rotation(0)
	U.brightness(0.2)
	U.off()

# Turn pixels off when program is stopped with Ctrl-C
atexit.register(reset)

colour = True	# True = use colour, False = white pixels
reset()			# Start with blank canvas
pix = []		# List of currently fading pixels

while True:
	# Update fading pixel data
	i = 0
	while i < len(pix):
		if pix[i]['dz'] == 0:
			# Done at prev iteration, now delete
			del pix[i]
			# No need to increment i
		else:
			# Fade in or out at dz speed
			pix[i]['z'] += pix[i]['dz']
			# Check for extreme values
			if pix[i]['z'] >= 255:
				# Reverse from fade in to fade out
				pix[i]['z'] = 255
				pix[i]['dz'] *= -1
			elif pix[i]['z'] <= 0:
				# Done, turn off pixel
				pix[i]['z'] = 0
				pix[i]['dz'] = 0
			# Next pixel in the list
			i += 1

	# Try to start a new fading pixel
	x = random.randrange(8)
	y = random.randrange(8)
	# But only if this pixel is currently off
	if U.get_pixel(x, y) == (0, 0, 0):
		# Fade speed (step size from 0 to 255 and back)
		dz = random.randint(1, 10)
		if colour:
			# RGB fractions
			# range from 0.6 to 1 to keep it bright
			# step size 0.2 for "web palette"
			c = (random.randint(3, 5) / 5,
				 random.randint(3, 5) / 5,
				 random.randint(3, 5) / 5)
		else:
			# White
			c = (1, 1, 1)
		pix.append({'x': x, 'y': y, 'z': dz, 'dz': dz, 'c': c})

	# Draw pixels
	for p in pix:
		U.set_pixel(p['x'], p['y'],
			int(p['c'][0] * p['z']),
			int(p['c'][1] * p['z']),
			int(p['c'][2] * p['z']))
	U.show()

	# Uncomment and increase value for slower fade (or for RPi2)
	#sleep(0.05)
