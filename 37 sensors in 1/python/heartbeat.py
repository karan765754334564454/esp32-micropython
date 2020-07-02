import time
from machine import Pin, ADC

inputPin = Pin(34, Pin.IN)
inputADC = ADC(inputPin)
inputADC.atten(ADC.ATTN_11DB)

a = 0.75
c = 0.0

oldVal = 0
oldC = 0

while True: 
  rawVal = inputADC.read()
  val = a*oldVal+(1-a)*rawVal
 
  c = val - oldVal
  
  temp = (c < 0.0 and oldC >0.0)
  
  if temp:
    print("Beat")
  else:
    print(".")
    
  oldVal = val
  oldC = c
  
  time.sleep(0.01)
