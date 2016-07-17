#!/usr/bin/env python3

from envirophat import leds, light, weather, motion
import time, datetime, os, sys

leds.off()
old = None
while True:

	# Hourly log files
	now = datetime.datetime.now()
	log = "/home/pi/envir/{:%F%H}.csv".format(now)
	if log != old:

		# Check free disk space
		disk = os.statvfs("/home/pi")
		freemb = disk.f_bsize * disk.f_bavail / 1024 / 1024
		if freemb < 512:
			sys.exit("envir.py: Low on disk space" + (", last log in " + old if old else "."))

		# Column headers on new log file
		if not os.path.isfile(log):
			with open(log, "w") as file:
				file.write("Date,Time,CPU,Temp,Press,Light,Red,Green,Blue,Heading,AccelX,AccelY,AccelZ\n")
			os.chown(log, 1000, 1000)

		old = log

	# Read CPU temperature in degrees Celsius
	with open("/sys/class/thermal/thermal_zone0/temp") as file:
		cputemp = float(file.read().strip()) / 1000

	# EnviroPhat measurements
	temperature = weather.temperature()
	pressure    = float(weather.pressure()) / 100
	lightflux   = light.light()
	r, g, b     = light.rgb()
	heading     = motion.heading()
	ax, ay, az  = motion.accelerometer()

	# Comma Separated Values
	csv = "{n:%F,%T},{c:.1f},{t:.1f},{p:.1f},{f},{r},{g},{b},{h:.0f},{x:.1f},{y:.1f},{z:.1f}\n".format(
		n = now,
		c = cputemp,
		t = temperature,
		p = pressure,
		f = lightflux,
		r = r, g = g, b = b,
		h = heading,
		x = ax, y = ay, z = az
	)

	# Append to log file
	with open(log, "a") as file:
		file.write(csv)

	# Wait 5 seconds => ~720 lines per hourly log file = ~40 KB
	time.sleep(5)
