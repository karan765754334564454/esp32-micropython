import time
from machine import Pin, ADC, PWM

pin_LED_R = Pin(21, Pin.OUT)
pin_LED_G = Pin(19, Pin.OUT)
pin_LED_B = Pin(18, Pin.OUT)

pwm_LED_R = PWM(pin_LED_R)
pwm_LED_G = PWM(pin_LED_G)
pwm_LED_B = PWM(pin_LED_B)

while True:
  pwm_LED_R.duty(1023)
  pwm_LED_G.duty(1023)
  pwm_LED_B.duty(1023)
  time.sleep(0.01)



