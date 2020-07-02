import time
from machine import Pin, ADC, PWM

pin_analog = Pin(34, Pin.IN)
adc_analog = ADC(pin_analog)
adc_analog.atten(ADC.ATTN_11DB) #Read voltages between 0.0v to 3.6v
adc_analog.width(ADC.WIDTH_12BIT) #12 bit width so ADC values between 0 ~ 4095

pin_digital = Pin(21, Pin.IN)
while True:
  adc_value = adc_analog.read()
  digital_value = pin_digital.value()
  if (adc_value != 1970):
    print('Magnetic field detected. A0 =', adc_value)
  if (digital_value == 1):
    print('Magnetic field value is above threshold)
  time.sleep(1.0/100)

