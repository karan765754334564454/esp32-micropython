import time
from machine import Pin, ADC, PWM

pin_CLK = Pin(35, Pin.IN) #GPIO 34 is input only, also has an ADC
pin_DDT = Pin(34, Pin.IN) #GPIO 34 is input only, also has an ADC

prev_clk_value = 0

while True:
  #Get the digital values from the rotary encoder
  clk_value = pin_CLK.value()
  ddt_value = pin_DDT.value()
  #If the clk value is different from the previous clk value, a rotation has occured.
  if prev_clk_value != clk_value:
    print('Rotation occured.')
    if clk_value != ddt_value:
      print('Clockwise rotation')
    else:
      print('Anticlockwise rotation')
  #Update the previous values for the next tick
  prev_clk_value = clk_value
  time.sleep(0.01)
