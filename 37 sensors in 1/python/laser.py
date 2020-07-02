import time
from machine import Pin

pin_laser_signal = Pin(21, Pin.OUT)
laser_state = False

while True:
  #Turn the laser on and off every second
  laser_state = not laser_state
  pin_laser_signal.value(laser_state)
  time.sleep(1)
