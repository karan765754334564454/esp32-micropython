import time
from machine import Pin, ADC

inputPin = Pin(34, Pin.IN)
inputADC = ADC(inputPin)
inputADC.atten(ADC.ATTN_11DB) #Read voltages between 0.0v to 3.6v

while True:
  inputValue = inputADC.read()
  if (inputValue > 0):
    print('Object in gap detected. A0 =', inputValue)
  time.sleep(0.01)
