import time
from machine import Pin, ADC, PWM

pin_digital = Pin(21, Pin.IN)
while True:
  if (digital_value == 1):
    print('Sensor touched.')
  time.sleep(0.01)

