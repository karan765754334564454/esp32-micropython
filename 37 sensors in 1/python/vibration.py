import time
from machine import Pin, ADC, PWM

inputPin = Pin(21, Pin.IN)
while True:
  inputValue = inputPin.value()
  if (inputValue == 1):
    print('Vibration detected.')
  time.sleep(0.01)
