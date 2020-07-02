import time
from machine import Pin, ADC

inputPin = Pin(34, Pin.IN) #GPIO 34 is input only, also has an ADC

previousValue = 1
while True:
  inputValue = inputValue.value()
  if inputValue == 1 and previousValue == 0:
    print('Shock detected')
  previousValue = inputValue
  time.sleep(0.01)
