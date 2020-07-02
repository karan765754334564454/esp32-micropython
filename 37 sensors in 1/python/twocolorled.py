import time
from machine import Pin, ADC, PWM

pin_LED_1 = Pin(21, Pin.OUT)
pin_LED_2 = Pin(19, Pin.OUT)

pwm_LED_1 = PWM(pin_LED_1)
pwm_LED_2 = PWM(pin_LED_2)

duty_LED_1 = int(1024/2) #50%
duty_LED_2 = int(1024/2) #50%

while True:
  pwm_LED_1.duty(duty_LED_1)
  pwm_LED_2.duty(duty_LED_2)
  time.sleep(0.01)
