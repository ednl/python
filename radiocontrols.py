#!/usr/bin/env python3

from dothat import touch, lcd, backlight
import re, signal, time, subprocess

findnum = re.compile(r"\d+")
index = 0
stations = []
with open("/home/pi/radio.txt") as file:
	for line in file:
		stations.append(line.split()[0])

def reset():
	backlight.set_graph(0)
	backlight.off()
	lcd.clear()

def line(row, txt):
	lcd.set_cursor_position(0, row)
	lcd.write("{:16}".format(txt))

def show_volume():
	volume = subprocess.check_output("mpc volume", shell=True, universal_newlines=True).strip().capitalize()
	line(1, volume)

	percent = float(findnum.search(volume).group()) / 100
	backlight.set_graph(percent)

	time.sleep(1)
	backlight.set_graph(0)

def show_all():
	global index
	backlight.rgb(255, 255, 255)

	station = subprocess.check_output("station", universal_newlines=True).strip()
	try:
		index = stations.index(station)
	except ValueError:
		index = 0
	line(0, "Stream: " + station)

	snooze = subprocess.check_output("snooze", universal_newlines=True).strip()
	line(2, "Snooze: " + snooze)

	show_volume()
	backlight.off()

def tune():
	if 0 <= index < len(stations):
		subprocess.call("piradio " + stations[index], shell=True)
	show_all()

# Volume up
@touch.on(touch.UP)
def press_up(channel, event):
	subprocess.call("piradio vol +", shell=True)
	show_volume()

# Volume down
@touch.on(touch.DOWN)
def press_down(channel, event):
	subprocess.call("piradio vol -", shell=True)
	show_volume()

# Radio off
@touch.on(touch.CANCEL)
def press_cancel(channel, event):
	subprocess.call("piradio off", shell=True)
	reset()

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

show_all()
signal.pause()
