#!/usr/bin/env python

from envirophat import light, weather, leds
import time, datetime, os, sys

old = None
while True:

	# Flash LEDs as an activity indicator
	leds.on()

	# Hourly log files
	now = datetime.datetime.now()
	log = "/home/pi/envir/{:%F%H}.csv".format(now)
	if log != old:

		# Check free disk space
		disk = os.statvfs("/home/pi")
		freemb = disk.f_bsize * disk.f_bavail / 1024 / 1024
		if freemb < 512:
			print("envir.py: Low on disk space" + (", last log in " + old if old else "."))
			sys.exit()

		# Column headers on new log file
		if !os.path.isfile(log):
			with open(log, "w") as file:
				file.write("Date,Time,CPU,Temp,Press,Light,Red,Green,Blue\n")

		old = log

	# Read CPU temperature, round to tenths of degrees Celsius
	with open("/sys/class/thermal/thermal_zone0/temp") as file:
		cpu = round(float(file.read().strip()) / 100) / 10

	# Comma Separated Values
	csv = "{d:%F,%T},{c:.1f},{t:.1f},{p:.0f},{x},{},{},{}".format(
		d = now,
		c = cpu,
		t = weather.temperature(),
		p = weather.pressure(),
		x = light.light(),
		*light.rgb()
	)

	# Append to log file
	with open(log, "a") as file:
		file.write(csv + "\n")

	# Wait 5 seconds = ~720 lines per log file
	leds.off()
	time.sleep(5)
