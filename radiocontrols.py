#!/usr/bin/env python3

##### Imports ###############

from dothat import touch, lcd, backlight
import re, signal, time, subprocess, threading

##### Globals ###############

# To extract numbers from "mpc volume" command output
findnum = re.compile(r"\d+")

# Read station IDs
index = 0
stations = []
with open("/home/pi/radio.txt") as file:
	for line in file:
		stations.append(line.split()[0])

##### Functions ###############

# Write to LCD
def line(row, txt):
	lcd.set_cursor_position(0, row)
	lcd.write("{:16}".format(txt))

# Avoid dealing with Timer function arguments
def leds_off():
	backlight.set_graph(0)

# Update LCD text and LED graph
def show():
	global index

	# Turn on LCD backlight, set timer to turn off
	backlight.rgb(255, 255, 255)
	t1 = threading.Timer(4.0, backlight.off)
	t1.start()

	# Get radio info
	station = subprocess.check_output("station", universal_newlines=True).strip()
	volume = subprocess.check_output("mpc volume", shell=True, universal_newlines=True).strip().capitalize()
	snooze = subprocess.check_output("snooze", universal_newlines=True).strip()

	# Update LCD text
	line(0, "Stream: " + station)
	line(1, volume)
	line(2, "Snooze: " + snooze)

	# Turn on LED graph, set timer to turn off
	percent = float(findnum.search(volume).group()) / 100
	backlight.set_graph(percent)
	t2 = threading.Timer(1.5, leds_off)
	t2.start()

	# Update station index (set on first run)
	try:
		index = stations.index(station)
	except ValueError:
		index = 0

# Tune radio to station, update info
def tune():
	if 0 <= index < len(stations):
		subprocess.call("piradio " + stations[index], shell=True)
	show()

##### Hooks ###############

# Volume up
@touch.on(touch.UP)
def press_up(channel, event):
	subprocess.call("piradio vol +", shell=True)
	show()

# Volume down
@touch.on(touch.DOWN)
def press_down(channel, event):
	subprocess.call("piradio vol -", shell=True)
	show()

# Radio off
@touch.on(touch.CANCEL)
def press_cancel(channel, event):
	subprocess.call("piradio off", shell=True)
	backlight.set_graph(0)
	backlight.off()
	lcd.clear()

# Radio on
@touch.on(touch.BUTTON)
def press_button(channel, event):
	tune()

# Previous station
@touch.on(touch.LEFT)
def press_left(channel, event):
	global index
	index -= 1
	if index < 0:
		index = len(stations) - 1
	tune()

# Next station
@touch.on(touch.RIGHT)
def press_right(channel, event):
	global index
	index += 1
	if index >= len(stations):
		index = 0
	tune()

##### Main ###############

# Initial update
show()

# Suspend program while keeping touch controls active
signal.pause()
