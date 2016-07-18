#!/usr/bin/env python3

from dothat import touch, lcd, backlight
import subprocess as SP
import signal, re

findnum = re.compile(r"\d+")

def clear():
        lcd.clear()
        backlight.off()
        backlight.set_graph(0)

def status():
        clear()

        lcd.set_cursor_position(0, 0)
        lcd.write("Stream: " + SP.check_output("station", universal_newlines=True).strip())

        lcd.set_cursor_position(0, 1)
        vol = SP.check_output("mpc volume", shell=True, universal_newlines=True).strip()
        lcd.write(vol.capitalize())
        val = float(findnum.search(vol).group()) / 100
        backlight.set_graph(val)

        lcd.set_cursor_position(0, 2)
        lcd.write("Snooze: " + SP.check_output("snooze", universal_newlines=True).strip())

status()

@touch.on(touch.UP)
def vol_up(channel, event):
        SP.call("piradio vol +", shell=True)
        status()

@touch.on(touch.DOWN)
def vol_down(channel, event):
        SP.call("piradio vol -", shell=True)
        status()

@touch.on(touch.CANCEL)
def radio_off(channel, event):
        SP.call("piradio off", shell=True)
        clear()

@touch.on(touch.BUTTON)
def radio_on(channel, event):
        SP.call("piradio fip", shell=True)
        status()

signal.pause()
