#touch sensor

#D0 goes high when touch, low when not touched

#not sure about A0
import math
import time
from machine import Pin, ADC, PWM

#AO
pin_analog = Pin(34, Pin.IN)
adc_analog = ADC(pin_analog)
#Maybe disable this 
adc_analog.atten(ADC.ATTN_11DB) #Read voltages between 0.0v to 3.6v
adc_analog.width(ADC.WIDTH_9BIT)

#D0
pin_digital = Pin(21, Pin.IN)

pin_LED = Pin(19, Pin.OUT)

while True:
  
  adc_value = adc_analog.read()
  digital_value = pin_digital.value()
  
  Temp = math.log((10240000/adc_value)-10000)
  Temp = 1/(0.001129148+(0.000234125+(0.0000000876741*Temp*Temp ))*Temp);
  Temp = Temp - 273.15
  
  if (adc_value != 4095):
    print('A0 =', adc_value, ', D0 =', digital_value, ', Temp =', Temp)
  
  
  if (digital_value == 1):
    pin_LED.value(1)
  else:
    pin_LED.value(0)
    
  time.sleep(1.0/100)

