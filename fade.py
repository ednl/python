#!/usr/bin/env python3

import unicornhat as U
import atexit
from random import randrange
from time import sleep

def reset():
	U.rotation(0)
	U.brightness(0.2)
	U.off()

atexit.register(reset)

reset()
pix = []

while True:
	i = 0
	while i < len(pix):
		if pix[i]['dz'] == 0:
			del pix[i]
		else:
			pix[i]['z'] += pix[i]['dz']
			if pix[i]['z'] >= 255:
				pix[i]['z'] = 255
				pix[i]['dz'] *= -1
			elif pix[i]['z'] <= 0:
				pix[i]['z'] = 0
				pix[i]['dz'] = 0
			i += 1

	x = randrange(8)
	y = randrange(8)
	if U.get_pixel(x, y) == (0, 0, 0):
		dz = 1 + randrange(10)
		pix.append({'x': x, 'y': y, 'z': dz, 'dz': dz})

	for p in pix:
		U.set_pixel(p['x'], p['y'], p['z'], p['z'], p['z'])
	U.show()

	sleep(0.001)
