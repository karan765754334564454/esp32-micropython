import time
from machine import Pin, ADC

pin_audio_analog = Pin(34, Pin.IN)
adc_audio_analog = ADC(pin_audio_analog)
adc_audio_analog. atten(ADC.ATTN_11DB) #Read voltages between 0.0v to 3.6v
adc_audio_analog.width(ADC.WIDTH_12BIT)

pin_audio_digital = Pin(21, Pin.IN)
while True:
  adc_audio_analog_value = adc_audio_analog.read()
  audio_digital_value = pin_audio_digital.value()
  print('A0 =', adc_audio_analog_value, ', D0 =', audio_digital_value)
  if (audio_digital_value == 0):
    print('Audio value above threshold')
  time.sleep(0.01)