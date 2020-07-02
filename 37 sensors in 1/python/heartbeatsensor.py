import time
from machine import Pin, ADC, PWM

inputPin = Pin(34, Pin.IN)
inputADC = ADC(inputPin)
inputADC.atten(ADC.ATTN_11DB)

while True:
  inputValue = inputADC.read()
  print('A0 =', inputValue)
  time.sleep(0.01)
