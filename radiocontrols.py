#!/usr/bin/env python3

from dothat import touch, lcd, backlight
import re, signal, time, subprocess

findnum = re.compile(r"\d+")
station = 0
stations = []
with open("/home/pi/radio.txt") as file:
	for line in file:
		stations.append(line.split()[0])

def clear_all():
	backlight.set_graph(0)
	backlight.off()
	lcd.clear()

def lcd_out(row, txt):
	lcd.set_cursor_position(0, row)
	lcd.write("{:16}".format(txt))

def adj_vol():
	volume = subprocess.check_output("mpc volume", shell=True, universal_newlines=True).strip().capitalize()
	percent = float(findnum.search(volume).group()) / 100

	lcd_out(1, volume)
	backlight.set_graph(percent)

	time.sleep(1)
	backlight.set_graph(0)

def full_status():
	backlight.rgb(255, 255, 255)

	stream = "Stream: " + subprocess.check_output("station", universal_newlines=True).strip()
	lcd_out(0, stream)

	snooze = "Snooze: " + subprocess.check_output("snooze", universal_newlines=True).strip()
	lcd_out(2, snooze)

	adj_vol()
	backlight.off()

# Volume up
@touch.on(touch.UP)
def press_up(channel, event):
	subprocess.call("piradio vol +", shell=True)
	adj_vol()

# Volume down
@touch.on(touch.DOWN)
def press_down(channel, event):
	subprocess.call("piradio vol -", shell=True)
	adj_vol()

# Radio off
@touch.on(touch.CANCEL)
def press_cancel(channel, event):
	subprocess.call("piradio off", shell=True)
	clear_all()

# Radio on
@touch.on(touch.BUTTON)
def press_button(channel, event):
	if 0 <= station < len(stations):
		subprocess.call("piradio " + stations[station], shell=True)
	full_status()

# Previous station
@touch.on(touch.LEFT)
def press_left(channel, event):
	global station
	station -= 1
	if station < 0:
		station = len(stations) - 1
	if 0 <= station < len(stations):
		subprocess.call("piradio " + stations[station], shell=True)
	full_status()

# Next station
@touch.on(touch.RIGHT)
def press_right(channel, event):
	global station
	station += 1
	if station >= len(stations):
		station = 0
	if 0 <= station < len(stations):
		subprocess.call("piradio " + stations[station], shell=True)
	full_status()

full_status()
signal.pause()
