import time
from machine import Pin, ADC, PWM

inputPin = Pin(34, Pin.IN) #GPIO 34 is input only
while True:
  inputValue = inputPin.value()
  if (inputValue == 0):
    print('Upright.')
  else:
    print('Upside down.')
  time.sleep(0.01)
