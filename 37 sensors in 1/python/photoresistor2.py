import time
from machine import Pin, ADC, PWM

pin_photoresistor = Pin(34, Pin.IN)
adc_photoresistor = ADC(pin_photoresistor)
adc_photoresistor. atten(ADC.ATTN_11DB) #Read voltages between 0.0v to 3.6v
adc_photoresistor.width(ADC.WIDTH_12BIT)

while True:
  adc_photoresistor_value = adc_photoresistor.read()
  if (adc_photoresistor_value > 0):
    print('Light detected. A0 =', adc_photoresistor_value)
  else:
    print('No light detected.')
  time.sleep(0.01)
