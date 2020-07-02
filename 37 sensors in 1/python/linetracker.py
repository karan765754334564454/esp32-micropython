import time
from machine import Pin, ADC, PWM

pin_linetracker = Pin(21, Pin.IN)

while True:
  linetracker_value = pin_linetracker.value()
  if (linetracker_value == 0):
    print('Line not found')
  else:
    print('Line found')
  time.sleep(0.01)
